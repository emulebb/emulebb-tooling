---
id: FEAT-009
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/58
title: Mirror audit guard seam — WIP work from stale branch parent commit
status: OPEN
priority: Trivial
category: feature
labels: [testing, audit, mirror, stale-branch]
milestone: ~
created: 2026-04-08
source: Stale branch parent commit 226356a "WIP mirror audit guard seam for oracle tests"
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/58. This local document is retained as an engineering spec/evidence record.

## Background

The parent of the oracle seam work (commit `226356a`, "WIP mirror audit guard seam
for oracle tests") contains incomplete work on a "mirror audit guard seam" — a test
mechanism designed to verify that two code paths (the "oracle" and the live
implementation) produce identical or compatible outputs for the same inputs.

The intent appears to be a parity check: given a protocol trace, verify that
the current implementation's output matches the recorded oracle output byte-for-byte
or within an allowed delta.

## Current State

- WIP — not merged, not completed.
- The concept is related to FEAT-008 (oracle guard seams) and is a dependency or
  companion to that work.

## Open Questions

1. What was the "mirror" — two different code paths in the same binary, or a
   reference implementation in the test harness?
2. What audit property was being verified? (Bit-exact output? Semantic
   equivalence? Error-handling parity?)

## Proposed Action

1. Review the actual diff of commit `226356a` against its parent.
2. Determine if the mirror audit approach is compatible with the existing
   `emulebb-build-tests` infrastructure.
3. If salvageable: fold into FEAT-008 as the "oracle comparison" phase.
4. If not salvageable: close as Wont-Fix.

## Priority

Trivial — depends on FEAT-008 assessment.

## Dependency

Blocked on or subsumed by: FEAT-008.
