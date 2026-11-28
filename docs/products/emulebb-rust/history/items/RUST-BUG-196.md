---
id: RUST-BUG-196
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/384
title: Report unverified Kad UDP reachability as unknown
status: DONE
priority: Minor
category: bug
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/384. This local document owns the durable engineering specification and evidence.

# RUST-BUG-196 - Report unverified Kad UDP reachability as unknown

## Closure

REST reports an unknown UDP verdict until verified and after expiration. The UI renders unknown. The fixture covers verified open, retest, verified closed, and expiration while preserving stock wire behavior.

Verified on Rust main `c1414405`. [PR #406](https://github.com/emulebb/emulebb-rust/pull/406) · [Exact main CI](https://github.com/emulebb/emulebb-rust/actions/runs/46121217391) · [Optional platform CI](https://github.com/emulebb/emulebb-rust/actions/runs/46121217360) · [Nightly workflow](https://github.com/emulebb/emulebb-rust/actions/runs/46124453788)

Show unverified UDP state as unknown in REST and WebUI. Leave stock HELLO and publication wire semantics intact and prove startup, verified and retest states.

This is a parallel Client follow-up. Record the exact stock eMule and
amule-org aMule revisions and retain the relevant fixtures with
[RUST-CI-031](../../active/items/RUST-CI-031.md).
