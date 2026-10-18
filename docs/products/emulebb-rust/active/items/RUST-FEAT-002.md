---
id: RUST-FEAT-002
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/2
title: Indexer — autonomous Kad/eD2K observation index
status: OPEN
priority: Major
category: feature
labels: [kad, ed2k, indexer, suite]
milestone: post-beta-suite
created: 2026-06-14
source: integrated-suite product direction
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/2. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-002 - Indexer — autonomous Kad/eD2K observation index

## Summary

Add the integrated suite's persistent remote-observation index after the Client
gate closes. The Indexer runs inside the existing bounded-monolith daemon and
single SQLite database, consumes the Client domain's validated traffic and
search services, and exposes live, index, and hybrid results through one
canonical provenance-bearing model.

Full design: [`kad-ed2k-indexer`](../../design/kad-ed2k-indexer.md) and
[`integrated-suite`](../../design/integrated-suite.md).

## Current State

- The current `emulebb-index` crate owns the protocol-required local Kad
  keyword/source/notes index and snoop queue. That Client behavior is not the
  autonomous persistent corpus described here.
- Production Indexer implementation is prohibited until every Client Gate item,
  including newly accepted client work, closes.
- Torznab and qBittorrent compatibility are not part of this item; RUST-FEAT-004
  owns the later Arr phase.

## Intended Shape

- Capture validated passive observations without extra network requests.
- Run replay and curated discovery sweeps under one documented bounded budget.
- Use existing Client identities, sockets, searches, validation, and rate
  controls; do not create a second network client.
- Persist observations indefinitely until explicit operator deletion. Do not
  add a product TTL, record limit, or configured disk quota.
- Retain source, protocol, observation provenance, first/last seen times,
  metadata, availability evidence, and validation state.
- Enable passive capture and bounded active discovery by default when the phase
  ships.
- Pause index writes and active discovery on low disk or SQLite write failure,
  keep normal client networking/transfers operating, and expose a persistent
  fault.

## Scope Constraints

- One daemon, one profile, one database, and one schema version.
- An incompatible Indexer schema change invalidates the entire beta profile;
  there is no partial rebuild or migration path.
- Indexer tables have one owning service. Client and future adapters do not
  write them directly.
- Active discovery remains gentle and bounded even though storage retention is
  intentionally unbounded.
- No Torznab, qBittorrent compatibility, federation, internal media-selection
  rules, scheduling, or post-processing under this item.

## Acceptance Criteria

- [ ] The complete Client gate is closed before production implementation begins.
- [ ] Passive observations add no network queries and retain provenance.
- [ ] Replay and discovery obey a deterministic documented rate budget.
- [ ] Live, index, and hybrid queries share one canonical result model.
- [ ] Restart preserves the persistent corpus and observation provenance.
- [ ] The corpus has no product TTL or configured capacity ceiling and supports
      explicit operator deletion.
- [ ] Low disk and SQLite write failures pause Indexer writes/discovery without
      interrupting normal client transfers or sharing.
- [ ] API, WebUI, logs, and diagnostics expose Indexer state and persistent faults.
- [ ] Packaged lifecycle coverage passes on Windows, Linux, and macOS x64/ARM64.

## Validation

- Unit/property tests for observation normalization, conflicts, deduplication,
  provenance, scheduling budgets, and pause/recovery state.
- Deterministic Kad/eD2K fixtures for passive capture and bounded active work.
- Large-corpus persistence, restart, explicit deletion, low-disk, and SQLite
  failure campaigns.
- Bounded public-network evidence through maintained harness entry points only
  after deterministic traffic-budget proof.

## Notes

RUST-FEAT-004 consumes this domain after the Indexer gate closes. It must not
pull compatibility-specific DTOs or transfer state into the Indexer.
