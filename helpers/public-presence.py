#!/usr/bin/env python3
"""Validate public-presence metadata and render dependent public surfaces."""

from __future__ import annotations

import argparse
import json
import re
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
REQUIRED_PRODUCT_KEYS = frozenset({"emulebb-rust"})
REQUIRED_REFERENCE_URLS = frozenset({"https://github.com/amule-org/amule", "https://github.com/irwir/eMule"})
READER_ROUTES = {
    "use": {"label": "Use eMuleBB Rust",
            "url": "https://emulebb.github.io/emulebb-tooling/products/emulebb-rust/reference/GUIDE-GETTING-STARTED/",
            "downloads_url": "https://emulebb.github.io/emulebb-tooling/products/emulebb-rust/reference/GUIDE-DOWNLOADS-PLATFORMS/"},
    "develop": {"label": "Develop with eMuleBB Rust",
                "url": "https://emulebb.github.io/emulebb-tooling/products/emulebb-rust/reference/GUIDE-CONTRIBUTING/",
                "api_url": "https://emulebb.github.io/emulebb-tooling/products/emulebb-rust/api/GUIDE-API-CONSUMERS/"},
}
BRAND_ASSETS = {
    "assets/brand/emulebb-logo-256.png": ("logo", 256, 256),
    "assets/brand/emulebb-logo-384.png": ("logo", 384, 384),
    "assets/brand/emulebb-logo-512.png": ("logo", 512, 512),
    "assets/brand/emulebb-donkey-180.png": ("touch-icon", 180, 180),
    "assets/brand/emulebb-favicon.ico": ("favicon", 256, 256),
    "assets/brand/rust-social-preview.png": ("social-card", 1280, 640),
}


def validate_public_extensions(payload: dict[str, Any], errors: list[str]) -> None:
    """@brief Validate optional schema-1 reader routes and approved Rust branding.
    @param payload The public-presence authority, including optional extensions.
    @param errors Existing validation failures to extend; legacy contracts remain valid.
    """
    if "reader_routes" in payload and payload["reader_routes"] != READER_ROUTES:
        errors.append("reader_routes must use the approved equal Use/Develop labels and canonical guide URLs")
    if "branding" not in payload:
        return
    brand = payload["branding"]
    if not isinstance(brand, dict):
        errors.append("branding must be an object")
        return
    if brand.get("selection") != "proposal-1":
        errors.append("branding must select the operator-approved proposal-1 assets")
    for key in ("source_sha256",):
        if not isinstance(brand.get(key), str) or re.fullmatch(r"[0-9a-f]{64}", brand[key]) is None:
            errors.append(f"branding.{key} requires a SHA-256 identity")
    if brand.get("logo_path") != "assets/brand/emulebb-logo-256.png" or brand.get("social_path") != "assets/brand/rust-social-preview.png":
        errors.append("branding logo/social paths must identify the approved assets")
    require_text(errors, brand, "social_alt", "branding")
    logo_url = brand.get("readme_logo_url", "")
    if (logo_url != "https://emulebb.github.io/assets/brand/emulebb-logo-256.png"
            and (not isinstance(logo_url, str) or re.fullmatch(
                r"https://raw\.githubusercontent\.com/emulebb/emulebb\.github\.io/[0-9a-f]{40}/assets/brand/emulebb-logo-256\.png", logo_url) is None)):
        errors.append("branding.readme_logo_url must use the approved public origin or an actual immutable Pages commit")
    assets = brand.get("assets", [])
    if not isinstance(assets, list) or not all(isinstance(asset, dict) for asset in assets):
        errors.append("branding.assets must be an approved asset array")
        return
    if not all(isinstance(asset.get("path"), str) for asset in assets):
        errors.append("branding asset paths must be strings")
        return
    if len(assets) != len(BRAND_ASSETS) or {asset.get("path") for asset in assets} != set(BRAND_ASSETS):
        errors.append("branding.assets must contain exactly the six approved public derivatives")
    for asset in assets:
        path = asset.get("path")
        if path not in BRAND_ASSETS:
            continue
        if (asset.get("role"), asset.get("width"), asset.get("height")) != BRAND_ASSETS[path]:
            errors.append(f"branding asset role/dimensions differ: {path}")
        if type(asset.get("bytes")) is not int or not 0 < asset["bytes"] <= 8 * 1024 * 1024:
            errors.append(f"branding asset requires a bounded byte count: {path}")
        if not isinstance(asset.get("sha256"), str) or re.fullmatch(r"[0-9a-f]{64}", asset["sha256"]) is None:
            errors.append(f"branding asset requires a SHA-256 identity: {path}")


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

    fields = ["key"]
    if section in {"repositories", "compatibility_references"}:
        fields.append("name")
    elif section == "public_surfaces":
        fields.append("repository")
    for field in fields:
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

    products = require_object_list(errors, payload, "products")
    validate_unique_fields(errors, products, "products")
    product_keys: set[str] = set()
    for index, product in enumerate(products):
        prefix = f"products[{index}]"
        product_keys.add(require_text(errors, product, "key", prefix))
        repository_key = require_text(errors, product, "repository_key", prefix)
        for key in (
            "display_name",
            "lifecycle_label",
            "published_version",
            "development_target",
            "development_eta",
            "testing_summary",
        ):
            require_text(errors, product, key, prefix)
        for key in ("nightly_url", "release_url", "docs_url", "issues_url"):
            require_https_url(errors, product, key, prefix)
        if repository_key and repository_key not in repository_keys:
            errors.append(f"{prefix}.repository_key does not resolve: {repository_key}")
    missing_product_keys = sorted(REQUIRED_PRODUCT_KEYS.difference(product_keys))
    if missing_product_keys:
        errors.append(f"products is missing required keys: {', '.join(missing_product_keys)}")

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
    validate_public_extensions(payload, errors)
    return errors


