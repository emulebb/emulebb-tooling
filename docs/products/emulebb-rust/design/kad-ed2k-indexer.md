# Design: Autonomous Kad/eD2K Indexer

Status: future Indexer-phase design owned by
[`RUST-FEAT-002`](../active/items/RUST-FEAT-002.md). Production implementation
is blocked until the Client gate in [`RELEASE-SCOPE`](../RELEASE-SCOPE.md)
closes. Torznab and qBittorrent compatibility belong to the later Arr phase and
RUST-FEAT-004.

## Goal

Add a persistent searchable corpus of validated remote eD2K/Kad observations to
the existing daemon without creating a second network client, transfer model,
database, or search-result shape.

The Indexer combines passive observations with bounded active discovery. It is
enabled by default when the phase ships, and retained observations persist until
the operator deletes them.

## Network inputs

1. **Passive Kad observations:** validated keyword/source/notes publish and
   search traffic already handled by the participating Kad node.
2. **Live-search observations:** validated results from explicit operator or
   controller eD2K/Kad searches.
3. **Bounded replay:** widely spaced replay of previously observed useful
   keywords under a documented global budget.
4. **Bounded discovery sweeps:** curated, protocol-compliant keyword/extension
   searches under the same global budget.
5. **Optional server enrichment:** results from already connected eD2K servers;
   the index never depends on server availability.

There is no dedicated aggressive source sweep, alternate network identity, or
parallel socket stack. Active work uses the Client domain's existing search and
rate-control services.

## Canonical observations

Every retained observation includes the eD2K hash, size, filename and available
standard metadata, source protocol, observation origin, first/last seen times,
availability evidence, and validation state. Conflicting observations remain
separate inputs to a deterministic presentation summary.

Live, index-only, and hybrid queries use the canonical search/result model in
[`integrated-suite`](integrated-suite.md). Indexing must not require a parallel
Torznab-specific result shape.

## Storage

- Use the product's single SQLite database and schema version.
- Keep Indexer table writes behind an owning service; client and adapters do not
  write those tables directly.
- Use FTS5 projections for normalized keyword search and preserve raw validated
  observation values needed for provenance.
- Do not impose a product TTL, record ceiling, or configured disk quota.
- Do not claim schema parity with unrelated harvesters; share neutral concepts
  only where they remain correct for eD2K/Kad.
- Any incompatible schema change invalidates the entire profile during beta.

## Failure isolation

Low disk or SQLite index-write failure pauses new index writes and active
discovery. Client networking, transfers, uploads, and sharing continue. API,
WebUI, logs, and diagnostic dumps expose a persistent fault until a validated
recovery condition is met. Failed observations are not silently discarded while
active discovery continues.

## Acceptance direction

- Passive observations add no network queries.
- Active replay and discovery obey one documented rate budget with deterministic
  scheduling tests.
- Restart preserves observations and provenance.
- Live, index, and hybrid queries produce one canonical result model.
- Conflicts, malformed metadata, duplicate observations, and stale availability
  remain bounded and attributable.
- Indefinite retention remains operational across large corpora.
- Disk-pressure tests prove Indexer pause without Client interruption.
- Packaged operation passes on Windows, Linux, and macOS x64/ARM64.

Public-network evidence follows the harness/live policy and begins only after
deterministic fixtures establish the traffic budget and failure behavior.
