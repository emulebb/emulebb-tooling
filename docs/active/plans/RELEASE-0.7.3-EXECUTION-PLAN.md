# 0.7.3 Release Execution Plan

Stable `emulebb-v0.7.3` is published. This plan is retained as the release
execution record for the 0.7.3 train; every actionable release task had its own
item ID.

## Release Freeze

- Freeze status: closed for `0.7.3` final.
- No new feature, refactor, UI polish, warning-debt, dependency refresh, or
  roadmap work may enter the published `0.7.x` line unless it is an approved
  compatibility-preserving maintenance fix.
- Stable publication, package hashes, and release evidence are complete.
- Current operator hold: none for `0.7.3`.

## Source Decision

- Release source: selected reviewed `main` commit
  `9402251c2dc986dfc2346e5c80046e22d5c7e3d6` in
  `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main`.
- Tag target: stable `emulebb-v0.7.3` published from the selected reviewed
  commit after the operator's 2026-07-05 ship instruction and waiver.
- Release maintenance branch: `release/0.7.x` carries legacy maintenance after
  stable `0.7.3`.
- Stock/community comparison baseline: `baseline/community-0.72a`.

## Blocking Work

None. [CI-035](../../history/items/CI-035.md) is closed by stable `0.7.3` publication,
published package hashes, and the explicit 2026-07-05 operator waiver for the
remaining stable live, soak, and Windows-VM proof rows.

## Known Deferred Proof Gaps

- `CI-038` is Done. The 2026-05-23 current-head `ui-resource-depth` run passed
  `resource-ui-smoke` for all 43 release languages and passed the Preferences
  companion.
- `CI-035`: final stable package hashes are recorded from the published GitHub
  release assets. Remaining stable live, soak, and Windows-VM proof rows were
  waived by the operator on 2026-07-05.
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
  operator evidence UX.
- [BUG-112](../../history/items/BUG-112.md) is Wont-Fix for 0.7.3;
  legacy WebServer/qBit-compatible session-token hardening is not release
  scope.
- [REF-034](../items/REF-034.md) is deferred; the Crypto++ 8.9 refresh is
  post-0.7.3 dependency hardening.
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
