---
id: RUST-BUG-114
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/81
title: Enforce an explicit maximum upload-slot ceiling and clarify maxUploadSlots semantics
status: DONE
priority: Minor
category: bug
labels: [rust, ed2k, upload, slots, parity, config]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K upload/ban/slot audit 2026-10-12 vs emulebb-mfc
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/81. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-114 - Enforce an explicit maximum upload-slot ceiling and clarify maxUploadSlots semantics

## Summary

The setting formerly named "Maximum upload slots" was consumed as the base
slot target rather than as a cap. Under sustained upload underfill, elastic
expansion could open additional slots above that value, and the upload queue
did not directly enforce the MFC `MAX_UP_CLIENTS_ALLOWED` ceiling of 128.

## Current State

- The upload queue owns an explicit `MAX_UP_CLIENTS_ALLOWED = 128` invariant.
  Both the base slot count and elastic allowance are bounded so no configuration
  or intermediate arithmetic can produce more than 128 active upload slots.
- Default behavior remains a base of 12 slots with an 80% elastic allowance;
  sustained-underfill expansion and slow/idle recycling are unchanged.
- The persisted setting and REST/WebUI contract use `baseUploadSlots` instead
  of the misleading `maxUploadSlots`. Retired persisted and REST keys are
  rejected rather than silently accepted.
- The upload-queue startup contract uses `baseSlots` instead of `activeSlots`.
  Effective-capacity diagnostics retain `activeSlots` because they report the
  actual active/effective count rather than configured base capacity.
- Settings metadata, REST validation, WebUI forms and fixtures, README mapping,
  and the pinned OpenAPI contract all describe the same base-slot semantics.

## Why This Matters

The old label promised a maximum while the value behaved as a floor. That
surprised operators and left the true ceiling as a coincidence of two separate
validation ranges. Making the queue own both bounds matches stock eMule's
safety invariant while preserving eMuleBB's elastic expansion.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/upload_queue.rs` - explicit minimum,
  maximum, elastic allowance, and effective active-slot limit
- `crates/emulebb-settings/src/lib.rs` - `baseUploadSlots` setting metadata and
  retired-key rejection
- `crates/emulebb-rest/src/settings.rs` - REST validation and compatibility
  rejection
- `webui/src` - base-slot contract, form, fixtures, and end-to-end coverage
- `.github/workflows/ci.yml` - pinned OpenAPI contract revision
- `docs/contracts/openapi/emulebb-rest-openapi-v1.yaml` in emulebb-tooling -
  shared REST schema

## Intended Shape

- Keep stock eMule's explicit 128-client ceiling as an upload-queue invariant.
- Expose the configured value truthfully as the base slot target while allowing
  bounded elastic expansion when the server and transfer conditions permit it.
- Reject retired beta-era keys so stale configuration cannot appear to work
  while being ignored.

## Scope Constraints

- Keep the default behavior unchanged (base 12, elastic 80%).
- Preserve the sustained-underfill elastic-open and slow/idle recycle logic.
- Do not couple this to the connection-rate or queue-size settings.

## Acceptance Criteria

- [x] The upload queue enforces an explicit maximum total active-slot count.
- [x] The `maxUploadSlots` setting is renamed to reflect base-slot semantics,
      with docs, OpenAPI, REST, and WebUI updated together.
- [x] Unit tests prove boundary and extreme configurations cannot exceed 128
      active upload slots.

## Validation

- `python tools/rust_quality_gate.py fmt`
- `python tools/rust_quality_gate.py policy` (108 policy tests passed)
- `python tools/rust_quality_gate.py diagnostics`
- `python tools/rust_quality_gate.py clippy`
- `cargo deny check` passed after prerequisite PR #111 updated `rustls` and
  cleared the active RustSec advisories.
- Workspace-orchestrated package suites passed: `emulebb-settings` (19),
  `emulebb-ed2k` (1,049), `emulebb-core` (400 unit tests plus all integration
  suites), and `emulebb-rest` (117 unit and 2 contract tests).
- The full workspace Rust suite and documentation tests passed in Debug
  configuration.
- WebUI validation passed 28 unit tests, 16 Playwright tests, type checking,
  and the production build.
- PR #110 required CI passed on Windows, macOS, and Ubuntu, including CodeQL,
  workflow lint, cargo-deny, policy/format/clippy, and live REST/OpenAPI
  conformance.
- Prerequisite PR #112 replaced timing-sensitive test reranking with the same
  cached offer-catalog ranking used by production; its full cross-platform CI
  passed before PR #110 was rebased and revalidated.

## Notes

Related constant consolidation remains tracked by RUST-REF-011. The existing
minimum bound remains unchanged.

- Completed on 2026-10-15 by emulebb-rust PR #110 in preserved commits
  `1ed364f0`, `fb7dfd10`, and `ffd12424`.
- The shared OpenAPI rename landed in emulebb-tooling PR #14 at `346696cf`.
- Security prerequisite PR #111 landed at `45e9bae6`; deterministic test
  prerequisite PR #112 landed at `3981971a`.
- GitHub issue #81 is closed and the eMuleBB Roadmap item is Done.
