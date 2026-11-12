---
id: RUST-CI-035
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/293
title: Separate mandatory Windows/Linux gates from optional platform outcomes
status: DONE
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

Delivered the operator-authorized separation of mandatory Windows/Linux merge
checks from visible optional platform outcomes, with explicit full versus
unpublished Windows/Linux candidate profiles. Full nightly and publication
retain their complete selected inventory and qualification requirements.

## Closure And Evidence

[#293](https://github.com/emulebb/emulebb-rust/issues/293) is closed and Project
#3 records Done. [Rust PR #314](https://github.com/emulebb/emulebb-rust/pull/314)
merged on 2026-11-11 as
`08bfe94bc9edb8f449e67439e9757808de342d54`, consuming the merged Builder profile
provider at `995d13f350c8342437fdb3122d2a271696ac6e29` from
[Builder PR #53](https://github.com/emulebb/emulebb-build/pull/53).

The reduced, unpublished `windows-linux` candidate was exercised by
[run 43206709335](https://github.com/emulebb/emulebb-rust/actions/runs/43206709335)
at Rust `a099bf45871998a5a7f88e844212fce9fb15eaba`: eight packages, six lifecycle
platforms, both OCI variants and four native OCI proofs passed; publication was
skipped. Later [full Nightly 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692)
at `080a5dea70186da31dab958757b5b8c0fd883f82` independently passed all twelve
payloads and eight lifecycle platforms, then published. Its 81 public assets
and both OCI graphs were verified against exact source and provenance.

Retained receipts are under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/packaging-identity/prepared-consumer-43206709335`
and `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/nightly-publication-review/43242135692`.
These are distinct source/profile executions; neither substitutes for a future
Beta 3 candidate. Beta 3 certification, publication approval and long soak
remain separate held outcomes. Earlier implementation and pending-proof
statements below are dated premerge provenance, superseded by this closure.

## Release Placement

Delivered Windows/Linux Beta 3 prerequisite; candidate certification remains
owned by [RUST-CI-009](../../active/items/RUST-CI-009.md).

Priority: Major. Delivery lane: beta3-platform-gates.

## Historical Initial Findings

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

- [x] Define an explicit mandatory Windows/Linux target and artifact contract; separately identify optional macOS, Android and other platform work.
- [x] Separate required-summary and candidate dependency graphs so an optional OS-only failure cannot skip mandatory smoke/assembly.
- [x] Keep shared source, workflow lint, quality, supply-chain, CodeQL, REST, integrity and provenance failures mandatory.
- [x] Publish independent optional results and failures; do not blanket continue-on-error shared checks.
- [x] Update assembler inventory/manifest validation and failure-injection tests for missing optional versus mandatory assets.
- [x] Preserve enforced checks until the reviewed workflow change lands; tagging/publication remain separately authorized.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

## Historical Implementation Checkpoint

The managed `rust-platform-gates` workstream owns one coordinated outcome
across Rust workflow/control code, Builder candidate assembly, and this spec.
The Builder provider is refreshed onto main `8c471fdc` and this spec onto
Tooling main `56ea89b2`. The parked Rust candidate remains based on
`a8d6189c`; it must incorporate the integrated registered-runtime consumer
before its own qualification. Current source-selection repairs and the
experimental Android nightly graph are retained. Builder integration and its
immutable workflow pin update precede the Rust platform-graph consumer PR.
The deployed Rust graph remains unchanged until that consumer integrates.

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

The Rust platform-graph consumer needs the actual merged Builder profile API
pinned by immutable revision for candidate format 4. It uses the normal package
commands and has no prepared-image dependency. RUST-CI-045 separately binds its
prepared-image digest and attestation to an exact Builder revision; its producer
and consumer refresh follow the relevant packaging/provisioning changes.
Release guidance/finalization functions and prepared-image provisioning/pins
remain separately coordinated workstream ownership boundaries.

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
  Those source checkpoints did not establish hosted feature qualification.
- Builder's normal fast commit checks passed at
  `04e5617`. Rust's normal commit checks passed at
  `2ea95e9a0a0a1ebcd38a7228d00feb1cec93039c`: environment provenance,
  actionlint, client policy, 238 unittest cases (one POSIX-only skip), and
  rustfmt. The Android consumer regression reads the new optional workflow
  and retains its ABI, immutable pin and provenance assertions.

## Refreshed Source Checkpoint

- Builder `6a98fd4fb7c8712476fe4da1789ddd32fc91a341`, based on `8c471fdc`,
  preserves the default full inventory and Android nightly requirements while
  providing explicit reduced unpublished-candidate assembly and format-4
  profile binding. Supported managed host qualification passed 261 tests with
  zero failures, errors or skips at
  `reports/builder-unit/c6e1b54fe5ee`. The selected files cover platform
  profiles, candidate manifests, release assembly, Android packaging and CLI;
  one existing `TestTargets` collection warning was reported. No Cargo, WSL or
  runtime staging ran. The provider can be reviewed before the Rust graph changes;
  existing workflows retain their immutable older Builder pins until updated.
- Rust `f749c50b31593ebd66f3e0749fae8e0d1b732806` passed the normal workflow
  commit checks, including environment provenance, actionlint, client policy,
  256 unittest cases with one POSIX-only aggregate-shell case skipped on
  Windows, and rustfmt. Regression coverage retains Android assembly joins,
  mandatory native ARM64 membership, independent optional failures and bounded
  source qualification.
- Fast push checks and hosted workflows qualify the provider under the daytime
  validation policy. Explicit `local-check --stage full` retains the workspace
  lock; no local broad Cargo/WSL matrix runs for this provider preparation.
  Rust graph qualification, Linux aggregate-shell proof and real candidate
  assembly/publication evidence remain pending and are not implied by provider
  unit tests.
- The Rust release workflow's final Builder pin awaits the actual merged
  profile API. Rust source can then incorporate the integrated runtime consumer,
  pin that Builder and qualify through GitHub without waiting for packaging or
  image production. RUST-CI-045's producer remains separate and waits for its
  selected packaging/provisioning inputs, avoiding duplicate production jobs.
