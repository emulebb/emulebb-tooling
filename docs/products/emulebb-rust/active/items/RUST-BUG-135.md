---
id: RUST-BUG-135
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/161
title: Return errors for Kad wire-count overflow
status: OPEN
priority: Minor
category: bug
labels: [rust, kad, protocol, serialization, panic-safety, api]
milestone: post-beta-polish
created: 2026-10-23
source: 2026-10-23 Rust best-practices and safety audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/161. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-135 - Return errors for Kad wire-count overflow

## Summary

Make every Kad encoder reject collections that exceed the stock protocol's
`u8` or `u16` count fields through `ProtoError` instead of panicking inside a
public `KadPacket::encode() -> Result` API.

## Current State

Kad packet writers convert result, contact, entry, and tag collection lengths
with `try_from(...).expect(...)`. The public packet structs expose ordinary
vectors and the public encoder promises a fallible result, but a caller can
construct an oversized value that aborts the operation through panic rather
than returning an error. The same pattern exists in custom writers and binrw
`#[bw(calc = ...)]` fields.

## Why This Matters

Wire-width constraints are protocol validation, not process invariants. Keeping
them in panic paths makes internal refactors, future indexer result sources, and
library use less robust. Silent truncation is not acceptable either because it
would diverge from stock framing and corrupt packet boundaries.

## Representative Sites

- `crates/emulebb-kad-proto/src/packet.rs` `KadPacket::encode`.
- `crates/emulebb-kad-proto/src/packet/codec.rs` search and publish writers.
- `crates/emulebb-kad-proto/src/packet/types.rs` binrw count fields.
- `crates/emulebb-kad-proto/src/error.rs` `ProtoError`.

## Intended Shape

- Add a typed wire-count overflow error containing the field, maximum, and
  actual count, or introduce bounded protocol collection types that fail at
  construction.
- Validate every count before writing any bytes so failure cannot return a
  partially encoded packet.
- Replace binrw `expect` calculations with genuinely fallible writes or a
  prevalidated representation.
- Keep the stock `u8`/`u16` field widths and reject oversized data without
  truncation, paging ambiguity, or a proprietary extension.

## Scope Constraints

- Stock/community eMule remains authoritative for packet layout and count
  widths.
- Response paging and UDP size policy remain separate from count-width
  validation; both constraints must hold.
- API breakage is acceptable during beta if bounded construction gives a
  clearer long-term model.
- Do not hide an overflow by dropping tags, contacts, entries, or results.

## Acceptance Criteria

- [ ] No Kad packet encoder uses `expect`, unchecked narrowing, or truncation
      for a wire count derived from a collection length.
- [ ] Every count overflow returns a typed `ProtoError` before any packet bytes
      are exposed to the transport.
- [ ] Maximum valid `u8` and `u16` counts encode successfully with stock framing.
- [ ] One-over-maximum counts fail deterministically for every affected packet
      family.
- [ ] DHT response paging continues to honor the UDP datagram ceiling as an
      independent constraint.

## Validation

- Boundary tests at maximum and maximum-plus-one for each count width and
  packet family.
- Property tests asserting `encode` never panics for constructible public packet
  values.
- Existing stock packet fixtures, Kad interoperability tests, and response-size
  tests.
