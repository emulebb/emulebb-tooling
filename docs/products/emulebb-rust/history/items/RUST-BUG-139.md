---
id: RUST-BUG-139
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/188
title: Bound Kad restrictive-search evaluation work
status: DONE
priority: Major
category: bug
labels: [rust, kad, search, resource-bounds, abuse-resistance]
milestone: rust-v0.1.0-beta.3
created: 2026-10-30
source: 2026-10-30 current-aMule hardening review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/188. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-139 - Bound Kad restrictive-search evaluation work

## Summary

Add request-wide work budgets so a legal-depth restrictive Kad query cannot
amplify parsing and comparison work across a large local index.

## Intended Shape

- Parse and normalize request terms once.
- Budget AST nodes, compared values or tags, candidates examined, and results emitted.
- Stop deterministically on exhaustion without changing wire shapes.
- Keep ordinary stock-shaped searches below the budget result-equivalent.

## Acceptance Criteria

- [x] Every restrictive-search request has one shared work budget.
- [x] Evaluation does not reparse or renormalize the request per indexed entry.
- [x] Adversarial large-index tests prove bounded work.
- [x] Normal deterministic search fixtures preserve their results.

## Validation

- Focused parser, evaluator, and large-index budget tests.
- Existing Kad search request/response goldens.

## Resolution

- Added shared AST, candidate, tag, and normalization budgets for restrictive Kad searches.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-index`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`
