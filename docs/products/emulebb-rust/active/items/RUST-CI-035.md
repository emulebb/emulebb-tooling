---
id: RUST-CI-035
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/293
title: Separate mandatory Windows/Linux gates from optional platform outcomes
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/293. This local document owns the durable engineering specification and evidence.

# RUST-CI-035 - Separate mandatory Windows/Linux gates from optional platform outcomes

## Summary

Parent-reserved RUST-CI-035 owns the user-authorized split. CI combines Linux ARM/Windows/macOS in build-test and requires Android; release smoke/images depend on the entire native matrix, and the assembler hardcodes macOS assets. Docs alone cannot implement the new gate.

## Release Placement

Beta 3 blocker for Windows/Linux.

Priority: Major. Delivery lane: beta3-platform-gates.

## Current Findings

The original workflow needs/matrix and assembler contract were verified
statically. The isolated implementation below changes workflow definitions;
no release workflow has been dispatched or candidate certified under this item.

- `repos/emulebb-rust/.github/workflows/ci.yml:222`
- `repos/emulebb-rust/.github/workflows/ci.yml:709`
- `repos/emulebb-rust/.github/workflows/release.yml:133`
- `repos/emulebb-rust/.github/workflows/release.yml:267`
- `repos/emulebb-rust/.github/workflows/release.yml:438`
- `repos/emulebb-rust/.github/workflows/release.yml:630`
- `repos/emulebb-build/emule_workspace/release_candidate.py:124`
- `repos/emulebb-tooling/docs/products/emulebb-rust/active/items/RUST-CI-009.md:210`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_multi-platform.md` section beta3-gate-split

## Acceptance Criteria

- [ ] Define an explicit mandatory Windows/Linux target and artifact contract; separately identify optional macOS, Android and other platform work.
- [ ] Separate required-summary and candidate dependency graphs so an optional OS-only failure cannot skip mandatory smoke/assembly.
- [ ] Keep shared source, workflow lint, quality, supply-chain, CodeQL, REST, integrity and provenance failures mandatory.
- [ ] Publish independent optional results and failures; do not blanket continue-on-error shared checks.
- [ ] Update assembler inventory/manifest validation and failure-injection tests for missing optional versus mandatory assets.
- [ ] Preserve enforced checks until the reviewed workflow change lands; tagging/publication remain separately authorized.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

## Implementation In Progress

The managed `rust-platform-gates` workstream owns one coordinated outcome
across Rust workflow/control code, Builder candidate assembly, and this spec.
The Rust checkout explicitly depends on the parent's unpublished native-source
foundation at `2bc122715712621cc9378d9dcd20677ec0d52bbb`; the parent must
integrate that foundation before publishing this feature without duplicate
commits. Builder integration and its immutable workflow pin update precede
the Rust consumer PR.

- Required CI keeps Linux GNU and Windows native x64/ARM64, both native musl
  CPUs, REST/OpenAPI, shared quality, workflow lint and supply-chain checks.
  Required CodeQL and the existing ruleset check names remain unchanged.
- macOS native build/tests and Android compilation move to an independent
  optional workflow with its own concurrency group, pinned dependencies,
  failure-aware aggregate and visible failures. No continue-on-error waiver
  or observer failure suppression is introduced.
- Release control selects an explicit `full` or `windows-linux` profile before
  producers run. `full` remains the default and retains all six native targets,
  both musl CPUs, both OCI variants/architectures and existing proofs. The
  reduced profile is restricted to unpublished manual candidate code paths;
  nightly, tags and publication reject it.
- Selected native packaging/smoke matrices share the validated profile output.
  Optional macOS packaging/smoke uses a separate artifact namespace and cannot
  skip mandatory smoke, OCI verification or assembly. Full assembly still
  requires macOS, and full source qualification also requires the latest exact
  optional-platform workflow attempt to pass.
- Candidate format 4 binds `platformProfile` to caller-owned source/workflow
  identities. Strict selected inventories retain native/musl payloads, hashes,
  SPDX, lifecycle, image security and provenance checks. Writers and verifiers
  change together; no format is inferred from whatever files happen to exist.
- Source qualification waits within an eight-minute budget for pending/missing
  exact-source workflows, rechecking the latest invocation/attempt. Terminal
  failures and malformed inventories fail immediately. Scheduled nightly
  timeouts retain their exact-source skip reason and later scheduled retry;
  neither old green sources nor old successful attempts are substituted.

Initial Windows/private CPython 3.15.2 lightweight evidence:

- Builder candidate/profile synthetic tests: 72 passed. Existing assembly
  subset: 11 passed. These execute the real manifest/inventory validators,
  including missing mandatory assets, provenance failures, profile binding,
  and full-versus-reduced inventories.
- Rust release/source-qualification/policy/graph tests: 176 passed, 118 subtests
  passed, one POSIX aggregate-shell test skipped on Windows. Pending-to-success,
  terminal failure, timeout and stale-attempt behavior use deterministic mocks;
  no real qualification polling or release workflow was launched.
- Actual aggregate-shell failure injection remains a Linux proof obligation.
  Normal pre-push and hosted checks have not run for this feature.
- Builder's normal fast commit checks passed at `04e5617`. Rust's normal
  commit hook passed environment provenance, actionlint and the client policy,
  then found one stale Android workflow-location assertion in its broader
  unittest discovery (238 cases, one error and one POSIX-only skip). Correct
  that consumer test and rerun the normal hook after the scratch hold permits
  tests; do not bypass it or treat the Rust checkpoint as committed.

The operator's HDD-pressure hold stops further local tests until the approved
scratch backend is ready. Preserve the checkpoint, required validation and
release hold; no native/Docker/live work, push or publication is authorized by
these lightweight results.
