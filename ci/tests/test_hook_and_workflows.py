"""Protect staged edits and keep active documentation deployments running."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("commit_checks", ROOT / "helpers/git-pre-commit-editorconfig.py")
HOOK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOOK)


class HookAndWorkflowTests(unittest.TestCase):
    def test_hooks_route_normalization_and_checks_through_workspace_python(self):
        for name in ("pre-commit", "pre-push"):
            source = (ROOT / "hooks" / name).read_text(encoding="utf-8")
            self.assertIn('python_runner="$hook_dir/../helpers/workspace-python.py"', source)
            self.assertIn('python -B "$python_runner"', source)
            self.assertNotIn('exec python "$hook_dir/../helpers/git-local-checks.py"', source)

    def test_partial_staging_is_rejected_before_normalization(self):
        with patch.object(HOOK, "staged_paths", return_value=["selected.txt"]), patch.object(HOOK, "run_git") as git, patch.object(HOOK, "run_normalizer") as normalize:
            git.return_value.returncode = 1
            with self.assertRaisesRegex(RuntimeError, "Unstaged tracked edits"):
                HOOK.main(["--repo-root", str(ROOT)])
            normalize.assert_not_called()

    def test_documentation_cancellation_is_limited_to_build_job(self):
        text = (ROOT / ".github/workflows/docs-site.yml").read_text(encoding="utf-8")
        self.assertNotIn("\nconcurrency:", text)
        build, deploy = text.split("  deploy:\n")
        self.assertIn("group: docs-build-${{ github.ref }}", build)
        self.assertIn("cancel-in-progress: true", build)
        self.assertIn("group: pages-deploy", deploy)
        self.assertIn("cancel-in-progress: false", deploy)
