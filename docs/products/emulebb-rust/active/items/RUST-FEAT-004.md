---
id: RUST-FEAT-004
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/4
title: Arr integration — Torznab and qBittorrent compatibility adapters
status: OPEN
priority: Major
category: feature
labels: [arr, torznab, qbittorrent-api, prowlarr, suite]
milestone: post-beta-suite
created: 2026-06-14
source: integrated-suite product direction
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/4. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-004 - Arr integration — Torznab and qBittorrent compatibility adapters

## Summary

Add the integrated suite's Arr-facing protocol adapters after the Indexer gate
closes: Torznab over the persistent observation index, a Prowlarr definition,
and only the qBittorrent Web API subset required by supported
Prowlarr/Sonarr/Radarr workflows.

The adapters run in the bounded-monolith daemon and translate to canonical
search and transfer services. They do not define the core model and do not own
parallel state.

## Current State

- The Client phase owns the unstable first-party `/api/v1` contract and transfer
  lifecycle.
- RUST-FEAT-002 owns the later autonomous Indexer and must close before this
  item's production implementation begins.
- Existing MFC or qBittorrent-shaped APIs are behavioral references only; they
  are not contracts to copy into the Rust core.

## Intended Shape

- Serve native Torznab and qBittorrent-compatible paths from the same listener
  as `/api/v1` with explicit route-family authentication and rate controls.
- Map Torznab queries to canonical Indexer searches and provenance-bearing
  results.
- Map the Arr-required qBittorrent add/list/pause/resume/delete/status behavior
  to canonical Client transfers and categories.
- Ship and validate a Prowlarr definition for the supported Torznab surface.
- Reject unsupported qBittorrent operations explicitly rather than fabricating
  state or success.

## Scope Constraints

- No near-complete qBittorrent emulation goal.
- No adapter-owned transfer, category, credential, search, or index tables.
- No internal media-selection, category-rule, scheduling, post-processing, or
  federation engine; external controllers own those workflows.
- Compatibility requirements apply only to the documented supported Arr paths.
- `/api/v1`, configuration, and schema remain beta-unstable until this gate
  passes; they freeze together afterward.

## Acceptance Criteria

- [ ] The complete Indexer gate is closed before production implementation begins.
- [ ] Torznab returns canonical indexed results with supported caps, categories,
      authentication, pagination, and failure behavior.
- [ ] The Prowlarr definition discovers and queries the adapter successfully.
- [ ] Supported Sonarr/Radarr workflows can search, grab, inspect, pause, resume,
      and remove an eD2K transfer through the Arr-required qBittorrent subset.
- [ ] Unsupported qBittorrent operations fail clearly and never create shadow state.
- [ ] First-party API, WebUI, Torznab, and qBittorrent views converge on the same
      search, transfer, category, and status state.
- [ ] The post-Arr API/config/schema freeze has an explicit compatibility and
      versioning decision backed by conformance tests.

## Validation

- Torznab and qBittorrent contract fixtures for authentication, success,
  unsupported operations, malformed input, pagination, and rate limits.
- Local Prowlarr/Sonarr/Radarr search-to-grab-to-transfer lifecycle.
- State-convergence tests across first-party API, WebUI, and adapters.
- Packaged listener/authentication smoke on Windows, Linux, and macOS x64/ARM64.

## Notes

This is a protocol-adapter phase, not permission to make qBittorrent concepts
the canonical Rust data model.
