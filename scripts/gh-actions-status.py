#!/usr/bin/env python3
"""Poll one pull request, exact commit, or workflow run compactly."""

from __future__ import annotations

import argparse
import json
import os
import re
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
    return read_jobs(f"repos/{repo}/actions/runs/{run['id']}/attempts/{attempt}/jobs?per_page=100", run["id"])


def read_jobs(endpoint: str, run_id: int) -> list[dict[str, Any]]:
    """Read the paginated inventory for a single run."""
    pages = run_gh(["api", "--paginate", "--slurp", endpoint])
    if not isinstance(pages, list) or not pages:
        raise RuntimeError("workflow attempt returned no job inventory")
    jobs = []
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("jobs"), list):
            raise RuntimeError("workflow attempt returned invalid job data")
        jobs.extend(page["jobs"])
    if any(not isinstance(job, dict) or type(job.get("id")) is not int or job.get("run_id") != run_id
           or type(job.get("run_attempt")) is not int or not isinstance(job.get("name"), str) for job in jobs):
        raise RuntimeError("workflow attempt returned invalid job identity")
    return jobs


def previous_job_names(repo: str, run: dict[str, Any]) -> set[str]:
    """Record prior job names once per rerun so previously skipped work stays new."""
    if run["run_attempt"] == 1:
        return set()
    history = read_jobs(f"repos/{repo}/actions/runs/{run['id']}/jobs?filter=all&per_page=100", run["id"])
    return {job["name"] for job in history if job["run_attempt"] < run["run_attempt"]
            and job.get("conclusion") not in {None, "skipped"}}


