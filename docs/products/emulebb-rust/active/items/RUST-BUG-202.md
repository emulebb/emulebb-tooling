---
id: RUST-BUG-202
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/403
title: Use a valid sender address for optional eD2K UDP obfuscation
status: OPEN
priority: Major
category: bug
labels: [rust, bug, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-27
source: Stock and aMule comparison for Beta 3 readiness
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/403. This local document owns the durable engineering specification and evidence.

# RUST-BUG-202 - Use a valid sender address for optional eD2K UDP obfuscation

## Summary

Use stock plaintext framing for ordinary reasks and replies when the local public IPv4 or peer hash is unknown. Preserve valid known-address obfuscation and required-encryption TCP policy. Cover both send directions and the reported framing state in deterministic tests.

[Reference](https://github.com/amule-org/amule/pull/2614)

## Validation

Retain deterministic package-level evidence under [RUST-CI-031](RUST-CI-031.md).
