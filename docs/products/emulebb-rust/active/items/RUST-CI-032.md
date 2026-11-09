---
id: RUST-CI-032
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/258
title: Add dependency-aware early Rust checks without weakening pre-push coverage
status: OPEN
priority: Major
category: ci
labels: [rust, ci, tests, workflow]
milestone: post-beta-polish
created: 2026-11-07
source: Operator-approved local and GitHub CI parity follow-up
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/258. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-032 - Add dependency-aware early Rust checks without weakening pre-push coverage

## Current Focus (2026-11-09)

The operator prioritizes workspace improvements and multiarchitecture/
multiplatform development before the broader bugs/issues queue, with Beta3
release held. This dependency-aware feedback item is now Major because full
validation latency limits that parallel work. Its post-beta-polish milestone
is unchanged; this priority change does not introduce a new release gate.
Keep the complete pre-push/hosted checks and existing workspace lock authority;
faster partial feedback must not claim complete qualification. GitHub issue
[#258](https://github.com/emulebb/emulebb-rust/issues/258) and Project #3 own
execution status. Current qualification may continue; no candidate freeze,
certification, release dispatch, publication, tag, or version bump is authorized.

## Summary

Add faster developer feedback before the complete pre-push gate. Reuse the
canonical Rust check definitions and Cargo's dependency metadata to select
changed workspace crates and their dependants. This is follow-up backlog work;
the current CI/CD cleanup keeps complete applicable pre-push validation.

## Acceptance Criteria

- [ ] An explicit developer check mode validates changed crates and affected
      workspace dependants using the existing orchestration and workspace lock.
- [ ] Shared manifests, lockfiles, toolchains, build scripts, feature selection,
      and uncertain change ownership expand to the full relevant validation set.
- [ ] Package selection has regression coverage for cross-crate changes and
      dependency changes; unknown inputs cannot silently omit checks.
- [ ] Full pre-push and required GitHub coverage remains intact, including
      doctests, diagnostics, observed-egress tests, UI, and REST conformance.
- [ ] Reports distinguish partial developer feedback from complete validation.
      No prior-pass receipts or automatic retries hide failures.
- [ ] Evaluate an alternative runner such as nextest only with demonstrated
      benefit and equivalent coverage, including explicit doctest execution and
      resource-sharing test serialization. Adoption is a separate decision.

## Constraints And Validation

Use supported feature combinations rather than blanket `--all-features`;
`egress-audit` remains test-only. Keep generated output external and operator
environment unchanged. Validate representative dependent-crate changes and the
complete gate on the same source revision before claiming equivalent coverage.

Broader Rust structure and runtime safety work remains in RUST-REF-005 and
RUST-REF-006; deterministic protocol test quality remains in RUST-CI-031.
