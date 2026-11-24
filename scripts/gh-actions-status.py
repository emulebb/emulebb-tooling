#!/usr/bin/env python3
"""Poll one pull request, exact commit, or workflow run compactly."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECK_FAILURE_STATES = {
    "ACTION_REQUIRED",
    "CANCELLED",
    "ERROR",
    "FAILURE",
    "STALE",
    "STARTUP_FAILURE",
    "TIMED_OUT",
}
RUN_FAILURE_CONCLUSIONS = {
    "action_required",
    "cancelled",
    "failure",
    "stale",
    "startup_failure",
    "timed_out",
}


def run_gh(arguments: list[str], *, json_output: bool = True) -> Any:
    """Run GitHub CLI and return parsed JSON or stripped text."""

    result = subprocess.run(
        ["gh", *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
    )
    output = result.stdout.strip()
    if json_output and output:
        try:
            return json.loads(output)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"gh returned invalid JSON: {output}") from exc
    if result.returncode != 0:
        detail = result.stderr.strip() or output or f"exit code {result.returncode}"
        raise RuntimeError(f"gh {' '.join(arguments)} failed: {detail}")
    if json_output:
        return None
    return output


def resolve_repo(explicit_repo: str | None) -> str:
    """Return OWNER/REPO for the current checkout or explicit override."""

    if explicit_repo:
        return explicit_repo
    value = run_gh(
        ["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
        json_output=False,
    )
    if not value:
        raise RuntimeError("unable to resolve the current GitHub repository")
    return value


def read_pr(repo: str, pr_number: int) -> dict[str, Any]:
    """Return current pull request metadata needed by the monitor."""

    value = run_gh(
        [
            "pr",
            "view",
            str(pr_number),
            "--repo",
            repo,
            "--json",
            "headRefName,headRefOid,mergeStateStatus,mergeable,reviewDecision,state,url",
        ]
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"pull request #{pr_number} returned no metadata")
    return value


def read_checks(repo: str, pr_number: int) -> list[dict[str, Any]]:
    """Return pull request check rollup entries regardless of gh exit status."""

    value = run_gh(
        [
            "pr",
            "checks",
            str(pr_number),
            "--repo",
            repo,
            "--json",
            "link,name,state,workflow",
        ]
    )
    if value is None:
        return []
    if not isinstance(value, list):
        raise RuntimeError(f"pull request #{pr_number} returned invalid check data")
    return value


def read_head_runs(repo: str, head_sha: str) -> list[dict[str, Any]]:
    """Return exact-head workflow runs, including no-job definition failures."""

    value = run_gh(
        [
            "api",
            "--method",
            "GET",
            f"repos/{repo}/actions/runs",
            "-f",
            f"head_sha={head_sha}",
            "-f",
            "per_page=100",
        ]
    )
    if not isinstance(value, dict) or not isinstance(value.get("workflow_runs"), list):
        raise RuntimeError(f"head {head_sha} returned invalid workflow run data")
    return value["workflow_runs"]


def read_run(repo: str, run_id: int) -> dict[str, Any]:
    """Return one exact workflow run."""

    value = run_gh(["api", f"repos/{repo}/actions/runs/{run_id}"])
    if not isinstance(value, dict) or not value.get("id"):
        raise RuntimeError(f"workflow run {run_id} returned invalid data")
    return value


def read_attempt_jobs(repo: str, run: dict[str, Any]) -> list[dict[str, Any]]:
    """Read exact-attempt jobs, including successful work reused from earlier attempts."""
    attempt = run.get("run_attempt")
    if type(attempt) is not int or attempt < 1:
        raise RuntimeError("workflow metadata has no valid attempt")
    endpoint = f"repos/{repo}/actions/runs/{run['id']}/attempts/{attempt}/jobs?per_page=100"
    pages = run_gh(["api", "--paginate", "--slurp", endpoint])
    if not isinstance(pages, list) or not pages:
        raise RuntimeError("workflow attempt returned no job inventory")
    jobs = []
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("jobs"), list):
            raise RuntimeError("workflow attempt returned invalid job data")
        jobs.extend(page["jobs"])
    if any(not isinstance(job, dict) or type(job.get("id")) is not int or job.get("run_id") != run["id"]
           or not isinstance(job.get("name"), str) for job in jobs):
        raise RuntimeError("workflow attempt returned invalid job identity")
    return jobs


def job_state(job: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    """Key visible transitions by state and any failed steps."""
    state = str(job.get("conclusion") or job.get("status") or "unknown")
    failed = tuple(str(step["name"]) for step in job.get("steps") or []
                   if step.get("name") and step.get("conclusion") in RUN_FAILURE_CONCLUSIONS)
    return state, failed


def elapsed_seconds(start: str | None, end: str | None, now: datetime) -> int | None:
    """Use the reported start and end rather than the polling interval."""
    if not start:
        return None
    started = datetime.fromisoformat(start)
    finished = datetime.fromisoformat(end) if end else now
    return max(0, int((finished - started).total_seconds()))


def report_attempt(run: dict[str, Any], jobs: list[dict[str, Any]],
                   previous: dict[int, tuple[str, tuple[str, ...]]], destination: Path | None) -> None:
    """Print job transitions and optionally persist the same snapshot as compact JSON."""
    now = datetime.now(timezone.utc)
    elapsed = elapsed_seconds(run.get("run_started_at"),
                              run.get("updated_at") if run.get("status") == "completed" else None, now)
    counts = Counter(job_state(job)[0] for job in jobs)
    count_summary = " ".join(f"{name}={count}" for name, count in sorted(counts.items()))
    print(f"run {run['id']} attempt {run['run_attempt']}: {run.get('conclusion') or run['status']}"
          f" elapsed={elapsed if elapsed is not None else '?'}s {count_summary}".rstrip(), flush=True)
    snapshot = []
    for job in jobs:
        state, steps = job_state(job)
        duration = elapsed_seconds(job.get("started_at"), job.get("completed_at"), now)
        snapshot.append({"id": job["id"], "name": job["name"], "state": state, "elapsedSeconds": duration,
                         "failedSteps": steps, "url": job.get("html_url")})
        if previous.get(job["id"]) == (state, steps) or state == "skipped":
            continue
        if not previous and state in {"success", "neutral"}:
            continue
        name = job["name"].rsplit(" / ", 1)[-1]
        suffix = f" step={', '.join(steps)}" if steps else ""
        if state in RUN_FAILURE_CONCLUSIONS:
            suffix += f" {job.get('html_url') or ''}"
        print(f"  {name}: {state} elapsed={duration if duration is not None else '?'}s{suffix}", flush=True)
    if destination is not None:
        payload = {"id": run["id"], "attempt": run["run_attempt"], "sourceSha": run.get("head_sha"),
                   "status": run["status"], "conclusion": run.get("conclusion"), "elapsedSeconds": elapsed,
                   "observedAt": now.isoformat(), "jobs": snapshot, "url": run.get("html_url")}
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=destination.parent, prefix="actions-status-") as temp:
            staged = Path(temp) / "snapshot.json"
            staged.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
            staged.replace(destination)


def check_bucket(check: dict[str, Any]) -> str:
    """Classify one pull request check."""

    state = str(check.get("state") or "").upper()
    if state in CHECK_FAILURE_STATES:
        return "failed"
    if state in {"SUCCESS", "SKIPPED", "NEUTRAL"}:
        return "passed"
    return "pending"


def run_bucket(run: dict[str, Any]) -> str:
    """Classify one workflow run."""

    status = str(run.get("status") or "").lower()
    conclusion = str(run.get("conclusion") or "").lower()
    if status != "completed":
        return "pending"
    if conclusion in RUN_FAILURE_CONCLUSIONS:
        return "failed"
    return "passed"


def format_counts(label: str, buckets: list[str]) -> str:
    """Format deterministic compact bucket counts."""

    if not buckets:
        return f"{label}[none]"
    counts = Counter(buckets)
    values = [f"{name}={counts[name]}" for name in ("failed", "pending", "passed") if counts[name]]
    return f"{label}[{','.join(values)}]"


def resolve_commit(repo: str, commit: str) -> str:
    """Resolve one commit-ish to its full repository SHA."""

    value = run_gh(
        ["api", f"repos/{repo}/commits/{commit}", "--jq", ".sha"],
        json_output=False,
    )
    if not value:
        raise RuntimeError(f"unable to resolve commit {commit} in {repo}")
    return value


def snapshot_pr(
    repo: str, pr_number: int
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """Read one consistent-enough Actions snapshot for the current PR head."""

    pr = read_pr(repo, pr_number)
    head_sha = str(pr.get("headRefOid") or "")
    if not head_sha:
        raise RuntimeError(f"pull request #{pr_number} has no head SHA")
    return pr, read_checks(repo, pr_number), read_head_runs(repo, head_sha)


def snapshot_signature(
    head_sha: str, checks: list[dict[str, Any]], runs: list[dict[str, Any]]
) -> tuple[Any, ...]:
    """Return a stable signature used to suppress unchanged polling output."""

    check_values = tuple(
        sorted((str(item.get("name") or ""), str(item.get("state") or "")) for item in checks)
    )
    run_values = tuple(
        sorted(
            (
                str(item.get("id") or ""),
                str(item.get("name") or item.get("path") or ""),
                str(item.get("status") or ""),
                str(item.get("conclusion") or ""),
            )
            for item in runs
        )
    )
    return head_sha, check_values, run_values


def print_summary(checks: list[dict[str, Any]], runs: list[dict[str, Any]]) -> None:
    """Print one compact state line."""

    check_buckets = [check_bucket(item) for item in checks]
    run_buckets = [run_bucket(item) for item in runs]
    print(f"{format_counts('checks', check_buckets)} {format_counts('head-runs', run_buckets)}", flush=True)


def print_failures(checks: list[dict[str, Any]], runs: list[dict[str, Any]]) -> None:
    """Print only failed names and links."""

    for check in checks:
        if check_bucket(check) == "failed":
            print(f"failed check: {check.get('name') or 'unknown'} {check.get('link') or ''}".rstrip())
    for run in runs:
        if run_bucket(run) == "failed":
            name = run.get("name") or run.get("path") or "unknown"
            print(f"failed run: {name} {run.get('html_url') or ''}".rstrip())


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""

    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--pr", type=int, help="Pull request number to monitor.")
    target.add_argument("--commit", help="Exact commit or commit-ish to monitor.")
    target.add_argument("--run", type=int, help="Exact workflow run ID to monitor.")
    parser.add_argument("--repo", help="Optional OWNER/REPO override. Defaults to the current checkout.")
    parser.add_argument("--once", action="store_true", help="Print one snapshot without waiting.")
    parser.add_argument("--snapshot", type=Path, help="Save --run JSON under the inherited output root.")
    parser.add_argument("--interval-seconds", type=float, default=20.0)
    parser.add_argument("--settle-seconds", type=float, default=30.0)
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    return parser.parse_args()


def validate_timing(args: argparse.Namespace) -> None:
    """Reject timing values that would create a busy or unbounded poll loop."""

    if args.interval_seconds < 5:
        raise RuntimeError("--interval-seconds must be at least 5")
    if args.settle_seconds < 0:
        raise RuntimeError("--settle-seconds must not be negative")
    if args.timeout_seconds <= 0:
        raise RuntimeError("--timeout-seconds must be positive")
    if args.snapshot is not None and args.run is None:
        raise RuntimeError("--snapshot requires --run")


def resolve_snapshot(destination: Path | None) -> Path | None:
    """Keep persisted snapshots within the operator's inherited output root."""
    if destination is None:
        return None
    value = os.environ.get("EMULEBB_WORKSPACE_OUTPUT_ROOT")
    if not value or not Path(value).is_absolute() or not Path(value).is_dir():
        raise RuntimeError("--snapshot requires an existing absolute EMULEBB_WORKSPACE_OUTPUT_ROOT")
    root = Path(value).resolve()
    path = (root / destination).resolve()
    if path == root or not path.is_relative_to(root):
        raise RuntimeError("--snapshot must name a file below EMULEBB_WORKSPACE_OUTPUT_ROOT")
    return path


