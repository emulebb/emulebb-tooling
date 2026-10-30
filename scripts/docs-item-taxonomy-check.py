#!/usr/bin/env python3
"""Validate current Rust item records and the compact legacy ID catalog."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RUST = DOCS / "products" / "emulebb-rust"
RUST_ACTIVE = RUST / "active" / "items"
RUST_HISTORY = RUST / "history" / "items"
LEGACY_CATALOG = DOCS / "history" / "LEGACY-ITEM-CATALOG.md"

ACTIVE_STATUSES = {"OPEN", "IN_PROGRESS", "BLOCKED"}
CLOSED_STATUSES = {"DONE", "PASSED", "WONT_DO"}
RECORDED_STATUSES = ACTIVE_STATUSES | CLOSED_STATUSES | {"DEFERRED"}
REQUIRED_ACTIVE_FIELDS = (
    "id",
    "title",
    "status",
    "priority",
    "category",
    "labels",
    "milestone",
    "created",
    "source",
)
RUST_ID = re.compile(r"^RUST-(?:BUG|FEAT|REF|CI)-\d{3}$")
LEGACY_ID = re.compile(r"^(?:BUG|FEAT|REF|CI|AMUT|ARR)-\d{3}$")
CATALOG_ROW = re.compile(
    r"^\| `([A-Z]+-\d{3,})` \| ([^|]+) \| ([^|]+) \| (.*?) \|$",
    re.MULTILINE,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        fields[name.strip()] = value.strip()
    return fields


def check_catalog(errors: list[str], ids: defaultdict[str, list[Path]]) -> int:
    text = read_text(LEGACY_CATALOG)
    rows = list(CATALOG_ROW.finditer(text))
    if not rows:
        errors.append(f"{LEGACY_CATALOG}: no legacy item rows found")
        return 0

    for row in rows:
        item_id = row.group(1)
        status = row.group(2).strip()
        if not LEGACY_ID.fullmatch(item_id):
            errors.append(f"{LEGACY_CATALOG}: invalid legacy item id {item_id!r}")
        if status not in RECORDED_STATUSES:
            errors.append(
                f"{LEGACY_CATALOG}: unsupported recorded status {status!r} for {item_id}"
            )
        ids[item_id].append(LEGACY_CATALOG)
    return len(rows)


def check_rust_items(
    root: Path,
    active: bool,
    errors: list[str],
    ids: defaultdict[str, list[Path]],
) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for path in sorted(root.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        fields = parse_frontmatter(read_text(path))
        item_id = fields.get("id", "")
        status = fields.get("status", "").upper().replace("-", "_")
        if status == "WONT_FIX":
            status = "WONT_DO"
        if not item_id:
            errors.append(f"{path}: missing id frontmatter")
            continue
        if path.stem != item_id:
            errors.append(f"{path}: filename stem must match id {item_id!r}")
        if item_id != "CI-054" and not RUST_ID.fullmatch(item_id):
            errors.append(f"{path}: invalid Rust item id {item_id!r}")
        if item_id == "CI-054" and path.parent != RUST_ACTIVE:
            errors.append(f"{path}: CI-054 is allowed only as the active migration exception")
        if active:
            missing = [name for name in REQUIRED_ACTIVE_FIELDS if not fields.get(name)]
            if missing:
                errors.append(f"{path}: missing active fields {', '.join(missing)}")
            if status not in ACTIVE_STATUSES:
                errors.append(f"{path}: active status must be OPEN, IN_PROGRESS, or BLOCKED")
        elif status and status not in CLOSED_STATUSES:
            errors.append(f"{path}: historical status must be closed, got {status!r}")
        ids[item_id].append(path)
        found[item_id] = path
    return found


def check_rust_index(active_paths: dict[str, Path], errors: list[str]) -> int:
    text = read_text(RUST / "active" / "INDEX.md")
    rows = {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"^\| \[([A-Z]+(?:-[A-Z]+)?-\d+)\]\((items/[^)]+)\) \|",
            text,
            re.MULTILINE,
        )
    }
    for item_id, path in sorted(active_paths.items()):
        expected = f"items/{path.name}"
        actual = rows.get(item_id)
        if actual != expected:
            errors.append(
                f"{item_id}: Rust active index link is {actual!r}, expected {expected!r}"
            )
    for item_id in sorted(rows):
        if item_id not in active_paths:
            errors.append(f"{item_id}: Rust active index row has no active item file")
    return len(rows)


def main() -> int:
    errors: list[str] = []
    ids: defaultdict[str, list[Path]] = defaultdict(list)

    legacy_count = check_catalog(errors, ids)
    active_paths = check_rust_items(RUST_ACTIVE, True, errors, ids)
    history_paths = check_rust_items(RUST_HISTORY, False, errors, ids)
    row_count = check_rust_index(active_paths, errors)

    obsolete_active = DOCS / "active" / "items"
    if obsolete_active.exists():
        errors.append(f"{obsolete_active}: central active item directory must not exist")

    for item_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            joined = ", ".join(str(path.relative_to(ROOT)) for path in paths)
            errors.append(f"{item_id}: duplicate reserved id in {joined}")

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    print(
        f"checked {legacy_count} legacy ids, {len(active_paths)} active Rust items, "
        f"{len(history_paths)} closed Rust items, {row_count} Rust index rows"
    )
    if errors:
        print(f"errors: {len(errors)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
