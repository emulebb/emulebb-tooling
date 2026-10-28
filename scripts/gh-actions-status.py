#!/usr/bin/env python3
"""Poll one pull request's GitHub Actions state with compact output."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from collections import Counter
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


def snapshot(repo: str, pr_number: int) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """Read one consistent-enough Actions snapshot for the current PR head."""

    pr = read_pr(repo, pr_number)
    head_sha = str(pr.get("headRefOid") or "")
    if not head_sha:
        raise RuntimeError(f"pull request #{pr_number} has no head SHA")
    return pr, read_checks(repo, pr_number), read_head_runs(repo, head_sha)


def snapshot_signature(
    pr: dict[str, Any], checks: list[dict[str, Any]], runs: list[dict[str, Any]]
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
    return str(pr.get("headRefOid") or ""), check_values, run_values


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
    parser.add_argument("--pr", type=int, required=True, help="Pull request number to monitor.")
    parser.add_argument("--repo", help="Optional OWNER/REPO override. Defaults to the current checkout.")
    parser.add_argument("--once", action="store_true", help="Print one snapshot without waiting.")
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


def main() -> int:
    """Poll until checks fail, complete, or time out."""

    args = parse_args()
    try:
        validate_timing(args)
        repo = resolve_repo(args.repo)
        deadline = time.monotonic() + args.timeout_seconds
        last_signature: tuple[Any, ...] | None = None
        stable_since = time.monotonic()

        while True:
            pr, checks, runs = snapshot(repo, args.pr)
            signature = snapshot_signature(pr, checks, runs)
            now = time.monotonic()
            if signature != last_signature:
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
                print(
                    f"complete: PR #{args.pr} head={str(pr['headRefOid'])[:8]} "
                    f"merge={pr.get('mergeStateStatus')}/{pr.get('mergeable')} {pr.get('url')}",
                    flush=True,
                )
                return 0
            if now >= deadline:
                print(f"timeout: PR #{args.pr} did not reach a final Actions state", file=sys.stderr)
                return 3
            time.sleep(args.interval_seconds)
    except (OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
