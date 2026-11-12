---
id: RUST-CI-045
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/302
title: Make Linux release provisioning bounded and reproducible
status: DONE
priority: Major
category: ci
labels: [rust, ci]
milestone: ""
created: 2026-11-10
source: Nightly APT provisioning stall and operator-approved CI infrastructure work
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/302. This document owns the durable specification and evidence boundaries.

# RUST-CI-045 - Make Linux release provisioning bounded and reproducible

## Closure And Evidence

The parent closed [#302](https://github.com/emulebb/emulebb-rust/issues/302#issuecomment-6829946635)
after the actual prepared producer and final consumer passed. Builder
`7a713aef251e4066890e898c031140ead4c0c500` produced the verified image
`ghcr.io/emulebb/emulebb-build-ci/ubuntu-rust@sha256:c90563f122dc08fae678936347df486a092ed799b1a915cc86d363da9aa6deee`
in [producer 43190149335](https://github.com/emulebb/emulebb-build/actions/runs/43190149335).
Both native CPU probes exercised the real non-root AppImage assembly/extraction
path; signed receipts and anonymous registry reads were verified before
consumer activation. The source/image pair is inseparable evidence.

[Rust PR #322](https://github.com/emulebb/emulebb-rust/pull/322) integrated the
consumer. Published [Nightly 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692)
at `080a5dea70186da31dab958757b5b8c0fd883f82` passed actual prepared GNU
DEB/AppImage packaging on x64 and ARM64, all selected lifecycle/OCI checks and
publication, without a retry. The independent public-byte review verified all
81 assets and both OCI graphs with the exact source/material pins. This is not
a byte-for-byte reproducibility claim or Android device qualification.

Final receipts remain under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/nightly-publication-review/43242135692`.
The failure and recovery discussion below is retained provenance, not the
current consumer state; earlier failed images/candidates are not relabeled.

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
the successful attempt-1 producers. All 31 jobs subsequently passed and the
81-asset prerelease was published. Independent verification matched the signed
subjects, metadata and OCI identities to source `78f74541`. Large archives were
not downloaded or executed locally, and Android device/runtime qualification
remains untested. The recovery did not execute the new provisioning helper.

Keep original and recovery attempts distinct. Earlier producer attempts are
acceptable only under the existing same-repository, same-run, same-workflow
identity and ordering checks. Do not relabel proofs, retry unexplained product
failures, guess image digests or repair inherited operator configuration.

Detailed local receipts stay below
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/nightly-publication-review`.

Beta3 publication, long-soak and Android APK holds remain unchanged.
