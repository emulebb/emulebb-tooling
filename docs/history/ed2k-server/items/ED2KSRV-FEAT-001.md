---
id: ED2KSRV-FEAT-001
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/8
title: Add graceful shutdown and supervised task lifecycle
status: WONT_DO
priority: Major
category: feature
labels: [operations, shutdown, task-lifecycle, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-FEAT-001 - Add graceful shutdown and supervised task lifecycle

## Summary

Give the service a bounded SIGINT/SIGTERM shutdown path and ownership of all
long-lived/background tasks so deployments can drain, stop, and restart safely.

## Acceptance Criteria

- [ ] SIGINT and SIGTERM stop new admission, notify listeners/workers, and begin drain.
- [ ] Long-lived and per-request tasks are supervised; failures and panics are surfaced.
- [ ] Shutdown has a configurable deadline followed by explicit cancellation.
- [ ] Session/file cleanup preserves internal invariants during drain and forced cancellation.
- [ ] The systemd unit runs as a dedicated unprivileged identity with journald-visible logs and appropriate hardening.
- [ ] Integration evidence covers clean shutdown, forced timeout, and immediate restart on the same ports.

## Notes

This item must coordinate with the bounded work model in `ED2KSRV-BUG-003`.
