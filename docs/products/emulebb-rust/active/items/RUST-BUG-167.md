---
id: RUST-BUG-167
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/251
title: Release and retry failed AICH recovery requests across eligible peers
status: OPEN
priority: Minor
category: bug
labels: [rust, aich, recovery, scheduling, protocol]
milestone: post-beta-compatibility
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/251. This local document owns the durable engineering specification and evidence.

# RUST-BUG-167 - Release and retry failed AICH recovery requests across eligible peers

## Summary and Disposition

Consume RUST-BUG-166's bounded request authority and add alternate-source retry
after unavailable, invalid, silent, or disconnected
peers. Preserve ordinary whole-part redownload when recovery cannot help.
This is tolerable temporarily in controlled beta use, but wastes bandwidth and
disk I/O and remains part of the Client gate.

## Revalidated Findings

On branch `fix/stock-hash-share-tree` at `58595576`,
`pump_aich_recovery_requests` drains a session-local pending vector and may send
requests for several parts to one peer. The wire failure form contains only a
16-byte file hash, without a part number. The answer handler removes an
in-flight marker only when `answer.part` exists, leaving failures marked pending
for that session. There is no dedicated request deadline or immediate
alternate-source retry; reconnect initialization can rediscover corrupt pieces,
but is not a complete request lifecycle.

Duplicate suppression is per session, so different peers can independently
request recovery for the same transfer part. Pending entries that lack a root,
capable peer, or advertised part are drained rather than retained as bounded
transfer-owned demand. Peer part availability is checked, but this pump does
not require an advertised peer root matching the requested master.

The latest responder deliberately returns recovery-unavailable when its two
reconstruction slots are busy or duplicate work is already running. Such an
answer is an expected overload outcome, not proof that the file never has
recovery metadata. MFC's `ClientAICHRequestFailed` releases request ownership
and asks the file to choose another capable matching-root source.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/download/aich_request.rs`: queue draining,
  availability checks, request writes, and in-flight bookkeeping.
- `download/session/state.rs` and `download/session.rs` in that TCP module:
  startup corruption queue, answers, teardown, and A4AF reuse.
- `ed2k_transfer/aich_answer_cache.rs`: busy/duplicate unavailable outcomes.
- `ed2k_transfer/metadata.rs`: trusted identity and recovery serving.
- Stock/MFC `SHAHashSet.cpp::ClientAICHRequestFailed`,
  `PartFile.cpp::RequestAICHRecovery`, and `DownloadClient.cpp::SendAICHRequest`.

## Intended Shape

RUST-BUG-166 owns the minimum bounded request record, generation/deadline,
answer correlation, and cancellation authority for Beta 3. Reuse that owner
across inbound/outbound sessions; do not create a parallel request registry.
This item adds a transfer-owned bounded demand set, alternate-source selection,
retry/backoff fairness, and resumable scheduling above that authority.

Select a source with current AICH capability, a matching advertised master,
usable reachability, and required part availability according to stock rules.
Revalidate stock source-selection preferences; do not introduce a new packet
or require extra connection churn just for local scheduling convenience.
Coalesce duplicate demand from multiple download sessions.

Success, unavailable, invalid proof, timeout, send failure, and disconnect each
finish or release ownership exactly once. Retry another eligible source with
bounded backoff and per-peer cooldown. Prevent a busy responder from causing a
tight loop, starvation of another corrupt part, or permanent session-local
suppression. Preserve pending demand until it is satisfied, obsolete, or given
an explicit bounded fallback disposition. Define what is reconstructed after
restart without requiring persistence of live sockets/deadlines.

Pause, cancellation, delete, A4AF switch, completion, and trusted-root changes
invalidate old generations. Do not let a late answer clear a replacement
request. Recovery must not stall normal download indefinitely or ban a peer
merely for returning the standard unavailable packet. Consult validated local
proofs under RUST-REF-020 before making another network request.

## Acceptance Criteria

- [ ] At most one request per peer and one request per transfer part is active,
      including simultaneous demand from multiple sessions.
- [ ] The bare 16-byte failure releases the correct owner and schedules another
      eligible source or bounded fallback; no stale in-flight marker remains.
- [ ] Timeout, disconnect, invalid proof, and failed send release state and
      permits exactly once and cannot trigger a retry storm.
- [ ] Busy Rust responders eventually succeed when capacity returns, or normal
      whole-part redownload proceeds without waiting indefinitely.
- [ ] Unsupported/mismatching/unavailable sources are skipped without losing
      transfer-owned demand that can become serviceable later.
- [ ] Pause/delete/A4AF/root-change/late-answer races cannot consume replacement
      requests or reopen completed pieces.
- [ ] Queue depths, attempts, cooldowns, and fairness remain bounded and
      observable; unavailability alone does not affect corruption bans.

## Validation and Dependencies

Use paused-time state-machine tests and synthetic peer sessions for success,
unavailable-then-success, silence, malformed answers, disconnect, and retries
across multiple capable sources. Include two simultaneous corrupt parts and
duplicate sessions. Exercise responder saturation deterministically rather than
starting a real-media load. RUST-BUG-166 owns admission, RUST-BUG-164 owns root
trust, RUST-REF-020 owns proof reuse, and RUST-FEAT-065 owns diagnostic exposure.

## Beta 3 Boundary

The minimum request record and invalidation semantics are delivered under
RUST-BUG-166. This item's broader recovery retry, cooldown, and fair
alternate-peer scheduling remain parallel non-gating work for Beta 3.
Existing safety behavior and whole-part redownload remain mandatory.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_aich-trust.md` section 2 / 4 network-authoritative assertion (existing): Current store_aich_hashset still assigns the acquired root. Saved complete issue bodies distinguish consistency from trusted provenance and define verification/request defects. Reuse those owners; do not treat persistence as automatic authority. Their current disposition is broader public-release readiness, not a newly demonstrated Beta 3 exploit.

### Scoped Follow-up Acceptance

- [ ] Implement provenance before enforcing AICH disagreement.
- [ ] Coordinate answer admission and bounded request lifecycle with the same generations.
- [ ] Preserve mandatory MD4 completion and imported/operator authority.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

**Reviewable branch spec:** https://github.com/emulebb/emulebb-tooling/blob/fix/stock-hash-share-tree/docs/products/emulebb-rust/active/items/RUST-BUG-167.md
