# eMuleBB 0.7.3-rc.3 Changelog

Status: PUBLISHED 2026-06-21 as the `emulebb-v0.7.3-rc.3` prerelease (app `fd17a04`). Final published hashes are recorded below; the aMuTorrent companion release is pending.

Format: one line per item, grouped by area; this is a power-user changelog, not a Git log.

RC3 is a delta over the published RC2 artifact set. **Operator decision
2026-06-13: RC3 is stabilization-only** — crash/data-loss, packaging/provenance,
regression, and release-documentation fixes on supported surfaces. Operator
decision 2026-06-19 keeps the release train on the existing PowerShell
MFC+aMuTorrent bundle: qBittorrentBB, emulebb-rust, TrackMuleBB, `uv`, and the
Python installer are out of RC3/final scope. **Operator decision 2026-06-20**
keeps a **soft freeze** (small bug fixes and small features may still land) and
reconfirms the scope as: Pages `install.ps1` as a thin wrapper over the release
`Bootstrap-eMuleBBSuite.ps1`; MFC client + aMuTorrent + Arr suite as currently
shipped; **qBittorrentBB and emulebb-rust stay out of the `0.7.x` line entirely
and ship in the `0.8.*` program** (the forward suite + MFC modernization wave that
begins after `0.7.3`). The Upload
Policy Clarity lane is **not taken** for RC3 (#147/#158 upload slots deferred
post-0.7.3). From the UI Power-User Polish lane, the **#159 toolbar button-reorder
regression is fixed** in RC3 under the soft freeze; the remaining #159 cosmetic
request (bold the active category tab) stays deferred post-0.7.3. The core eMuleBB protocol surface and package shape are unchanged
from RC2 except where noted. Final package hashes and proof status are recorded in
[RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) and tracked by
[CI-035](items/CI-035.md). For the RC2-and-earlier delta and the RC1-vs-baseline
history, see [RELEASE-0.7.3-RC2-CHANGELOG](RELEASE-0.7.3-RC2-CHANGELOG.md).

### Published Heads And Artifacts

Published on app `fd17a04` (origin/main) via the `Publish release` workflow
(run 27905947687), built with `build_ref=main` (deterministic pinned Node for the
aMuTorrent package). Locked heads:

| Repo | Head | Notes |
| --- | --- | --- |
| `emulebb` (app) | `fd17a04` | MFC client; FEAT-123 + #159 toolbar fix over rc.2 |
| `emulebb-build` | `af19faa` | build orchestration; deterministic pinned-Node aMuTorrent build |
| `emulebb-build-tests` | current `main` | harness and campaigns; rc.3 campaign + cpu-heavy-quick trim |
| `amutorrent` | `2da7c19` | controller companion (rc.3 companion release pending) |
| `emulebb-tooling` | current `main` | docs and proof tracking |

