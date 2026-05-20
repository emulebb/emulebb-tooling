#!/usr/bin/env python3
"""Create or refresh GitHub roadmap issues from eMule BB local specs."""

from __future__ import annotations

import argparse
import json
import re
import sys

from github_roadmap_common import (
    ISSUE_REPO,
    LABEL_DEFINITIONS,
    OWNER,
    PROJECT_RELEASE,
    PROJECT_TITLE,
    issue_body,
    load_items,
    load_json,
    require_success,
    run_gh,
    update_item_github_metadata,
)


PROJECT_FIELDS = {
    "Status": ("SINGLE_SELECT", ["Triage", "Ready", "In Progress", "Blocked", "Deferred", "Done", "Won't Do"]),
    "Type": ("SINGLE_SELECT", ["Bug", "Feature", "Refactor", "CI", "Planning"]),
    "Priority": ("SINGLE_SELECT", ["Critical", "Major", "Minor", "Trivial"]),
    "Lane": (
        "SINGLE_SELECT",
        [
            "Connectivity",
            "Search and Trust",
            "UI Polish",
            "Security and Operations",
            "Anti-Leecher Review",
            "Planning",
        ],
    ),
    "Local ID": ("TEXT", []),
    "Release": ("TEXT", []),
}


def print_plan() -> None:
    """Print the first-rollout roadmap import plan."""

    items = load_items()
    print(f"project: {OWNER}/{PROJECT_TITLE}")
    print(f"issue repo: {ISSUE_REPO}")
    print(f"release: {PROJECT_RELEASE}")
    print(f"items: {len(items)}")
    for item in items:
        labels = ", ".join(item.github_labels)
        print(
            f"- {item.item_id}: {item.title} "
            f"[lane={item.lane}; status={item.project_status}; labels={labels}]"
        )


def ensure_label(name: str, color: str, description: str) -> None:
    """Create or update one GitHub issue label."""

    create = run_gh(
        [
            "label",
            "create",
            name,
            "--repo",
            ISSUE_REPO,
            "--color",
            color,
            "--description",
            description,
        ]
    )
    if create.returncode == 0:
        return
    if "already exists" not in create.stderr:
        require_success(create, f"create label {name}")
    edit = run_gh(
        [
            "label",
            "edit",
            name,
            "--repo",
            ISSUE_REPO,
            "--color",
            color,
            "--description",
            description,
        ]
    )
    require_success(edit, f"edit label {name}")


def ensure_labels() -> None:
    """Ensure all roadmap labels exist in the issue repository."""

    for name, (color, description) in LABEL_DEFINITIONS.items():
        ensure_label(name, color, description)


def project_list() -> list[dict[str, object]]:
    """Return org project entries visible to the current GitHub token."""

    data = load_json(
        run_gh(["project", "list", "--owner", OWNER, "--format", "json", "--limit", "100"]),
        "list projects",
    )
    if isinstance(data, dict):
        projects = data.get("projects", [])
        if isinstance(projects, list):
            return [project for project in projects if isinstance(project, dict)]
    return []


def ensure_project() -> tuple[str, str]:
    """Create or find the roadmap project and return number plus node ID."""

    for project in project_list():
        if project.get("title") == PROJECT_TITLE:
            number = str(project.get("number"))
            project_id = str(project.get("id", ""))
            require_success(
                run_gh(
                    [
                        "project",
                        "edit",
                        number,
                        "--owner",
                        OWNER,
                        "--visibility",
                        "PUBLIC",
                    ]
                ),
                "make project public",
            )
            return number, project_id

    data = load_json(
        run_gh(
            [
                "project",
                "create",
                "--owner",
                OWNER,
                "--title",
                PROJECT_TITLE,
                "--format",
                "json",
            ]
        ),
        "create project",
    )
    if not isinstance(data, dict):
        raise SystemExit("error: unexpected project create response")
    number = str(data.get("number"))
    require_success(
        run_gh(
            [
                "project",
                "edit",
                number,
                "--owner",
                OWNER,
                "--visibility",
                "PUBLIC",
            ]
        ),
        "make project public",
    )
    return number, str(data.get("id", ""))


def field_list(project_number: str) -> list[dict[str, object]]:
    """Return fields for the target project."""

    data = load_json(
        run_gh(["project", "field-list", project_number, "--owner", OWNER, "--format", "json"]),
        "list project fields",
    )
    if isinstance(data, dict):
        fields = data.get("fields", [])
        if isinstance(fields, list):
            return [field for field in fields if isinstance(field, dict)]
    return []


def ensure_project_fields(project_number: str) -> dict[str, dict[str, object]]:
    """Ensure custom project fields exist and return them by name."""

    fields_by_name = {
        str(field.get("name")): field for field in field_list(project_number)
    }
    for name, (data_type, options) in PROJECT_FIELDS.items():
        if name in fields_by_name:
            continue
        args = [
            "project",
            "field-create",
            project_number,
            "--owner",
            OWNER,
            "--name",
            name,
            "--data-type",
            data_type,
            "--format",
            "json",
        ]
        if options:
            args.extend(["--single-select-options", ",".join(options)])
        require_success(run_gh(args), f"create project field {name}")
    return {str(field.get("name")): field for field in field_list(project_number)}


