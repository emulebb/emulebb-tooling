---
id: RUST-REF-012
workflow: local
title: Disposition OP_DISCONNECT server-session parity note
status: WONT_DO
priority: Minor
category: refactor
labels: [rust, ed2k, server, parity, disposition]
milestone: post-beta-polish
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

# RUST-REF-012 - Disposition OP_DISCONNECT server-session parity note

## Summary

Disposition-only record: the Rust client never sends `OP_DISCONNECT` (0x18) on a
clean server disconnect. This matches stock eMule and aMule practice - aMule
marks the opcode "not verified" and neither implementation actually emits it -
so no code change is required.

## Current State

- The Rust server opcode table has no `OP_DISCONNECT` (0x18) and never sends it.
- Stock eMule lists the opcode but does not send it on a clean disconnect;
  aMule lists it with a "not verified" note.
- `repos/ed2k-server/src/proto/opcodes.rs` lists it client-to-server for
  completeness only.

## Why This Matters

Preserve the audit conclusion so a future parity re-audit does not re-flag a
non-gap as a defect.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\include\protocol\ed2k\Client2Server\TCP.h` - `OP_DISCONNECT = 0x18` ("not verified")
- `EMULEBB_WORKSPACE_ROOT\repos\ed2k-server\src\proto\opcodes.rs` - `OP_DISCONNECT` listed client-to-server

## Intended Shape

No code change. Record the disposition in the ED2K parity evidence so the
observation is treated as stock-aligned, then close the item `WONT_DO`.

## Scope Constraints

- Do not add an `OP_DISCONNECT` send path.
- Keep this as provenance, not active work.

## Acceptance Criteria

- [x] The disposition is captured in the parity matrix.
- [x] The item is closed `WONT_DO` after capture.

## Notes

Found by the 2026-10-12 ED2K static audit; classified as parity, not a defect.
Closed `WONT_DO` on 2026-10-13 after the stock-aligned no-send disposition was
recorded in current parity evidence.
