---
id: FEAT-092
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/82
title: Add layered peer behavior guard for client quarantine and IP-ban escalation
status: OPEN
priority: Minor
category: feature
labels: [anti-leecher, quarantine, banning, peer-behavior, diagnostics, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-26
source: operator live-log review after OP_OutOfPartReqs loop suppression testing
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/82. This local document is retained as an engineering spec/evidence record.

# FEAT-092 - Add Layered Peer Behavior Guard For Client Quarantine And IP-Ban Escalation

## Summary

Design and implement a conservative peer behavior guard that separates three
different response levels:

- log and score suspicious but inconclusive events
- cool down or quarantine one logical `CUpDownClient`
- temporarily IP-ban only when behavior is clearly IP-level abuse

The immediate trigger for this item was live testing of a peer that repeatedly
accepted upload slots and then immediately replied with `OP_OutOfPartReqs`.
The narrow `OP_OutOfPartReqs` loop guard handled that peer correctly: it
cooled the client down after three zero-payload loops in 30 seconds, suppressed
the next accept, and avoided a broad IP ban. This item generalizes that
strategy without turning normal P2P churn into false bans.

## Current Behavior

eMuleBB currently has two separate protection styles:

- The classic eMule ban list is an in-memory, two-hour, IP-keyed ban cache.
  It is appropriate for proven IP-level abuse, but it is intentionally blunt.
- The new `OP_OutOfPartReqs` guard is per `CUpDownClient`, session-local, and
  blocks expensive download restarts only after a repeated loop pattern.

Current automatic classic ban paths include:

- userhash changed for a tracked IP/port
- aggressive same-file request behavior
- `FileReq flood`
- `QR flood`
- `Identified as Spammer`
- CorruptionBlackBox identifying more than `32%` corrupt data
- TCP error flooding, default enabled at 10 events in 60 minutes
- manual UI or REST bans

The current `OP_OutOfPartReqs` guard:

- records inbound `OP_OutOfPartReqs` only while the client is downloading
- starts a two-minute cooldown after three events in 30 seconds
- suppresses `OP_AcceptUploadReq` during cooldown and sends `OP_CancelTransfer`
- escalates to client quarantine after 10 pressure events in five minutes
- does not write to the classic IP ban list
- does not persist across restart

## Evidence From Live Logs

The live run on 2026-05-26 showed why a layered model is needed.

High-confidence client-level loop:

- `92.186.216.159 'axgujo [ePlus]'`
- three zero-second, zero-byte `OP_OutOfPartReqs` download ends at `21:33:22`
- cooldown and accept suppression logged
- no broad IP ban needed

Suspicious but not safe to IP-ban:

- `OP_OutOfPartReqs` one-offs after useful payload transfer, such as hundreds
  of MB from one peer
- wrong-header disconnects after substantial payload, including hundreds of MB
  and more than 1 GB from some peers
- scattered `10053` disconnects across many different clients
- upload timeouts with one occurrence per client
- two unknown UDP protocol packets from one IP

These events should produce diagnostics and possibly client-local scores, but
they are not by themselves strong enough for the classic IP ban list.

## Design Goal

Create a small, explainable behavior guard with explicit event classification,
decay windows, and staged responses. The guard should protect the running app
from wasteful or abusive peers while preserving stock network compatibility
and avoiding punishment for normal unstable peer behavior.

## Proposed Architecture

Introduce two ledgers with different authority:

### `ClientBehaviorState`

Owned by or attached to `CUpDownClient`.

Use for behavior tied to one logical client/session:

- repeated `OP_OutOfPartReqs` accept/start/stop loops
- repeated `OP_AcceptUploadReq` without useful download payload progress
- repeated zero-payload download sessions
- repeated wrong-header disconnects from the same client when payload is near
  zero
- repeated timeouts after slots are granted but no useful data arrives
- queue or downloading-list churn that repeatedly spends scheduler work
  without useful transfer

Allowed responses:

- log only
- add decaying behavior score
- short cooldown
- session-local client quarantine

Client quarantine should block expensive transitions such as `StartDownload()`
or repeated accept handling. It should not automatically add the IP to the
classic ban list.

### `IpBehaviorState`

Owned by `CClientList` or an adjacent helper.

Use only for behavior that is safe to attribute to the IP itself:

- pre-handshake TCP garbage or bad headers before any valid client identity
- repeated accepted incoming sockets from the same IP that fail before useful
  identity or first valid packet
- repeated malformed protocol packets from the same IP in a short window
- repeated unknown UDP protocol packets from the same IP
- repeated invalid file requests across client objects from the same IP
- identity churn from the same IP/port that appears to evade tracking
- confirmed corrupt-data sender evidence

Allowed responses:

- log only
- add decaying IP score
- temporary IP ban through the existing `m_bannedList`

IP bans should remain limited to high-confidence abuse because many peers can
appear behind NAT, LowID forwarding, relays, or shared infrastructure.

## Event Model

Each behavior event should carry enough context for a safe decision:

- event type
- peer IP and port when known
- logical client pointer or stable client identity when known
- user hash availability and whether identity was established
- socket phase, especially pre-handshake versus established client
- download/upload state at the failure
- bytes transferred and useful payload bytes
- requested file hash when relevant
- whether the peer is LowID, server-mediated, callback-mediated, or otherwise
  not safely attributable to the visible IP
- reason string used for logs and UI diagnostics
- recent count and window

Rules should be data-driven enough to make later tuning possible, but the first
slice should stay simple and compile-time conservative.

## Classification Policy

### IP-Ban Worth

Use the classic two-hour IP ban only for high-confidence IP-level abuse:

- CorruptionBlackBox proves the IP is a corrupt-data sender over the existing
  threshold.
- TCP pre-handshake garbage repeats from the same IP.
- Wrong headers or malformed packets repeat before useful payload and before a
  stable client identity exists.
- Unknown UDP protocol packets repeat from the same IP beyond a conservative
  threshold.
- Invalid file requests repeat across client objects from the same IP.
- Same IP/port repeatedly changes userhash or identity in an evasion-like
  pattern.

### Client-Quarantine Worth

Use `CUpDownClient` quarantine for expensive but client-local behavior:

- repeated zero-payload `OP_OutOfPartReqs` accept/start/stop loops
- repeated accepted upload slots that immediately return no useful data
- repeated wrong-header disconnects from the same client with near-zero payload
- repeated timeouts from the same client after granted download slots
- repeated queue/downloading-list churn from the same client without useful
  bytes

### Log Or Score Only

Do not punish immediately:

- one `OP_OutOfPartReqs` after useful transfer
- one wrong header after useful transfer
- one `10053` disconnect
- one upload timeout
- normal remote close
- occasional unknown UDP protocol packets
- any LowID or relay-mediated case where the visible IP is not safely
  attributable

These should be visible in logs and diagnostics so operators can decide
whether a pattern is emerging.

## Scope Constraints

- Do not import all of CShield behavior from `FEAT-011` in this item.
- Do not add broad hard bans for ordinary disconnects, `10053`, or wrong
  headers after useful payload.
- Do not persist quarantine state in the first implementation.
- Do not change eD2K/Kad protocol semantics or emit non-stock protocol
  messages.
- Do not silently downgrade existing classic ban behavior.
- Do not punish LowID, callback, server-mediated, or NAT-shared peers by IP
  unless the abuse signal is clearly IP-level.
- Keep every enforcement action loggable with an explicit reason and count.

## Candidate Implementation Plan

1. Extract the existing `OP_OutOfPartReqs` loop counters into a small
   `ClientBehaviorState` helper while preserving behavior.
2. Add an event enum and shared score-window utilities for client-local
   behavior.
3. Extend client-local scoring with log-only counters for wrong header,
   zero-payload timeout, and zero-payload session churn.
4. Add cooldown/quarantine thresholds only for repeated near-zero-payload
   behavior.
5. Add an `IpBehaviorState` map in `CClientList` for identity-less or
   pre-handshake abuse.
6. Feed repeated unknown UDP protocol and pre-handshake TCP error events into
   IP scoring, with log-only mode first.
7. Promote only high-confidence repeated IP-level abuse to the existing
   two-hour IP ban list.
8. Expose summary counters in verbose logs, and later in UI/REST diagnostics if
   useful.

## Acceptance Criteria

- [ ] Existing `OP_OutOfPartReqs` cooldown and quarantine behavior is preserved.
- [ ] Client-local and IP-level behavior accounting are separate in code and
      logs.
- [ ] Wrong-header after useful payload is not enough to ban or quarantine.
- [ ] Repeated zero-payload wrong-header behavior can cool down or quarantine a
      logical client.
- [ ] Repeated pre-handshake malformed traffic can escalate to the IP ban list.
- [ ] `10053`, normal close, single timeout, and single unknown UDP packet
      remain log-only or score-only by default.
- [ ] Every cooldown, quarantine, and IP ban logs event type, count, time
      window, peer identity, and reason.
- [ ] LowID or relay-mediated peers are not IP-banned from weak attribution.
- [ ] Focused tests cover score decay, client quarantine thresholds, IP-ban
      thresholds, useful-payload exemptions, and LowID attribution guards.

## Validation

- `python -m emule_workspace validate`
- focused native tests for `ClientBehaviorState` and `IpBehaviorState`
- focused source-level tests for expected log strings and threshold constants
- live-log replay or synthetic log analyzer coverage for:
  - `OP_OutOfPartReqs` loop suppression
  - one-off useful-payload wrong header
  - repeated zero-payload wrong header
  - repeated pre-handshake TCP error
  - repeated unknown UDP protocol from the same IP
- x64 Debug and Release app builds before implementation commit
