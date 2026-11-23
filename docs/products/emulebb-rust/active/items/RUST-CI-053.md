---
id: RUST-CI-053
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/352
title: Qualify live upload and REST during SQLite writer contention
status: OPEN
priority: Major
category: ci
labels: [rust]
milestone: rust-v0.1.0-beta.3
created: 2026-11-23
source: Public Foundation Round One backlog cutover
---

# RUST-CI-053 - Qualify live upload and REST during SQLite writer contention

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/352. Project #3 owns placement.

The bounded persistence owner keeps SQLite waits off async execution. Existing forced writer contention proof establishes executor progress and durable friend-write drain. This issue extends the proof to active upload and REST responsiveness.

## Acceptance

- Hold a synthetic SQLite writer lock while a real upload is active and measure upload byte growth plus an unrelated REST read and peer timer.
- Verify bounded admission while locked. Release the lock and verify queued writes reconcile, drain, and survive reopen.
- Retain the exact source bundle and one reproducible result.

Predecessors [#155](https://github.com/emulebb/emulebb-rust/issues/155). [Foundation contract](../../design/PUBLIC-FOUNDATION.md)
