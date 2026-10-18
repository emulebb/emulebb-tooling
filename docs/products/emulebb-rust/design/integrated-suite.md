# emulebb-rust Integrated Suite Design

Status: forward design. [`RELEASE-SCOPE`](../RELEASE-SCOPE.md) owns the product
boundary and gates; active backlog items own implementation and evidence.

## Product shape

The product is one automation-first bounded monolith delivered in three ordered
phases: Client, Indexer, and Arr. It remains one daemon, one profile, one SQLite
database, one embedded operations console, and one HTTP listener. The bounded-
monolith rule is about ownership inside that process: each domain owns its
models and writes, and other domains use explicit internal services rather than
reaching through tables or mutable runtime state.

The current production phase is Client. This document describes future domain
boundaries so current client work does not make the later phases require a
second transfer model, a second search model, or a compatibility-shaped core.
It does not authorize Indexer or Arr production implementation before their
gates open.

## Domain ownership

### Client

The Client domain owns:

- eD2K and Kad sessions, identity, capabilities, routing, and protocol state;
- live searches and their remote observations;
- transfers, sources, upload queue, categories, friends, and bans;
- shared roots, known/shared files, delivery, verification, and seeding;
- settings, diagnostics, logs, NAT, VPN guard, and application lifecycle; and
- the protocol-required local Kad keyword/source/notes index.

The Client domain does not own autonomous discovery policy, Arr workflows,
content selection, scheduling, media management, or post-processing.

### Indexer

The future Indexer domain owns persistent remote observations, active-discovery
budgets, FTS projection, index health, and operator deletion. It consumes
validated observations and invokes existing Client search services. It must
not open an independent Kad/eD2K identity, socket stack, or transfer engine.

Indexer records are durable product data, not a cache. They persist until
explicit operator deletion. There is no product TTL, record ceiling, or disk
quota. Active discovery remains bounded even though retained storage does not.

### Compatibility adapters

The future Arr domain owns protocol translation only:

- Torznab maps canonical indexed search/results into the supported feed shape.
- The qBittorrent adapter maps the Arr-required Web API subset into canonical
  transfer and category services.
- Prowlarr definitions describe those adapter surfaces.

Adapters do not own searches, results, transfers, categories, index rows, or
credentials used by another route family. Unsupported qBittorrent operations
fail explicitly instead of fabricating success.

## Canonical data flow

The long-term first-party model uses one search resource with three execution
modes:

- `live` performs eD2K/Kad network work and records validated observations;
- `index` queries only persisted Indexer observations; and
- `hybrid` returns persisted matches while live work enriches the same result
  set.

A canonical result is identified by eD2K hash and size and retains individual
observations rather than flattening conflicts prematurely. Each observation
records origin, protocol, responder or publisher context where safe, first and
last seen timestamps, availability evidence, metadata, and validation state.
Merge logic produces a presentation summary without destroying provenance.

Downloading a result always creates the canonical Client transfer. The WebUI,
first-party API, Torznab grab flow, and qBittorrent adapter all converge on that
operation. No adapter-specific transfer row or shadow lifecycle is permitted.

## API target

`/api/v1` remains the first-party beta namespace. It evolves toward durable
domains for system/settings, networks, searches/results, transfers, library/
sharing, and index operations. Imperative network actions may remain explicit
operations where a state-only representation would hide failure or lifecycle.

The route namespace and DTOs may break during all three phases. A break updates
daemon handlers, OpenAPI, conformance checks, the embedded WebUI, examples, and
owned adapters in one work slice. Compatibility aliases for prior beta shapes
are forbidden.

Torznab and qBittorrent-compatible routes use their native paths on the same
listener. Route-family authentication and rate controls remain explicit. The
listener is LAN-reachable by default and never treats LAN location as
authentication.

The contract freezes only after the Arr gate. At that point, `/api/v1`, config,
and the durable schema acquire coordinated compatibility obligations.

## Persistence target

All domains use one SQLite database and one schema version. Tables still have
one owning domain; cross-domain reads and writes go through owner services or
purpose-built projections.

Before the post-Arr freeze, an incompatible schema invalidates the entire
profile. Startup fails and requires a fresh profile. Product code never
migrates, repairs, resets, partially rebuilds, or silently preserves one domain
from an incompatible database. This includes index-only incompatibilities.

When index writes fail because of low disk or SQLite errors:

1. stop new index writes;
2. stop active discovery that would create more observations;
3. preserve normal Client networking, transfers, uploads, and sharing;
4. expose a persistent fault through API, WebUI, logs, and diagnostics; and
5. resume only after a deliberate, validated recovery condition.

Dropping observations silently while discovery continues is not acceptable.

## Configuration target

Configuration is opinionated by default. Operator-facing settings cover
identity, paths, authentication, listener exposure, routing, sharing, enabled
networks, transfer limits, and Indexer/adapter enablement. Low-level tuning
belongs in a clearly marked advanced section and requires a demonstrated use
case; protocol timing and adaptive control internals are not settings merely
because MFC exposed them.

When the Indexer phase ships, passive capture and bounded active discovery are
enabled by default. The settings surface explains their network and persistent-
storage effects but does not add a storage cap or TTL.

## WebUI target

The embedded SPA is an operations console for one long-lived daemon. It covers
health, faults, settings, networks, searches, transfers, uploads, sharing,
index status, adapter status, logs, and diagnostics. It does not reproduce a
desktop window model or own automation rules.

## Gate rules

- Client production work has priority until every active client item, including
  newly accepted items, closes or is explicitly removed from the product.
- Indexer production work starts only after the complete Client evidence and
  platform gate passes.
- Arr production work starts only after the Indexer behavior, persistence,
  provenance, disk-pressure, and packaging gate passes.
- API, config, and schema freeze only after the Arr gate.

Design exploration must not create dormant production modules, settings, route
aliases, or schema placeholders before the owning phase opens.
