# eMule Broadband Edition 0.7.3 Beta Release Dashboard

This is the current release dashboard for beta target `emule-bb-v0.7.3`.
Use it for status, release-source truth, and the open beta task list.

## Current Status

- Status: Final proof in progress.
- Proof status: release proof resumed by operator direction on 2026-05-17.
  Live proof, package refresh, and evidence recording are active; Git tagging
  still requires a later separate operator instruction.
- Release source: selected reviewed `main` commit in
  `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\eMule-main`.
- Tag target: `emule-bb-v0.7.3` on the selected reviewed `main` commit after
  fresh proof passes and the operator gives a separate tagging instruction.
- Stock/community comparison baseline: `baseline/community-0.72a`.
- Former broadband stabilization branch: retired from the active beta topology.
- Package publication: held until all beta-blocking item IDs below are closed
  or explicitly accepted, final proof passes, and fresh packages are generated.

## Release Identity

- Public product name: `eMule broadband edition`
- Compact app/mod/API name: `eMule BB`
- GitHub organization and URL slug: `emulebb`
- Tag: `emule-bb-v0.7.3`
- Assets:
  - `eMule-broadband-0.7.3-x64.zip`
  - `eMule-broadband-0.7.3-arm64.zip`
  - optional controller asset:
    `eMule-broadband-0.7.3-amutorrent-x64.zip`

Superseded `1.0.0`, `1.0.1`, and `1.1.1` labels are internal evidence only.
Do not publish GitHub releases or package assets for those labels.

## Active Control Docs

- [Execution plan](plans/RELEASE-0.7.3-EXECUTION-PLAN.md)
- [Operator checklist](RELEASE-0.7.3-CHECKLIST.md)
- [Operator runbook](RELEASE-0.7.3-RUNBOOK.md)
- [Controller surface matrix](CONTROLLER-SURFACE-MATRIX.md)

Historical gate evidence and superseded cluster plans live under
`docs\history\release-0.7.3`. Release audit provenance lives under
`docs\history\release-0.7.3\audits`.

## Open Beta Tasks

| ID | Priority | Area | Required outcome |
|----|----------|------|------------------|
| [CI-038](items/CI-038.md) | Major | Language/resource proof | Current-head `ui-resource-depth` release-scope language smoke passes for the full stock language set. |
| [CI-035](items/CI-035.md) | Major | Final proof | Current-head beta proof passes and fresh x64/ARM64 core package hashes plus optional aMuTorrent x64 hash are recorded. |

## Remaining Release Backlog

The beta backlog is narrowed to `CI-038` and `CI-035`. Remaining work is the
release-scope language/resource live gate, final certification proof, fresh
x64/ARM64 core package regeneration, optional aMuTorrent x64 package
regeneration, hash recording, clean-worktree confirmation, and the later
operator-controlled tag instruction.

`FEAT-056` remains post-beta automation and evidence UX work. It is not a beta
tag blocker unless a later item promotes a specific slice.

Accepted non-blockers for beta `0.7.3`:

- [CI-034](../history/items/CI-034.md): package-release now rejects dirty
  provenance inputs and records selected `main` source/build/test/tooling
  commits in package manifests.
- [CI-037](items/CI-037.md): the expanded weak-path live profile is supported
  and has passed with `100/100` required REST live download triggers; cite it as
  evidence unless a later release-candidate change invalidates it.
- [BUG-102](../history/items/BUG-102.md): aMuTorrent browser smoke now uses
  generated harness ports with isolated state and passed on current `main`.
- [BUG-111](../history/items/BUG-111.md): release, update, and help URLs now
  use the policy-owned `emulebb` namespace.
- [BUG-112](../history/items/BUG-112.md): legacy WebServer/qBit-compatible
  session-token hardening is Wont-Fix for this beta.
- [FEAT-057](../history/items/FEAT-057.md): qBittorrent-style download
  shortcuts and batch menu actions landed as user-facing polish; it does not
  change the final proof/package/tag gates.
- [FEAT-058](../history/items/FEAT-058.md): final closeout copy/audit polish
  aligned release-facing docs with the beta `0.7.3` source rule; it resets the
  candidate head but does not replace fresh proof or package hashes.
- [FEAT-059](../history/items/FEAT-059.md): Display preferences now keep
  `Always show tray icon` adjacent to `Minimize to system tray`; it resets the
  candidate head but does not replace fresh proof or package hashes.
- [FEAT-060](../history/items/FEAT-060.md): preference INI keys are now covered
  by a machine-readable inventory and REST mutable preference metadata is
  centralized; it resets the candidate heads but does not replace fresh proof or
  package hashes.
- [FEAT-061](../history/items/FEAT-061.md): a strong section-qualified
  preference schema now validates storage uniqueness, REST bindings, and
  Preferences UI source bindings; it resets the build-tests/tooling candidate
  heads but does not replace fresh proof or package hashes.
- [REF-034](items/REF-034.md): Crypto++ 8.9 dependency refresh is deferred
  post-beta.
- IP-filter HTTP update transport from
  [BETA-READINESS-SECURITY-2026-05-11](../history/release-0.7.3/audits/BETA-READINESS-SECURITY-2026-05-11.md)
  is accepted as not release scope.

## Ship Rule

Beta `0.7.3` can be tagged only when:

- every row in **Open Beta Tasks** is Done or explicitly accepted in its item
  doc;
- [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) records fresh command,
  artifact, commit, and package evidence;
- no active workspace repo has unrelated uncommitted changes; and
- the operator gives a separate tagging instruction.

The accepted `FEAT-058`, `FEAT-059`, `FEAT-060`, and `FEAT-061` closeout
hardening changed release-facing documentation, app UI, app REST metadata, and
build-test guardrails after the previous prep audit. Final proof must target
the pushed heads that exist after this polish and hardening lands.
