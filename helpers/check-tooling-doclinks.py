#!/usr/bin/env python3
"""Validate that rendered-doc deep links resolve to emulebb-tooling sources.

Public surfaces such as the org profile README (``emulebb-org-profile``) and the
marketing site (``emulebb-pages``) link into the rendered MkDocs documentation at
``https://emulebb.github.io/emulebb-tooling/<path>/``. Each rendered URL maps back
to a Markdown (or static) source under ``emulebb-tooling/docs/<path>``. When a doc
is renamed, moved, or archived, those links silently 404. This checker re-derives
every source path and fails when one is missing, so the cross-repo links can be
guarded in CI instead of rotting unnoticed.

Usage:
    python helpers/check-tooling-doclinks.py [--docs-root DIR] PATH [PATH ...]

PATH may be a file or a directory. Directories are scanned recursively for
``*.html`` and ``*.md`` files. With no PATH, the tooling docs tree is scanned.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SITE_DOCS_BASE = "https://emulebb.github.io/emulebb-tooling/"
# Capture the path segment after the rendered-docs base. The path charset is
# restricted to URL-path-safe characters so URL fragments embedded in prose,
# backtick spans, or regex/code samples do not produce spurious matches.
LINK_RE = re.compile(r"https://emulebb\.github\.io/emulebb-tooling/([A-Za-z0-9._/\-]*)")
SCAN_SUFFIXES = (".html", ".md")
# Suffixes that denote a literal static asset served as-is (not a rendered page).
# Anything else - including version-dotted page names like RELEASE-0.7.3 - is a
# directory-style rendered page that maps to a Markdown source.
STATIC_SUFFIXES = frozenset(
    {".yaml", ".yml", ".json", ".xml", ".txt", ".png", ".svg", ".ico", ".css", ".js"}
)


def url_path_to_source(url_path: str, docs_root: Path) -> Path:
    """Map a rendered-doc URL path to its expected source file under docs_root."""
    clean = url_path.strip().strip("/")
    if clean == "" or clean.lower() == "index":
        return docs_root / "INDEX.md"
    if Path(clean).suffix.lower() in STATIC_SUFFIXES:
        return docs_root / clean
    return docs_root / f"{clean}.md"


def iter_inputs(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            for suffix in SCAN_SUFFIXES:
                files.extend(p for p in path.rglob(f"*{suffix}") if ".git" not in p.parts)
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(f"Input path does not exist: {path}")
    return sorted(set(files))


def check_file(path: Path, docs_root: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for url_path in dict.fromkeys(LINK_RE.findall(text)):  # de-dup, preserve order
        source = url_path_to_source(url_path, docs_root)
        if not source.exists():
            errors.append(
                f"{path}: {SITE_DOCS_BASE}{url_path} -> missing source {source}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_docs_root = Path(__file__).resolve().parents[1] / "docs"
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=default_docs_root,
        help="Root of the emulebb-tooling docs tree (default: this repo's docs/).",
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="Files or directories to scan (default: the docs tree itself).",
    )
    args = parser.parse_args()

    docs_root = args.docs_root.resolve()
    if not docs_root.is_dir():
        print(f"error: docs root not found: {docs_root}", file=sys.stderr)
        return 2

    inputs = args.inputs or [docs_root]
    files = iter_inputs([p.resolve() for p in inputs])

    errors: list[str] = []
    for path in files:
        errors.extend(check_file(path, docs_root))

    if errors:
        print("Broken emulebb-tooling rendered-doc links:")
        for err in errors:
            print(f"  {err}")
        print(f"\n{len(errors)} broken link(s) across {len(files)} file(s).")
        return 1

    print(f"OK: all emulebb-tooling rendered-doc links resolve ({len(files)} file(s) scanned).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
