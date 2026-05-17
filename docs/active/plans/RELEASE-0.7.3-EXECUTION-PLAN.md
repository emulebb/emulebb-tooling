# Beta 0.7.3 Execution Plan

This is the only active execution plan for beta `emule-bb-v0.7.3`.
Every actionable release task must have its own item ID.

## Source Decision

- Release source: selected reviewed `main` commit in
  `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\eMule-main`.
- Tag target: the same selected reviewed `main` commit after final proof passes
  and the operator gives a separate tagging instruction.
- Former broadband stabilization branch: retired from the active beta topology.
- Stock/community comparison baseline: `baseline/community-0.72a`.

## Blocking Work

| Order | ID | Owner repo | Required outcome |
|-------|----|------------|------------------|
| 1 | [CI-038](../items/CI-038.md) | build/tests/tooling | Full stock-language `ui-resource-depth` smoke passes on the selected current head before final packaging. |
| 2 | [CI-035](../items/CI-035.md) | build/tests/tooling | Fresh current-head proof and x64/ARM64 core package hashes plus optional aMuTorrent x64 package hash are recorded before tag creation. |

Execution resumed by operator direction on 2026-05-17. Run the proof and
packaging commands in the checklist order, then stop before Git tagging until
the operator gives a separate tag instruction.

## Non-Blocking Follow-Up

- [CI-034](../../history/items/CI-034.md) is closed; `package-release` now
  rejects dirty provenance inputs and records selected source/build/test/tooling
  commits in package manifests.
- [BUG-102](../../history/items/BUG-102.md) is closed; the dedicated
  aMuTorrent browser smoke passed on current `main` with generated harness port
  and isolated state coverage.
- [CI-037](../items/CI-037.md) is passed; the expanded weak-path live profile
  remains release evidence unless a later candidate change invalidates it.
- [BUG-111](../../history/items/BUG-111.md) is closed; app release, update,
  and help URLs now point at `emulebb` destinations with focused update-check
  coverage.
- [FEAT-056](../items/FEAT-056.md) owns post-beta proof automation and operator
  evidence UX. Do not block beta `0.7.3` on it unless a later release decision
  promotes a specific slice into a new beta-blocking item ID.
- [BUG-112](../../history/items/BUG-112.md) is Wont-Fix for beta `0.7.3`;
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

- Docs-only changes: `git diff --check` in `repos\eMule-tooling` and
  `python -m emule_workspace validate`.
- App blockers: `validate`, focused tests for the touched area, and Release x64
  app build when behavior or resources change.
- Build/package blockers: `validate`, package-focused tests when available, and
  x64 plus ARM64 package rehearsal.
- Final proof: the command set in
  [RELEASE-0.7.3-CHECKLIST](../RELEASE-0.7.3-CHECKLIST.md).
