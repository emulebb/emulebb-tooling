---
id: RUST-CI-028
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/156
title: Make Windows manifest embedding target-aware
status: OPEN
priority: Minor
category: ci
labels: [rust, windows, cross-build, packaging, long-path, portability]
milestone: post-beta-polish
created: 2026-10-23
source: 2026-10-23 Rust async and portability audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/156. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-028 - Make Windows manifest embedding target-aware

## Summary

Embed the Windows application manifest whenever the Cargo target is Windows,
including cross-builds from Linux or macOS hosts, and prove that packaged
binaries retain the long-path declaration.

## Current State

`crates/emulebb-daemon/build.rs` reads `CARGO_CFG_WINDOWS`, which is target
aware, but the embedding block is also compiled behind `#[cfg(windows)]`, which
describes the build-script host. A non-Windows host targeting Windows therefore
skips manifest embedding even though the target is Windows. The resulting
binary can omit `longPathAware` and other declared Windows process metadata.

## Why This Matters

Build scripts must distinguish host and target explicitly. Native Windows
release jobs can conceal this defect, while reproducible cross-build or future
multi-platform packaging produces a behaviorally different executable.

## Representative Sites

- `crates/emulebb-daemon/build.rs` Windows manifest target detection and embed.
- Windows package and long-path smoke lanes in `emulebb-build-tests`.
- `RUST-CI-008` cross-platform Unicode and long-path evidence.

## Intended Shape

- Gate manifest embedding only on Cargo target metadata, not host compile-time
  configuration.
- Keep non-Windows target builds free of Windows resource work.
- Inspect the produced PE resource instead of relying only on build-script log
  output.
- Exercise at least one supported non-Windows-host to Windows-target build path.

## Scope Constraints

- Do not claim a supported release target solely because a cross-compile step
  succeeds; retain the supported package and lifecycle matrix.
- Preserve the existing manifest contents unless a separate compatibility item
  approves a change.
- Keep native Windows packaging as a validation lane even after cross-build
  coverage exists.

## Acceptance Criteria

- [ ] Every Windows target invokes manifest embedding regardless of build host.
- [ ] Non-Windows targets do not invoke Windows resource embedding.
- [ ] PE inspection proves the packaged daemon contains the expected manifest
      and `longPathAware` declaration.
- [ ] At least one non-Windows-host cross-build and the native Windows package
      build pass the same manifest assertion.
- [ ] Windows long-path package smoke succeeds with the inspected artifact.

## Validation

- Build-script target/host matrix tests where practical.
- Native Windows and non-Windows-host Windows-target package builds.
- PE resource inspection plus the bounded long-path smoke owned by
  `RUST-CI-008`.
