---
id: ED2KSRV-FEAT-003
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/10
title: Make source selection bounded and fair
status: OPEN
priority: Major
category: feature
labels: [protocol, sources, fairness, compatibility]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-FEAT-003 - Make source selection bounded and fair

## Summary

Define bounded, compatible source selection that avoids returning the same
prefix indefinitely for popular files and behaves predictably across HighID,
LowID, IPv4, IPv6, and obfuscated-source cases.

## Acceptance Criteria

- [ ] Per-response source counts are explicitly bounded and protocol-compatible.
- [ ] Repeated requests rotate or sample fairly without unbounded per-request work.
- [ ] Stale, unreachable, incompatible, or requester-self sources are excluded consistently.
- [ ] Smart-source caching cannot freeze a biased subset indefinitely.
- [ ] Golden and statistical tests cover popular files, mixed address families, LowID, and obfuscation.
- [ ] Behavior differences from Go and observed Lugdunum are documented and intentional.

## Notes

Validation uses the corpus from `ED2KSRV-CI-001` and the scale profiles from
`ED2KSRV-CI-002`.
