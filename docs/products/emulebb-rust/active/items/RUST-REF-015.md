---
id: RUST-REF-015
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/100
title: Track the non-stock offerfiles_v server-login extension
status: OPEN
priority: Minor
category: refactor
labels: [rust, ed2k, server, protocol-extension, login, parity]
milestone: post-beta-polish
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/100. This local document is retained as the durable engineering spec and evidence record.

# RUST-REF-015 - Track the non-stock offerfiles_v server-login extension

## Summary

Disposition record. The Rust client appends a named `offerfiles_v=1` u32 tag to
its `OP_LOGINREQUEST` (a fifth tag where stock eMule sends four) and, when a
server answers with the matching capability envelope in `OP_SERVERIDENT`,
switches large-library `OP_OFFERFILES` publishing to the negotiated batch and
minimum-interval policy. Stock eMule and aMule never send the login tag. The
operator confirmed on 2026-10-12 that this is an intentional, tracked
extension; this item is the durable disposition so future parity audits treat
it as a known divergence instead of re-flagging it as an unintended gap.

## Current State

Client login (`crates/emulebb-ed2k/src/ed2k_server/startup.rs`
`encode_login_request`):

- The stock four-tag login is `CT_NAME` (string), `CT_VERSION` (u32 = `0x3C`),
  `CT_SERVER_FLAGS` (u32 `SRVCAP_*`), `CT_EMULE_VERSION` (u32).
- When `ServerLoginCapabilities.offer_files_v1` is true, the tag count becomes
  5 and a named `TAGTYPE_UINT32` tag `offerfiles_v=1`
  (`OFFER_FILES_CAPABILITY_VERSION`) is appended.
- `offer_files_capability_enabled` defaults to `true` in
  `crates/emulebb-ed2k/src/config.rs:288` and
  `crates/emulebb-settings/src/lib.rs:958`.

Server negotiation (`crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs`
`decode_server_ident_details`):

- On `OP_SERVERIDENT`, the client parses the standard `ST_SOFTFILES` /
  `ST_HARDFILES` tags plus three named text tags `offerfiles_v`,
  `offerfiles_batch_max`, and `offerfiles_min_interval_ms`.
- The five values are validated through
  `OfferFilesPolicy::validate` (`offer_policy.rs`) and surfaced as
  `OfferFilesCapabilityAdvertisement::{Absent, Invalid, Supported}`.

Pacing fallback (`crates/emulebb-ed2k/src/ed2k_server/session.rs`
`begin_offer_files_publishing`):

- With v1 enabled but no server envelope yet, the session waits
  `OFFER_FILES_NEGOTIATION_WAIT` (2 s) for the first `OP_SERVERIDENT`.
- Without an envelope it falls back to legacy pacing
  (`OFFER_FILES_LEGACY_MIN_INTERVAL` = 60 s, local batch max 200) using the
  standard `ST_SOFTFILES` / `ST_HARDFILES` limits.
- Stock servers ignore the unknown login tag, so against them the negotiation
  is a no-op and standard pacing is preserved.

## Why This Matters

The extra login tag is both a wire fingerprint and a protocol extension. It is
deliberate: it lets a matching server bound the per-advertisement batch size and
minimum interval so a 100k-file shared library can be published incrementally
instead of in one oversized `OP_OFFERFILES` burst. Recording the decision here
satisfies the workspace rule that protocol changes carry explicit justification
and tracking, and prevents repeated re-audit churn.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server/startup.rs` - `encode_login_request`,
  `encode_offer_files_payload*`
- `crates/emulebb-ed2k/src/ed2k_server/offer_policy.rs` -
  `OFFER_FILES_CAPABILITY_VERSION`, `OfferFilesPolicy::validate`
- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs` -
  `decode_server_ident_details`
- `crates/emulebb-ed2k/src/ed2k_server/session.rs` -
  `begin_offer_files_publishing`, `observe_offer_files_capability`,
  `offer_files_batch_limit`
- `crates/emulebb-ed2k/src/config.rs` and `crates/emulebb-settings/src/lib.rs` -
  default-on setting
- `analysis/community-0.72/srchybrid/ServerConnect.cpp` - stock four-tag login
- `analysis/amule/src/ServerConnect.cpp` - aMule four-tag login

## Intended Shape

- Keep the extension enabled by default as the large-library publish mechanism.
- Treat it as a known, tracked divergence in parity evidence; a future ED2K
  re-audit must not report it as an unintended gap.
- If a machine-readable "tracked extension" registry is ever added beside
  `policy/rust-client-omissions.toml`, move this disposition there.
- Keep the advertisement uniform across every server session type (see
  RUST-BUG-112).

## Scope Constraints

- No wire-behavior removal: the `offerfiles_v` login tag stays.
- Do not weaken the negotiated batch/min-interval safety envelope;
  `OfferFilesPolicy::validate` remains authoritative.
- This is a provenance/tracking record, not a call for new code.

## Acceptance Criteria

- [ ] The extension is recorded in the parity matrix or equivalent evidence as
      intentional and tracked.
- [ ] A future ED2K parity re-audit treats `offerfiles_v` as a known divergence
      rather than a new defect.
- [ ] The justification (bounded incremental large-library publishing) is
      captured in this record.

## Validation

- Docs-only record: `python scripts\docs-item-taxonomy-check.py` and
  `python scripts\docs-structure-check.py` stay green.

## Notes

Complements RUST-BUG-112 (uniform advertisement across session types).
RUST-CI-005 owns the negotiated offerfiles capability proof. The duplicated
opcode/capability constants are in scope for the RUST-REF-011 consolidation.
