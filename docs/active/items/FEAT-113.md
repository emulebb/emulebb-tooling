---
id: FEAT-113
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/139
title: Persist peer upload performance history for slot selection
status: OPEN
priority: Minor
category: feature
labels: [uploads, bandwidth, slots, peers, persistence, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-06
source: operator request during live upload-fill monitoring
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/139. This local document is retained as an engineering spec/evidence record.

# FEAT-113 - Persist Peer Upload Performance History For Slot Selection

## Summary

Remember observed peer upload-slot behavior across sessions so eMuleBB can avoid
repeatedly giving scarce upload slots to peers that have historically failed to
consume data, while still preferring fast downloaders when the configured upload
budget is underfilled.

The live broadband monitoring campaign showed that upload fill can collapse
even with 10 active upload slots when several active peers are zero-rate,
no-request, or repeatedly drain local buffers without keeping the network busy.
Current in-session slow-slot recycling helps, but a clean restart loses that
peer-behavior memory and can admit the same poor performers again.

## Intended Shape

- Persist a bounded peer-performance record keyed by stable peer identity where
  available, such as user hash, with conservative fallbacks that avoid unsafe
  identity conflation.
- Track upload-slot productivity over time:
  - accepted upload sessions
  - useful uploaded bytes
  - average and recent upload data rate
  - zero-rate or no-request slot time
  - drained-buffer/no-network-progress episodes
  - disconnects shortly after slot admission
  - last-seen and last-good timestamps
- Use decay so old behavior stops dominating after enough time or enough newer
  good sessions.
- Apply the history as a scheduling hint, not a ban:
  - prefer historically fast, productive peers when upload bandwidth is
    underfilled
  - deprioritize historically poor peers when better eligible candidates exist
  - avoid punishing first-time or sparse-history peers too aggressively
  - let a peer recover after improved behavior
- Expose concise diagnostics so operators can see when peer history influenced
  an upload-slot decision.

## Scope Constraints

- Do not change eD2K or Kad protocol behavior.
- Do not add a new anti-leecher punishment system.
- Do not replace existing bans, credits, friend slots, file priority, or score
  policy; this is a broadband slot-efficiency hint layered below those rules.
- Do not permanently exclude a peer only because of historical low throughput.
- Do not persist unbounded per-peer data; cap record count and age out stale
  entries.
- Do not make IP-only history strong enough to punish NAT/shared-IP clients.
- Do not require UI visibility for collection, decay, or scheduling decisions.

## Candidate Implementation Notes

- Reuse existing known-client or client-credit persistence only if ownership,
  privacy, and compatibility are clear; otherwise add a narrow eMuleBB-owned
  persistence file with versioned records.
- Keep the first policy conservative: apply history only during sustained
  upload underfill and only as a tie-breaker or small score modifier.
- Make the live instrumentation report:
  - count of active peers with poor persisted history
  - count of queued peers skipped or delayed by history
  - count of historically fast peers promoted
  - decay or recovery events
- Coordinate with `FEAT-106` ramp-up policy, `FEAT-107` under-target reason
  diagnostics, and `FEAT-111` peer/queue diagnostics columns.

## Acceptance Criteria

- [ ] Peer upload productivity history survives an app restart.
- [ ] History is bounded by count and/or age and has deterministic cleanup.
- [ ] Historically poor peers are deprioritized only when better eligible
      candidates exist or when upload bandwidth is under target.
- [ ] Historically fast peers can be preferred for upload slots during
      underfilled broadband operation.
- [ ] First-time peers and peers with sparse data are not strongly penalized.
- [ ] Good newer behavior can recover a previously poor peer.
- [ ] Friend slots, bans, file priority, credits, and existing hard upload caps
      remain respected.
- [ ] Upload instrumentation and/or diagnostics explain when persisted peer
      history influenced admission or recycling.

## Validation

- focused unit tests for peer-history scoring, decay, and recovery
- persistence round-trip tests with versioned sample records
- upload-queue tests proving history is only a bounded scheduling hint
- live upload smoke across restart with a mix of fast and poor peers
- x64 Debug and Release app builds before implementation commit
