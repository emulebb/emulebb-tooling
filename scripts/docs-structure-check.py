#!/usr/bin/env python3
"""Audit current eMule tooling Markdown structure and browser readability."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WIDE_TABLE_WARN_LIMIT = 180
MAX_WIDE_TABLE_WARNINGS = 50
AGENT_CHECKLIST_REL = "reference/AGENT-CHECKLIST.md"

# Exact-content baseline for legacy current-doc table rows that predate the
# strict wide-table gate.  The path plus SHA-256 digest permits only these rows;
# edits or additional wide rows remain failures under --fail-on-wide-tables.
WIDE_TABLE_BASELINE = (
    (
        "docs/active/FROZEN-SURFACES.md",
        "cfd6fd3a937cae947313b76e652ac3cd14c4a263d9f85bb3bf4addbbba5fed2f",
    ),
    (
        "docs/active/FROZEN-SURFACES.md",
        "9822d0888233904142879627b201092104451f966a80c42175aa0cc98686124a",
    ),
    (
        "docs/active/FROZEN-SURFACES.md",
        "5272d88706fbbb34a0bb5995f941db1ab891f8cac9d579f5692e2ddcac8a2172",
    ),
    (
        "docs/active/FROZEN-SURFACES.md",
        "9c22df3730a18627571360d0055bf080f7243120e44f0a7750c8d41cfe3d8add",
    ),
    (
        "docs/active/FROZEN-SURFACES.md",
        "5a296e0ffbc300f02e39c5d4fef36a4732ed621efb78955cdf33d8aa67246452",
    ),
    (
        "docs/active/FUTURE-ROADMAP.md",
        "b0b92763d8327b3f4e9f31ac6f63225c2c4b1183e84f9664f2b40f4ac03d50b3",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "c38b6cb18b9a9176197762bc8dc8cb687aab6546ae288309c99d8f11276ca794",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "e3a989a98d9dd16dee6538400ea8abb68e179bca3b781fb211d1ff00efbe5dca",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "9d29cf6f519f10cf5c91cb4da8e24b0b3e9bc4a2cba42d39be7bf6a01228ea25",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "33005203d88d2338b1743884bef0a27d096fe06ae56433ea24d7f440f9d4d497",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "c48edd71721231c7f499a6fcf68ee1dcdaaaf2556b02c69087939ba0f571315b",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "df9ddb9fe5fc5c72d0ee9b345fb619ca77278261bd1651240c6a236d858ce2e4",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "c3e0b099832fea311e727d4f262eb4107cd266fb2764f2cbb4fe52ffeb4aa584",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "e95832f98a8d989e005d2eb6b4605b214099803a762beff53c2ea773cf5f51b8",
    ),
    (
        "docs/active/plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md",
        "28fd86c838ed3cdc3fe9b86bdb296efa892d541daeaa15b2fc81a84d723282e7",
    ),
    (
        "docs/active/plans/MFC-0.8.0-STARTUP-TIME-TO-INTERACTIVE.md",
        "7ec2409e43bc3e31058d00211572bccf936a8990d9879140ee028d10e18cc009",
    ),
)

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
    digest: str


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


def assert_contains(path: Path, needle: str, errors: list[str], message: str) -> None:
    """Validate that a text file contains a required reference."""

    if not path.is_file():
        errors.append(f"{path.relative_to(ROOT)}: missing required file")
        return
    if needle not in read_text(path):
        errors.append(f"{path.relative_to(ROOT)}: {message}")


def check_agent_checklist(errors: list[str]) -> None:
    """Validate that the agent checklist is present and discoverable."""

    checklist = DOCS / AGENT_CHECKLIST_REL
    if not checklist.is_file():
        errors.append(f"docs/{AGENT_CHECKLIST_REL}: missing agent checklist")
        return

    assert_contains(
        DOCS / "INDEX.md",
        AGENT_CHECKLIST_REL,
        errors,
        "missing link to agent checklist",
    )
    assert_contains(
        DOCS / "WORKSPACE-POLICY.md",
        "reference/AGENT-CHECKLIST.md",
        errors,
        "missing link to agent checklist",
    )
    assert_contains(
        DOCS / "reference" / "DEVELOPMENT-GUIDE.md",
        "AGENT-CHECKLIST.md",
        errors,
        "missing link to agent checklist",
    )
    assert_contains(
        ROOT / "README.md",
        "docs/reference/AGENT-CHECKLIST.md",
        errors,
        "missing link to agent checklist",
    )

    mkdocs = ROOT / "mkdocs.yml"
    if not mkdocs.is_file():
        errors.append("mkdocs.yml: missing required MkDocs config")
        return
    mkdocs_text = read_text(mkdocs)
    if f"Agent Checklist: {AGENT_CHECKLIST_REL}" not in mkdocs_text:
        errors.append("mkdocs.yml: missing top-level Agent Checklist nav entry")


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
                        digest=hashlib.sha256(line.encode("utf-8")).hexdigest(),
                    )
                )
    return sorted(rows, key=lambda row: (-row.width, str(row.path), row.line_number))


def main() -> int:
    """Run the Markdown structure audit."""

    # Markdown samples can carry non-cp1252 characters (em dashes, arrows); force
    # UTF-8 output so reporting them does not crash on a Windows console codepage.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass

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
    check_agent_checklist(errors)

    wide_rows = find_wide_table_rows(args.wide_table_limit)
    baseline_remaining = Counter(WIDE_TABLE_BASELINE)
    allowed_wide_rows: list[WideTableRow] = []
    unallowed_wide_rows: list[WideTableRow] = []
    for row in wide_rows:
        key = (row.path.relative_to(ROOT).as_posix(), row.digest)
        if baseline_remaining[key] > 0:
            allowed_wide_rows.append(row)
            baseline_remaining[key] -= 1
        else:
            unallowed_wide_rows.append(row)

    reported_rows = unallowed_wide_rows if args.fail_on_wide_tables else wide_rows
    for row in reported_rows[:MAX_WIDE_TABLE_WARNINGS]:
        message = (
            f"{row.path.relative_to(ROOT)}:{row.line_number}: table row is "
            f"{row.width} chars wide: {row.sample}"
        )
        if args.fail_on_wide_tables:
            errors.append(message)
        else:
            print(f"warning: {message}")
    if len(reported_rows) > MAX_WIDE_TABLE_WARNINGS:
        print(
            "warning: "
            f"{len(reported_rows) - MAX_WIDE_TABLE_WARNINGS} additional wide table rows suppressed"
        )

    if args.fail_on_wide_tables and allowed_wide_rows:
        print(
            f"allowed {len(allowed_wide_rows)} exact-content baseline wide table rows"
        )

    print(
        f"checked {len(current_markdown_files())} current Markdown docs, "
        f"{len(wide_rows)} wide table rows over {args.wide_table_limit} chars "
        f"({len(allowed_wide_rows)} baseline, {len(unallowed_wide_rows)} unallowed)"
    )

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"errors: {len(errors)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
