---
id: RUST-CI-050
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/327
title: Give genuine documentation changes a trusted short CI path
status: DONE
priority: Major
category: ci
labels: [rust, audit]
milestone: ""
created: 2026-11-12
source: Operator-approved change-aware hosted CI and parent integration batching
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/327. Project #3 owns placement; this item owns the engineering contract and evidence.

# RUST-CI-050 - Give genuine documentation changes a trusted short CI path

## Closure And Evidence

[PR #329](https://github.com/emulebb/emulebb-rust/pull/329) integrated the
classifier and its consumers. The selected local tip
`b73e16e7497766b6ad5f75a19b28b03aa18d9d79` passed full local qualification in
`reports/local-check/emulebb-rust/20261113T024809Z-2fadee68/results.json`.
Its 30 checks across four hosted workflows also passed; the retained receipt is
`reports/ci-scope/qualification-b73e16e7/hosted-acceptance.json`.
The parent verified that merged actual-main
`6429b952eac6f19ee9bf084d3a84d5649dfba0c2` has the identical tree. Actual-main
[CI](https://github.com/emulebb/emulebb-rust/actions/runs/43369209303),
[CodeQL](https://github.com/emulebb/emulebb-rust/actions/runs/43369209301) and
[optional-platform checks](https://github.com/emulebb/emulebb-rust/actions/runs/43369209289)
passed with full coverage. This first deployment selected full because its
trusted base lacked the helper; it did not use the new head to exempt itself.

The subsequent genuine README-only [PR #330](https://github.com/emulebb/emulebb-rust/pull/330)
passed at head `f22daf58374126a58608cfc87bf6189638300ef4`, with actual tested
merge `b936accd3cda103915ab59d420e04e43695eafd5` and base `6429b952`.
Its trusted-base classifier blob was
`4eb5667d9ef0d772efa68251d1a06cbccd25bd84`, SHA-256
`bebc6064f0ab840134831a0f501ff191e532d12fe7332452eed3ce0b94dc287e`.
[CI](https://github.com/emulebb/emulebb-rust/actions/runs/43372468032),
[CodeQL](https://github.com/emulebb/emulebb-rust/actions/runs/43372467997) and
[optional-platform checks](https://github.com/emulebb/emulebb-rust/actions/runs/43372467893)
retained 13 successful jobs and exactly eight deliberate heavy skips, with all
three aggregates green. The accepted receipt is
`reports/ci-change-scope/pr330-f22daf58/acceptance.json`. The three source
workflows completed over a measured 146-second interval; the actual lightweight
docs step took 10 seconds. This is one observation, not a performance promise.

PR #330 merged at `2026-11-13T06:51:33Z`; actual main became
`bc0f319d1841e94e7a2b0f0d5428d318065b679c`, with only the regular root README
changed from `6429b952`. Its complete push range selected `docs` through the
same immutable classifier blob and hash above.
[CI](https://github.com/emulebb/emulebb-rust/actions/runs/43381619962),
[CodeQL](https://github.com/emulebb/emulebb-rust/actions/runs/43381619991) and
[optional-platform checks](https://github.com/emulebb/emulebb-rust/actions/runs/43381619961)
passed with 12 successful jobs and exactly eight deliberate heavy skips.
The accepted push receipt is
`reports/ci-change-scope/main-bc0f319d/acceptance.json`: 91 seconds across the
three workflows, including an 11-second actual lightweight docs step.
Both the real PR and actual merged-main push therefore prove the path; source
fixtures or an implementation merge alone did not close it.

The parent also accepted the complete public-byte and cryptographic inventory
of [nightly 43375379055](https://github.com/emulebb/emulebb-rust/actions/runs/43375379055),
retained in `reports/nightly-publication-review/43375379055/final-acceptance.json`.
Published binaries remain from `6429b952`, not the later README-only `bc0f319d`.
Issue #327 is closed. This change does not weaken the full nightly or local
pre-push gates.

## Outcome And Ownership

Avoid expensive Rust platform fanout only for proven, narrowly eligible prose
changes. The Rust worker owns `tools/ci_change_scope.py`, primary CI, CodeQL and
optional-platform consumers; the parent owns source selection, integration and
qualification. Required aggregates always report and cannot turn an unknown
or accidental skip into success.

The delivered [#323 preflight](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-CI-048.md)
remains in full primary validation. [#258](../../active/items/RUST-CI-032.md) separately owns
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
- PRs verify the main base repository, event repository, checkout origin and
  checked-out tested SHA, plus the actual ordered base/head parents of the
  merge commit. Distinguish tested merge SHA from PR head SHA; a fork head is
  not required to share the base repository name. Never inspect only the latest
  authored commit.
- Preserve complete NUL-safe path/status and before/after modes, including
  both sides of renames and all changed paths. Do not interpolate filenames
  into shell commands. Workflows start from fresh immutable checkouts; the
  classifier checks HEAD identity and Git objects, not working-tree dirtiness.
  Subsequent source admission retains its own clean-source checks.

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

- [x] The original source contribution was clean/pushed at Rust
  `12c0db5dde7c6a61a040e5ff56755d5756cdee68`; 134 scoped tests, real-Git/actual
  Bash fixtures, pinned actionlint and normal hooks passed. That historical
  worker checkpoint is separate from the integrated/main delivery above.
- [x] Review and qualify the parent's exact integrated tip through applicable
  full local and hosted checks; first deployment must select full because the
  trusted base lacks the helper.
- [x] Prove a subsequent genuine README-only change uses the trusted helper,
  retains all required aggregate contexts and accepts only deliberate heavy
  skips after real lightweight validation.
- [x] Retain regression coverage for event/base/head/merge identity, complete
  multi-commit ranges, strict TOML types, modes/renames/binary changes, helper
  tampering/failure, and aggregate failure/skip rejection.
- [x] Record actual hosted timing and source-bound receipts. No fixed speed
  guarantee follows from source inspection or local fixture success.

The parent integrates authored contributions linearly into one coherent batch
PR per affected repository. Beta 3 promotion, APK/signing and long soak remain
held; no source pass transfers to a changed integration head.

### Repeated Inspection And Repair Evidence

Round one independently reviewed the trusted-base classifier and strict
aggregate accounting. Round two found incomplete full-gate receipt paths and
an actual inherited `npm_config_call` process-boundary failure. Local full gate
`68886` failed after 123 seconds while admitting the Playwright command, before
Linux/Android qualification; it did not pass the full matrix or attempt a
browser download.

The scoped shared-child-environment repair at Rust `b0c34ee1` passed 39 focused
tests. A real pinned npm 11.20 offline probe retained the same command arguments:
the contaminated child failed and the isolated child succeeded. This proves
that process-boundary repair, not browser, network or product-runtime behavior.
The separate complete-receipt repair and normal hooks are included in the
clean/pushed Rust checkpoint
`288c571c9c391726b589eae42daee021d8de58b6`. The final combined-source local and
hosted qualification is recorded above; the later actual merged-main README
proof is separately retained and accepted there.
