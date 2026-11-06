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

Implementation and deterministic tests are complete. Native profile and Docker
validation remain in progress; retained evidence belongs below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`.
