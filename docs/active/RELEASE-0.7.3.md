# eMule Broadband Edition 0.7.3 Release Train Dashboard

This is the current release-train dashboard for the fixed 0.7.3 candidate
sequence. RC1 is frozen historical evidence. Active release testing, bugfixes,
and improvements now target RC2 and later candidates. Use this document for
status, release-source truth, and the open RC task list.

## Current Status

- Status: RC1 evidence is frozen; RC2+ test-gate rationalization is active.
  Operator tag instruction is still pending and no tag should be created.
- Target publication window: blocked until `CI-035` quick proof,
  package/SBOM/hash confirmation, clean-worktree confirmation, successful push
  of pending build commit `fb6e286`, `CI-052` RC2+ test-gate rationalization,
  and the separate operator tag instruction.
- Proof status: release proof resumed by operator direction on 2026-05-17.
  On 2026-06-05 the quick campaign was reduced to the repeatable RC gate:
  Hyper-V VM proof is now on-demand/nonblocking and `live-process-monitor` is
  isolated behind the `installer-controller-surface-soak` profile. The latest
  dry-run planned `18/18` commands. The latest execute run completed `18/18`
  commands with `--continue-on-failure` but failed while outbound HTTPS/public
  network access was unavailable (`WinError 10051` against GitHub, nodejs.org,
  public seed refresh, and REST probes). Candidate x64, ARM64, diagnostics,
  and optional aMuTorrent x64 packages were regenerated during that failed run
  and are recorded in [CI-035](items/CI-035.md).
- Release freeze: active. No new feature, refactor, UI polish, warning-debt, or
  roadmap work enters RC2+ unless it is a direct release-gate blocker, package
  or proof fix, approved regression fix, or release-documentation correction.
- Current hold: none for release proof. Continue one gate at a time and stop
  before Git tagging until the operator gives the separate RC tag instruction.
- Release source: selected reviewed `main` commit in
  `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main`.
- Tag target: the active RC2+ candidate on the selected reviewed `main` commit
  after fresh proof passes and the operator gives a separate tagging
  instruction.
- Stock/community comparison baseline: `baseline/community-0.72a`.
- Release stabilization branch: `release/0.7.3` once the operator starts the
  0.7.3 RC branch.
- Package publication: held until the quick release-campaign proof passes or is
  explicitly accepted, final checklist rows are confirmed, and the operator
  gives the separate tag/publication instruction.

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

## Candidate Structure

This structure keeps RC evidence separate from future-roadmap planning. Fill
only the active candidate section during release execution; frozen candidate
sections are historical scaffolds.

### RC1 Frozen Gate

Purpose:
preserve historical evidence from the first candidate. RC1 is no longer an
active test-compatibility or bugfix target.

Allowed changes:
none. Any further bugfix, test campaign change, packaging improvement, or proof
refresh goes to RC2+.

Historical task:
[CI-035](items/CI-035.md).

Evidence owner:
[RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) plus the artifact and
hash records in `CI-035`.

### RC2+ Active Gate

Purpose:
absorb only the delta from frozen RC1 evidence and rationalize release proof
around installer-backed, reusable local/VM campaign scenarios.

Allowed changes:
release blockers reported from RC1, proof refreshes invalidated by those
changes, packaging fixes, release-documentation corrections, and approved
regression fixes. Campaign modules and schemas may evolve for RC2+ without
preserving RC1 command compatibility.

Required scaffold before RC2 work starts:

- identify the RC1 evidence that carries forward unchanged;
- list every RC1 artifact, proof row, or hash invalidated by the RC2 delta;
- create or promote item IDs for every RC2 blocker;
- record the exact package and SBOM regeneration scope;
- keep all future-roadmap and `0.8.0` removal work out of RC2 unless it fixes a
  direct release blocker on a supported surface;
- make the packaged PowerShell suite installer the default starting point for
  release-relevant local/live tests;
- keep local host and VM campaign scenarios mostly paritetic, with VM proof
  nonblocking unless a package/installer delta invalidates guest evidence.

### RC3 Delta Gate

Purpose:
absorb only final release-candidate corrections after RC2. RC3 should be
smaller than RC2 and should not reopen product scope.

Required scaffold before RC3 work starts:

- identify RC2 evidence that carries forward unchanged;
- list every proof or artifact invalidated by the RC3 delta;
- record any explicit operator acceptance for proof that cannot be rerun;
- confirm stable `0.7.3` documentation can be produced from the RC3 state.

### Stable 0.7.3 Closeout

Purpose:
turn the accepted RC state into stable `emulebb-v0.7.3`.

Required scaffold before stable tagging:

- stable release notes derived from the accepted RC notes;
- package names changed from `0.7.3-rc.N` to `0.7.3`;
- final package, manifest, SBOM, and hash evidence;
- branch split confirmation for `release/0.7.x` legacy maintenance and `main`
  opening for `0.8.0` frozen-surface removal.

## Historical RC1 Release Identity

This block records the frozen RC1 asset shape. RC2+ package names and hashes
must be regenerated from the active RC2+ gate rather than inferred from this
historical list.

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

| ID | Priority | Area |
|----|----------|------|
| [CI-035](items/CI-035.md) | Major | Final proof |
| [CI-052](items/CI-052.md) | Major | RC2+ installer-backed test gate |

Required outcome:
restore public network connectivity, push pending build commit `fb6e286`, rerun
the quick aggregate campaign against the RC2+ installer-backed gate, confirm or
regenerate package hashes, rerun the clean-worktree audit, then wait for the
operator-controlled tag instruction.

## Remaining Release Backlog

The 0.7.3 RC2+ backlog is narrowed to `CI-035` and `CI-052`. `CI-038` is Done with a
current-head `ui-resource-depth` pass covering all 43 release languages. The
latest quick campaign dry-run reports the intended 18-command RC gate with VM
proof on-demand. Candidate x64/ARM64 core package hashes, package SBOM hashes,
and optional aMuTorrent x64 hashes are recorded, but the aggregate quick proof
failed under public-network outage conditions. Remaining work is network
restoration, push of `fb6e286`, quick release-campaign proof or explicit
acceptance, RC2+ installer-backed campaign rationalization, final checklist
confirmation, clean-worktree audit, and the later operator-controlled tag
instruction.

All other active `FEAT`, `REF`, warning-debt, cleanup, and polish items are
post-0.7.3 by default. A non-blocking item may enter RC2+ only if a current
release gate exposes a direct blocker and the item doc records that promotion
explicitly.

`FEAT-056` remains post-`0.7.3` automation and evidence UX work. It is not an RC
tag blocker unless a later item promotes a specific slice.

Historical accepted non-blockers for 0.7.3 RC1:

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

0.7.3 RC2+ can be tagged only when:

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
