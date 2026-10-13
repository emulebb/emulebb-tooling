---
id: RUST-FEAT-051
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/94
title: Implement ED2K server user search (OP_SEARCH_USER / OP_USERS_LIST)
status: WONT_DO
priority: Minor
category: feature
labels: [rust, ed2k, server, search, user-search, interoperability]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/94. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-051 - Implement ED2K server user search (OP_SEARCH_USER / OP_USERS_LIST)

## Summary

Disposition record. `OP_SEARCH_USER` (0x1A) and `OP_USERS_LIST` (0x43) appear in
stock eMule and aMule opcode headers, but the current reference review found no
executable request, response decoder, or user-facing feature in either client or
the maintained Rust server reference. No independent product requirement calls
for server-side user discovery.

## Current State

- The Rust server opcode table intentionally contains the implemented file
  search, source, and callback families, not these declaration-only opcodes.
- Stock eMule and aMule declare both numeric values in protocol headers, but
  repository-wide searches found no executable call sites or handlers.
- `repos/ed2k-server` likewise provides no behavior establishing a supported
  user-search exchange.
- User records are a distinct domain and do not belong in the existing file
  search-result model.

## Why This Matters

Implementing a request grammar, result domain, REST API, and WebUI from opcode
declarations alone would create a new product feature rather than close a
demonstrated parity gap. It would also distort the file-search model with user
identity records.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server.rs` - server opcode table
- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs` - server-reply dispatch
- `crates/emulebb-ed2k/src/ed2k_server/search_expr.rs` - query-tree encoding
- `EMULEBB_WORKSPACE_ROOT\analysis\community-0.72\srchybrid\Opcodes.h` - `OP_SEARCH_USER` (0x1A) and `OP_USERS_LIST` (0x43)
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\include\protocol\ed2k\Client2Server\TCP.h` - same opcodes and payload shapes

## Intended Shape

No product change. A future user-discovery feature requires a separate product
case, captured or executable protocol evidence, and a dedicated user-result
domain rather than reuse of file search results.

## Scope Constraints

- Do not infer request or response shapes from opcode names alone.
- Do not add speculative API, OpenAPI, or WebUI surfaces.
- Any later independently justified feature receives a new backlog item.

## Acceptance Criteria

- [x] Reference review distinguishes declarations from executable behavior.
- [x] The file-search result model remains limited to file results.
- [x] The unsupported proposal is closed without speculative wire or API work.

## Validation

- Documentation taxonomy and structure checks.

## Notes

Closed `WONT_DO` on 2026-10-13 after revalidating stock eMule, aMule, and
`ed2k-server`: declarations exist, but no executable behavior or product need
supports the proposed feature.
