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
The current source refresh uses Rust main `a8d6189c`, Builder main `43abac2d`
and Tooling main `dad45eef` as its bases. Current source-selection repairs and
the experimental Android nightly graph are retained. Builder integration and
its immutable workflow pin update precede the Rust consumer PR.

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
- Full nightly assembly retains both experimental Android ABI packages and
  their existing source, compile/ELF, checksum and inventory validation.
  Android may be skipped only by a non-nightly candidate's existing condition.
- Selected native packaging/smoke matrices share the validated profile output.
  YAML step anchors share the package and smoke recipes across the selected
  and optional jobs. Fixed job-local prefixes retain their distinct artifact
  namespaces while checkout identities and lifecycle sources share one recipe.
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
  Each Actions API request uses the remaining deadline, and a result arriving
  after the deadline cannot qualify the source.

## Merge Readiness And Independent Outcomes

The enforced default-branch contexts are `Single active PR`, `Required CI` and
`Required CodeQL`, with the existing strict up-to-date rule. The parent checks
those contexts and their source identities at the actual pull-request HEAD.
Native Windows/Linux x64 and ARM64 remain in the mandatory graph, together
with both native musl CPUs and the shared quality, security and REST checks.

The persisted GitHub observer continues reporting every head workflow,
including pending or failed optional platform work. Its complete-outcome view
does not replace the enforced-context decision. Optional failures retain their
own failed checks and summaries. Full nightly and publication eligibility
still require the optional source qualification and every included artifact's
own validation.

The prepared-image producer under RUST-CI-045 binds its digest and attestation
to the exact Builder revision. After the Builder profile changes merge, a new
producer run must verify that merged source before the prepared-image consumer
and this release profile consumer select its immutable revision and digest.
Release guidance/finalization functions and prepared-image provisioning/pins
remain coordinated workstream ownership boundaries during source integration.

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
- Builder's normal fast commit checks passed at
  `04e5617`. Rust's normal commit checks passed at
  `2ea95e9a0a0a1ebcd38a7228d00feb1cec93039c`: environment provenance,
  actionlint, client policy, 238 unittest cases (one POSIX-only skip), and
  rustfmt. The Android consumer regression reads the new optional workflow
  and retains its ABI, immutable pin and provenance assertions.

## Refreshed Source Checkpoint

- Builder `b7a1e4b0044e111efe793361ab8b395a54d8b5f1` preserves Android nightly
  inventory and rejects reduced nightly assembly. Its normal fast commit
  checks passed. The refreshed Builder synthetic suites await their supported
  serialized runner slot.
- Rust `f749c50b31593ebd66f3e0749fae8e0d1b732806` passed the normal workflow
  commit checks, including environment provenance, actionlint, client policy,
  256 unittest cases with one POSIX-only aggregate-shell case skipped on
  Windows, and rustfmt. Regression coverage retains Android assembly joins,
  mandatory native ARM64 membership, independent optional failures and bounded
  source qualification.
- Normal full local pre-push validation, the Linux aggregate-shell proof and
  independent hosted qualification remain pending. Full local pre-push checks
  continue using the workspace validation lock.
- The Rust release workflow's final Builder pin awaits the actual merged
  profile API. Current source checkpoints remain unpublished until the
  coordinated immutable pins and qualification are complete.
