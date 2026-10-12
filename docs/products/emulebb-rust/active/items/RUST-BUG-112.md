---
id: RUST-BUG-112
workflow: local
title: Advertise offerfiles_v uniformly across ED2K server session types
status: OPEN
priority: Minor
category: bug
labels: [rust, ed2k, server, login, parity, fingerprint]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule
---

# RUST-BUG-112 - Advertise offerfiles_v uniformly across ED2K server session types

## Summary

The long-lived background server session logs in with the configured
`offerfiles_v=1` capability (five login tags by default), while the one-shot
keyword, source, and callback server sessions log in with
`ServerLoginCapabilities::default()` and therefore emit only the stock four
login tags. The same daemon, against the same server, presents two different
login fingerprints depending on which feature opened the session.

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

A non-uniform login shape is an observable fingerprint and makes the extension
behave inconsistently. The extension itself is intentional and stays
(RUST-REF-015), but its advertisement must not flip per call site. One-shot
sessions that publish no offerfiles may legitimately omit the tag, but then
that omission should be a deliberate, documented policy — not an accidental
`Default` at three unrelated call sites.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs` - background login
  capability wiring
- `crates/emulebb-ed2k/src/ed2k_server/active_keyword.rs` - keyword login
- `crates/emulebb-ed2k/src/ed2k_server/active_source.rs` - source login
- `crates/emulebb-ed2k/src/ed2k_server/active_callback.rs` - callback login
- `crates/emulebb-ed2k/src/ed2k_server/startup.rs` - `encode_login_request`,
  `ServerLoginCapabilities`

## Intended Shape

- Decide the single policy for which session types advertise `offerfiles_v=1`,
  and encode that decision in one place rather than per call site.
- Most likely shape: every server session that uses the shared login builder
  advertises the same capability, so the login fingerprint is identical
  regardless of entry point.
- If one-shot sessions intentionally stay four-tag, state that rationale with a
  named helper (not `Default`) so the asymmetry is obvious and tested.

## Scope Constraints

- Keep the extension enabled for the large-library background publish path.
- Do not start one-shot sessions consuming the offerfiles envelope unless that
  is part of the chosen policy; this item is about consistent advertisement,
  not new publishing behavior.

## Acceptance Criteria

- [ ] A single authority decides whether a server login carries the
      `offerfiles_v` tag.
- [ ] Keyword, source, callback, and background sessions produce the same login
      tag-count policy (or an explicitly documented, centrally enforced
      exception).
- [ ] A codec/session test asserts the login tag set per session type.

## Validation

- Existing server-login codec tests
  (`crates/emulebb-ed2k/src/ed2k_server/tests/protocol.rs`) stay green; add an
  assertion covering each session entry point.

## Notes

Depends on the RUST-REF-015 disposition. Related constant consolidation is
tracked by RUST-REF-011.
