---
id: RUST-FEAT-033
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/20
title: Release - first usable release rust-v0.1.0-beta.1 (scope doc, GH release workflow, WebUI proof, soak-gated tag)
status: IN_PROGRESS
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

Ship the first usable emulebb-rust release: unsigned Windows ZIPs, Linux
DEBs/AppImages, macOS app-in-DMGs (x64 and ARM64 on each OS), and a two-arch
GHCR image built by GitHub Actions, tagged `rust-v0.1.0-beta.1`, with the
supported, permanent-drop, deferred, and beta-backlog surface documented
unambiguously. Release publication is **workflow-only by operator direction
(2026-07-05)**. The workflow-owned packaging helper requires explicit absolute
target and archive directories outside the source workspace.

## Locked Decisions

- Version `0.1.0-beta.1` (`[workspace.package]`, own semver line decoupled from
  MFC `0.7.x`/`0.8.x` and from the REST `x-contract-version`).
- Tag scheme `rust-vX.Y.Z[-pre.N]`, distinct from MFC `emulebb-v*`.
- Native artifacts cover x64 and ARM64 on Windows, Linux, and macOS; all are
  unsigned, and macOS DMGs are unnotarized. The combined set has `SHA256SUMS`,
  manifests, and SBOMs.
- Embedded SPA WebUI proof is required for beta acceptance. TrackMuleBB is
  parked future controller work and is not tagged, packaged, or required for
  this first Rust prerelease.
- The annotated tag is created only after stock-parity, safety, REST-contract,
  WebUI, and soak evidence review plus an explicit operator go.
- The Rust REST contract remains unstable between betas. Native VPN-safe claims
  are deferred; direct routing is explicit and Docker-over-Gluetun is the beta
  VPN deployment with a separate fail-closed test.
- Both x64 deep campaigns must finish a small approved Linux document; one
  must also finish a Linux ISO. Local deterministic Rust upload is sufficient,
  while a stock-identifying public peer must supply accepted download bytes.

## Intended Shape

1. **Scope doc** `RELEASE-SCOPE.md` records the usable eD2K/Kad/WebUI surface,
   omissions, deferred work, unstable REST API, selected-route safety, and the
   six native package targets plus the Docker image.
2. **Release workflow** builds and retains candidate artifacts on manual runs;
   after the separate approved tag, all six native package jobs and two-arch
   image jobs must pass before publication. Output stays outside source trees.
3. **Release documentation** includes a version-specific changelog,
   first-run/API-key instructions, unsigned macOS launch steps, and the isolated
   Gluetun deployment example.

## Release Gate (all must hold before the tag)

- [x] Docker-over-Gluetun tunnel-down proof records zero off-tunnel P2P egress;
      no native VPN-safe claim is made.
- [x] RUST-REF-004 re-audits every non-SX1 registry entry with no
      undispositioned P0 or stock-wire-critical findings.
- [x] RUST-CI-003 OpenAPI conformance/drift gate passes against the Rust-forward
      OpenAPI artifact.
- [x] The packaged embedded SPA WebUI is green against the candidate daemon:
      status, transfers, uploads, search/download, shared files, servers/Kad,
      settings, logs, and diagnostics.
- [x] Stock-parity soak evidence covers UDP reask, buddy callback,
      firewall-check, HighID + LowID, finished-file delivery, and sustained REST
      responsiveness. emulebb-mfc may be a frozen witness but is not the product
      parity target.
- [x] Fresh no-share direct campaigns on Windows x64 and WSL Ubuntu x64 each
      finish an approved small Linux document; one also finishes an approved
      Linux ISO, with exact SHA-256 verification and stock-identifying peer
      file-block bytes. Local Rust/MFC upload and download are deterministic.
- [x] Each of the six native packages passes install/launch, every current
      WebUI panel, local transfer, and shutdown smoke. The amd64/arm64 image
      passes ownership, persistence, and Gluetun isolation checks.
- [x] `RELEASE-SCOPE.md` matches the re-audit dispositions and does not imply
      full stock parity where beta backlog remains.
- [ ] Operator gives the explicit tagging go.

## Current Candidate Evidence (2026-09-26)

- GitHub issue `emulebb/emulebb-rust#20` and milestone
  `release-0.1.0-beta.1` now own the release decision; this document remains the
  engineering evidence record.
- RUST-FEAT-005 passed the isolated Docker-over-Gluetun tunnel-down campaign:
  the positive sensor was proven, the P2P bind remained pinned to the tunnel,
  and packet capture recorded zero off-tunnel P2P packets after tunnel loss.
