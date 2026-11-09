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

## Nightly Input and Current-head CD Disposition (2026-11-09)

Historical Nightly run [42356965321](https://github.com/emulebb/emulebb-rust/actions/runs/42356965321)
failed on 2026-11-07 at Rust `f4527c2d0ca4ca1e7000260dc0d23767f37d8ef4`
when its pinned image input returned HTTP 429. Later same-head run
[42370250815](https://github.com/emulebb/emulebb-rust/actions/runs/42370250815)
passed all six package/lifecycle lanes, image candidate, assembly, and
publication. Its [dated nightly](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.2.nightly.20261107.gf4527c2d)
was published on 2026-11-07. The earlier 429 is historical, not a current
blocker; this sequence does not prove a permanent provider/authentication fix.

The latest verified non-publishing candidate rehearsal,
[42562013163](https://github.com/emulebb/emulebb-rust/actions/runs/42562013163),
passed at `80ccc06e5f7dfc295a1c93b3312c2fa7759a4b62`, including both musl
targets, six native packages/lifecycle lanes, four native Ubuntu/Alpine
image validations, and assembly. Publication jobs were skipped. It proves
that revision's rehearsal, not the eventual Beta 3 candidate.

Current main `edc59a003fff873e26d2c720bf9ca06f4b640871` has green CI and
CodeQL but no verified current-head nightly/candidate run. Its CD result
remains unverified. Scheduled Nightly
[42633861093](https://github.com/emulebb/emulebb-rust/actions/runs/42633861093)
reported success at older `f4527c2d`, but packaging and source-verification
jobs were skipped; metadata-only success is not package evidence.

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
- Assemble mandatory Windows/Linux native assets, checksums, SBOMs, and Linux
  OCI images in dry-run form without invoking any tag-triggered or publishing workflow.
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
- [ ] RUST-CI-035's reviewed workflow graph separates optional platform outcomes
      from required aggregation without bypassing checks. Mandatory hosted CI
      is green at the candidate revision, including policy, format, Clippy,
      Windows/Linux tests, supply-chain checks, CodeQL, and REST/OpenAPI
      conformance.
- [ ] Dry-run release assembly produces the mandatory Windows/Linux and Linux
      OCI asset set with matching checksums, SBOMs, provenance, and revision
      metadata.
- [ ] Mandatory Windows/Linux packaged lifecycle lanes install or unpack,
      start, serve the WebUI, complete the required local transfer smoke, and shut down cleanly.
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

## Windows/Linux Candidate Contract (2026-11-09)

Only Windows and Linux native x64/ARM64 packages plus the required Linux
OCI variants gate Beta 3. macOS, Android/Fire OS, ChromeOS, NAS-specific
certification, and additional Unix qualification continue in parallel.
RUST-CI-035 owns the actual required-job, release-assembly, and artifact
graph split; until it lands, existing workflow enforcement remains active.
Changing prose alone does not turn a failing required job into a pass.

Keep all shared safety, integrity, privacy, policy, provenance, CodeQL,
dependency, and Windows/Linux correctness checks. Every published optional
artifact must independently pass its own qualification; omission of an
optional artifact must be explicit in the immutable candidate manifest.
Candidate invalidation and the separate operator decision to publish remain
unchanged. Earlier six-target rehearsal results remain historical evidence,
not the new candidate's required inventory.

## Soak Readiness Evidence

The maintained default status check found no campaign manifest. The current
long-running soak revision and evidence therefore remain unverified; this
does not establish whether an operator-owned profile is active. Select and
inspect the intended campaign/profile through maintained harness entrypoints
before making a readiness claim. Duration alone does not prove parity. No
VM infrastructure gap was identified by this audit intake.

## Beta 3 Evidence Placement

Retain this item's required Windows/Linux candidate outcome. Other-platform
qualification proceeds in parallel. A static audit, elapsed process time,
or an old passing revision does not establish current-candidate readiness.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_protocol_01.md` section 9.1 / 10.3 (existing): Static audit is not candidate runtime proof. Reuse existing candidate certification and current-head evidence owners; other platforms are parallel and non-gating for the user's Beta 3 scope.
- `PM.md` section release-checklist (existing): The requested release checklist already exists as the candidate certification item. Update its platform scope under the user's Windows/Linux Beta 3 decision; do not create a second release authority.
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section platform-evidence (existing): Windows/Linux are Beta 3 gates. macOS and extended target qualification continue in parallel, with per-target limitations and no stronger support claim than retained runtime evidence.
- `emulebb-rust-prompt_audit_findings_product_direction.md` section delivery-focus (existing): Existing Client/Indexer/Arr sequencing already owns product focus. Beta increments may ship while the broader Client gate stays open; the user now selects Windows/Linux readiness, with other platform work parallel.

### Scoped Follow-up Acceptance

- [ ] Retain exact revisions and artifacts for required Windows/Linux candidate workflows.
- [ ] Do not equate public-soak duration with deterministic parity.
- [ ] One immutable Windows/Linux candidate revision set maps all mandatory checks and artifacts.
- [ ] Optional platform results remain visible and do not become Beta 3 readiness blockers.
- [ ] Required Windows/Linux proof is recorded under the candidate owner.
- [ ] Optional target status distinguishes compile, package and runtime evidence.
- [ ] Candidate review uses the explicitly selected Beta 3 scope and immutable evidence.
- [ ] Later-phase implementation remains behind its gate.
- [ ] Do not treat all optional/design intake as mandatory Beta 3 implementation.
