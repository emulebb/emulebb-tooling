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
| Regular headless persisted launch | PASS for current soak profile | `repos/emulebb-build-tests/scripts/start-rust-soak-profile.py --describe` and the staged `launch-client-here.py` resolve to the regular `emulebb-rust.exe` with the persisted profile. The tracked `--install-launchers` path now refreshes `launch-client-here.py` from `emule_test_harness.rust_profile_client_launcher` and writes a disabled `launch-UI-here.py` stub. On 2026-07-22 the installed launcher refused a second daemon, requested ED2K/Kad startup on the running regular daemon, and reported 44085 upload-capable shared files with the hash backlog still draining. The native Slint UI is not a beta launch path. |
| Early network connection | PASS for current persisted profile | The repeatable `repos/emulebb-build-tests/scripts/rust-soak-control.py early-connect-proof` gate now requests normal P2P startup, polls immediately, writes a sanitized retained report, and exits nonzero unless ED2K is connected with HighID and Kad is connected before the bounded timeout. On 2026-07-22 it passed against the regular persisted daemon in 3.148 s and wrote `reports/rust-early-connect-proof/rust-early-connect-proof.latest.json`. |
| Shared library persistence | PARTIAL | The 2026-07-22 persisted profile recovery restored 2534 accessible shared roots from the persisted `shareddir.dat`, and conformance no longer clears them. The accidental live `replaceSharedDirectories` conformance call forced a rehash/republish pass, so the release gate still needs a clean restart/reload proof with hashing already settled. |
| Public upload path | PASS for current live/profile proof; keep monitoring | The regular persisted daemon showed fresh public upload throughput after the 2026-07-22 shared-root recovery: `knownUploadedBytes` rose from 507176960 to 508575907 between 16:24:23Z and 16:32:29Z, upload requests/accepts rose from 2777 to 2782, and a sample showed 13.13 KiB/s while ED2K/Kad stayed connected. After the 2026-07-22 orchestrated regular rebuild/restart, a direct persisted-profile sample showed `uploadSpeedKiBps=498.44` with ED2K HighID and Kad connected while republish was still maturing. Deterministic regular-exe Rust-Rust upload proof also passed at `rust-local-upload/20260722T181737Z` with 4 MiB completed/delivered, max active uploads 1, max upload speed 573.857 KiB/s, and delivered-path verification. After the regular-log hardening rebuild, deterministic regular-exe proof passed again at `rust-local-upload/20260722T192636Z` with 4 MiB completed/delivered, max active uploads 1, max upload speed 481.283 KiB/s, 60 observed upload rows, and delivered-path verification. The retained profile watcher now runs Rust-only by default, survives transient REST sample failures, and on 2026-07-22 wrote a fresh sample with ED2K HighID, Kad connected, visibility at 22.44%, and no stale parity-monitor repair recommendation. |
| Download and finished-file delivery | PARTIAL | Fresh deterministic regular-exe Rust-Rust proof passed at `rust-local-upload/20260722T164553Z`: the leecher added the ED2K link paused, resumed through REST, completed 4 MiB, and verified the delivered path/bytes. A bounded public persisted-profile proof at `reports/rust-public-search-download-proof.latest.json` found a sanitized safe public candidate, added it paused, resumed it, and observed source acquisition. The 2026-07-22 hardened public proof now fails on source count alone and tries bounded safe candidates until byte movement or completion. Strict complete-source runs for `documents` and `generic_open` still failed with `reason=no-safe-public-candidate`, but the relaxed complete-source retained proof at `reports/rust-public-search-download-proof/rust-public-search-download-proof.relaxed-complete.latest.json` selected one sanitized candidate with `completeSources=0`, added it paused at 0 bytes, resumed it, and observed 184320 downloaded bytes with 2 sources and 1 transferring source. The same transfer later completed and the retained sanitized report at `reports/rust-public-search-download-proof/rust-public-transfer-completion.latest.json` shows `completedBytes=sizeBytes=6738525`, `progress=1.0`, `state=completed`, `deliveredPathPresent=true`, and `deliveredFileExists=true`. The beta tag still needs strict complete-source success or an explicit gate decision for byte-moving/completing `completeSources=0` candidates, plus a clean restart/reload proof after hashing settles. |
| Search and publish | PARTIAL | Current soak samples show ED2K visibility and Kad publish counters progressing. The 2026-07-22 public persisted-profile probes found safe candidates from ignored operator-local terms without retaining names, hashes, paths, or terms in tracked output. Source count alone remains weak evidence: the hardened harness requires byte movement or completion, records sanitized progress JSONL, exposes no-safe-candidate as a failing executable gate, and retained a relaxed complete-source proof that moved 184320 bytes before completing with delivered-file verification. The release gate still needs stronger public discoverability evidence through a strict complete-source pass or an explicit beta decision that byte-moving/completing zero-complete-source public candidates are acceptable. |
| REST/OpenAPI conformance | PASS for current candidate | `check-rust-rest-openapi-responses.py --rest-coverage-budget contract` passed against the live persisted daemon on 2026-07-22 after the Rust OpenAPI contract and conformance harness were aligned with current response shapes. The harness now skips live-disruptive network, shared-root replacement, server mutation, Kad mutation, log clear, and search-delete routes during contract smoke. |
| Embedded SPA WebUI | PARTIAL | Mocked WebUI unit/e2e/build gates are green after the polling reduction. On 2026-07-22 `python -m emule_workspace build clients --client emulebb-rust --config Release --platform x64 --build-output-mode ErrorsOnly` staged the current packaged WebUI beside the regular daemon (`index-BPwZs_jh.js`). The reusable `scripts/rust-webui-live-proof.py` proof passed against the persisted regular daemon and wrote `reports/rust-webui-live-proof/rust-webui-live-proof.latest.json`: the default-tab steady window made only 6 `snapshot?limit=500` API polls over 18 s, the stale secondary-endpoint polling check passed, browser diagnostics were clean, and the proof visited Overview, Transfers, Search, Sharing, Shared Files, Uploads, Network, Servers, Kad, Categories, Friends, Settings, Diagnostics, and Logs. The gate remains partial until the WebUI proof also covers a successful public search/download byte-progress or completed-delivery workflow. |
| Regular logs and diagnostics | PASS for current candidate | The repeatable `repos/emulebb-build-tests/scripts/rust-soak-control.py regular-log-proof` gate writes a sanitized retained report and exits nonzero when beta diagnostic categories are missing. The regular daemon now keeps a 2000-entry REST log ring and emits a 10 s regular summary with VPN Guard HTTP public IPv4/STUN probe state, ED2K/Kad, publish, upload, download, transfer, and shared-hashing counters, without diagnostics-only binaries. After the 2026-07-22 regular rebuild/restart, `early-connect-proof` passed in 47.332 s and `regular-log-proof` passed at `reports/rust-regular-log-proof/rust-regular-log-proof.latest.json`: the recent regular log window contained startup, VPN Guard HTTP public IPv4, STUN, ED2K, Kad, publish, upload, and download categories; `/status` plus persisted metadata proved ED2K HighID, Kad connected, 589932079 uploaded bytes, 2951 upload accepts, 47142 completed known files, and 47154 transfers. |
| VPN leak gate | BLOCKER | RUST-FEAT-005 remains release-blocking: CI/socket-truth plus operator wire-truth tunnel-down proof must show zero off-tunnel eD2K/Kad traffic. |
| Stock-wire parity re-audit | BLOCKER | RUST-REF-004/RUST-CI-002 must leave no undispositioned P0 or stock-wire-critical finding before tag. |
| Packaging workflow | PARTIAL | Versioning and release-scope decisions are in place. The orchestrated Rust client build now stages the regular exe and packaged WebUI together under the canonical tools path. The Windows x64 zip workflow and release artifact contents still need candidate evidence before operator tag approval. |

## Next Core Feature Focus

The next coding/testing priority is turning the public search/download proof
from a relaxed complete-source success into a strict gate decision, because both
local and public persisted-profile delivery now have fresh completion evidence
while the strict complete-source probe still lacks a safe candidate.
Work this as small slices:

1. Keep the sanitized `public-search-download-proof` harness on the regular
   daemon path and continue strict complete-source probes for a cleaner gate.
2. Preserve the privacy boundary: operator-owned terms and public result names,
   hashes, and paths stay out of tracked docs, tests, and retained reports.
3. Treat `sources>0` without transfer bytes or `sourcesTransferring` as weak
   evidence only; fix the first reproducible Rust core or harness failure with
   focused tests before another live run.

## Notes

- Release-output hygiene landed in emulebb-rust commit `0d12f91`; the policy
  checker and packaging-helper tests guard the external-output requirement.
- The INDEX scope note "emulebb-rust is out of RC2 ship scope" remains true for
  the MFC RC2 train; this item creates the rust client's own release gate.
- Docker/GHCR (RUST-FEAT-006) intentionally stays out of this release.
