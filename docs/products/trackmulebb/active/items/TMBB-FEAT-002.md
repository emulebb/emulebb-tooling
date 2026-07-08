---
id: TMBB-FEAT-002
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/2
title: Suite automation: cross-network grab + reconcile/orphan actuation
status: OPEN
priority: Major
category: feature
labels: [controller, automation, suite, reconciliation]
milestone: phase-2
created: 2026-06-15
source: SUITE-JOINT-ROADMAP Decision 2026-06-15; design ref AMUT-FEAT-002
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-002 - Suite automation: cross-network grab + reconcile/orphan actuation

## Summary

The suite-specific automation no single client or the generic Arr stack can
express: cross-network grab decisions (eD2K collection vs BT torrent for the same
content), dedup via v2 file-roots across networks, and acting on the Python
fabric's reconcile/orphan reports. Generic, REST-expressible rules stay external
(qBittorrentBB native rules, Sonarr/Radarr/Prowlarr). Design origin:
`amutorrent/docs/SUITE-AUTOMATION.md`.

## Why This Matters

Only the controller sees both indexes, both download clients, and the metadata
fabric. Reconcile/orphan reports are report-only by design — TrackMuleBB is their
natural actuator.

## Intended Shape

- Read reconcile/orphan reports; optionally promote `orphan→harvest-matched` data
  to the live library and start seeding; flag mixed-content directories.
- Given a rule match or intent, choose network + client and dispatch the grab.
- Trigger the qBittorrentBB branded export and (later) the BEP-46 library publish.

## Scope Constraints

- Own only the cross-network / eD2K-aware / metadata-fabric delta; do not reinvent
  the Arr stack. Whether TrackMuleBB ever owns *all* generic rules is **parked**.
- Additive layer — clients + Prowlarr stay standalone.

## Acceptance Criteria

- [ ] Reconcile/orphan reports drive at least one actuation (e.g. adopt + seed).
- [ ] A cross-network grab decision routes to the correct client.
- [ ] No required-hop dependency introduced.

## Notes

- Depends on the metadata fabric reports and the branded export (`QBBB-FEAT-001`).
