# Test Campaign Architecture Plan — MFC maintenance + rust construction

Status: proposal (no code yet). Owner decision pending on sequencing.
Companion docs: [Test Tiers](../../reference/TEST-TIERS.md),
[Test Inventory](../../reference/TEST-INVENTORY.md),
[Test Curation](../../reference/TEST-CURATION.md).

## Context

We run two products with opposite test needs. **eMuleBB MFC** is in maintenance
(0.7.3 shipped, stable, stock-compatible; 0.8.0 is the future legacy-removal line):
its tests are **regression guards** — cheap, stable, run often, with the heavy
stock-parity comparisons already moved on-demand. **eMuleBB-rust** is under active
construction (0.0.x headless core): its tests are the **specification** — they define
correct, and the bar is convergence to the MFC + stock reference.

The bridge between the two is a single fact: they must speak the **same eD2K/Kad wire
protocol** and the **same `/api/v1` REST contract**. As rust matures, the test center of
gravity shifts from "MFC regression" to "**rust ≡ MFC ≡ stock conformance**". The decisive
move is to promote the already-existing but scattered conformance mechanisms into a
**first-class wire-conformance campaign** that becomes rust's real ship bar: not "rust
passes its own tests" but "rust is indistinguishable from eMuleBB on the wire".

## Existing assets to reuse (do not rebuild)

- **`manifests/protocol-oracle-golden.v1.json`** — normalized eD2K/Kad packet vectors
  (opcode, payloadDigest, direction), generated from MFC + community baseline native
  protocol-parity + the tracing-harness JSONL normalizer. The canonical wire truth.
- **`emule_test_harness/packet_trace_diff.py`** — diffs two `ed2k_packet_v1` JSONL dumps
  (rust via `EMULEBB_RUST_LOG_DIR`, eMuleBB via the `EMULEBB_ENABLE_PACKET_DIAGNOSTICS`
  build). Wire identity key = `(protocol_marker, opcode, payload_hex)` — not opcode name,
  not transport vocab, not timestamps. Reports match / payload-diff / one-side-only.
- **`emule_test_harness/diag_event_diff.py`** — diffs `diag_event_v1` per-decision
  scheduling + kad_udp between the MFC master and rust.
- **`scripts/multi-client-p2p-matrix.py`** — rust↔emulebb↔amule bidirectional exchange with
  `userHash` / MD4 / AICH metadata assertions and `--require-scenario`.
- **`scripts/local-ed2k-protocol-combinations.py`** (MFC) and
  **`scripts/local-ed2k-rust-protocol-combinations.py`** (rust) — the 4 protocol cases:
  plain, obfuscation-preferred, obfuscation-required, server-UDP-disabled.
- **Oracle pipeline:** `normalize-protocol-oracle.py`, `compare-protocol-oracle.py`,
  `protocol-pcap-capture.py`, `validate-protocol-goldens.py`.
- **`emule_test_harness/master_source.py`** + `test_master_source_parity` — source parity.
- Campaign schema: `manifests/release-campaigns/v1.schema.json`,
  `STRICT_PHASE_TAXONOMY` = preflight, protocol-parity, controller-surface,
  live-wire-release, ui-resource-depth, stabilization-stress, packaging-provenance.

## Target campaign set (three circles)

| Campaign | Product | Cadence | Purpose | State |
| --- | --- | --- | --- | --- |
| `emulebb-0.7.3` (+ overnight) | MFC | quick/fast + release | regression + patch proof | exists, green |
| `emulebb-0.8.0` modernization | MFC | future | legacy-removal line (`scheduler_removal`, `kad-broadband` guards flip green) | to design when 0.8.0 starts |
| `emulebb-rust` (+ overnight) | rust | cargo + overnight | construction inner loop + local parity | exists |
| **`emulebb-wire-conformance`** ⭐ | cross | protocol-change + nightly | rust ≡ MFC ≡ stock on the wire | **to build (priority)** |
| **`emulebb-rest-conformance`** | cross | contract-change | `/api/v1` identical on both products | to build |
| **`*-leak-test`** (P0) | per product | release-blocking | VPN-down → zero data-plane egress | gaps open |

