---
id: RUST-BUG-105
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/26
title: Disposition stock source-acquisition default drift
status: DONE
priority: Major
category: bug
labels: [rust, ed2k, sources, scheduling, parity]
milestone: post-beta-compatibility
created: 2026-10-03
source: Product authority decision plus stock/aMule review and maintained eMuleBB MFC source
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/26. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-105 - Disposition stock source-acquisition default drift

## Summary

The source-limit difference is an intentional operational policy, not a wire
compatibility defect. Stock/community eMule remains authoritative for eD2K/Kad
wire semantics. Maintained eMuleBB MFC is authoritative for non-wire operational
limits and disk/network I/O outcomes, implemented through Rust-native async
architecture. Stock wire behavior wins if those authorities conflict.

## Disposition

- Retain the eMuleBB MFC broadband source target and ceilings: configured
  `maxSources` default 600, soft ceiling 1,000, and UDP ceiling 100.
- Retain the stock-compatible formulas `min(maxSources * 9 / 10, 1000)` and
  `min(maxSources * 3 / 4, 100)`. At the default target they yield effective
  soft and UDP per-file caps of 540 and 100.
- Treat stock eMule's and current aMule's lower operational values as comparison
  evidence, not as the Rust product target.
- Keep packet shapes, per-request packet bounds, source deduplication, query and
  reask pacing, connection budgets, retry backoff, and other wire-facing
  behavior stock-compatible and independently bounded.
- Do not add a stock-conservative profile. Operational authority is a product
  policy, not a compatibility toggle.

## Product Policy

The general authority split is recorded in the Rust product policy, release
scope, and machine-readable `policy/rust-client.toml`. Its checker rejects a
missing, changed, or extended authority table. Intentional divergence from MFC
operational limits or I/O outcomes requires a future tracked disposition.

Rust REST, UI, settings shape, controllers, and threading are not MFC mirrors.
The MFC authority defines operational limits and observable I/O outcomes; Rust
owns the idiomatic async implementation.

## Implementation

- Corrected source-limit comments and test names that had attributed the
  600/1,000/100 values to the stock oracle.
- Kept the existing `maxSourcesPerFile` setting as the configured target and
  clarified its operator-facing description. The derived soft/UDP caps remain
  internal scheduling values.
- Added an enforced behavior-authority table covering stock wire precedence,
  MFC operational limits and I/O behavior, and Rust-native async
  implementation.
- Made no numeric, persistence, REST, OpenAPI, schema, `apiVersion`, or runtime
  behavior change, so no migration, release toggle, or new diagnostic field is
  required.

## Provenance

- eMuleBB MFC `Preferences.h` sets the 600 source default; blame resolves that
  line to commit `8d310d9c9`.
- eMuleBB MFC `Opcodes.h` sets the 1,000 soft and 100 UDP ceilings; blame
  resolves those lines to commit `860d7a5ad`.
- eMuleBB MFC `PartFile.cpp` applies the stock-compatible 9/10 and 3/4 formulas
  before clamping to those ceilings.
- Rust implementation and machine-policy commit:
  `emulebb/emulebb-rust@19654e01`.

## Acceptance Criteria

- [x] Every source-limit constant and default has accurate MFC provenance or an
      explicit product-policy rationale.
- [x] The MFC broadband profile is documented consistently in product policy,
      machine policy, configuration comments, tests, and the operator-facing
      setting description.
- [x] Wire-compatible UDP request sizing and packet bounds remain unchanged.
- [x] Per-file source caps, global reask pacing, connection budgets,
      deduplication, and retry backoff remain bounded by the existing tested
      coordinator and acquisition paths.
- [x] No migration is required because persisted values, defaults, meanings,
      schemas, and runtime behavior did not change.
- [x] The parity and release-scope language now states the authority split
      instead of attributing MFC limits to stock/community references.

## Evidence

- `python -m unittest tools.tests.test_check_rust_client_policy` - 22 passed.
- `python tools/check_rust_client_policy.py` - passed.
- `cargo fmt --all -- --check` - passed.
- `python tools/rust_quality_gate.py quick` - policy and 50 policy-tool tests,
  rustfmt, workspace clippy with warnings denied, diagnostics build, 22 WebUI
  unit tests, 15 Chromium end-to-end tests, typecheck, and SPA build passed.
- `python -m emule_workspace test rust-unit --config Release --build-output-mode ErrorsOnly`
  - the complete Rust unit/integration/doc-test suite passed.
- `python -m emule_workspace validate --include-product-family --product-family-tier quick`
  passed its policy audits, then stopped at the workspace artifact audit on 70
  pre-existing virtual-environment binaries in unrelated repositories. No
  workspace artifacts were removed or modified for this item.
- Tooling taxonomy, structure/wide-table, and local roadmap metadata checks
  passed. The GitHub-wide roadmap audit reported 363 pre-existing non-Rust
  Project #2/label mismatches; no Rust item mismatch was reported.
- Strict docs publication reached MkDocs and stopped on an unrelated stale
  RUST-BUG-104 link in an existing idea page.

## Validation Scope

No live, soak, stock/aMule fixture, or MFC rebuild was required: the selected
MFC values and bounded acquisition behavior were already implemented, and this
change records and enforces their authority without changing runtime behavior.
