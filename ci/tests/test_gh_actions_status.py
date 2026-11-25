import runpy
import unittest
from datetime import datetime
from pathlib import Path


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
