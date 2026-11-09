---
id: RUST-REF-006
workflow: github
product: emulebb-rust
phase: Phase 0
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

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/9. This local document is retained as the durable engineering spec and evidence record.

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
- Leave provider selection, current settings, and live NAT evidence
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
- [ ] Background tasks have explicit cancellation and shutdown owners, and
      tests observe task completion instead of relying on fixed sleeps.
- [ ] Synchronous lock guards do not span `.await`; bounded queues expose
      backpressure and failure rather than silently dropping required work.
- [ ] Targeted async and safety lints are adopted with focused fixes and narrow,
      reasoned exceptions. Avoid blanket pedantic enforcement or broad allows.

These are backlog follow-ups, not prerequisites for the current CI/CD cleanup.
Beta contracts may change together when necessary; no legacy implementation,
compatibility alias, or migration is introduced to preserve the prior shape.

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

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_async-lifecycle.md` section 2.1 (existing): Existing REF006 explicitly owns task lifecycle. Prefer owned cancellation/RAII guards and observable completion; do not blindly add catch_unwind to every task.
- `emulebb-rust-prompt_audit_findings_async-lifecycle.md` section 2.2 (existing): Latent API contract improvement under existing lifecycle owner, not a demonstrated user-triggered crash.
- `emulebb-rust-prompt_audit_findings_async-lifecycle.md` section 2.3 (design): Drop cannot await; scheduling abort is expected. No synchronous-drop-join fix.
- `emulebb-rust-prompt_audit_findings_async-lifecycle.md` section 2.4 (existing): Attach caller retry/cancellation proof to existing lifecycle work; unknown means potentially delivered, not automatic retry.
- `emulebb-rust-prompt_audit_findings_async-lifecycle.md` section evidence-gaps (existing): Use existing safety item for Kad task ownership and blocking-job cancellation evidence, without a new broad soak project.
- `emulebb-rust-prompt_audit_findings_code-quality-unsafe.md` section 2.4 (design): Unsafe count and SAFETY comments are not soundness proof; keep proof in existing owners.
- `emulebb-rust-prompt_audit_findings_code-quality-unsafe.md` section 3.3 (existing): Follow-up safety/contract slice under existing owner. Preserve one settings inventory and avoid a second manual mapping.
- `unsafe1.md` section inventory (design): Unsafe counts are not backlog units. Windows/macOS primitives and reference NAT providers remain intentional.
- `unsafe1.md` section MoveFileExW (existing): Duplicate implementation can be reviewed under REF006, but no-replace publication must never inherit replacement flags.
- `unsafe1.md` section route-table (existing): Dedicated zero/multi-row/error/drop tests are meaningful FFI safety evidence; no replacement of windows-sys layouts suggested.
- `unsafe2.md` section correction-1 (design): Pure-Rust alternatives do not establish equal PCP/NAT-PMP/UPnP behavior. Existing providers remain; ABI and leak-free ownership proof belong to existing items.
- `unsafe2.md` section recommendation-1 (existing): Same owner and outcome as unsafe1; do not create duplicate tickets.
- `unsafe2.md` section recommendation-2 (existing): Same owner and outcome as unsafe1; do not create duplicate tickets.
- `LIBPCPNATPMP-CONSUMER-REFACTOR-AUDIT-2026-11-09.md` section native-proof (existing): Adapter work must compose with existing native layout and runtime-safety items. Desktop/musl/Android compile evidence does not alone prove allocator lifecycle correctness; MFC changes require a separate bounded consumer assignment.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section security-native (existing): Native miniupnpc/PCP input hardening belongs to existing runtime-safety and mechanical ABI proof owners. Rust memory safety does not establish the C boundary is safe.

### Scoped Follow-up Acceptance

- [ ] Shutdown observes promotion/callback task completion and restores permits on error, cancellation and panic where supported.
- [ ] Consume handle or document/enforce single-join ownership; test the chosen contract.
- [ ] Cancellation after enqueue cannot produce duplicate retries or false not-sent claims.
- [ ] Observe task completion with deterministic barriers; do not claim cancellation stops already-running blocking I/O.
- [ ] Adding a setting cannot silently reach an untested runtime panic; mapping completeness is mechanically checked.
- [ ] Shared helper, if justified, preserves each caller's replace/no-replace, durability and atomicity contract.
- [ ] Slice lifetime cannot escape table owner; zero/multi-row and error paths preserve alignment and one free.
- [ ] Check C/Rust layouts for the exact target and headers.
- [ ] Prove repeated create/destroy, flow-info release, route rejection and successful mapping.
- [ ] Keep optional platform proof non-gating for Beta 3 and Android signing on hold.
- [ ] Bound native response/input assumptions and prove ownership on failures.
- [ ] Qualify exact C headers/layouts and neutral malformed fixtures.
