# eMule Broadband Edition 0.7.3 Release Train Dashboard

This is the current release-train dashboard for the fixed 0.7.3 candidate
sequence. RC1 is frozen historical evidence. Active release testing, bugfixes,
and improvements now target RC2 and later candidates. Use this document for
status, release-source truth, and the open RC task list.

## Current Status

- Status: RC2 is PUBLISHED. The annotated tag `emulebb-v0.7.3-rc.2` peels to app
  `38827709`; GitHub prerelease at
  <https://github.com/emulebb/emulebb/releases/tag/emulebb-v0.7.3-rc.2>, built by
  the `Publish release` workflow after the relaxed-gate fast certification passed
  for the shipped scope. The first publish (2026-06-12T20:48:22Z) shipped BUG-017
  — the `irm | iex` one-liner install failed on an optional `-UiLanguage`
  ValidateSet without a valid default — so that release/tag were deleted and rc.2
  was rebuilt with the fix (`emulebb-build` `0fceae7`) and re-published
  2026-06-12T21:36:15Z; the published bootstrapper is verified to bind under
  `irm | iex`. The RC2 delta over RC1 is installer/bootstrapper
  correctness, an aMuTorrent controller refresh, broadband upload-queue tuning
  (FEAT-015) and diagnostics flush (FEAT-027), and the GPL-2.0 relicense; the
  protocol surface and package shape are unchanged from RC1 except as recorded in
  the [RC2 changelog](RELEASE-0.7.3-RC2-CHANGELOG.md). Final published artifact
  SHA-256 hashes are recorded in [CI-035](items/CI-035.md).
- Next milestone: **rc.3** is the active next candidate — **stabilization-only**
  (operator decision 2026-06-13; the optional Upload Policy Clarity and UI
  Power-User Polish lanes are not taken for RC3, and #147/#158/#159 are deferred
  post-0.7.3), then stable `0.7.3`. The operator re-confirmed on 2026-06-19 that
  RC3/final ships the MFC suite through the existing PowerShell bootstrapper with
  aMuTorrent still bundled, and **without qBittorrentBB, emulebb-rust,
  TrackMuleBB, `uv`, or the Python installer**. The Pages one-liner moves back to
  the release bootstrap wrapper instead of the future TrackMuleBB scaffold. `main`
  currently carries no app-behavior delta over rc.2 — only the publish-release
  `irm|iex` CI gate (`f83072e6`) and the README install sync (`bf599469`). Draft
  delta: [RC3 changelog](RELEASE-0.7.3-RC3-CHANGELOG.md).
