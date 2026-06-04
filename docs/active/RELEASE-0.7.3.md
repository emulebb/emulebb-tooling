# eMule Broadband Edition 0.7.3 RC1 Release Dashboard

This is the current release dashboard for the 0.7.3 RC1 target
`emulebb-v0.7.3-rc.1`.
Use it for status, release-source truth, and the open RC task list.

## Current Status

- Status: Installer-controller VM proof passed; final release-campaign proof
  and operator tag instruction still pending.
- Target publication window: 2026-06-03, contingent on `CI-035` proof,
  package/SBOM/hash recording, clean-worktree confirmation, and the separate
  operator tag instruction.
- Proof status: release proof resumed by operator direction on 2026-05-17.
  The 2026-06-04 installer-controller VM proof passed on Win10 and Win11 with
  fresh x64, ARM64, and optional aMuTorrent x64 package hashes recorded in
  [CI-035](items/CI-035.md). GitHub controlled smoke run `26959062075` passed
  both x64 and ARM64 package smoke lanes. Git tagging still requires a later
  separate operator instruction.
- Release freeze: active. No new feature, refactor, UI polish, warning-debt, or
  roadmap work enters 0.7.3 RC1; only direct release-gate blockers may be
  fixed before the tag.
- Current hold: none for release proof. Continue one gate at a time and stop
  before Git tagging until the operator gives the separate RC tag instruction.
- Release source: selected reviewed `main` commit in
  `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main`.
- Tag target: `emulebb-v0.7.3-rc.1` on the selected reviewed `main` commit after
  fresh proof passes and the operator gives a separate tagging instruction.
- Stock/community comparison baseline: `baseline/community-0.72a`.
- Release stabilization branch: `release/0.7.3` once the operator starts the
  0.7.3 RC1 branch.
- Package publication: held until the remaining quick release-campaign proof is
  run or explicitly accepted, final checklist rows are confirmed, and the
  operator gives the separate tag/publication instruction.

## Release Train

The public `0.7.3` candidate train is fixed:

1. `emulebb-v0.7.3-rc.1`
2. `emulebb-v0.7.3-rc.2`
3. `emulebb-v0.7.3-rc.3`
4. `emulebb-v0.7.3`

Each RC absorbs only release blockers, proof refreshes, packaging fixes, and
approved regression fixes. After stable `0.7.3`, `main` opens for `0.8.0`
surface-removal work and `release/0.7.x` carries legacy support for the frozen
`0.7.x` public surface.

## Release Identity

- Public product name: `eMule broadband edition`
- Compact app/mod/API name: `eMuleBB`
- GitHub organization and URL slug: `emulebb`
- Tag: `emulebb-v0.7.3-rc.1`
- Assets:
  - `Bootstrap-eMuleBBSuite.ps1`
  - `Bootstrap-eMuleBBSuite.ps1.sha256`
  - `emulebb-0.7.3-rc.1-x64.zip`
  - `emulebb-0.7.3-rc.1-x64.manifest.json`
  - `emulebb-0.7.3-rc.1-x64.sbom.spdx.json`
  - `emulebb-0.7.3-rc.1-arm64.zip`
  - `emulebb-0.7.3-rc.1-arm64.manifest.json`
  - `emulebb-0.7.3-rc.1-arm64.sbom.spdx.json`
  - optional controller asset:
    `emulebb-0.7.3-rc.1-amutorrent-x64.zip`
  - optional controller manifest:
    `emulebb-0.7.3-rc.1-amutorrent-x64.manifest.json`
  - optional controller SBOM:
    `emulebb-0.7.3-rc.1-amutorrent-x64.sbom.spdx.json`

## Active Control Docs

- [Execution plan](plans/RELEASE-0.7.3-EXECUTION-PLAN.md)
- [Operator checklist](RELEASE-0.7.3-CHECKLIST.md)
- [Operator runbook](RELEASE-0.7.3-RUNBOOK.md)
- [Release test campaigns](RELEASE-TEST-CAMPAIGNS.md)
- [Controller surface matrix](CONTROLLER-SURFACE-MATRIX.md)

