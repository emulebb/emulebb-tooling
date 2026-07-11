---
id: RUST-REF-005
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/7
title: Decompose oversized Rust modules by responsibility
status: IN_PROGRESS
priority: Major
category: refactor
labels: [maintainability, rust, architecture]
milestone: release-0.1.0-beta.1
created: 2026-07-10
source: Operator maintainability direction 2026-07-10
---

# RUST-REF-005 - Decompose oversized Rust modules by responsibility

## Summary

Reduce the Rust client's legacy oversized source files through small,
behavior-preserving extractions. Start with `emulebb-core/src/lib.rs`, which is
13,711 lines at the start of this item, then continue through the largest
responsibility-mixed production and test modules.

## Invariants

- Preserve public Rust paths, REST/OpenAPI behavior, serialization, persistence,
  and configuration semantics.
- Preserve stock-compatible eD2K/Kad behavior and all VPN fail-closed boundaries.
- Keep module boundaries responsibility-based; do not split cohesive control flow
  solely to satisfy a mechanical line count.
- Remove private dead code and dependencies only when repository-wide references,
  all-target Clippy, and tests prove they are unused.
- Deliver each extraction as a separate reviewed and validated commit.

## Work Plan

1. Split the inline `emulebb-core` tests into responsibility-focused modules.
2. Move the `EmulebbCore` facade and API implementations into focused modules.
3. Split download and Kad orchestration into explicit runtime responsibilities.
4. Use non-failing maintainability advisories to identify files that deserve a
   responsibility review; do not treat line count as a validation limit.
5. Continue with the largest mixed-responsibility modules in the core and
   protocol crates.

## Acceptance Criteria

- [ ] `emulebb-core/src/lib.rs` is a thin crate root with stable public re-exports.
- [ ] Inline core tests are grouped by subsystem with unchanged assertions.
- [ ] Static IPv4 and P2P binding audits cover every relocated boundary.
- [ ] No repository-local Cargo `target` directory is created.
- [ ] Workspace format, Clippy, tests, Kad swarm, and VPN leak gates pass.
- [ ] Remaining large files are reviewed by responsibility without hard limits
      or per-file allowlist rationales.
- [ ] Substantial tests live in sibling test modules or integration-test trees;
      only focused white-box tests remain inline with production code.

## Validation

- `python tools\rust_quality_gate.py policy`
- `python -m emule_workspace validate --include-product-family --product-family-tier full`
- Rust workspace, isolated Kad swarm, and VPN leak gates through supported
  workspace orchestration.
