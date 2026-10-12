---
id: RUST-FEAT-051
workflow: local
title: Implement ED2K server user search (OP_SEARCH_USER / OP_USERS_LIST)
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, server, search, user-search, interoperability]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

# RUST-FEAT-051 - Implement ED2K server user search (OP_SEARCH_USER / OP_USERS_LIST)

## Summary

Add the server-side user-search leg of the ED2K client-to-server TCP protocol:
encode `OP_SEARCH_USER` (0x1A) with a query tree and decode `OP_USERS_LIST`
(0x43) results into the existing search-result pipeline. Stock eMule and aMule
implement this; the Rust client currently has neither opcode, so a server-side
user search cannot be issued and any `OP_USERS_LIST` reply is silently dropped.

## Current State

- The server opcode table in `crates/emulebb-ed2k/src/ed2k_server.rs` (around
  lines 147-181) defines `OP_SEARCHREQUEST` (0x16), `OP_GETSOURCES` (0x19), and
  `OP_CALLBACKREQUEST` (0x1C) but not `OP_SEARCH_USER` (0x1A) or
  `OP_USERS_LIST` (0x43).
- `packet_handler.rs` has no `OP_USERS_LIST` branch; the reply falls into the
  default branch and is logged as an unsupported opcode.
- Query-tree encoding already exists (`ed2k_server/search_expr.rs`,
  `encode_search_request`), so the request-side grammar is available to reuse.

## Why This Matters

User search is part of stock server behavior. Its absence is not a wire
interoperability break (peers and file search are unaffected), but it is an
unintended protocol gap compared with stock eMule and aMule and leaves an
incoming `OP_USERS_LIST` unhandled.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server.rs` - server opcode table
- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs` - server-reply dispatch
- `crates/emulebb-ed2k/src/ed2k_server/search_expr.rs` - query-tree encoding
- `EMULEBB_WORKSPACE_ROOT\analysis\community-0.72\srchybrid\Opcodes.h` - `OP_SEARCH_USER` (0x1A) and `OP_USERS_LIST` (0x43)
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\include\protocol\ed2k\Client2Server\TCP.h` - same opcodes and payload shapes

## Intended Shape

- Add the two opcodes, encode `OP_SEARCH_USER` as a query tree reusing the
  existing search-expression encoder, and decode `OP_USERS_LIST` results
  (`<count 4>(<HASH 16><ID 4><PORT 2><1 Tag_set>)[count]`) into the same
  search-result model as keyword results.
- Expose an additive Rust-native user-search capability following the existing
  keyword-search entry point; keep the OpenAPI, embedded WebUI models, and
  validators synchronized.
- Bound the result count and tag sizes exactly like keyword search results.

## Scope Constraints

- Do not add an MFC-style user-search presentation layer; the Rust-forward
  `/api/v1` contract stays authoritative.
- Unknown or malformed `OP_USERS_LIST` tags must be bounded and must not drop an
  otherwise valid result.
- Preserve stock wire shapes; no new protocol behavior.

## Acceptance Criteria

- [ ] `OP_SEARCH_USER` requests encode a stock-shaped query tree.
- [ ] `OP_USERS_LIST` replies decode into the shared search-result model with
      bounded tags.
- [ ] The Rust-native API, OpenAPI, embedded WebUI, and validators stay
      synchronized.
- [ ] Golden fixtures cover a valid reply, an empty reply, and malformed tags.

## Validation

- Codec unit tests for `OP_SEARCH_USER` request encoding and `OP_USERS_LIST`
  result decoding.
- API/WebUI round-trip tests for the new capability.
- Stock/aMule fixture comparison for the same user-search query.

## Notes

This is a protocol-completeness gap found by the 2026-10-12 ED2K static audit;
it does not block the published beta.