Historical gate evidence and superseded cluster plans live under
`docs\history\release-0.7.3`. Release audit provenance lives under
`docs\history\release-0.7.3\audits`.

## Open RC Tasks

| ID | Priority | Area | Required outcome |
|----|----------|------|------------------|
| [CI-035](items/CI-035.md) | Major | Final proof | Fresh x64/ARM64 core package hashes plus optional aMuTorrent x64 hash are recorded; remaining quick release-campaign proof, checklist confirmation, and operator-controlled tag instruction are still open. |

## Remaining Release Backlog

The 0.7.3 RC1 backlog is narrowed to `CI-035`. `CI-038` is Done with a
current-head `ui-resource-depth` pass covering all 43 release languages. Fresh
x64/ARM64 core package hashes, package SBOM hashes, optional aMuTorrent x64
hashes, the installer-controller VM proof, and the GitHub x64/ARM64 controlled
smoke pass are recorded. Remaining work is the quick release-campaign proof or
explicit acceptance, final checklist confirmation, clean-worktree confirmation,
and the later operator-controlled tag instruction.

All other active `FEAT`, `REF`, warning-debt, cleanup, and polish items are
post-0.7.3 RC1 by default. A non-blocking item may enter RC1 only if a
current release gate exposes a direct blocker and the item doc records that
promotion explicitly.

`FEAT-056` remains post-`0.7.3` automation and evidence UX work. It is not an RC
tag blocker unless a later item promotes a specific slice.

Accepted non-blockers for 0.7.3 RC1:

- [CI-034](../history/items/CI-034.md): package-release now rejects dirty
  provenance inputs and records selected `main` source/build/test/tooling
  commits in package manifests.
- [CI-037](../history/items/CI-037.md): the expanded weak-path live profile is supported
  and has passed with `100/100` required REST live download triggers; cite it as
  evidence unless a later release-candidate change invalidates it.
- [BUG-102](../history/items/BUG-102.md): aMuTorrent browser smoke now uses
  generated harness ports with isolated state and passed on current `main`.
- [BUG-111](../history/items/BUG-111.md): release, update, and help URLs now
  use the policy-owned `emulebb` namespace.
- [BUG-112](../history/items/BUG-112.md): legacy WebServer/qBit-compatible
  session-token hardening is Wont-Fix for this RC.
- [FEAT-057](../history/items/FEAT-057.md): qBittorrent-style download
  shortcuts and batch menu actions landed as user-facing polish; it does not
  change the final proof/package/tag gates.
- [FEAT-058](../history/items/FEAT-058.md): final closeout copy/audit polish
  aligned release-facing docs with the 0.7.3 RC1 source rule; it resets the
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
- [FEAT-071](../history/items/FEAT-071.md): remote filename intake now repairs
  conservative Western mojibake and bounded HTML/XML entities before existing
  filename cleanup; it resets the app/build-tests/tooling candidate heads but
  does not replace fresh proof or package hashes.
- [REF-034](items/REF-034.md): Crypto++ 8.9 dependency refresh is deferred
  post-`0.7.3`.
- IP-filter HTTP update transport from
  [BETA-READINESS-SECURITY-2026-05-11](../history/release-0.7.3/audits/BETA-READINESS-SECURITY-2026-05-11.md)
  is accepted as not release scope.

## Ship Rule

0.7.3 RC1 can be tagged only when:

- every row in **Open RC Tasks** is Done or explicitly accepted in its item
  doc;
- [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) records fresh command,
  artifact, commit, and package evidence;
- no active workspace repo has unrelated uncommitted changes; and
- the operator gives a separate tagging instruction.

The accepted `FEAT-058`, `FEAT-059`, `FEAT-060`, `FEAT-061`, and `FEAT-071`
closeout hardening changed release-facing documentation, app UI, app REST
metadata, build-test guardrails, and remote filename intake after the previous
prep audit. Final proof must target the pushed heads that exist after this
polish and hardening lands.
