#!/usr/bin/env python3
"""Run the local gate for publishing Markdown docs as HTML."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_step(label: str, args: list[str], env: dict[str, str] | None = None) -> int:
    """Run one publishing check and return its process status."""

    print(f"==> {label}")
    result = subprocess.run(args, cwd=ROOT, env=env)
    if result.returncode != 0:
        print(f"failed: {label}", file=sys.stderr)
    return result.returncode


def main() -> int:
    """Run docs taxonomy, structure, roadmap, and MkDocs HTML checks."""

    steps = [
        ("item taxonomy", [sys.executable, "scripts/docs-item-taxonomy-check.py"], None),
        (
            "docs structure",
            [sys.executable, "scripts/docs-structure-check.py", "--fail-on-wide-tables"],
            None,
        ),
        ("GitHub roadmap metadata", [sys.executable, "scripts/github-roadmap-check.py"], None),
    ]

    mkdocs_env = os.environ.copy()
    mkdocs_env["NO_MKDOCS_2_WARNING"] = "1"
    steps.append(("MkDocs strict HTML build", [sys.executable, "-m", "mkdocs", "build", "--strict"], mkdocs_env))

    for label, args, env in steps:
        status = run_step(label, args, env)
        if status != 0:
            return status

    print("docs publish check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
