# Test Curation — Necessary vs Not

Companion to the generated [Test Inventory](TEST-INVENTORY.md) and the
[Test Tiers](TEST-TIERS.md). It records how the maintained test surface was
curated through four lenses, in priority order:

1. **Non-redundancy** — cut where multiple layers cover the same thing.
2. **Minimize runtime** — push slow load/soak/stress to the highest tier.
3. **Forward program** — rust / qBittorrentBB / TrackMuleBB coverage, not just the frozen MFC app.
4. **0.7.3 correctness gate** — what proves the shipped surface.

Verdict vocabulary: **KEEP**, **WIRED-IN** (was dormant, now gated), **OPTIONAL**
(targeted-only / higher tier), **TRIAGE** (failing — fix before gating), **CUT**.

## Headline findings

- **The native layer's real problem was dormancy, not redundancy.** 30 of 34 doctest
  suites (305 cases) ran by *no* tier or campaign — reachable only via
  `test native --suite-name`. Probing the built test binary showed most are fast
  (sub-100ms), seam-driven, and green.
- **Three dormant suites were actually failing** and nobody noticed because no tier ran
  them: `fake_file_detector` (1 failed of 129) and `startup` (1 of 61) were stale assertions
  — both fixed and wired — and `divergence` (8 of 431) is a deliberate 0.8.0 removal guard.
- **The "duplicate profile" was a false positive.** `multi-client-p2p` and
  `multi-client-p2p-required` share a suite list but differ in semantics — the `-required`
  variant enforces optional third-party clients as mandatory (`live_e2e_suite.py`
  branch on `multi-client-p2p-required`). Both are kept.
- **Live-e2e tiering is already clean:** the quick/fast set is entirely low-stress; every
  soak/stress/hammer/chaos suite is overnight-tier only (one orphan noted below).

## Native layer — executed

19 dormant suites were verified green and fast against the built test binary and
**wired into `test all`** (`TEST_ALL_NATIVE_SUITES` in `test_runs.py`), so they now gate at
every tier:

`async_dns_resolve`, `background_refresh`, `diagnostic_snapshot`, `fake_file_detector`,
`kad-base`, `known_file_hash_open`, `packets`, `part_file_hash_launch`,
`part_file_majority_name`, `process_launch`, `restart_app`, `search_trust_hint`,
`server_connect`, `server_info`, `standby_prevention`, `startup`, `startup_storage`,
`version_check_launch`, `windows_firewall_repair`.

`fake_file_detector` and `startup` were failing on stale assertions; both were fixed,
re-verified green against a fresh test build, and wired in with the rest.

| Group | Verdict | Notes |
| --- | --- | --- |
| `parity` (859 cases), `web_api` (87), `protocol-parity` (13) | **KEEP** | The 0.7.3 gate backbone. |
| `community-core-divergence` | **KEEP** | Orchestrated by community-core coverage (overnight). |
| The 19 suites above | **WIRED-IN** | Were dormant; verified green; now in `test all`. |
| `divergence` | **KEEP DORMANT** | A deliberate 0.8.0 scheduler-removal guard; red by design until the removal lands. |
| `benchmark`, `pipeline`, `pipeline-benchmark` | **OPTIONAL** | Performance, not correctness; stay targeted-only. |
| `kad-broadband` | **OPTIONAL** | Cases are behind a build flag (0 assertions in the standard build); investigate before gating. |
| Frozen MFC UI suites (`*_keyboard_shortcuts`, `download_progress_bar`, `status_bar`, `pro_user_menu_copy`, `shared_dirs_tree_ctrl`) | **OPTIONAL** | Frozen low-churn UI; targeted-only, out of the tiers. |

## Live-e2e layer

| Group | Verdict | Notes |
| --- | --- | --- |
| Fast set — `preference-ui`, `shared-files-ui`, `config-stability-ui`, `shared-hash-ui`, `startup-diagnostics`, `shared-directories-rest`, `rest-api` (+ `auto-browse-live`) | **KEEP (quick/fast)** | All `stressClass = scenario`. |
| Soak/stress/hammer/chaos + storage (10) | **KEEP (overnight only)** | Already overnight-tier profiles; none leak into quick/fast. |
| `multi-client-p2p` vs `multi-client-p2p-required` | **KEEP (both)** | Same suites, different evidence policy — intentional, not redundant. |
| `shared-directory-browse-stress` | **OPTIONAL (orphan)** | In no profile and not default-enabled; has fixture support. Wire into `stabilization-stress` or remove with its self-test — deferred (needs the long-paths fixture pipeline). |
| `deterministic-two-client-transfer` | **KEEP (review)** | Overlaps `multi-client-p2p-matrix` on local transfer; acceptable as a deterministic baseline. |
| Live-wire ARR (`radarr`/`sonarr`/`prowlarr-emulebb`) | **KEEP (live-wire/release only)** | Forward/controller surface; never quick/fast. |

## Python-harness layer

| Group | Verdict | Notes |
| --- | --- | --- |
| All modules | **KEEP (quick/fast)** | Fast unit tests, no app/network. |
| 56 modules self-testing a live script | **KEEP** | Unit-vs-integration pairing, intentional. When a live suite/script is cut, cut its self-test too (mapping in the catalog `selfTestsScript`). |

## Triage of the failing suites

The failures were diagnosed against the built test binary (the relevant source had not
changed since it was built, so they are real on current source — not stale-binary noise):

- **`divergence` / `scheduler_removal`** — **deliberate, keep dormant.** These are
  compile-time guards (`#if __has_include("Scheduler.h")`, `#ifdef IDS_SCHEDULER`, …) that
  assert the legacy scheduler is *removed*. It is still present, so they are red by design
  until the 0.8.0 legacy-surface removal lands. Correctly excluded from the 0.7.3 gate.
- **`startup` / `app_command_line`** — **stale test, fixed and wired.** The product was
  rebranded to emit "…canonical absolute **eMuleBB** base directory…"
  (`AppCommandLineSeams.h`), but the test still expected "eMule". Updated the expected
  string; a fresh test build confirmed 61/61 and the suite is now in `test all`.
- **`fake_file_detector`** — **stale expectation, fixed and wired.** BUG-150 added
  year-token stripping under broad release metadata, and the operator confirmed `2000` is the
  film's release year, so `Sports Madness 2000 XviD 1080p` correctly canonicalizes to
  `sports madness` (year dropped) while the title divergence is still flagged. Updated the
  assertion to expect `sports madness`; a fresh build confirmed 129/129 and the suite is now
  in `test all`.

## Remaining / deferred

1. **`kad-broadband`** — cases are behind a build flag (0 assertions in the standard build);
   confirm the flag, then wire or document.
2. **`shared-directory-browse-stress`** — wire into `stabilization-stress` or delete with its self-test.
3. **`divergence`** stays dormant by design until the 0.8.0 scheduler removal lands.

Regenerate the catalog after any change with
`python scripts/show-test-inventory.py --markdown` and re-run
`python -m pytest tests/python/test_test_inventory.py`.
