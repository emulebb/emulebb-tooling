#!/usr/bin/env python3
"""Shared Python CI checks for workspace-owned repositories."""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GuardRule:
    """One path or content rule loaded from a privacy policy manifest."""

    id: str
    reason: str
    regex: str


class PrivacyGuardFailure(RuntimeError):
    """Failure raised when the tracked-file privacy scan finds violations."""

    def __init__(self, summary: dict[str, Any]) -> None:
        super().__init__("Tracked-file privacy guard failed.")
        self.summary = summary


class BasicHygieneFailure(RuntimeError):
    """Failure raised when the basic hygiene scan finds violations."""

    def __init__(self, summary: dict[str, Any]) -> None:
        super().__init__("Basic hygiene checks failed.")
        self.summary = summary


class CleanWorktreeFailure(RuntimeError):
    """Failure raised when tracked worktree changes are present."""

    def __init__(self, issues: tuple[str, ...]) -> None:
        super().__init__("\n\n".join(issues))
        self.issues = issues


WORKSPACE_CLEAN_REPO_PATHS = (
    "repos/emulebb",
    "repos/emulebb-build",
    "repos/emulebb-build-tests",
    "repos/emulebb-tooling",
    "repos/third_party/emulebb-cryptopp",
    "repos/third_party/emulebb-id3lib",
    "repos/third_party/emulebb-mbedtls",
    "repos/third_party/emulebb-miniupnp",
    "repos/third_party/emulebb-resizablelib",
    "repos/third_party/emulebb-zlib",
    "workspaces/workspace/app/emulebb-main",
    "workspaces/workspace/app/emulebb-community-baseline",
    "workspaces/workspace/app/emulebb-community-tracing-harness",
)


def get_tracked_files(repo_root: Path) -> list[str]:
    """Returns Git-tracked paths under one repository."""

    completed = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "-z"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git ls-files failed for '{repo_root}'." + (f" {detail}" if detail else ""))
    return [entry for entry in completed.stdout.decode("utf-8", errors="surrogateescape").split("\0") if entry.strip()]


def run_clean_worktree_guard(*, workspace_root: Path, setup_repo_root: Path | None = None) -> None:
    """Fails when managed workspace repos contain tracked changes."""

    repos_to_check = [workspace_root.resolve() / relative_path for relative_path in WORKSPACE_CLEAN_REPO_PATHS]
    if setup_repo_root is not None:
        repos_to_check.insert(0, setup_repo_root.resolve())

    issues: list[str] = []
    for repo_root in repos_to_check:
        if not repo_root.exists():
            continue
        status_lines = tracked_status_lines(repo_root)
        if status_lines:
            issues.append(f"Tracked changes present in {repo_root}:\n" + "\n".join(status_lines))
    if issues:
        raise CleanWorktreeFailure(tuple(issues))


def tracked_status_lines(repo_root: Path) -> tuple[str, ...]:
    """Returns modified tracked status lines for one Git repo."""

    completed = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--short", "--untracked-files=no", "--ignore-submodules=all"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip()
        raise RuntimeError(f"git status failed for '{repo_root}'." + (f" {detail}" if detail else ""))
    return tuple(line for line in completed.stdout.splitlines() if line.strip())


def get_personal_identifiers(repo_root: Path) -> tuple[str, ...]:
    """Builds dynamic personal-identifier rules from environment and local overrides."""

    candidates: list[str] = []
    for variable_name in ("USERPROFILE", "HOME"):
        profile_path = os.environ.get(variable_name)
        if profile_path:
            candidates.append(Path(profile_path).name)
    for variable_name in ("USERNAME", "USER"):
        value = os.environ.get(variable_name)
        if value:
            candidates.append(value)
    for value in re.split(r"[,;]", os.environ.get("TRACKED_FILE_PRIVACY_IDENTIFIERS", "")):
        if value.strip():
            candidates.append(value.strip())

    local_identifier_path = repo_root / ".tracked-file-privacy-identifiers.local.json"
    if local_identifier_path.is_file():
        local_policy = json.loads(local_identifier_path.read_text(encoding="utf-8"))
        for value in local_policy.get("personalIdentifiers", []):
            if str(value).strip():
                candidates.append(str(value).strip())

    seen: set[str] = set()
    normalized: list[str] = []
    for value in candidates:
        identifier = value.strip().lower()
        if not re.match(r"^[a-z0-9][a-z0-9._-]{2,}$", identifier):
            continue
        if identifier in seen:
            continue
        seen.add(identifier)
        normalized.append(identifier)
    return tuple(normalized)


