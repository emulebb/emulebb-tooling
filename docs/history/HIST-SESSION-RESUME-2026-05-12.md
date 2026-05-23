# Session Resume

This file is the session-termination handoff for the canonical eMule
workspace. Update it only when ending a work session or when the user
explicitly asks for a current handoff. Do not use it for mid-task planning.
This file is not policy, not backlog authority, and not a substitute for
`EMULE_WORKSPACE_ROOT\repos\emulebb-tooling\docs\WORKSPACE-POLICY.md`.

## Current State

- Date: 2026-05-12.
- Active app worktree: `%EMULE_WORKSPACE_ROOT%\workspaces\v0.72a\app\eMule-main`
  on `main`.
- Supporting repos checked this session:
  - `%EMULE_WORKSPACE_ROOT%\repos\emulebb-tooling` on `main`
  - `%EMULE_WORKSPACE_ROOT%\repos\emulebb-build-tests` on `main`
- App and build-test repos are clean on `main...origin/main`.
- Beta-readiness audit snapshots now live under
  `docs\history\release-0.7.3\audits`.
- Latest app commit:
  `07572d6 CI-024 report shared hashing REST busy state`.
- Latest build-tests commit:
  `641700f CI-024 gate Arr acquisition on shared hashing idle`.

## Completed This Session

- Investigated whether a large shared-folder tree can block REST/Arr live
  tests.
- Confirmed the web listener can still answer cheap routes while native-state
  routes can stall behind UI/native model work.
- Added REST shared-hashing diagnostics:
  - `/api/v1/status` stats now include `sharedHashingCount` and
    `sharedHashingActive`.
  - `/api/v1/shared-directories` uses the same null-safe hashing counter.
- Added a `SERVICE_BUSY` REST error mapping to HTTP `503`.
- Made `/api/v1/transfers` reject while shared hashing is active instead of
  letting transfer snapshots pile up behind a long shared-file scan.
- Added Arr live-test gating so Radarr/Sonarr acquisition waits until
  `sharedHashingCount == 0` after REST startup and after eMule category setup.
- Kept the live-wire policy intact: no movie or series titles were hardcoded.

## Validation References

Completed validation:

- `python -m pytest tests\python\test_radarr_sonarr_emulebb_live.py -q`
  passed: `43 passed`.
- `python -m pytest tests\python\test_rest_api_smoke.py -q` passed:
  `85 passed`.
- `python -m emule_workspace build app --config Release --platform x64
  --build-output-mode ErrorsOnly` passed with `0 warnings`.
- `python -m emule_workspace test all --config Release --platform x64
  --build-output-mode ErrorsOnly` passed with exit code `0`.

## Live-Test Handoff

- A Radarr live rerun was started with:
  `python -m emule_workspace test live-e2e --suite radarr-emulebb --config
  Release --platform x64 --build-output-mode ErrorsOnly
  --live-wire-inputs-file
  %EMULE_WORKSPACE_ROOT%\repos\emulebb-build-tests\live-wire-inputs.local.json
  --fail-fast`.
- The user intentionally interrupted that run after roughly 11 minutes.
- Partial report:
  `%EMULE_WORKSPACE_ROOT%\repos\emulebb-build-tests\reports\radarr-emulebb-live\20260511-235514-eMule-main-release\result.json`.
- Important partial result: the new shared-hashing gates both passed:
  - `shared_hashing_idle_after_rest_ready`: `hashingCount=0`, `idle=true`
  - `shared_hashing_idle_after_category_setup`: `hashingCount=0`, `idle=true`
- The interrupted report ended at `radarr_search_and_grab` with a
  `URLError` connection-refused message after cleanup started. Do not treat
  that interrupted run as a completed acquisition verdict.
- No `emule.exe` process was left running after the interruption. The only
  observed Python processes were unrelated local services:
  `Plex-Auto-Languages` and `qbautom`.

## Next Steps

- Read `repos\emulebb-tooling\docs\WORKSPACE-POLICY.md` before the next
  workspace task.
- Use `python -m emule_workspace` for build, validation, test, and live
  commands.
- Continue with Radarr first, then Sonarr, using logs and
  `%EMULE_WORKSPACE_ROOT%\repos\emulebb-build-tests\.env.local` plus
  `live-wire-inputs.local.json`.
- Treat the shared-hashing question as answered for the latest run:
  hashing was idle, so the next debugging focus is the Radarr/prowlarr
  connection-refused failure during `radarr_search_and_grab`.
