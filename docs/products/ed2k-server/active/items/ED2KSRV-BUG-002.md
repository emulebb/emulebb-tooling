---
id: ED2KSRV-BUG-002
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/3
title: Enforce configured client and publication limits
status: OPEN
priority: Critical
category: bug
labels: [resource-safety, admission-control, configuration, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-BUG-002 - Enforce configured client and publication limits

## Summary

The server advertises configurable limits for total clients, clients per IP,
soft/hard files, strings, and listener backlog, but several are not enforced at
the actual admission or publication boundaries. Make the configuration truthful
and remove hard-coded substitutes.

## Current State

Limits are defined in `src/config.rs` and sent during login. Publication has a
hard-coded `4000` check in `src/server/offerfiles.rs`; connection admission and
per-IP accounting do not consistently enforce the configured ceilings.

## Acceptance Criteria

- [ ] All plain, obfuscated, IPv4, and IPv6 listeners share atomic total-client admission.
- [ ] Per-IP limits have documented IPv4/IPv6 aggregation semantics and regression tests.
- [ ] Soft and hard publication limits have defined behavior and use the configured values.
- [ ] Listener backlog is applied as configured or removed from the public configuration.
- [ ] Rejections are observable and do not leak session/file state.
- [ ] Boundary and concurrent-admission tests prove the ceilings cannot be exceeded materially.

## Validation

Run focused concurrent admission/publication tests followed by the locked
source-quality and integration-test gates.
