---
id: RUST-REF-014
workflow: local
title: Disposition ed2k-server capability-constant discrepancy
status: WONT_DO
priority: Minor
category: refactor
labels: [rust, ed2k, reference, parity, disposition]
milestone: post-beta-polish
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

# RUST-REF-014 - Disposition ed2k-server capability-constant discrepancy

## Summary

Disposition-only record: the reference `ed2k-server` repo defines
`SRVFLG_SUPPORTCRYPT = 0x0800` in its shared opcode table, while stock eMule's
server-to-client TCP obfuscation bit is `SRV_TCPFLG_TCPOBFUSCATION = 0x0400`.
Its own login path emits the correct `0x0400` inside `0x05DD`, so the live
server is correct and emulebb-rust is unaffected. No emulebb-rust change is
required.

## Current State

- emulebb-rust uses `SERVER_TCP_FLAG_TCPOBFUSCATION = 0x0400`, matching stock.
- `repos/ed2k-server/src/proto/opcodes.rs` documents `SRVFLG_SUPPORTCRYPT =
  0x0800`, but `repos/ed2k-server/src/server/login.rs` actually builds the
  IDCHANGE flags with the correct `0x0400` inside `0x05DD`.

## Why This Matters

Record the discrepancy so the reference's misleading shared constant is not
treated as authoritative when emulebb-rust capabilities are re-audited.

## Representative Sites

- `repos/ed2k-server/src/proto/opcodes.rs` - `SRVFLG_SUPPORTCRYPT`
- `repos/ed2k-server/src/server/login.rs` - IDCHANGE flag construction
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_server.rs` - `SERVER_TCP_FLAG_TCPOBFUSCATION`

## Intended Shape

No code change. Record the observation in the parity evidence and close the item
`WONT_DO`.

## Scope Constraints

- Do not alter emulebb-rust capability bits.
- Keep this as provenance, not active work.

## Acceptance Criteria

- [x] The discrepancy is captured in the parity matrix.
- [x] The item is closed `WONT_DO` after capture.

## Notes

Found by the 2026-10-12 ED2K static audit; classified as a reference-repo
caveat, not an emulebb-rust defect. Closed `WONT_DO` on 2026-10-13 after the
reference caveat was recorded in current parity evidence.