Circle 1 = per-product (cheap, frequent). Circle 2 = shared conformance (the contract —
where to invest now). Circle 3 = P0 safety (release-blocking both sides).

## Priority design: `emulebb-wire-conformance` campaign

New manifest `manifests/release-campaigns/emulebb-wire-conformance.v1.json`, schema
`kind: instance`, `templateId: emulebb.release.template.default.v1`,
`campaignId: emulebb-wire-conformance`, `proofTier: future` (rust is 0.0.x; promote to a
gating tier when fully green). All seven taxonomy phases present; scenarios below. Every
scenario reuses an existing mechanism — the campaign is wiring + evidence, not new test code.

### preflight
- `wire.preflight.materialize` — `python -m emule_workspace sync` (rust resolves from the
  org; goed2k server present). Evidence: manual.
- `wire.preflight.build-pair` — build MFC main (Release x64) + rust (cargo) + goed2k server.
  Evidence: manual / build recap. (Both clients must emit their packet/diag dumps:
  MFC `--diagnostics` with `EMULEBB_ENABLE_PACKET_DIAGNOSTICS`; rust `EMULEBB_RUST_LOG_DIR`.)

### protocol-parity (the heart)
- `wire.golden.mfc` — `validate-protocol-goldens.py` over `protocol-oracle-golden.v1.json`
  for the MFC client. Evidence: json-status, all golden vectors match.
- `wire.golden.rust` — the rust protocol-combinations run validated against the **same**
  oracle. Evidence: json-status, same vector set, zero divergence.
- `wire.packet-diff.rust-vs-mfc` ⭐ — drive a local rust↔eMuleBB exchange (via the
  multi-client matrix / protocol-combinations), then `packet_trace_diff.py` aligns the two
  `ed2k_packet_v1` dumps. **Evidence (json-status): 0 one-side-only packets, 0
  same-opcode payload divergences** across all `(flow, direction)` pairs.
- `wire.diag-diff.rust-vs-mfc` — `diag_event_diff.py` over the `diag_event_v1` dumps →
  same per-decision scheduling + kad_udp send decisions. Evidence: json-status, 0 decision
  divergences (or an allow-list of documented, justified deltas).
- `wire.protocol-combinations` — the 4-case matrix (plain / obf-preferred / obf-required /
  UDP-disabled) run for **both** clients with identical pass criteria (link round-trip,
  3 transfers/case, hash-only metadata recovery, userHash + MD4/AICH per named transfer).
- `wire.cross-client.bidirectional` — multi-client matrix rust↔eMuleBB and rust↔aMule
  bidirectional, Unicode filenames, rust-persisted userHash/MD4/AICH (aMule's missing AICH
  recorded). Evidence: json-status on the matrix report.

### controller-surface
- `wire.rest.contract-pointer` — thin pointer to `emulebb-rest-conformance` (below); keep
  here as a non-blocking evidence row so the campaign view is complete.

### live-wire-release
- `wire.live.deferred` — non-blocking; public-network rust↔stock conformance is deferred
  until rust has the hide.me-bound VPN contract (RUST-FEAT-003/005). Documents the gate.

### ui-resource-depth / stabilization-stress / packaging-provenance
- ui-resource-depth: empty (n/a for a wire campaign).
- stabilization-stress: optional non-blocking soak of the rust↔eMuleBB exchange under load,
  re-running packet-diff to catch divergence only under pressure.
- packaging-provenance: optional — record the converged `ed2k_packet_v1` /
  `protocol-oracle-golden` schema versions used, for provenance.

### releaseGates
- `wire-golden-conformance` ← `wire.golden.mfc`, `wire.golden.rust`
- `wire-packet-faithfulness` ← `wire.packet-diff.rust-vs-mfc`, `wire.diag-diff.rust-vs-mfc`
- `wire-cross-client` ← `wire.protocol-combinations`, `wire.cross-client.bidirectional`

The headline gate is **`wire-packet-faithfulness`**: this is "rust is the same client on the
wire". When it is durably green, rust graduates from `proofTier: future` to a gating tier.

## Second design: `emulebb-rest-conformance` campaign

