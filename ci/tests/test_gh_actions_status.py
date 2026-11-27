import runpy
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch


WATCHER = runpy.run_path(str(Path(__file__).resolve().parents[2] / "scripts/gh-actions-status.py"))


class TestAttemptTiming(unittest.TestCase):
    def test_distinguishes_copied_records_from_jobs_that_ran_again(self):
        now = datetime.fromisoformat("2026-11-25T01:30:00Z")
        job = {"name": "APK runtime", "status": "completed", "conclusion": "success",
               "created_at": "2026-11-25T00:57:40Z", "started_at": "2026-11-25T00:57:42Z",
               "completed_at": "2026-11-25T01:27:16Z", "run_attempt": 2}
        prior = {job["name"]}
        observe = WATCHER["job_timing"]
        self.assertEqual(observe(job, prior, now), ("rerun", 2, 1774))
        self.assertEqual(observe(job, set(), now), ("new", 2, 1774))
        copied = {**job, "started_at": "2026-11-25T00:28:39Z", "completed_at": "2026-11-25T00:55:55Z"}
        self.assertEqual(observe(copied, prior, now), ("reused", None, 1636))
        self.assertEqual(observe({**job, "conclusion": "skipped"}, prior, now), ("skipped", None, None))
        queued = {**job, "status": "queued", "conclusion": None, "completed_at": None}
        self.assertEqual(observe(queued, prior, now), ("rerun", 1940, None))


class TestRecovery(unittest.TestCase):
    def test_ambiguous_retry_only_observes_the_run_after_one_request(self):
        retry = WATCHER["retry_job"]
        run = {"run_attempt": 1, "status": "completed", "html_url": "example"}
        request = Mock(side_effect=RuntimeError("HTTP 500"))
        read = Mock(side_effect=[run, {**run, "status": "queued"}])
        job = {"id": 3, "run_attempt": 1, "conclusion": "failure"}
        with patch.dict(retry.__globals__, {"run_gh": request, "read_run": read,
                                           "read_attempt_jobs": Mock(return_value=[job])}):
            retry("emulebb/emulebb-rust", 2, 1, 3)
        self.assertEqual(read.call_count, 2)
        self.assertEqual(request.call_count, 1)

    def test_unresolved_dispatch_is_not_submitted_twice(self):
        dispatch = WATCHER["dispatch_diagnostic"]
        attempts = []

        def gh(args, **kwargs):
            if "POST" in args:
                attempts.append(args)
                raise RuntimeError("HTTP 500")
            return {"workflow_runs": []}

        with TemporaryDirectory() as directory, patch.dict(dispatch.__globals__, {
            "run_gh": gh, "resolve_snapshot": lambda path: Path(directory) / path,
        }):
            inputs = ["run_id=1", "attempt=1", "source_sha=test", "artifact_name=test",
                      "artifact_sha256=test", "harness_sha=test"]
            for detail in ("acceptance is unresolved", "was already attempted"):
                with self.assertRaisesRegex(RuntimeError, detail):
                    dispatch("emulebb/emulebb-rust", "a" * 32, inputs)
        self.assertEqual(len(attempts), 1)
