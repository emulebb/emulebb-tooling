---
id: RUST-BUG-112
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/79
title: Centralize offerfiles_v policy by ED2K server-session role
status: DONE
priority: Minor
category: bug
labels: [rust, ed2k, server, login, parity, fingerprint]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/79. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-112 - Centralize offerfiles_v policy by ED2K server-session role

## Summary

The long-lived publishing session logs in with the configured
`offerfiles_v=1` capability, while one-shot keyword, source, and callback
sessions emit the stock four-tag login through an incidental `Default` value.
The wire difference is appropriate because only the background session can
publish files, but that policy must be centralized and named rather than
emerging independently at each call site.

## Current State

- `crates/emulebb-ed2k/src/ed2k_server/startup.rs` owns an explicit
  `ServerSessionRole` for publishing, keyword-search, source-search, and
  callback sessions; login encoding derives its tag set from that role.
- The publishing role carries the configured `offer_files_v1_enabled` value,
  which defaults on, and the background driver uses the same value for login
  advertisement and capability-envelope negotiation.
- Keyword-search, source-search, and callback roles explicitly emit the stock
  four-tag login and cannot accidentally advertise publishing capability
  through a defaultable capability struct.
- An exhaustive codec test locks the tag count and `offerfiles_v` presence for
  every role, including explicitly disabled publishing.

## Why This Matters

The extension itself is intentional and stays (RUST-REF-015), but capability
advertisement must describe actual session behavior. Advertising a publishing
extension from sessions that never publish is misleading; omitting it via
three unrelated defaults is fragile. A single role-aware policy should make
both outcomes explicit and testable.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs` - background login
  capability wiring
- `crates/emulebb-ed2k/src/ed2k_server/active_keyword.rs` - keyword login
- `crates/emulebb-ed2k/src/ed2k_server/active_source.rs` - source login
- `crates/emulebb-ed2k/src/ed2k_server/active_callback.rs` - callback login
- `crates/emulebb-ed2k/src/ed2k_server/startup.rs` - `encode_login_request`,
  `ServerLoginCapabilities`

## Intended Shape

- Define explicit server-session roles in the shared login construction path.
- Advertise `offerfiles_v=1` only for a publishing session that can consume the
  returned pacing envelope and send `OP_OFFERFILES`.
- Keep keyword, source, and callback sessions on the stock four-tag login and
  make that non-publishing policy impossible to express through an incidental
  derived default.

## Scope Constraints

- Keep the extension enabled for the large-library background publish path.
- Do not make one-shot sessions consume an envelope or publish files.
- Do not optimize for identical fingerprints at the cost of truthful
  capability advertisement.

## Acceptance Criteria

- [x] A single role-aware authority decides whether a server login carries the
      `offerfiles_v` tag.
- [x] The publishing session advertises the extension; keyword, source, and
      callback sessions emit the stock four-tag login.
- [x] Tests assert the tag set for every server-session role and prevent a new
      call site from selecting capabilities through `Default`.

## Validation

- `python tools/rust_quality_gate.py fmt`
- `python tools/rust_quality_gate.py policy` (108 policy tests passed)
- `python tools/rust_quality_gate.py diagnostics`
- `python tools/rust_quality_gate.py clippy`
- Workspace-orchestrated `emulebb-ed2k` tests (1,049 passed) and
  `emulebb-core` unit/integration tests (400 unit tests plus all integration
  suites) passed in Debug configuration.
- PR #108 required CI passed on Windows, macOS, and Ubuntu; live REST/OpenAPI
  conformance and required CodeQL passed. Its first two Ubuntu attempts exposed
  an unrelated concurrent-reload race in `native_path_shared_dir`; test-only
  PR #109 serialized that setup and passed all required gates before #108 was
  rebased and revalidated.

## Notes

Depends on the RUST-REF-015 disposition. Related constant consolidation is
tracked by RUST-REF-011.

- Completed on 2026-10-14 by emulebb-rust PR #108 in preserved commits
  `a823bc6b` and `4fcd5c10`.
- GitHub issue #79 is closed and the eMuleBB Roadmap item is Done.