Both products implement `/api/v1`. Today the rust side (`test_emulebb_rust_rest_contract`)
checks route table + request/response field set vs the OpenAPI; MFC has the native `web_api`
suite (87 cases). Unify into one campaign that validates **both** against the single
`docs/rest/REST-API-OPENAPI.yaml`:
- `rest.contract.openapi.rust` — route table + deny-unknown-fields + response field
  alignment (existing rust test).
- `rest.contract.openapi.mfc` — the `web_api` native suite mapped to the same OpenAPI.
- `rest.controllers.parity` — drive aMuTorrent (and the arr handoff) against **both** the
  MFC and rust controller and assert identical observable behavior on the shared envelopes
  (connect, categories, snapshot, shared files, search, transfer create/control).
This is what guarantees controllers (aMuTorrent, Prowlarr/Radarr/Sonarr) work the same on
either core.

## Third: network-safety leak-test (P0, per product)

Release-blocking invariant: tunnel down → zero data-plane egress (eD2K TCP, Kad/eD2K UDP).
- MFC: the VPN Guard exists; add an explicit automated leak-test scenario to the MFC
  campaign (tunnel down → assert no eD2K/Kad egress off the tunnel).
- rust: close `RUST-FEAT-003` (eD2K TCP egress pin) + `RUST-FEAT-005` (leak-test), then add
  the same scenario to the rust campaign.
Each product's leak-test is a blocking gate in its own campaign.

## Future: `emulebb-0.8.0` modernization campaign

When 0.8.0 work starts, the dormant guards become positive assertions: `scheduler_removal`
(currently red-by-design) goes green once the legacy scheduler is removed; `kad-broadband`
becomes buildable once `KadPublishGuard.h` / `SafeKad.h` land. A 0.8.0 campaign tracks the
legacy-surface removals as gates.

## What to reuse vs build

- **Reuse (≈90%):** all mechanisms above already exist (oracle golden, packet_trace_diff,
  diag_event_diff, multi-client matrix, protocol-combinations, validate-protocol-goldens,
  rust REST contract test, web_api suite).
- **Build (small):** the **manifests** (`emulebb-wire-conformance.v1.json`,
  `emulebb-rest-conformance.v1.json`), thin **aggregator scripts** that run an exchange then
  invoke `packet_trace_diff` / `diag_event_diff` and emit one json-status report under the
  output root, the **evidence wiring** (campaign scenarios → report pointers), and the
  per-campaign **leak-test** scenarios. Plus tests in `test_release_campaigns.py` that
  validate the new manifests against the schema and gate coverage.

## Sequencing

1. **Wire-conformance manifest + packet/diag aggregator + evidence** (highest value; turns
   scattered checks into one "same client on the wire" gate). Start as `proofTier: future`.
2. **REST-conformance manifest** (pairs the existing rust + MFC contract checks).
3. **Leak-test scenarios** (P0) — MFC first (guard exists), then rust after RUST-FEAT-003/005.
4. **Promote wire-conformance to a gating tier** once `wire-packet-faithfulness` is durably
   green.
5. **0.8.0 modernization campaign** — when that line opens.

## Acceptance / verification

- New manifests pass `release_campaigns.validate_release_campaign` (schema, strict phase
  taxonomy, gates ⊆ scenarios) and new cases in `tests/python/test_release_campaigns.py`.
- `python -m emule_workspace test campaign --campaign emulebb-wire-conformance` (report
  mode) renders all phases/gates; execute mode runs the reused mechanisms and writes the
  json-status evidence the gates read.
- `wire.packet-diff.rust-vs-mfc` produces 0 one-side-only and 0 same-opcode payload
  divergences on a local exchange — the concrete green bar.

## Open decisions for the owner

1. **proofTier** for wire-conformance: start `future` (recommended) vs go straight to a
   gating tier.
2. **diag-diff tolerance**: exact 0 divergences vs an allow-listed set of documented,
   justified scheduling deltas (rust may legitimately differ on non-wire-visible decisions).
3. **Whether to fold REST-conformance into wire-conformance** (one cross-product campaign)
   or keep them separate (recommended separate: different cadence and failure modes).
4. **Naming**: `emulebb-wire-conformance` / `emulebb-rest-conformance` vs a single
   `emulebb-conformance` umbrella.
