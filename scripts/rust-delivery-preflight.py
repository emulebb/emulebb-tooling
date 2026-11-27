#!/usr/bin/env python3
"""Check Rust delivery inputs before hooks or qualification acquire resources."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path


def output(repo: Path, *command: str) -> str:
    return subprocess.check_output(command, cwd=repo, text=True, stderr=subprocess.PIPE, timeout=30).strip()


def preflight(repo: Path, remote: str, offline: bool) -> tuple[dict, list[str]]:
    manifest = json.loads((repo / "tools" / "ci-toolchain.json").read_text(encoding="utf-8"))
    problems = []
    versions = {}
    for tool, pattern, args in (("go", r"go version go(\S+)", ("version",)),
                                ("npm", r"^(\d+\.\d+\.\d+)$", ("--version",))):
        try:
            executable = "npm.cmd" if tool == "npm" and os.name == "nt" else tool
            actual = re.search(pattern, output(repo, executable, *args))
            versions[tool] = actual[1] if actual else None
        except (OSError, subprocess.SubprocessError):
            versions[tool] = None
        if versions[tool] != manifest[tool]:
            problems.append(f"{tool}: expected {manifest[tool]}, observed {versions[tool] or 'unavailable'}")
    head = output(repo, "git", "rev-parse", "HEAD")
    report = {"head": head, "versions": versions, "inputs": manifest["inputs"]}
    for name, revision in manifest["inputs"].items():
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            problems.append(f"{name}: missing full pinned revision")
    if not offline:
        try:
            base_line = output(repo, "git", "ls-remote", "--exit-code", remote, "refs/heads/main")
            base = base_line.split()[0]
            report["base"] = base
            report["commits"] = int(output(repo, "git", "rev-list", "--count", f"{base}..{head}"))
            if report["commits"] > 100:
                problems.append("GitHub rebase merge allows at most 100 commits")
        except (OSError, subprocess.SubprocessError, IndexError, ValueError):
            problems.append("Could not compare HEAD with actual remote main. Fetch main and rerun")
        try:
            methods = json.loads(output(repo, "gh", "repo", "view", "--json", "mergeCommitAllowed,rebaseMergeAllowed"))
            if not methods["rebaseMergeAllowed"] or methods["mergeCommitAllowed"]:
                problems.append("Rust repository is expected to use rebase merge")
        except (OSError, subprocess.SubprocessError, ValueError, KeyError):
            problems.append("Could not verify the GitHub rebase merge settings")
    return report, problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--offline", action="store_true", help="Check tool and manifest inputs without GitHub access.")
    args = parser.parse_args()
    try:
        report, problems = preflight(args.repo.resolve(), args.remote, args.offline)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Preflight could not read the Rust inputs: {error}\n")
    print(json.dumps({**report, "problems": problems}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