def repository_by_key(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index current repositories by their stable contract key."""

    return {repository["key"]: repository for repository in payload["repositories"]}


def product_by_key(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index current products by their stable contract key."""

    return {product["key"]: product for product in payload["products"]}


def render_org_profile(payload: dict[str, Any]) -> str:
    """Render the GitHub organization profile from the validated contract."""

    organization = payload["organization"]
    repositories = repository_by_key(payload)
    rust_product = product_by_key(payload)["emulebb-rust"]
    routes = payload.get("reader_routes", READER_ROUTES)
    lines = [
        "<!-- Generated by emulebb-tooling/helpers/public-presence.py. -->",
        "# eMuleBB",
        "",
    ]
    if brand := payload.get("branding"):
        lines.extend([f'<img src="{brand["readme_logo_url"]}" width="160" height="160" alt="eMuleBB Rust pixel donkey identity" />', ""])
    lines.extend([
        "[![Rust CI](https://github.com/emulebb/emulebb-rust/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/emulebb/emulebb-rust/actions/workflows/ci.yml)",
        "[![Docs](https://github.com/emulebb/emulebb-tooling/actions/workflows/docs-site.yml/badge.svg?branch=main)](https://github.com/emulebb/emulebb-tooling/actions/workflows/docs-site.yml)",
        "",
        "**Contents:** [Use or develop](#use-or-develop) · [Repositories](#work-across-the-project) · [Support](#keep-in-touch)",
        "",
        organization["summary"],
        "",
        f"**{rust_product['lifecycle_label']}.** CI-gated nightly builds are the public testing channel. {rust_product['development_eta']}",
        "",
        "## Use or develop",
        "",
        f"| {routes['use']['label']} | {routes['develop']['label']} |",
        "| --- | --- |",
        f"| [First launch and daily use]({routes['use']['url']}) | [Contribute to the client]({routes['develop']['url']}) |",
        f"| [Choose a platform and package]({routes['use']['downloads_url']}) | [Build against the REST API]({routes['develop']['api_url']}) |",
        "",
        "- **Browser operation:** search eD2K/Kad, manage transfers and monitor chosen shared folders from the packaged console.",
        "- **Automation:** use authenticated REST requests and the documented API contract.",
        "- **Explicit network controls:** review interface settings, connection status and diagnostics.",
        "- **Identifiable builds:** inspect source-bound package manifests, checksums and provenance.",
        "",
        rust_product["testing_summary"],
        "",
        f"- [Choose the newest dated nightly build]({rust_product['nightly_url']})",
        f"- [Report {rust_product['display_name']} issues]({rust_product['issues_url']})",
        "",
        "## Work across the project",
        "",
        "| Repository | Role |",
        "| --- | --- |",
    ])
    primary = ("emulebb-rust", "emulebb-tooling", "emulebb-build", "emulebb-build-tests")
    for key in primary:
        repository = repositories[key]
        lines.append(f"| [`{repository['name']}`]({repository['url']}) | {repository['role']} |")
    lines.extend(["", "## Maintenance and references", "", organization["development_posture"], ""])
    for channel in payload["release_channels"]:
        if channel["key"] == "rust-nightly":
            continue
        lines.append(f"- [{channel['label']} downloads]({channel['download_url']}): {channel['description']}")
    lines.extend(["", "<details>", "<summary>Test infrastructure and compatibility references</summary>", ""])
    for repository in payload["repositories"]:
        if repository["key"] not in primary:
            lines.append(f"- [`{repository['name']}`]({repository['url']}): {repository['role']}")
    for reference in payload["compatibility_references"]:
        lines.append(f"- [{reference['name']}]({reference['url']}) (`{reference['tracking_ref']}`): {reference['role']}")
    lines.extend(
        [
            "", "</details>", "", "## Keep in touch", "",
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
