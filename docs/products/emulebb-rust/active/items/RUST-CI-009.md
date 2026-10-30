---
id: RUST-CI-009
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/142
title: Certify a Beta 3 candidate without publishing
status: OPEN
priority: Major
category: ci
labels: [rust, release, packaging, harness, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-22
source: 2026-10-22 Beta 3 readiness planning after the server-retirement and local-client evidence repairs
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/142. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-009 - Certify a Beta 3 candidate without publishing

## Summary

Turn one explicitly selected immutable Rust revision into a reviewable Beta 3
candidate by composing the current-head parity campaign, hosted CI, release
asset assembly, packaged lifecycle checks, and retained provenance into one
reproducible sign-off manifest. This item prepares a candidate for later human
approval; it does not bump the version, create a tag or GitHub Release, publish
an image, close the milestone, or declare the beta shipped.

Creating this item does not freeze `main`. Review and implementation iterations
continue normally until an operator explicitly selects a candidate revision.

## Current State

- The bounded parity, persistence, lifecycle, and policy findings merged through
  Rust PR [#194](https://github.com/emulebb/emulebb-rust/pull/194) at
  `431d45a8283fe5edbc8357be412e933771af3232`; their fifteen owning issues are
  closed. Remaining milestone items still block candidate selection.
- The current published baseline remains `rust-v0.1.0-beta.2`.
- RUST-CI-006 still owns the same-head stock eMule/current-aMule/Rust parity
  campaign and documentation reconciliation.
- Hosted CI and release packaging cover the supported platform and architecture
  matrix. The release workflow now retains a non-publishing candidate bundle
  with exact revision, artifact, and packaged-lifecycle metadata, but no Beta 3
  candidate has been selected and certified against RUST-CI-006.

## Non-Publishing Rehearsal Evidence (2026-10-22)

Rust PR [#143](https://github.com/emulebb/emulebb-rust/pull/143) added the
always-on candidate assembly boundary. Workflow run
[`39796808727`](https://github.com/emulebb/emulebb-rust/actions/runs/39796808727)
then exercised it successfully without publishing:

- Rust source `9e9320e69f070c62d04d1170a5a8997eba7387e2` passed exact-source
  Required CI and Required CodeQL checks.
- Support revisions were `emulebb-build`
  `bd96006a94b92ab9a8499f563c86011f36dfbfd9`, `emulebb-build-tests`
  `160da394fc74343bffd2846db4058eb3a11ed050`, and `emulebb-tooling`
  `9af34723a508b46be839502138b64a0be7e39dde`.
- Native source revisions were `emulebb-miniupnp`
  `4e7a10948004ca2085ac8103e14fc77edb898b4c` and
  `emulebb-libpcpnatpmp` `a6e787f837e507336a8774522c33b54264ef4a4b`.
- All six native package jobs, the multi-architecture OCI image/security job,
  and the non-publishing assembly job completed successfully.
- The retained manifest recorded 29 hashed evidence files plus itself. Its OCI
  manifest digest was
  `sha256:edcb1129228e06ec6465d4f4ae825b0cab6224316e81c738ee8c99200b665854`;
  independent inspection matched every recorded size, SHA-256 value, native
  checksum entry, image-security checksum entry, and revision.
- GHCR publication, GitHub prerelease publication, nightly channel advancement,
  and nightly retention jobs were skipped. No tag or GitHub Release was created.

This run deliberately used the current `0.1.0-beta.2` package identity. It
proves the dry-run assembly and provenance machinery only; it is not the Beta 3
candidate, does not satisfy RUST-CI-006 or the packaged lifecycle acceptance
criterion, and does not close any acceptance checkbox below.

## Packaged Lifecycle Rehearsal Evidence (2026-10-22)

Rust PR [#144](https://github.com/emulebb/emulebb-rust/pull/144) added an
isolated downstream lifecycle job for every native package target and upgraded
the retained candidate manifest to format version 2. The job checks out package
artifacts from the selected candidate but executes only trusted workflow code
and the immutable `emulebb-build-tests` harness revision.

The first rehearsal,
[`39818800981`](https://github.com/emulebb/emulebb-rust/actions/runs/39818800981),
correctly stopped at candidate assembly. GitHub artifact download had removed
the AppImage executable bit, and the harness temporary-directory context manager
suppressed the resulting body exception, leaving a partial Linux report.
`emulebb-build-tests` PR
[#16](https://github.com/emulebb/emulebb-build-tests/pull/16) restored the
owner-execute bit before AppImage extraction and preserved body exceptions.
Rust PR [#145](https://github.com/emulebb/emulebb-rust/pull/145) then pinned the
merged harness revision.

The corrected non-publishing rehearsal,
[`39832416413`](https://github.com/emulebb/emulebb-rust/actions/runs/39832416413),
completed successfully:

- Rust source `45b4d40005472315b6e675515f725c95565c3384` passed exact-source
  Required CI in run
  [`39828335412`](https://github.com/emulebb/emulebb-rust/actions/runs/39828335412)
  and Required CodeQL in run
  [`39828335419`](https://github.com/emulebb/emulebb-rust/actions/runs/39828335419).
- Support revisions were `emulebb-build`
  `bd96006a94b92ab9a8499f563c86011f36dfbfd9`, `emulebb-build-tests`
  `fdabef50aaacbb4818dfa8b8561a9441e76afc70`, and `emulebb-tooling`
  `9af34723a508b46be839502138b64a0be7e39dde`. Native source revisions remained
  `emulebb-miniupnp` `4e7a10948004ca2085ac8103e14fc77edb898b4c` and
  `emulebb-libpcpnatpmp` `a6e787f837e507336a8774522c33b54264ef4a4b`.
- All six native package jobs, all six downstream packaged-lifecycle jobs, the
  multi-architecture OCI image/security job, and candidate assembly passed.
- Manifest format version 2 recorded six package-smoke reports covering eight
  unique assets: one Windows ZIP and one macOS DMG per architecture, plus both
  the DEB and AppImage for each Linux architecture.
- Every package result started from a fresh local-only profile, served the REST
  API and WebUI, accepted and completed a 262144-byte direct-source ED2K
  transfer with public discovery disabled, delivered the exact SHA-256 payload
  inside the incoming directory, and completed two graceful shutdowns.
- Independent inspection matched each report SHA-256 to the manifest:
  `linux-arm64` `d375b00ecb6229f14efce418e8e2234755c133c526c32b892471bec34bea664b`,
  `linux-x64` `88318b762aa072ebd71dea3ab1fc4a560e8edc9b3410596f5d6fc5de03c73ea1`,
  `macos-arm64` `c854a9af04155bec094363c8e6667806401eccf2a52a785b4b7120d708e38e88`,
  `macos-x64` `0e3bc631530da7456302851e7b19b8a9e1e64e19ed910aca2c3974aed74e174c`,
  `windows-arm64` `6311a3e631d93baa5fc9f33aa467dad1f2c9e30dbf237c6102c96d6ddaff19d0`,
  and `windows-x64` `db3973935f867e52366a8022728248ffb2ee2878b0141aa7652311ef37c159a2`.
- GHCR publication, GitHub prerelease publication, nightly channel advancement,
  and nightly retention were skipped. No tag, release, image, version bump, or
  milestone change was performed.

This corrected run proves the hosted packaged-lifecycle and manifest machinery
against one immutable revision set. It still uses the `0.1.0-beta.2` package
identity and is not the selected Beta 3 candidate. RUST-CI-006 and the remaining
candidate-selection review must still run on the eventual candidate revision,
so no acceptance checkbox is closed by this rehearsal.

## Intended Shape

- Select the candidate only after the current review iteration has no accepted
  implementation changes left in flight.
- Record exact commits for `emulebb-rust`, `emulebb-build-tests`,
  `emulebb-tooling`, and `emulebb-build`, plus the stock eMule and current-aMule
  build identities consumed by RUST-CI-006.
- Require RUST-CI-006 evidence from the exact candidate Rust revision. Do not
  merge evidence from another product revision into the candidate manifest.
- Reuse the supported build orchestration and persisted Python harnesses for
  package assembly, install/start, WebUI, local transfer, shutdown, cleanup,
  privacy, and artifact audits.
- Assemble every supported native asset, checksums, SBOMs, and the OCI image in
  dry-run form without invoking any tag-triggered or publishing workflow.
- Produce one compact manifest that maps every required gate to its command,
  revision, result, retained report, and artifact digest.

## Candidate Invalidation

- Any change to Rust product source, policy, OpenAPI, embedded WebUI, packaging,
  or dependency locks invalidates the candidate and requires a new Rust
  revision plus a fresh complete certification pass.
- A support-repository change invalidates the recorded support revision. Rerun
  every affected lane before replacing the manifest; never edit a passing
  manifest to point at untested support code.
- Documentation-only reconciliation may follow the evidence only when it does
  not change a product contract, gate definition, command, or evidence claim.
- A failed mandatory lane leaves the item open. Fix the cause on a normal branch
  and begin again from the resulting clean revision rather than patching the
  candidate in place.

## Scope Constraints

- Do not change `0.1.0-beta.2`, create `0.1.0-beta.3`, move a tag, draft a
  release, publish GHCR content, or close the Beta 3 milestone under this item.
- Do not introduce a compatibility freeze. API, configuration, and schema may
  still break before the post-Arr freeze; such a change simply invalidates the
  current candidate.
- Do not create ad-hoc PowerShell, inline Python, or alternate launch logic for
  a missing lane. Improve the owning persisted harness in a separate reviewed
  scope first.
- Keep bulky, private, and machine-specific evidence below
  `EMULEBB_WORKSPACE_OUTPUT_ROOT`. Commit only stable conclusions, hashes, and
  safe report references.
- Do not waive a failing safety, data-integrity, privacy, stock-wire, packaging,
  or lifecycle result merely to make the candidate complete.

## Acceptance Criteria

- [ ] The Beta 3 milestone has no open implementation item other than this
      certification gate.
- [ ] One immutable revision set is recorded for the Rust product, support
      repositories, reference clients, contracts, fixtures, and toolchains.
- [ ] RUST-CI-006 is complete against the exact candidate Rust revision and its
      evidence manifest passes cleanup, secret, privacy, and documentation
      reconciliation checks.
- [ ] Required hosted CI is green at the candidate revision, including policy,
      format, Clippy, tests, supply-chain checks, CodeQL, and live REST/OpenAPI
      conformance.
- [ ] Dry-run release assembly produces the complete Windows, Linux, macOS, and
      OCI asset set with matching checksums, SBOMs, provenance, and revision
      metadata.
- [ ] Supported packaged lifecycle lanes install or unpack, start, serve the
      WebUI, complete the required local transfer smoke, and shut down cleanly.
- [ ] The retained candidate manifest maps every mandatory result and artifact
      to exact revisions and digests without private paths, secrets, or operator
      content.
- [ ] The final review explicitly records that no Beta 3 tag, release, image,
      version bump, or milestone closure was performed.

## Validation

- Run Rust build, test, package, assembly, and artifact-audit entry points only
  through `repos/emulebb-build` using `python -m emule_workspace`.
- Run live, soak, parity, and packaged lifecycle work only through maintained
  Python entry points in `repos/emulebb-build-tests`.
- Run repository-native documentation, taxonomy, link, policy, and roadmap
  checks at the recorded support revisions.
- Review the manifest manually against RUST-CI-006, the Beta 3 milestone, the
  omission and extension registries, the OpenAPI contract, and the produced
  asset inventory.

## Notes

This gate is intentionally restartable. More review iterations are expected;
the cost of accepting a better beta design is selecting and certifying a new
candidate, not preserving a stale candidate or weakening the long-term model.
