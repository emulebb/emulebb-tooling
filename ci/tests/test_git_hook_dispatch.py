"""Exercise registered hook dispatch with real linked Git checkouts."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("hook_dispatch_under_test", ROOT / "helpers/git-local-checks.py")
DISPATCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISPATCH)


class HookDispatchTests(unittest.TestCase):
    def setUp(self):
        parent = os.environ.get("EMULEBB_WORKSPACE_OUTPUT_ROOT")
        parent = Path(parent) / "tmp" if parent else None
        if parent:
            parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temporary.cleanup)
        self.fixture = Path(self.temporary.name).resolve()
        self.source = self.fixture / "source"
        self.output = self.fixture / "output"
        self.output.mkdir()
        self.environment = DISPATCH.validation_environment()
        self.canonical = {}
        self.selected = {}
        self.receipt = self.fixture / "receipt.json"
        for name in ("emulebb-build", "emulebb-rust"):
            anchor = self.source / "repos" / name
            anchor.mkdir(parents=True)
            self.git(anchor, "init", "--initial-branch=main")
            self.git(anchor, "config", "user.name", "Synthetic Author")
            self.git(anchor, "config", "user.email", "fixture@example.invalid")
            self.git(anchor, "config", "commit.gpgsign", "false")
            self.git(anchor, "config", "core.hooksPath", str(self.fixture / "empty-hooks"))
            self.git(anchor, "remote", "add", "origin", f"https://example.invalid/{name}.git")
            if name == "emulebb-build":
                module = anchor / "emule_workspace"
                module.mkdir()
                (module / "__init__.py").write_text("", encoding="utf-8")
                self.module_body = (
                    "import json, os, pathlib, sys\n"
                    "pathlib.Path(os.environ['HOOK_RECEIPT']).write_text(json.dumps({'mode': MODE, 'cwd': os.getcwd(), 'argv':sys.argv[1:], 'stdin':sys.stdin.read(), 'root':os.environ['EMULEBB_WORKSPACE_ROOT'], 'git_context':[k for k in ('GIT_DIR','GIT_INDEX_FILE','GIT_WORK_TREE') if k in os.environ]}))\n"
                )
                (module / "__main__.py").write_text("MODE='canonical'\n" + self.module_body, encoding="utf-8")
            else:
                (anchor / "sample.txt").write_text("sample\n", encoding="utf-8")
            self.git(anchor, "add", ".")
            self.git(anchor, "commit", "-m", "Synthetic baseline")
            selected = self.source / "workspaces" / "agents" / "alpha" / name
            selected.parent.mkdir(parents=True, exist_ok=True)
            self.git(anchor, "worktree", "add", "-b", "chore/alpha", str(selected))
            self.canonical[name], self.selected[name] = anchor, selected
        (self.selected["emulebb-build"] / "emule_workspace" / "__main__.py").write_text(
            "MODE='selected'\n" + self.module_body, encoding="utf-8")
        self.registration = {"schema": 1, "id": "alpha", "state": "ready", "workspace_root": str(self.source),
                             "branch": "chore/alpha", "owner": "parent", "repositories": {}}
        for name, path in self.selected.items():
            self.registration["repositories"][name] = {
                "path": str(path), "canonical_path": str(self.canonical[name]), "status": "ready",
                "branch": "chore/alpha", "base_revision": self.git(path, "rev-parse", "HEAD"),
                "common_dir": self.git(path, "rev-parse", "--path-format=absolute", "--git-common-dir"),
                "origin": self.git(path, "remote", "get-url", "origin"),
            }
        self.record = self.output / "tmp" / "workstreams" / "alpha.json"
        self.record.parent.mkdir(parents=True)
        self.write_registration()

    def git(self, path, *args):
        return subprocess.check_output(["git", "-C", str(path), *args], env=self.environment,
                                       text=True, stderr=subprocess.PIPE).strip()

    def write_registration(self):
        self.record.write_text(json.dumps(self.registration), encoding="utf-8")

    def invoke(self, repo, *, valid=True):
        environment = {**self.environment, "EMULEBB_WORKSPACE_ROOT": str(self.source),
                       "EMULEBB_WORKSPACE_OUTPUT_ROOT": str(self.output), "HOOK_RECEIPT": str(self.receipt),
                       "GIT_DIR": self.git(repo, "rev-parse", "--absolute-git-dir"),
                       "GIT_WORK_TREE": str(repo)}
        updates = "refs/heads/sample " + "1" * 40 + " refs/heads/sample " + "0" * 40 + "\n"
        before = os.environ.copy()
        result = subprocess.run([sys.executable, "-B", str(ROOT / "helpers/git-local-checks.py"), "push"],
                                cwd=repo, env=environment, text=True, input=updates, capture_output=True)
        self.assertEqual(os.environ, before)
        if not valid:
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(self.receipt.exists())
            return
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(self.receipt.read_text())
        self.assertEqual(data["git_context"], [])
        self.assertEqual(data["stdin"], updates)
        self.assertEqual(Path(data["root"]), self.source)
        self.assertEqual(Path(data["argv"][data["argv"].index("--repo") + 1]), repo)
        return data

    def test_canonical_hook_keeps_canonical_owner_without_selector(self):
        data = self.invoke(self.canonical["emulebb-rust"])
        self.assertEqual(data["mode"], "canonical")
        self.assertNotIn("--workstream", data["argv"])

    def test_registered_hook_runs_selected_builder_with_explicit_selector(self):
        data = self.invoke(self.selected["emulebb-rust"])
        self.assertEqual(data["mode"], "selected")
        self.assertEqual(Path(data["cwd"]), self.selected["emulebb-build"])
        self.assertEqual(data["argv"][-2:], ["--workstream", "alpha"])

    def test_workstream_without_builder_uses_canonical_owner_with_selector(self):
        del self.registration["repositories"]["emulebb-build"]
        self.write_registration()
        data = self.invoke(self.selected["emulebb-rust"])
        self.assertEqual(data["mode"], "canonical")
        self.assertEqual(data["argv"][-2:], ["--workstream", "alpha"])

    def test_builder_path_cannot_be_replaced_by_unrelated_checkout(self):
        self.registration["repositories"]["emulebb-build"]["path"] = str(self.canonical["emulebb-build"])
        self.write_registration()
        self.invoke(self.selected["emulebb-rust"], valid=False)

    def test_unregistered_managed_hook_fails_before_starting_validation(self):
        self.record.unlink()
        self.invoke(self.selected["emulebb-rust"], valid=False)

    def test_changed_builder_branch_or_common_directory_fails_closed(self):
        entry = self.registration["repositories"]["emulebb-build"]
        original = entry.copy()
        for field, replacement in (("branch", "chore/unassigned"),
                                   ("common_dir", str(self.canonical["emulebb-rust"] / ".git")),
                                   ("origin", "https://example.invalid/unrelated.git"), ("status", "planned")):
            with self.subTest(field=field):
                entry.update(original)
                entry[field] = replacement
                self.write_registration()
                self.invoke(self.selected["emulebb-rust"], valid=False)

    def test_incomplete_registration_fails_closed(self):
        self.registration["state"] = "creating"
        self.write_registration()
        self.invoke(self.selected["emulebb-rust"], valid=False)

    def test_redirected_registration_fails_before_dispatch(self):
        target = self.fixture / "redirected-registration.json"
        target.write_bytes(self.record.read_bytes())
        self.record.unlink()
        try:
            self.record.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("Host does not permit synthetic symlinks")
        self.invoke(self.selected["emulebb-rust"], valid=False)

    def test_unmanaged_hook_cannot_select_registered_builder(self):
        owner, selector = DISPATCH.orchestration_owner(self.source, self.output,
                                                      self.fixture / "unrelated", self.environment)
        self.assertEqual(owner, self.canonical["emulebb-build"])
        self.assertIsNone(selector)
