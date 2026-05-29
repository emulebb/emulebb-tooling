#!/usr/bin/env python3
"""Fails when managed workspace repos contain tracked changes."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from policy_guards import CleanWorktreeFailure, run_clean_worktree_guard


def build_parser() -> argparse.ArgumentParser:
    """Builds the clean-worktree guard CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=None)
    parser.add_argument("--setup-repo-root", type=Path, default=None)
    return parser


def resolve_workspace_root(value: Path | None) -> Path:
    """Returns the canonical workspace root from CLI input or environment."""

    if value is not None:
        return value.resolve()
    env_value = os.environ.get("EMULEBB_WORKSPACE_ROOT", "")
    if env_value.strip():
        return Path(env_value).resolve()
    raise RuntimeError("EMULEBB_WORKSPACE_ROOT or --workspace-root is required.")


def main(argv: list[str] | None = None) -> int:
    """Runs the clean-worktree guard CLI."""

    args = build_parser().parse_args(argv)
    try:
        run_clean_worktree_guard(
            workspace_root=resolve_workspace_root(args.workspace_root),
            setup_repo_root=args.setup_repo_root,
        )
    except CleanWorktreeFailure as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Tracked worktree cleanliness audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
