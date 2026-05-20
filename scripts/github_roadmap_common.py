#!/usr/bin/env python3
"""Shared helpers for eMule BB GitHub roadmap migration scripts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ACTIVE_ITEMS = DOCS / "active" / "items"
FUTURE_ROADMAP = DOCS / "active" / "FUTURE-ROADMAP.md"

OWNER = "eMulebb"
ISSUE_REPO = "eMulebb/eMule"
PROJECT_TITLE = "eMule BB Roadmap"
PROJECT_RELEASE = "post-beta-0.7.3"
SPEC_BASE_URL = "https://github.com/eMulebb/eMule-tooling/blob/main"

ID_PATTERN = re.compile(r"\b(?:BUG|FEAT|REF|CI|AMUT|ARR)-\d{3}\b")

LANE_BY_TITLE = {
    "Connectivity modernization": "Connectivity",
    "Search and trust clarity": "Search and Trust",
    "UI power-user polish": "UI Polish",
    "Security and operations": "Security and Operations",
    "Narrow anti-leecher review": "Anti-Leecher Review",
}

STATUS_TO_PROJECT = {
    "OPEN": "Ready",
    "IN_PROGRESS": "In Progress",
    "BLOCKED": "Blocked",
    "DEFERRED": "Deferred",
}

CATEGORY_TO_TYPE = {
    "bug": "Bug",
    "feature": "Feature",
    "refactor": "Refactor",
    "ci": "CI",
}

TYPE_LABELS = {
    "bug": "type:bug",
    "feature": "type:feature",
    "refactor": "type:refactor",
    "ci": "type:ci",
    "planning": "type:planning",
}

LANE_LABELS = {
    "Connectivity": "lane:connectivity",
    "Search and Trust": "lane:search-trust",
    "UI Polish": "lane:ui-polish",
    "Security and Operations": "lane:security-operations",
    "Anti-Leecher Review": "lane:anti-leecher-review",
    "Planning": "lane:planning",
}

LABEL_DEFINITIONS = {
    "type:feature": ("a2eeef", "Product behavior, UX, or capability work"),
    "type:refactor": ("c5def5", "Internal modernization or architecture cleanup"),
    "type:ci": ("5319e7", "Build, validation, packaging, or release tooling"),
    "type:bug": ("d73a4a", "Runtime or user-visible correctness defect"),
    "type:planning": ("fbca04", "Roadmap, scope, or planning umbrella"),
    "priority:critical": ("b60205", "Critical priority"),
    "priority:major": ("d93f0b", "Major priority"),
    "priority:minor": ("fbca04", "Minor priority"),
    "priority:trivial": ("cfd3d7", "Trivial priority"),
    "roadmap:future": ("1d76db", "Post-beta future roadmap item"),
    "release:post-beta-0.7.3": ("0e8a16", "Post-beta 0.7.3 release planning"),
    "lane:connectivity": ("0052cc", "Connectivity modernization roadmap lane"),
    "lane:search-trust": ("5319e7", "Search and trust clarity roadmap lane"),
    "lane:ui-polish": ("d876e3", "UI power-user polish roadmap lane"),
    "lane:security-operations": ("0e8a16", "Security and operations roadmap lane"),
    "lane:anti-leecher-review": ("b60205", "Narrow anti-leecher review roadmap lane"),
    "lane:planning": ("fbca04", "Roadmap planning umbrella"),
}


@dataclass(frozen=True)
class Item:
    """A local roadmap item plus the GitHub metadata derived from it."""

    item_id: str
    title: str
    status: str
    priority: str
    category: str
    labels: tuple[str, ...]
    milestone: str
    lane: str
    path: Path
    github_issue: str
    workflow: str

    @property
    def issue_title(self) -> str:
        return f"{self.item_id}: {self.title}"

    @property
    def project_status(self) -> str:
        if self.item_id == "FEAT-064":
            return "Ready"
        return STATUS_TO_PROJECT.get(self.status, "Triage")

    @property
    def project_type(self) -> str:
        if self.item_id == "FEAT-064":
            return "Planning"
        return CATEGORY_TO_TYPE.get(self.category, "Planning")

    @property
    def spec_url(self) -> str:
        rel_path = self.path.relative_to(ROOT).as_posix()
        return f"{SPEC_BASE_URL}/{rel_path}"

    @property
    def github_labels(self) -> list[str]:
        labels = [
            TYPE_LABELS.get(self.category, "type:planning"),
            f"priority:{self.priority.lower()}",
            "roadmap:future",
            "release:post-beta-0.7.3",
            LANE_LABELS[self.lane],
        ]
        if self.item_id == "FEAT-064":
            labels[0] = "type:planning"
        return sorted(set(labels))


def read_text(path: Path) -> str:
    """Read a UTF-8 text file while tolerating historical byte drift."""

    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, text: str) -> None:
    """Write normalized UTF-8 LF text with a final newline."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse the simple scalar front matter used by backlog item docs."""

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


