#!/usr/bin/env python3
"""Dispatch shared Git checks to the owning workspace orchestration."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def validation_environment() -> dict[str, str]:
    """Clear repository-local hook context before checks invoke Git in other repos."""
    local_names = subprocess.check_output(["git", "rev-parse", "--local-env-vars"], text=True)
    environment = os.environ.copy()
    # WHY: Git exports GIT_DIR and related variables to hooks. Child validation
    # creates and inspects other repositories; leaking this context can rewrite
    # the invoking repository's configuration or index despite a different cwd.
    # Follow githooks' documented `git rev-parse --local-env-vars` guidance.
    for name in local_names.splitlines():
        environment.pop(name, None)
    return environment


def orchestration_owner(root: Path, output: Path | None, repo: Path,
                        child_env: dict[str, str]) -> tuple[Path, str | None]:
    """Select a registered builder only after checking its shared Git identity."""
    root, repo = root.resolve(), repo.resolve()
    canonical = root / "repos" / "emulebb-build"
    boundary = root / "workspaces" / "agents"
    if not repo.is_relative_to(boundary):
        return canonical, None
    parts = repo.relative_to(boundary).parts
    if len(parts) != 2:
        raise RuntimeError("Hook checkout must identify a managed workstream repository")
    workstream_id, name = parts
    if not workstream_id or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in workstream_id):
        raise RuntimeError("Invalid workstream identity")
    if output is None or not output.is_absolute() or not output.is_dir() or output.resolve().is_relative_to(root):
        raise RuntimeError("Managed hook dispatch requires the inherited external output root")

    def unredirected(path: Path, limit: Path) -> None:
        current = path
        while current != limit.parent:
            if current.is_symlink() or getattr(current, "is_junction", lambda: False)():
                raise RuntimeError("Redirected hook registration or checkout is forbidden")
            current = current.parent
        if path.resolve() != path.absolute():
            raise RuntimeError("Hook registration or checkout resolves outside its declared path")

    record = output.resolve() / "tmp" / "workstreams" / f"{workstream_id}.json"
    unredirected(record, output.resolve())
    registration = json.loads(record.read_text(encoding="utf-8"))
    if (not isinstance(registration, dict) or registration.get("schema") != 1
            or registration.get("id") != workstream_id or registration.get("state") != "ready"
            or Path(registration.get("workspace_root", "")).resolve() != root):
        raise RuntimeError("Invalid or incomplete hook workstream registration")
    repositories = registration.get("repositories")
    if not isinstance(repositories, dict) or name not in repositories:
        raise RuntimeError("Hook repository is not registered in the selected workstream")
    invoking = repositories[name]
    if not isinstance(invoking, dict) or invoking.get("status") != "ready" or Path(invoking.get("path", "")).absolute() != repo:
        raise RuntimeError("Hook repository registration does not match its checkout")
    entry = repositories.get("emulebb-build")
    if entry is None:
        # The current canonical manager validates the complete registration. An
        # older manager must reject the explicit selector rather than check main.
        return canonical, workstream_id
    candidate = boundary / workstream_id / "emulebb-build"
    unredirected(candidate, root)
    if (not isinstance(entry, dict) or entry.get("status") != "ready"
            or Path(entry.get("path", "")).absolute() != candidate
            or Path(entry.get("canonical_path", "")).resolve() != canonical.resolve()):
        raise RuntimeError("Selected hook builder registration has an invalid identity")

    def git(path: Path, *arguments: str) -> str:
        return subprocess.check_output(["git", "-C", str(path), *arguments], env=child_env, text=True).strip()

    common_args = ("rev-parse", "--path-format=absolute", "--git-common-dir")
    common = Path(git(canonical, *common_args)).resolve()
    if (Path(git(candidate, "rev-parse", "--show-toplevel")).resolve() != candidate
            or Path(git(candidate, *common_args)).resolve() != common
            or Path(entry.get("common_dir", "")).resolve() != common
            or git(candidate, "remote", "get-url", "origin") != entry.get("origin")
            or git(canonical, "remote", "get-url", "origin") != entry.get("origin")
            or git(candidate, "branch", "--show-current") != entry.get("branch")):
        raise RuntimeError("Selected hook builder Git identity changed")
    # Full source-set validation remains the selected manager's responsibility,
    # before it executes any check. This bootstrap does not import worker code.
    return candidate, workstream_id


def main() -> int:
    """Forward hook input without changing inherited operator configuration."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("commit", "push"))
    parser.add_argument("remote", nargs="?", default="origin")
    parser.add_argument("remote_url", nargs="?", default="")
    args = parser.parse_args()
    root_value = os.environ.get("EMULEBB_WORKSPACE_ROOT")
    if not root_value:
        parser.error("EMULEBB_WORKSPACE_ROOT is required; configure the operator environment")
    root = Path(root_value)
    owner = root / "repos" / "emulebb-build"
    if not root.is_absolute() or not (owner / "emule_workspace").is_dir():
        parser.error("EMULEBB_WORKSPACE_ROOT must identify the canonical workspace")
    repo = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    child_env = validation_environment()
    output_value = os.environ.get("EMULEBB_WORKSPACE_OUTPUT_ROOT")
    owner, workstream_id = orchestration_owner(root, Path(output_value) if output_value else None,
                                               Path(repo), child_env)
    command = [sys.executable, "-B", "-m", "emule_workspace", "local-check", "--repo", repo,
               "--stage", args.stage, "--remote", args.remote]
    if args.stage == "push":
        command.append("--push-stdin")
    if workstream_id:
        command.extend(["--workstream", workstream_id])
    return subprocess.call(command, cwd=owner, env=child_env)


if __name__ == "__main__":
    raise SystemExit(main())
