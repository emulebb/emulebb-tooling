#!/usr/bin/env python3
"""Runs cheap cross-repo hygiene checks against tracked files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from policy_guards import BasicHygieneFailure, run_basic_hygiene

REPO_ROOT = Path(__file__).resolve().parent.parent


def build_parser() -> argparse.ArgumentParser:
    """Builds the basic hygiene CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument(
        "--repo-kind",
        choices=("generic", "workspace", "app", "tests", "tooling", "node-web", "amutorrent"),
        default="generic",
    )
    parser.add_argument("--summary-path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Runs the basic hygiene CLI."""

    args = build_parser().parse_args(argv)
    try:
        summary = run_basic_hygiene(
            repo_root=args.repo_root,
            repo_kind=args.repo_kind,
            summary_path=args.summary_path,
        )
    except BasicHygieneFailure as exc:
        print(json.dumps(exc.summary, indent=2))
        return 1
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
