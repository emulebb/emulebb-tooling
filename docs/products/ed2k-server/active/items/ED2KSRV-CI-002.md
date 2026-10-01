---
id: ED2KSRV-CI-002
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/7
title: Qualify load, soak, and controlled canary gates
status: OPEN
priority: Major
category: ci
labels: [testing, load, soak, canary, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-CI-002 - Qualify load, soak, and controlled canary gates

## Summary

Define and automate the evidence required to advance from source-quality CI to
a controlled public canary and, eventually, a production recommendation.

## Scope Constraints

- Start with offline/local load and soak lanes in `repos/emulebb-build-tests`.
- Do not make `ed2k-server` the default test server as part of this item.
- A public canary requires a separate operator go/no-go after local gates pass.

## Acceptance Criteria

- [ ] Capacity targets define clients, files, requests/sec, memory, CPU, and latency budgets.
- [ ] Repeatable steady-state, burst, abusive-input, restart, and long-soak profiles retain evidence outside source trees.
- [ ] Resource ceilings and overload recovery from `ED2KSRV-BUG-001` through `003` pass under load.
- [ ] A canary runbook defines isolation, monitoring, rollback, data handling, and stop conditions.
- [ ] No production-ready claim is made until the canary result and remaining risks are explicitly accepted.

## Notes

Depends on the P0 resource-safety items, graceful lifecycle, and observability.
