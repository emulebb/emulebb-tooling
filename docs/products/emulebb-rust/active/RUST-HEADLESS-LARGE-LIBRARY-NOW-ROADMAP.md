# emulebb-rust Headless Large-Library Roadmap — NOW

**Updated:** 2026-10-03  
**Product boundary:** `repos/emulebb-rust`, plus the Rust soak/contract harness in
`repos/emulebb-build-tests`  
**Product intent:** a lean, powerful, headless eD2K/Kad client optimized for
large sharing libraries while preserving the smallest wire-compatible surface
that works cleanly on the public IPv4 networks.

## Decision

The daemon, authenticated REST API, and embedded SPA are the product. The
dormant Slint desktop client is removed from the workspace, dependency graph,
fresh-build gate, and package staging. Stock eMule compatibility is a wire and
state-machine requirement, not a requirement to reproduce its GUI or preference
surface.

The next live-test lane is WSL/Linux through a plain OpenVPN network namespace.
Use the persisted `repos/emulebb-build-tests/scripts/smoke-rust-openvpn.py`
launcher and operator-provided archive, Compose file, private credential root,
and report destination. Do not replace this path with inline launch logic or a
Gluetun-only result.

## NOW — implemented on development head

### 1. Large-library catalog and persistence

- Shared-file insert, replacement, removal, and hash lookup use the catalog's
  hash index rather than full-list scans.
- Startup restores persisted media metadata instead of reopening and extracting
  unchanged shared files. Schema version 23 stores artist, album, title,
  duration, bitrate, codec, and extractor version.
- Direct `/shared-files/{hash}` reads use a metadata hash lookup rather than
  materializing the complete catalog.
- `/shared-files` supports exclusive `afterHash` keyset pagination and returns
  `nextAfterHash`. Offset paging remains temporarily available for current
  consumers but is no longer the preferred large-library path.
- Server-offer ranking is cached for a publication sweep. A catalog is sorted
  once per refresh, and publish timestamp updates are indexed instead of
  scanning the whole library after every batch.

### 2. Negotiated fast server publishing

The client implements the upcoming `offerfiles_v=1` server advertisement from
`andrey23127/ed2k-server#19`:

- post-login `OP_SERVERIDENT` must contain exactly one correctly typed value for
  `offerfiles_v`, `offerfiles_batch_max`, `offerfiles_min_interval_ms`,
  `ST_SOFTFILES`, and `ST_HARDFILES`;
- version must be 1, soft/batch/interval must be non-zero, and hard must be
  greater than the advertised batch maximum;
- missing, partial, duplicate, wrongly typed, or inconsistent advertisements
  fail closed to the legacy one-batch policy for that connection;
- a capable connection uses a long-lived timer pump, bounded by the remaining
  soft candidate budget, advertised batch maximum, `hard - 1`, and the local
  200-record packet cap;
- the local client additionally caps sustained offer traffic at 400 records per
  second, even if the server advertises a faster interval;
- a rejected negotiated offer switches that connection to legacy behavior;
- search work pauses the background publish pump, and disconnect clears the
  negotiated policy because the capability is connection-scoped.

The setting `ed2k.offerFilesCapabilityEnabled` defaults on, is exposed as an
advanced restart-required control, and can disable negotiation if a server-side
rollout needs isolation. Server diagnostics expose the selected pacing mode,
current batch limit, advertised minimum interval, fallback reason, and
published/pending progress.

For a 100,000-file library and the proposed 200-record/500 ms server policy,
the deterministic client model emits 500 bounded batches over about 249.5
seconds, below the five-minute objective without enlarging legacy packet shape.

### 3. Lean supported surface

- Keep: eD2K server discovery/search/source discovery, peer download/upload,
  secure identification and credits, Kad bootstrap/search/publish/firewall and
  buddy behavior, NAT mapping, SQLite persistence, REST, and the embedded SPA.
- Remove: the separate Slint executable and its dependency/build/package cost.
- Do not add compatibility aliases, legacy GUI concepts, or dormant knobs unless
  they are required by a real peer/server wire behavior or an owned controller.

### 4. Startup scanning and publication overlap

- Persisted shared catalogs hydrate in bounded keyset pages after the first
  immediately useful page is available to the network runtimes.
