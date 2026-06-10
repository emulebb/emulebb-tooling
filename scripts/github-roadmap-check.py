#!/usr/bin/env python3
"""Validate eMuleBB GitHub-primary active backlog metadata."""

from __future__ import annotations

import argparse
import re
import sys

from github_roadmap_common import (
    ISSUE_REPO,
    MANAGED_LABEL_PREFIXES,
    OWNER,
    PROJECT_TITLE,
    load_items,
    load_json,
    read_text,
    run_gh,
)


def check_local_metadata(errors: list[str]) -> None:
    """Check local active specs for GitHub workflow metadata."""

    for item in load_items():
        if item.workflow == "local":
            # Explicitly local-only specs (e.g. deferred 0.8.x items, or already-shipped
            # local fixes) are exempt from GitHub-primary metadata until promoted.
            continue
        if item.workflow != "github":
            errors.append(f"{item.item_id}: missing workflow: github front matter")
        if not item.github_issue:
            errors.append(f"{item.item_id}: missing github_issue front matter")
        elif not re.match(r"^https://github\.com/emulebb/emulebb/issues/\d+$", item.github_issue):
            errors.append(f"{item.item_id}: invalid github_issue URL {item.github_issue!r}")

        text = read_text(item.path)
        if "Workflow status is tracked in GitHub" not in text:
            errors.append(f"{item.item_id}: missing GitHub workflow-status note")


def check_github_issue(item, errors: list[str]) -> None:
    """Check that the GitHub issue for one local item is discoverable."""

    result = run_gh(
        [
            "issue",
            "view",
            item.github_issue,
            "--repo",
            ISSUE_REPO,
            "--json",
            "title,url,labels",
        ]
    )
    if result.returncode != 0:
        errors.append(f"{item.item_id}: cannot read GitHub issue {item.github_issue}")
        return
    data = load_json(result, f"read issue {item.item_id}")
    if not isinstance(data, dict):
        errors.append(f"{item.item_id}: unexpected issue JSON")
        return
    title = str(data.get("title", ""))
    if item.item_id not in title:
        errors.append(f"{item.item_id}: issue title does not contain local ID")
    labels = data.get("labels", [])
    label_names = {
        str(label.get("name"))
        for label in labels
        if isinstance(label, dict) and label.get("name")
    }
    for expected in item.github_labels:
        if expected not in label_names:
            errors.append(f"{item.item_id}: missing issue label {expected}")
    for label in sorted(label_names):
        if label not in item.github_labels and label.startswith(MANAGED_LABEL_PREFIXES):
            errors.append(f"{item.item_id}: stale managed issue label {label}")


def project_number(errors: list[str]) -> str:
    """Return the roadmap project number visible to the current token."""

    result = run_gh(["project", "list", "--owner", OWNER, "--format", "json", "--limit", "100"])
    if result.returncode != 0:
        errors.append("cannot list org projects; run `gh auth refresh -s project`")
        return ""
    data = load_json(result, "list projects")
    projects = data.get("projects", []) if isinstance(data, dict) else []
    for project in projects:
        if isinstance(project, dict) and project.get("title") == PROJECT_TITLE:
            return str(project.get("number", ""))
    errors.append(f"missing org project {OWNER}/{PROJECT_TITLE}")
    return ""


def project_items_by_url(project_number_value: str, errors: list[str]) -> dict[str, dict[str, object]]:
    """Return project items keyed by GitHub issue URL."""

    if not project_number_value:
        return {}
    result = run_gh(
        [
            "project",
            "item-list",
            project_number_value,
            "--owner",
            OWNER,
            "--format",
            "json",
            "--limit",
            "200",
        ]
    )
    if result.returncode != 0:
        errors.append(f"cannot list project items for {OWNER}/{PROJECT_TITLE}")
        return {}
    data = load_json(result, "list project items")
    items = data.get("items", []) if isinstance(data, dict) else []
    by_url: dict[str, dict[str, object]] = {}
    for project_item in items:
        if not isinstance(project_item, dict):
            continue
        content = project_item.get("content")
        if isinstance(content, dict):
            url = str(content.get("url", ""))
            if url:
                by_url[url] = project_item
    return by_url


def project_item_field_value(project_item: dict[str, object], field_name: str) -> str:
    """Return a project item field value from gh's item-list JSON shape."""

    key = field_name[:1].lower() + field_name[1:]
    value = project_item.get(key, "")
    if isinstance(value, dict):
        option = value.get("name")
        if option:
            return str(option)
    return str(value) if value is not None else ""


def check_project_item(item, project_items: dict[str, dict[str, object]], errors: list[str]) -> None:
    """Check that one GitHub-primary item is present in Project #2 with fields."""

    project_item = project_items.get(item.github_issue)
    if not project_item:
        errors.append(f"{item.item_id}: missing Project #2 item")
        return
    expected_values = {
        "Roadmap Status": item.project_status,
        "Work Type": item.project_type,
        "Priority": item.priority,
        "Lane": item.lane,
        "Local ID": item.item_id,
        "Release": item.project_release,
    }
    for field_name, expected in expected_values.items():
        actual = project_item_field_value(project_item, field_name)
        if actual != expected:
            errors.append(f"{item.item_id}: Project #2 {field_name} is {actual!r}, expected {expected!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--github",
        action="store_true",
        help="also query GitHub issues and org project visibility",
    )
    args = parser.parse_args()

    errors: list[str] = []
    check_local_metadata(errors)
    if args.github:
        number = project_number(errors)
        project_items = project_items_by_url(number, errors)
        for item in load_items():
            if item.github_issue:
                check_github_issue(item, errors)
                check_project_item(item, project_items, errors)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"errors: {len(errors)}", file=sys.stderr)
        return 1

    print(f"checked {len(load_items())} GitHub-primary active backlog specs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
