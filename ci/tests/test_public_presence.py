"""The public contract keeps branding bounded and the two reader routes equal."""
import copy
import hashlib
from html import unescape
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("public_presence", ROOT / "helpers/public-presence.py")
presence = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = presence
SPEC.loader.exec_module(presence)


class PublicPresenceTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads((ROOT / "manifests/public-presence.v1.json").read_text(encoding="utf-8"))

    def test_current_and_legacy_schema_one_contracts_validate(self):
        self.assertEqual(presence.validate_contract(self.contract), [])
        legacy = copy.deepcopy(self.contract)
        legacy.pop("reader_routes")
        legacy.pop("branding")
        self.assertEqual(presence.validate_contract(legacy), [])

    def test_unrelated_urls_assets_and_incomplete_brand_metadata_are_rejected(self):
        changes = (
            lambda value: value["branding"].update(selection="proposal-1"),
            lambda value: value["branding"].update(source_manifest_path="../private.json"),
            lambda value: value["branding"].update(application_manifest_url="https://example.invalid/branding.json"),
            lambda value: value["reader_routes"]["use"].update(url="https://example.invalid/"),
            lambda value: value["branding"].update(readme_logo_url="https://example.invalid/logo.png"),
            lambda value: value["branding"].update(logo_path="../private.png"),
            lambda value: value["branding"]["assets"][0].update(path="assets/unapproved.png"),
            lambda value: value["branding"]["assets"][0].pop("width"),
            lambda value: value["branding"]["assets"][0].update(sha256="not-a-digest"),
            lambda value: value["branding"]["assets"].append(copy.deepcopy(value["branding"]["assets"][0])),
        )
        for change in changes:
            with self.subTest(change=change):
                modified = copy.deepcopy(self.contract)
                change(modified)
                self.assertTrue(presence.validate_contract(modified))

    def test_public_derivatives_match_the_retained_supplied_inventory(self):
        brand = self.contract["branding"]
        data = (ROOT / brand["source_manifest_path"]).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), brand["source_sha256"])
        source = json.loads(data)
        self.assertEqual(source["proposal"], brand["selection"])
        identities = {asset["name"]: (asset["bytes"], asset["sha256"]) for asset in source["files"]}
        names = {"logo": lambda asset: f'logo-tile-{asset["width"]}.png',
                 "touch-icon": lambda asset: "donkey-180.png",
                 "favicon": lambda asset: "favicon.ico",
                 "social-card": lambda asset: "rust-social-preview.png"}
        for asset in brand["assets"]:
            self.assertEqual((asset["bytes"], asset["sha256"]), identities[names[asset["role"]](asset)])

    def test_generated_profile_is_deterministic_and_keeps_maintenance_secondary(self):
        rendered = presence.render_org_profile(self.contract)
        self.assertEqual(rendered, presence.render_org_profile(copy.deepcopy(self.contract)))
        for route in self.contract["reader_routes"].values():
            self.assertIn(f'<strong>{route["label"]}</strong></a>', rendered)
            self.assertIn(f'<h3>{route["label"]}</h3>', rendered)
        self.assertIn('width="160" height="160" alt="eMuleBB Rust pixel donkey identity"', rendered)
        self.assertNotIn("few more weeks", rendered)
        for retired_story in ("historical", "migration", "beta.2", "uploadqueuemigration"):
            self.assertNotIn(retired_story, rendered.lower())
        self.assertNotIn(self.contract["products"][0]["release_url"], rendered)
        self.assertLess(rendered.index("## Work across the project"), rendered.index("## Maintenance and references"))
        for repository in self.contract["repositories"]:
            self.assertIn(repository["url"], rendered)
            self.assertIn(repository["role"], unescape(rendered))
        for reference in self.contract["compatibility_references"]:
            self.assertIn(reference["url"], rendered)

    def test_cards_keep_only_approved_identity_and_build_status_images(self):
        class Images(HTMLParser):
            def __init__(self):
                super().__init__()
                self.sources = []

            def handle_starttag(self, tag, attrs):
                if tag == "img":
                    self.sources.append(dict(attrs)["src"])

        rendered = presence.render_org_profile(self.contract)
        images = Images()
        images.feed(rendered)
        self.assertEqual(images.sources, [
            self.contract["branding"]["readme_logo_url"],
            "https://github.com/emulebb/emulebb-rust/actions/workflows/ci.yml/badge.svg?branch=main",
            "https://github.com/emulebb/emulebb-tooling/actions/workflows/docs-site.yml/badge.svg?branch=main",
        ])
        self.assertNotIn("<style", rendered)
        self.assertNotIn("<script", rendered)
        legacy = copy.deepcopy(self.contract)
        legacy.pop("branding")
        legacy.pop("reader_routes")
        self.assertIn("Use eMuleBB Rust", presence.render_org_profile(legacy))
        self.assertNotIn("pixel donkey", presence.render_org_profile(legacy))

    def test_contract_text_is_escaped_inside_html(self):
        self.contract["organization"]["summary"] = 'Search <sample> & "share"'
        self.contract["repositories"][0]["role"] = "Rust <client> & console"
        rendered = presence.render_org_profile(self.contract)
        self.assertIn("Search &lt;sample&gt; &amp; &quot;share&quot;", rendered)
        self.assertIn("Rust &lt;client&gt; &amp; console", rendered)
        self.assertNotIn("<sample>", rendered)
