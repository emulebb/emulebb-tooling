---
id: FEAT-076
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/72
title: Parallelize shared-file hashing across physical volumes and SSDs
status: OPEN
priority: Minor
category: feature
labels: [hashing, shared-files, performance, storage, ssd, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-24
source: operator request for parallel hashing from different physical volumes and SSD drives
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/72. This local document is retained as an engineering spec/evidence record.

# FEAT-076 - Parallelize shared-file hashing across physical volumes and SSDs

## Summary

Shared-file hashing should be able to use more concurrency when the workload is
backed by independent physical storage, especially SSDs. The goal is to reduce
large-library scan/hash time without turning one mechanical disk into a random
I/O bottleneck or starving the UI.

## Intended Shape

- Detect or classify hashing candidates by physical volume/device where
  practical.
- Allow parallel hashing across different physical volumes.
- Set per-volume hashing worker limits from storage class, with conservative
  defaults for rotational HDDs, higher bounded limits for SSD/NVMe, and
  fail-safe limits for network/removable or unknown storage.
- Allow controlled higher parallelism for SSD-backed volumes and across
  independent physical devices.
- Keep conservative serialization or low concurrency for a single rotational
  disk by default.
- Keep UI progress, cancellation/shutdown, and known-file persistence ordering
  deterministic.
- Add diagnostics so live profiling can explain chosen worker counts and volume
  grouping.
- Keep worker ownership explicit: workers may perform file I/O and hashing, but
  shared-file map mutation, UI updates, and final `CKnownFile` adoption remain
  on the owning application/UI path.

## Current Mainline Evidence

Current `main` already has a long-lived shared-file hash worker and queue, but
actual hashing is still serialized:

- `CAddFileThread::Run()` takes `theApp.hashing_mut` before hashing one file.
- `CSharedFileList::RunSharedHashJob()` also takes `theApp.hashing_mut` before
  creating the `CKnownFile` from disk.

That serialization is intentional for safety, but it is now the main limit for
large multi-volume and SSD-backed profiles. FEAT-076 should replace the single
global hash bottleneck with a bounded scheduler, not with unbounded per-file
threads.

## Scope Constraints

- Do not alter eD2K/AICH hash semantics or on-disk known-file formats.
- Do not introduce unbounded worker creation.
- Do not regress slow HDD behavior to improve SSD-only scenarios.
- Do not make physical drive detection a hard startup dependency; fall back to
  the current conservative policy when detection is uncertain.
- Do not let background workers mutate `CSharedFileList`, `CKnownFileList`,
  MFC controls, or upload/download queue state directly.
- Do not parallelize part-file hash write-back without preserving the existing
  hash-layout generation checks.

## Acceptance Criteria

- [ ] hashing scheduler groups candidates by physical volume/device when known
- [ ] candidates on distinct physical volumes can hash concurrently
- [ ] per-volume hashing thread limits differ for HDD, SSD/NVMe,
      network/removable, and unknown storage
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
