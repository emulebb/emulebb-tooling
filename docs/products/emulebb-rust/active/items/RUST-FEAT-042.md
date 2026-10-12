---
id: RUST-FEAT-042
workflow: local
title: Handle OP_INVALID_LOWID server-UDP notification
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, server, udp, diagnostics]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

# RUST-FEAT-042 - Handle OP_INVALID_LOWID server-UDP notification

## Summary

Recognize and log the server-to-client UDP `OP_INVALID_LOWID` (0x9E) packet
instead of dropping it through the generic unsupported-opcode path. The packet
carries `<ID 4>` and tells a LowID client that the server rejected an operation
because of its ID. Stock eMule handles it; the Rust client currently has no
constant or decode branch for it.

## Current State

- `crates/emulebb-ed2k/src/ed2k_server.rs` defines the server UDP opcode family
  (`OP_GLOBSEARCHREQ3` through `OP_SERVER_LIST_REQ2`) but not
  `OP_INVALID_LOWID` (0x9E).
- The server-UDP receive path logs unsupported opcodes generically, so an
  `OP_INVALID_LOWID` datagram is invisible beyond that generic line.

## Why This Matters

This is diagnostic-only rather than a wire break, but dropping the notification
silently hides a server-visible LowID rejection and makes live troubleshooting
harder than in stock clients.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server.rs` - server UDP opcode table
- `crates/emulebb-ed2k/src/ed2k_server/udp.rs` - server-UDP datagram framing
- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs` - server-UDP receive
  dispatch
- `EMULEBB_WORKSPACE_ROOT\analysis\community-0.72\srchybrid\Opcodes.h` - `OP_INVALID_LOWID` (0x9E)

## Intended Shape

- Add `OP_INVALID_LOWID` (0x9E) and decode its 4-byte little-endian client-ID
  payload.
- Emit a debug/diagnostic record naming the server endpoint and the rejected
  client ID; do not change any other UDP state.

## Scope Constraints

- Diagnostic-only; no retry, reconnect, or policy change on receipt.
- Reuse the existing UDP decode/obfuscation framing unchanged.

## Acceptance Criteria

- [ ] The server-UDP receiver recognizes `OP_INVALID_LOWID`.
- [ ] The 4-byte payload decodes and the rejected client ID appears in
      diagnostics.
- [ ] A unit test covers a plaintext and an obfuscated `OP_INVALID_LOWID`
      datagram.

## Validation

- Codec/dispatch unit tests for the new opcode in both UDP transport modes.

## Notes

Found by the 2026-10-12 ED2K static audit; not a beta blocker.
