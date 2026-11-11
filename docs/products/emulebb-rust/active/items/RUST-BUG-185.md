---
id: RUST-BUG-185
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/310
title: Preserve stopped transfer authority against stale background updates
status: IN_PROGRESS
priority: Major
category: bug
labels: [bug, rust]
milestone: rust-v0.1.0-beta.3
created: 2026-11-11
source: Stopped-transfer regression found during parent-coordinated AICH qualification
---

> Workflow status is tracked in GitHub. This local document owns the durable engineering specification and retained evidence. [Issue #310](https://github.com/emulebb/emulebb-rust/issues/310)

# RUST-BUG-185 - Preserve stopped transfer authority against stale background updates

## Summary

Keep an operator's persisted stopped state authoritative when a detached
download-attempt completion publishes an older queued result. This reliability
fix is a delivery prerequisite for AICH trust work in RUST-BUG-164 / #248.

## Current State

The existing `stopped_transfer_cannot_be_resumed` core test failed during AICH
qualification at `51fdfc084cb8d658ca34b55e77158a6d536599fc`. Source tracing
identified the same affected paths on main
`e40b0eb53932f08cb5775ca8063ed18aeba5f7e8`.

A detached attempt can be queued before stop persists and publishes stopped
state. Its later queued-result publication can replace the cached transfer
state. A subsequent resume trusts that stale cache and clears persisted control
state.

## Representative Sites

- `crates/emulebb-core/src/lib.rs` and `transfer_state_api.rs` own transfer
  publication and operator lifecycle behavior.
- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs` owns the persisted control
  state and existing manifest lock.
- Colocated core and ED2K lifecycle tests retain the deterministic regressions.

## Intended Shape

Preserve explicit stopped authority during background refresh publication.
Reject resume atomically against persisted stopped state under the existing
manifest lock, including when the cached row is stale. Preserve explicit pause,
active creation, completed transfers, and intentional resume behavior.

## Scope Constraints

The parent coordinates the reserved core, ED2K metadata, and colocated lifecycle
test files. Atomic settings shares `lib.rs` through separately reserved wiring.
AICH shares `metadata.rs` and restacks after this prerequisite merges. Beta3
publication and the long soak remain on hold.

## Acceptance Criteria

- [x] Preserve explicit stopped state against stale queued background publication.
- [x] Reject resume against persisted stopped state atomically under the existing
      manifest lock, including a stale cached row.
- [x] Retain explicit pause, active-create, completed-transfer, intentional resume,
      and existing stop/resume coverage.
- [x] Add deterministic regressions for stale queued publication and stale cache.
- [x] Complete the normal exact-source Windows/Linux/Android pre-push gate.
- [ ] Pass hosted exact-head checks and integrate the reviewed fix before AICH.

## Validation

The executed fix source is
`ca9f923be3a9c3690a45ca13996f0784fa161344`. Managed scoped validation passed
473 core unit tests and 35 core integration tests, totaling 508, plus 1,273 ED2K
tests, with zero failures.

The ordinary full pre-push qualification is recorded below
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/local-check/emulebb-rust/20261111T024225Z-b9ce96a1`.
Its full native phase passed in 788.364 seconds, covering policy, Clippy,
diagnostics, WebUI, fresh debug/release/diagnostics builds, and full workspace
tests. Observed-egress VPN validation passed in 52.6 seconds and REST/OpenAPI
validation in 31.6 seconds. Full Linux qualification passed in 5,972.347 seconds,
including both GNU and both musl targets plus image, security, and smoke checks.
Android qualification passed for both native ABIs in 922.866 seconds. The
Android evidence covers its required compilation and ELF scope.

The ordinary push completed successfully at the exact fix source. Managed WSL
teardown confirmed EOF and the workspace lock was released. The worktree was
clean after the push. Hosted checks, review, and integration remain pending.
Retain the hosted exact-head results and merged source when those gates
complete. [PR #311](https://github.com/emulebb/emulebb-rust/pull/311)

## Notes

The parent owns merge order and subsequent AICH restacking. Track AICH trust
acceptance under its existing owner. [RUST-BUG-164](RUST-BUG-164.md) and
[issue #248](https://github.com/emulebb/emulebb-rust/issues/248)
