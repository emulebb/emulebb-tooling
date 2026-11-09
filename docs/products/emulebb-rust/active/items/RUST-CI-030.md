---
id: RUST-CI-030
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/163
title: Verify Rust FFI layouts against vendored C headers
status: OPEN
priority: Major
category: ci
labels: [rust, ffi, abi, safety, portability, native-dependencies]
milestone: post-beta-polish
created: 2026-10-23
source: 2026-10-23 Rust best-practices and safety audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/163. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-030 - Verify Rust FFI layouts against vendored C headers

## Summary

Generate or mechanically verify the MiniUPnPc and libpcpnatpmp Rust FFI layouts
against the exact vendored C headers for every supported target so ABI drift
fails at build or test time instead of reaching unsafe pointer interpretation.

## Current State

`emulebb-miniupnpc-sys` and `emulebb-pcpnatpmp-sys` hand-maintain `#[repr(C)]`
types for native structures. The PCP surface includes target-dependent socket
layouts, `in6_addr` alignment, a C enum, and `time_t` fields. Their build scripts
compile the vendored native sources but do not generate bindings or compare Rust
size, alignment, and field offsets with the C compiler's view.

The safe wrappers then dereference native pointers and construct slices using
those Rust layouts. A vendored-header update or newly admitted target can
therefore turn unnoticed ABI drift into undefined behavior.

## Why This Matters

Documentation on an unsafe block cannot prove a foreign layout. The proof must
come from the same headers, preprocessor defines, compiler, and target ABI used
to build the linked library. Cross-platform support expands the combinations
that need a mechanical fail-closed gate.

## Representative Sites

- `crates/emulebb-pcpnatpmp-sys/src/lib.rs` socket and flow-info layouts.
- `crates/emulebb-pcpnatpmp-sys/build.rs` native compilation.
- `crates/emulebb-miniupnpc-sys/src/lib.rs` URL, device, and IGD layouts.
- `crates/emulebb-miniupnpc-sys/build.rs` native compilation.
- Safe wrapper calls that dereference or slice native-returned storage.

## Intended Shape

- Prefer generated bindings from the pinned vendored headers when generation is
  reproducible and does not impose an uncontrolled developer dependency.
- Otherwise compile a small C ABI probe and compare `sizeof`, `_Alignof`, and
  required field offsets with Rust values for every shared structure.
- Prove enum widths, `time_t`, address-family fields, and target-specific socket
  alignment explicitly.
- Make an unverified target fail closed rather than guessing a layout with cfg
  branches.
- Keep unsafe operations concentrated in sys/safe-wrapper boundaries and forbid
  new unsafe code in crates that do not need it.

## Scope Constraints

- The vendored headers and build defines used for the native library are the ABI
  authority; do not validate against an unrelated system installation.
- Generated output, if checked in, must have a deterministic refresh and review
  process tied to dependency updates.
- Do not broaden the supported target matrix merely because a probe compiles.
- Preserve MiniUPnPc and PCP/NAT-PMP behavior while changing the binding proof.

## Acceptance Criteria

- [ ] Every C struct read or written by Rust has a generated or mechanically
      verified size, alignment, and required field-offset contract.
- [ ] C enum representation, `time_t`, socket-family layout, and `in6_addr`
      alignment are verified on every supported target.
- [ ] Updating either vendored header fails CI when Rust bindings or ABI
      expectations are stale.
- [ ] Unsupported or unverified targets fail with an actionable build error
      instead of compiling guessed layouts.
- [ ] Safe wrappers expose no raw native pointer lifetime beyond the smallest
      audited ownership boundary.
- [ ] Crates without a justified unsafe boundary forbid unsafe code.

## Validation

- Native ABI probes on every supported operating-system and architecture lane.
- Deliberate mismatch tests proving size, alignment, and offset drift fails.
- Existing MiniUPnPc, PCP/NAT-PMP, NAT orchestration, and package builds.
- Dependency-update documentation covering binding/probe regeneration.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_reachability.md` section 2.4 / 4.2-3 (existing): ABI verification and native-target compile/runtime proof belong to existing FFI and platform items. Android is parallel and non-gating for Beta 3; do not replace proven C libraries with a narrower pure-Rust fallback to avoid qualification.
- `emulebb-rust-prompt_audit_findings_code-quality-unsafe.md` section 2.3 (existing): Use exact native-header ABI proof; zero is valid for current C aggregates. A bool field by itself does not make zero invalid.
- `emulebb-rust-prompt_audit_findings_code-quality-unsafe.md` section 2.4 (design): Unsafe count and SAFETY comments are not soundness proof; keep proof in existing owners.
- `emulebb-rust-prompt_audit_findings_code-quality-unsafe.md` section evidence-gaps (existing): Closed lint/suppression work does not establish C ABI layout compatibility.
- `unsafe1.md` section inventory (design): Unsafe counts are not backlog units. Windows/macOS primitives and reference NAT providers remain intentional.
- `unsafe2.md` section correction-1 (design): Pure-Rust alternatives do not establish equal PCP/NAT-PMP/UPnP behavior. Existing providers remain; ABI and leak-free ownership proof belong to existing items.
- `LIBPCPNATPMP-CONSUMER-REFACTOR-AUDIT-2026-11-09.md` section native-proof (existing): Adapter work must compose with existing native layout and runtime-safety items. Desktop/musl/Android compile evidence does not alone prove allocator lifecycle correctness; MFC changes require a separate bounded consumer assignment.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section security-native (existing): Native miniupnpc/PCP input hardening belongs to existing runtime-safety and mechanical ABI proof owners. Rust memory safety does not establish the C boundary is safe.

### Scoped Follow-up Acceptance

- [ ] Mechanical C/Rust layout proof uses exact vendored headers.
- [ ] Keep musl and Android compile proof distinct from runtime/device NAT proof.
- [ ] Header/layout drift fails mechanically and initialized foreign storage remains ownership-safe.
- [ ] Windows/Linux candidate ABIs have exact-header layout evidence; other platforms remain non-gating beta follow-up.
- [ ] Check C/Rust layouts for the exact target and headers.
- [ ] Prove repeated create/destroy, flow-info release, route rejection and successful mapping.
- [ ] Keep optional platform proof non-gating for Beta 3 and Android signing on hold.
- [ ] Bound native response/input assumptions and prove ownership on failures.
- [ ] Qualify exact C headers/layouts and neutral malformed fixtures.
