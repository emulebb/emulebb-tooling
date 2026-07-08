---
id: TMBB-FEAT-004
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/4
title: Rust API alignment - remove legacy capability-negotiation assumptions
status: OPEN
priority: Major
category: feature
labels: [controller, api-v1, rust, compatibility, suite]
milestone: phase-2
created: 2026-06-16
source: API lineage reset 2026-07-08
---

> Workflow status is tracked in GitHub. This local document is retained as an
> engineering spec/evidence record.

# TMBB-FEAT-004 - Rust API alignment

## Summary

Update TrackMuleBB to target the emulebb-rust forward `/api/v1` contract
directly. The first TrackMuleBB beta is a Rust Console UI; it does not need to
drive frozen emulebb-mfc and does not need generic `/capabilities` negotiation.
The beta is accepted as a full Rust console: status, transfers, uploads,
search/download, shared files, servers/Kad, and settings.

## Why This Matters

The old item assumed one shared contract where emulebb-mfc was a subset of Rust.
That direction is retired. TrackMuleBB should now be simpler:
use Rust-native routes and schemas for status, transfers, uploads, search,
shared files, servers/Kad, and settings.

## Intended Shape

- Remove product-agnostic `/capabilities` assumptions from the Rust adapter path.
- Treat the Rust OpenAPI in tooling docs as the adapter contract fixture source.
- Gate the first beta around Rust-only pages and poll-based refresh.
- Leave qBittorrentBB, SABnzbd, installer, and cross-network automation for later
  suite phases.

## Scope Constraints

- No emulebb-mfc adapter or compatibility layer in the first beta.
- No SSE/event-stream requirement for this item; polling is the beta transport.
- Do not make TrackMuleBB a required hop for Rust itself.

## Acceptance Criteria

- [ ] TrackMuleBB Rust adapter tests align with the Rust OpenAPI fixture shape.
- [ ] First-beta UI pages for status, transfers, uploads, search/download,
      shared files, servers/Kad, and settings call Rust-native routes directly.
- [ ] No first-beta code path branches for emulebb-mfc support.
- [ ] Any remaining `/capabilities` usage is either removed or documented as a
      later optional resilience feature, not a product requirement.
