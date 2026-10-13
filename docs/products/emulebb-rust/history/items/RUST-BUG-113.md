---
id: RUST-BUG-113
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/80
title: Advertise share-viewing capability truthfully in CT_EMULE_MISCOPTIONS1
status: DONE
priority: Minor
category: bug
labels: [rust, ed2k, hello, capability, parity, browse]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/80. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-113 - Advertise share-viewing capability truthfully in CT_EMULE_MISCOPTIONS1

## Summary

`emule_misc_options1()` currently advertises `no_view_shared_files = 0`, telling
peers that the actual shared catalog can be browsed. The listener intentionally
returns an empty file list and denies directory browsing, so the capability bit
is the inverse of the implemented privacy policy.

## Current State

- `crates/emulebb-ed2k/src/ed2k_tcp/hello.rs` sets
  `no_view_shared_files = 0` in MISCOPTIONS1 bit 2.
- `listener/session/browse.rs` returns an empty catalog for
  `OP_ASKSHAREDFILES` and denies `OP_ASKSHAREDDIRS` plus
  `OP_ASKSHAREDFILESDIR`.
- Existing listener tests already prove the empty/denied behavior, while hello
  tests and the full hello golden pin the incorrect advertised bit.
- Stock ties the bit to the operator preference:
  `analysis/community-0.72/srchybrid/BaseClient.cpp:974`
  `uNoViewSharedFiles = (thePrefs.CanSeeShares() == vsfaNobody)`, so a default
  client that denies viewing advertises bit 1.

## Why This Matters

Advertising browse permission while returning no shared content is a false
capability contract and an observable privacy-policy mismatch. The preview bit
remains a separate approved omission (`ed2k-preview`).

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/hello.rs` - `emule_misc_options1`
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs` - browse dispatch arms
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session/browse.rs` - browse answers
- `analysis/community-0.72/srchybrid/BaseClient.cpp:974` - stock bit source

## Intended Shape

- Advertise `no_view_shared_files = 1` for the current non-browsable product
  policy.
- Keep hello encoding and browse request handling driven by one policy when a
  future feature exposes the real shared catalog.
- Do not add a fake configuration state before browse-enabled behavior exists.

## Scope Constraints

- Preview stays `0` per the `ed2k-preview` omission; do not couple this change
  to preview.
- No browse behavior or configuration change; only restore the truthful
  advertised MISCOPTIONS1 bit and its goldens.

## Acceptance Criteria

- [x] The current non-browsable client advertises `no_view_shared_files = 1`.
- [x] Hello encoding and the existing empty/denied browse responses express the
      same policy.
- [x] Hello bit and full-wire golden tests pin the truthful current profile.

## Validation

- Update `crates/emulebb-ed2k/src/ed2k_tcp/tests/protocol/hello.rs` direct bit
  assertion and full hello-answer golden; retain existing listener deny tests.

## Notes

Related capability honesty is recorded in RUST-REF-015 (offerfiles_v) and the
existing `ed2k-preview` omission.

- PR #101 (commit `d93d1172`) inverted the bit based on an incorrect assumption
  that dispatching browse opcodes exposed the real catalog. The 2026-10-13
  closure audit verified the handlers remain intentionally empty/denied and
  reopened the item.
- Completed on 2026-10-13 in emulebb-rust commit `3f3bb819`. The 25 hello tests,
  the listener browse-policy test, formatting, and targeted all-target Clippy
  pass.
