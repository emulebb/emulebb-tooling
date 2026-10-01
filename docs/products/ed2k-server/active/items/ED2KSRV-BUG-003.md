---
id: ED2KSRV-BUG-003
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/4
title: Bound TCP and UDP work admission and rate limits
status: OPEN
priority: Critical
category: bug
labels: [resource-safety, rate-limiting, udp, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-BUG-003 - Bound TCP and UDP work admission and rate limits

## Summary

Introduce bounded concurrency and rate limits for remotely initiated TCP, UDP,
search, callback, probe, and gossip work. Overload must shed work predictably
without starving existing sessions or the runtime.

## Intended Shape

- Shared bounded work budgets for expensive operations.
- Per-source and global rate limits covering IPv4 and IPv6.
- Explicit rejection/drop metrics by path and reason.
- Load-shedding behavior that remains responsive under abusive traffic.

## Acceptance Criteria

- [ ] Every remotely triggered background path has an explicit concurrency/queue budget.
- [ ] TCP and UDP rate policies cover both address families and cannot be bypassed by listener choice.
- [ ] Callback, probe, search, and gossip work cannot create unbounded detached tasks.
- [ ] Existing sessions retain bounded service during overload and readiness reflects saturation.
- [ ] A repeatable overload test proves bounded queues, memory, and recovery after traffic stops.

## Notes

This item depends on the final configured ceilings from `ED2KSRV-BUG-002` and
feeds the scale campaign in `ED2KSRV-CI-002`.
