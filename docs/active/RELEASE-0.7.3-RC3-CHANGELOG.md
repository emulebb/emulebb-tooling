# eMuleBB 0.7.3-rc.3 Changelog

Status: draft for RC3 preparation; finalize at RC3 go after the candidate heads, package names, hashes, proof status, and accepted deviations are recorded.

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
shipped; **qBittorrentBB and emulebb-rust stay out and are now positioned
post-`0.8.*`** (beyond the `0.7.x` line, not merely post-`0.7.3`). The two
optional lanes (Upload Policy Clarity, UI Power-User Polish) are **not taken**
for RC3; their candidate inbound issues (#147/#158 upload slots, #159 Customize
Toolbar) are deferred post-0.7.3. The core eMuleBB protocol surface and package shape are unchanged
from RC2 except where noted. Final package hashes and proof status are recorded in
[RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) and tracked by
[CI-035](items/CI-035.md). For the RC2-and-earlier delta and the RC1-vs-baseline
history, see [RELEASE-0.7.3-RC2-CHANGELOG](RELEASE-0.7.3-RC2-CHANGELOG.md).

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
- RC3/Shared files (in flight — the soft-freeze small feature for RC3, **not yet
  merged to `main`**): shared directories auto-check for new direct child files
  every 5 minutes using bounded one-level polling; recursive monitored sharing
  remains opt-in and unchanged ([FEAT-123](items/FEAT-123.md), issue #148). This
  bullet finalizes only once the implementation lands and its acceptance criteria
  pass.
- _(Further crash/data-loss, packaging/provenance, regression, and release-doc
  fixes land here as approved and merged.)_

### Upload Policy Clarity

- None for RC3. Lane not taken (operator decision 2026-06-13); #147/#158 upload
  slots deferred post-0.7.3.

### UI Power-User Polish

- None for RC3. Lane not taken (operator decision 2026-06-13); #159 Customize
  Toolbar deferred post-0.7.3.

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
- RC3/Proof: **Pre-tag blocker** — current `main` CI is red. The
  `0.7.3-nightly.20260615` nightly (commit `72a6f7e`) has a failing Nightly
  build (issue #160) and failing x64+ARM64 Controlled Smoke (issue #161). RC3 is
  cut from `main`, so both must be green (or the failures triaged as
  non-blocking with recorded operator acceptance) before the RC3 candidate head
  is locked. The locked rc.2 heads remain green; this is a newer-`main` delta.

### Risk and Testing Focus

- RC3/Risk: With no optional slice taken, RC3 risk is confined to the
  release-tooling/doc delta. Confirm the regenerated package set and the
  aMuTorrent companion install and run cleanly on a fresh install, including the
  `irm | iex` one-liner that the new CI gate protects.
- RC3/Risk: Confirm no qBittorrentBB folder, process, config, service entry, or
  public install claim is produced by the default Full bundle.
