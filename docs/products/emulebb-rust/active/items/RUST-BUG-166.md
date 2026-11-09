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
milestone: rust-v0.1.0-beta.3
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/250. This local document owns the durable engineering specification and evidence.

# RUST-BUG-166 - Admit AICH recovery answers only for matching outstanding requests

## Summary and Disposition

Reject unsolicited, stale, or mismatched AICH recovery answers before payload
reads, substantial CPU work, piece-state changes, or corruption attribution.
Use one request authority shared by outbound download and inbound established
sessions. Treat the missing admission boundary as a Windows/Linux Beta 3 integrity
requirement. The review established source-level defects, not a
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

This item owns the minimum bounded request authority needed for Beta 3:
one live record per transfer part and at most one recovery request per peer,
including peer/session, eD2K hash, file size, part, master, request/trust/transfer
generation, and deadline. Consume answers only against that record. Matching
must precede clearing state. A wrong-file
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
reopen a verified piece. A genuine malformed answer leaves the existing safe normal redownload fallback
available. Broader alternate-peer retry and scheduling remain RUST-BUG-167 work.

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
that the connection survives is insufficient. Implement the minimum request records here with RUST-BUG-164's
provenance/generation contract. RUST-BUG-167 consumes that shared authority;
its broader retry/backoff implementation is not a hidden Beta 3 prerequisite. Preserve
metadata-only outbound proof serving and the standard unavailable response.

## Minimum Request Authority Acceptance

- [ ] One bounded owner per transfer part and at most one live request per peer
      make the part-less failure response unambiguous.
- [ ] Dispatch, completion, failure, deadline, disconnect, pause, cancellation,
      delete, A4AF switch, and root/trust changes release or invalidate the
      correct generation without consuming a replacement request.
- [ ] Listener and download sessions consult the same authority before
      clearing state, reading payload, validating expensive proofs, or
      updating corruption attribution.
- [ ] Existing whole-part redownload remains available. Alternate-peer
      selection, retry fairness, and adaptive backoff do not gate this slice.

## Beta 3 Windows/Linux Placement

Promoted to the Windows/Linux Beta 3 correctness gate on 2026-11-09. Unsolicited or stale recovery answers must not cause payload work or mutate transfer state before matching a live request authority.

Qualify the affected behavior on Windows and Linux, using deterministic
faults and synthetic filesystem/protocol inputs. Other-platform qualification,
including macOS/APFS variants, continues in parallel and does not block
Beta 3. This changes release placement; it does not claim a measured exploit
or routine corruption, and it does not authorize publication.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_aich-trust.md` section 2 / 4 network-authoritative assertion (existing): Current store_aich_hashset still assigns the acquired root. Saved complete issue bodies distinguish consistency from trusted provenance and define verification/request defects. Reuse those owners; do not treat persistence as automatic authority. Their current disposition is broader public-release readiness, not a newly demonstrated Beta 3 exploit.
- `emulebb-rust-prompt_audit_findings_aich-trust.md` section 6.1,6.3 / 7.3 (existing): Existing tests cover one vote per subnet; hand-derived mask boundaries and large-file/cross-client proof remain evidence extensions, owned by current AICH and canonical protocol items.
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section aich-regressions (existing): Trailing recovery bytes and equal-weight trust tie behavior should be reconciled with existing AICH admission/provenance/reuse items and the separate AICH audit.

### Scoped Follow-up Acceptance

- [ ] Implement provenance before enforcing AICH disagreement.
- [ ] Coordinate answer admission and bounded request lifecycle with the same generations.
- [ ] Preserve mandatory MD4 completion and imported/operator authority.
- [ ] Use independent /20 byte-order fixtures and 16/32-bit proof boundaries.
- [ ] Avoid duplicate evidence tickets or duplicating payload reads.
- [ ] Reject noncanonical recovery framing under the owning admission contract.
- [ ] Equal input evidence yields a deterministic trust result.
- [ ] Tests preserve request matching and trusted-root authority.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

**Reviewable branch spec:** https://github.com/emulebb/emulebb-tooling/blob/fix/stock-hash-share-tree/docs/products/emulebb-rust/active/items/RUST-BUG-166.md
