"""The stable Pages installer retains its narrow PowerShell compatibility contract."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import policy_guards


class PagesInstallerHygieneTests(unittest.TestCase):
    def check_header(self, owner, relative, version):
        """Check synthetic script text without writing source or fixture files."""
        root = Path("synthetic-repositories") / owner
        with patch.object(Path, "read_text", return_value=f"#Requires -Version {version}\n"):
            return policy_guards.test_powershell_version_header(root, "generic", relative, root / relative)

    def test_admitted_pages_roots_keep_top_level_installer_at_51(self):
        for owner in ("emulebb-pages", "emulebb.github.io"):
            with self.subTest(owner=owner):
                self.assertIsNone(self.check_header(owner, "install.ps1", "5.1"))
                self.assertIn("5.1", self.check_header(owner, "install.ps1", "7.6"))

    def test_exception_does_not_admit_other_owners_or_script_paths(self):
        cases = (
            ("other-project", "install.ps1"),
            ("emulebb-org-profile", "install.ps1"),
            ("emulebb-pages", "scripts/install.ps1"),
            ("emulebb-pages", "nested/install.ps1"),
            ("emulebb-pages", "helper.ps1"),
            ("emulebb-pages", "../install.ps1"),
        )
        for owner, relative in cases:
            with self.subTest(owner=owner, path=relative):
                self.assertIn("7.6", self.check_header(owner, relative, "5.1"))
                self.assertIsNone(self.check_header(owner, relative, "7.6"))