- Scope reconfirm (operator decision 2026-06-20): RC3 stays a **soft freeze**
  (small bug fixes and small features may still land — e.g. FEAT-123 / issue
  #148, the only feature lane taken, still in flight). Scope is the Pages
  `install.ps1` thin wrapper over the release `Bootstrap-eMuleBBSuite.ps1`, the
  MFC client + aMuTorrent + Arr suite as currently shipped. **qBittorrentBB and
  emulebb-rust stay out of the `0.7.x` line entirely and ship in the `0.8.*`
  program** (the forward suite + MFC modernization wave that begins after `0.7.3`).
  See [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md).
- CI status (pre-tag blocker): current `main` CI is red. The
  `0.7.3-nightly.20260615` nightly (commit `72a6f7e`) failed the Nightly build
  (issue #160) and x64+ARM64 Controlled Smoke (issue #161). Because RC3 is cut
  from `main`, these must be green — or triaged as non-blocking with recorded
  operator acceptance — before the RC3 candidate head is locked. The locked rc.2
  heads below remain green; this is a newer-`main` regression to resolve.
- Locked candidate heads: app `38827709` (FEAT-015 broadband upload tuning,
  FEAT-027 diagnostics flush), `emulebb-build` `0fceae7` (the rc.2 build_ref:
  fefff3f plus the BUG-017 `irm|iex` fix), `emulebb-build-tests`
  `2f936c9`, `amutorrent` `8259273` (rebased on upstream `got3nks/amutorrent`
  v3.8.5, plus the RC2 controller delete and pause/resume/stop fixes),
  `emulebb-rust` `656c9a2`, plus current `emulebb-tooling` main. All repos are
  clean and on origin.
- Relaxed proof gate (operator decision 2026-06-12): the shipped app is stable,
  so a passing `test certification --profile fast` is sufficient to gate the RC.
  The full live-network quick release-campaign is downgraded from a hard blocker
  to operator-accepted/non-blocking, and `emulebb-rust` is out of RC2 ship scope
  (lab/preview per the RC2 changelog), so its tests do not gate the ship.
- Publication: DONE. rc.2 is shipped — the operator gave the tag instruction and
  `emulebb-v0.7.3-rc.2` (with the `amutorrent-v3.8.5-emulebb-v0.7.3-rc.2`
  controller companion) is published on GitHub Releases. The candidate was built
  clean from the locked heads (Node-24-pinned aMuTorrent), the fast certification
  passed for the shipped scope, the clean-worktree audit passed, and the RC2
  changelog is finalized.
- Proof status: PASSED for shipped scope. `test certification --profile fast
  --test-network offline` on the locked heads (app `38827709`, build `fefff3f`,
  build-tests `2f936c9`, tooling `7996733`) passed `validate` and all build
  steps (x64 Debug/Release, ARM64 Release, build-tests Debug/Release) on
  2026-06-12; report
  `emulebb_out/reports/certification/20260612T194324Z-fast/certification-result.json`.
  The python-harness ran 1387 tests: 1385 passed (including the new FEAT-015 and
  FEAT-027 coverage); the only 2 failures are `emulebb-rust` preview local tests
  (resume-manifest write + local-swarm exchange), accepted out of RC2 scope. The
  candidate package set (x64/ARM64 standard + diagnostics, aMuTorrent x64) was
  rebuilt clean from these heads. Clean-worktree audit passed; CI is green on all
  candidate heads. Final published package SHA-256/SBOM hashes (for the shipped
  re-published rc.2 built from `emulebb-build` `0fceae7`) are recorded in
  [CI-035](items/CI-035.md). Historical proof trail:
  [CI-035 evidence log](../history/release-0.7.3/CI-035-PROOF-EVIDENCE-LOG.md).
- Release freeze: active. No new feature, refactor, UI polish, warning-debt, or
  roadmap work enters RC2+ unless it is a direct release-gate blocker, package
  or proof fix, approved regression fix, or release-documentation correction.
- Current hold: none. rc.2 is shipped; the next train milestone (rc.3 or stable)
  absorbs only release blockers, proof refreshes, and approved fixes.
- Release source: selected reviewed `main` commit in
  `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main`.
- Tag target: rc.2 is tagged at `emulebb-v0.7.3-rc.2` (annotated, peels to app
  `38827709`). Future candidates tag on the selected reviewed `main` commit after
  fresh proof and a separate operator tag instruction.
- Stock/community comparison baseline: `baseline/community-0.72a`.
- Release stabilization branch: `release/0.7.3` once the operator starts the
  0.7.3 RC branch.
- Package publication: rc.2 core packages and the aMuTorrent companion are
  published on GitHub Releases with manifests, SPDX SBOMs, and GitHub artifact
  attestations; final hashes are recorded in [CI-035](items/CI-035.md).

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
- maintain `RELEASE-0.7.3-RC2-CHANGELOG.md` during RC2 preparation and
  finalize it only when the operator gives the RC2 go;
- include a separate RC1-vs-stock/community-baseline section in that changelog,
  with the RC1 release date from the GitHub release record;
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
- produce the version-specific RC3 changelog before RC3 tag approval;
- record any explicit operator acceptance for proof that cannot be rerun;
- confirm Pages `install.ps1` resolves and forwards to the GitHub Release
  `Bootstrap-eMuleBBSuite.ps1`;
- confirm qBittorrentBB remains out of the RC3/final installer manifest,
  lifecycle scripts, package proof, and public release claims;
- confirm stable `0.7.3` documentation can be produced from the RC3 state.

### Stable 0.7.3 Closeout

Purpose:
turn the accepted RC state into stable `emulebb-v0.7.3`.

Required scaffold before stable tagging:

- stable release notes derived from the accepted RC notes;
- stable `0.7.3` changelog derived from the accepted RC changelog and stable
  deltas;
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

Required outcome:
restore public network connectivity, rerun the quick aggregate campaign against
the RC2+ installer-backed gate, confirm or regenerate package hashes, rerun the
clean-worktree audit, then wait for the operator-controlled tag instruction.

## Remaining Release Backlog

The 0.7.3 RC2+ backlog is narrowed to `CI-035`. `CI-038` is Done with a
current-head `ui-resource-depth` pass covering all 43 release languages, and
`CI-052` is Done with the installer-backed RC2+ campaign rationalization on
`main`. The latest quick campaign dry-run reports the intended 18-command RC
gate with VM proof on-demand. Candidate x64/ARM64 core package hashes, package
SBOM hashes, and optional aMuTorrent x64 hashes are recorded, but the aggregate
quick proof failed under public-network outage conditions. Remaining work is
network restoration, quick release-campaign proof or explicit acceptance, final
checklist confirmation, clean-worktree audit, and the later operator-controlled
tag instruction.

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
- the active candidate has version-specific release notes and changelog, with
  the RC2 changelog carrying the RC1-vs-stock/community-baseline section and
  RC1 release date from the GitHub release record;
- no active workspace repo has unrelated uncommitted changes; and
- the operator gives a separate tagging instruction.

The accepted `FEAT-058`, `FEAT-059`, `FEAT-060`, `FEAT-061`, and `FEAT-071`
closeout hardening changed release-facing documentation, app UI, app REST
metadata, build-test guardrails, and remote filename intake after the previous
prep audit. Final proof must target the pushed heads that exist after this
polish and hardening lands.