- RUST-REF-004 closed with all 10 non-SX1 registry entries dispositioned and no
  undispositioned release blocker. The release scope and beta limitations use
  those dispositions and make no native VPN-safety or full-parity claim.
- The packaged embedded SPA passed unit/e2e/build gates and a Windows live
  browser proof against the candidate daemon across all 14 current panels. The
  transfer workflow observed an active nonzero-progress transfer and retained
  no public result names, terms, hashes, or paths.
- The Windows x64 fresh direct campaign passed HighID, Kad connectivity,
  stock-identifying accepted file bytes, exact document/ISO SHA-256 delivery,
  sustained REST diagnostics, and graceful shutdown. The final WSL Ubuntu x64
  rerun on Rust commit `5c5bf7f` passed at retained run `20260926T092121Z`:
  eD2K and Kad connected, 239 Kad contacts were observed, all 20 probes found
  sources, two approved PDF deliveries passed exact size and SHA-256
  verification, 9,728,000 stock-identifying payload bytes were accepted,
  108,131 diagnostic records contained zero malformed records or error events,
  and teardown was graceful. No public result names, hashes, or paths are
  retained here.
- The six-hour Windows direct campaign recorded live UDP reask, buddy callback,
  Kad firewall-check, HighID, finished-file delivery, and sustained REST
  evidence. The deterministic private parity campaign passed all 55 cases again
  on `e5e9436`,
  including LowID upload-queue, callback-session, core callback-route, Kad
  firewall runtime, and server-callback decode coverage.
- Hosted CI run `36232498272` passed on exact Rust candidate `5c5bf7f` across
  Windows, Linux, and macOS, including policy, format, Clippy, cargo-deny, and
  the live REST/OpenAPI gate. Its retained Linux report matched all 100 OpenAPI
  routes to the runtime registry, exercised all 78 safe routes plus SSE with
  zero failures, kept public networks disabled and REST on loopback, and shut
  down gracefully.
- Manual release-candidate run `36234229443` passed on exact Rust candidate
  `5c5bf7f` without publishing. All six Windows/Linux/macOS x64/ARM64 native
  packages launched from fresh profiles, served the embedded SPA, exercised
  all 14 current panel backends, reported REST status, and shut down
  gracefully. The linux/amd64 and linux/arm64 OCI candidate passed first-run
  WebUI, UID/GID `1234:1235`, `/config` and `/data` ownership/persistence, and
  zero-published-port checks. Both publication jobs were intentionally skipped.
- Rust candidate `5c5bf7f`, tooling evidence baseline `914d02a`, and build-test
  harness `d7a59c8` were clean, synchronized with their upstream `main`
  branches, and used for the final evidence review. The release workflow pins
  the exact tooling and harness revisions that supplied the reviewed public
  release documents and smoke logic.
- Tag creation and publication remain explicitly unauthorized until every open
  checkbox above is closed and the operator separately gives the tagging go.

## Historical Gate Snapshot (2026-07-22)

This snapshot predates the 2026-09-25 six-target and Docker beta decisions.
It is historical evidence, not the current release gate or sign-off.

