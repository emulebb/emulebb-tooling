#!/usr/bin/env python3
"""Audit current eMule tooling Markdown structure and browser readability."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WIDE_TABLE_WARN_LIMIT = 180
MAX_WIDE_TABLE_WARNINGS = 50

CURRENT_DOC_DIRS = {
    "active",
    "dependencies",
    "reference",
    "rest",
}
NAV_REQUIRED_DIRS = {
    "dependencies",
    "reference",
    "rest",
}


@dataclass(frozen=True)
class WideTableRow:
    """A Markdown table row whose raw width can render poorly in browsers."""

    path: Path
    line_number: int
    width: int
    sample: str


def read_text(path: Path) -> str:
    """Read a UTF-8 Markdown file while tolerating historical byte drift."""

    return path.read_text(encoding="utf-8", errors="ignore")


def current_markdown_files() -> list[Path]:
    """Return Markdown files that belong to the current documentation surface."""

    files = [DOCS / name for name in ("HELP.md", "INDEX.md", "DOCS-POLICY.md", "WORKSPACE-POLICY.md", "HISTORICAL-REFERENCES.md")]
    for dirname in sorted(CURRENT_DOC_DIRS):
        root = DOCS / dirname
        if root.exists():
            files.extend(sorted(root.rglob("*.md")))
    return sorted(path for path in files if path.exists())


def is_item_doc(path: Path) -> bool:
    """Return whether a path is an active backlog item record."""

    return path.parent == DOCS / "active" / "items"


def is_current_doc(path: Path) -> bool:
    """Return whether a Markdown file is part of the current-doc audit surface."""

    if path.parent == DOCS:
        return True
    relative = path.relative_to(DOCS)
    return bool(relative.parts) and relative.parts[0] in CURRENT_DOC_DIRS


def is_upper_slug(name: str) -> bool:
    """Return whether a filename stem follows the current UPPER-SLUG convention."""

    stem = name.removesuffix(".md")
    return bool(re.fullmatch(r"[A-Z0-9]+(?:[.-][A-Z0-9]+)*", stem))


def check_filename(path: Path, errors: list[str]) -> None:
    """Validate current-doc filename conventions."""

    if not is_current_doc(path):
        return
    if is_item_doc(path):
        if not re.fullmatch(r"(?:BUG|FEAT|REF|CI|AMUT|ARR)-\d{3,}", path.stem):
            errors.append(f"{path.relative_to(ROOT)}: active item filename must be an item ID")
        return
    if not is_upper_slug(path.name):
        errors.append(f"{path.relative_to(ROOT)}: current Markdown filename must be UPPER-SLUG")


def check_heading(path: Path, errors: list[str]) -> None:
    """Validate that current non-item docs have exactly one top-level heading."""

    if is_item_doc(path):
        return
    headings = [line for line in read_text(path).splitlines() if line.startswith("# ")]
    if len(headings) != 1:
        errors.append(
            f"{path.relative_to(ROOT)}: expected exactly one top-level heading, found {len(headings)}"
        )


def check_index_navigation(errors: list[str]) -> None:
    """Validate that current reference/rest/dependency docs are linked from docs/INDEX.md."""

    index_text = read_text(DOCS / "INDEX.md")
    for dirname in sorted(NAV_REQUIRED_DIRS):
        for path in sorted((DOCS / dirname).glob("*.md")):
            rel = path.relative_to(DOCS).as_posix()
            if rel not in index_text:
                errors.append(f"docs/INDEX.md: missing navigation link for {rel}")


def find_wide_table_rows(limit: int) -> list[WideTableRow]:
    """Return current-doc Markdown table rows wider than the configured limit."""

    rows: list[WideTableRow] = []
    for path in current_markdown_files():
        for line_number, line in enumerate(read_text(path).splitlines(), 1):
            if line.startswith("|") and line.endswith("|") and len(line) > limit:
                rows.append(
                    WideTableRow(
                        path=path,
                        line_number=line_number,
                        width=len(line),
                        sample=line[:160],
                    )
                )
    return sorted(rows, key=lambda row: (-row.width, str(row.path), row.line_number))


def main() -> int:
    """Run the Markdown structure audit."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wide-table-limit",
        type=int,
        default=WIDE_TABLE_WARN_LIMIT,
        help=f"raw table-row width that triggers a warning (default: {WIDE_TABLE_WARN_LIMIT})",
    )
    parser.add_argument(
        "--fail-on-wide-tables",
        action="store_true",
        help="treat wide Markdown table rows as errors instead of warnings",
    )
    args = parser.parse_args()

    errors: list[str] = []
    for path in current_markdown_files():
        check_filename(path, errors)
        check_heading(path, errors)
    check_index_navigation(errors)

    wide_rows = find_wide_table_rows(args.wide_table_limit)
    for row in wide_rows[:MAX_WIDE_TABLE_WARNINGS]:
        message = (
            f"{row.path.relative_to(ROOT)}:{row.line_number}: table row is "
            f"{row.width} chars wide: {row.sample}"
        )
        if args.fail_on_wide_tables:
            errors.append(message)
        else:
            print(f"warning: {message}")
    if len(wide_rows) > MAX_WIDE_TABLE_WARNINGS:
        print(
            "warning: "
            f"{len(wide_rows) - MAX_WIDE_TABLE_WARNINGS} additional wide table rows suppressed"
        )

    print(
        f"checked {len(current_markdown_files())} current Markdown docs, "
        f"{len(wide_rows)} wide table rows over {args.wide_table_limit} chars"
    )

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"errors: {len(errors)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