- A cold empty profile scans and hashes a bounded small-first cohort before the
  exhaustive library walk. Successful files enter the live catalog and server
  publication queue immediately.
- The exhaustive scan and hash job is detached from the request that triggered
  it, and blocking filesystem/hash work does not run on asynchronous workers.
- Reload diagnostics expose scan, plan, hash, byte, failure, queue, and per-disk
  activity without placing source paths in normal path-free evidence.
- The LAN-only startup harness proves eD2K publication and active Kad publish
  workers while the initial 100k ingestion remains incomplete.

## Verification completed

- Rust policy gate and tooling tests.
- Rust formatting and clippy gate.
- Full Rust workspace unit/integration/doc-test gate, including the 100,000-file
  publisher model, capability parser/fallback tests, catalog persistence tests,
  keyset query validation, and REST settings/diagnostic coverage.
- Embedded SPA unit, Chromium end-to-end, typecheck, and production-build gates.
- Offline Rust router/OpenAPI route, parameter, settings, response, and error
  contract alignment.
- External soak metadata migration tests for schema 23, including v22 to v23.
- The deterministic 100,000-file SSD campaign passed cold scan, warm reload,
  one-percent mutation, 1,000 long-path files, watcher lifecycle, restart, and
  cleanup. Its retained report is
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-shared-library-io-20261003T153209Z-11012.json`.
- The LAN-only startup campaign observed 8,596 shareable files with 91,407 hashes
  still pending, and the local eD2K server accepted the first 200 files while
  Kad publication workers were active. Its retained report is
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-shared-library-lan-startup-20261003T183046Z-16340.json`.
- The credentialed WSL2 + plain-OpenVPN public-network witness passed on Rust
  commit `10a9c74e`. The retained report is
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\rust-openvpn\20261003T065145Z-rust-now-10a9c74e.json`;
  its six PCAPs are beside it. Archive SHA-256 is
  `987776074f27b5f34b52eab6682386ac12c98a96c69078336b36800a4f9440bf` and the
  certified daemon SHA-256 is
  `ea51bd60c1f571ab1e4cb972a293ab660b7d7a3ac7d39e69cad3a46f002421a9`.
  Plain OpenVPN owned PID 1, public traffic and the interface+IP P2P binding used
  `tun0`, eD2K and Kad became ready, and two rounds each of server, global UDP,
  and Kad search completed with results. The four-case NAT matrix passed with
  the VPN route correctly classified as mapping-unsupported, pre-existing
  Compose projects were preserved, and teardown left no test resources.

## NEXT — in order

1. Add a deterministic server fixture that emits the exact five-field
   `OP_SERVERIDENT` advertisement, accepts the complete 100,000-record sweep,
   and verifies connection-scoped fallback for malformed and rejected batches.
2. Reduce the measured SQLite/catalog amplification tracked by
   [RUST-REF-008](items/RUST-REF-008.md): index and batch stale-source removal,
   batch initial share persistence without weakening durability, decouple media
   enrichment from first publication, and repeat the bounded SSD comparison.
3. Correct cross-platform filesystem identity through
   [RUST-BUG-107](items/RUST-BUG-107.md) and storage-domain scheduling through
   [RUST-REF-009](items/RUST-REF-009.md) before claiming equivalent multi-disk
   behavior on Linux/macOS.
4. Bound watcher reconciliation through
   [RUST-REF-010](items/RUST-REF-010.md), then run the Unicode/long-path platform
   matrix in [RUST-CI-008](items/RUST-CI-008.md).
5. Capture representative per-HDD cohorts only after the preceding counters and
   fixes exist. Keep the completed 100k SSD report as the baseline and do not
   rerun an unbounded real-media library.
6. Once keyset consumers have shipped, decide whether offset paging is worth
   retaining. Removal is an API-cleanup decision, not a wire-compatibility issue.
7. Resume autonomous indexer/Torznab and Arr work only after the large-library
   base and live publishing witness remain green.

## PARKED — explicit future boundary

IPv6 support remains a separate protocol project. Do not reinterpret classic
IPv4 fields, advertise eMuleAI IPv6 bits, or mix IPv4/IPv6 Kad contacts before
there is an end-to-end address model, persistence format, capability contract,
peer/server consumer coverage, and dual-stack live evidence. aMule/eMuleAI
research remains valuable input, but partial advertisement would reduce
interoperability rather than improve it.
