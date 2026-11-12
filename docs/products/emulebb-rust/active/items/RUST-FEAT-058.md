---
id: RUST-FEAT-058
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/228
title: Certify NAS deployments across supported appliance systems
status: OPEN
priority: Major
category: feature
labels: [rust, nas, containers, docker, packaging, portability, distribution-expansion]
milestone: post-beta-polish
created: 2026-11-04
source: operator-approved universal-platform expansion 2026-11-04
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/228. This local document owns the durable engineering contract.

# RUST-FEAT-058 - Certify NAS deployments across supported appliance systems

## Distribution Intake Acceptance

This is explicitly optional environment expansion. Keep its owning phase and
applicable qualification; it does not independently block the mandatory core
Client gate or become a new Beta 3 gate.

- [ ] Reuse immutable Ubuntu/Alpine OCI digests and one deployment model; qualify
      appliance/version/CPU combinations individually, without generic NAS claims.
- [ ] Prove user/group permissions, profile/key/data mounts, health, networking,
      transfer/sharing, restart, stopped-profile backup and compatible rollback.
- [ ] Keep direct and Docker-over-Gluetun evidence distinct. Generic container
      smoke is not appliance certification or fail-closed VPN proof; no SPK/QPKG
      or new hardware purchase is required by this intake.

## Summary

Make the existing multi-architecture OCI client a supported NAS deployment
lane for Synology DSM, QNAP QTS/QuTS hero, TrueNAS SCALE, and Unraid. Use one
Linux AMD64/ARM64 image and shared runtime contract rather than creating
vendor-specific protocol or persistence implementations.

## Current State

- RUST-FEAT-006 delivered a LinuxServer-style AMD64/ARM64 GHCR image with
  `/config`, `/data`, `PUID`, `PGID`, and `TZ` conventions.
- Container smoke proves the generic image, but no appliance family has a
  supported storage, identity, networking, update, backup, or recovery contract.
- NAS interfaces frequently wrap Compose, hide host networking details, and
  apply vendor-specific volume permission models.

## Intended Shape

- Treat the OCI digest as the product artifact; appliance instructions select
  and configure that exact artifact.
- Maintain one canonical deployment model for `/config`, incoming/shared data,
  REST, eD2K TCP, Kad UDP, user/group mapping, time zone, and health checks.
- Provide appliance-specific setup only where the management surface requires
  different input, naming, or permission steps.
- Support direct and explicitly selected VPN-container topologies without
  silently falling back between them.

## Scope Constraints

- Native `.spk`, `.qpkg`, or other vendor package formats are not required.
- TrueNAS CORE belongs to the FreeBSD platform item; this item owns TrueNAS
  SCALE and the OCI deployment lane.
- Appliance UI automation must not become a second topology authority. Durable
  runtime validation stays in the shared Python harness.
- No real library names, private paths, host addresses, credentials, or
  appliance identifiers enter tracked fixtures or retained public evidence.

## Acceptance Criteria

- [ ] Synology DSM, QNAP QTS/QuTS hero, TrueNAS SCALE, and Unraid each have a
      documented supported version range and exact OCI deployment procedure.
- [ ] Representative AMD64 and ARM64 appliances pull the correct manifest
      platform and record the exact image digest.
- [ ] Fresh deployment proves profile creation, authenticated WebUI, persistent
      SQLite, incoming delivery, sharing, upload, restart, and clean shutdown.
- [ ] Volume ownership through `PUID`/`PGID`, read-only shares, writable data,
      path mapping, low space, and permission denial behave predictably.
- [ ] Upgrade and rollback preserve an exact compatible profile, while schema-
      incompatible builds continue to require a fresh profile.
- [ ] Backup/restore captures the bounded profile contract and never treats
      incomplete copying of a live database as valid evidence.
- [ ] Direct bridge/host networking and supported VPN-container topology expose
      only the declared REST and P2P surfaces and preserve fail-closed routing.
- [ ] Appliance sleep, reboot, container restart policy, log retention, and
      image update behavior receive bounded evidence.
- [ ] Generic OCI, Linux package, and native product gates remain green.

## Validation

- Shared container/package smoke reused against each appliance deployment.
- Deterministic local two-peer transfer with exact payload size and SHA-256.
- Restart, upgrade, rollback, backup/restore, permission, low-space, and
  network-mode campaigns.
- Retained per-appliance receipts recording version class, architecture, image
  digest, configuration shape, and harness revision without private data.

## Delivery Slices

1. Canonical NAS runtime and evidence contract.
2. Synology DSM and QNAP validation.
3. TrueNAS SCALE and Unraid validation.
4. Upgrade, backup, permission, and low-space campaigns.
5. Supported deployment documentation and release integration.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_multi-platform.md` section platform-evidence (existing): Windows/Linux are Beta 3 gates. macOS and extended target qualification continue in parallel, with per-target limitations and no stronger support claim than retained runtime evidence.

### Scoped Follow-up Acceptance

- [ ] Required Windows/Linux proof is recorded under the candidate owner.
- [ ] Optional target status distinguishes compile, package and runtime evidence.
