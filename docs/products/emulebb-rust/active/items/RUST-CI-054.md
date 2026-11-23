---
id: RUST-CI-054
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/353
title: Qualify final-block takeover latency and aMule interoperation
status: OPEN
priority: Minor
category: ci
labels: [rust]
milestone: post-beta-compatibility
created: 2026-11-23
source: Public Foundation Round One backlog cutover
---

# RUST-CI-054 - Qualify final-block takeover latency and aMule interoperation

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/353. Project #3 owns placement.

Bounded endgame takeover lets healthy peers finish stalled final blocks. Existing loopback tests cover both winners, accounting, and redundant socket drain. Comparative latency and an independent client witness remain.

## Acceptance

- Run the same deterministic slow-final-source fixture with and without takeover. Compare completion times and verify payload hashes and source attribution.
- Verify failed-takeover requeue and bounded duplicate traffic. Record socket drain and any supported wire cancellation explicitly.
- Retain a local frozen-aMule witness with exact source and fixture provenance.

Predecessors [#27](https://github.com/emulebb/emulebb-rust/issues/27). [Foundation contract](../../design/PUBLIC-FOUNDATION.md)
