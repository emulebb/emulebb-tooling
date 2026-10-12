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

`emule_misc_options1()` hardcodes the `no_view_shared_files` bit (bit 2) to `1`
in `CT_EMULE_MISCOPTIONS1`, telling peers we do not permit browsing shared
files. The listener actually serves `OP_ASKSHAREDFILES`, `OP_ASKSHAREDDIRS`,
and `OP_ASKSHAREDFILESDIR`, so the advertised capability is the inverse of the
implemented behavior.

## Current State

- `crates/emulebb-ed2k/src/ed2k_tcp/hello.rs:89` sets
  `let no_view_shared_files = 1u32;` unconditionally; line 102 places it in
  MISCOPTIONS1 bit 2.
- The browse surface is live: `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs:886-895`
  dispatches `OP_ASKSHAREDFILES`, `OP_ASKSHAREDDIRS`, and `OP_ASKSHAREDFILESDIR`
  to the `browse::handle_*` handlers.
- Stock ties the bit to the operator preference:
  `analysis/community-0.72/srchybrid/BaseClient.cpp:974`
  `uNoViewSharedFiles = (thePrefs.CanSeeShares() == vsfaNobody)`, so a default
  stock client that permits viewing advertises bit 0.

## Why This Matters

Advertising "no view shared files" while serving browse discourages peers from
requesting a feature the client does implement and is a small, observable
capability fingerprint divergence. The preview bit remains a separate, approved
omission (`ed2k-preview`); this item is only about the view-shared-files bit.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/hello.rs` - `emule_misc_options1`
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs` - browse dispatch arms
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session/browse.rs` - browse answers
- `analysis/community-0.72/srchybrid/BaseClient.cpp:974` - stock bit source

## Intended Shape

- Derive `no_view_shared_files` from the effective share-visibility policy: `1`
  only when browsing is disabled, `0` otherwise.
- If the headless client has no operator-facing share-visibility toggle yet,
  advertise `0` (viewing allowed) to match the implemented browse handlers, and
  add a setting later without changing the wire default.

## Scope Constraints

- Preview stays `0` per the `ed2k-preview` omission; do not couple this change
  to preview.
- No browse behavior change; only the advertised MISCOPTIONS1 bit changes.

## Acceptance Criteria

- [ ] A default client advertises `no_view_shared_files = 0` when browsing is
      enabled/served.
- [ ] The bit becomes `1` if and only if share browsing is configured off.
- [ ] A hello codec test pins the bit for both settings.

## Validation

- Extend `crates/emulebb-ed2k/src/ed2k_tcp/tests/protocol/hello.rs` with
  MISCOPTIONS1 assertions for browse-enabled and browse-disabled
  configurations.

## Notes

Related capability honesty is recorded in RUST-REF-015 (offerfiles_v) and the
existing `ed2k-preview` omission.

- Fixed in emulebb-rust PR #101 (commit `d93d1172`), rebase-merged to `main`.
