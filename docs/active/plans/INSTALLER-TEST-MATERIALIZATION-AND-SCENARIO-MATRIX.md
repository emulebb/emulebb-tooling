# Installer Test Materialization And Scenario Matrix Plan

This plan tracks the active goal to reuse the packaged eMuleBB suite installer
for local development installs and test materialization, while making the live
E2E scenario structure easier to audit and repeat.

## Goal

Materialize fully configured local and test installs through the suite
installer, then let Python-owned test harness scripts apply scenario-specific
runtime tuning. The installer remains the only PowerShell implementation layer;
test automation stays in Python.

## Boundaries

- `repos\emulebb-build` owns workspace orchestration, package creation, local
  install materialization, and test-install roots.
- `repos\emulebb-build-tests` owns Python scenarios, live-wire input loading,
  profile tuning for tests, scenario registries, and matrix reporting.
- The suite installer owns deployed app layout, suite profile creation,
  packaged scripts, manifests, and PDB placement beside `emulebb.exe`.
- Existing profiles are imported only when the target suite profile does not
  already exist. Refreshing an install must not overwrite or reset an existing
  profile.
- Parallel test runs use isolated roots under
  `state\test-installs\<run-id>\<suite>\<client>` and must not share writable
  profile state.

## Current Landed Slices

1. `emulebb-build`:
   - `3123285 chore: let live e2e use materialized test installs`
   - `a3806a4 fix: keep materialized profile out of synthetic seeds`
2. `emulebb-build-tests`:
   - `c63a05f fix: keep live monitor on materialized profiles`
   - `0d13cd8 fix: separate live monitor profiles from suite seeds`
   - `e1845f5 BUG-130 sync source contract tests`
   - `6cc796e CI-035 expand live scenario matrix report`
3. `emulebb`:
   - `4f7141ed chore: sync release localization layout`
   - `68ef8124 BUG-125 remove pending upload reads by pointer`
4. `emulebb-tooling`:
   - `bb72e0f chore: require EMULEBB workspace root`
   - `aa72bc8 BUG-130 document REST paging query contract`

## Granular Commit Plan

### 1. Installer/Test Materialization Contract

Status: landed.

- Build repo commit: expose `--materialize-test-install` through
  `python -m emule_workspace test live-e2e`.
- Build repo commit: map each test materialization to an isolated
  `state\test-installs` root.
- Build repo commit: preserve installer-owned profile directories and keep PDB
  validation beside the deployed executable.
- Build repo commit: derive a curated `harness-profile-seed\config` from the
  installer-owned profile for Python scenarios, supplementing only missing
  seed files from the checked-in harness seed and filtering runtime cache
  files.
- Test repo commit: point live process monitoring at the materialized profile.
- Test repo commit: keep synthetic seeds and generated throw-away profiles out
  of the suite install profile.

Validation:

- Focused installer/local-package unit tests.
- Materialized `godzilla-local-swarm` launch-scale run.
- CPU-profiled `resource-ui-smoke` run.
- Full build-tests Python suite.

### 2. Profile Import And Refresh Semantics

Status: landed for current local/test path; keep as a regression area.

- Build repo commit: read `import_profile_dir` from ignored live-wire JSON.
- Installer commit: import that profile only when
  `profiles\emulebb\config` does not already exist.
- Build/test commit: reject retired `profile_dir` and `procdump_path` keys so
  the installer remains the profile owner.

Validation:

- Refresh an existing local install twice and confirm profile files are not
  reset.
- Materialize a test install with no profile and confirm initial import happens.
- Materialize another test install with an existing profile and confirm import
  is skipped.

### 3. Scenario Matrix Audit Surface

Status: audit and first ownership cleanup slices landed.

- Test repo commit: generate matrix rollups by network scope, topology, stress
  class, and profile visibility.
- Test repo commit: report repeated profile coverage and classify overlap.
- Test repo commit: report unprofiled/default-only suites and mixed-client
  downgrade risks as explicit gaps.
- Test/build repo commit: add named ownership for default-only UI/startup
  lanes, local controller lanes, live-process diagnostics, required optional
  multi-client proof, and Godzilla launch-scale stabilization coverage.
- Build repo commit: expose the new named profiles through
  `python -m emule_workspace test live-e2e` and cover wrapper forwarding.
- Test repo commit: make Godzilla write `mixed_client_evidence` so runtime
  aMule readiness downgrades are explicit report data, not hidden weakness.

Current matrix findings:

- 40 live E2E suites: 19 offline, 11 LAN, 10 VPN.
- Stress classes: 29 scenario, 3 matrix, 3 smoke, 2 soak, 1 chaos, 1 stress,
  1 hammer.
