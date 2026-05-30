#!/usr/bin/env python3
"""Shared helpers for eMuleBB GitHub backlog sync scripts."""

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

OWNER = "emulebb"
ISSUE_REPO = "emulebb/emulebb"
PROJECT_TITLE = "eMuleBB Roadmap"
SPEC_BASE_URL = "https://github.com/emulebb/emulebb-tooling/blob/main"

ID_PATTERN = re.compile(r"\b(?:BUG|FEAT|REF|CI|AMUT|ARR)-\d{3}\b")

LANE_BY_TITLE = {
    "connectivity modernization": "Connectivity",
    "search and trust clarity": "Search and Trust",
    "ui power-user polish": "UI Polish",
    "startup and storage performance": "Security and Operations",
    "controller surface performance": "Security and Operations",
    "upload policy clarity": "Search and Trust",
    "security and operations": "Security and Operations",
    "product-family integration": "Planning",
    "local state and configuration planning": "Planning",
    "narrow anti-leecher review": "Anti-Leecher Review",
    "planning": "Planning",
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
    "roadmap:future": ("1d76db", "Post-0.7.3 future roadmap item"),
    "release:0.7.3-rc.1": ("0e8a16", "0.7.3 RC1 release planning"),
    "release:future": ("0e8a16", "Future release planning"),
    "release:post-0.7.3": ("0e8a16", "Post-0.7.3 release planning"),
    "release:unscheduled": ("0e8a16", "Unscheduled backlog item"),
    "lane:connectivity": ("0052cc", "Connectivity modernization roadmap lane"),
    "lane:search-trust": ("5319e7", "Search and trust clarity roadmap lane"),
    "lane:ui-polish": ("d876e3", "UI power-user polish roadmap lane"),
    "lane:security-operations": ("0e8a16", "Security and operations roadmap lane"),
    "lane:anti-leecher-review": ("b60205", "Narrow anti-leecher review roadmap lane"),
    "lane:planning": ("fbca04", "Roadmap planning umbrella"),
}

MANAGED_LABEL_PREFIXES = ("type:", "priority:", "roadmap:", "release:", "lane:")

LANE_KEYWORDS = (
    (
        "Anti-Leecher Review",
        {
            "anti-leecher",
            "banning",
            "cshield",
            "quarantine",
        },
    ),
    (
        "Connectivity",
        {
            "async",
            "bind-policy",
            "cgnat",
            "connectivity",
            "dual-stack",
            "ipv6",
            "kad",
            "lowid",
            "miniupnp",
            "nat-pmp",
            "nat-traversal",
            "network",
            "network-binding",
            "network-change",
            "networking",
            "pcp",
            "relay",
            "sockets",
            "tcp",
            "transport",
            "udp",
            "upnp",
            "utp",
            "vpn",
            "wsapoll",
        },
    ),
    (
        "Search and Trust",
        {
            "blacklist",
            "browse",
            "clients",
            "download",
            "downloads",
            "duplicates",
            "fake",
            "intake",
            "search",
            "sources",
            "trust",
        },
    ),
    (
        "UI Polish",
        {
            "dark-mode",
            "dpi",
            "hdpi",
            "keyboard-shortcuts",
            "layout",
            "localization",
            "mfc",
            "polish",
            "preferences",
            "theming",
            "toolbar",
            "transfers",
            "ui",
            "visualization",
            "win10",
            "windows",
        },
    ),
    (
        "Security and Operations",
        {
            "api",
            "asan",
            "automation",
            "build",
            "controller-surface",
            "dependencies",
            "diagnostics",
            "docker",
            "evidence",
            "hardening",
            "ipfilter",
            "live-e2e",
            "memory-safety",
            "openapi",
            "packaging",
            "release",
            "release-gate",
            "release-proof",
            "rest",
            "sanitizer",
            "security",
            "test-campaigns",
            "test-harness",
            "testing",
            "tooling",
            "warnings",
            "webserver",
        },
    ),
    (
        "Planning",
        {
            "configuration",
            "database",
            "future-roadmap",
            "planning",
            "p2p-overlord",
            "product-family",
            "sqlite",
        },
    ),
)


@dataclass(frozen=True)
class Item:
    """A local backlog item plus the GitHub metadata derived from it."""

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
            f"release:{self.project_release_label}",
            LANE_LABELS[self.lane],
        ]
        if self.item_id == "FEAT-064":
            labels[0] = "type:planning"
        return sorted(set(labels))

    @property
    def project_release(self) -> str:
        value = self.milestone.strip()
        if value in {"", "~"}:
            return "unscheduled"
        if value == "0.7.3 RC1":
            return "0.7.3-rc.1"
        if value == "future-release":
            return "future"
        return value

    @property
    def project_release_label(self) -> str:
        return self.project_release.lower().replace(" ", "-")


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
    """Return active backlog item IDs mapped to their approved lane."""

    lanes: dict[str, str] = {}
    text = read_text(FUTURE_ROADMAP)
    section_pattern = re.compile(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", re.MULTILINE | re.DOTALL)
    for match in section_pattern.finditer(text):
        lane_title = match.group(1).strip()
        lane = LANE_BY_TITLE.get(lane_title.casefold())
        if not lane:
            continue
        for item_id in ID_PATTERN.findall(match.group(2)):
            if (ACTIVE_ITEMS / f"{item_id}.md").exists():
                lanes[item_id] = lane

    table_pattern = re.compile(r"^\| ([^|]+) \| [^|]+ \| ([^|]+) \|$", re.MULTILINE)
    for match in table_pattern.finditer(text):
        lane_title = match.group(1).strip()
        lane = LANE_BY_TITLE.get(lane_title.casefold())
        if not lane:
            continue
        for item_id in ID_PATTERN.findall(match.group(2)):
            if (ACTIVE_ITEMS / f"{item_id}.md").exists():
                lanes[item_id] = lane
    lanes["FEAT-064"] = "Planning"
    return dict(sorted(lanes.items()))


def infer_lane(fields: dict[str, str]) -> str:
    """Return a deterministic Project lane for an active item."""

    if fields.get("category", "") == "ci":
        return "Security and Operations"

    text = " ".join(
        [
            fields.get("id", ""),
            fields.get("title", ""),
            fields.get("category", ""),
            " ".join(parse_label_list(fields.get("labels", ""))),
        ]
    ).casefold()
    tokens = set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text))
    for lane, keywords in LANE_KEYWORDS:
        if tokens & keywords:
            return lane
    return "Planning"


def load_items() -> list[Item]:
    """Load all active backlog items from local docs."""

    lane_by_id = active_item_ids_by_lane()
    items: list[Item] = []
    for path in sorted(ACTIVE_ITEMS.glob("*.md")):
        text = read_text(path)
        fields = parse_frontmatter(text)
        item_id = fields.get("id", path.stem)
        lane = lane_by_id.get(item_id) or infer_lane(fields)
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
    """Build the canonical GitHub issue body for an imported backlog item."""

    local_status_note = (
        "This issue is the authoritative workflow record. The linked local "
        "document is retained as an engineering spec/evidence record."
    )
    return "\n".join(
        [
            f"Imported backlog item `{item.item_id}`.",
            "",
            f"- Lane: `{item.lane}`",
            f"- Type: `{item.project_type}`",
            f"- Priority: `{item.priority}`",
            f"- Release: `{item.project_release}`",
            f"- Local spec: {item.spec_url}",
            "",
            local_status_note,
            "",
            "Before implementation, revalidate this slice against current `main`, "
            "current dependency pins, and `WORKSPACE-POLICY.md`.",
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