def find_issue(item_id: str) -> dict[str, object] | None:
    """Find an existing GitHub issue whose title contains the local item ID."""

    data = load_json(
        run_gh(
            [
                "issue",
                "list",
                "--repo",
                ISSUE_REPO,
                "--state",
                "all",
                "--search",
                f"{item_id} in:title",
                "--json",
                "number,title,url",
                "--limit",
                "20",
            ]
        ),
        f"search issue {item_id}",
    )
    if not isinstance(data, list):
        return None
    for issue in data:
        if isinstance(issue, dict) and re.search(rf"\b{re.escape(item_id)}\b", str(issue.get("title", ""))):
            return issue
    return None


def ensure_issue(item) -> dict[str, object]:
    """Create or update the GitHub issue for one roadmap item."""

    existing = find_issue(item.item_id)
    labels = ",".join(item.github_labels)
    body = issue_body(item)

    if existing:
        number = str(existing["number"])
        require_success(
            run_gh(
                [
                    "issue",
                    "edit",
                    number,
                    "--repo",
                    ISSUE_REPO,
                    "--title",
                    item.issue_title,
                    "--body-file",
                    "-",
                    "--add-label",
                    labels,
                ],
                input_text=body,
            ),
            f"update issue {item.item_id}",
        )
        return existing

    stdout = require_success(
        run_gh(
            [
                "issue",
                "create",
                "--repo",
                ISSUE_REPO,
                "--title",
                item.issue_title,
                "--body-file",
                "-",
                "--label",
                labels,
            ],
            input_text=body,
        ),
        f"create issue {item.item_id}",
    ).strip()
    issue = load_json(
        run_gh(
            [
                "issue",
                "view",
                stdout,
                "--repo",
                ISSUE_REPO,
                "--json",
                "number,title,url",
            ]
        ),
        f"read created issue {item.item_id}",
    )
    if not isinstance(issue, dict):
        raise SystemExit(f"error: unexpected issue view response for {item.item_id}")
    return issue


def project_item_list(project_number: str) -> list[dict[str, object]]:
    """Return project items for the target project."""

    data = load_json(
        run_gh(
            [
                "project",
                "item-list",
                project_number,
                "--owner",
                OWNER,
                "--format",
                "json",
                "--limit",
                "200",
            ]
        ),
        "list project items",
    )
    if isinstance(data, dict):
        items = data.get("items", [])
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
    return []


def ensure_project_item(project_number: str, issue_url: str) -> str:
    """Add an issue to the roadmap project and return the project item ID."""

    for project_item in project_item_list(project_number):
        content = project_item.get("content")
        if isinstance(content, dict) and content.get("url") == issue_url:
            return str(project_item.get("id", ""))

    data = load_json(
        run_gh(
            [
                "project",
                "item-add",
                project_number,
                "--owner",
                OWNER,
                "--url",
                issue_url,
                "--format",
                "json",
            ]
        ),
        f"add project item {issue_url}",
    )
    if not isinstance(data, dict):
        raise SystemExit(f"error: unexpected project item response for {issue_url}")
    return str(data.get("id", ""))


def field_option_id(field: dict[str, object], option_name: str) -> str:
    """Return a single-select option ID from a project field."""

    options = field.get("options", [])
    if not isinstance(options, list):
        return ""
    for option in options:
        if isinstance(option, dict) and option.get("name") == option_name:
            return str(option.get("id", ""))
    return ""


def set_project_field(project_id: str, item_id: str, field: dict[str, object], value: str) -> None:
    """Set one project field value on a project item."""

    field_id = str(field.get("id", ""))
    data_type = str(field.get("dataType", field.get("type", ""))).upper()
    args = [
        "project",
        "item-edit",
        "--id",
        item_id,
        "--project-id",
        project_id,
        "--field-id",
        field_id,
    ]
    if "SINGLE_SELECT" in data_type or field.get("options"):
        option_id = field_option_id(field, value)
        if not option_id:
            raise SystemExit(f"error: missing option {value!r} for project field {field.get('name')!r}")
        args.extend(["--single-select-option-id", option_id])
    else:
        args.extend(["--text", value])
    require_success(run_gh(args), f"set project field {field.get('name')}={value}")


def sync_project_fields(project_id: str, project_item_id: str, fields: dict[str, dict[str, object]], item) -> None:
    """Synchronize project fields for one roadmap item."""

    values = {
        "Status": item.project_status,
        "Type": item.project_type,
        "Priority": item.priority,
        "Lane": item.lane,
        "Local ID": item.item_id,
        "Release": PROJECT_RELEASE,
    }
    for field_name, value in values.items():
        field = fields.get(field_name)
        if not field:
            raise SystemExit(f"error: missing project field {field_name!r}")
        set_project_field(project_id, project_item_id, field, value)


def apply_sync() -> None:
    """Apply the GitHub roadmap migration."""

    items = load_items()
    project_number, project_id = ensure_project()
    if not project_id:
        raise SystemExit("error: project id missing; cannot edit project fields")
    fields = ensure_project_fields(project_number)
    ensure_labels()

    for item in items:
        issue = ensure_issue(item)
        issue_url = str(issue.get("url", ""))
        if not issue_url:
            number = issue.get("number")
            issue_url = f"https://github.com/{ISSUE_REPO}/issues/{number}"
        project_item_id = ensure_project_item(project_number, issue_url)
        sync_project_fields(project_id, project_item_id, fields, item)
        update_item_github_metadata(item, issue_url)
        print(f"synced {item.item_id}: {issue_url}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="mutate GitHub and local item metadata")
    args = parser.parse_args()

    if not args.apply:
        print_plan()
        print("\ndry run only; pass --apply to mutate GitHub and local metadata")
        return 0

    apply_sync()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        raise SystemExit(130)
