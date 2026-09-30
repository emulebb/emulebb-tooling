---
id: RUST-CI-004
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/8
title: Harden Rust toolchain, feature, and supply-chain gates
status: DONE
priority: Major
category: ci
labels: [rust, toolchain, ci, dependencies, supply-chain]
milestone: release-0.1.0-beta.1
created: 2026-07-11
source: Operator-approved Rust development hygiene review 2026-07-11
---

# RUST-CI-004 - Harden Rust toolchain, feature, and supply-chain gates

## Summary

Make Rust development and release inputs reproducible: pin the supported stable
toolchain, exercise the diagnostics feature explicitly, centralize workspace
manifest policy, and enforce dependency source and license rules after obsolete
Git dependencies are removed.

## Scope

- Pin the supported Rust toolchain in one repository-owned file and make CI
  consume it; the current beta candidate uses Rust 1.98.1 (`rust-version = 1.98`).
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

- [x] Local development and every CI job use Rust 1.98.1 from one pin.
- [x] The default daemon, diagnostics binary, and isolated egress-audit test
      configuration each have an explicit gate.
- [x] All internal crates are `publish = false` and `GPL-2.0-only`.
- [x] Cargo-deny rejects unapproved Git/registry sources and incompatible
      licenses.
- [x] The repository documents and checks a repeatable toolchain update cadence.
- [x] Policy advisories remain non-failing and prioritize changed files.

## Validation

- `python tools\rust_quality_gate.py policy`
- Supported workspace Rust format, Clippy, build, and test orchestration.
- Cargo-deny advisories, sources, licenses, and the reviewed bans baseline.

## Evidence

- `0d236f2` pins Rust 1.97.0 and adds toolchain-drift checks.
- `1b8e06d` makes all 14 workspace crates GPL-2.0-only and non-publishable.
- `a9c0790` centralizes registry dependency versions.
- `94a5607` removes Tokio `full`; all eight Tokio-using crates passed isolated
  all-target Clippy with per-crate features.
- `ecc3081` enables Cargo-deny advisories/licenses/sources, pins the action by
  commit, records the Slint royalty-free license selection and attribution, and
  passes cargo-deny 0.20.2 against the locked graph.
- `f31eb99` adds a named diagnostics gate to the canonical quality runner and
  includes its exact `packet-diagnostics` build in every quick/CI quality run;
  tests ensure `egress-audit` and `--all-features` cannot leak into that command.
- `6e7a347` prioritizes working-tree/index Rust changes (or the latest clean-tree
  commit) ahead of repository-wide context, retains non-failing size signals,
  and rejects permanent broad lint allows.

## Closure Evidence (2026-09-30)

- `c1871bb` updates the repository pin to Rust 1.98.1, `rust-version` to 1.98,
  actions and dependencies to the reviewed current baseline, and cargo-deny to
  the resulting locked graph; `16bb6e1` closes the platform-specific lint.
- `334db49` closes the remaining Rust 1.98 Clippy debt without weakening the
  `-D warnings` gate.
- Hosted run `36697107023` passes policy/format, Clippy, cargo-deny, Windows,
  Linux, macOS, and live REST/OpenAPI conformance on exact SHA `334db49`.
- The current quick quality gate passes policy, 40 policy tests, formatting,
  Clippy, packet diagnostics, 19 WebUI unit tests, 12 browser tests, and the
  production WebUI build. No acceptance criterion remains open.