def parse_label_list(raw_value: str) -> tuple[str, ...]:
    """Parse bracket-style label front matter without a YAML dependency."""

    value = raw_value.strip()
    if not value.startswith("[") or not value.endswith("]"):
        return tuple()
    entries = [entry.strip() for entry in value[1:-1].split(",")]
    return tuple(entry for entry in entries if entry)


def active_item_ids_by_lane() -> dict[str, str]:
    """Return active roadmap item IDs mapped to their approved lane."""

    lanes: dict[str, str] = {}
    table_pattern = re.compile(r"^\| ([^|]+) \| [^|]+ \| ([^|]+) \|$", re.MULTILINE)
    text = read_text(FUTURE_ROADMAP)
    for match in table_pattern.finditer(text):
        lane_title = match.group(1).strip()
        lane = LANE_BY_TITLE.get(lane_title)
        if not lane:
            continue
        for item_id in ID_PATTERN.findall(match.group(2)):
            if (ACTIVE_ITEMS / f"{item_id}.md").exists():
                lanes[item_id] = lane
    lanes["FEAT-064"] = "Planning"
    return dict(sorted(lanes.items()))


def load_items() -> list[Item]:
    """Load first-rollout future-roadmap items from local docs."""

    lane_by_id = active_item_ids_by_lane()
    items: list[Item] = []
    for item_id, lane in lane_by_id.items():
        path = ACTIVE_ITEMS / f"{item_id}.md"
        text = read_text(path)
        fields = parse_frontmatter(text)
        items.append(
            Item(
                item_id=item_id,
                title=fields.get("title", ""),
                status=fields.get("status", ""),
                priority=fields.get("priority", ""),
                category=fields.get("category", ""),
                labels=parse_label_list(fields.get("labels", "")),
                milestone=fields.get("milestone", ""),
                lane=lane,
                path=path,
                github_issue=fields.get("github_issue", ""),
                workflow=fields.get("workflow", ""),
            )
        )
    return items


def run_gh(args: Iterable[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    """Run a GitHub CLI command and return the completed process."""

    command = ["gh", *args]
    return subprocess.run(
        command,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT,
        check=False,
    )


def require_success(result: subprocess.CompletedProcess[str], action: str) -> str:
    """Return stdout or exit with a clear GitHub CLI failure message."""

    if result.returncode == 0:
        return result.stdout
    print(f"error: {action} failed", file=sys.stderr)
    if result.stdout.strip():
        print(result.stdout.strip(), file=sys.stderr)
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    raise SystemExit(result.returncode)


def load_json(result: subprocess.CompletedProcess[str], action: str) -> object:
    """Load JSON stdout from a successful GitHub CLI command."""

    stdout = require_success(result, action)
    return json.loads(stdout) if stdout.strip() else {}


def issue_body(item: Item) -> str:
    """Build the canonical GitHub issue body for an imported roadmap item."""

    local_status_note = (
        "This issue is the authoritative workflow record. The linked local "
        "document is retained as an engineering spec/evidence record."
    )
    return "\n".join(
        [
            f"Imported roadmap item `{item.item_id}`.",
            "",
            f"- Lane: `{item.lane}`",
            f"- Type: `{item.project_type}`",
            f"- Priority: `{item.priority}`",
            f"- Release: `{PROJECT_RELEASE}`",
            f"- Local spec: {item.spec_url}",
            "",
            local_status_note,
            "",
            "Before implementation, revalidate this slice against current `main`, "
            "current dependency pins, and `WORKSPACE_POLICY.md`.",
        ]
    )


def update_item_github_metadata(item: Item, issue_url: str) -> bool:
    """Insert or refresh GitHub workflow metadata in a local item doc."""

    text = read_text(item.path)
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---", 4)
    if end == -1:
        return False

    lines = text[4:end].splitlines()
    values = {"workflow": "github", "github_issue": issue_url}
    seen = set()
    updated: list[str] = []
    inserted_after_id = False

    for line in lines:
        if ":" not in line:
            updated.append(line)
            continue
        name, _ = line.split(":", 1)
        key = name.strip()
        if key in values:
            updated.append(f"{key}: {values[key]}")
            seen.add(key)
        else:
            updated.append(line)
        if key == "id":
            for meta_key in ("workflow", "github_issue"):
                if meta_key not in seen and not any(
                    existing.split(":", 1)[0].strip() == meta_key
                    for existing in lines
                    if ":" in existing
                ):
                    updated.append(f"{meta_key}: {values[meta_key]}")
                    seen.add(meta_key)
            inserted_after_id = True

    if not inserted_after_id:
        for meta_key in ("workflow", "github_issue"):
            if meta_key not in seen:
                updated.insert(0, f"{meta_key}: {values[meta_key]}")

    body = text[end:]
    note = (
        "\n\n> Workflow status is tracked in GitHub: "
        f"{issue_url}. This local document is retained as an engineering "
        "spec/evidence record.\n"
    )
    if "Workflow status is tracked in GitHub" not in body:
        body = body.replace("\n---\n", "\n---\n" + note, 1)
    new_text = "---\n" + "\n".join(updated) + body
    if new_text == text:
        return False
    write_text(item.path, new_text)
    return True
