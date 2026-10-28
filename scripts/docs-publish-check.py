#!/usr/bin/env python3
"""Run the local gate for publishing Markdown docs as HTML."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_path_env(name: str) -> Path:
    """Return one required absolute path from the inherited environment."""

    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"{name} must be set; refusing to derive or override it")
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise SystemExit(f"{name} must be an absolute path: {path}")
    return path.resolve()


def docs_site_dir() -> Path:
    """Return the MkDocs build directory below the workspace output root."""

    workspace_root = require_path_env("EMULEBB_WORKSPACE_ROOT")
    output_root = require_path_env("EMULEBB_WORKSPACE_OUTPUT_ROOT")
    try:
        ROOT.resolve().relative_to(workspace_root)
    except ValueError as exc:
        raise SystemExit(f"EMULEBB_WORKSPACE_ROOT must contain this checkout: {workspace_root}") from exc
    try:
        output_root.relative_to(workspace_root)
    except ValueError:
        pass
    else:
        raise SystemExit(
            f"EMULEBB_WORKSPACE_OUTPUT_ROOT must be outside EMULEBB_WORKSPACE_ROOT: {output_root}"
        )
    return output_root / "artifacts" / "docs" / "emulebb-tooling-site"


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
        (
            "emulebb-rust roadmap metadata",
            [
                sys.executable,
                "scripts/github-roadmap-check.py",
                "--product",
                "emulebb-rust",
            ],
            None,
        ),
    ]

    mkdocs_env = os.environ.copy()
    mkdocs_env["NO_MKDOCS_2_WARNING"] = "1"
    steps.append(
        (
            "MkDocs strict HTML build",
            [
                sys.executable,
                "-m",
                "mkdocs",
                "build",
                "--strict",
                "--site-dir",
                str(docs_site_dir()),
            ],
            mkdocs_env,
        )
    )

    for label, args, env in steps:
        status = run_step(label, args, env)
        if status != 0:
            return status

    print("docs publish check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