Published artifact SHA-256 (authoritative, from the GitHub release assets), tag
[`emulebb-v0.7.3-rc.3`](https://github.com/emulebb/emulebb/releases/tag/emulebb-v0.7.3-rc.3),
published 2026-06-21:

| Asset | SHA-256 |
| --- | --- |
| `emulebb-0.7.3-rc.3-x64.zip` | `1e6a3a4e4603c39564fc17c6ee47482fd1e1757cac62d0af9d76f72c8cd75d2d` |
| `emulebb-0.7.3-rc.3-arm64.zip` | `8e00aecc25c694ccaedb522b16fcb39179674ec93f5a0cba76058be1c2ff1efb` |
| `emulebb-0.7.3-rc.3-diagnostics-x64.zip` | `bd7a5eb0bd43c2f44a7878344e0cdd12655d33c8b6d4ee3bd04101be36453069` |
| `emulebb-0.7.3-rc.3-diagnostics-arm64.zip` | `8eeb9ea6a718f04574fa395184d957e92999fccd76b421887d604b04c0f3d4f6` |
| `Bootstrap-eMuleBBSuite.ps1` | `dc39cbc599e7532b47f58a05525dd4f7bec6c644a0e327b3b233dacb3ef631b6` |

SPDX SBOM SHA-256 (each ZIP ships its `.manifest.json` + `.sbom.spdx.json`
sidecars; the bootstrapper ships its `.sha256`):

- x64: `5be22b32330b3348535eb121eac489e20ca4d95a05604b034916fef180ca9c9c`
- arm64: `4d83e4564d8a3f19dba27abbcbace00fd087208a26ebd82b0f9370269631ed97`
- diagnostics-x64: `8eff68bfe9c73e37d967cfb04662829ed88cad7629b5c2117cfdce4cf5144726`
- diagnostics-arm64: `e632df928ce2a96f98a841617516ef7d02003253c616689aabd2d839028e2452`

The aMuTorrent x64 controller companion (`emulebb-0.7.3-rc.3-amutorrent-x64.zip`)
publishes as a separate `amutorrent-v*-emulebb-v0.7.3-rc.3` release; **pending**.

### Stabilization

- RC3/Release-tooling: `Publish release` now gates on the install scripts binding
  cleanly under `irm | iex` (app `f83072e6`), closing the BUG-017 class of
  one-liner-install regressions at CI time.
- RC3/Docs: README install commands synced to the published `0.7.3-rc.2` assets
  (app `bf599469`).
- RC3/Installer: GitHub Pages `install.ps1` is restored to a thin wrapper around
  the release `Bootstrap-eMuleBBSuite.ps1` asset. The future TrackMuleBB/`uv`
  scaffold is documented as post-0.7.3 only.
- RC3/Installer: qBittorrentBB is parked outside the RC3/final suite manifest and
  cannot be selected by the packaged MFC+aMuTorrent installer.
- RC3/Shared files: shared directories auto-check for new direct child files
  every 5 minutes using bounded one-level polling; recursive monitored sharing
  remains opt-in and unchanged ([FEAT-123](../history/items/FEAT-123.md), issue
  #148). Landed and accepted for RC3.
- _(Further crash/data-loss, packaging/provenance, regression, and release-doc
  fixes land here as approved and merged.)_

### Upload Policy Clarity

- None for RC3. Lane not taken (operator decision 2026-06-13); #147/#158 upload
  slots deferred post-0.7.3.

### UI Power-User Polish

- RC3/UI: Customize Toolbar **button reordering fixed** (app `ff81a810`, issue
  #159). `TBN_GETBUTTONINFO` returned its result inverted — a regression from the
  ARM64 merge (`24d1de79`) — so the customize button-info enumeration came back
  empty and the dialog could not reorder existing buttons; only separators could
  be added. The fix also removes the related out-of-bounds read. Built green on
  x64 Debug + Release + Release-diagnostics.
- Deferred: the remaining #159 cosmetic request (bold the active category tab)
  stays post-0.7.3.

### Packages

- RC3/Packages: x64 and ARM64 standard + diagnostics ZIPs, the suite bootstrapper,
  and the optional aMuTorrent x64 controller companion are regenerated from the
  selected RC3 head with refreshed manifests, SPDX SBOMs, and SHA-256 hashes.
  *(Final names and hashes pending the RC3 candidate build.)*
- RC3/Packages: no qBittorrentBB, emulebb-rust, TrackMuleBB, `uv`, or Python
  setup assets are part of the RC3/final package set.
- RC3/Packages: Release ZIPs remain **unsigned** (accepted posture); verification
  continues through manifests, SBOMs, SHA-256 evidence, and GitHub artifact
  attestations.

### Proof

- RC3/Proof: Pending — `test certification --profile fast --test-network offline`
  (shipped scope) on the selected RC3 head, the clean-worktree audit, and the
  publish-release `irm|iex` gate before the operator tag instruction. Tracked by
  [CI-035](items/CI-035.md).
- RC3/Proof: Pending — Pages wrapper dry-run/parse proof that the public one-liner
  resolves `Bootstrap-eMuleBBSuite.ps1`, verifies the sidecar hash when present,
  and forwards existing bootstrapper parameters.
- RC3/Proof: CI is **green** on current `main`. The earlier
  `0.7.3-nightly.20260615` failure (commit `72a6f7e`, issues #160/#161) is
  resolved and both issues are closed; the scheduled Nightly (2026-06-21) and the
  2026-06-20 Controlled Smoke and RC Package Proof runs pass. The pre-tag CI
  blocker is cleared — lock the RC3 candidate head, then run the pending
  certification and package refresh above.

### Risk and Testing Focus

- RC3/Risk: Beyond the release-tooling/doc delta, RC3 now carries the #159
  toolbar button-reorder fix (and the landed FEAT-123 shared-file lane).
  Confirm the regenerated package set and the aMuTorrent companion install and run
  cleanly on a fresh install, including the `irm | iex` one-liner that the new CI
  gate protects, and verify Customize Toolbar can reorder buttons (not just add
  separators).
- RC3/Risk: Confirm no qBittorrentBB folder, process, config, service entry, or
  public install claim is produced by the default Full bundle.
