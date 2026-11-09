---
id: RUST-BUG-183
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/290
title: Verify and upstream the PCP socket-initialization allocation leak
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/290. This local document owns the durable engineering specification and evidence.

# RUST-BUG-183 - Verify and upstream the PCP socket-initialization allocation leak

## Summary

The context allocation precedes socket creation; the failing socket path returns null without returning ownership. The existing fork does not establish a fix. Confirm against the pinned upstream revision and prefer a small upstream correction.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: upstream-dependency.

## Current Findings

Static source/spec review; no validation executed.

- `repos/third_party/emulebb-libpcpnatpmp/lib/src/pcp_api.c:110`
- `repos/third_party/emulebb-libpcpnatpmp/lib/src/pcp_api.c:137`

## Audit Provenance

- `LIBPCPNATPMP-CONSUMER-REFACTOR-AUDIT-2026-11-09.md` section upstream-init-leak

## Acceptance Criteria

- [ ] A fault-injected socket failure proves allocation release.
- [ ] Record the upstream issue/patch disposition and exact imported revision.
- [ ] Do not add allocator interception or claim the consumer can free an unreturned pointer.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.
