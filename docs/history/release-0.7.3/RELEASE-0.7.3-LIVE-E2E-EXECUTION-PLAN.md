# Beta 0.7.3 Live E2E Execution Plan

> Historical release plan only. Current beta `0.7.3` execution is controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

This is the active execution plan for the Release 1 live E2E umbrella. It does
not own gate status; use [RELEASE-0.7.3](RELEASE-0.7.3-GATE-HISTORY.md) for release decisions
and [CI-011](../items/CI-011.md) for completion evidence.

Current status: the 2026-05-09 full Release x64 live lane passed with
`auto-browse-live` accepted as inconclusive because the live networks connected
but no safe downloadable browse-capable sourced transfer was available. Do not
tag or package until the release checklist and clean-worktree gate are complete.

## Decisions

- [CI-011](../items/CI-011.md) owns the operator-facing aggregate command and result
  artifact shape.
- The final release proof is the full Release x64 `live-e2e` run, not a set of
  focused diagnostic runs.
- Focused `live-e2e` suites are valid for diagnosis and gate repair, but they
  do not replace the final aggregate proof.
- Public-network failures may be accepted as inconclusive only when the child
  report proves that the app and harness behaved correctly.
- The live lane must use isolated temp profiles and must not depend on the
  operator's normal eMule profile state.

## Gate Map

| Area | Release item | Execution responsibility |
|------|--------------|--------------------------|
| Aggregate release lane | [CI-011](../items/CI-011.md) | one supported command, stable suite selection, and aggregate result artifact |
| REST robustness | [BUG-075](../items/BUG-075.md), [BUG-076](../items/BUG-076.md), [BUG-077](../items/BUG-077.md), [CI-014](../items/CI-014.md), [CI-015](../items/CI-015.md) | included through the `rest-api` suite |
| Controller integrations | [AMUT-001](../items/AMUT-001.md), [ARR-001](../items/ARR-001.md) | included through aMuTorrent and Arr live suites |
| Release identity | [RELEASE-0.7.3-CHECKLIST](../../active/RELEASE-0.7.3-CHECKLIST.md) | final operator evidence and artifact naming checks |

## Required Aggregate Suites

The final aggregate run must include:

- `preference-ui`
- `shared-files-ui`
- `config-stability-ui`
- `shared-hash-ui`
- `startup-profile`
- `shared-directories-rest`
- `rest-api`
- `amutorrent-browser-smoke`
- `prowlarr-emulebb`
- `radarr-sonarr-emulebb`
- `auto-browse-live`

## Result Rules

- No release-blocking suite may have status `failed`.
- `passed` is required for deterministic local suites.
- `inconclusive` is acceptable only for live-network proof where diagnostics
  distinguish unavailable external conditions from product or harness failure.
- The aggregate artifact must record status, command line, timings, suite
  result paths, and failure phase for failed or inconclusive child suites.
- Reports must redact API keys and exact live-wire transfer identifiers.

## Revalidation Path

Before Release 1 tagging, run:

```powershell
python -m emule_workspace validate
python -m emule_workspace test live-e2e --config Release --platform x64
```

Record the aggregate result path and any accepted inconclusive external
condition in [CI-011](../items/CI-011.md) and
[RELEASE-0.7.3-CHECKLIST](../../active/RELEASE-0.7.3-CHECKLIST.md).

## Latest Revalidation

- `python -m emule_workspace test live-e2e --config Release
  --platform x64`
- Artifact:
  `repos\emulebb-build-tests\reports\live-e2e-suite\20260509-093500-eMule-main-release\result.json`
- Aggregate status: `passed`; `has_inconclusive_suites=true`.
- Deterministic suites and controller suites passed:
  `preference-ui`, `shared-files-ui`, `config-stability-ui`,
  `shared-hash-ui`, `startup-profile`, `shared-directories-rest`,
  `rest-api`, `amutorrent-browser-smoke`, `prowlarr-emulebb`,
  `radarr-sonarr-emulebb`.
- `auto-browse-live` returned the documented inconclusive code `2` with
  `LiveSourceUnavailableError`; the child report records normal cleanup and no
  product or harness failure.