def run_privacy_guard(*, repo_root: Path, policy_path: Path, summary_path: Path | None = None) -> dict[str, Any]:
    """Scans tracked files for local-path or personal-identifier leaks."""

    repo_root_path = repo_root.resolve()
    if not policy_path.is_file():
        raise RuntimeError(f"Privacy-guard policy not found at '{policy_path}'.")

    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    excluded_path_regexes = [str(value) for value in policy.get("excludedPathRegexes", [])]
    dynamic_path_rules = [
        GuardRule(
            id="personal-identifier-filename",
            reason="Tracked filenames must not embed configured or environment-derived personal identifiers.",
            regex=rf"(^|[\\/])[^\\/]*{re.escape(identifier)}[^\\/]*$",
        )
        for identifier in get_personal_identifiers(repo_root_path)
    ]
    path_rules = [GuardRule(**entry) for entry in policy.get("pathRules", [])] + dynamic_path_rules
    content_rules = [GuardRule(**entry) for entry in policy.get("contentRules", [])]

    scanned_tracked_files: list[str] = []
    excluded_tracked_files: list[str] = []
    path_matches: list[dict[str, str]] = []
    for relative_path in get_tracked_files(repo_root_path):
        if any(re.search(regex, relative_path, flags=re.IGNORECASE) for regex in excluded_path_regexes):
            excluded_tracked_files.append(relative_path)
            continue
        scanned_tracked_files.append(relative_path)
        for rule in path_rules:
            if re.search(rule.regex, relative_path, flags=re.IGNORECASE):
                path_matches.append(
                    {
                        "path": relative_path,
                        "rule": rule.id,
                        "reason": rule.reason,
                        "regex": rule.regex,
                    }
                )
                break

    content_matches = find_content_matches(repo_root_path, scanned_tracked_files, content_rules)
    summary = {
        "schemaVersion": "tracked-file-privacy-guard-summary/v1",
        "repoRoot": str(repo_root_path),
        "policyVersion": policy.get("policyVersion"),
        "personalIdentifierRuleCount": len(dynamic_path_rules),
        "scannedTrackedFiles": len(scanned_tracked_files),
        "excludedTrackedFiles": excluded_tracked_files,
        "pathMatches": path_matches,
        "contentMatches": content_matches,
        "passed": not path_matches and not content_matches,
    }
    write_summary(summary, summary_path)
    if not summary["passed"]:
        raise PrivacyGuardFailure(summary)
    return summary


def find_content_matches(repo_root: Path, relative_paths: list[str], rules: list[GuardRule]) -> list[dict[str, str]]:
    """Scans tracked text files for configured content-rule matches."""

    matches: list[dict[str, str]] = []
    compiled_rules = [(rule, re.compile(rule.regex)) for rule in rules]
    for relative_path in relative_paths:
        file_path = repo_root / relative_path
        if not file_path.is_file():
            continue
        raw = file_path.read_bytes()
        if b"\0" in raw:
            continue
        for line_number, line in enumerate(raw.decode("utf-8", errors="replace").splitlines(), start=1):
            for rule, compiled in compiled_rules:
                if compiled.search(line):
                    matches.append(
                        {
                            "rule": rule.id,
                            "reason": rule.reason,
                            "path": relative_path,
                            "line": str(line_number),
                            "preview": line,
                        }
                    )
    return matches


