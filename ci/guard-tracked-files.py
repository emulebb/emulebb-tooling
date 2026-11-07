#!/usr/bin/env python3
"""Fails when tracked files contain local path or personal-identifier leaks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from policy_guards import PrivacyGuardFailure, run_privacy_guard

REPO_ROOT = Path(__file__).resolve().parent.parent


def build_parser() -> argparse.ArgumentParser:
    """Builds the tracked-file privacy guard CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--policy-path", type=Path, default=REPO_ROOT / "manifests" / "privacy-guard" / "policy.v1.json")
    parser.add_argument("--summary-path", type=Path)
    parser.add_argument("--paths-file", type=Path, help="JSON list of changed paths; omit for a full tracked-file audit.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Runs the tracked-file privacy guard CLI."""

    args = build_parser().parse_args(argv)
    try:
        summary = run_privacy_guard(
            repo_root=args.repo_root,
            policy_path=args.policy_path,
            summary_path=args.summary_path,
            paths=set(json.loads(args.paths_file.read_text(encoding="utf-8"))) if args.paths_file else None,
        )
    except PrivacyGuardFailure as exc:
        print(json.dumps(exc.summary, indent=2))
        return 1
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
