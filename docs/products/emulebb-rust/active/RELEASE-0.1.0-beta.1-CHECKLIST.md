# emulebb-rust 0.1.0-beta.1 Release Evidence Checklist

This is the single operator checklist for the `rust-v0.1.0-beta.1` candidate.
The selected Rust commit is immutable for this evidence cycle. Any source or
release-workflow change selects a new candidate and invalidates evidence below.

**Status:** exact-candidate evidence in progress; tag and publication are not
approved by this checklist.

## Candidate Identity

| Component | Selected revision | Purpose |
|---|---|---|
| `emulebb-rust` | [`28a0703561f135b03ffcca94527ceb538ef9012e`](https://github.com/emulebb/emulebb-rust/commit/28a0703561f135b03ffcca94527ceb538ef9012e) | Immutable beta candidate |
| `emulebb-build` | [`80e2a1cae4cdd1b56ffba75685466c1f4ceabe12`](https://github.com/emulebb/emulebb-build/commit/80e2a1cae4cdd1b56ffba75685466c1f4ceabe12) | Orchestration and packaging |
| `emulebb-build-tests` | [`ecd19103d4a3bab615d47b89d195594501d7b0b4`](https://github.com/emulebb/emulebb-build-tests/commit/ecd19103d4a3bab615d47b89d195594501d7b0b4) | Live, package, and image evidence harnesses |
| `emulebb-tooling` | [`8035fc8ad161917bdaf97306e0c4a41eebe52437`](https://github.com/emulebb/emulebb-tooling/commit/8035fc8ad161917bdaf97306e0c4a41eebe52437) | Frozen release notes, changelog, and OpenAPI contract |

## Final Evidence

- [x] Candidate identity is selected, pushed, and pinned by full commit SHA in
  the CI and release workflows.
- [ ] Hosted CI succeeds for the selected candidate:
  [workflow run 36980088250](https://github.com/emulebb/emulebb-rust/actions/runs/36980088250).
- [ ] The manually dispatched, non-publishing release workflow succeeds for the
  selected candidate:
  [workflow run 36980108964](https://github.com/emulebb/emulebb-rust/actions/runs/36980108964).
- [ ] The exact-candidate Windows campaign succeeds. Campaign ID and report:
  pending.
- [ ] The exact-candidate WSL campaign succeeds. Campaign ID and report:
  pending.
- [ ] The fail-closed Gluetun proof succeeds. Proof ID and report: pending.
- [ ] All release packages come from the selected candidate and their SHA-256
  hashes are recorded below.
- [ ] Every package manifest identifies the selected candidate and pinned
  support revisions; manifest and SBOM hashes verify against `SHA256SUMS`.
- [ ] `emulebb-rust`, `emulebb-build`, `emulebb-build-tests`, and
  `emulebb-tooling` are clean and synchronized with their remotes at final
  review.
- [x] Final operator-facing release text is frozen in
  [release notes](../RELEASE-0.1.0-beta.1-NOTES.md) and the
  [changelog](../RELEASE-0.1.0-beta.1-CHANGELOG.md) at tooling revision
  `8035fc8ad161917bdaf97306e0c4a41eebe52437`.
- [ ] No unresolved beta-blocking security, packaging, or protocol finding
  remains.

## Package Hashes

Exact-candidate packages and `SHA256SUMS` are pending the release workflow.
Packages from earlier commits are test artifacts and are not release evidence.

## Publication Boundary

Completion of this checklist proves release readiness only. Creating
`rust-v0.1.0-beta.1`, publishing the GitHub prerelease, and pushing the GHCR
image require a separate explicit operator instruction.
