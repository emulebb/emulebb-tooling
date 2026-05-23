#!/usr/bin/env python3
"""Validate eMuleBB GitHub-primary future roadmap metadata."""

from __future__ import annotations

import argparse
import re
import sys

from github_roadmap_common import (
    ISSUE_REPO,
    OWNER,
    PROJECT_TITLE,
    load_items,
    load_json,
    read_text,
    run_gh,
)


def check_local_metadata(errors: list[str]) -> None:
    """Check local future-roadmap specs for GitHub workflow metadata."""

    for item in load_items():
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


def project_exists(errors: list[str]) -> None:
    """Check that the roadmap project is visible to the current token."""

    result = run_gh(["project", "list", "--owner", OWNER, "--format", "json", "--limit", "100"])
    if result.returncode != 0:
        errors.append("cannot list org projects; run `gh auth refresh -s project`")
        return
    data = load_json(result, "list projects")
    projects = data.get("projects", []) if isinstance(data, dict) else []
    if not any(isinstance(project, dict) and project.get("title") == PROJECT_TITLE for project in projects):
        errors.append(f"missing org project {OWNER}/{PROJECT_TITLE}")


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
        project_exists(errors)
        for item in load_items():
            if item.github_issue:
                check_github_issue(item, errors)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"errors: {len(errors)}", file=sys.stderr)
        return 1

    print(f"checked {len(load_items())} GitHub-primary roadmap specs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
