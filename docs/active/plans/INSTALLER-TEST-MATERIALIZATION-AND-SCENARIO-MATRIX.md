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

Status: first audit slice landed.

- Test repo commit: generate matrix rollups by network scope, topology, stress
  class, and profile visibility.
- Test repo commit: report repeated profile coverage and classify overlap.
- Test repo commit: report unprofiled/default-only suites and mixed-client
  downgrade risks as explicit gaps.

Current matrix findings:

- 40 live E2E suites: 19 offline, 11 LAN, 10 VPN.
- Stress classes: 29 scenario, 3 matrix, 3 smoke, 2 soak, 1 chaos, 1 stress,
  1 hammer.
- Swarm lanes: 3 local swarms plus 1 large Godzilla hammer.
- Named gaps now visible:
  - `config-stability-ui`, `startup-profile`, and `auto-browse-live` are
    default aggregate only.
  - `live-process-monitor`, `radarr-emulebb-local`, and
    `sonarr-emulebb-local` are neither default-enabled nor profile-visible.
  - `godzilla-local-swarm` is release-expanded only, not
    stabilization-stress visible.
  - mixed-client optional/readiness policy can weaken
    `multi-client-p2p-matrix` and Godzilla evidence.

### 4. Remaining Scenario Cleanup Slices

Status: next work.

- Test repo commit: decide named-profile ownership for default-only suites.
  Candidate: add `config-stability-ui` and `startup-profile` to
  `release-expanded-quick`; keep `auto-browse-live` in full
  `release-expanded` only unless live-wire runtime cost is acceptable.
- Test repo commit: add a dedicated diagnostics profile or include
  `live-process-monitor` in `stabilization-stress` when explicitly requested
  with real-profile inputs.
- Test repo commit: split local controller lanes from public-network controller
  lanes so `radarr-emulebb-local` and `sonarr-emulebb-local` have visible
  ownership without pretending to be public live-wire proof.
- Test repo commit: add a required optional-client mode profile for
  `multi-client-p2p-matrix`, separate from the current opportunistic profile.
- Test repo commit: decide whether Godzilla belongs in
  `stabilization-stress-quick` as `launch-scale`, or remains release-expanded
  only with a documented runtime exception.

Each slice should update `tests\python\test_scenario_matrix.py`, run
`python -m pytest tests\python\test_scenario_matrix.py -q`, then run the full
build-tests Python suite before pushing.

### 5. Whole-Install Proof Loop

Status: repeat after the scenario ownership changes.

- Run the installer-backed test path with `--materialize-test-install`.
- Run constrained Godzilla launch-scale through that install.
- Run one profiled UI/resource scenario and confirm symbols are found beside
  `emulebb.exe`.
- Run `python -m emule_workspace validate`.

## Validation Evidence

Latest completed validation before this plan update:

- `python -m pytest tests\python -q`: `940 passed`.
- `python -m emule_workspace validate`: passed.
- App Debug and Release x64 builds passed after the app source fix.
