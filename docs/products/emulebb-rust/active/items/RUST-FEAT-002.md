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

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_search.md` section 3.5 (existing): Future live/index/hybrid semantics belong to Indexer owner; identical local and wire normalization is not automatically correct. Closed issue198 explicitly avoids offline-library search.
- `emulebb-rust-prompt_audit_findings_indexer.md` section queue-restart (existing): Snapshot/merge helpers exist without a production persistence/restore call. Track a separately deliverable slice under the existing Indexer owner; do not silently turn default-off Client passive replay into autonomous Indexer production.
- `emulebb-rust-prompt_audit_findings_indexer.md` section write-fault-latch (existing): Current passive writes log and continue; the future Indexer contract requires persistent fault reporting and discovery isolation. This is an unimplemented future-phase acceptance outcome, not a Beta 3 shipped-Indexer defect.
- `emulebb-rust-prompt_audit_findings_indexer.md` section global-replay-budget (existing): Current general/source budgets can sum to 84 queries per 600 seconds, while the future design says one global budget. Choose an explicit combined ceiling or a reviewed documented interpretation.
- `emulebb-rust-prompt_audit_findings_indexer.md` section passive-file-type (existing): Passive indexed rows currently hardcode unknown. Reuse canonical type classification and metadata merge rules, while keeping live search metadata ownership in #29 and autonomous Indexer work behind its phase gate.
- `emulebb-rust-prompt_audit_findings_product_direction.md` section retention-policy (design): The recommendation for a configurable record/disk ceiling directly conflicts with the explicit no-TTL/no-quota product decision. Track a design review, not an automatic implementation or a current runtime defect.
- `emulebb-rust-prompt_audit_findings_product_direction.md` section indexer-data-policy (design): Track data-retention, provenance, operator controls and abuse/moderation questions as a future Indexer design outcome. The report's jurisdictional risk is a question for review, not a proven compliance defect.
- `emulebb-rust-prompt_audit_findings_product_direction.md` section delivery-focus (existing): Existing Client/Indexer/Arr sequencing already owns product focus. Beta increments may ship while the broader Client gate stays open; the user now selects Windows/Linux readiness, with other platform work parallel.

### Scoped Follow-up Acceptance

- [ ] Define query/provenance semantics before Indexer implementation; do not rewrite network folding to match local FTS.
- [ ] Persist bounded SnoopEntry observations in the single SQLite authority.
- [ ] Restore deterministic demand/provenance while keeping transient ReplayFeedback ephemeral.
- [ ] Test restart, duplicate merge and interrupted writes.
- [ ] Disk/SQLite failure stops new Indexer writes and active discovery.
- [ ] Transfers, uploads, sharing and client networking continue.
- [ ] API/WebUI/diagnostics expose the fault; recovery requires a verified write.
- [ ] One authoritative budget contract covers keyword, note and source traffic.
- [ ] A deterministic mixed-family test proves the aggregate bound.
- [ ] Classify available standard metadata or filename-derived types with provenance.
- [ ] Type-filtered queries remain consistent across origins.
- [ ] Do not create a second result model.
- [ ] Compare indefinite retention with disk-pressure isolation, compaction and operator expectations.
- [ ] Record retain/change decision and policy implications.
- [ ] Keep production work behind the Indexer gate.
- [ ] Specify stored fields, retention and deletion/control behavior.
- [ ] Record owner and decisions before Indexer release claims.
- [ ] Candidate review uses the explicitly selected Beta 3 scope and immutable evidence.
- [ ] Later-phase implementation remains behind its gate.
- [ ] Do not treat all optional/design intake as mandatory Beta 3 implementation.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

Part of the post-0.7.3 suite forward program (Phase 0). Workflow state is tracked here; the spec lives in the linked doc.
