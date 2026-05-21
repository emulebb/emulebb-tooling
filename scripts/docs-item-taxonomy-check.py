#!/usr/bin/env python3
"""Validate eMule tooling backlog item IDs and statuses."""

from __future__ import annotations

import re
import sys
from collections import Counter
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

ALLOWED_PREFIXES = {"BUG", "FEAT", "REF", "CI", "AMUT", "ARR"}
ACTIVE_STATUSES = {"OPEN", "IN_PROGRESS", "BLOCKED", "DEFERRED"}
CLOSED_STATUSES = {"DONE", "PASSED", "WONT_DO"}
ALLOWED_STATUSES = ACTIVE_STATUSES | CLOSED_STATUSES
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
LEGACY_STATUS_MAP = {
    "Open": "OPEN",
    "In Progress": "IN_PROGRESS",
    "Blocked": "BLOCKED",
    "Deferred": "DEFERRED",
    "Done": "DONE",
    "Passed": "PASSED",
    "Wont-Fix": "WONT_DO",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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


def frontmatter_field(text: str, name: str) -> str:
    return parse_frontmatter(text).get(name, "")


def item_files() -> list[Path]:
    return sorted((DOCS / "active" / "items").glob("*.md")) + sorted(
        (DOCS / "history" / "items").glob("*.md")
    )


def parse_active_index() -> dict[str, dict[str, str]]:
    text = read_text(DOCS / "active" / "INDEX.md")
    rows: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r"^\| \[([A-Z]+-\d+)\]\(([^)]+)\) \| ([^|]+) \| ([^|]+) \| (.*?) \|$",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        rows[match.group(1)] = {
            "link": match.group(2),
            "priority": match.group(3).strip(),
            "status": match.group(4).strip(),
            "title": match.group(5).strip(),
        }
    return rows


def item_sort_key(item_id: str) -> tuple[str, int]:
    prefix, number = item_id.split("-", 1)
    return prefix, int(number)


def check_active_index_order(errors: list[str]) -> None:
    text = read_text(DOCS / "active" / "INDEX.md")
    section_heading = re.compile(r"^## (.+)$", re.MULTILINE)
    headings = list(section_heading.finditer(text))
    row_pattern = re.compile(
        r"^\| \[([A-Z]+-\d+)\]\([^)]+\) \| [^|]+ \| [^|]+ \| .*? \|$",
        re.MULTILINE,
    )

    for index, heading in enumerate(headings):
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[start:end]
        item_ids = [match.group(1) for match in row_pattern.finditer(section)]
        if len(item_ids) < 2:
            continue
        expected = sorted(item_ids, key=item_sort_key)
        if item_ids != expected:
            section_name = heading.group(1).strip()
            errors.append(
                "docs/active/INDEX.md: item rows in section "
                f"{section_name!r} are not sorted by item id"
            )


def check_active_snapshot_counts(
    active_paths: dict[str, Path], errors: list[str]
) -> None:
    text = read_text(DOCS / "active" / "INDEX.md")
    counts = Counter()
    for path in active_paths.values():
        status = frontmatter_field(read_text(path), "status")
        if status in ACTIVE_STATUSES:
            counts[status] += 1

    total = sum(counts.values())
    total_match = re.search(r"\*\*Current non-done count:\*\* `(\d+)`", text)
    if not total_match:
        errors.append("docs/active/INDEX.md: missing current non-done count")
    elif int(total_match.group(1)) != total:
        errors.append(
            "docs/active/INDEX.md: current non-done count does not match "
            f"active items ({total_match.group(1)} != {total})"
        )

    status_match = re.search(
        r"\*\*Non-done by status:\*\* `(\d+)` OPEN, `(\d+)` IN_PROGRESS, "
        r"`(\d+)` DEFERRED, `(\d+)` BLOCKED\.",
        text,
    )
    if not status_match:
        errors.append("docs/active/INDEX.md: missing canonical non-done status counts")
        return

    expected = [
        counts["OPEN"],
        counts["IN_PROGRESS"],
        counts["DEFERRED"],
        counts["BLOCKED"],
    ]
    actual = [int(value) for value in status_match.groups()]
    if actual != expected:
        errors.append(
            "docs/active/INDEX.md: non-done status counts do not match "
            f"active items ({actual} != {expected})"
        )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    ids: defaultdict[str, list[Path]] = defaultdict(list)

    id_pattern = re.compile(r"^([A-Z]+)-(\d{3,})$")

    for path in item_files():
        text = read_text(path)
        item_id = frontmatter_field(text, "id")
        status = frontmatter_field(text, "status")
        is_active = "docs/active/items" in path.as_posix()

        if not item_id:
            errors.append(f"{path}: missing id frontmatter")
            continue

        ids[item_id].append(path)
        if path.stem != item_id:
            errors.append(f"{path}: filename stem must match id frontmatter {item_id!r}")
        match = id_pattern.match(item_id)
        if not match:
            errors.append(f"{path}: id must match PREFIX-###, got {item_id!r}")
        elif match.group(1) not in ALLOWED_PREFIXES:
            errors.append(f"{path}: unsupported item prefix {match.group(1)!r}")

        if is_active:
            fields = parse_frontmatter(text)
            missing = [name for name in REQUIRED_ACTIVE_FIELDS if not fields.get(name)]
            if missing:
                errors.append(
                    f"{path}: missing required active frontmatter fields "
                    + ", ".join(missing)
                )
            if status not in ALLOWED_STATUSES:
                errors.append(f"{path}: active status must be canonical, got {status!r}")
        elif status and status not in ALLOWED_STATUSES:
            canonical = LEGACY_STATUS_MAP.get(status)
            if canonical:
                warnings.append(f"{path}: legacy status {status!r} maps to {canonical!r}")
            else:
                errors.append(f"{path}: unknown historical status {status!r}")

    for item_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            joined = ", ".join(str(path.relative_to(ROOT)) for path in paths)
            errors.append(f"{item_id}: duplicate frontmatter id in {joined}")

    rows = parse_active_index()
    active_paths = {path.stem: path for path in (DOCS / "active" / "items").glob("*.md")}
    check_active_snapshot_counts(active_paths, errors)
    check_active_index_order(errors)

    for item_id, path in sorted(active_paths.items()):
        row = rows.get(item_id)
        text = read_text(path)
        if not row:
            errors.append(f"{item_id}: active item missing from docs/active/INDEX.md")
            continue
        if not row["link"].startswith("items/"):
            errors.append(f"{item_id}: active index row must link to items/, got {row['link']!r}")
        if row["status"] != frontmatter_field(text, "status"):
            errors.append(f"{item_id}: index status does not match item frontmatter")
        if row["priority"] != frontmatter_field(text, "priority"):
            errors.append(f"{item_id}: index priority does not match item frontmatter")
        if row["title"] != frontmatter_field(text, "title"):
            errors.append(f"{item_id}: index title does not match item frontmatter")

    for item_id, row in sorted(rows.items()):
        status = row["status"]
        if status not in ALLOWED_STATUSES:
            errors.append(f"{item_id}: active index uses unsupported status {status!r}")
        if status in ACTIVE_STATUSES and not row["link"].startswith("items/"):
            errors.append(f"{item_id}: non-closed status links outside active items")
        if status in CLOSED_STATUSES and row["link"].startswith("items/"):
            errors.append(f"{item_id}: closed status links into active items")

    max_warnings = 20
    for warning in warnings[:max_warnings]:
        print(f"warning: {warning}")
    if len(warnings) > max_warnings:
        print(f"warning: {len(warnings) - max_warnings} additional historical warnings suppressed")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    print(
        f"checked {len(ids)} item ids, {len(active_paths)} active items, "
        f"{len(rows)} active index rows"
    )
    if warnings:
        print(f"warnings: {len(warnings)}")
    if errors:
        print(f"errors: {len(errors)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
