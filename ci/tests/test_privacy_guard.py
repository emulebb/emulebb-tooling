"""Changed-file privacy checks retain the full-audit default."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import policy_guards


class PrivacyScopeTests(unittest.TestCase):
    def test_hosted_account_is_not_personal_but_explicit_rules_remain(self):
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "HOME": str(Path("fixture-profile") / "runner"), "USER": "runner"}, clear=True):
            self.assertEqual(policy_guards.get_personal_identifiers(Path(".")), ())
            with patch.dict(os.environ, {"TRACKED_FILE_PRIVACY_IDENTIFIERS": "runner,operator"}):
                self.assertEqual(policy_guards.get_personal_identifiers(Path(".")), ("runner", "operator"))
        with patch.dict(os.environ, {"USER": "runner"}, clear=True):
            self.assertEqual(policy_guards.get_personal_identifiers(Path(".")), ("runner",))

    def test_changed_scope_does_not_weaken_default_full_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "changed.txt").write_text("safe fixture\n")
            (root / "old.txt").write_text("PRIVATE_MARKER\n")
            policy = root / "policy.json"
            policy.write_text(json.dumps({"contentRules": [{"id": "test", "reason": "synthetic marker", "regex": "PRIVATE_MARKER"}]}))
            with patch.object(policy_guards, "get_tracked_files", return_value=["changed.txt", "old.txt"]), patch.object(policy_guards, "get_personal_identifiers", return_value=[]):
                result = policy_guards.run_privacy_guard(repo_root=root, policy_path=policy, paths={"changed.txt"})
                self.assertEqual(result["scannedTrackedFiles"], 1)
                with self.assertRaises(policy_guards.PrivacyGuardFailure):
                    policy_guards.run_privacy_guard(repo_root=root, policy_path=policy)
                with self.assertRaises(policy_guards.PrivacyGuardFailure):
                    policy_guards.run_privacy_guard(repo_root=root, policy_path=policy, paths={"old.txt"})
