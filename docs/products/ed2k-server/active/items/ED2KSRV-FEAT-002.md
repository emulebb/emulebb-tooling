---
id: ED2KSRV-FEAT-002
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/9
title: Add production observability and restart recovery
status: OPEN
priority: Major
category: feature
labels: [operations, observability, recovery, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-FEAT-002 - Add production observability and restart recovery

## Summary

Expose the signals required to operate the server and prove that planned or
unexpected restarts return to a healthy, internally consistent state.

## Acceptance Criteria

- [ ] Metrics cover active/admitted/rejected sessions, files/sources, request rates, queue saturation, errors, and latency.
- [ ] Health and readiness have distinct meanings and readiness fails on critical saturation or incomplete startup.
- [ ] Structured logs identify lifecycle transitions and rejection/error classes without private payload data.
- [ ] Restart semantics document which state is ephemeral, how clients repopulate it, and expected recovery time.
- [ ] Crash/restart and configuration-reload tests show no stale registrations, corrupted counters, or false readiness.
- [ ] Operator guidance defines alert thresholds used by the soak and canary gates.

## Notes

Metrics must expose the admission decisions implemented by `ED2KSRV-BUG-002`
and `ED2KSRV-BUG-003`.