def main() -> int:
    """Poll until checks fail, complete, or time out."""

    args = parse_args()
    try:
        validate_timing(args)
        destination = resolve_snapshot(args.snapshot)
        repo = resolve_repo(args.repo)
        commit_sha = resolve_commit(repo, args.commit) if args.commit else None
        deadline = time.monotonic() + args.timeout_seconds
        last_signature: tuple[Any, ...] | None = None
        last_attempt = None
        last_jobs: dict[int, tuple[str, tuple[str, ...]]] = {}
        stable_since = time.monotonic()

        while True:
            jobs = []
            if args.pr is not None:
                pr, checks, runs = snapshot_pr(repo, args.pr)
                head_sha = str(pr["headRefOid"])
            elif args.run is not None:
                pr = None
                run = read_run(repo, args.run)
                head_sha = str(run.get("head_sha") or "")
                checks = []
                runs = [run]
                jobs = read_attempt_jobs(repo, run)
            else:
                pr = None
                head_sha = str(commit_sha)
                checks = []
                runs = read_head_runs(repo, head_sha)
            signature = snapshot_signature(head_sha, checks, runs)
            if args.run is not None:
                job_states = {job["id"]: job_state(job) for job in jobs}
                signature += (run["run_attempt"], tuple(sorted(job_states.items())))
            now = time.monotonic()
            if signature != last_signature:
                if args.run is not None:
                    report_attempt(run, jobs, last_jobs if run["run_attempt"] == last_attempt else {}, destination)
                    last_attempt, last_jobs = run["run_attempt"], job_states
                else:
                    print_summary(checks, runs)
                last_signature = signature
                stable_since = now

            failed = any(check_bucket(item) == "failed" for item in checks) or any(
                run_bucket(item) == "failed" for item in runs
            )
            pending = any(check_bucket(item) == "pending" for item in checks) or any(
                run_bucket(item) == "pending" for item in runs
            )
            observed = bool(checks or runs)

            if failed:
                print_failures(checks, runs)
                return 1
            if args.once:
                return 0 if observed and not pending else 8
            if observed and not pending and now - stable_since >= args.settle_seconds:
                if pr is not None:
                    detail = (
                        f"PR #{args.pr} head={head_sha[:8]} "
                        f"merge={pr.get('mergeStateStatus')}/{pr.get('mergeable')} {pr.get('url')}"
                    )
                elif args.run is not None:
                    detail = f"run {args.run} head={head_sha[:8]} {runs[0].get('html_url') or ''}".rstrip()
                else:
                    detail = f"commit {head_sha[:8]} https://github.com/{repo}/commit/{head_sha}"
                print(f"complete: {detail}", flush=True)
                return 0
            if now >= deadline:
                if args.pr is not None:
                    target_name = f"PR #{args.pr}"
                elif args.run is not None:
                    target_name = f"run {args.run}"
                else:
                    target_name = f"commit {head_sha[:8]}"
                print(f"timeout: {target_name} did not reach a final Actions state", file=sys.stderr)
                return 3
            time.sleep(args.interval_seconds)
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
