---
id: RUST-BUG-112
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/79
title: Centralize offerfiles_v policy by ED2K server-session role
status: OPEN
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

- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs:120-121` builds
  `ServerLoginCapabilities { offer_files_v1: context.offer_files_capability_enabled }`.
- `crates/emulebb-ed2k/src/ed2k_server/active_keyword.rs:459`,
  `crates/emulebb-ed2k/src/ed2k_server/active_source.rs:213` (also `:230`), and
  `crates/emulebb-ed2k/src/ed2k_server/active_callback.rs:71` call
  `encode_login_request(..., ServerLoginCapabilities::default())`, where the
  derived `Default` leaves `offer_files_v1 = false`.
- Only the background session runs the two-second server-ident negotiation and
  applies a returned `OfferFilesPolicy`; the one-shot sessions never request or
  consume the envelope.

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

- [ ] A single role-aware authority decides whether a server login carries the
      `offerfiles_v` tag.
- [ ] The publishing session advertises the extension; keyword, source, and
      callback sessions emit the stock four-tag login.
- [ ] Tests assert the tag set for every server-session role and prevent a new
      call site from selecting capabilities through `Default`.

## Validation

- Existing server-login codec tests
  (`crates/emulebb-ed2k/src/ed2k_server/tests/protocol.rs`) stay green; add an
  assertion covering each session entry point.

## Notes

Depends on the RUST-REF-015 disposition. Related constant consolidation is
tracked by RUST-REF-011.
