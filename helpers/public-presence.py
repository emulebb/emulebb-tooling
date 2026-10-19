#!/usr/bin/env python3
"""Validate public-presence metadata and render dependent public surfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SCHEMA_VERSION = 1
LIFECYCLES = frozenset({"active-beta", "stable-maintenance", "active-test-infrastructure", "active-support"})
RETIRED_CURRENT_REPOSITORIES = frozenset({"goed2k-server", "amutorrent", "qbittorrentbb", "emulebb-libtorrent"})
REQUIRED_REPOSITORY_KEYS = frozenset(
    {"emulebb-rust", "emulebb", "ed2k-server", "emulebb-build-tests", "emulebb-build", "emulebb-tooling"}
)
REQUIRED_REFERENCE_URLS = frozenset({"https://github.com/amule-org/amule", "https://github.com/irwir/eMule"})


def load_contract(path: Path) -> dict[str, Any]:
    """Load the public-presence contract as a JSON object."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("contract root must be a JSON object")
    return payload


def require_text(errors: list[str], container: dict[str, Any], key: str, prefix: str) -> str:
    """Return a required non-empty string while collecting validation errors."""

    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix}.{key} must be a non-empty string")
        return ""
    return value


def require_https_url(errors: list[str], container: dict[str, Any], key: str, prefix: str) -> str:
    """Return a required HTTPS URL while collecting validation errors."""

    value = require_text(errors, container, key, prefix)
    parsed = urlparse(value)
    if value and (parsed.scheme != "https" or not parsed.netloc):
        errors.append(f"{prefix}.{key} must be an absolute HTTPS URL")
    return value


