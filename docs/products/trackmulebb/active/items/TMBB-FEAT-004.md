---
id: TMBB-FEAT-004
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/4
title: Parked Rust API alignment - remove legacy capability-negotiation assumptions
status: DEFERRED
priority: Major
category: feature
labels: [controller, api-v1, rust, compatibility, suite]
milestone: phase-2
created: 2026-06-16
source: API lineage reset 2026-07-08
---

> Workflow status is tracked in GitHub. This local document is retained as an
> engineering spec/evidence record.

# TMBB-FEAT-004 - Parked Rust API alignment

## Summary

When TrackMuleBB is reactivated, update it to target the emulebb-rust forward
`/api/v1` contract directly. TrackMuleBB is parked future controller work; it
does not drive the current Rust beta, does not link to frozen emulebb-mfc, and
does not need generic `/capabilities` negotiation as a first-order product
requirement.

## Why This Matters

The old item assumed one shared contract where emulebb-mfc was a subset of Rust.
That direction is retired. If TrackMuleBB resumes, it should use Rust-native
routes and schemas for status, transfers, uploads, search, shared files,
servers/Kad, settings, logs, and diagnostics.

## Intended Shape

- Remove product-agnostic `/capabilities` assumptions from the Rust adapter path.
- Treat the Rust OpenAPI in tooling docs as the adapter contract fixture source.
- Keep TrackMuleBB out of the Rust beta gate; if reactivated later, start with
  Rust-only pages and poll-based refresh.
- Leave qBittorrentBB, SABnzbd, installer, and cross-network automation for later
  suite phases.

## Scope Constraints

- No emulebb-mfc adapter or compatibility layer.
- No SSE/event-stream requirement for this item; polling is the initial
  transport if the item is reactivated.
- Do not make TrackMuleBB a required hop for Rust itself.

## Acceptance Criteria

- [ ] TrackMuleBB Rust adapter tests align with the Rust OpenAPI fixture shape.
- [ ] UI pages for status, transfers, uploads, search/download, shared files,
      servers/Kad, settings, logs, and diagnostics call Rust-native routes
      directly when TrackMuleBB is reactivated.
- [ ] No code path branches for emulebb-mfc support.
- [ ] Any remaining `/capabilities` usage is either removed or documented as a
      later optional resilience feature, not a product requirement.
