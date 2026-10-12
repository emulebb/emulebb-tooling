---
id: RUST-REF-013
workflow: local
title: Disposition OP_IDCHANGE auxiliary-port field handling
status: DEFERRED
priority: Minor
category: refactor
labels: [rust, ed2k, server, parity, disposition]
milestone: post-beta-polish
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

# RUST-REF-013 - Disposition OP_IDCHANGE auxiliary-port field handling

## Summary

Disposition-only record: the `OP_IDCHANGE` payload's auxiliary-port field
(bytes 8-11) is ignored by the Rust client. This matches stock eMule, which
skips those bytes; aMule reads them as the server port. The Rust choice is the
correct eMule-compatible one and requires no code change.

## Current State

- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs`
  `decode_id_change_payload` parses `client_id[0..4]`, `server_flags[4..8]`,
  and `reported_client_ip[12..16]`, ignoring `[8..12]`.
- Stock eMule reads the same three fields and skips `[8..12]`; aMule treats
  `[8..12]` as an auxiliary/standard port.
- `repos/ed2k-server/src/server/login.rs` (lines 180-192) documents this
  aMule-vs-eMule divergence explicitly.

## Why This Matters

Record the intentional choice so future audits do not re-flag the ignored field
as a decode gap.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs` - `decode_id_change_payload`
- `EMULEBB_WORKSPACE_ROOT\analysis\community-0.72\srchybrid\ServerSocket.cpp` - IDCHANGE parse
- `EMULEBB_WORKSPACE_ROOT\repos\ed2k-server\src\server\login.rs` - IDCHANGE field layout and divergence note

## Intended Shape

No code change. Record the disposition in the ED2K parity evidence and close the
item `WONT_DO`.

## Scope Constraints

- Do not start reading the auxiliary-port field.
- Keep this as provenance, not active work.

## Acceptance Criteria

- [ ] The eMule-compatible disposition is captured in the parity matrix or
      omissions registry.
- [ ] The item is closed `WONT_DO` after capture.

## Notes

Found by the 2026-10-12 ED2K static audit; classified as stock-aligned.
