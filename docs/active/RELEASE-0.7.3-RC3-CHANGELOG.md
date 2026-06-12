# eMuleBB 0.7.3-rc.3 Changelog

Status: draft for RC3 preparation; finalize at RC3 go after the candidate heads, package names, hashes, proof status, and accepted deviations are recorded.

Format: one line per item, grouped by area; this is a power-user changelog, not a Git log.

RC3 is a delta over the published RC2 artifact set. It is **stabilization-first**:
crash/data-loss, packaging/provenance, regression, and release-documentation
fixes on supported surfaces. It may also carry **very minimal, operator-approved**
slices from two lanes only — Upload Policy Clarity and UI Power-User Polish — each
small, observable, opt-in, and low-risk, with stock eD2K/Kad wire semantics
unchanged. The core eMuleBB protocol surface and package shape are unchanged from
RC2 except where noted. Final package hashes and proof status are recorded in
[RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) and tracked by
[CI-035](items/CI-035.md). For the RC2-and-earlier delta and the RC1-vs-baseline
history, see [RELEASE-0.7.3-RC2-CHANGELOG](RELEASE-0.7.3-RC2-CHANGELOG.md).

### Stabilization

- _(RC3 stabilization fixes — crash/data-loss, packaging/provenance, regression,
  release-doc — land here as they are approved and merged.)_

### Upload Policy Clarity

- _(Optional. Minimal, opt-in upload/seeding clarity slices only; no silent
  state mutation. Empty unless a slice is approved for RC3.)_

### UI Power-User Polish

- _(Optional. Small, self-contained, low-risk UI slices only. Empty unless a
  slice is approved for RC3.)_

### Packages

- RC3/Packages: x64 and ARM64 standard + diagnostics ZIPs, the suite bootstrapper,
  and the optional aMuTorrent x64 controller companion are regenerated from the
  selected RC3 head with refreshed manifests, SPDX SBOMs, and SHA-256 hashes.
  *(Final names and hashes pending the RC3 candidate build.)*
- RC3/Packages: Release ZIPs remain **unsigned** (accepted posture); verification
  continues through manifests, SBOMs, SHA-256 evidence, and GitHub artifact
  attestations.

### Proof

- RC3/Proof: Pending — `test certification --profile fast --test-network offline`
  (shipped scope) on the selected RC3 head, the clean-worktree audit, and the
  publish-release `irm|iex` gate before the operator tag instruction. Tracked by
  [CI-035](items/CI-035.md).

### Risk and Testing Focus

- RC3/Risk: Re-confirm the supported surfaces touched by any approved slice
  (upload policy and/or UI) on a fresh install; confirm the regenerated package
  set and the aMuTorrent companion install and run cleanly, including the
  `irm | iex` one-liner.
