# RC 0.7.3 Execution Plan

This is the only active execution plan for RC `emulebb-v0.7.3-rc.1`.
Every actionable release task must have its own item ID.

## Release Freeze

- Freeze status: active.
- No new feature, refactor, UI polish, warning-debt, dependency refresh, or
  roadmap work may enter RC `0.7.3`.
- Allowed pre-tag changes are limited to direct release-gate blockers,
  packaging/provenance failures, release-doc drift, or severe app defects found
  by the required release proof.
- Current operator hold: do not run eMule tests or edit eMule test/harness
  files. Keep `CI-035` and `CI-038` open until test work resumes and fresh
  current-head proof is recorded.

## Source Decision

- Release source: selected reviewed `main` commit in
  `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\eMule-main`.
- Tag target: the same selected reviewed `main` commit after final proof passes
  and the operator gives a separate tagging instruction.
- Release stabilization branch: `release/0.7.3` once the operator starts the
  RC branch.
- Stock/community comparison baseline: `baseline/community-0.72a`.

## Blocking Work

| Order | ID | Owner repo | Required outcome |
|-------|----|------------|------------------|
| 1 | [CI-038](../items/CI-038.md) | build/tests/tooling | Full stock-language `ui-resource-depth` smoke passes on the selected current head before final packaging. |
| 2 | [CI-035](../items/CI-035.md) | build/tests/tooling | Fresh current-head proof and x64/ARM64 core package hashes plus optional aMuTorrent x64 package hash are recorded before tag creation. |

Execution resumed by operator direction on 2026-05-17. Run the proof and
packaging commands in the checklist order, then stop before Git tagging until
the operator gives a separate tag instruction.

## Known Deferred Proof Gaps

- `CI-038`: latest observed `resource-ui-smoke` artifact failed before full
  language proof because `resource-ui-smoke.py` referenced
  `emule_live_profile_common.prepare_scenario_profile`, which is not exported
  by the current helper module. Do not fix while the test/harness hold is
  active.
- `CI-035`: latest observed fast certification artifact failed, the latest
  overnight artifact was not final release evidence, and final package hashes
  must be regenerated from the selected heads after proof passes.
- Controller/live rows that depend on Radarr, Sonarr, or live-wire inputs must
  be rerun later with operator-owned local inputs and explicit Arr roots.

## Non-Blocking Follow-Up

- [CI-034](../../history/items/CI-034.md) is closed; `package-release` now
  rejects dirty provenance inputs and records selected source/build/test/tooling
  commits in package manifests.
- [BUG-102](../../history/items/BUG-102.md) is closed; the dedicated
  aMuTorrent browser smoke passed on current `main` with generated harness port
  and isolated state coverage.
- [CI-037](../../history/items/CI-037.md) is passed; the expanded weak-path live profile
  remains release evidence unless a later candidate change invalidates it.
- [BUG-111](../../history/items/BUG-111.md) is closed; app release, update,
  and help URLs now point at `emulebb` destinations with focused update-check
  coverage.
- [FEAT-056](../items/FEAT-056.md) owns post-`0.7.3` proof automation and
  operator evidence UX. Do not block RC `0.7.3` on it unless a later release
  decision promotes a specific slice into a new RC-blocking item ID.
- [BUG-112](../../history/items/BUG-112.md) is Wont-Fix for RC `0.7.3`;
  legacy WebServer/qBit-compatible session-token hardening is not release
  scope.
- [REF-034](../items/REF-034.md) is deferred; the Crypto++ 8.9 refresh is
  post-beta dependency hardening.
- The IP-filter HTTP update transport finding in
  [BETA-READINESS-SECURITY-2026-05-11](../../history/release-0.7.3/audits/BETA-READINESS-SECURITY-2026-05-11.md)
  is accepted as not release scope.

## Historical Inputs

The following are provenance, not current execution owners:

- `docs\history\release-0.7.3\RELEASE-0.7.3-GATE-HISTORY.md`
- superseded release cluster plans under `docs\history\release-0.7.3`
- 2026-05-11 beta readiness audits under
  `docs\history\release-0.7.3\audits`

## Validation Bar

- Docs-only changes while the test hold is active: `git diff --check` in
  `repos\emulebb-tooling` plus documentation taxonomy checks only. Do not run
  eMule test commands.
- App blockers: `validate`, focused checks for the touched area when the hold
  is lifted, and both active x64 app builds when behavior or resources change:
  Debug x64 and Release x64 through the supported workspace entrypoint.
- Build/package blockers: `validate`, package-focused tests when available, and
  x64 plus ARM64 package rehearsal.
- Final proof: the command set in
  [RELEASE-0.7.3-CHECKLIST](../RELEASE-0.7.3-CHECKLIST.md).
