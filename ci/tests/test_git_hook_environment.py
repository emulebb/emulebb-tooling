"""Prove hook checks cannot redirect fixture Git operations into the caller repo."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("git_local_checks", ROOT / "helpers/git-local-checks.py")
CHECKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKS)


class GitHookEnvironmentTests(unittest.TestCase):
    def test_scrubber_removes_all_git_local_names_from_child_copy_only(self):
        names = subprocess.check_output(["git", "rev-parse", "--local-env-vars"], text=True).splitlines()
        hook_values = {name: "synthetic-hook-context" for name in names}
        with patch.dict(os.environ, {**hook_values, "EMULEBB_FIXTURE_ANCHOR": "keep-anchor"}), \
                patch.object(CHECKS.subprocess, "check_output", return_value="\n".join(names)):
            before = os.environ.copy()
            child = CHECKS.validation_environment()
            self.assertTrue(all(name not in child for name in names))
            self.assertEqual(child["EMULEBB_FIXTURE_ANCHOR"], "keep-anchor")
            self.assertEqual(os.environ, before)

    def test_hook_dispatch_preserves_stdin_and_cannot_reinitialize_original_repository(self):
        output = os.environ.get("EMULEBB_WORKSPACE_OUTPUT_ROOT")
        fixture_parent = Path(output) / "tmp" if output else None
        if fixture_parent:
            fixture_parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=fixture_parent) as directory:
            root = Path(directory)
            source = root / "source"
            owner = source / "repos" / "emulebb-build"
            module = owner / "emule_workspace"
            module.mkdir(parents=True)
            module.joinpath("__init__.py").write_text("", encoding="utf-8")
            second = root / "second.git"
            receipt = root / "receipt.json"
            module.joinpath("__main__.py").write_text(
                "import json, os, pathlib, subprocess, sys\n"
                "subprocess.run(['git', 'init', '--bare', os.environ['HOOK_FIXTURE_SECOND']], check=True, capture_output=True)\n"
                "pathlib.Path(os.environ['HOOK_FIXTURE_RECEIPT']).write_text(json.dumps({'argv': sys.argv[1:], 'stdin': sys.stdin.read(), 'root': os.environ['EMULEBB_WORKSPACE_ROOT'], 'context': [k for k in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE') if k in os.environ]}))\n",
                encoding="utf-8",
            )
            original = source / "repos" / "sample"
            original.mkdir(parents=True)
            clean = CHECKS.validation_environment()
            def git(*args):
                return subprocess.check_output(["git", "-C", str(original), *args], env=clean, text=True).strip()
            git("init")
            original.joinpath("sample.txt").write_text("retained staged input\n", encoding="utf-8")
            git("add", "sample.txt")
            index = original / ".git" / "index"
            before_index = index.read_bytes()
            before_config = (original / ".git" / "config").read_bytes()
            hook = {**clean, "GIT_DIR": str(original / ".git"), "GIT_WORK_TREE": str(original),
                    "GIT_INDEX_FILE": str(index), "EMULEBB_WORKSPACE_ROOT": str(source),
                    "HOOK_FIXTURE_SECOND": str(second), "HOOK_FIXTURE_RECEIPT": str(receipt)}
            before_parent = os.environ.copy()
            ref_updates = "refs/heads/sample " + "1" * 40 + " refs/heads/sample " + "0" * 40 + "\n"
            completed = subprocess.run([sys.executable, "-B", str(ROOT / "helpers/git-local-checks.py"),
                                        "push", "origin"], cwd=original, env=hook, input=ref_updates,
                                       text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            data = json.loads(receipt.read_text())
            self.assertEqual(data["context"], [])
            self.assertEqual(data["stdin"], ref_updates)
            self.assertEqual(data["root"], str(source))
            self.assertIn("--push-stdin", data["argv"])
            self.assertEqual(Path(data["argv"][data["argv"].index("--repo") + 1]), original)
            self.assertEqual(index.read_bytes(), before_index)
            self.assertEqual((original / ".git" / "config").read_bytes(), before_config)
            self.assertEqual(git("config", "--get", "core.bare"), "false")
            self.assertTrue((second / "HEAD").is_file())
            self.assertEqual(os.environ, before_parent)