def require_object_list(errors: list[str], payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    """Return a required list of objects while collecting validation errors."""

    value = payload.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{key} must be a non-empty array")
        return []
    if not all(isinstance(item, dict) for item in value):
        errors.append(f"{key} entries must be objects")
        return []
    return value


def validate_unique_fields(errors: list[str], records: list[dict[str, Any]], section: str) -> None:
    """Validate stable unique identifiers for one contract record list."""

    for field in ("key", "name" if section != "public_surfaces" else "repository"):
        values = [record.get(field) for record in records]
        duplicates = sorted({value for value in values if isinstance(value, str) and values.count(value) > 1})
        if duplicates:
            errors.append(f"{section} contains duplicate {field} values: {', '.join(duplicates)}")


def validate_contract(payload: dict[str, Any]) -> list[str]:
    """Return all public-presence contract validation failures."""

    errors: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")

    organization = payload.get("organization")
    if not isinstance(organization, dict):
        errors.append("organization must be an object")
        organization = {}
    for key in ("name", "summary", "development_posture"):
        require_text(errors, organization, key, "organization")
    for key in ("website_url", "docs_url", "roadmap_url"):
        require_https_url(errors, organization, key, "organization")

    repositories = require_object_list(errors, payload, "repositories")
    validate_unique_fields(errors, repositories, "repositories")
    repository_keys: set[str] = set()
    for index, repository in enumerate(repositories):
        prefix = f"repositories[{index}]"
        key = require_text(errors, repository, "key", prefix)
        name = require_text(errors, repository, "name", prefix)
        url = require_https_url(errors, repository, "url", prefix)
        lifecycle = require_text(errors, repository, "lifecycle", prefix)
        require_text(errors, repository, "role", prefix)
        repository_keys.add(key)
        if lifecycle and lifecycle not in LIFECYCLES:
            errors.append(f"{prefix}.lifecycle is not supported: {lifecycle}")
        if name.casefold() in RETIRED_CURRENT_REPOSITORIES:
            errors.append(f"{prefix} exposes retired repository {name!r} as current")
        if url.rstrip("/").casefold() == "https://github.com/emulebb/amule".casefold():
            errors.append(f"{prefix} must reference official aMule upstream, not the retired organization fork")
    missing_repository_keys = sorted(REQUIRED_REPOSITORY_KEYS.difference(repository_keys))
    if missing_repository_keys:
        errors.append(f"repositories is missing required keys: {', '.join(missing_repository_keys)}")

    channels = require_object_list(errors, payload, "release_channels")
    validate_unique_fields(errors, channels, "release_channels")
    channel_keys: set[str] = set()
    for index, channel in enumerate(channels):
        prefix = f"release_channels[{index}]"
        channel_keys.add(require_text(errors, channel, "key", prefix))
        repository_key = require_text(errors, channel, "repository_key", prefix)
        require_text(errors, channel, "label", prefix)
        require_text(errors, channel, "description", prefix)
        require_https_url(errors, channel, "download_url", prefix)
        contributing_url = channel.get("contributing_url")
        if contributing_url is not None:
            require_https_url(errors, channel, "contributing_url", prefix)
        if repository_key and repository_key not in repository_keys:
            errors.append(f"{prefix}.repository_key does not resolve: {repository_key}")

    references = require_object_list(errors, payload, "compatibility_references")
    validate_unique_fields(errors, references, "compatibility_references")
    reference_urls: set[str] = set()
    for index, reference in enumerate(references):
        prefix = f"compatibility_references[{index}]"
        require_text(errors, reference, "key", prefix)
        require_text(errors, reference, "name", prefix)
        reference_urls.add(require_https_url(errors, reference, "url", prefix).rstrip("/"))
        require_text(errors, reference, "tracking_ref", prefix)
        require_text(errors, reference, "role", prefix)
    missing_reference_urls = sorted(REQUIRED_REFERENCE_URLS.difference(reference_urls))
    if missing_reference_urls:
        errors.append(f"compatibility_references is missing required URLs: {', '.join(missing_reference_urls)}")

    surfaces = require_object_list(errors, payload, "public_surfaces")
    validate_unique_fields(errors, surfaces, "public_surfaces")
    surface_keys: set[str] = set()
    for index, surface in enumerate(surfaces):
        prefix = f"public_surfaces[{index}]"
        surface_keys.add(require_text(errors, surface, "key", prefix))
        require_text(errors, surface, "repository", prefix)
        require_https_url(errors, surface, "url", prefix)
        require_text(errors, surface, "role", prefix)

    installer = payload.get("installer")
    if not isinstance(installer, dict):
        errors.append("installer must be an object")
        installer = {}
    owner_surface_key = require_text(errors, installer, "owner_surface_key", "installer")
    release_channel_key = require_text(errors, installer, "release_channel_key", "installer")
    require_https_url(errors, installer, "stable_url", "installer")
    require_https_url(errors, installer, "checksum_url", "installer")
    if owner_surface_key and owner_surface_key not in surface_keys:
        errors.append(f"installer.owner_surface_key does not resolve: {owner_surface_key}")
    if release_channel_key and release_channel_key not in channel_keys:
        errors.append(f"installer.release_channel_key does not resolve: {release_channel_key}")

    require_text(errors, payload, "historical_bundle_note", "contract")
    return errors


def repository_by_key(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index current repositories by their stable contract key."""

    return {repository["key"]: repository for repository in payload["repositories"]}


def render_org_profile(payload: dict[str, Any]) -> str:
    """Render the GitHub organization profile from the validated contract."""

    organization = payload["organization"]
    repositories = repository_by_key(payload)
    lines = [
        "<!-- Generated by emulebb-tooling/helpers/public-presence.py. -->",
        "# eMuleBB",
        "",
        "[![Rust CI](https://github.com/emulebb/emulebb-rust/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/emulebb/emulebb-rust/actions/workflows/ci.yml)",
        "[![MFC baseline](https://github.com/emulebb/emulebb/actions/workflows/baseline.yml/badge.svg?branch=main)](https://github.com/emulebb/emulebb/actions/workflows/baseline.yml)",
        "[![Docs](https://github.com/emulebb/emulebb-tooling/actions/workflows/docs-site.yml/badge.svg?branch=main)](https://github.com/emulebb/emulebb-tooling/actions/workflows/docs-site.yml)",
        "",
        organization["summary"],
        "",
        "## Client Lanes",
        "",
    ]
    for channel in payload["release_channels"]:
        repository = repositories[channel["repository_key"]]
        lines.extend(
            [
                f"- **[{repository['name']}]({repository['url']}) — {channel['label']}.** {channel['description']}",
            ]
        )
        if contributing_url := channel.get("contributing_url"):
            lines.append(f"  [Contributions are welcome.]({contributing_url})")
    lines.extend(["", organization["development_posture"], "", "## Repository Status", "", "| Repository | Role |", "| --- | --- |"])
    for repository in payload["repositories"]:
        lines.append(f"| [`{repository['name']}`]({repository['url']}) | {repository['role']} |")
    lines.extend(["", "## Compatibility References", "", "| Reference | Role |", "| --- | --- |"])
    for reference in payload["compatibility_references"]:
        lines.append(
            f"| [{reference['name']}]({reference['url']}) (`{reference['tracking_ref']}`) | {reference['role']} |"
        )
    lines.extend(
        [
            "",
            "## Releases And Historical Bundles",
            "",
            payload["historical_bundle_note"],
            "",
            "## Start Here",
            "",
        ]
    )
    for channel in payload["release_channels"]:
        lines.append(f"- [{channel['label']} downloads]({channel['download_url']})")
    lines.extend(
        [
            f"- [Read the public documentation]({organization['docs_url']})",
            f"- [Review the eMuleBB Roadmap]({organization['roadmap_url']})",
            f"- [Open the organization website]({organization['website_url']})",
            "",
            "Please report issues in the repository that owns the affected code.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    default_contract = Path(__file__).resolve().parents[1] / "manifests" / "public-presence.v1.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=default_contract)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate the public-presence contract.")
    render = subparsers.add_parser("render-org-profile", help="Render the organization profile README.")
    render.add_argument("--output", type=Path, required=True)
    check = subparsers.add_parser("check-org-profile", help="Fail when the organization profile differs from the contract.")
    check.add_argument("--input", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    """Run the selected public-presence operation."""

    args = parse_args()
    try:
        payload = load_contract(args.contract)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"public-presence contract error: {exc}", file=sys.stderr)
        return 1
    errors = validate_contract(payload)
    if errors:
        for error in errors:
            print(f"public-presence contract error: {error}", file=sys.stderr)
        return 1
    if args.command == "validate":
        print(f"validated {args.contract}")
        return 0
    rendered = render_org_profile(payload)
    if args.command == "render-org-profile":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"rendered {args.output}")
        return 0
    current = args.input.read_text(encoding="utf-8") if args.input.exists() else ""
    if current != rendered:
        print(f"organization profile is out of date: {args.input}", file=sys.stderr)
        return 1
    print(f"organization profile matches {args.contract}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
