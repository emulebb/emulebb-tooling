"""The public contract keeps branding bounded and the two reader routes equal."""
import copy
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

    def test_generated_profile_is_deterministic_and_keeps_maintenance_secondary(self):
        rendered = presence.render_org_profile(self.contract)
        self.assertEqual(rendered, presence.render_org_profile(copy.deepcopy(self.contract)))
        self.assertIn("| Use eMuleBB Rust | Develop with eMuleBB Rust |", rendered)
        self.assertIn('width="160" height="160" alt="eMuleBB Rust pixel donkey identity"', rendered)
        self.assertNotIn("few more weeks", rendered)
        for retired_story in ("historical", "migration", "beta.2", "uploadqueuemigration"):
            self.assertNotIn(retired_story, rendered.lower())
        self.assertNotIn(self.contract["products"][0]["release_url"], rendered)
        self.assertLess(rendered.index("## Work across the project"), rendered.index("## Maintenance and references"))
        for repository in self.contract["repositories"]:
            self.assertIn(repository["url"], rendered)
        for reference in self.contract["compatibility_references"]:
            self.assertIn(reference["url"], rendered)
