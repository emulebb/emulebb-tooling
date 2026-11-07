#!/usr/bin/env python3
"""Dispatch shared Git checks to the owning workspace orchestration."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


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
    command = [sys.executable, "-m", "emule_workspace", "local-check", "--repo", repo,
               "--stage", args.stage, "--remote", args.remote]
    if args.stage == "push":
        command.append("--push-stdin")
    return subprocess.call(command, cwd=owner)


if __name__ == "__main__":
    raise SystemExit(main())
