---
id: RUST-REF-006
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/9
title: Consolidate Rust NAT and runtime safety internals
status: OPEN
priority: Major
category: refactor
labels: [rust, nat, safety, concurrency, maintainability]
milestone: post-beta-polish
created: 2026-07-11
source: Operator-approved Rust development hygiene review 2026-07-11
---

# RUST-REF-006 - Consolidate Rust NAT and runtime safety internals

## Summary

Keep obsolete Rust NAT implementations retired while the capability-aware
PCP/NAT-PMP-first stack in RUST-FEAT-037 owns provider architecture. Continue
hardening synchronous runtime state and native-code boundaries without changing
eD2K/Kad wire behavior.

## Release Triage (2026-09-30)

**Post-beta.** The remaining lock/lint consolidation is maintainability work,
not a demonstrated release defect. RUST-FEAT-037 supersedes this item's former
provider-diversity scope: PCP/NAT-PMP is preferred, MiniUPnPc is the fallback,
and the Rust in-tree SSDP/SOAP provider is removed.

## Scope

- Keep the deprecated `rupnp` backend, its `ssdp-client` dependency, and
  personal Git patches absent.
- Leave provider selection, fallback, settings migration, and live NAT evidence
  to RUST-FEAT-037.
- Adopt non-poisoning `parking_lot::Mutex` for short synchronous runtime state;
  keep asynchronous locks only where a guard must cross `.await`.
- Fail closed explicitly for security-sensitive state instead of relying on
  mutex poisoning.
- Audit every unsafe boundary, especially `Gateway: Send`, and enable
  `unsafe_op_in_unsafe_fn` plus documented-unsafe-block enforcement.
- Narrow broad dead-code and unused-import suppressions after reference and
  feature-matrix proof.

## Acceptance Criteria

- [x] NAT provider architecture is separated into RUST-FEAT-037 and no longer
      blocks this runtime-safety refactor.
- [x] `rupnp`, `ssdp-client`, and their dependency stack are absent from source,
      manifests, and the lockfile.
- [ ] Short synchronous runtime state cannot cascade through mutex poisoning.
- [ ] Security-sensitive failure paths are explicitly fail-closed.
- [x] Every unsafe block and unsafe implementation has a concrete safety proof.
- [ ] Broad lint suppressions are removed or reduced to justified items.

## Validation

- Focused lock, unsafe-boundary, and fail-closed state tests.
- Supported workspace Rust format, Clippy, build, tests, Kad swarm, and VPN leak
  gates.

## Evidence

- `6348bb0`, `1c81311`, `e334933`, `8ad2668`, and `b56bc95` move the credit
  ledger, Kad rate limiter, Kad peer state, Kad RPC tracking, and eD2K connection
  budget to non-poisoning synchronous locks with focused tests.
- `e1c3705` removes the unnecessary unsafe `Gateway: Send` implementation after
  isolated MiniUPnPc and eD2K compilation proved it was not required.
- `2c97349` makes all 14 crates inherit deny-level `unsafe_op_in_unsafe_fn` and
  `undocumented_unsafe_blocks`, with concrete FFI safety invariants at each
  remaining unsafe block.
- `7a22c3f` implements and tests the independent bind-pinned SSDP/SOAP IGD
  fallback without reviving the retired dependency stack; RUST-FEAT-037 later
  supersedes and removes that provider in favor of PCP/NAT-PMP plus MiniUPnPc.
