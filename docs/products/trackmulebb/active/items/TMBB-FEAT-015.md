---
id: TMBB-FEAT-015
workflow: github
github_issue: TBD - file on emulebb/trackmulebb when scheduled
title: Long-term cross-network analytics - GeoIP (country/city/ASN) over a DuckDB store
status: OPEN
priority: Major
category: feature
labels: [controller, analytics, geoip, duckdb, observability]
milestone: phase-2
created: 2026-06-17
source: dashboard design discussion (2026-06-17); reuse eMuleBB IP2Country MMDB
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-015 - Long-term cross-network analytics (GeoIP over DuckDB)

## Summary

Persist long-term, cross-network transfer analytics in TrackMuleBB: per-country /
per-city / per-IP-range (and optionally per-ASN) peer and volume statistics over
time, for **both** emulebb-rust (eD2K) and qBittorrentBB (BT) in one place. The
controller samples each client's existing peer/source REST endpoints, enriches IPs
via GeoIP, rolls them up into a time-series store, and renders dashboards.

## Why This Matters

Analytics is the one place where a cross-network vantage point is essential -
"transfers by country across eD2K + BT combined" is exactly the cross-network
delta TrackMuleBB is meant to own. Putting it in the controller avoids implementing
analytics twice (Rust core under RC2 freeze + the C++ qBittorrent fork) and
respects the core-vs-REST policy: the clients already expose peers over REST, so
the aggregation belongs outside the cores.

## Where the data lives (decision)

- **Clients**: keep *exposing* live peers/sources over their existing REST
  (qBittorrentBB `/sync/torrentPeers` includes country + bytes; emulebb-rust
  transfer-sources include peer IPs). They do **not** persist long-term analytics.
- **TrackMuleBB (web/controller)**: owns the **historical time-series + rollups +
  GeoIP enrichment + dashboards**.
- **Hybrid escape hatch (future, out of scope here)**: only if gap-free /
  byte-accurate per-peer accounting is needed (snapshot polling misses short-lived
  peers), push raw capture down into **emulebb-rust only** (our code, post-freeze) -
  never the qBittorrent C++ fork (REST suffices; fork-delta cost too high).

## GeoIP (decision)

- **Reuse eMuleBB's existing IP2Country MMDB** (MaxMind `.mmdb`, GeoLite2 City) -
  no new database/licence. TrackMuleBB reads it in Python via `maxminddb`/`geoip2`;
  config points `geoip_mmdb` at the eMuleBB config-dir file. One DB shared by both
  clients + controller.
- City mmdb yields country/city/subdivision and the matched **network prefix** (so
  per-IP-range bucketing is free). Per-**ASN**/operator needs the additional
  `GeoLite2-ASN.mmdb` (same reader) - add only if ASN breakdown is wanted.
- Enrichment happens **at ingest in Python**; DuckDB stores resolved columns
  (DuckDB does not read mmdb).

## Storage (decision: DuckDB)

- Long-term analytics in a dedicated **DuckDB** file (`analytics.duckdb`), separate
  from the intent-dedup SQLite (right tool per job: OLAP vs OLTP). DuckDB's columnar
  + vectorized engine fits the group-by/time-bucket/percentile workload; SQLite
  stays for the small transactional intent store.
- Optional cold tier: raw samples as **Parquet** partitioned by day, queried by
  DuckDB as an external table; prune by deleting old partitions.
- Pin the DuckDB version in the uv lockfile (storage format stable since v1.0).

## Acceptance Criteria

- [ ] A capability-gated sampling lane pulls peers/sources per backend on an
      interval and enriches IPs via the eMuleBB MMDB.
- [ ] Samples land in `analytics.duckdb`; a periodic rollup produces per-day
      per-country (and per-network/ASN if enabled) aggregates; raw is pruned.
- [ ] A NiceGUI analytics page renders charts (`ui.echart`/`ui.plotly`, no Node)
      from DuckDB aggregate queries, split/combined across eD2K + BT.
- [ ] Privacy: only aggregates persisted long-term; raw IP retention short or
      hashed; the store is local and git-ignored; no IP/private data in commits.
- [ ] Config: `geoip_mmdb` (+ optional `geoip_asn_mmdb`), retention, sample interval.

## Notes

- Builds on the transfers adapters (TMBB-FEAT-003) and capability negotiation
  (TMBB-FEAT-004). Independent of the push/SSE work (TMBB-FEAT-014 / RUST-FEAT-007).
- `maxminddb`/`geoip2` and `duckdb` are pure-Python wheels - no Node, consistent
  with the stack.
