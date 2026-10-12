---
id: RUST-REF-011
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/99
title: Consolidate duplicated ED2K opcode and capability constants
status: OPEN
priority: Minor
category: refactor
labels: [rust, ed2k, protocol, constants, maintainability]
milestone: post-beta-polish
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/99. This local document is retained as the durable engineering spec and evidence record.

# RUST-REF-011 - Consolidate duplicated ED2K opcode and capability constants

## Summary

Move the ED2K opcode, server TCP/UDP flag, and client capability constants into
one tested authority so the client-to-server and server-to-client directions
cannot drift. Today `SRVCAP_*` (login capability bits) and `SERVER_TCP_FLAG_*`
or `SERVER_UDP_FLAG_*` (server-advertised bits) live beside the opcode tables
in `ed2k_server.rs`, with a second opcode block in `ed2k_tcp.rs`, and nothing
asserts the values against stock.

## Current State

- `crates/emulebb-ed2k/src/ed2k_server.rs` lines 288-310 define `SRVCAP_*` and
  `SERVER_TCP_FLAG_*` / `SERVER_UDP_FLAG_*`.
- `crates/emulebb-ed2k/src/ed2k_tcp.rs` carries a separate peer-protocol opcode
  block (around lines 158-231).
- The reference `repos/ed2k-server/src/proto/opcodes.rs` documents this exact
  duplication as its own historical source of a wrong crypt-capability bit.

## Why This Matters

Two spellings of the same wire constants invite silent drift. A wrong
capability bit is exactly the class of bug that passes review because the
shared table is never exercised.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server.rs` - opcode and flag constants
- `crates/emulebb-ed2k/src/ed2k_tcp.rs` - peer-protocol opcode constants
- `repos/ed2k-server/src/proto/opcodes.rs` - reference precedent and drift warning

## Intended Shape

- Introduce a single canonical opcode/flag module (or reuse one crate-level
  authority) that both the server and peer paths reference.
- Add value-asserting tests for every capability and flag bit against the stock
  eMule values documented in the reference.
- Keep duplicate-name opcodes that share a numeric value but differ by protocol
  byte grouped under explicit protocol enums so the 0x60/0x61 collisions are
  obvious, matching how aMule names them.

## Scope Constraints

- No wire-behavior change; this is a pure consolidation.
- Preserve existing public items and only change internal references.

## Acceptance Criteria

- [ ] One canonical source owns each opcode and flag value.
- [ ] Tests assert the stock bit values and the client-vs-server asymmetry.
- [ ] Server and peer paths compile against the consolidated authority with no
      behavior change.

## Validation

- Existing unit and codec tests stay green; added constant-value tests pass.

## Notes

Found by the 2026-10-12 ED2K static audit. Related disposition:
RUST-REF-014 records a discrepancy in the reference server's shared table.
