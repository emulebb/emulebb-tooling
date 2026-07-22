---
id: RUST-FEAT-033
workflow: github
github_issue: TBD - file on emulebb/emulebb-rust when scheduled
title: Release - first usable release rust-v0.1.0-beta.1 (scope doc, GH release workflow, WebUI proof, soak-gated tag)
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
- Embedded SPA WebUI proof is required for beta acceptance. TrackMuleBB is
  parked future controller work and is not tagged, packaged, or required for
  this first Rust prerelease.
- The annotated tag is created only after stock-parity, safety, REST-contract,
  WebUI, and soak evidence review plus an explicit operator go.

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
   one-line-per-item, operational focus) + source-run WebUI instructions.

## Release Gate (all must hold before the tag)

- [ ] RUST-FEAT-005 fail-closed VPN leak gate passes in CI and candidate
      evidence.
- [ ] RUST-REF-004 re-audits every non-SX1 registry entry with no
      undispositioned P0 or stock-wire-critical findings.
- [ ] RUST-CI-003 OpenAPI conformance/drift gate passes against the Rust-forward
      OpenAPI artifact.
- [ ] The packaged embedded SPA WebUI is green against the candidate daemon:
      status, transfers, uploads, search/download, shared files, servers/Kad,
      settings, logs, and diagnostics.
- [ ] Stock-parity soak evidence covers UDP reask, buddy callback,
      firewall-check, HighID + LowID, finished-file delivery, and sustained REST
      responsiveness. emulebb-mfc may be a frozen witness but is not the product
      parity target.
- [ ] `RELEASE-SCOPE.md` matches the re-audit dispositions and does not imply
      full stock parity where beta backlog remains.
- [ ] Operator gives the explicit tagging go.

## Current Beta Gate Status (2026-07-22)

This is the working gate map for turning the broad beta goal into executable
evidence. It is not release sign-off; unchecked items remain blockers for the
`rust-v0.1.0-beta.1` tag.

| Gate | Current status | Evidence / next proof |
| --- | --- | --- |
| Regular headless persisted launch | PASS for current soak profile | `repos/emulebb-build-tests/scripts/start-rust-soak-profile.py --describe` and the staged `launch-client-here.py` resolve to the regular `emulebb-rust.exe` with the persisted profile. The native Slint UI is not a beta launch path. |
| Early network connection | PARTIAL | Current persisted soak samples show ED2K connected with High ID and Kad connected. Convert this into a repeatable early-connect gate that fails fast instead of waiting for long soak windows. |
| Shared library persistence | PARTIAL | Current persisted soak profile reloads 64k+ known/shared files without active hashing. Keep this as a restart/reload gate, not just a one-sample observation. |
| Public upload path | PASS for current live soak; keep monitoring | Current persisted soak samples show active public uploads and non-zero upload speed. The local deterministic upload soak also proves a regular-exe upload path; retain both live and local proof in the release bundle. |
| Download and finished-file delivery | BLOCKER until fresh candidate proof exists | Existing history has multiple live-wire download fixes and completions, but the beta tag needs a current candidate proof that adds a file, downloads, resumes as needed, and delivers by name into `incomingDir` or a category path. |
| Search and publish | PARTIAL | Current soak samples show ED2K visibility and Kad publish counters progressing. The release gate still needs a current search/download proof and a disposition for any weak discoverability evidence. |
| REST/OpenAPI conformance | PASS for current candidate | `check-rust-rest-openapi-responses.py --rest-coverage-budget contract` passed against the live persisted daemon on 2026-07-22 after the Rust OpenAPI contract and conformance harness were aligned with current response shapes. |
| Embedded SPA WebUI | PARTIAL | Mocked WebUI unit/e2e/build gates are green after the polling reduction. Candidate proof still needs the packaged WebUI against the persisted daemon, including status, transfers, uploads, search/download, shared files, servers/Kad, settings, logs, and diagnostics with acceptable idle CPU. |
| Regular logs and diagnostics | PARTIAL | Regular logs now include VPN Guard HTTP/STUN probe attempts and connection/upload state. Before tag, verify a regular-exe log excerpt is enough to diagnose startup, network probe, ED2K/Kad, publish, upload, and download failures without the diagnostics binary. |
| VPN leak gate | BLOCKER | RUST-FEAT-005 remains release-blocking: CI/socket-truth plus operator wire-truth tunnel-down proof must show zero off-tunnel eD2K/Kad traffic. |
| Stock-wire parity re-audit | BLOCKER | RUST-REF-004/RUST-CI-002 must leave no undispositioned P0 or stock-wire-critical finding before tag. |
| Packaging workflow | PARTIAL | Versioning and release-scope decisions are in place. The Windows x64 zip workflow and release artifact contents still need candidate evidence before operator tag approval. |

## Next Core Feature Focus

The next coding/testing priority is the download gate, because uploads and
connectivity have current live evidence while download/resume/delivery is the
largest core user-facing requirement without fresh candidate proof. Work this
as small slices:

1. Add or identify a repeatable persisted-profile download smoke that uses the
   regular daemon and records add-link, source discovery, byte progress, resume,
   and delivered-file evidence.
2. Run it against the current staged regular executable.
3. Fix the first reproducible failure in the Rust core or harness, with focused
   tests before another live run.

## Notes

- Release-output hygiene landed in emulebb-rust commit `0d12f91`; the policy
  checker and packaging-helper tests guard the external-output requirement.
- The INDEX scope note "emulebb-rust is out of RC2 ship scope" remains true for
  the MFC RC2 train; this item creates the rust client's own release gate.
- Docker/GHCR (RUST-FEAT-006) intentionally stays out of this release.
