# eMule Broadband Edition 0.7.3 Release Train Dashboard

This is the current release-train dashboard for the fixed 0.7.3 candidate
sequence. RC1 and RC2 are frozen historical evidence. RC3 is the current
published candidate; active release work now targets stable `0.7.3`. Use this
document for status, release-source truth, and the open RC task list.

## Current Status

- Status: **RC3 is PUBLISHED** (2026-06-21). The annotated tag
  `emulebb-v0.7.3-rc.3` peels to app `fd17a04`; GitHub prerelease at
  <https://github.com/emulebb/emulebb/releases/tag/emulebb-v0.7.3-rc.3>, built by
  the `Publish release` workflow (run 27909074408, `build_ref=main`) after the
  relaxed-gate fast certification passed for the shipped scope. The matching
  `amutorrent-v3.8.8-emulebb-v0.7.3-rc.3` controller companion is published
  alongside it. After GitHub's `/releases/tags/<tag>` endpoint flapped 504, the
  Pages wrapper and bootstrapper were hardened to resolve from the `/releases`
  list and rc.3 was re-published with the by-tag-free bootstrapper. The RC3 delta
  over RC2 is FEAT-123 (shared-files one-level auto-updater), the #159 toolbar
  button-reorder regression fix, the publish-release `irm|iex` CI gate
  (`f83072e6`), and the README install sync (`bf599469`); the protocol surface and
  package shape are unchanged from RC2 except as recorded in the
  [RC3 changelog](RELEASE-0.7.3-RC3-CHANGELOG.md). Final published artifact
  SHA-256 hashes are recorded there and in [CI-035](items/CI-035.md).
- Next milestone: **stable `0.7.3`** under a **soft freeze** (operator decision
  2026-06-13, refined 2026-06-20; see the scope-reconfirm bullet below). The
  optional Upload Policy Clarity lane is not taken (#147/#158 upload slots
  deferred post-0.7.3); both the #159 toolbar button-reorder regression fix and
  the #159 active-category-tab bold (an opt-in Tweaks option) shipped in rc.3.
  The operator re-confirmed on 2026-06-19 that
  RC3/final ships the MFC suite through the existing PowerShell bootstrapper with
  aMuTorrent still bundled, and **without qBittorrentBB, emulebb-rust,
  TrackMuleBB, `uv`, or the Python installer**. The Pages one-liner uses the
  release bootstrap wrapper instead of the future TrackMuleBB scaffold.
