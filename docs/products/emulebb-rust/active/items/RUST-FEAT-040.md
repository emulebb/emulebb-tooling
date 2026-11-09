---
id: RUST-FEAT-040
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/29
title: Carry ED2K and Kad search metadata end to end
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, kad, search, metadata, interoperability]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against eMule 0.72a and current aMule 3.1
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/29. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-040 - Carry ED2K and Kad search metadata end to end

## Summary

Preserve standard search metadata from ED2K server and Kad decoders through the
internal model, persistence, and Rust-native API. Rust publishes media metadata
but drops much of the equivalent inbound data; Kad mapping additionally forces
unknown file type, zero rating, and empty AICH. Current aMule also attaches
available notes/ratings to public search results.

## Current State

- Sharing/publishing paths extract and emit media metadata.
- `crates/emulebb-ed2k/src/ed2k_server/result_decoder.rs` retains basic type,
  rating, and AICH data but does not surface standard media tags such as artist,
  album, title, length, bitrate, and codec.
- `crates/emulebb-core/src/search_query.rs` maps Kad results with unknown file
  type, zero rating, and no AICH candidate.
- Notes search exists for known files/passive replay, but it is not reconciled
  into the public search-result model with source/provenance semantics.

## Why This Matters

Metadata is part of practical cross-client search behavior even when it does
not change packet compatibility. Dropping information makes Rust results less
useful than the same result viewed in stock clients and prevents consumers from
making informed choices without starting a download.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_server\result_decoder.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-core\src\search_query.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-kad-dht\src\types.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-core\src\lib.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\amule\src\kademlia\kademlia\Search.cpp`

## Intended Shape

- Define typed optional fields for media artist, album, title, length, bitrate,
  codec, file type, rating/note summary, and AICH candidate.
- Decode the standard server and version-gated Kad tags strictly, preserving raw
  unknown tags where useful without making them public API accidents.
- Carry origin/provenance so server, Kad responder, publisher, and notes sources
  can be reconciled without pretending conflicting observations are identical.
- Persist enough normalized metadata for result replay and indexing.
- Evolve the Rust-native OpenAPI/REST model to the clean canonical search-result
  shape with absence represented explicitly and no MFC API-shape constraint.

## Scope Constraints

- Bound string/tag sizes and reject malformed numeric encodings safely.
- Do not trust a remote rating count as independent local observations.
- RUST-BUG-104 owns AICH consensus/trust; this item owns the end-to-end field
  transport and API surface.
- The beta API and schema may break. Update all owned consumers atomically and
  reject stale API fields or incompatible profiles rather than adding aliases,
  migrations, or fallback reads.

## Acceptance Criteria

- [ ] ED2K server results retain every supported standard media field through
      decoder, internal model, persistence, and API serialization.
- [ ] Kad results retain file type, rating/note metadata, and one provenance-
      bearing AICH candidate when valid for the peer version.
- [ ] Conflicting observations retain provenance and use documented merge rules.
- [ ] Malformed/oversized tags are bounded without losing an otherwise valid
      result.
- [ ] OpenAPI, generated/handwritten clients, embedded WebUI, and the exact
      current persistence schema remain synchronized.
- [ ] A stock/current-aMule fixture produces materially equivalent visible
      metadata for the same server and Kad search results.

## Validation

- Golden packet fixtures covering all supported server/Kad tags, missing tags,
  conflicts, wrong types, malformed values, and size bounds.
- Storage and API round-trip tests against the exact current schema, plus a
  startup failure test for an incompatible prior schema.
- Local stock/current-aMule result comparison and WebUI/API witness.

## Notes

The external API should remain Rust-native. Compatibility here means preserving
standard network semantics, not copying the MFC presentation layer.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_indexer.md` section passive-file-type (existing): Passive indexed rows currently hardcode unknown. Reuse canonical type classification and metadata merge rules, while keeping live search metadata ownership in #29 and autonomous Indexer work behind its phase gate.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A2-search-metadata (existing): Standard media tags, type, note/rating and provenance-bearing AICH metadata already belong to RUST-FEAT-040. Verify which decoders/storage/API fields still drop data rather than create a second metadata project.

### Scoped Follow-up Acceptance

- [ ] Classify available standard metadata or filename-derived types with provenance.
- [ ] Type-filtered queries remain consistent across origins.
- [ ] Do not create a second result model.
- [ ] Bound malformed fields and define cross-origin merge rules.
- [ ] Update decoders, storage, REST and WebUI consistently.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

Priority: Minor
Milestone: post-beta-compatibility

Carry standard media, type, note/rating, and provenance-bearing AICH metadata from ED2K server/Kad decoders through storage and the Rust-native API. Bound malformed data, define merge rules, and keep API consumers/migrations synchronized.
