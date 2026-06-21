# eMuleBB 0.7.3-rc.3 Changelog

Status: PUBLISHED 2026-06-21 as the `emulebb-v0.7.3-rc.3` prerelease (app `fd17a04`) with the `amutorrent-v3.8.8-emulebb-v0.7.3-rc.3` companion. Final published hashes are recorded below.

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
(run 27909074408), built with `build_ref=main` (deterministic pinned Node for the
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
| `emulebb-0.7.3-rc.3-x64.zip` | `0a10276a690aeb7b603a6cb3c864b0328be72d6f6645679b8fe7ec8b0c7e4d53` |
| `emulebb-0.7.3-rc.3-arm64.zip` | `f571eca7f8179dd4794fec8f98c49a82597ed9a032c821b6eeca63912e81b8e6` |
| `emulebb-0.7.3-rc.3-diagnostics-x64.zip` | `6d3c0cf8f420608b54bdb4b11321ff12cf7dd85596aebe8e890a2573553b762f` |
| `emulebb-0.7.3-rc.3-diagnostics-arm64.zip` | `a8ce7a91ddf9e1bb700766debb4c8adf8db63043a04d78cd7039d649911f01be` |
| `Bootstrap-eMuleBBSuite.ps1` | `edf901f4362639bb842d3fa8278a96fe35b76a57d8a6a2ec3da6701ecfb28429` |

SPDX SBOM SHA-256 (each ZIP ships its `.manifest.json` + `.sbom.spdx.json`
sidecars; the bootstrapper ships its `.sha256`):

- x64: `c53762f1197953abc507fd520bbe04f3bed0a72b0edbe9f70e31931e0832f000`
- arm64: `e7baba2c542ab8307f468186f37e3713017de8adebc289e381f46b52c8998d56`
- diagnostics-x64: `27619fc2013aecb7b805baa2fc140403efc7383a10881d909658f1a4ed28b613`
- diagnostics-arm64: `962d89af6c9050acaa7485a9d21b5aa628c7d892460ea3b4726da54bf65de3a4`

The aMuTorrent x64 controller companion is published as
[`amutorrent-v3.8.8-emulebb-v0.7.3-rc.3`](https://github.com/emulebb/amutorrent/releases/tag/amutorrent-v3.8.8-emulebb-v0.7.3-rc.3)
(built deterministically against pinned Node 24.16.0):
`emulebb-0.7.3-rc.3-amutorrent-x64.zip` SHA-256
`3e7aaf65c570361fa8ef6fcf52bc21b041bb9dda793ac4a85fa2eccaefee897d`.

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
  Final published hashes are recorded in "Published Heads And Artifacts" above.
- RC3/Packages: no qBittorrentBB, emulebb-rust, TrackMuleBB, `uv`, or Python
  setup assets are part of the RC3/final package set.
- RC3/Packages: Release ZIPs remain **unsigned** (accepted posture); verification
  continues through manifests, SBOMs, SHA-256 evidence, and GitHub artifact
  attestations.

### Proof

- RC3/Proof: Done — `test certification --profile fast --test-network offline`
  passed for shipped scope (1436/1439; 3 out-of-scope `emulebb-rust` failures
  accepted), clean-worktree audit passed, and the publish-release `irm|iex` gate
  passed. Recorded in [CI-035](items/CI-035.md).
- RC3/Proof: Done — the Pages `install.ps1` one-liner resolves the release and the
  bootstrapper resolves rc.3 + the aMuTorrent companion and plans the Full install
  end-to-end (verified by `-DryRun` against the published release). Both the wrapper
  and bootstrapper were hardened to resolve from the `/releases` list with retry,
  after GitHub's `/releases/tags/<tag>` endpoint flapped 504; rc.3 was re-published
  with the by-tag-free bootstrapper.
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
