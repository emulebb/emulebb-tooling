---
id: RUST-CI-007
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/32
title: Publish immutable nightly beta builds
status: OPEN
priority: Minor
category: ci
labels: [rust, github-actions, release, nightly]
milestone: post-beta-ci
created: 2026-10-03
source: Operator request for automated nightly beta builds and compact changelogs
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/32. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-007 - Publish immutable nightly beta builds

## Summary

Publish CI-gated nightly prereleases from `emulebb-rust/main` by reusing the
formal six-platform beta packaging workflow. Each nightly has an immutable
version derived from the promoted beta, UTC date, and source commit, while the
container channel also exposes a moving `nightly` tag.

## Intended Shape

- Derive versions such as
  `0.1.0-beta.2.nightly.20261003.g9e43ea5e` without changing the Cargo package
  version for every nightly.
- Require the normal default-branch CI checks to be green for the exact source
  commit before packaging.
- Reuse the release workflow for Windows, Linux, macOS, x64, ARM64, and the
  multi-architecture OCI image.
- Publish GitHub prereleases with `SHA256SUMS`, build-provenance attestations,
  and a compact changelog generated from commit subjects plus a compare link.
- Retain the newest 14 nightly prereleases and never prune formal beta tags.
- Keep formal beta image behavior unchanged; only nightly publication updates
  the moving `nightly` tag, and neither path publishes `latest`.

## Acceptance Criteria

- [x] A manual non-publishing run completes the full package and smoke matrix.
- [ ] A scheduled run publishes immutable GitHub and GHCR nightly artifacts
      only for a source commit with all required CI checks passing.
- [x] Generated release notes cover the range since the previous successful
      nightly and link the exact commits and full comparison.
- [x] Retention selection is strictly limited to well-formed nightly
      prereleases and keeps the newest 14.
- [x] The formal `rust-v0.1.0-beta.2` release path remains valid and does not
      gain a moving channel tag.

## Validation

- Run the nightly helper and release-policy unit tests.
- Run the Rust policy checker and GitHub Actions workflow linter.
- Trigger `Nightly` manually with publication disabled after the implementation
  commit's normal CI checks are green, then retain the run URL here.

## Evidence

- 2026-10-03: default-branch CI passed on source commit
  `bba6cbbd3d5eb842e99c42bef129c3c5c0d79ee1`, including Windows, Linux,
  macOS, policy/Clippy, cargo-deny, and live REST/OpenAPI conformance:
  https://github.com/emulebb/emulebb-rust/actions/runs/37150371404
- 2026-10-03: manual `Nightly` dry-run passed for
  `0.1.0-beta.2.nightly.20261003.gbba6cbbd`. All six native package/smoke jobs
  and the multi-architecture OCI image candidate passed; publication jobs were
  skipped as requested:
  https://github.com/emulebb/emulebb-rust/actions/runs/37151402599
- Nightly metadata, changelog grouping/linking, required-CI selection, and
  retention protections are covered by the nightly helper tests. Rust policy
  checks and `actionlint` also passed after the final workflow pins were set.
- The remaining unchecked criterion requires observing the first scheduled
  publishing run; the item stays open until that evidence exists.
