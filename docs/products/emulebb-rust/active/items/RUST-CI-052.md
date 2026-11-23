---
id: RUST-CI-052
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/351
title: Qualify the Rust foundation under sustained mixed load
status: OPEN
priority: Major
category: ci
labels: [rust]
milestone: rust-v0.1.0-beta.3
created: 2026-11-23
source: Public Foundation Round One backlog cutover
---

# RUST-CI-052 - Qualify the Rust foundation under sustained mixed load

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/351. Project #3 owns placement.

The foundation keeps mixed transfers, watched-library changes, bounded reads, and persistence responsive on large profiles. The retained capacity runs cover fixed workloads. This issue qualifies resource growth and durable progress over time.

## Acceptance

- Record the exact source bundle, isolated profile, duration, workload and resource limits before the run.
- Use the persisted Harness to overlap verified payload progress, watched-library mutation and scans, paged REST reads, and SQLite writes.
- Compare warm and final memory, queue latency and progress samples against the declared limits. Verify durable state after graceful stop and restart and retain one report.

Predecessors [#155](https://github.com/emulebb/emulebb-rust/issues/155), [#298](https://github.com/emulebb/emulebb-rust/issues/298). [Foundation contract](../../design/PUBLIC-FOUNDATION.md)
