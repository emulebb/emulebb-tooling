---
id: RUST-CI-004
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/8
title: Harden Rust toolchain, feature, and supply-chain gates
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, toolchain, ci, dependencies, supply-chain]
milestone: release-0.1.0-beta.1
created: 2026-07-11
source: Operator-approved Rust development hygiene review 2026-07-11
---

# RUST-CI-004 - Harden Rust toolchain, feature, and supply-chain gates

## Summary

Make Rust development and release inputs reproducible: pin the current stable
toolchain, exercise the diagnostics feature explicitly, centralize workspace
manifest policy, and enforce dependency source and license rules after obsolete
Git dependencies are removed.

## Scope

- Pin Rust 1.97.0 in one repository-owned toolchain file and make CI consume it.
- Declare the workspace Rust version and verify the active compiler in CI.
- Build/check the `packet-diagnostics` binary without enabling test-only
  `egress-audit` in product builds.
- Set internal crates non-publishable and use `GPL-2.0-only`.
- Centralize repeated direct dependencies and narrow Tokio features by crate.
- Enforce Cargo-deny source and license policy after the dependency baseline is
  green; record justified duplicate-version exceptions separately.
- Make maintainability advisories emphasize changed files without becoming
  source-size failures.

## Acceptance Criteria

- [ ] Local development and every CI job use Rust 1.97.0 from one pin.
- [ ] The default daemon, diagnostics binary, and isolated egress-audit test
      configuration each have an explicit gate.
- [ ] All internal crates are `publish = false` and `GPL-2.0-only`.
- [ ] Cargo-deny rejects unapproved Git/registry sources and incompatible
      licenses.
- [ ] The repository documents and checks a repeatable toolchain update cadence.
- [ ] Policy advisories remain non-failing and prioritize changed files.

## Validation

- `python tools\rust_quality_gate.py policy`
- Supported workspace Rust format, Clippy, build, and test orchestration.
- Cargo-deny advisories, sources, licenses, and the reviewed bans baseline.
