---
id: FEAT-076
title: Parallelize shared-file hashing across physical volumes and SSDs
status: OPEN
priority: Minor
category: feature
labels: [hashing, shared-files, performance, storage, ssd, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-24
source: operator request for parallel hashing from different physical volumes and SSD drives
---

# FEAT-076 - Parallelize Shared-File Hashing Across Physical Volumes And SSDs

## Summary

Shared-file hashing should be able to use more concurrency when the workload is
backed by independent physical storage, especially SSDs. The goal is to reduce
large-library scan/hash time without turning one mechanical disk into a random
I/O bottleneck or starving the UI.

## Intended Shape

- Detect or classify hashing candidates by physical volume/device where
  practical.
- Allow parallel hashing across different physical volumes.
- Allow controlled higher parallelism for SSD-backed volumes.
- Keep conservative serialization or low concurrency for a single rotational
  disk by default.
- Keep UI progress, cancellation/shutdown, and known-file persistence ordering
  deterministic.
- Add diagnostics so live profiling can explain chosen worker counts and volume
  grouping.

## Scope Constraints

- Do not alter eD2K/AICH hash semantics or on-disk known-file formats.
- Do not introduce unbounded worker creation.
- Do not regress slow HDD behavior to improve SSD-only scenarios.
- Do not make physical drive detection a hard startup dependency; fall back to
  the current conservative policy when detection is uncertain.

## Acceptance Criteria

- [ ] hashing scheduler groups candidates by physical volume/device when known
- [ ] candidates on distinct physical volumes can hash concurrently
- [ ] SSD-backed volumes can use controlled parallel hashing
- [ ] single rotational-disk workloads remain conservative by default
- [ ] cancellation, shutdown, and persistence remain safe under parallel work
- [ ] profiling evidence compares current behavior, multi-volume behavior, and
      SSD behavior on representative live profiles

## Validation

- `python -m emule_workspace validate`
- focused native scheduler/hash tests for volume grouping and worker limits
- shared-files startup/hash regression tests
- live profiling with the operator-provided large shared-file profile
- x64 Debug and Release app builds before commit
