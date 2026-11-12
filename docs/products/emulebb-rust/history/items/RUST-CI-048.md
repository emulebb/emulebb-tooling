---
id: RUST-CI-048
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/323
title: Run Clippy and WebUI type checks before platform fanout
status: DONE
priority: Major
category: ci
labels: [rust]
milestone: ""
created: 2026-11-12
source: Operator-approved hosted preflight and PM integration batching
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/323. Project #3 owns placement; this item owns the engineering contract.

# RUST-CI-048 - Run Clippy and WebUI type checks before platform fanout

## Closure And Evidence

[PR #326](https://github.com/emulebb/emulebb-rust/pull/326) merged as
`080a5dea70186da31dab958757b5b8c0fd883f82`. The parent closed
[#323](https://github.com/emulebb/emulebb-rust/issues/323#issuecomment-6829949478)
after actual-main [CI 43230067399](https://github.com/emulebb/emulebb-rust/actions/runs/43230067399)
and the separately source-gated, published
[Nightly 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692)
passed. Typecheck and existing all-targets Clippy run before primary native/musl
fanout; full coverage and exact-source admission remain in force.

The scoped 102-second preflight measurement below remains one observation,
not a guaranteed cold-build duration. Developer-selective checks stay with
#258; the next trusted change-aware hosted short path belongs to #327. Neither
is claimed delivered by this item. The original contract below is historical;
the current standing coordination policy governs later batches.

## Outcome And Ownership

Run existing Clippy and WebUI type checks once before expensive primary
Windows/Linux/musl fanout. The assigned Rust workflow worker owns implementation;
the parent owns integration batches and acceptance. Developer-selective,
dependency-aware checks remain separately owned by
[#258 / RUST-CI-032](../../active/items/RUST-CI-032.md).

## Required Behavior

- Reuse `tools/rust_quality_gate.py clippy`, retaining workspace/all-targets,
  locked dependency resolution and warnings denied.
- Add `--typecheck-only` to the existing `tools/test_webui.py` owner. Reuse pinned
  `ci_environment.prepare_command`, locked `npm ci --ignore-scripts`, isolated
  output staging and `npm run typecheck`. Default unit/Playwright/build behavior
  stays complete.
- Add one primary hosted preflight after PR coordination and workflow lint.
  Use pinned Ubuntu 24.04 tools/native checkouts and exact source/material
  admission before and after execution. Keep inventory, output and provenance
  under the existing owners.
- Require explicit preflight success for primary native/musl fanout and in
  `Required CI`. Skipped, cancelled or failed preflight cannot count as success.
- Keep optional-platform workflows independent and preserve all current full
  Clippy, WebUI, protocol, REST, runtime, platform and publication checks.

## Acceptance And Validation

- [ ] Clippy/type failures stop primary platform fanout before those jobs run.
- [ ] The default WebUI path remains complete and type-only staging never writes
      generated dependencies or output into source.
- [ ] Source/native-material checks reject dirty, foreign or changed inputs.
- [ ] Existing `test_webui_workspace`, `ci_environment`, `ci_parity`,
      `platform_gate_graph` and `check_rust_client_policy` owners cover selection,
      explicit dependency success and aggregate rejection behavior.
- [ ] Normal hooks, scoped regressions and applicable hosted qualification pass
      on the exact implementation head. Retain reports under the configured
      output root and link hosted run identities from the owning issue.
- [ ] Record measured feedback timing and cold-build limits. Clippy may compile
      dependencies/all targets; there is no fixed fast-duration promise.

## Scoped Hosted Evidence

[PR #326's hosted preflight](https://github.com/emulebb/emulebb-rust/actions/runs/43220233958/job/131189869166)
passed for PR head `1c95ea6c`: 102 seconds total, including typecheck 3 seconds
and Clippy 61 seconds. The exact merge-event/native-source fences passed and
all six primary platform jobs were admitted afterward. This is one scoped
timing result, not full-matrix completion or a fixed cold-build guarantee.

## Coordination Limits

Finish this existing lane and the documentation intake through reviewable PRs
and full applicable hosted qualification in parallel now. The parent coordinates
normal-gated merges, then freezes the final combined mains/source pins for one
full nightly and actual public-byte acceptance. No intermediate nightly blocks
these PRs, and no Scoop/storage implementation or additional lane begins before
closeout. Integration batching is PM work, not a scheduler, queue, cache program,
machine or capacity change.

Beta 3 promotion, APK/signing and long soak remain held. This item does not
change pre-push coverage or replace complete applicable qualification.
