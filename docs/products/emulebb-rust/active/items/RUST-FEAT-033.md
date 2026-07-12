---
id: RUST-FEAT-033
workflow: github
github_issue: TBD - file on emulebb/emulebb-rust when scheduled
title: Release - first usable release rust-v0.1.0-beta.1 (scope doc, GH release workflow, soak-gated tag)
status: OPEN
priority: Critical
category: feature
labels: [release, packaging, docs, ci]
milestone: release-0.1.0-beta.1
created: 2026-07-05
source: Operator decision 2026-07-05; product-direction reset 2026-07-08; WORKSPACE-POLICY release + network-safety rules
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# RUST-FEAT-033 - First usable release `rust-v0.1.0-beta.1`

## Summary

Ship the first usable emulebb-rust release: an unsigned Windows x64 zip built
by a GitHub Actions release workflow, tagged `rust-v0.1.0-beta.1`, with the
supported, permanent-drop, deferred, and beta-backlog surface documented
unambiguously. Release publication is **workflow-only by operator direction
(2026-07-05)**. The workflow-owned packaging helper requires explicit absolute
target and archive directories outside the source workspace.

## Locked Decisions

- Version `0.1.0-beta.1` (`[workspace.package]`, own semver line decoupled from
  MFC `0.7.x`/`0.8.x` and from the REST `x-contract-version`).
- Tag scheme `rust-vX.Y.Z[-pre.N]`, distinct from MFC `emulebb-v*`.
- Artifact `emulebb-rust-v<version>-windows-x64.zip` + `SHA256SUMS`, always
  unsigned.
- `emulebb-rust-ui` proof is required for beta acceptance. TrackMuleBB is parked
  future controller work and is not tagged, packaged, or required for this first
  Rust prerelease.
- The annotated tag is created only after stock-parity, safety, REST-contract,
  Rust-native UI, and soak evidence review plus an explicit operator go.

## Intended Shape

1. **Scope doc** `docs/RELEASE-SCOPE.md` - the human-facing authority:
   supported surface; SX1 as the only pre-approved permanent drop; explicit
   deferred backlog; beta-allowed parity backlog; platform tier (Windows x64
   release-supported; Linux runtime-proven unpackaged; macOS compile-only).
2. **Version bump** `0.0.3` -> `0.1.0-beta.1` + regenerated `Cargo.lock`.
3. **Release workflow** `.github/workflows/release.yml` on `rust-v*` tags:
   windows runner, `cargo build --release --locked -p emulebb-daemon` with
   default features (assert the `egress-audit` test feature is absent from the
   resolved feature set), stage exe + `emulebb-rust.example.toml` (fail-closed
   VPN defaults verified) + `RELEASE-SCOPE.md` + `LICENSE`, zip + `SHA256SUMS`,
   attach to the GitHub release. Cargo output and staged release artifacts use
   runner-temporary directories rather than `target/` or `dist/` in the source
   checkout.
4. **Release documentation:** version-specific changelog (compact
   one-line-per-item, operational focus) + source-run UI instructions.

## Release Gate (all must hold before the tag)

- [ ] RUST-FEAT-005 fail-closed VPN leak gate passes in CI and candidate
      evidence.
- [ ] RUST-REF-004 re-audits every non-SX1 registry entry with no
      undispositioned P0 or stock-wire-critical findings.
- [ ] RUST-CI-003 OpenAPI conformance/drift gate passes against the Rust-forward
      OpenAPI artifact.
- [ ] `emulebb-rust-ui` pass is green against the candidate daemon: status,
      transfers, uploads, search/download, shared files, servers/Kad, settings,
      logs, and diagnostics.
- [ ] Stock-parity soak evidence covers UDP reask, buddy callback,
      firewall-check, HighID + LowID, finished-file delivery, and sustained REST
      responsiveness. emulebb-mfc may be a frozen witness but is not the product
      parity target.
- [ ] `RELEASE-SCOPE.md` matches the re-audit dispositions and does not imply
      full stock parity where beta backlog remains.
- [ ] Operator gives the explicit tagging go.

## Notes

- Release-output hygiene landed in emulebb-rust commit `0d12f91`; the policy
  checker and packaging-helper tests guard the external-output requirement.
- The INDEX scope note "emulebb-rust is out of RC2 ship scope" remains true for
  the MFC RC2 train; this item creates the rust client's own release gate.
- Docker/GHCR (RUST-FEAT-006) intentionally stays out of this release.
