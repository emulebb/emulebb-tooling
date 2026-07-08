# Test Strategy & Gating Taxonomy

Status: planning / direction. Captured 2026-06-15. This document is the plan for a
later test-suite code revision; it makes **no test-code changes**. Goal: a
complete, clean test suite where code is reused, repeated operations live in
dedicated modules, end-to-end coverage is strong, and a release's gating set is
clearly separated from reference-only tests kept on demand.

Companion governance: [QUALITY-GATES](QUALITY-GATES.md),
[PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md),
[WORKSPACE-POLICY Network Safety](../WORKSPACE-POLICY.md#network-safety-no-clearnet-leak-p0-invariant).

## Goal

- **Uniformity & reuse:** one shared harness; repeated operations in dedicated
  reusable modules + pytest fixtures, not copied per test.
- **Dedicated modules for repeated operations** — the headline example is
  *registering an executable in the VPN split-tunnel*: it already has a clean
  module (`hideme_split_tunnel.ensure_vpn_ready(exe)`); make it the universal
  funnel + a fixture and use it for every networked product.
- **Strong end-to-end coverage**, including the suite's headline flows
  (cross-network eD2K↔BitTorrent, and the network-safety leak-test).
- **Gating vs reference:** the suite release gate runs a lean, fast, deterministic
  set; MFC-source and parity/VM tests are kept as historical reference, run on
  demand, and excluded from the forward-suite gate.

## Current state (grounded, 2026-06-15)

Five test ecosystems; the Python harness is the cross-product orchestration + E2E
layer and the main leverage point for uniformity.

| Ecosystem | Where | Footprint |
|---|---|---|
| Python harness (E2E/orchestration) | `emulebb-build-tests` | 178 pytest tests, ~50 harness modules |
| C++ MFC native | `emulebb-build-tests/src` + `emule-tests.vcxproj` | native test exe |
| qBittorrentBB C++/Qt | `qbittorrentbb/test` | 16 test `.cpp` + `livewire/` |
| Go (goed2k) | `goed2k-server` | 21 `*_test.go` |
| Rust (emulebb-rust) | `emulebb-rust/crates` | 116 unit-test files + 59 integration tests |
| amutorrent JS (Jest) | `amutorrent/tests` | 10 `*.test.js` |

Python harness specifics:

- Default gate selection is `addopts = -m "not live and not native"`. Markers
  defined: only `unit`, `native`, `live`, `slow`.
- **58 `tests/python/test_*_source.py`** assert seams/guards in the **frozen MFC
  C++ source** (`workspaces/workspace/app/emulebb-main/srchybrid/...`). They are
  pure-Python, unmarked, so they **currently gate every run** (~33% of the Python
  tests).
- **27 `*live*` files**, but only ~3 actually carry `@pytest.mark.live`; the rest
  rely on env-var self-skip — inconsistent marker discipline.
- **No `conftest.py`** anywhere — no shared pytest fixtures.

What is already good (do not rebuild): the shared harness is rich; the VPN module
(`hideme_split_tunnel.py`) is clean and idempotent; there are real cross-client
E2E tests; markers `live`/`unit` exist; a tracked-file privacy guard runs in CI.

## Problems identified

- **R1 — No shared fixtures.** No `conftest.py`; the standard reuse mechanism is
  absent, forcing duplication.
- **R2 — Duplicated primitives.** `free_lan_port` is defined **6 times with 4
  different signatures** (`free_lan_port(host)`, `free_lan_port_not(host,
  forbidden)`, `_free_lan_port(host, taken)`, `_free_port(host, taken)`) across
  `test_amutorrent_rust_controller`, `test_emulebb_rust_local_client`, and the 3
  goed2k live tests. A flake fix previously had to be applied to multiple copies.
- **R3 — VPN module under-funneled / product-siloed.** `ensure_vpn_ready` is the
  right module but is imported by only a script + `test_live_bind_policy_static`;
  parallel VPN-lifecycle code likely lives in `windows_vm_hideme_live.py` (451
  lines) and `vpn_guard_live.py`. **qBittorrentBB and amutorrent live tests do not
  use the shared VPN module at all** — the suite is going cross-network while VPN
  registration is still eMule/rust-centric.
- **R4 — Scattered client-launch logic.** Launch/Popen/visible-app code is spread
  across ~12 harness modules (`amule.py`, `goed2k.py`, `rust_client.py`,
  `rust_local_ed2k.py`, `vm_guest_profiles.py`, `windows_vm_local_ed2k.py`,
  `windows_vm_profile_smoke.py`, `live_e2e_suite.py`, …) with overlapping
  responsibilities and no single client-runner abstraction.
- **R5 — Mega-modules.** `live_e2e_suite.py` is **2990 lines**;
  `windows_vm_profile_smoke.py` 1146; `windows_vm_guest.py` 1116;
  `live_process_monitor.py` 745. Low cohesion blocks reuse.
- **R6 — Thin marker taxonomy.** Only `live/native/unit/slow`; there is no way to
  express "reference / non-gating but keepable", so MFC-source and parity tests
  gate the suite.
- **R7 — E2E gaps on headline flows.** No cross-network (eD2K↔BitTorrent / metadata
  fabric / "download the torrent instead") E2E; no network-safety leak-test;
  qBittorrentBB is in no cross-client E2E.

## Target structure

```
emulebb-build-tests/
  emule_test_harness/
    net_ports.py          # ONE free LAN port helper (replaces the 6 copies)
    vpn.py                # = hideme_split_tunnel; the SINGLE VPN funnel for ALL products
    client_runner.py      # prepare profile -> register in VPN -> launch -> drive REST -> teardown
    leak_assert.py        # "no P2P egress off the tunnel" assertion, reused by every networked product
    steps/                # reusable E2E step library (extracted from live_e2e_suite)
    ...                   # existing focused modules stay
  tests/python/
    conftest.py           # shared fixtures + auto-marking by filename convention
    unit/ contract/ source/ live_local/ live_public/   # taxonomy mirrored in layout (optional)
```

Principles: (1) **one harness, every product plugs in** — no parallel suites for
qBittorrentBB/amutorrent; (2) **each repeated operation = one module + one
fixture** (ports, VPN, launch, leak); (3) the VPN module is the **exemplar** for
how a repeated operation is packaged.

## Test taxonomy (tiers + markers)

| Marker | Meaning | Gating role |
|---|---|---|
| `unit` | fast pure-Python harness/logic tests | suite gate |
| `contract` | REST/Torznab/`/api/v1` contract tests | suite gate |
| `e2e_local` | deterministic local multi-client transfer (workspace services only) | suite gate |
| `mfc_source` | MFC C++ source-seam coverage (the 58 `*_source.py`) | MFC `0.7.x` gate only |
| `reference` | community-baseline / tracing-harness parity, superseded, historical | never gates; on demand |
| `live_local` | local live stack against deterministic workspace services | conditional / on demand |
| `live_public` | real public eD2K/Kad/BitTorrent network | never gates; manual |
| `vm` | visible-VM / interactive-desktop / hide.me live smoke | never gates; manual |
| `slow` | long-running scenarios | excluded from fast gate |
| `native` | requires the built `emule-tests.exe` | MFC gate only |

## Gating matrix (per release)

| Release gate | Selection (intent) |
|---|---|
| **Suite / forward** (rust, qBittorrentBB, amutorrent) | `unit or contract or e2e_local` — excludes `reference`, `mfc_source`, `vm`, `live_public`, `slow` |
| **emulebb-mfc 0.7.x patch** | the above **plus** `mfc_source`, `native`, and community parity |
| **On demand / manual** | `mfc_source`, `reference`, `vm or live_public`, `slow` (run explicitly) |

This row should be added to [QUALITY-GATES](QUALITY-GATES.md) as the "test gating
set per tier".

## The reference (non-gating) set — explicit

Kept as historical reference, runnable on demand, **excluded from the suite gate**:

- **The 58 `tests/python/test_*_source.py`** — MFC C++ source-seam coverage of the
  frozen `emulebb-main/srchybrid` app (e.g. `test_download_list_ctrl_source`,
  `test_kad_ui_source`, `test_irc_channel_tab_source`). → marker `mfc_source`;
  gate only for MFC `0.7.x` patches.
- **Community/baseline & native parity** — `test_community_core_coverage`,
  `test_native_coverage`, and any `baseline/community-0.72a` / tracing-harness
  comparison. → `reference`.
- **VM / UI / hide.me / public-network smoke** — `windows_vm_profile_smoke`,
  visible-VM tests, hide.me live, public-network live. → `vm` / `live_public`;
  manual only.
- **Superseded tests** — replaced by newer coverage (precedent: the removed
  `test_goed2k_amule_publish_live`). → delete or `reference`.

Forward-relevant tests that **stay in the suite gate** (not reference): harness
unit tests, REST contract tests, the rust parity audits
(`test_rust_ed2k_private_parity_modules`, `test_rust_ed2k_total_parity_audit`),
deterministic local cross-client transfer, per-product unit suites, and the future
leak-test.

## Dedicated modules plan (repeated operations)

- **`net_ports.py`** — one `free_lan_port(host, *, taken=())` (and a fixture
  `free_port`) replacing the 6 duplicated definitions. Carries the
  `udp = tcp + 4` Windows-reserved-range guard already learned for goed2k.
- **`vpn.py` (the exemplar)** — make `ensure_vpn_ready(exe_path)` the **single
  funnel**: route `windows_vm_hideme_live.py` and `vpn_guard_live.py` through it
  (remove parallel VPN-lifecycle code) and use it for **every** product's live
  exe (rust, eMuleBB, qBittorrentBB). Expose a fixture `vpn_ready_exe`.
- **`client_runner.py`** — one interface: `prepare_profile -> register_in_vpn ->
  launch -> drive_rest -> teardown`, implemented per client (amule / rust /
  eMuleBB / qBittorrentBB), replacing scattered launch logic.
- **`leak_assert.py`** — assert no eD2K/Kad/BitTorrent data egress off the tunnel
  with the tunnel down; reused by every networked product (the automated form of
  the P0 Network Safety invariant; backs `RUST-FEAT-005` / `QBBB-FEAT-004`).
- **`steps/`** — extract reusable E2E steps from `live_e2e_suite.py` (2990 lines)
  into a focused step library; scenarios compose steps.

## End-to-end coverage plan

Add the headline flows that are currently uncovered:

- **Cross-network eD2K↔BitTorrent** — exercise the metadata fabric and the
  "download the torrent instead" handoff end-to-end (eD2K client + qBittorrentBB +
  fabric). Currently zero.
- **Network-safety leak-test** — `leak_assert` driven for each networked product;
  release-blocking.
- **qBittorrentBB in cross-client E2E** — wire it into the shared harness rather
  than its isolated `test/` suite for the cross-product scenarios.

## Implementation plan (later code revision — sequenced)

Each phase is its own focused change; **do not bundle**.

1. **Taxonomy & gating (classification only, no behavior change).**
   `conftest.py` with shared fixtures **and auto-marking by filename convention**
   (`*_source.py` -> `mfc_source`, `*live*` -> `live`, …) so the 58 source files
   need no edits; extend the marker list; define explicit gate profiles; update
   `addopts`/CI to the suite-gate selection; add the gating row to QUALITY-GATES.
2. **De-duplicate primitives.** `net_ports.py` + `free_port` fixture replacing the
   6 copies; make `vpn.py`/`ensure_vpn_ready` the single funnel + `vpn_ready_exe`
   fixture.
3. **Client runner + split mega-modules.** `client_runner.py`; extract
   `live_e2e_suite.py` into `steps/` + scenarios.
4. **New E2E.** `leak_assert.py` + leak-tests; cross-network fabric E2E; wire
   qBittorrentBB into the shared harness.

## Open questions / decisions

- Confirm `mfc_source` gates **only** MFC `0.7.x` patches (not the suite). (Default
  assumption: yes.)
- Auto-marking by filename in `conftest.py` vs explicit per-file markers (default:
  auto-marking, lowest touch).
- Whether `live_local` deterministic tests join the suite gate or stay on demand
  (depends on runtime + determinism per test).
- Home of the leak-test primitive (default: shared harness `leak_assert.py`,
  consumed by per-product live tests).
