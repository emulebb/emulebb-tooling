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
- WSL2 Ubuntu, Docker Engine, the plain-OpenVPN Compose input, and the persisted
  smoke launcher's Linux entrypoint are available; the credentialed live witness
  still requires an operator-supplied candidate archive and private VPN root.

The WSL + OpenVPN public-network witness is intentionally a separate operator
evidence step because it consumes private VPN configuration and a packaged
client archive. It must record the archive hash, Compose input, binding mode,
methods exercised, tunnel evidence, and output report path.

## NEXT — in order

1. Run the packaged client through `smoke-rust-openvpn.py` in WSL with `tun0`
   interface+IP binding. Exercise server, global UDP, and Kad searches; include
   repeated searches and the NAT matrix where the provider supports it.
2. Add a deterministic server fixture that emits the exact five-field
   `OP_SERVERIDENT` advertisement, accepts the complete 100,000-record sweep,
   and verifies connection-scoped fallback for malformed and rejected batches.
3. Capture performance evidence for cold scan, warm restart, REST traversal,
   steady-state watcher updates, and publication sweep at 10k, 50k, and 100k
   shared files. Treat wall time, peak RSS, SQLite growth, and event-loop stalls
   as release evidence rather than informal observations.
4. Once keyset consumers have shipped, decide whether offset paging is worth
   retaining. Removal is an API-cleanup decision, not a wire-compatibility issue.
5. Resume autonomous indexer/Torznab and Arr work only after the large-library
   base and live publishing witness remain green.

## PARKED — explicit future boundary

IPv6 support remains a separate protocol project. Do not reinterpret classic
IPv4 fields, advertise eMuleAI IPv6 bits, or mix IPv4/IPv6 Kad contacts before
there is an end-to-end address model, persistence format, capability contract,
peer/server consumer coverage, and dual-stack live evidence. aMule/eMuleAI
research remains valuable input, but partial advertisement would reduce
interoperability rather than improve it.
