#!/usr/bin/env python3
"""Python workspace policy audits used by emulebb-build validation."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from policy_guards import run_clean_worktree_guard


@dataclass(frozen=True)
class GitResult:
    """Captured Git command output."""

    returncode: int
    lines: tuple[str, ...]

    @property
    def text(self) -> str:
        """Returns stdout as a trimmed newline-joined string."""

        return "\n".join(self.lines).strip()


def workspace_root_from_env() -> Path:
    """Returns the canonical workspace root from EMULEBB_WORKSPACE_ROOT."""

    value = os.environ.get("EMULEBB_WORKSPACE_ROOT", "")
    if not value.strip():
        raise RuntimeError("EMULEBB_WORKSPACE_ROOT is required.")
    return Path(value).resolve()


def resolve_workspace_path(root: Path, relative_path: str) -> Path:
    """Resolves one workspace-relative path."""

    return (root / relative_path).resolve()


def run_git(repo_root: Path, args: Sequence[str], *, allow_failure: bool = False) -> GitResult:
    """Runs Git and captures stdout lines."""

    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    if completed.returncode != 0 and not allow_failure:
        raise RuntimeError(f"git {' '.join(args)} failed for '{repo_root}'.")
    lines = tuple(line for line in completed.stdout.splitlines() if line.strip())
    return GitResult(returncode=completed.returncode, lines=lines)


def read_text(path: Path) -> str:
    """Reads a required text file."""

    if not path.is_file():
        raise RuntimeError(f"Required file is missing: {path}")
    return path.read_text(encoding="utf-8")


def assert_contains(path: Path, pattern: str, reason: str) -> None:
    """Requires one regex pattern in a file."""

    if not re.search(pattern, read_text(path), re.MULTILINE):
        raise RuntimeError(reason)


def assert_not_contains(path: Path, pattern: str, reason: str) -> None:
    """Rejects one regex pattern in a file."""

    if re.search(pattern, read_text(path), re.MULTILINE | re.IGNORECASE):
        raise RuntimeError(reason)


def local_name(tag: str) -> str:
    """Returns the XML local name without a namespace."""

    return tag.rsplit("}", 1)[-1]


def direct_children(element: ET.Element, name: str) -> list[ET.Element]:
    """Returns direct XML children by local name."""

    return [child for child in list(element) if local_name(child.tag) == name]


def first_child(element: ET.Element, name: str) -> ET.Element | None:
    """Returns the first direct child by local name."""

    matches = direct_children(element, name)
    return matches[0] if matches else None


def child_text(element: ET.Element, name: str) -> str:
    """Returns direct child text or an empty string."""

    child = first_child(element, name)
    return (child.text or "").strip() if child is not None else ""


def load_project_xml(root: Path, relative_path: str) -> ET.Element:
    """Loads a required Visual Studio project XML document."""

    path = resolve_workspace_path(root, relative_path)
    if not path.is_file():
        raise RuntimeError(f"Required project file not found: {path}")
    return ET.parse(path).getroot()


def property_group(project: ET.Element, condition: str) -> ET.Element | None:
    """Finds a PropertyGroup by exact Condition."""

    for group in direct_children(project, "PropertyGroup"):
        if group.attrib.get("Condition") == condition:
            return group
    return None


def item_definition_group(project: ET.Element, condition: str) -> ET.Element | None:
    """Finds an ItemDefinitionGroup by exact Condition."""

    for group in direct_children(project, "ItemDefinitionGroup"):
        if group.attrib.get("Condition") == condition:
            return group
    return None


def assert_value(project_label: str, condition: str, property_name: str, actual_value: str, expected_value: str) -> None:
    """Checks one policy value."""

    if not actual_value.strip():
        raise RuntimeError(f"{project_label} is missing {property_name} for {condition}")
    if actual_value != expected_value:
        raise RuntimeError(f"{project_label} has {property_name}={actual_value} for {condition}, expected {expected_value}")


def assert_property_group_value(project: ET.Element, label: str, condition: str, property_name: str, expected_value: str) -> None:
    """Checks one PropertyGroup value."""

    group = property_group(project, condition)
    if group is None:
        raise RuntimeError(f"{label} is missing PropertyGroup for {condition}")
    assert_value(label, condition, property_name, child_text(group, property_name), expected_value)


def assert_cl_compile_value(project: ET.Element, label: str, condition: str, property_name: str, expected_value: str) -> None:
    """Checks one ClCompile setting."""

    group = item_definition_group(project, condition)
    compile_group = first_child(group, "ClCompile") if group is not None else None
    if compile_group is None:
        raise RuntimeError(f"{label} is missing ClCompile settings for {condition}")
    assert_value(label, condition, property_name, child_text(compile_group, property_name), expected_value)


def assert_link_value(project: ET.Element, label: str, condition: str, property_name: str, expected_value: str) -> None:
    """Checks one Link setting."""

    group = item_definition_group(project, condition)
    link_group = first_child(group, "Link") if group is not None else None
    if link_group is None:
        raise RuntimeError(f"{label} is missing Link settings for {condition}")
    assert_value(label, condition, property_name, child_text(link_group, property_name), expected_value)


def assert_app_multi_processor_compilation(project: ET.Element, condition: str) -> None:
    """Checks app MultiProcessorCompilation, including the ARM64 exception."""

    group = item_definition_group(project, condition)
    compile_group = first_child(group, "ClCompile") if group is not None else None
    if compile_group is None:
        raise RuntimeError(f"emule.vcxproj is missing ClCompile settings for {condition}")
    nodes = direct_children(compile_group, "MultiProcessorCompilation")
    if len(nodes) == 1:
        assert_value("emule.vcxproj", condition, "MultiProcessorCompilation", (nodes[0].text or "").strip(), "true")
        return
    if len(nodes) != 2:
        raise RuntimeError(f"emule.vcxproj has unexpected MultiProcessorCompilation entries for {condition}")
    by_condition = {node.attrib.get("Condition", ""): node for node in nodes}
    non_arm64 = by_condition.get("'$(Platform)'!='ARM64'")
    arm64 = by_condition.get("'$(Platform)'=='ARM64'")
    if non_arm64 is None or arm64 is None:
        raise RuntimeError(f"emule.vcxproj ARM64 MultiProcessorCompilation exception is missing required platform conditions for {condition}")
    assert_value("emule.vcxproj", condition, "MultiProcessorCompilation non-ARM64", (non_arm64.text or "").strip(), "true")
    assert_value("emule.vcxproj", condition, "MultiProcessorCompilation ARM64", (arm64.text or "").strip(), "false")


def assert_no_project_configuration(project: ET.Element, label: str, child_name: str, forbidden_value: str) -> None:
    """Rejects one project configuration platform or configuration value."""

    for item_group in direct_children(project, "ItemGroup"):
        for project_configuration in direct_children(item_group, "ProjectConfiguration"):
            if child_text(project_configuration, child_name) == forbidden_value:
                raise RuntimeError(f"{label} still declares {forbidden_value} project configurations")


def audit_build_policy(root: Path) -> None:
    """Runs active build policy checks."""

    app_debug = "'$(Configuration)'=='Debug'"
    app_release = "'$(Configuration)'=='Release'"
    tests_debug = "'$(Configuration)|$(Platform)'=='Debug|x64'"
    tests_release = "'$(Configuration)|$(Platform)'=='Release|x64'"
    tests_debug_arm64 = "'$(Configuration)|$(Platform)'=='Debug|ARM64'"
    tests_release_arm64 = "'$(Configuration)|$(Platform)'=='Release|ARM64'"
    tests_debug_build = "'$(Configuration)'=='Debug'"
    tests_release_build = "'$(Configuration)'=='Release'"
    id3_debug_x64 = "'$(Configuration)|$(Platform)'=='Debug|x64'"
    id3_debug_arm64 = "'$(Configuration)|$(Platform)'=='Debug|ARM64'"
    id3_release_x64 = "'$(Configuration)|$(Platform)'=='Release|x64'"
    id3_release_arm64 = "'$(Configuration)|$(Platform)'=='Release|ARM64'"
    resizable_debug_x64 = "'$(Configuration)|$(Platform)'=='Debug|x64'"
    resizable_debug_arm64 = "'$(Configuration)|$(Platform)'=='Debug|ARM64'"
    resizable_release_x64 = "'$(Configuration)|$(Platform)'=='Release|x64'"
    resizable_release_arm64 = "'$(Configuration)|$(Platform)'=='Release|ARM64'"
    miniupnp_debug_x64 = "'$(Configuration)|$(Platform)'=='Debug|x64'"
    miniupnp_debug_arm64 = "'$(Configuration)|$(Platform)'=='Debug|ARM64'"
    miniupnp_release_x64 = "'$(Configuration)|$(Platform)'=='Release|x64'"
    miniupnp_release_arm64 = "'$(Configuration)|$(Platform)'=='Release|ARM64'"
    cryptopp_debug = "'$(Configuration)'=='Debug' Or '$(Configuration)'=='DLL-Import Debug'"
    cryptopp_release = "'$(Configuration)'=='Release' Or '$(Configuration)'=='DLL-Import Release'"

    app = load_project_xml(root, r"workspaces\workspace\app\emulebb-main\srchybrid\emule.vcxproj")
    assert_no_project_configuration(app, "emule.vcxproj", "Platform", "Win32")
    assert_no_project_configuration(app, "emule.vcxproj", "Configuration", "_SpecialBootstrapNodes")
    for prop, expected in (
        ("LanguageStandard", "stdcpp17"),
        ("Optimization", "Disabled"),
        ("RuntimeLibrary", "MultiThreadedDebug"),
        ("BufferSecurityCheck", "true"),
        ("SDLCheck", "true"),
        ("DebugInformationFormat", "ProgramDatabase"),
        ("ControlFlowGuard", "Guard"),
    ):
        assert_cl_compile_value(app, "emule.vcxproj", app_debug, prop, expected)
    assert_app_multi_processor_compilation(app, app_debug)
    assert_link_value(app, "emule.vcxproj", app_debug, "IncrementalLink", "true")
    assert_link_value(app, "emule.vcxproj", app_debug, "LinkControlFlowGuard", "true")
    for prop, expected in (
        ("LanguageStandard", "stdcpp17"),
        ("Optimization", "MaxSpeed"),
        ("RuntimeLibrary", "MultiThreaded"),
        ("BufferSecurityCheck", "true"),
        ("SDLCheck", "true"),
        ("FunctionLevelLinking", "true"),
        ("IntrinsicFunctions", "true"),
        ("ControlFlowGuard", "Guard"),
    ):
        assert_cl_compile_value(app, "emule.vcxproj", app_release, prop, expected)
    assert_app_multi_processor_compilation(app, app_release)
    assert_link_value(app, "emule.vcxproj", app_release, "IncrementalLink", "false")
    assert_link_value(app, "emule.vcxproj", app_release, "LinkControlFlowGuard", "true")

    tests = load_project_xml(root, r"repos\emulebb-build-tests\emule-tests.vcxproj")
    assert_no_project_configuration(tests, "emule-tests.vcxproj", "Platform", "Win32")
    assert_no_project_configuration(tests, "emule-tests.vcxproj", "Configuration", "_SpecialBootstrapNodes")
    for condition in (tests_debug, tests_release, tests_debug_arm64, tests_release_arm64):
        assert_property_group_value(tests, "emule-tests.vcxproj", condition, "PlatformToolset", "v143")
    for prop, expected in (
        ("LanguageStandard", "stdcpp17"),
        ("Optimization", "Disabled"),
        ("RuntimeLibrary", "MultiThreadedDebug"),
        ("BufferSecurityCheck", "true"),
        ("DebugInformationFormat", "ProgramDatabase"),
        ("MultiProcessorCompilation", "true"),
    ):
        assert_cl_compile_value(tests, "emule-tests.vcxproj", tests_debug_build, prop, expected)
    assert_link_value(tests, "emule-tests.vcxproj", tests_debug_build, "IncrementalLink", "true")
    for prop, expected in (
        ("LanguageStandard", "stdcpp17"),
        ("Optimization", "MaxSpeed"),
        ("RuntimeLibrary", "MultiThreaded"),
        ("BufferSecurityCheck", "true"),
        ("FunctionLevelLinking", "true"),
        ("IntrinsicFunctions", "true"),
        ("MultiProcessorCompilation", "true"),
    ):
        assert_cl_compile_value(tests, "emule-tests.vcxproj", tests_release_build, prop, expected)
    assert_link_value(tests, "emule-tests.vcxproj", tests_release_build, "IncrementalLink", "false")

    id3 = load_project_xml(root, r"repos\third_party\emulebb-id3lib\libprj\id3lib.vcxproj")
    for condition in (id3_debug_x64, id3_debug_arm64):
        for prop, expected in (
            ("LanguageStandard", "stdcpp17"),
            ("Optimization", "Disabled"),
            ("BufferSecurityCheck", "true"),
            ("DebugInformationFormat", "ProgramDatabase"),
            ("MultiProcessorCompilation", "true"),
            ("RuntimeLibrary", "MultiThreadedDebug"),
        ):
            assert_cl_compile_value(id3, "id3lib.vcxproj", condition, prop, expected)
    for condition in (id3_release_x64, id3_release_arm64):
        for prop, expected in (
            ("LanguageStandard", "stdcpp17"),
            ("BufferSecurityCheck", "true"),
            ("MultiProcessorCompilation", "true"),
            ("RuntimeLibrary", "MultiThreaded"),
            ("FunctionLevelLinking", "true"),
            ("IntrinsicFunctions", "true"),
            ("WholeProgramOptimization", "true"),
        ):
            assert_cl_compile_value(id3, "id3lib.vcxproj", condition, prop, expected)

    resizable = load_project_xml(root, r"repos\third_party\emulebb-resizablelib\ResizableLib\ResizableLib.vcxproj")
    for condition in (resizable_debug_x64, resizable_debug_arm64):
        for prop, expected in (
            ("LanguageStandard", "stdcpp17"),
            ("Optimization", "Disabled"),
            ("BufferSecurityCheck", "true"),
            ("MultiProcessorCompilation", "true"),
            ("RuntimeLibrary", "MultiThreadedDebug"),
        ):
            assert_cl_compile_value(resizable, "ResizableLib.vcxproj", condition, prop, expected)
    for condition in (resizable_release_x64, resizable_release_arm64):
        for prop, expected in (
            ("LanguageStandard", "stdcpp17"),
            ("Optimization", "MaxSpeed"),
            ("BufferSecurityCheck", "true"),
            ("MultiProcessorCompilation", "true"),
            ("RuntimeLibrary", "MultiThreaded"),
            ("FunctionLevelLinking", "true"),
        ):
            assert_cl_compile_value(resizable, "ResizableLib.vcxproj", condition, prop, expected)

    miniupnp = load_project_xml(root, r"repos\third_party\emulebb-miniupnp\miniupnpc\msvc\miniupnpc.vcxproj")
    for condition in (miniupnp_debug_x64, miniupnp_debug_arm64):
        for prop, expected in (
            ("Optimization", "Disabled"),
            ("BufferSecurityCheck", "true"),
            ("MultiProcessorCompilation", "true"),
            ("RuntimeLibrary", "MultiThreadedDebug"),
        ):
            assert_cl_compile_value(miniupnp, "miniupnpc.vcxproj", condition, prop, expected)
    for condition in (miniupnp_release_x64, miniupnp_release_arm64):
        for prop, expected in (
            ("Optimization", "MaxSpeed"),
            ("BufferSecurityCheck", "true"),
            ("MultiProcessorCompilation", "true"),
            ("RuntimeLibrary", "MultiThreaded"),
            ("FunctionLevelLinking", "true"),
            ("IntrinsicFunctions", "true"),
        ):
            assert_cl_compile_value(miniupnp, "miniupnpc.vcxproj", condition, prop, expected)

    cryptopp = load_project_xml(root, r"repos\third_party\emulebb-cryptopp\cryptlib.vcxproj")
    for prop, expected in (
        ("Optimization", "Disabled"),
        ("BufferSecurityCheck", "true"),
        ("DebugInformationFormat", "ProgramDatabase"),
        ("MultiProcessorCompilation", "true"),
        ("RuntimeLibrary", "MultiThreadedDebug"),
    ):
        assert_cl_compile_value(cryptopp, "cryptlib.vcxproj", cryptopp_debug, prop, expected)
    for prop, expected in (
        ("Optimization", "MaxSpeed"),
        ("BufferSecurityCheck", "true"),
        ("MultiProcessorCompilation", "true"),
        ("RuntimeLibrary", "MultiThreaded"),
        ("FunctionLevelLinking", "true"),
        ("IntrinsicFunctions", "true"),
    ):
        assert_cl_compile_value(cryptopp, "cryptlib.vcxproj", cryptopp_release, prop, expected)

    cmake_module = resolve_workspace_path(root, r"repos\emulebb-build\emule_workspace\cmake.py")
    assert "-DCMAKE_POLICY_DEFAULT_CMP0091=NEW" in read_text(cmake_module)
    assert "-DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded$<$<CONFIG:Debug>:Debug>" in read_text(cmake_module)
    build_module = resolve_workspace_path(root, r"repos\emulebb-build\emule_workspace\build.py")
    assert "static_msvc_runtime_cmake_arguments()" in read_text(build_module)
    print("Active build policy audit passed.")


def current_branch(repo_root: Path) -> str:
    """Returns the current branch or '(detached)'."""

    result = run_git(repo_root, ["symbolic-ref", "--quiet", "--short", "HEAD"], allow_failure=True)
    return result.text if result.returncode == 0 else "(detached)"


def head_commit(repo_root: Path, revision: str = "HEAD") -> str:
    """Resolves one Git revision."""

    result = run_git(repo_root, ["rev-parse", revision])
    if not result.text:
        raise RuntimeError(f"Unable to resolve git revision '{revision}' in '{repo_root}'.")
    return result.text


def assert_branch_allowed(repo_label: Path, expected_branch: str, actual_branch: str) -> None:
    """Checks active branch policy."""

    if actual_branch == expected_branch:
        return
    if expected_branch == "main" and re.match(r"^(feature|fix|chore)/", actual_branch):
        return
    raise RuntimeError(f"{repo_label} is on branch '{actual_branch}', expected '{expected_branch}'.")


def workspace_relative(root: Path, absolute_path: Path) -> str:
    """Returns a Windows-style workspace-relative path."""

    return os.path.relpath(absolute_path.resolve(), root.resolve()).replace("/", "\\")


def audit_branch_policy(root: Path) -> None:
    """Runs branch/worktree policy checks."""

    build_deps_path = resolve_workspace_path(root, r"repos\emulebb-build\deps.json")
    build_deps = json.loads(read_text(build_deps_path))
    workspace_name = build_deps.get("workspace", {}).get("name") or "workspace"
    workspace_path = resolve_workspace_path(root, f"workspaces\\{workspace_name}")
    manifest_path = workspace_path / "deps.json"
    manifest = json.loads(read_text(manifest_path))
    app_repo = manifest.get("workspace", {}).get("app_repo", {})
    seed_repo = app_repo.get("seed_repo", {})
    if not seed_repo:
        raise RuntimeError(f"Generated workspace manifest '{manifest_path}' is missing workspace.app_repo.seed_repo.")
    seed_repo_path = workspace_relative(root, (workspace_path / seed_repo["path"]).resolve())
    variants = []
    for variant in app_repo.get("variants", []):
        variants.append(
            {
                "name": str(variant["name"]),
                "path": workspace_relative(root, (workspace_path / variant["path"]).resolve()),
                "branch": str(variant["branch"]),
            }
        )

    canonical_repo = resolve_workspace_path(root, seed_repo_path)
    if not canonical_repo.exists():
        raise RuntimeError(f"Canonical app repo is missing: {canonical_repo}")
    if current_branch(canonical_repo) != "(detached)":
        raise RuntimeError(f"Canonical app repo must be detached; found branch '{current_branch(canonical_repo)}'.")
    expected_anchor = f"origin/{seed_repo['branch']}"
    canonical_head = head_commit(canonical_repo)
    expected_head = head_commit(canonical_repo, expected_anchor)
    if canonical_head != expected_head:
        raise RuntimeError(f"Canonical app repo HEAD is {canonical_head}, expected detached {expected_anchor} at {expected_head}.")

    for variant in variants:
        variant_path = resolve_workspace_path(root, variant["path"])
        if not variant_path.exists():
            raise RuntimeError(f"Managed app worktree is missing: {variant_path}")
        branch = current_branch(variant_path)
        if branch == "(detached)":
            raise RuntimeError(f"Managed app worktree '{variant['name']}' must stay on a named branch, but is detached.")
        if branch.startswith("stale/"):
            raise RuntimeError(f"Managed app worktree '{variant['name']}' must not use stale history branch '{branch}'.")
        assert_branch_allowed(variant_path, variant["branch"], branch)
    print("Branch policy audit passed.")


def audit_dependency_pins(root: Path) -> None:
    """Runs third-party dependency pin checks."""

    build_repo = resolve_workspace_path(root, r"repos\emulebb-build")
    sys.path.insert(0, str(build_repo))
    from emule_workspace.topology import canonical_topology  # pylint: disable=import-outside-toplevel

    topology_by_path = {repo.relative_path: repo.branch for repo in canonical_topology().third_party_repos}
    for relative_path in (
        r"repos\third_party\emulebb-cryptopp",
        r"repos\third_party\emulebb-id3lib",
        r"repos\third_party\emulebb-mbedtls",
        r"repos\third_party\emulebb-miniupnp",
        r"repos\third_party\emulebb-nlohmann-json",
        r"repos\third_party\emulebb-resizablelib",
        r"repos\third_party\emulebb-zlib",
    ):
        repo_root = resolve_workspace_path(root, relative_path)
        if not repo_root.exists():
            raise RuntimeError(f"Pinned third-party repo path is missing: {repo_root}")
        repo_name = repo_root.name
        branch = current_branch(repo_root)
        if branch == "(detached)":
            raise RuntimeError(f"Dependency repo '{repo_name}' must stay on a named branch; it is detached.")
        origin_head = run_git(repo_root, ["symbolic-ref", "--quiet", "refs/remotes/origin/HEAD"])
        expected_branch = origin_head.text.rsplit("/", 1)[-1]
        if branch != expected_branch:
            raise RuntimeError(f"Dependency repo '{repo_name}' is on '{branch}', expected active branch '{expected_branch}' from local origin/HEAD.")
        if relative_path not in topology_by_path:
            raise RuntimeError(f"Python topology is missing third-party repo path '{relative_path}'.")
        if topology_by_path[relative_path] != expected_branch:
            raise RuntimeError(f"Python topology pin for '{repo_name}' is '{topology_by_path[relative_path]}', expected '{expected_branch}'.")
    print("Dependency pin audit passed.")


def assert_path_missing(path: Path) -> None:
    """Rejects one obsolete path."""

    if path.exists():
        raise RuntimeError(f"Obsolete project entrypoint still exists: {path}")


def audit_project_entrypoints(root: Path) -> None:
    """Runs project entrypoint policy checks."""

    for variant in (
        r"workspaces\workspace\app\emulebb-main",
        r"workspaces\workspace\app\emulebb-community-baseline",
        r"workspaces\workspace\app\emulebb-community-tracing-harness",
    ):
        app_root = resolve_workspace_path(root, variant)
        assert_path_missing(app_root / r"srchybrid\emule.sln")
        assert_path_missing(app_root / r"srchybrid\emule.slnx")

    build_project = resolve_workspace_path(root, r"repos\emulebb-build\pyproject.toml")
    build_cli = resolve_workspace_path(root, r"repos\emulebb-build\emule_workspace\cli.py")
    build_module = resolve_workspace_path(root, r"repos\emulebb-build\emule_workspace\build.py")
    assert_contains(build_project, "emule-workspace", "emulebb-build must expose the Python-first emule_workspace orchestration package.")
    assert_contains(build_cli, "test python", "emule_workspace CLI must include the migrated Python test command surface.")
    assert_contains(build_cli, "package-release", "emule_workspace CLI must include the migrated release package command surface.")
    assert_contains(build_module, r"srchybrid.*emule\.vcxproj", r"emule_workspace must build the app through srchybrid\emule.vcxproj.")
    assert_not_contains(build_module, r"emule\.slnx?", "emule_workspace must not rely on emule.sln or emule.slnx.")
    assert_path_missing(resolve_workspace_path(root, r"repos\emulebb-build\workspace.ps1"))
    for doc in (
        resolve_workspace_path(root, r"repos\emulebb-build\README.md"),
        resolve_workspace_path(root, r"repos\emulebb-build-tests\README.md"),
        resolve_workspace_path(root, r"repos\emulebb-tooling\README.md"),
        resolve_workspace_path(root, r"repos\emulebb-tooling\AGENTS.md"),
        resolve_workspace_path(root, r"repos\emulebb-tooling\docs\WORKSPACE-POLICY.md"),
    ):
        assert_not_contains(doc, r"emule\.slnx?", f"{doc} must not describe emule.sln or emule.slnx as active build entrypoints.")
        assert_not_contains(
            doc,
            r"(^|\s|`|&)(?:&\s*)?msbuild(?:\.exe)?\s+(?:[./\\\w:-]+\.vcxproj|[./\\\w:-]+\.slnx?|/t:|/p:|-t:|-p:)",
            f"{doc} must not document direct MSBuild command lines as active build entrypoints; use repos\\emulebb-build orchestration.",
        )
    print("Project entrypoint audit passed.")


def audit_warning_policy(root: Path) -> None:
    """Runs warning policy checks."""

    projects = {
        r"repos\third_party\emulebb-cryptopp\cryptlib.vcxproj": (
            (r"_SILENCE_STDEXT_ARR_ITERS_DEPRECATION_WARNING", True, "Crypto++ must keep the narrow checked-iterator suppression."),
            (r"DisableSpecificWarnings[^<]*4996", False, "Do not blanket-disable C4996 in Crypto++ project settings."),
            (r"/wd4996", False, "Do not inject /wd4996 into Crypto++ build flags."),
        ),
        r"repos\third_party\emulebb-miniupnp\miniupnpc\msvc\miniupnpc.vcxproj": (
            (r"_WINSOCK_DEPRECATED_NO_WARNINGS", True, "miniupnp must keep the Winsock-specific deprecation suppression."),
            (r"DisableSpecificWarnings[^<]*4996", False, "Do not blanket-disable C4996 in miniupnp project settings."),
            (r"/wd4996", False, "Do not inject /wd4996 into miniupnp build flags."),
        ),
        r"workspaces\workspace\app\emulebb-main\srchybrid\emule.vcxproj": (
            (r"<ExternalWarningLevel>TurnOffAllWarnings</ExternalWarningLevel>", True, "The app project must keep external headers at /external:W0 through ExternalWarningLevel in Debug and Release."),
            (r"<AdditionalOptions[^>]*>[^<]*/external:W[0-4]\b", False, "Do not inject raw /external:W* switches through app AdditionalOptions; use ExternalWarningLevel instead."),
        ),
        r"repos\emulebb-build-tests\emule-tests.vcxproj": (
            (r"DisableSpecificWarnings[^<]*4996", False, "Do not blanket-disable C4996 in active project settings."),
            (r"/wd4996", False, "Do not inject /wd4996 into active build flags."),
        ),
        r"repos\third_party\emulebb-id3lib\libprj\id3lib.vcxproj": (
            (r"DisableSpecificWarnings[^<]*4996", False, "Do not blanket-disable C4996 in active project settings."),
            (r"/wd4996", False, "Do not inject /wd4996 into active build flags."),
        ),
        r"repos\third_party\emulebb-resizablelib\ResizableLib\ResizableLib.vcxproj": (
            (r"DisableSpecificWarnings[^<]*4996", False, "Do not blanket-disable C4996 in active project settings."),
            (r"/wd4996", False, "Do not inject /wd4996 into active build flags."),
        ),
    }
    for relative_path, checks in projects.items():
        path = resolve_workspace_path(root, relative_path)
        text = read_text(path)
        for pattern, should_match, reason in checks:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if should_match and not matches:
                raise RuntimeError(f"{path}: {reason}")
            if not should_match and matches:
                raise RuntimeError(f"{path}: {reason}")
            if relative_path.endswith(r"emule.vcxproj") and pattern.startswith("<ExternalWarningLevel") and len(matches) != 2:
                raise RuntimeError(f"{path}: {reason} Expected 2, found {len(matches)}.")
    print("Warning policy audit passed.")


def audit_localization_policy(root: Path) -> None:
    """Runs the aggregate release-localization preflight."""

    tooling_root = resolve_workspace_path(root, r"repos\emulebb-tooling")
    preflight = tooling_root / r"helpers\rc-localization-preflight.py"
    if not preflight.is_file():
        raise RuntimeError(f"Required localization preflight is missing: {preflight}")
    completed = subprocess.run(
        [sys.executable, str(preflight), "--workspace-root", str(root)],
        cwd=tooling_root,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("Release localization preflight failed.")
    print("Release localization policy audit passed.")


def tracked_powershell_paths(repo_root: Path) -> tuple[str, ...]:
    """Returns tracked PowerShell script paths for one repo."""

    return run_git(repo_root, ["ls-files", "*.ps1"]).lines


def is_direct_child_of(normalized_path: str, directory: str) -> bool:
    """Returns whether a slash-normalized path is a direct child of directory."""

    if not normalized_path.startswith(directory):
        return False
    child_name = normalized_path[len(directory) :]
    return bool(child_name) and "/" not in child_name


def is_runtime_powershell_name(path: str) -> bool:
    """Returns whether a runtime script uses the package Verb-Noun.ps1 shape."""

    name = Path(path.replace("\\", "/")).name
    return re.fullmatch(r"[A-Z][A-Za-z0-9]*-[A-Za-z][A-Za-z0-9]*\.ps1", name) is not None


def is_automation_example_path(path: str) -> bool:
    """Returns whether a path is a direct automation example PowerShell asset."""

    return is_direct_child_of(
        path.replace("\\", "/"),
        "emule_workspace/release_assets/emulebb_automation_examples/automation/",
    )


def audit_powershell_boundary(root: Path) -> None:
    """Checks that only approved Windows runtime assets carry PowerShell."""

    tooling_root = resolve_workspace_path(root, r"repos\emulebb-tooling")
    build_root = resolve_workspace_path(root, r"repos\emulebb-build")
    scan_roots = (
        tooling_root,
        resolve_workspace_path(root, r"repos\amutorrent"),
        build_root,
        resolve_workspace_path(root, r"repos\emulebb-build-tests"),
        resolve_workspace_path(root, r"repos\emulebb"),
        resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-main"),
        resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-community-baseline"),
        resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-community-tracing-harness"),
    )
    issues: list[str] = []
    for repo_root in scan_roots:
        if not repo_root.is_dir():
            continue
        for relative_path in tracked_powershell_paths(repo_root):
            normalized = relative_path.replace("\\", "/")
            path = repo_root / relative_path
            if not path.is_file():
                continue
            if repo_root == build_root and is_direct_child_of(
                normalized,
                "emule_workspace/release_assets/emulebb/scripts/",
            ):
                first_non_empty = next((line.strip() for line in read_text(path).splitlines() if line.strip()), "")
                if first_non_empty != "#Requires -Version 5.1":
                    issues.append(f"{path}: eMuleBB runtime PowerShell must declare #Requires -Version 5.1.")
                if not is_runtime_powershell_name(relative_path):
                    issues.append(f"{path}: eMuleBB runtime PowerShell scripts must use Verb-Noun.ps1 names.")
                continue
            if repo_root == build_root and is_automation_example_path(normalized):
                first_non_empty = next((line.strip() for line in read_text(path).splitlines() if line.strip()), "")
                if first_non_empty != "#Requires -Version 5.1":
                    issues.append(f"{path}: eMuleBB automation example PowerShell must declare #Requires -Version 5.1.")
                continue
            issues.append(
                f"{repo_root}\\{relative_path}: tracked PowerShell is only allowed under "
                "repos\\emulebb-build\\emule_workspace\\release_assets\\emulebb\\scripts or "
                "repos\\emulebb-build\\emule_workspace\\release_assets\\emulebb_automation_examples\\automation."
            )
    if issues:
        raise RuntimeError("\n".join(issues))
    print("PowerShell boundary audit passed.")


def modified_tracked_paths(repo_root: Path) -> tuple[str, ...]:
    """Returns modified tracked paths for normalization checks."""

    paths: set[str] = set()
    for args in (
        ["diff", "--name-only", "--diff-filter=ACMRT"],
        ["diff", "--cached", "--name-only", "--diff-filter=ACMRT"],
    ):
        paths.update(run_git(repo_root, args).lines)
    return tuple(sorted(paths))


def audit_editorconfig_policy(root: Path) -> None:
    """Runs editorconfig/normalization checks on modified tracked files."""

    tooling_root = resolve_workspace_path(root, r"repos\emulebb-tooling")
    normalizer = tooling_root / r"helpers\source-normalizer.py"
    if not normalizer.is_file():
        raise RuntimeError(f"Missing source normalizer: {normalizer}")
    for label, repo_root in (
        ("tooling", tooling_root),
        ("build", resolve_workspace_path(root, r"repos\emulebb-build")),
        ("tests", resolve_workspace_path(root, r"repos\emulebb-build-tests")),
        ("app-main", resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-main")),
        ("app-community", resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-community-baseline")),
        ("app-tracing-harness", resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-community-tracing-harness")),
    ):
        if not repo_root.is_dir():
            raise RuntimeError(f"Editorconfig audit root is missing: {repo_root}")
        paths = modified_tracked_paths(repo_root)
        if not paths:
            print(f"Editorconfig audit: {label} (no modified tracked files)")
            continue
        print(f"Editorconfig audit: {label}")
        completed = subprocess.run(
            [sys.executable, str(normalizer), "--root", str(repo_root), "--check", *paths],
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"Editorconfig audit failed for '{label}'.")
    print("Editorconfig policy audit passed.")


def tracked_doc_paths(repo_root: Path, patterns: Sequence[str]) -> tuple[str, ...]:
    """Returns tracked doc paths matching one git pathspec list."""

    return run_git(repo_root, ["ls-files", "--", *patterns]).lines


def get_optional_text(repo_root: Path, relative_path: str) -> str | None:
    """Reads an optional tracked text file."""

    path = repo_root / relative_path
    return path.read_text(encoding="utf-8") if path.is_file() else None


def collect_doc_path_issues(root: Path) -> list[str]:
    """Collects active documentation path audit issues."""

    issues: list[str] = []
    tooling = resolve_workspace_path(root, r"repos\emulebb-tooling")
    scan_scopes = (
        (tooling, ("README.md", "AGENTS.md", r"docs\WORKSPACE-POLICY.md")),
        (tooling, (r"docs\active\*.md", r"docs\active\items\*.md", r"docs\active\plans\*.md", r"docs\active\reviews\*.md")),
        (resolve_workspace_path(root, r"repos\emulebb-build"), ("README.md", "AGENTS.md")),
        (resolve_workspace_path(root, r"repos\emulebb-build-tests"), ("README.md", "AGENTS.md")),
        (resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-main"), ("README.md", "AGENTS.md")),
        (resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-community-baseline"), ("AGENTS.md",)),
        (resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-community-tracing-harness"), ("AGENTS.md",)),
    )
    absolute_path_re = re.compile(r"\b[a-z]:\\", re.IGNORECASE)
    for repo_root, patterns in scan_scopes:
        if not repo_root.exists():
            raise RuntimeError(f"Documentation scan root is missing: {repo_root}")
        for relative_path in tracked_doc_paths(repo_root, patterns):
            path = repo_root / relative_path
            if not path.is_file():
                continue
            for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if absolute_path_re.search(line):
                    issues.append(f"{path}:{index}: hardcoded absolute path in markdown: {line.strip()}")
    return issues


def collect_current_doc_stale_reference_issues(root: Path) -> list[str]:
    """Collects stale product/workspace wording from the current doc surface."""

    issues: list[str] = []
    tooling = resolve_workspace_path(root, r"repos\emulebb-tooling")
    scan_patterns = (
        "README.md",
        "AGENTS.md",
        r"docs\WORKSPACE-POLICY.md",
        r"docs\INDEX.md",
        r"docs\DOCS-POLICY.md",
        r"docs\HISTORICAL-REFERENCES.md",
        r"docs\active\*.md",
        r"docs\active\items\*.md",
        r"docs\active\plans\*.md",
        r"docs\active\reviews\*.md",
        r"docs\dependencies\*.md",
        r"docs\reference\*.md",
        r"docs\rest\*.md",
    )
    stale_patterns = (
        (re.compile(r"\beMule BB\b"), "compact product name must be eMuleBB in current docs"),
        (re.compile(r"\bpost-beta(?:-0\.7\.3)?\b", re.IGNORECASE), "current release-era wording should use post-0.7.3, not post-beta"),
        (re.compile(r"\bPost-beta\b"), "current release-era wording should use Post-0.7.3, not Post-beta"),
        (re.compile(r"\bemule-bb-v\b"), "release tag prefix must use emulebb-v in current docs"),
        (re.compile(r"\beMule-broadband-\b"), "package identity must use current lowercase emulebb naming in current docs"),
    )
    retired_repo_pattern = re.compile(r"\bemulebb-ed2k-server\b")
    retired_repo_allow = re.compile(r"\b(obsolete|stale|retired|removed|no current|no active|historical|decommissioned)\b", re.IGNORECASE)
    for relative_path in tracked_doc_paths(tooling, scan_patterns):
        path = tooling / relative_path
        if not path.is_file():
            continue
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern, message in stale_patterns:
                if pattern.search(line):
                    issues.append(f"{path}:{index}: {message}: {line.strip()}")
            if retired_repo_pattern.search(line) and not retired_repo_allow.search(line):
                issues.append(
                    f"{path}:{index}: emulebb-ed2k-server may only appear in current docs as an explicit retired/obsolete reference: {line.strip()}"
                )
    return issues


def assert_text_contains(issues: list[str], repo_root: Path, relative_path: str, needle: str, message: str) -> None:
    """Records an issue if a required text fragment is missing."""

    text = get_optional_text(repo_root, relative_path)
    if text is None:
        issues.append(f"{repo_root}: missing required file: {relative_path}")
        return
    if needle not in text:
        issues.append(f"{repo_root}\\{relative_path}: {message}")


def assert_text_not_contains(issues: list[str], repo_root: Path, relative_path: str, needles: Sequence[str], message: str) -> None:
    """Records an issue if a forbidden fragment is present."""

    text = get_optional_text(repo_root, relative_path)
    if text is None:
        return
    for needle in needles:
        if needle in text:
            issues.append(f"{repo_root}\\{relative_path}: {message}: {needle}")


def assert_rest_contract_defers_to_openapi(issues: list[str], tooling: Path) -> None:
    """Checks REST contract documentation ownership."""

    relative_path = r"docs\rest\REST-API-CONTRACT.md"
    text = get_optional_text(tooling, relative_path)
    if text is None:
        issues.append(f"{tooling}: missing required file: {relative_path}")
        return
    if "Source of truth:** [REST-API-OPENAPI.yaml](REST-API-OPENAPI.yaml)" not in text:
        issues.append(f"{tooling}\\{relative_path}: REST contract doc must identify OpenAPI as the source of truth.")
    active_text = text.split("## Retired Before Public Release", 1)[0]
    route_patterns = (
        r"(?im)^\s*\|.*\b(GET|POST|PATCH|DELETE)\b\s+(/api/v1|/app|/status|/stats|/snapshot|/categories|/transfers|/shared|/uploads|/upload-queue|/servers|/kad|/searches|/friends|/logs)\b",
        r"(?im)^\s*[-*]\s+`?(GET|POST|PATCH|DELETE)\s+(/api/v1|/app|/status|/stats|/snapshot|/categories|/transfers|/shared|/uploads|/upload-queue|/servers|/kad|/searches|/friends|/logs)\b",
    )
    for pattern in route_patterns:
        match = re.search(pattern, active_text)
        if match:
            issues.append(f"{tooling}\\{relative_path}: active REST route tables/lists must live in REST-API-OPENAPI.yaml, not the human contract doc: {match.group(0).strip()}")


def assert_active_index_non_done_count(issues: list[str], tooling: Path) -> None:
    """Checks active item index non-done count metadata."""

    relative_path = r"docs\active\INDEX.md"
    text = get_optional_text(tooling, relative_path)
    if text is None:
        issues.append(f"{tooling}: missing required file: {relative_path}")
        return
    declared = re.search(r"\*\*Current non-done count:\*\*\s*`(?P<count>\d+)`", text)
    if declared is None:
        issues.append(f"{tooling}\\{relative_path}: missing Current non-done count metadata.")
        return
    status_map = {
        "OPEN": "OPEN",
        "IN_PROGRESS": "IN_PROGRESS",
        "BLOCKED": "BLOCKED",
        "DEFERRED": "DEFERRED",
        "DONE": "DONE",
        "PASSED": "PASSED",
        "WONT_DO": "WONT_DO",
        "Open": "OPEN",
        "In Progress": "IN_PROGRESS",
        "Blocked": "BLOCKED",
        "Deferred": "DEFERRED",
        "Done": "DONE",
        "Passed": "PASSED",
        "Wont-Fix": "WONT_DO",
    }
    active_statuses = {"OPEN", "IN_PROGRESS", "BLOCKED", "DEFERRED"}
    row_re = re.compile(r"(?m)^\| \[[A-Z]+-\d+\]\([^)]+\) \| [^|]+ \| (?P<status>[^|]+) \|")
    actual = 0
    for match in row_re.finditer(text):
        status = match.group("status").strip().strip("*")
        if status_map.get(status) in active_statuses:
            actual += 1
    expected = int(declared.group("count"))
    if expected != actual:
        issues.append(f"{tooling}\\{relative_path}: Current non-done count is {expected}, but active item tables contain {actual} OPEN/IN_PROGRESS/BLOCKED/DEFERRED items.")


def audit_doc_paths(root: Path) -> None:
    """Runs active documentation path checks."""

    issues = collect_doc_path_issues(root)
    issues.extend(collect_current_doc_stale_reference_issues(root))
    tooling = resolve_workspace_path(root, r"repos\emulebb-tooling")
    policy_text = r"repos\emulebb-tooling\docs\WORKSPACE-POLICY.md"
    agent_files = (
        (root, "AGENTS.md"),
        (tooling, "AGENTS.md"),
        (tooling, r"scripts\AGENTS.md"),
        (resolve_workspace_path(root, r"repos\emulebb-build"), "AGENTS.md"),
        (resolve_workspace_path(root, r"repos\emulebb-build-tests"), "AGENTS.md"),
        (resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-main"), "AGENTS.md"),
        (resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-community-baseline"), "AGENTS.md"),
        (resolve_workspace_path(root, r"workspaces\workspace\app\emulebb-community-tracing-harness"), "AGENTS.md"),
    )
    for repo_root, relative_path in agent_files:
        assert_text_contains(issues, repo_root, relative_path, policy_text, "AGENTS.md must point to the central workspace policy.")
    # In-scope downstream/sibling forks must also point at the central policy, but
    # only when the fork is materialized in this workspace (minimal checkouts may
    # omit them). p2p-overlord-* is a separate product family and is excluded.
    for relative_repo in (
        r"repos\emulebb-rust",
        r"repos\amutorrent",
        r"repos\qbittorrentbb",
        r"repos\amule",
        r"repos\goed2k-server",
    ):
        fork_root = resolve_workspace_path(root, relative_repo)
        if fork_root.is_dir():
            assert_text_contains(issues, fork_root, "AGENTS.md", policy_text, "AGENTS.md must point to the central workspace policy.")
    for repo_root, relative_path in agent_files[:6]:
        assert_text_not_contains(
            issues,
            repo_root,
            relative_path,
            (r"the canonical remote repo is `EMULEBB_WORKSPACE_ROOT\repos\emulebb-remote`", "community/v0.72a` is the imported baseline"),
            "AGENTS.md contains stale workspace directive text",
        )
    resume_text = get_optional_text(tooling, r"docs\RESUME.md")
    if resume_text is not None:
        if "handoff" not in resume_text:
            issues.append(f"{tooling}\\docs\\RESUME.md: RESUME.md must identify itself as a handoff note.")
        if "not policy" not in resume_text:
            issues.append(f"{tooling}\\docs\\RESUME.md: RESUME.md must not be usable as policy authority.")
    assert_text_not_contains(issues, tooling, "README.md", (r"repos\emulebb-remote", "remote companion app"), "active tooling README must not reference abandoned eMule-remote entrypoints")
    assert_rest_contract_defers_to_openapi(issues, tooling)
    assert_active_index_non_done_count(issues, tooling)
    if issues:
        raise RuntimeError("\n".join(issues))
    print("Active documentation path audit passed.")


def audit_clean_worktree(root: Path) -> None:
    """Runs the explicit tracked worktree cleanliness guard."""

    run_clean_worktree_guard(workspace_root=root)
    print("Tracked worktree cleanliness audit passed.")


# In-scope managed forks for the cross-fork hygiene audits. Each entry is a
# (label, workspace-relative path) pair. The p2p-overlord-* family is a separate
# product line and is intentionally excluded. The emulebb app is audited through
# its managed worktree, not the detached repos\emulebb anchor.
HYGIENE_SCOPE_REPOS: tuple[tuple[str, str], ...] = (
    ("app-main", r"workspaces\workspace\app\emulebb-main"),
    ("emulebb-rust", r"repos\emulebb-rust"),
    ("amutorrent", r"repos\amutorrent"),
    ("qbittorrentbb", r"repos\qbittorrentbb"),
    ("amule", r"repos\amule"),
    ("goed2k-server", r"repos\goed2k-server"),
    ("emulebb-build", r"repos\emulebb-build"),
    ("emulebb-build-tests", r"repos\emulebb-build-tests"),
    ("emulebb-tooling", r"repos\emulebb-tooling"),
)

# Script/source globs scanned by the cross-fork hygiene audits.
HYGIENE_SOURCE_GLOBS: tuple[str, ...] = (
    "*.py", "*.ps1", "*.psm1", "*.bat", "*.cmd", "*.sh",
    "*.rs", "*.mjs", "*.js", "*.toml", "*.md",
)

# The authoritative workspace path variables an agent must never assign; they
# are machine-level inputs that orchestration only ever reads.
AUTHORITATIVE_ENV_VARS: tuple[str, ...] = (
    "CARGO_TARGET_DIR",
    "EMULEBB_WORKSPACE_ROOT",
    "EMULEBB_WORKSPACE_OUTPUT_ROOT",
)

# (repo-relative path suffix, variable) writes that are sanctioned boundary
# bootstraps and therefore allowlisted from the env-override audit.
ENV_OVERRIDE_ALLOWLIST: frozenset[tuple[str, str]] = frozenset(
    {
        (r"emule_workspace\materialize.py", "EMULEBB_WORKSPACE_ROOT"),
    }
)


def _scoped_repo_roots(root: Path) -> list[tuple[str, Path]]:
    """Returns existing (label, path) roots for the in-scope managed forks."""

    roots: list[tuple[str, Path]] = []
    for label, relative_path in HYGIENE_SCOPE_REPOS:
        repo_root = resolve_workspace_path(root, relative_path)
        if repo_root.is_dir():
            roots.append((label, repo_root))
    return roots


def _tracked_source_files(repo_root: Path) -> tuple[str, ...]:
    """Returns tracked source/script files under one repo as posix-ish paths."""

    return run_git(repo_root, ["ls-files", "--", *HYGIENE_SOURCE_GLOBS]).lines


def _env_write_patterns() -> tuple[tuple[re.Pattern[str], str], ...]:
    """Builds (regex, variable) pairs matching env writes across shells/langs."""

    forms = (
        r"\$env:{var}\s*=",                                # PowerShell
        r"(?:^|\s)set\s+{var}\s*=",                        # cmd/batch
        r"(?:^|\s)export\s+{var}\s*=",                     # POSIX sh
        r"os\.environ\[\s*[\"']{var}[\"']\s*\]\s*=",       # python assignment
        r"os\.environ\.setdefault\(\s*[\"']{var}[\"']",    # python setdefault
        r"os\.putenv\(\s*[\"']{var}[\"']",                 # python putenv
        r"(?:std::)?env::set_var\(\s*\"{var}\"",           # rust
        r"process\.env\.{var}\s*=[^=]",                    # node assignment
    )
    pairs: list[tuple[re.Pattern[str], str]] = []
    for var in AUTHORITATIVE_ENV_VARS:
        for form in forms:
            pairs.append((re.compile(form.format(var=re.escape(var))), var))
    return tuple(pairs)


def audit_emulebb_env_override(root: Path) -> None:
    """Rejects writes to authoritative workspace path environment variables.

    Orchestration, scripts, and tests must read ``EMULEBB_WORKSPACE_ROOT`` and
    ``EMULEBB_WORKSPACE_OUTPUT_ROOT`` from the process environment and must read
    ``CARGO_TARGET_DIR`` as the operator-provided Rust target root. They must
    never reassign, shadow, or default those variables. Command-scoped knobs such
    as ``EMULEBB_TEST_*`` and ``EMULEBB_REST_*`` are owned by their orchestration
    modules and are out of scope for this audit.
    """

    patterns = _env_write_patterns()
    issues: list[str] = []
    for _label, repo_root in _scoped_repo_roots(root):
        for relative_path in _tracked_source_files(repo_root):
            path = repo_root / relative_path
            if not path.is_file():
                continue
            normalized = relative_path.replace("/", "\\")
            for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                for pattern, var in patterns:
                    if not pattern.search(line):
                        continue
                    if any(normalized.endswith(suffix) and var == allowed_var for suffix, allowed_var in ENV_OVERRIDE_ALLOWLIST):
                        continue
                    issues.append(
                        f"{path}:{index}: assigns authoritative {var} (read it, never override): {line.strip()}"
                    )
    if issues:
        raise RuntimeError("\n".join(issues))
    print("Authoritative env override audit passed.")


def audit_output_root(root: Path) -> None:
    """Checks that build output is redirected under EMULEBB_WORKSPACE_OUTPUT_ROOT.

    Concretely: the Rust fork must keep its ``target/`` out of the source tree,
    no tracked script may redirect ``CARGO_TARGET_DIR`` back inside a repo, and
    no tracked build command may target the retired
    ``workspaces\\workspace\\state\\tools`` location instead of the output root.
    """

    issues: list[str] = []

    # Rust fork: target/ must be gitignored and untracked so ad-hoc cargo cannot
    # pollute the source tree. CARGO_TARGET_DIR must be pre-set by the operator
    # to EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\rust\target.
    rust_root = resolve_workspace_path(root, r"repos\emulebb-rust")
    if rust_root.is_dir():
        gitignore = rust_root / ".gitignore"
        ignore_text = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
        if not re.search(r"(?m)^/?target/?\s*$", ignore_text):
            issues.append(f"{gitignore}: emulebb-rust must gitignore the build target/ directory")
        tracked_target = run_git(rust_root, ["ls-files", "--", "target", "target/**"]).lines
        if tracked_target:
            issues.append(f"{rust_root}: tracked files exist under target/ (build output in source tree): {tracked_target[0]} ...")

    # No tracked script may redirect Cargo output to a non-output-root path.
    cargo_re = re.compile(r"CARGO_TARGET_DIR")
    state_tools_re = re.compile(r"workspaces[\\/]workspace[\\/]state[\\/]tools", re.IGNORECASE)
    build_verb_re = re.compile(r"build\s+-o|/p:OutDir|target-dir|CARGO_TARGET_DIR", re.IGNORECASE)
    prj_path_re = re.compile(r"[\\/]prj[\\/]|repos[\\/]", re.IGNORECASE)
    for _label, repo_root in _scoped_repo_roots(root):
        for relative_path in _tracked_source_files(repo_root):
            path = repo_root / relative_path
            if not path.is_file():
                continue
            for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if cargo_re.search(line) and "=" in line and "EMULEBB_WORKSPACE_OUTPUT_ROOT" not in line and prj_path_re.search(line):
                    issues.append(f"{path}:{index}: CARGO_TARGET_DIR points inside a source tree, not the output root: {line.strip()}")
                if state_tools_re.search(line) and build_verb_re.search(line):
                    issues.append(f"{path}:{index}: build output targets retired state\\tools instead of EMULEBB_WORKSPACE_OUTPUT_ROOT\\tools: {line.strip()}")

    if issues:
        raise RuntimeError("\n".join(issues))
    print("Output-root build redirection audit passed.")


# High-precision non-English (Italian) marker words. The English-only tracked-
# content rule (WORKSPACE-POLICY Documentation Policy) forbids non-English prose in
# tracked files. UI-localization and vendored/fork/translation paths are exempt.
LANGUAGE_DENYLIST_FRAGMENTS: tuple[str, ...] = (
    "/doc/", "/lang/", "/translations/", "/locale/", "/3rdparty/",
    "/node_modules/", "/readme-", "/changelog-",
)
ITALIAN_MARKERS: tuple[str, ...] = (
    "perché", "perchè", "perciò", "abbiamo", "dovremmo", "vorrei", "qualcosa",
    "soltanto", "faremo", "facciamo", "dobbiamo", "vogliamo", "questo", "questa",
    "queste", "questi", "anche", "così", "adesso", "invece", "oppure",
)


def audit_language_policy(root: Path) -> None:
    """Tracked Markdown prose must be English (WORKSPACE-POLICY Documentation Policy).

    Scans authored Markdown across the managed repos for high-precision Italian
    marker words. UI-localization resources and vendored/fork or translation paths
    are exempt.
    """

    pattern = re.compile(
        r"(?<!\w)(" + "|".join(re.escape(w) for w in ITALIAN_MARKERS) + r")(?!\w)",
        re.IGNORECASE,
    )
    issues: list[str] = []
    for label, repo_root in _scoped_repo_roots(root):
        for rel in run_git(repo_root, ["ls-files", "--", "*.md"]).lines:
            if any(fragment in "/" + rel.lower() for fragment in LANGUAGE_DENYLIST_FRAGMENTS):
                continue
            text = read_text(repo_root / rel)
            for index, line in enumerate(text.splitlines(), start=1):
                match = pattern.search(line)
                if match:
                    issues.append(
                        f"{label}\\{rel}:{index}: non-English marker "
                        f"'{match.group(1)}' — tracked content must be English"
                    )
                    break
    if issues:
        raise RuntimeError("\n".join(issues))


AUDITS = {
    "build-policy": audit_build_policy,
    "branch-policy": audit_branch_policy,
    "language-policy": audit_language_policy,
    "clean-worktree": audit_clean_worktree,
    "dependency-pins": audit_dependency_pins,
    "doc-paths": audit_doc_paths,
    "editorconfig-policy": audit_editorconfig_policy,
    "emulebb-env-override": audit_emulebb_env_override,
    "localization-policy": audit_localization_policy,
    "output-root": audit_output_root,
    "project-entrypoints": audit_project_entrypoints,
    "powershell-boundary": audit_powershell_boundary,
    "warning-policy": audit_warning_policy,
}


def main(argv: Sequence[str] | None = None) -> int:
    """Runs one requested workspace policy audit."""

    parser = argparse.ArgumentParser()
    parser.add_argument("audit", choices=sorted(AUDITS))
    args = parser.parse_args(argv)
    try:
        AUDITS[args.audit](workspace_root_from_env())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
