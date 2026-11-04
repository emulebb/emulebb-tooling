---
id: RUST-FEAT-059
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/229
title: Support FreeBSD on x64 and ARM64
status: OPEN
priority: Minor
category: feature
labels: [rust, freebsd, bsd, packaging, portability, arm64]
milestone: post-beta-polish
created: 2026-11-04
source: operator-approved universal-platform expansion 2026-11-04
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/229. This local document owns the durable engineering contract.

# RUST-FEAT-059 - Support FreeBSD on x64 and ARM64

## Summary

Add FreeBSD x64 and ARM64 as supported native daemon targets with
platform-correct networking, filesystem watching, service lifecycle,
packaging, and runtime evidence. Preserve one Rust protocol, persistence, REST,
and WebUI implementation across every operating system.

## Current State

- FreeBSD is absent from the platform contract, target map, release matrix, and
  package harness.
- Non-Windows socket code is Unix-oriented, but default-route discovery has no
  FreeBSD implementation and runtime binding has not been proven.
- Native NAT libraries, bundled SQLite, file identity, filesystem watching,
  disk-space reporting, and signal behavior need explicit FreeBSD disposition.

## Intended Shape

- Build supported x64 and ARM64 artifacts natively or through a reviewed cross
  toolchain, with native runtime proof for both architectures.
- Publish a FreeBSD package or portable archive containing the daemon, WebUI,
  service assets, manifest, checksums, SBOM, and provenance.
- Integrate with the normal `rc.d` service model while retaining direct CLI use.
- Document host and jail deployment boundaries without creating jail-specific
  product state.

## Scope Constraints

- No protocol, API, configuration, or schema fork for FreeBSD.
- ZFS and UFS must preserve transfer correctness; filesystem-specific
  optimization is optional and cannot weaken capacity or durability rules.
- VPN/interface selection must be proven fail-closed or rejected before public
  traffic. Linux or Windows socket assumptions may not be copied blindly.
- FreeBSD support does not imply TrueNAS CORE appliance certification; that
  deployment can consume this platform only after separate evidence.

## Acceptance Criteria

- [ ] The complete product and native dependencies build for supported FreeBSD
      x64 and ARM64 toolchains.
- [ ] Default-route detection, interface inventory/index resolution, TCP/UDP
      binding, VPN failure, and NAT behavior have focused runtime proof.
- [ ] SQLite, file identity, filesystem watching, disk-space checks, sparse or
      dense transfer storage, signals, and graceful shutdown behave correctly.
- [ ] The release artifact installs or extracts without source-tree output and
      includes WebUI, license, manifest, hashes, SBOM, and provenance.
- [ ] `rc.d` start, status, stop, restart, boot enablement, non-root ownership,
      and stale-process recovery are deterministic.
- [ ] Native x64 and ARM64 smokes prove first launch, authenticated REST/WebUI,
      deterministic local transfer, restart/resume, and shutdown.
- [ ] Existing supported-platform and supply-chain gates remain green.

## Validation

- Native FreeBSD Cargo build/test and native-library checks on x64 and ARM64.
- Package and `rc.d` lifecycle smoke under a non-root service account.
- Local transfer, restart, storage, route/bind, VPN-failure, and NAT campaigns.
- Existing Rust quality and release matrices.
