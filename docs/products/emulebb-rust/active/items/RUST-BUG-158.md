---
id: RUST-BUG-158
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/238
title: Reuse trusted stock profile hashes without payload rehashing
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, persistence, sharing, tests]
product: emulebb-rust
phase: Phase 1
milestone: post-beta-polish
created: 2026-11-06
source: operator-approved stock hash import and path-remapping workflow
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/238. This local document owns the durable engineering contract.

# RUST-BUG-158 - Reuse trusted stock profile hashes without payload rehashing

Stock/MFC profile hashes are trusted by default. Reuse the existing portable
manifest and Rust importer. Bind unambiguous filename, size, and stock timestamp
matches to target-native fingerprints without reading payload contents.

- Keep known hashes and available MD4/AICH hashsets independent of roots and
  payload availability. Hash-only import preserves the target's sharing roots
  and does not require the export platform to match.
- Keep normal root admission and upload checks. Changed metadata invalidates
  the affected association; coarse timestamps alone do not invalidate it.
- Report ambiguous records without silently hashing them. Retain offline-file
  records. Missing optional AICH data does not invalidate eD2K hashes.
- Use the current clean schema only. Do not add migrations or compatibility
  shims; optional local AICH roots require a fresh schema-55 profile.
- Reconcile offline with the normal scan/reuse planner. Report pending work
  without executing hashing or starting daemon networking.
- Validate actual stock imports on Windows and isolated network-none Docker,
  including exact imported hashset comparison, process/container recreation,
  and hash-only reimport independent of the manifest's target platform.

Implementation and offline validation are complete; delivery checks remain in
progress. Product source is `b2758345`; the persisted audit is in
`emulebb-build-tests` through `d8d06829`.

| Target | Imported records | Reused paths | Payload bytes read | Files hashed |
|---|---:|---:|---:|---:|
| Native Windows | 53,910 | 53,985 | 0 | 0 |
| Docker/Linux | 53,910 | 53,985 | 0 | 0 |

Every exported record and ordered MD4/AICH hashset matched the imported cache:
367,821 part hashes of each kind. Reconciliation bound 53,907 distinct content
identities to the reusable paths; all 53,910 imported records remain retained.
Counts and reuse remained stable across process/container recreation and
cross-platform hash-only reimport. No daemon networking was started; Docker
used network-none containers and read-only payload mounts.

Windows reported 11,681 unmatched paths and Docker 11,683. They were counted as
pending new-file work and were never hashed by the audit. The scans differed
by two paths and two intake exclusions across platforms.

Retained receipts below `EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- `reports/stock-hash-import/windows/20261106T135523Z/summary.json`
- `reports/stock-hash-import/docker/20261106T140547Z/summary.json`
- `logs/trusted-stock-rust-tests.log`
- `logs/builds/20261106T135205Z-build-clients/build-result.json`
- `logs/builds/20261106T135724Z-package-emulebb-rust/build-result.json`

The full Rust workspace tests, focused exporter/import/audit tests, Windows and
Linux release builds, local DEB/image packaging, and workspace policy validation
passed. The Docker candidate is
`local/emulebb-rust:0.1.0-beta.2.nightly.20261106.gb2758345`. The operator's existing
Docker stack profile was not replaced.
