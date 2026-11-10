---
id: RUST-CI-045
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/302
title: Make Linux release provisioning bounded and reproducible
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, ci]
milestone: rust-v0.1.0-beta.3
created: 2026-11-10
source: Nightly APT provisioning stall and operator-approved CI infrastructure work
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/302. This document owns the durable specification and evidence boundaries.

# RUST-CI-045 - Make Linux release provisioning bounded and reproducible

## Problem

Nightly run `42761216405`, attempt 1, spent its Linux x64 package job's
45-minute budget in `apt-get update`. Requests to the Azure Ubuntu mirror
stopped progressing before product compilation. The other native packages,
both musl targets and both experimental Android ABI packages passed, but
downstream lifecycle, OCI, assembly and publication jobs were skipped.

The failure concerns host package provisioning. A Docker Hub image mirror
alone cannot repair it. Later successful requests from the operator network
do not establish that every hosted runner route has recovered.

## Coordinated implementation

- Builder owns persisted Python for Ubuntu dependency provisioning. Use signed
  HTTPS sources with amd64/arm64 selection, bounded network retries, a total
  deadline and failure on incomplete index updates. Preserve unrelated APT
  configuration and signature verification.
- Rust's workflow calls that helper with a short outer step timeout. Bind the
  consumer to the actual merged Builder revision before delivery.
- Builder owns a trusted-main image producer, prepared Linux environment
  recipes and exact upstream OCI replication. Preserve source index, platform
  and config identities, including all referenced supported CPU manifests.
- Prepared environments include the required packages and pinned toolchain.
  Probe their actual native runtime dependencies before activation, including
  Python SSL, SQLite, venv and compression support.
- Publish infrastructure through GitHub workflows with provenance and minimal
  permissions. A new GHCR package's visibility or cross-repository access is
  not assumed. Verify actual registry access and digests before consumer use.

## Acceptance

- [x] Preserve the failed attempt and isolate provisioning from product tests.
- [ ] Integrate and qualify the bounded helper and workflow consumer.
- [ ] Exercise real hosted Ubuntu provisioning for both native CPU targets.
- [ ] Publish and verify prepared environment and upstream mirror receipts.
- [ ] Bind consumers to actual verified immutable image digests.
- [ ] Preserve all native, musl, Android, lifecycle, image-security and
      publication gates and the complete candidate inventory.
- [ ] Complete required local and hosted checks, parent integration and cleanup.

## Recovery and evidence

A single parent-controlled replacement of the stalled hosted runner is
separate from deploying the permanent hardening. Attempt 2 retained the same
source and workflow SHA, completed dependency setup in 11 seconds and retained
the successful attempt-1 producers. This does not mean the new helper ran or
that publication has completed.

Keep original and recovery attempts distinct. Earlier producer attempts are
acceptable only under the existing same-repository, same-run, same-workflow
identity and ordering checks. Do not relabel proofs, retry unexplained product
failures, guess image digests or repair inherited operator configuration.

Detailed local receipts stay below
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/nightly-publication-review`.

Beta3 publication, long-soak and Android APK holds remain unchanged.
