---
id: RUST-BUG-172
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/274
title: Omit unavailable MD4 sections from modern hashset answers
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/274. This local document owns the durable engineering specification and evidence.

# RUST-BUG-172 - Omit unavailable MD4 sections from modern hashset answers

## Summary

The encoder still sets the MD4-present bit for Some(empty) with a multi-part size. Serving callers obtain metadata through the runtime, so production reachability must be demonstrated; the encoder currently cannot enforce the stock expected-count invariant.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-hardening.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/codec/hashset.rs:48`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/listener/session/shared_file.rs:444`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_hashset-largefile.md` section 2.1

## Acceptance Criteria

- [ ] Trace all production callers and model unavailable/partial metadata explicitly.
- [ ] Do not emit a present but zero-count MD4 section for an unavailable multi-part set.
- [ ] Retain valid small-file and complete modern hashset exchanges.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.
