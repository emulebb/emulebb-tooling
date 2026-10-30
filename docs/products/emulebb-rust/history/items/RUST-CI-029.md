---
id: RUST-CI-029
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/160
title: Test packet diagnostics without unsafe environment mutation
status: DONE
priority: Major
category: ci
labels: [rust, tests, safety, environment, diagnostics, concurrency, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-23
source: 2026-10-23 Rust best-practices and safety audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/160. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-029 - Test packet diagnostics without unsafe environment mutation

## Summary

Remove process-environment mutation from the packet-diagnostics unit test and
make dump-path behavior testable through an injected path/provider or an
isolated subprocess whose environment is fixed before threads start.

## Current State

The packet-diagnostics regression in
`crates/emulebb-ed2k/src/ed2k_tcp/dump.rs` uses Rust 2024 unsafe calls to remove
and set `EMULEBB_RUST_LOG_DIR`. Its safety comment establishes only that the
test expects to own the dump writer's first access. It does not prove exclusive
process-wide environment access while Cargo may execute tests and native code
on other threads. The test also does not restore a pre-existing variable value.

## Why This Matters

Rust marks environment mutation unsafe because some platforms and foreign
libraries cannot safely tolerate concurrent reads and writes. A test suite must
not rely on undocumented runner serialization or carry an unsatisfied unsafe
precondition merely to exercise configuration refresh behavior.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/dump.rs`
  `dump_recovers_when_log_dir_appears_after_first_access`.
- Packet-diagnostics dump path resolution and writer initialization.
- Feature-enabled parallel Cargo test lanes.

## Intended Shape

- Extract dump destination lookup behind a small injectable provider or state
  object and test changing availability without changing the process
  environment.
- If exact environment startup behavior needs proof, run a dedicated child
  process with the desired environment established before its runtime creates
  threads.
- Keep production environment lookup lazy/retryable if that behavior remains
  required by the diagnostics harness.
- Do not treat a test-local mutex as proof against arbitrary environment access
  from other Rust tests or linked native libraries.

## Scope Constraints

- Preserve the regression guarantee that an early unavailable log directory
  does not permanently disable later packet dumps.
- Do not serialize the entire Rust test suite as a workaround.
- Do not add another mutable process-global test hook.
- Persisted live diagnostics behavior remains owned by the build-tests harness;
  this item changes only code seams and deterministic proof.

## Acceptance Criteria

- [x] No in-process Rust test calls unsafe `std::env::set_var` or
      `std::env::remove_var` after the test runtime may be multithreaded.
- [x] The early-miss/late-success dump regression remains deterministic and
      restores all injected state through ordinary ownership.
- [x] Any subprocess-based environment test sets its environment before child
      execution and does not mutate the parent environment.
- [x] Packet-diagnostics tests pass under default parallel execution and when
      repeatedly filtered or reordered.
- [x] Production dump lookup remains retryable after an initially unavailable
      destination.

## Validation

- Parallel and repeated feature-enabled unit tests for packet diagnostics.
- A deterministic early-miss/late-success test through the injected seam.
- Existing persisted diagnostics harness validation without ad-hoc launch
  logic.

## Resolution

- Replaced process-environment mutation with injected diagnostics configuration and retryable dump ownership.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-diagnostics`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`