- Scope reconfirm (operator decision 2026-06-20): RC3 stays a **soft freeze**
  (small bug fixes and small features may still land — e.g. FEAT-123 / issue
  #148, the only feature lane taken, now landed). Scope is the Pages
  `install.ps1` thin wrapper over the release `Bootstrap-eMuleBBSuite.ps1`, the
  MFC client + aMuTorrent + Arr suite as currently shipped. **qBittorrentBB and
  emulebb-rust stay out of the `0.7.x` line entirely and ship in the `0.8.*`
  program** (the forward suite + MFC modernization wave that begins after `0.7.3`).
  See [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md).
- CI status: **green on current `main`.** The earlier `0.7.3-nightly.20260615`
  failure (commit `72a6f7e`, issues #160/#161) is resolved and both issues are
  closed; subsequent `main` fixes (package `preferences.ini` requirement, the
  controlled-smoke LAN-transfer retry) restored the gates. As of 2026-06-21 the
  scheduled Nightly is green, and the 2026-06-20 Controlled Smoke and RC Package
  Proof workflow runs passed on `main`. The pre-tag CI blocker is cleared; the
  RC3 candidate head was locked, certified, packaged, and published per
  [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md).
- Locked candidate heads (rc.3): app `fd17a04` (FEAT-123 shared-files
  auto-reload + #159 toolbar fix over rc.2), `emulebb-build` `af19faa`
  (deterministic pinned-Node aMuTorrent build), `emulebb-build-tests` current
  `main` (rc.3 campaign + cpu-heavy-quick trim), `amutorrent` `2da7c19`
  (controller companion, published as `amutorrent-v3.8.8-emulebb-v0.7.3-rc.3`),
  plus current `emulebb-tooling` main. All repos are clean and on origin.
- Relaxed proof gate (operator decision 2026-06-12): the shipped app is stable,
  so a passing `test certification --profile fast` is sufficient to gate the RC.
  The full live-network quick release-campaign is downgraded from a hard blocker
  to operator-accepted/non-blocking, and `emulebb-rust` is out of RC ship scope
  (lab/preview), so its tests do not gate the ship.
- Publication: DONE. rc.3 is shipped — the operator gave the tag instruction and
  `emulebb-v0.7.3-rc.3` (with the `amutorrent-v3.8.8-emulebb-v0.7.3-rc.3`
  controller companion) is published on GitHub Releases. The candidate was built
  clean from the locked heads (Node-24-pinned aMuTorrent), the fast certification
  passed for the shipped scope, the clean-worktree audit passed, and the RC3
  changelog is finalized.
- Proof status: PASSED for shipped scope. `test certification --profile fast
  --test-network offline` on the rc.3 locked heads passed `validate` and all
  build steps; the python-harness ran 1439 tests, 1436 passed, and the only 3
  failures are `emulebb-rust` preview local tests accepted out of RC scope. The
  candidate package set (x64/ARM64 standard + diagnostics, aMuTorrent x64) was
  rebuilt clean from these heads, the Pages `install.ps1` one-liner dry-run
  resolved rc.3 + the aMuTorrent companion end-to-end, and the clean-worktree
  audit passed. Final published package SHA-256/SBOM hashes are recorded in the
  [RC3 changelog](RELEASE-0.7.3-RC3-CHANGELOG.md) and [CI-035](items/CI-035.md).
  Historical proof trail:
  [CI-035 evidence log](../history/release-0.7.3/CI-035-PROOF-EVIDENCE-LOG.md).
- Release freeze: active. No new feature, refactor, UI polish, warning-debt, or
  roadmap work enters RC3/final unless it is a direct release-gate blocker,
  package or proof fix, approved regression fix, or release-documentation
  correction.
- Current hold: none. rc.3 is shipped; the next train milestone (stable `0.7.3`)
  absorbs only release blockers, proof refreshes, and approved fixes.
- Release source: selected reviewed `main` commit in
  `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main`.
- Tag target: rc.3 is tagged at `emulebb-v0.7.3-rc.3` (annotated, peels to app
  `fd17a04`). Stable `0.7.3` tags on the selected reviewed `main` commit after
  fresh proof and a separate operator tag instruction.
- Stock/community comparison baseline: `baseline/community-0.72a`.
- Release stabilization branch: `release/0.7.3` once the operator starts the
  0.7.3 stable branch.
- Package publication: rc.3 core packages and the aMuTorrent companion are
  published on GitHub Releases with manifests, SPDX SBOMs, and GitHub artifact
  attestations; final hashes are recorded in the
  [RC3 changelog](RELEASE-0.7.3-RC3-CHANGELOG.md) and [CI-035](items/CI-035.md).

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
the rc.3 relaxed-gate proof is DONE (Fast certification passed for shipped
scope, package hashes recorded, Pages `install.ps1` dry-run passed,
clean-worktree audit passed, operator tag given, `emulebb-v0.7.3-rc.3`
published). `CI-035` now carries forward as the stable `0.7.3` final-proof
tracker, whose bar is higher than the relaxed RC gate.

## Remaining Release Backlog

The published rc.3 backlog is closed; `CI-035` continues as the stable `0.7.3`
final-proof tracker. `CI-038` is Done with a current-head `ui-resource-depth`
pass covering all 43 release languages, and `CI-052` is Done with the
installer-backed RC2+ campaign rationalization on `main`. Candidate x64/ARM64
core package hashes, package SBOM hashes, and optional aMuTorrent x64 hashes are
recorded for the published rc.3. Remaining work belongs to the stable `0.7.3`
cut: the higher final gate (live release-campaign rows, overnight soak, and a
Windows-VM matrix smoke), final checklist confirmation, clean-worktree audit,
and the later operator-controlled stable tag instruction.

All other active `FEAT`, `REF`, warning-debt, cleanup, and polish items are
post-0.7.3 by default. A non-blocking item may enter RC3/final only if a current
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
