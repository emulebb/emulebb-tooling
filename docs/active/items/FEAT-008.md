---
id: FEAT-008
title: Oracle protocol guard seams — integrate stale branch test scaffolding
status: OPEN
priority: Trivial
category: feature
labels: [testing, protocol, oracle, stale-branch]
milestone: ~
created: 2026-04-08
source: Stale branch remotes/origin/stale/v0.72a-experimental-clean (commit message: "TEST add oracle protocol guard seams")
---

> Historical reference only: `stale-v0.72a-experimental-clean` and
> `analysis\stale-v0.72a-experimental-clean` are retired reference sources, not
> active branch targets or current baselines. Use them only as provenance or
> idea-extraction sources; landed status is determined against `main`. See
> [Historical References](../../HISTORICAL-REFERENCES.md).

## Background

The stale experimental branch (`remotes/origin/stale/v0.72a-experimental-clean`,
tag `archive/v0.72a-experimental-clean-provisional-20260404`) contained work
titled "TEST add oracle protocol guard seams".

This was scaffolding for oracle-style test seams around protocol state machines —
a testing pattern where known-good protocol traces are replayed and the oracle
records expected output, which is then compared against future runs to detect
regressions.

## Current State

- The stale branch work was NOT merged into main.
- The concept is sound: the main tree already has `emulebb-build-tests` harness
  with bugfix regression seams for packet parsing.
- The oracle guard pattern extends that with richer state-machine coverage.

## Open Questions Before Implementing

1. What specific protocol state machines were targeted? (Upload queue flow?
   Kad search? Connection lifecycle?)
2. What format were the oracle traces stored in? (Binary packet dumps?
   Serialised state snapshots?)
3. Are the seam injection points still valid in the current tree?

## Proposed Action

1. Read the actual diff of the stale branch against its parent.
2. Extract the seam injection logic that doesn't depend on removed code.
3. Integrate compatible seams into the existing `emulebb-build-tests` harness.
4. Discard scaffolding that targeted code since refactored away.

## Priority

Trivial — low priority until the testing infrastructure (CI-001 through CI-006)
is in better shape.
