---
id: RUST-BUG-166
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/250
title: Admit AICH recovery answers only for matching outstanding requests
status: OPEN
priority: Major
category: bug
labels: [rust, aich, protocol, integrity, io]
milestone: post-beta-compatibility
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/250. This local document owns the durable engineering specification and evidence.

# RUST-BUG-166 - Admit AICH recovery answers only for matching outstanding requests

## Summary and Disposition

Reject unsolicited, stale, or mismatched AICH recovery answers before payload
reads, substantial CPU work, piece-state changes, or corruption attribution.
Use one request authority shared by outbound download and inbound established
sessions. Treat the missing admission boundary as a broader public-release
readiness requirement. The review established source-level defects, not a
measured exploit or evidence that all beta transfers fail.

## Revalidated Findings

On branch `fix/stock-hash-share-tree` at `58595576`, the download
`OP_AICHANSWER` handler decodes the packet, removes an in-flight marker by the
returned part when present, and passes the current download's hash to salvage.
It does not first require an outstanding request or compare the answer's file
hash with the active file. The listener instead takes the packet's file hash
and calls the same salvage helper without outstanding-request correlation.

`begin_part_salvage` checks the master, part range, and whether the piece is
already verified. Any other piece state can proceed. It reads the on-disk part
before validating the proof body against the trusted master, then calculates
block SHA-1 verdicts and updates the bitmap/blackbox. A matching public root in
an unsolicited malformed answer can therefore cause an avoidable part read;
a valid unsolicited proof can reach mutation of a nonverified piece.

MFC `CUpDownClient::ProcessAICHAnswer` first checks `m_fAICHRequested`, then
matches client, requested file, part, and current master before consuming the
proof. The corresponding Rust admission gaps remain on locally available main
`e3372aba`; revalidate current main before implementation.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/download/session.rs`: answer dispatch.
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs`: inbound answers.
- `crates/emulebb-ed2k/src/ed2k_tcp/aich_salvage.rs`: shared handler.
- `crates/emulebb-ed2k/src/ed2k_tcp/codec/aich.rs`: header decoding and exact
  16-byte recovery-unavailable form.
- `crates/emulebb-ed2k/src/ed2k_transfer/salvage.rs`: read, validation,
  attribution, and bitmap mutation order.
- `aich_recovery.rs` and `aich_tree.rs` in that directory: proof geometry.

## Intended Shape

RUST-BUG-167 owns the bounded request lifecycle. Consume answers only against
its live record of peer/session, eD2K hash, file size, part, master, and request/
trust/transfer generation. Matching must precede clearing state. A wrong-file
packet must neither be applied to the active file nor cancel its valid request.
Specify stock-compatible handling of unexpected answers without adding a wire
extension or treating every transient failure as malicious behavior.

Require a current corrupt/recovery-eligible piece and coordinate with its active
writer. Hold a suitable per-file/per-part ordering guard or take a revisioned
snapshot; no delayed recovery result may overwrite newer verified data or
discard newly received blocks. A canceled/retired request or changed trust
generation cannot authorize mutation.

Validate bounded proof framing, counts, identifiers, complete block coverage,
and reconstruction against the trusted master before reading payload bytes.
Reject unknown/out-of-range parts and invalid roots cheaply. Only after these
checks should a bounded storage/CPU job compare local blocks. Avoid a second
read or full-buffer copy solely to cross worker boundaries. RUST-REF-019 owns
CPU offloading and RUST-REF-009 owns storage admission; global core/session
locks must not span these waits.

Publish bitmap changes and corruption-blackbox verdicts only once after the
generation/state recheck. A duplicate answer must not double-debit senders or
reopen a verified piece. A genuine malformed answer leaves the safe normal
redownload fallback available through RUST-BUG-167.

## Acceptance Criteria

- [ ] Unrequested, wrong-peer, wrong-file, wrong-part, wrong-master, stale,
      retired-transfer, and duplicate answers cannot mutate piece state or
      corruption attribution.
- [ ] Instrumented payload readers observe zero reads for answers rejected by
      correlation, geometry, framing, or proof validation.
- [ ] Both listener and download sessions use the same request authority and
      preserve an unrelated valid request when rejecting a mismatched answer.
- [ ] A real solicited stock-compatible proof salvages only the corrupt part's
      good blocks and debits/credits each sender once.
- [ ] Barriers covering concurrent writes, verification, pause/delete, and trust
      changes prove a delayed result cannot overwrite a newer piece revision.
- [ ] Malformed 16/32-bit proof forms, master-overwrite identifiers, missing
      leaves, and large-file boundaries have bounded error paths.
- [ ] CPU/I/O admission and cancellation leave executor heartbeats responsive
      and retain permits until already-running blocking work actually ends.

## Validation and Dependencies

Use synthetic peers and instrumented readers, deterministic worker barriers,
the existing AICH/ICH blackbox suite, and stock/MFC packet goldens under
RUST-CI-031. Assert both state and actual read/attribution counts; checking only
that the connection survives is insufficient. Implement with RUST-BUG-167's
request records and RUST-BUG-164's provenance/generation contract. Preserve
metadata-only outbound proof serving and the standard unavailable response.
