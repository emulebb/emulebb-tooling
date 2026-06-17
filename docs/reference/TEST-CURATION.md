# Test Curation — Necessary vs Not

Companion to the generated [Test Inventory](TEST-INVENTORY.md) and the
[Test Tiers](TEST-TIERS.md). It applies four lenses, in priority order, to decide
what the maintained test surface should run and where:

1. **Non-redundancy** — cut where multiple layers cover the same thing.
2. **Minimize runtime** — push slow load/soak/stress to the highest tier.
3. **Forward program** — rust / qBittorrentBB / TrackMuleBB coverage, not just the frozen MFC app.
4. **0.7.3 correctness gate** — what proves the shipped surface.

Verdict vocabulary: **KEEP** (necessary, stays where it is), **OPTIONAL** (gate to a
higher tier or default-off), **WIRE-IN** (necessary but currently not auto-run — connect
it to a tier), **CUT** (redundant or dead — remove/merge). All numbers come from the
inventory catalog.

## Headline findings

- **At the native layer the problem is dormancy, not redundancy.** 30 of 34 doctest
  suites — **305 cases** — are reached only by `test native --suite-name` and run by **no
  tier or campaign**. That is a coverage hole, not waste.
- **Live-e2e tiering is already clean.** The quick/fast live set is entirely low-stress
  (`stressClass = scenario`); every soak/stress/hammer/chaos suite is overnight-tier only —
  with one exception below.
- **One concrete profile duplication:** `multi-client-p2p` and `multi-client-p2p-required`
  are the *same* 7-suite list.
- **One dead live suite:** `shared-directory-browse-stress` (558 LOC) belongs to no profile
  and is not default-enabled.

## Native layer (34 suites, 1165 cases)

| Group | Verdict | Notes |
| --- | --- | --- |
| `parity` (117 files, 859 cases), `web_api` (87), `protocol-parity` (13) | **KEEP** | `runBy = test-all`; the 0.7.3 gate backbone. |
| `community-core-divergence` (3) | **KEEP** | Orchestrated by community-core coverage (overnight). Correctly tier-gated. |
| Behavior suites currently dormant — e.g. `fake_file_detector` (32), `kad-broadband` (33), `kad-base` (6), `packets` (9), `startup` (13), `startup_storage` (5), `version_check_launch` (8), `server_connect`/`server_info` (3+4), `part_file_hash_launch` (8), `part_file_majority_name` (10), `search_trust_hint` (8), `process_launch`/`restart_app` (3+4), `windows_firewall_repair` (2), `background_refresh` (6), `async_dns_resolve` (4), `diagnostic_snapshot` (3) | **WIRE-IN** | Real shipped behavior with **no tier running it**. Recommend tagging into `parity` (or a new auto-run suite) so it gates. Highest-value native action. |
| `benchmark` (11), `pipeline` (11), `pipeline-benchmark` (11) | **KEEP targeted-only** | Performance, not correctness — never in a tier (runtime lens). |
| Frozen MFC UI suites — `download_list_keyboard_shortcuts` (5), `file_list_keyboard_shortcuts` (9), `download_progress_bar` (4), `status_bar` (5), `pro_user_menu_copy` (4), `shared_dirs_tree_ctrl` (1) | **OPTIONAL** | Frozen, low-churn UI surface; fine as targeted-only, out of quick. |
| `divergence` (6 files, 78 cases) | **REVIEW → possible CUT/merge** | Large dormant suite; verify overlap against `community-core-divergence` and the in-`parity` divergence checks; merge or drop if duplicated. |

## Live-e2e layer (41 suites, 8 default-enabled)

| Group | Verdict | Notes |
| --- | --- | --- |
| Fast set — `preference-ui`, `shared-files-ui`, `config-stability-ui`, `shared-hash-ui`, `startup-diagnostics`, `shared-directories-rest`, `rest-api` (+ `auto-browse-live`) | **KEEP (quick/fast)** | All `stressClass = scenario`; necessary core UI/REST. |
| Soak/stress/hammer/chaos — `godzilla-local-swarm`, `local-ed2k-search-soak`, `local-ed2k-chaos-mode`, `rest-cold-start-dump-stress`, `live-process-monitor`, swarms, `category-incoming-path-matrix` | **KEEP (overnight only)** | Already overnight-tier profiles; confirm none leak into quick/fast (catalog: none do). |
| Storage suites (10: vhd/unc/shared-cache/disk-space) — all `default_enabled=False` | **OPTIONAL** | Heavy filesystem; overnight/storage profiles only. Correct as-is. |
| `shared-directory-browse-stress` | **CUT (or WIRE-IN)** | Orphan: no profile, not default-enabled. Delete (with its self-test) or attach to `stabilization-stress`. |
| `multi-client-p2p` vs `multi-client-p2p-required` profiles | **CUT (dedup)** | Identical 7-suite lists; collapse to the `-required` variant (stronger evidence). |
| `deterministic-two-client-transfer` | **REVIEW** | Overlaps `multi-client-p2p-matrix` on local transfer; lives in 3 profiles. Consider OPTIONAL. |
| Live-wire ARR — `radarr-emulebb`, `sonarr-emulebb`, `prowlarr-emulebb` | **KEEP (live-wire/release only)** | Forward/controller surface; never in quick/fast. |

## Python-harness layer (124 modules, 56 self-test a live script)

| Group | Verdict | Notes |
| --- | --- | --- |
| All harness modules | **KEEP (quick/fast)** | Fast unit tests, no app/network. The big ones (`test_rest_api_smoke` 4398 LOC, `test_master_source_parity` 4264) are still app-free. |
| 56 modules that self-test a live script | **KEEP** | Unit-vs-integration pairing is intentional, not redundant. |
| Coupling rule | — | When a live suite/script is CUT, cut its self-test module too (mapping is in the catalog `selfTestsScript`). |

## Phase 3 — action list (separate approval; freeze-sensitive)

Ordered by value, each citing catalog evidence:

1. **Native dormancy (biggest win):** wire the ~20 behavior suites above (~250 cases) into an
   auto-run tier so they gate. Touches shipped-surface test execution during the freeze →
   explicit per-suite approval.
2. **Live cleanup:** delete or wire `shared-directory-browse-stress`; collapse the duplicate
   `multi-client-p2p` profile into `multi-client-p2p-required`.
3. **Native redundancy:** resolve `divergence` (78 cases) vs `community-core-divergence`; merge or cut.
4. **Coupling:** when cutting any live suite/script, remove its python self-test module.

Regenerate the catalog after any change with
`python scripts/show-test-inventory.py --markdown` and re-run
`python -m pytest tests/python/test_test_inventory.py`.
