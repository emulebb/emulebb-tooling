---
id: RUST-FEAT-061
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/231
title: Support illumos, NetBSD, and OpenBSD as portable Unix targets
status: OPEN
priority: Minor
category: feature
labels: [rust, illumos, netbsd, openbsd, unix, packaging, portability, distribution-expansion]
milestone: post-beta-polish
created: 2026-11-04
source: operator-approved universal-platform expansion 2026-11-04
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/231. This local document owns the durable engineering contract.

# RUST-FEAT-061 - Support illumos, NetBSD, and OpenBSD as portable Unix targets

## Distribution Intake Acceptance

This remains optional environment expansion in its existing phase; incomplete
additional-Unix qualification does not independently block the core Client gate.

- [ ] Retain independent illumos, NetBSD and OpenBSD verdicts, selected CPUs,
      native dependency, route/bind, storage and lifecycle evidence. Neither a
      generic Unix build nor another OS's success establishes support.
- [ ] Reuse one daemon/config/profile/REST model and existing platform owners;
      activate no additional service, package channel or publication from intake.
- [ ] Distinguish declared targets from proven minimums and retained execution
      evidence. Existing required CI/full-nightly checks are unchanged.

## Summary

Extend the portable headless daemon to illumos, NetBSD, and OpenBSD with
explicit per-OS compile and runtime evidence. Preserve one shared Rust protocol,
persistence, REST, and WebUI implementation while implementing the smallest
platform adapters required for networking, storage, lifecycle, and packaging.

## Support Matrix

- x64 is the initial required release architecture for each operating system.
- ARM64 is required where the OS, Rust target, native dependencies, and a
  maintained native runner form a supportable release lane.
- Each OS retains an independent evidence verdict. Success on one Unix does not
  imply support for the others.

## Current State

- None of the three systems appears in the product platform contract, target
  map, release workflow, or package harness.
- Generic Unix code covers some signals, filesystems, and sockets, but route
  discovery, interface binding, watcher backends, native C dependencies, and
  service managers differ materially.
- illumos SMF, NetBSD `rc.d`, and OpenBSD `rc.d` need separate lifecycle assets.

## Intended Shape

- Use portable archives as the common baseline artifact, with native package
  integration only where it is maintainable and provides clear operator value.
- Include the daemon, WebUI, service example/assets, manifest, checksums, SBOM,
  and exact source/toolchain provenance.
- Keep platform adapters narrow and capability-driven; do not accumulate broad
  `not(windows)` assumptions or duplicate runtime implementations.

## Scope Constraints

- No protocol, API, configuration, or schema fork by operating system.
- OpenBSD security mechanisms may be adopted only when they preserve required
  file and network behavior and have deterministic tests.
- A cross-compile result is not a runtime support claim. Every advertised
  OS/architecture pair needs native package and lifecycle evidence.
- Unsupported NAT, interface pinning, watcher, or filesystem behavior must be
  rejected explicitly rather than silently degraded.

## Acceptance Criteria

- [ ] Every workspace crate and native dependency has an explicit compile and
      runtime disposition on illumos, NetBSD, and OpenBSD.
- [ ] Per-OS route discovery, interface enumeration/index resolution, TCP/UDP
      binding, VPN failure, and supported NAT behavior are runtime-proven.
- [ ] SQLite, file identity, filesystem watching, disk-space reporting,
      transfer storage, signals, and graceful shutdown pass focused tests.
- [ ] Portable release assets contain the WebUI, service material, license,
      manifest, hashes, SBOM, and provenance and run as non-root users.
- [ ] illumos SMF, NetBSD `rc.d`, and OpenBSD `rc.d` lifecycle behavior is
      documented and proves start, status, stop, restart, and stale recovery.
- [ ] Each supported OS/architecture pair proves authenticated REST/WebUI,
      deterministic local transfer, restart/resume, and clean shutdown.
- [ ] Release assembly reports each OS independently and cannot treat partial
      family success as a green family verdict.
- [ ] Existing supported-platform and supply-chain gates remain green.

## Validation

- Native compile/test and native-dependency checks on each OS.
- Per-OS service/package lifecycle and deterministic local-transfer smoke.
- Route/bind, VPN-failure, NAT, watcher, storage, restart, and shutdown tests.
- Retained receipts recording OS release, architecture, toolchain, artifact
  digest, source revision, and harness revision.

## Delivery Slices

1. Capability and dependency audit for all three systems.
2. illumos build, SMF, and runtime proof.
3. NetBSD build, `rc.d`, and runtime proof.
4. OpenBSD build, `rc.d`, and runtime proof.
5. Shared package schema and independent release-matrix integration.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_multi-platform.md` section portable-delivery (existing): The unsupported-platform arm still rejects completed delivery. Android/FreeBSD/other Unix issues already own platform viability. Do not adopt the audit's check-then-rename suggestion: it can race and clobber data.
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section platform-evidence (existing): Windows/Linux are Beta 3 gates. macOS and extended target qualification continue in parallel, with per-target limitations and no stronger support claim than retained runtime evidence.

### Scoped Follow-up Acceptance

- [ ] Choose a platform primitive preserving no-replace and crash/durability guarantees.
- [ ] Prove destination collision and concurrent publication without clobbering.
- [ ] Record unsupported filesystems explicitly rather than silently weakening safety.
- [ ] Required Windows/Linux proof is recorded under the candidate owner.
- [ ] Optional target status distinguishes compile, package and runtime evidence.
