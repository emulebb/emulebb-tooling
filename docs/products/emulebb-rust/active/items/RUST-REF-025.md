---
id: RUST-REF-025
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/350
title: Replace Chrono with time
status: OPEN
priority: Major
category: refactor
labels: [rust]
milestone: rust-v0.1.0-beta.3
created: 2026-11-23
source: RUSTSEC-2026-0543 foundation validation
---

# RUST-REF-025 - Replace Chrono with time

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/350. Project #3 owns placement.

Use the already-locked `time` crate for UTC calendar operations. Keep
standard-library clocks for elapsed time and deadlines. Remove the
advisory-specific exception recorded in
[PR #349](https://github.com/emulebb/emulebb-rust/pull/349).

- Preserve REST Unix seconds and nulls, SQLite timestamp units, internal Kad
  milliseconds, and existing timing boundaries.
- Preserve fixed-millisecond UTC diagnostic timestamps and RFC 3339 support
  and snoop records. Cover timestamp range and serialization boundaries.
- Remove Chrono from the workspace and fuzz dependency graphs and remove the
  RUSTSEC-2026-0543 exception. Pass Cargo Deny and the Windows, Linux, and REST gates.