def job_state(job: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    """Key visible transitions by state and any failed steps."""
    state = str(job.get("conclusion") or job.get("status") or "unknown")
    failed = tuple(str(step["name"]) for step in job.get("steps") or []
                   if step.get("name") and step.get("conclusion") in RUN_FAILURE_CONCLUSIONS)
    return state, failed


def failure_kind(job: dict[str, Any]) -> str | None:
    """Classify only failures with a useful signal in the job metadata."""
    state, steps = job_state(job)
    first = steps[0].lower() if steps else ""
    if state == "skipped":
        return "skipped"
    if state in {"queued", "waiting", "pending", "requested"} and not job.get("runner_id"):
        return "waiting-for-runner"
    if state in {"startup_failure", "timed_out"} and not job.get("runner_id") and not steps:
        return "runner-startup"
    if state not in RUN_FAILURE_CONCLUSIONS:
        return None
    if first.startswith(("download ", "install ", "restore ", "set up ")):
        return "dependency-setup"
    if any(word in first for word in ("test", "smoke", "conformance")):
        return "product-or-test"
    return "unknown"


def write_snapshot(destination: Path, payload: dict[str, Any]) -> None:
    """Replace the snapshot only once complete JSON is available."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent, prefix="actions-status-") as temp:
        staged = Path(temp) / "snapshot.json"
        staged.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
        staged.replace(destination)


def elapsed_seconds(start: str | None, end: str | None, now: datetime) -> int | None:
    """Use the reported start and end rather than the polling interval."""
    if not start:
        return None
    started = datetime.fromisoformat(start)
    finished = datetime.fromisoformat(end) if end else now
    return max(0, int((finished - started).total_seconds()))


def job_timing(job: dict[str, Any], prior_names: set[str], now: datetime) -> tuple[str, int | None, int | None]:
    """Distinguish queue and execution time from copied Actions job records."""
    if job.get("conclusion") == "skipped":
        return "skipped", None, None
    created, started, completed = (job.get(field) for field in ("created_at", "started_at", "completed_at"))
    # WHY: GitHub gives copied jobs new IDs, creation times and attempt numbers,
    # while preserving the execution timestamps of the earlier attempt.
    if created and started and datetime.fromisoformat(started) < datetime.fromisoformat(created):
        return "reused", None, elapsed_seconds(started, completed, now)
    disposition = "rerun" if job["name"] in prior_names else "new"
    if job.get("status") in {"queued", "waiting", "pending", "requested"}:
        return disposition, elapsed_seconds(created, None, now), None
    queue = elapsed_seconds(created, started, now) if started else None
    return disposition, queue, elapsed_seconds(started, completed, now)


def report_attempt(run: dict[str, Any], jobs: list[dict[str, Any]],
                   previous: dict[int, tuple[str, tuple[str, ...]]], prior_names: set[str],
                   destination: Path | None) -> None:
    """Print job transitions and optionally persist the same snapshot as compact JSON."""
    now = datetime.now(timezone.utc)
    elapsed = elapsed_seconds(run.get("run_started_at"),
                              run.get("updated_at") if run.get("status") == "completed" else None, now)
    counts = Counter(job_state(job)[0] for job in jobs)
    count_summary = " ".join(f"{name}={count}" for name, count in sorted(counts.items()))
    timings = {job["id"]: job_timing(job, prior_names, now) for job in jobs}
    disposition_counts = Counter(state for state, _, _ in timings.values())
    max_queue = max((queue for _, queue, _ in timings.values() if queue is not None), default=None)
    max_execution = max((execution for state, _, execution in timings.values()
                         if state != "reused" and execution is not None), default=None)
    print(f"run {run['id']} attempt {run['run_attempt']}: {run.get('conclusion') or run['status']}"
          f" elapsed={elapsed if elapsed is not None else '?'}s {count_summary}"
          f" rerun={disposition_counts['rerun']} reused={disposition_counts['reused']}"
          f" maxQueue={max_queue if max_queue is not None else '?'}s"
          f" maxExecution={max_execution if max_execution is not None else '?'}s", flush=True)
    snapshot = []
    for job in jobs:
        state, steps = job_state(job)
        disposition, queue, duration = timings[job["id"]]
        snapshot.append({"id": job["id"], "name": job["name"], "state": state, "disposition": disposition,
                         "queueSeconds": queue, "elapsedSeconds": duration,
                         "failedSteps": steps, "firstFailedStep": steps[0] if steps else None,
                         "failureKind": failure_kind(job), "url": job.get("html_url")})
        if previous.get(job["id"]) == (state, steps) or state == "skipped":
            continue
        if not previous and state in {"success", "neutral"} and disposition != "rerun":
            continue
        name = job["name"].rsplit(" / ", 1)[-1]
        suffix = f" step={', '.join(steps)}" if steps else ""
        if state in RUN_FAILURE_CONCLUSIONS:
            suffix += f" {job.get('html_url') or ''}"
        print(f"  {name}: {state} ({disposition}) queue={queue if queue is not None else '?'}s"
              f" execution={duration if duration is not None else '?'}s{suffix}", flush=True)
    if destination is not None:
        payload = {"id": run["id"], "attempt": run["run_attempt"], "sourceSha": run.get("head_sha"),
                   "status": run["status"], "conclusion": run.get("conclusion"), "elapsedSeconds": elapsed,
                   "observedAt": now.isoformat(), "jobs": snapshot, "url": run.get("html_url"),
                   "maxQueueSeconds": max_queue, "maxExecutionSeconds": max_execution,
                   "rerunJobs": [job["name"] for job in snapshot if job["disposition"] == "rerun"],
                   "reusedJobCount": disposition_counts["reused"]}
        write_snapshot(destination, payload)


def retry_job(repo: str, run_id: int, attempt: int, job_id: int) -> None:
    """Request one job rerun after verifying its current failed attempt."""
    run = read_run(repo, run_id)
    if run["run_attempt"] != attempt or run["status"] != "completed":
        raise RuntimeError("Retry requires the requested run attempt to be current and completed")
    job = next((row for row in read_attempt_jobs(repo, run) if row["id"] == job_id), None)
    if not job or job["run_attempt"] != attempt or job.get("conclusion") not in RUN_FAILURE_CONCLUSIONS:
        raise RuntimeError("Retry requires a failed job from that exact attempt")
    try:
        run_gh(["api", "--method", "POST", f"repos/{repo}/actions/jobs/{job_id}/rerun"], json_output=False)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        # WHY: an unsuccessful response can follow an accepted mutation.
        current = read_run(repo, run_id)
        if current["run_attempt"] <= attempt and current["status"] == "completed":
            raise RuntimeError(
                "Retry acceptance is unresolved. Observe the run before issuing any further request"
            ) from error
    print(f"Observe the retry at {run['html_url']}")


def verify_nightly_publication(repo: str, run: dict[str, Any], jobs: list[dict[str, Any]], tag: str) -> bool:
    """Require executed publication jobs and a final release on the producer commit."""
    if run.get("path") != ".github/workflows/nightly.yml" or not re.fullmatch(r"rust-v[0-9][A-Za-z0-9.+-]*", tag):
        raise RuntimeError("Publication verification requires a Nightly run and exact Rust tag")
    expected = {"Publish both verified container variants", "Publish verified native release assets",
                "Advance both verified nightly image channels"}
    executed = {job["name"].rsplit(" / ", 1)[-1] for job in jobs if job.get("conclusion") == "success"}
    if not expected <= executed:
        print("Publication skipped or incomplete. Expected publication jobs did not all pass.")
        return False
    release = run_gh(["api", f"repos/{repo}/releases/tags/{tag}"])
    commit = run_gh(["api", f"repos/{repo}/commits/{tag}"])
    if release["draft"] or not release["assets"] or commit["sha"] != run["head_sha"]:
        raise RuntimeError("Final release bytes or tag do not match the Nightly source")
    print(f"Verified Nightly publication {release['html_url']}")
    return True


def dispatch_diagnostic(repo: str, request_id: str, inputs: list[str]) -> None:
    """Send each correlated ARM64 diagnostic dispatch at most once locally."""
    if repo != "emulebb/emulebb-rust" or not re.fullmatch(r"[a-f0-9]{32}", request_id):
        raise RuntimeError("Select emulebb/emulebb-rust and a 32-character lowercase hexadecimal request ID")
    required = {"run_id", "attempt", "source_sha", "artifact_name", "artifact_sha256", "harness_sha"}
    pairs = dict(item.split("=", 1) for item in inputs)
    if set(pairs) != required or len(pairs) != len(inputs) or not all(pairs.values()):
        raise RuntimeError(f"Supply each diagnostic input exactly once: {', '.join(sorted(required))}")
    endpoint = f"repos/{repo}/actions/workflows/arm64-package-replay.yml"
    title = f"ARM64 package replay {request_id}"
    receipt = resolve_snapshot(Path("reports/actions-dispatch") / f"{request_id}.json")

    def find_run() -> dict[str, Any] | None:
        runs = run_gh(["api", f"{endpoint}/runs?event=workflow_dispatch&branch=main&per_page=100"])
        matches = [run for run in runs["workflow_runs"] if run["display_title"] == title]
        if len(matches) > 1:
            raise RuntimeError("More than one Actions run has the diagnostic request ID")
        return matches[0] if matches else None

    found = find_run()
    if found:
        print(found["html_url"])
        return
    receipt.parent.mkdir(parents=True, exist_ok=True)
    try:
        with receipt.open("x", encoding="utf-8") as stream:
            json.dump({"workflow": endpoint, "requestId": request_id, "inputs": pairs}, stream)
    except FileExistsError as exc:
        raise RuntimeError("Dispatch was already attempted. Observe Actions for this request ID") from exc
    arguments = ["api", "--method", "POST", f"{endpoint}/dispatches", "-f", "ref=main"]
    for name, value in {**pairs, "request_id": request_id}.items():
        arguments.extend(["-f", f"inputs[{name}]={value}"])
    try:
        run_gh(arguments, json_output=False)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        found = find_run()
        if not found:
            raise RuntimeError("Dispatch acceptance is unresolved. Observe Actions using the same request ID") from exc
    print(found["html_url"] if found else f"Dispatched {title}")


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
    target.add_argument("--dispatch-arm64", metavar="REQUEST_ID", help="Dispatch one correlated ARM64 diagnostic.")
    parser.add_argument("--input", action="append", default=[], metavar="NAME=VALUE", help="ARM64 diagnostic workflow input.")
    parser.add_argument("--repo", help="Optional OWNER/REPO override. Defaults to the current checkout.")
    parser.add_argument("--once", action="store_true", help="Print one snapshot without waiting.")
    parser.add_argument("--snapshot", type=Path, help="Save JSON under the inherited output root.")
    parser.add_argument("--retry-job", type=int, metavar="JOB_ID", help="Explicitly retry a failed job and its dependents.")
    parser.add_argument("--attempt", type=int, help="Expected completed attempt for --retry-job.")
    parser.add_argument("--publication-tag", help="Require actual Nightly publication of this exact tag in --run mode.")
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
    if args.retry_job is not None:
        if args.run is None or not args.attempt or args.attempt < 1 or args.retry_job < 1 or args.once or args.snapshot:
            raise RuntimeError("--retry-job requires --run and a positive --attempt in place of monitoring options")
    elif args.attempt is not None:
        raise RuntimeError("--attempt requires --retry-job")
    if args.publication_tag and (args.run is None or args.retry_job is not None):
        raise RuntimeError("--publication-tag requires --run monitoring")
    if args.dispatch_arm64 is not None:
        if args.once or args.snapshot:
            raise RuntimeError("Diagnostic dispatch does not accept monitoring options")
    elif args.input:
        raise RuntimeError("--input requires --dispatch-arm64")


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
        if args.dispatch_arm64 is not None:
            dispatch_diagnostic(repo, args.dispatch_arm64, args.input)
            return 0
        if args.retry_job is not None:
            retry_job(repo, args.run, args.attempt, args.retry_job)
            return 0
        commit_sha = resolve_commit(repo, args.commit) if args.commit else None
        deadline = time.monotonic() + args.timeout_seconds
        last_signature: tuple[Any, ...] | None = None
        last_attempt = None
        last_jobs: dict[int, tuple[str, tuple[str, ...]]] = {}
        prior_names: set[str] = set()
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
                    if run["run_attempt"] != last_attempt:
                        prior_names = previous_job_names(repo, run)
                        last_jobs = {}
                    report_attempt(run, jobs, last_jobs, prior_names, destination)
                    last_attempt, last_jobs = run["run_attempt"], job_states
                else:
                    print_summary(checks, runs)
                    if destination is not None:
                        write_snapshot(destination, {
                            "repository": repo, "sourceSha": head_sha, "pullRequest": pr,
                            "checks": checks, "runs": runs, "observedAt": datetime.now(timezone.utc).isoformat(),
                        })
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
            if args.publication_tag and observed and not pending:
                return 0 if verify_nightly_publication(repo, run, jobs, args.publication_tag) else 4
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
