---
id: RUST-CI-033
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/267
title: Preserve native build scripts in Dependabot fuzz updates
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, ci, dependencies, fuzz, native]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Dependabot fuzz update run 42649427662 and verified offline Cargo reproduction
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/267. This local document owns the durable engineering specification and evidence.

# RUST-CI-033 - Preserve native build scripts in Dependabot fuzz updates

## Summary

Dependabot cannot update dependencies in the isolated `fuzz` workspace because
its reconstructed native path dependencies retain `links` but omit implicit
`build.rs` files. Cargo rejects the MiniUPnPc sys manifest before dependency
resolution. Eleven dependency updates failed in the observed run.

Declare the real build script explicitly in both native sys manifests. Keep
their existing implementations and native library identities unchanged. This
fix concerns resolver metadata; it does not replace native build qualification.

## Beta 3 Prerequisite

Restore the blocked fuzz dependency resolver before certifying Beta 3. The
prerequisite is the scoped manifest fix, its required checks, and a subsequent
hosted Dependabot update proving resolver recovery. Local reproduction proves
the failure mechanism and resolver workaround; hosted updater recovery remains
unverified until that later run supplies evidence.

This prerequisite does not require merging every dependency-version update
that the recovered updater produces. Those changes retain their own review,
validation, and release-triage decisions.

## Scope Constraints

- Preserve both `links` values and production build scripts.
- Do not introduce no-op production scripts or weaken native binding checks.
- Keep `fuzz` isolated from the release workspace.
- Preserve inherited operator roots and the canonical Cargo target.
- Do not treat local resolver success as a passed hosted Dependabot update.
- Do not gate Beta 3 on all resulting dependency-version updates.

## Acceptance Criteria

- [x] Both sys manifests explicitly declare `build = "build.rs"`.
- [x] Existing production scripts and native `links` identities remain intact.
- [x] Offline regressions reproduce the implicit-script failure and verify
      metadata and lockfile resolution for both explicit-script variants.
- [x] Actual `fuzz/Cargo.toml` metadata resolves with `--offline --locked`.
- [ ] Required local and hosted checks pass before integration.
- [ ] A subsequent hosted Dependabot update confirms recovery after merge.

## Validation

The exact observed updater revision is
[`fcf67e2f`](https://github.com/dependabot/dependabot-core/blob/fcf67e2f232b841cd1a585a1a5357fdac3513ee2/cargo/lib/dependabot/cargo/file_updater/lockfile_updater.rb).
Its `write_temporary_path_dependency_files` writes manifest and source stubs
without the build script written for ordinary package manifests.

`tools/tests/test_dependabot_manifests.py` preserves the actual native manifest
shapes and substitutes a local `cc` fixture to avoid network or compilation.
It omits `build.rs` to model the updater. Implicit discovery fails with the
observed missing-custom-build-script error. Explicit declarations preserve the
custom-build target and `links` through metadata and lockfile resolution even
though the reconstruction still has no script to execute.

The original verification passed two tests, covering eight offline Cargo
commands across both packages. The actual fuzz manifest also passed:

```text
cargo metadata --offline --locked --no-deps --format-version 1 --manifest-path fuzz/Cargo.toml
```

These results are historical evidence from the original fix. Refresh the
scoped checks and complete normal worker push qualification against the actual
rebased fix before integration. Unchanged main validation is not evidence for
this metadata fix.

Selected-checkout validation support is integrated in the workspace mains.
Parent acceptance and cleanup remain tracked separately by
[emulebb-build #28](https://github.com/emulebb/emulebb-build/issues/28).

## References

- [Observed failed updater run](https://github.com/emulebb/emulebb-rust/actions/runs/42649427662)
- [Owning issue](https://github.com/emulebb/emulebb-rust/issues/267)
