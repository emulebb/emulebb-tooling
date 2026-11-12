---
id: RUST-CI-050
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/327
title: Give genuine documentation changes a trusted short CI path
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, audit]
milestone: ""
created: 2026-11-12
source: Operator-approved change-aware hosted CI and parent integration batching
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/327. Project #3 owns placement; this item owns the engineering contract and evidence.

# RUST-CI-050 - Give genuine documentation changes a trusted short CI path

## Outcome And Ownership

Avoid expensive Rust platform fanout only for proven, narrowly eligible prose
changes. The Rust worker owns `tools/ci_change_scope.py`, primary CI, CodeQL and
optional-platform consumers; the parent owns source selection, integration and
qualification. Required aggregates always report and cannot turn an unknown
or accidental skip into success.

The delivered [#323 preflight](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-CI-048.md)
remains in full primary validation. [#258](RUST-CI-032.md) separately owns
developer-selective checks. This item changes neither pre-push coverage nor
the full nightly/publication inventory, and creates no scheduler or test queue.

## Initial Eligible Changes

- A regular-file root `README.md` edit with valid UTF-8/LF text. Additions,
  removals, renames, binary content or file-mode changes do not qualify.
- A parsed semantic change restricted to the existing nonempty
  `product.phase_gate` string in `policy/rust-client.toml`. Every other parsed
  key, value and type must remain identical. This is a specific prose exception,
  not permission to skip validation for arbitrary policy/config changes.

No template paths currently qualify. Executable code, workflows, dependencies,
package inputs, assets, unknown paths and uncertain input select full checks.
Do not broaden this allowlist through head-controlled data or infer prose from
a suffix. Packaged documentation is not automatically a safe short path.

## Trust And Complete Change Range

Each of `.github/workflows/ci.yml`, `codeql.yml` and `optional-platforms.yml`
uses the same small bootstrap contract. Extract a regular classifier blob from
the immutable event base and execute it with isolated `python -I -B` below
runner scratch. Never execute the tested head's classifier to decide whether
that head can skip its checks. Missing base/helper on first deployment selects
full coverage; unknown/untrusted input selects full. Unexpected helper
execution failure fails classification rather than granting a short path.

- Main pushes classify the complete event `before` to tested `after` range,
  with source identity and ancestry proved. An unavailable/uncertain range
  cannot qualify.
- PRs verify the main base, same-repository event/head/origin identities and
  the actual ordered two-parent merge commit. Distinguish tested merge SHA
  from PR head SHA. Never inspect only the latest authored commit.
- Preserve complete NUL-safe path/status and before/after modes, including
  both sides of renames and all changed paths. Do not interpolate filenames
  into shell commands or permit a dirty/foreign tested tree.

The receipt schema is `emulebb.ci-change-scope/1`: `repository`, `event`,
`baseSha`, `headSha`, `testedSha`, `classifierBlob`, `scope` (`docs` or `full`),
boolean `docsValidated`, `reason`, and `changes` records containing `path`,
`status`, `beforeMode`, `afterMode`. An admitted helper also binds
`classifierSha256`. Fallback receipts retain source identity and select full.

## Consumers And Required Results

Keep coordination, workflow lint, supply-chain checks and the applicable static
quality path. Rust's `ci-docs` path retains quality environment admission,
release-document/policy/Python checks and formatting; it omits the full WebUI
and compile/platform jobs only after trusted classification succeeds.

All three required aggregates use `always()` and bind successful
classification, exact tested SHA, known scope, docs validation and a real
trusted classifier blob before accepting the precisely expected heavy skips.
For full scope, every required selected job must actually succeed. Failed,
cancelled, unexpected or unaccounted skipped work cannot count as green.
Manual/scheduled security remains full; Nightly is unchanged.

Tooling deliberately receives no classifier or skipped checks in this batch.
[Measured baseline 43230048997](https://github.com/emulebb/emulebb-tooling/actions/runs/43230048997)
ran its Windows privacy/hygiene/unit jobs in 29 and 44 seconds, with no native,
Cargo or Docker build. Keep its existing docs publishing, privacy/hygiene,
taxonomy and strict MkDocs checks plus managed default CodeQL/Code Quality.
Do not create a second framework for negligible savings. If later considering
Tooling Markdown, exclude the packaged Rust `RELEASE-SCOPE.md` and legacy
`REST-API-CONTRACT.md`/`REST-API-PARITY-INVENTORY.md` inputs explicitly.

## Acceptance And Current Evidence

- [x] A source contribution is clean/pushed at Rust
  `12c0db5dde7c6a61a040e5ff56755d5756cdee68`; 134 scoped tests, real-Git/actual
  Bash fixtures, pinned actionlint and normal hooks passed. This is a worker
  checkpoint, not merged or hosted delivery.
- [ ] Review and qualify the parent's exact integrated tip through applicable
  full local and hosted checks; first deployment must select full because the
  trusted base lacks the helper.
- [ ] Prove a subsequent genuine README-only change uses the trusted helper,
  retains all required aggregate contexts and accepts only deliberate heavy
  skips after real lightweight validation.
- [ ] Retain regression coverage for event/base/head/merge identity, complete
  multi-commit ranges, strict TOML types, modes/renames/binary changes, helper
  tampering/failure, and aggregate failure/skip rejection.
- [ ] Record actual hosted timing and source-bound receipts. No fixed speed
  guarantee follows from source inspection or local fixture success.

The parent integrates authored contributions linearly into one coherent batch
PR per affected repository. Beta 3 promotion, APK/signing and long soak remain
held; no source pass transfers to a changed integration head.