- Swarm lanes: 3 local swarms plus 1 large Godzilla hammer.
- Named ownership now covers former unowned lanes:
  - `config-stability-ui` and `startup-profile` are in
    `release-expanded` and `release-expanded-quick`.
  - `auto-browse-live` is in full `release-expanded`.
  - `live-process-monitor` is owned by `diagnostics-soak`.
  - `radarr-emulebb-local` and `sonarr-emulebb-local` are owned by
    `controller-local`.
  - `multi-client-p2p-required` runs the same local P2P matrix with optional
    clients required.
  - `godzilla-local-swarm` is visible in `release-expanded` and
    `stabilization-stress` at `launch-scale`.
- The matrix currently reports no open taxonomy gaps; Godzilla runtime reports
  classify aMule participation as `full-mixed-client` or degraded
  `emulebb-harness-only` evidence.

### 4. Remaining Scenario Cleanup Slices

Status: profile ownership, readiness classification, installer-derived seed
forwarding, and runtime proof landed. A shorter quick gate remains an optional
future tuning slice, not a current completion blocker.

- Test repo commit: consider a short `stabilization-stress-quick` Godzilla
  lane only after the `stabilization-stress` launch-scale runtime proof is
  repeatable enough to justify quick-gate cost.

Each slice should update `tests\python\test_scenario_matrix.py`, run
`python -m pytest tests\python\test_scenario_matrix.py -q`, then run the full
build-tests Python suite before pushing.

### 5. Whole-Install Proof Loop

Status: installer-backed smoke, constrained Godzilla, and profiled resource UI
proof passed after the installer-derived seed forwarding slice.

- Installer-backed smoke:
  - Command: `python -m emule_workspace test live-e2e --suite command-line-smoke --test-network offline --materialize-test-install --materialize-test-install-skip-build --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json --startup-trace-mode optional --fail-fast`
  - Report:
    `state\test-reports\live-e2e-suite\20260529T200654Z-live-e2e-suite-release-14208`
  - Result: aggregate `passed`; child `command-line-smoke` `passed`.
  - Install root:
    `state\test-installs\20260529T200401Z-pid12712\live-e2e-suite\main`
  - Evidence: `profileImport.action=imported` from the operator live-wire
    profile path; adjacent `emulebb.pdb` hash matched the package-build PDB;
    derived `harness-profile-seed\config` contained only `nodes.dat`,
    `preferences.dat`, `preferences.ini`, and `server.met`.
- Constrained Godzilla:
  - Command: `python -m emule_workspace test live-e2e --suite godzilla-local-swarm --test-network lan --admin-volume-fixtures --materialize-test-install --materialize-test-install-skip-build --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json --startup-trace-mode optional --fail-fast --godzilla-stage launch-scale --godzilla-total-client-count 4 --godzilla-peer-transfer-count 4 --godzilla-harness-transfer-count 3 --godzilla-emulebb-files 6 --godzilla-extra-emulebb-files 2 --godzilla-harness-files 5 --godzilla-amule-files 2 --godzilla-adverse-kill-cycles 0 --godzilla-adverse-kill-warmup-seconds 0.1 --godzilla-adverse-recovery-timeout-seconds 30 --vhd-size-mb 256`
  - Report:
    `state\test-reports\live-e2e-suite\20260529T201051Z-live-e2e-suite-release-12328`
  - Result: aggregate `passed`; child `godzilla-local-swarm` `passed`.
  - Install root:
    `state\test-installs\20260529T200759Z-pid11952\live-e2e-suite\main`
  - Evidence: child command used the materialized `apps\eMuleBB\emulebb.exe`
    and derived `harness-profile-seed\config`; `mixed_client_evidence`
    recorded degraded `emulebb-harness-only` because aMule EC did not become
    ready, rather than hiding the downgrade.
- Profiled resource UI:
  - Command: `python -m emule_workspace test live-e2e --suite resource-ui-smoke --test-network offline --materialize-test-install --materialize-test-install-skip-build --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json --startup-trace-mode optional --profile-cpu --profile-cpu-stack --profile-cpu-max-file-mb 128 --profile-cpu-stack-min-hits 5 --profile-symbols-required --fail-fast`
  - Report:
    `state\test-reports\live-e2e-suite\20260529T201630Z-live-e2e-suite-release-6700`
  - Result: aggregate `passed`; child `resource-ui-smoke` `passed`; 43
    language probes passed.
  - Install root:
    `state\test-installs\20260529T201338Z-pid14044\live-e2e-suite\main`
  - Evidence: child command used the materialized `apps\eMuleBB\emulebb.exe`
    and derived `harness-profile-seed\config`; adjacent `emulebb.pdb` existed;
    CPU stack summary contained 426 symbolized app rows with `emulebb!`
    function names and a populated local symbol cache.

## Validation Evidence

Latest completed validation before this plan update:

- `python -m pytest tests\python -q`: `945 passed`.
- `python -m pytest -q` in `repos\emulebb-build`: `209 passed`.
- `python -m emule_workspace validate`: passed.
- App Debug and Release x64 builds passed after the app source fix.