def run_basic_hygiene(
    *,
    repo_root: Path,
    repo_kind: str = "generic",
    summary_path: Path | None = None,
) -> dict[str, Any]:
    """Runs cheap cross-repo hygiene checks against tracked files."""

    repo_root_path = repo_root.resolve()
    issues: list[dict[str, str]] = []
    checked = {
        "json": 0,
        "yaml": 0,
        "powershell": 0,
        "psd1": 0,
    }
    for relative_path in get_tracked_files(repo_root_path):
        full_path = repo_root_path / relative_path
        if not full_path.is_file():
            continue
        lower_path = relative_path.lower()
        if lower_path.endswith(".json"):
            checked["json"] += 1
            try:
                json.loads(full_path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001 - report parser detail.
                add_issue(issues, "json-parse", relative_path, str(exc))
        elif lower_path.endswith((".yml", ".yaml")):
            checked["yaml"] += 1
            yaml_issue = test_yaml_text_shape(full_path)
            if yaml_issue:
                add_issue(issues, "yaml-shape", relative_path, yaml_issue)
        elif lower_path.endswith(".ps1"):
            checked["powershell"] += 1
            header_issue = test_powershell_version_header(repo_root_path, repo_kind, relative_path, full_path)
            if header_issue:
                add_issue(issues, "powershell-version", relative_path, header_issue)
        elif lower_path.endswith(".psd1"):
            checked["psd1"] += 1
            psd1_issue = test_powershell_data_file_shape(full_path)
            if psd1_issue:
                add_issue(issues, "psd1-shape", relative_path, psd1_issue)

    if repo_kind in {"node-web", "amutorrent"}:
        package_json_path = repo_root_path / "package.json"
        if package_json_path.is_file():
            package_json = json.loads(package_json_path.read_text(encoding="utf-8"))
            scripts = package_json.get("scripts", {})
            for script_name in ("build", "test"):
                if script_name not in scripts:
                    add_issue(issues, "node-script", "package.json", f"Missing npm script '{script_name}'.")
        else:
            add_issue(issues, "node-package", "package.json", "Node web repo is missing package.json.")

    summary = {
        "schemaVersion": "basic-hygiene-summary/v1",
        "repoRoot": str(repo_root_path),
        "repoKind": repo_kind,
        "checked": checked,
        "issues": issues,
        "passed": not issues,
    }
    write_summary(summary, summary_path)
    if not summary["passed"]:
        raise BasicHygieneFailure(summary)
    return summary


def add_issue(issues: list[dict[str, str]], kind: str, path: str, reason: str) -> None:
    """Adds one structured hygiene issue."""

    issues.append({"kind": kind, "path": path, "reason": reason})


def test_yaml_text_shape(path: Path) -> str | None:
    """Returns a lightweight YAML shape issue for malformed-looking workflow files."""

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return "YAML file is empty."
    if "\t" in content:
        return "YAML file contains tab indentation."
    if not re.search(r"(?m)^\s*(name|on|jobs|defaults|env|version|updates|services)\s*:", content):
        return "YAML file does not contain an obvious top-level mapping key."
    return None


def test_powershell_version_header(repo_root: Path, repo_kind: str, relative_path: str, path: Path) -> str | None:
    """Checks the workspace-required PowerShell version header."""

    is_tooling_repo = repo_root.name == "emulebb-tooling" or (repo_root / "ci" / "check-workspace-policy.py").is_file()
    normalized_path = normalize_path(relative_path)
    is_amutorrent_installer = (repo_root.name == "amutorrent" or repo_kind == "amutorrent") and normalized_path.startswith("installer/windows/")
    expected_version = "5.1" if (is_tooling_repo and normalized_path.startswith("scripts/")) or is_amutorrent_installer else "7.6"
    expected_header = f"#Requires -Version {expected_version}"
    first_non_empty_line = next((line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()), "")
    if first_non_empty_line == expected_header:
        return None
    if not first_non_empty_line:
        return f"Missing required PowerShell version header '{expected_header}'."
    return f"Expected PowerShell version header '{expected_header}' but found '{first_non_empty_line}'."


def test_powershell_data_file_shape(path: Path) -> str | None:
    """Returns a lightweight issue for malformed-looking PowerShell data files."""

    content = path.read_text(encoding="utf-8-sig")
    if not content.strip():
        return "PowerShell data file is empty."
    if "@{" not in content:
        return "PowerShell data file does not contain a hashtable literal."
    return None


def normalize_path(value: str) -> str:
    """Returns a slash-normalized relative path."""

    return value.replace("\\", "/").lower()


def write_summary(summary: dict[str, Any], summary_path: Path | None) -> None:
    """Writes a machine-readable summary when requested."""

    if summary_path is None:
        return
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