| Gate | Current status | Evidence / next proof |
| --- | --- | --- |
| Regular headless persisted launch | PASS for current soak profile | `repos/emulebb-build-tests/scripts/start-rust-soak-profile.py --describe` and the staged `launch-client-here.py` resolve to the regular `emulebb-rust.exe` with the persisted profile. The tracked `--install-launchers` path now refreshes `launch-client-here.py` from `emule_test_harness.rust_profile_client_launcher` and writes a disabled `launch-UI-here.py` stub. On 2026-07-22 the installed launcher refused a second daemon, requested ED2K/Kad startup on the running regular daemon, and reported 44085 upload-capable shared files with the hash backlog still draining. The native Slint UI is not a beta launch path. |
| Early network connection | PASS for current persisted profile | The repeatable `repos/emulebb-build-tests/scripts/rust-soak-control.py early-connect-proof` gate now requests normal P2P startup, polls immediately, writes a sanitized retained report, and exits nonzero unless ED2K is connected with HighID and Kad is connected before the bounded timeout. On 2026-07-22 it passed against the regular persisted daemon in 3.148 s and wrote `reports/rust-early-connect-proof/rust-early-connect-proof.latest.json`. |
| Shared library persistence | PARTIAL | The 2026-07-22 persisted profile recovery restored 2534 accessible shared roots from the persisted `shareddir.dat`, and conformance no longer clears them. The retained `shared-reload-settled-proof` gate now waits for stable root/item/shared-file counts with no active hashing or reload before clean restart proof. A short live run on 2026-07-22 wrote `reports/rust-shared-reload-settled-proof/rust-shared-reload-settled-proof.latest.json` and correctly failed while hashing was still active: 2534 roots, 2617 items, 51083 shared files, `plannedHashCount=16980`, `hashedCount=3011`, `hashingCount=13969`, `failedHashCount=0`, reload still running/pending. The release gate still needs this proof to pass and then a clean restart/reload proof with hashing already settled. |
| Public upload path | PASS for current live/profile proof; keep monitoring | The regular persisted daemon showed fresh public upload throughput after the 2026-07-22 shared-root recovery: `knownUploadedBytes` rose from 507176960 to 508575907 between 16:24:23Z and 16:32:29Z, upload requests/accepts rose from 2777 to 2782, and a sample showed 13.13 KiB/s while ED2K/Kad stayed connected. After the 2026-07-22 orchestrated regular rebuild/restart, a direct persisted-profile sample showed `uploadSpeedKiBps=498.44` with ED2K HighID and Kad connected while republish was still maturing. Deterministic regular-exe Rust-Rust upload proof also passed at `rust-local-upload/20260722T181737Z` with 4 MiB completed/delivered, max active uploads 1, max upload speed 573.857 KiB/s, and delivered-path verification. After the regular-log hardening rebuild, deterministic regular-exe proof passed again at `rust-local-upload/20260722T192636Z` with 4 MiB completed/delivered, max active uploads 1, max upload speed 481.283 KiB/s, 60 observed upload rows, and delivered-path verification. The retained profile watcher now runs Rust-only by default, survives transient REST sample failures, and on 2026-07-22 wrote a fresh sample with ED2K HighID, Kad connected, visibility at 22.44%, and no stale parity-monitor repair recommendation. |
| Download and finished-file delivery | PASS for current live/profile proof | Fresh deterministic regular-exe Rust-Rust proof passed at `rust-local-upload/20260722T164553Z`: the leecher added the ED2K link paused, resumed through REST, completed 4 MiB, and verified the delivered path/bytes. A bounded public persisted-profile proof at `reports/rust-public-search-download-proof.latest.json` found a sanitized safe public candidate, added it paused, resumed it, and observed source acquisition. The 2026-07-22 hardened public proof now fails on source count alone and tries bounded safe candidates until byte movement or completion. After Rust network search rows were fixed to expose decoded complete-source counts, the rebuilt regular daemon passed the strict retained proof at `reports/rust-public-search-download-proof/rust-public-search-download-proof.strict-complete.latest.json`: the sanitized candidate had `sources=2` and `completeSources=2`, completion was required, final `completedBytes=sizeBytes=6738525`, `progress=1.0`, `state=completed`, `deliveredPathPresent=true`, and `deliveredFileExists=true`. |
| Search and publish | PARTIAL | Current soak samples show ED2K visibility and Kad publish counters progressing. The retained `publish-visibility-proof` gate now waits for ED2K connected/HighID, mature ED2K visibility, Kad connected, Kad publish gate allowed, and observed Kad keyword/source publish totals. A short live run on 2026-07-22 wrote `reports/rust-publish-visibility-proof/rust-publish-visibility-proof.latest.json` and correctly failed only on `ed2kVisibilityMature`: ED2K was connected with HighID, Kad was connected/gate-allowed/publishing, Kad keyword/source published totals were 1603/41, but ED2K visibility was still 6.26% with 47924 pending entries. The public persisted-profile probes found safe candidates from ignored operator-local terms without retaining names, hashes, paths, or terms in tracked output; the strict complete-source proof completed with delivered-file verification. The release gate still needs publish visibility to mature and a clean restart/reload proof after hashing settles. |
| REST/OpenAPI conformance | PASS for current candidate | `check-rust-rest-openapi-responses.py --rest-coverage-budget contract` passed against the live persisted daemon on 2026-07-22 after the Rust OpenAPI contract and conformance harness were aligned with current response shapes. The harness now skips live-disruptive network, shared-root replacement, server mutation, Kad mutation, log clear, and search-delete routes during contract smoke. |
| Embedded SPA WebUI | PASS for current live/profile proof | Mocked WebUI unit/e2e/build gates are green after the polling reduction. On 2026-07-22 `python -m emule_workspace build clients --client emulebb-rust --config Release --platform x64 --build-output-mode ErrorsOnly` staged the current packaged WebUI beside the regular daemon (`index-Bcfp4OWs.js`). The reusable `scripts/rust-webui-live-proof.py` proof passed against the persisted regular daemon and wrote `reports/rust-webui-live-proof/rust-webui-live-proof.latest.json`: the default-tab steady window made only 6 `snapshot?limit=500` API polls over 18 s, the stale secondary-endpoint polling check passed, browser diagnostics were clean, and the proof visited Overview, Transfers, Search, Sharing, Shared Files, Uploads, Network, Servers, Kad, Categories, Friends, Settings, Diagnostics, and Logs. The retained `transferWorkflow` check now verifies public download progress without retaining names or hashes; the current run showed 2 transfer rows, 1 active nonzero-progress row, and no empty table. The same retained proof now includes a steady browser main-thread budget: Chrome reported 0.130454 s `TaskDuration` over 18.004 s, a 0.0072 busy ratio against the 0.25 beta limit. |
| Regular logs and diagnostics | PASS for current candidate | The repeatable `repos/emulebb-build-tests/scripts/rust-soak-control.py regular-log-proof` gate writes a sanitized retained report and exits nonzero when beta diagnostic categories are missing. The regular daemon now keeps a 2000-entry REST log ring and emits a 10 s regular summary with VPN Guard HTTP public IPv4/STUN probe state, ED2K/Kad, publish, upload, download, transfer, and shared-hashing counters, without diagnostics-only binaries. After the 2026-07-22 regular rebuild/restart, `early-connect-proof` passed in 47.332 s and `regular-log-proof` passed at `reports/rust-regular-log-proof/rust-regular-log-proof.latest.json`: the recent regular log window contained startup, VPN Guard HTTP public IPv4, STUN, ED2K, Kad, publish, upload, and download categories; `/status` plus persisted metadata proved ED2K HighID, Kad connected, 589932079 uploaded bytes, 2951 upload accepts, 47142 completed known files, and 47154 transfers. |
| VPN leak gate | BLOCKER | RUST-FEAT-005 remains release-blocking: CI/socket-truth plus operator wire-truth tunnel-down proof must show zero off-tunnel eD2K/Kad traffic. |
| Stock-wire parity re-audit | BLOCKER | RUST-REF-004/RUST-CI-002 must leave no undispositioned P0 or stock-wire-critical finding before tag. |
| Packaging workflow | PARTIAL | Versioning and release-scope decisions are in place. The orchestrated Rust client build stages the regular exe and packaged WebUI together under the canonical tools path, and `python -m emule_workspace package-emulebb-rust --skip-build --config Release --platform x64 --build-output-mode ErrorsOnly` now creates the unsigned local candidate under `%EMULEBB_WORKSPACE_OUTPUT_ROOT%\release\rust-v0.1.0-beta.1\`. On 2026-07-22 the local candidate wrote `emulebb-rust-v0.1.0-beta.1-windows-x64.zip`, `.manifest.json`, `.sbom.spdx.json`, and `SHA256SUMS`; the package content gate reported 9 entries: regular `emulebb-rust.exe`, packaged WebUI assets, example settings, `LICENSE`, generated package `README.md`, `RELEASE-SCOPE.md`, and `SBOM.spdx.json`. The package excludes `emulebb-rust-ui.exe` and diagnostics binaries. The local orchestrated zip SHA256 was `c0a47eda35734d6f016db35642149c135aba121d46a2942df8ca8e0f8113ad74`. The repo-local `rust-v*` release workflow now packages from the canonical staged regular runtime, checks out the release-scope doc, uploads the zip/manifest/SBOM/SHA256SUMS assets, and prunes stale Slint UI staging artifacts. A post-commit probe from Rust commit `77a803f` wrote the same 9-entry shape under `%EMULEBB_WORKSPACE_OUTPUT_ROOT%\release\rust-v0.1.0-beta.1-workflow-packager-probe-20260722-current\`; its zip SHA256 was `9ce12cc136308371f8b0be836d12690a7e6782c1410e9669a7862531bb256fff`, manifest SHA256 `2cca97ecc95948f58381e3d9c3dab00913183120ebbd808e4f8a35d105544b8b`, and SBOM SHA256 `79407251ecefb0c1e78fabcc7b79dab8ae71995e865d42dcf9ea4ce54fed7336`. The release tag/GitHub release run still needs operator approval and final release evidence. |

## Next Core Feature Focus

The next coding/testing priority is turning the persisted shared-library state
into a clean restart/reload proof after hashing settles, while continuing public
download/search monitoring on the regular daemon.
Work this as small slices:

1. Keep the sanitized `public-search-download-proof`, `publish-visibility-proof`,
   `rust-webui-live-proof`, and `shared-reload-settled-proof` harnesses on the
   regular daemon path as the current download/search, publish, embedded WebUI,
   and shared-library gates.
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
- Docker/GHCR (RUST-FEAT-006) is now part of this beta's release gate.
