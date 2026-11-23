---
id: RUST-CI-055
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/354
title: Qualify Kad checkpoint cadence and import-only lifecycle
status: OPEN
priority: Major
category: ci
labels: [rust]
milestone: post-beta-polish
created: 2026-11-23
source: Public Foundation Round One backlog cutover
---

# RUST-CI-055 - Qualify Kad checkpoint cadence and import-only lifecycle

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/354. Project #3 owns placement.

SQLite owns the bounded Kad routing snapshot, and compatibility met files are import inputs. Existing tests cover changed-state persistence, race handling, and restart. This issue qualifies the periodic and import-only lifecycle end to end.

## Acceptance

- Verify dirty state on the 15-minute cadence and no write for a clean interval.
- Verify stopped and running URL imports commit immediately, then restart with the expected identity and contact fields.
- Verify automatic seed, import, checkpoint and final shutdown never write either compatibility met file.

Predecessors [#233](https://github.com/emulebb/emulebb-rust/issues/233). [Foundation contract](../../design/PUBLIC-FOUNDATION.md)
