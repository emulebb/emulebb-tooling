"""Only the reviewed local brand identity and exact derivative bytes can publish."""
import copy
import hashlib
import html
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("pages_site_tools", ROOT / "helpers/pages-site-tools.py")
site = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = site
SPEC.loader.exec_module(site)


class BrandValidationTests(unittest.TestCase):
    def setUp(self):
        self.brand = json.loads((ROOT / "manifests/public-presence.v1.json").read_text(encoding="utf-8"))["branding"]

    def parsed(self, source="../../assets/brand/emulebb-logo-256.png", attributes=None, social_card=False):
        attrs = {"src": source, "width": "256", "height": "256", "alt": ""}
        if attributes:
            for key, value in attributes.items():
                if value is None:
                    attrs.pop(key, None)
                else:
                    attrs[key] = value
        document = "<img " + " ".join(f'{key}="{html.escape(value, quote=True)}"' for key, value in attrs.items()) + ">"
        social = site.SITE_BASE_URL + "/" + self.brand["social_path"]
        metadata = {"og:image": social, "og:image:width": "1280", "og:image:height": "640",
                    "og:image:type": "image/png", "og:image:alt": self.brand["social_alt"],
                    "twitter:card": "summary_large_image", "twitter:image": social,
                    "twitter:image:alt": self.brand["social_alt"]}
        for key, value in (metadata if social_card else {"twitter:card": "summary"}).items():
            attribute = "property" if key.startswith("og:") else "name"
            document += f'<meta {attribute}="{key}" content="{html.escape(value, quote=True)}">'
        parsed = site.ParsedPage()
        parsed.feed(document)
        return parsed

    def test_approved_nested_local_logo_and_exact_social_metadata_pass(self):
        errors = []
        site.validate_images(Path("fr/faq/index.html"), self.parsed(), errors, self.brand)
        self.assertEqual(errors, [])

    def test_exact_social_card_is_limited_to_canonical_english_surfaces(self):
        errors = []
        parsed = self.parsed("../assets/brand/emulebb-logo-256.png", social_card=True)
        site.validate_images(Path("faq/index.html"), parsed, errors, self.brand)
        self.assertEqual(errors, [])
        site.validate_images(Path("fr/faq/index.html"), self.parsed(social_card=True), errors, self.brand)
        self.assertTrue(any("localized" in error for error in errors))

    def test_external_traversing_unapproved_and_inaccessible_images_fail(self):
        cases = (
            ("https://example.invalid/logo.png", None),
            ("//example.invalid/logo.png", None),
            ("../../../assets/brand/emulebb-logo-256.png", None),
            ("../../assets/brand/unapproved.png", None),
            ("../../assets/brand/emulebb-logo-256.png?alternate=1", None),
            ("../../assets/brand/emulebb-logo-256.png", {"alt": None}),
            ("../../assets/brand/emulebb-logo-256.png", {"height": "32"}),
        )
        for source, attributes in cases:
            with self.subTest(source=source, attributes=attributes):
                errors = []
                site.validate_images(Path("fr/faq/index.html"), self.parsed(source, attributes), errors, self.brand)
                self.assertTrue(errors)

    def test_extra_art_and_changed_approved_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("EMULEBB_WORKSPACE_OUTPUT_ROOT")) as directory:
            root = Path(directory)
            brand = copy.deepcopy(self.brand)
            for asset in brand["assets"]:
                path = root / asset["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                payload = b"synthetic approved derivative"
                path.write_bytes(payload)
                asset.update(bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
            errors = []
            site.validate_prohibited_assets(root, errors, brand)
            self.assertEqual(errors, [])
            (root / brand["logo_path"]).write_bytes(b"X" * len(payload))
            (root / "assets/unapproved.png").write_bytes(b"unapproved")
            site.validate_prohibited_assets(root, errors, brand)
            self.assertTrue(any("SHA-256" in error for error in errors))
            self.assertTrue(any("unexpected raster" in error for error in errors))
