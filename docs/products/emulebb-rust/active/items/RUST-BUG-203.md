---
id: RUST-BUG-203
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/404
title: Exclude the connected hostname server from global eD2K keyword search
status: OPEN
priority: Major
category: bug
labels: [rust, bug, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-27
source: Stock and aMule comparison for Beta 3 readiness
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/404. This local document owns the durable engineering specification and evidence.

# RUST-BUG-203 - Exclude the connected hostname server from global eD2K keyword search

## Summary

Resolve the configured server before checking it against the active TCP server. When the endpoint matches, send only the local TCP search. Continue the normal paced UDP search for other servers. Prove the resolved-hostname case with an isolated loopback socket.

[Reference](https://github.com/irwir/eMule/blob/ac3d52eafd88e9f6d9e0c2204c6dbead18db750b/srchybrid/SearchResultsWnd.cpp#L252)

## Validation

Retain deterministic package-level evidence under [RUST-CI-031](RUST-CI-031.md).
