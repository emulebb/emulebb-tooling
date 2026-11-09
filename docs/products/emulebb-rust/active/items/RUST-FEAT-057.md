---
id: RUST-FEAT-057
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/227
title: Publish portable Linux musl builds for x64 and ARM64
status: OPEN
priority: Major
category: feature
labels: [rust, linux, musl, packaging, portability, arm64]
milestone: post-beta-polish
created: 2026-11-04
source: operator-approved universal-platform expansion 2026-11-04
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/227. This local document owns the durable engineering contract.

# RUST-FEAT-057 - Publish portable Linux musl builds for x64 and ARM64

## Summary

Add supported `x86_64-unknown-linux-musl` and
`aarch64-unknown-linux-musl` release lanes so eMuleBB Rust runs on Alpine and
minimal Linux systems without a host glibc dependency. Publish portable
archives containing the daemon, browser WebUI, documentation, checksums, SBOM,
and exact build provenance.

## Current State

- The workstream adds static musl `.tar.zst` packages on x64 and ARM64 alongside
  the existing glibc DEB/AppImage assets.
- Ubuntu/glibc and Alpine/musl OCI variants each contain x64 and ARM64 manifests.
  Local WSL/Docker gates cover both variants; GitHub independently validates
  each image on the matching native runner CPU.
- Bundled SQLite and the MiniUPnPc and libpcpnatpmp C sources make this a native
  cross-toolchain lane, not merely an additional Rust target triple.

## Integration Evidence

The 2026-11-09 non-publishing
[candidate run](https://github.com/emulebb/emulebb-rust/actions/runs/42551615785)
used source `24f6fd051e3c6cf60b99b99f4a45e97713c03be0` and workflow control
`3883dc125dc63d58896f302797ddf4189af246ea`. All six desktop package producers
and their lifecycle smokes, both full native musl package/test lanes, both
multiarch OCI producers, and all four native image lifecycle/security jobs
passed. Image evidence includes SPDX inventories and the required fixable
HIGH/CRITICAL vulnerability gate. Local emulation is not substituted for the
hosted native ARM64 evidence.

Final assembly in that run failed on an obsolete copy of versioned release
notes from the tooling checkout. No publication ran. Rust
[`80ccc06e`](https://github.com/emulebb/emulebb-rust/commit/80ccc06e5f7dfc295a1c93b3312c2fa7759a4b62)
replaces that copy with a shared source-history document preflight in local
pre-push, required quality CI and release preparation. It binds the source and
baseline commits, retains versioned documents before packaging, and consumes
them before final checksumming. Its full local gate passed, including both
container variants and Android ABIs. The follow-up
[candidate run](https://github.com/emulebb/emulebb-rust/actions/runs/42562013163)
passed final assembly and strict candidate verification using the fully
CI/CodeQL-verified source `3ddf47ac1847760898d759189ffca90c66de4dca`. All native
and container producers, lifecycle tests and security checks passed, and the
exact candidate was retained. Publication and nightly-channel jobs were
skipped. Full [CI](https://github.com/emulebb/emulebb-rust/actions/runs/42562016095)
and [CodeQL](https://github.com/emulebb/emulebb-rust/actions/runs/42562019322)
also passed at workflow-control commit `80ccc06e`.

These are pushed workstream checkpoints. The item remains open until the
approved integration and published-artifact criteria are satisfied.

## Intended Shape

- Use pinned musl cross-compilers and the repository Rust toolchain through
  canonical build orchestration.
- Produce portable `.tar.zst` assets for x64 and ARM64. Do not present a
  partially static executable as fully static; record every dynamic dependency.
- Keep profile, WebUI, configuration, persistence, and network behavior
  identical to the supported glibc daemon.
- Use native Alpine runners or containers for runtime proof. QEMU compilation
  alone is not ARM64 runtime evidence.

## Scope Constraints

- No protocol, REST, settings, or schema fork for musl.
- No 32-bit architecture is introduced by this item.
- DNS, TLS roots, locale, time-zone, interface enumeration, and filesystem
  watching must not depend accidentally on glibc behavior.
- Existing DEB, AppImage, OCI, Windows, and macOS artifacts remain unchanged.

## Acceptance Criteria

- [ ] Both musl targets compile the daemon and complete workspace dependency
      graph from pinned toolchains and native-source revisions.
- [ ] MiniUPnPc, libpcpnatpmp, bundled SQLite, TLS, media parsing, filesystem
      watching, and interface enumeration have focused musl proof.
- [ ] Portable archives contain the daemon, WebUI, license material, release
      scope, manifest, per-file hashes, SBOM, and build provenance.
- [ ] Alpine x64 and ARM64 smokes prove first launch, authenticated REST/WebUI,
      SQLite creation, deterministic local transfer, restart/resume, and clean
      shutdown.
- [ ] Archive extraction and execution work from a non-root account with a
      fresh profile and explicit writable data paths.
- [ ] Published release assembly requires successful package smoke on the exact
      candidate assets for both architectures.
- [ ] Existing glibc and multi-platform release gates remain green.

## Validation

- Cross-target Cargo build, tests that can run under the selected runner, and
  native dependency compile checks.
- Native Alpine package lifecycle and local-transfer smoke on x64 and ARM64.
- ELF interpreter/dependency audit and archive-content validation.
- Existing Rust quality, supply-chain, glibc package, and OCI gates.

## Delivery Slices

1. Compile spike and native-dependency disposition.
2. Portable archive format and manifest contract.
3. x64 Alpine lifecycle smoke.
4. ARM64 native lifecycle smoke.
5. Hosted release matrix and publication assembly integration.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_secure-ident.md` section 5 / 7 (existing): Weak stock RSA/SHA1 is an accepted interoperability boundary. Key pinning has a closed owner; native-target build/runtime and cross-client proof have existing owners.
- `emulebb-rust-prompt_audit_findings_reachability.md` section 2.4 / 4.2-3 (existing): ABI verification and native-target compile/runtime proof belong to existing FFI and platform items. Android is parallel and non-gating for Beta 3; do not replace proven C libraries with a narrower pure-Rust fallback to avoid qualification.
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section extended-lanes (existing): The audit's no-musl/no-Android-CI claim is stale: both musl architectures and Android compile/ELF lanes now exist. Keep the owning feature issues open for their remaining runtime/package evidence; cross-compilation is not complete platform certification.
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section platform-evidence (existing): Windows/Linux are Beta 3 gates. macOS and extended target qualification continue in parallel, with per-target limitations and no stronger support claim than retained runtime evidence.

### Scoped Follow-up Acceptance

- [ ] Do not replace on-wire primitives locally.
- [ ] Retain key pin/restart/credit preservation proof.
- [ ] Keep Android evidence non-gating for Beta 3.
- [ ] Mechanical C/Rust layout proof uses exact vendored headers.
- [ ] Keep musl and Android compile proof distinct from runtime/device NAT proof.
- [ ] Reuse current lanes and identify missing runtime/device proof only.
- [ ] Track optional platform failures visibly without gating Beta 3.
- [ ] Required Windows/Linux proof is recorded under the candidate owner.
- [ ] Optional target status distinguishes compile, package and runtime evidence.
