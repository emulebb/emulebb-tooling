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

- [ ] A manual non-publishing run completes the full package and smoke matrix.
- [ ] A scheduled run publishes immutable GitHub and GHCR nightly artifacts
      only for a source commit with all required CI checks passing.
- [ ] Generated release notes cover the range since the previous successful
      nightly and link the exact commits and full comparison.
- [ ] Retention selection is strictly limited to well-formed nightly
      prereleases and keeps the newest 14.
- [ ] The formal `rust-v0.1.0-beta.2` release path remains valid and does not
      gain a moving channel tag.

## Validation

- Run the nightly helper and release-policy unit tests.
- Run the Rust policy checker and GitHub Actions workflow linter.
- Trigger `Nightly` manually with publication disabled after the implementation
  commit's normal CI checks are green, then retain the run URL here.
