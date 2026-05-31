#!/usr/bin/env python3
"""Run workspace staged-file pre-commit checks."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """Builds the pre-commit hook runner parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default="", help="Repository root. Defaults to the current Git repo.")
    return parser


def run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    """Runs a Git command in the selected repository."""

    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def resolve_repo_root(candidate: str) -> Path:
    """Resolves the repository root used by the hook."""

    if candidate:
        return Path(candidate).resolve()
    result = run_git(Path.cwd(), ["rev-parse", "--show-toplevel"])
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError("Unable to resolve the Git repo root for the editorconfig hook.")
    return Path(result.stdout.decode("utf-8", errors="replace").strip()).resolve()


def staged_paths(repo_root: Path) -> list[str]:
    """Returns staged tracked paths that should be normalized before commit."""

    result = run_git(repo_root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z", "--"])
    if result.returncode != 0:
        raise RuntimeError(f"git diff --cached failed for '{repo_root}'.")
    return [
        item
        for item in result.stdout.decode("utf-8", errors="surrogateescape").split("\0")
        if item
    ]


def resolve_workspace_root(repo_root: Path) -> Path | None:
    """Resolve the canonical workspace root when this repo is in one."""

    env_root = os.environ.get("EMULEBB_WORKSPACE_ROOT")
    if env_root:
        root = Path(env_root).resolve()
        if (root / "repos" / "emulebb-tooling").is_dir():
            return root
    for parent in (repo_root, *repo_root.parents):
        if (parent / "repos" / "emulebb-tooling").is_dir() and (parent / "workspaces").is_dir():
            return parent
    return None


def run_normalizer(repo_root: Path, files: list[str]) -> tuple[int, str]:
    """Runs source-normalizer.py for staged files and returns its output."""

    normalizer = Path(__file__).resolve().parent / "source-normalizer.py"
    if not normalizer.is_file():
        raise RuntimeError(f"Missing source normalizer: {normalizer}")
    completed = subprocess.run(
        [sys.executable, str(normalizer), "--root", str(repo_root), "--write", *files],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return completed.returncode, completed.stdout


def is_localization_sensitive_path(repo_root: Path, path: str) -> bool:
    """Return whether a staged path should trigger localization preflight."""

    normalized = path.replace("\\", "/")
    repo_name = repo_root.name.lower()
    if repo_name == "emulebb-tooling":
        return (
            normalized == "ci/check-workspace-policy.py"
            or normalized == "hooks/pre-commit"
            or normalized.startswith("helpers/rc-")
        )
    if repo_name == "emulebb-main":
        return (
            normalized == "srchybrid/emule.rc"
            or normalized == "srchybrid/resource.h"
            or (normalized.startswith("srchybrid/lang/") and normalized.endswith(".rc"))
        )
    return False


def run_localization_preflight(repo_root: Path) -> tuple[int, str]:
    """Runs the aggregate localization preflight for staged localization changes."""

    workspace_root = resolve_workspace_root(repo_root)
    if workspace_root is None:
        return 1, "Unable to resolve EMULEBB_WORKSPACE_ROOT for localization preflight.\n"
    preflight = workspace_root / "repos" / "emulebb-tooling" / "helpers" / "rc-localization-preflight.py"
    if not preflight.is_file():
        return 1, f"Missing localization preflight: {preflight}\n"
    completed = subprocess.run(
        [sys.executable, str(preflight), "--workspace-root", str(workspace_root)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return completed.returncode, completed.stdout


def main(argv: list[str] | None = None) -> int:
    """Runs staged-file normalization and relevant workspace preflight checks."""

    args = build_parser().parse_args(argv)
    repo_root = resolve_repo_root(args.repo_root)
    files = staged_paths(repo_root)
    if not files:
        return 0
    return_code, output = run_normalizer(repo_root, files)
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
    if return_code != 0:
        raise RuntimeError("Editorconfig pre-commit normalization failed.")
    if any(line.startswith("NORMALIZED:") for line in output.splitlines()):
        print()
        print("Edited tracked files were normalized to match .editorconfig/.gitattributes.")
        print("Review the rewritten files, re-stage them, and retry the commit.")
        return 1
    if any(is_localization_sensitive_path(repo_root, path) for path in files):
        return_code, output = run_localization_preflight(repo_root)
        if output:
            print(output, end="" if output.endswith("\n") else "\n")
        if return_code != 0:
            raise RuntimeError("Release localization preflight failed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
