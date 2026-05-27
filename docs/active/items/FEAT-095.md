---
id: FEAT-095
title: Move part-file durability work off foreground paths
status: OPEN
priority: Major
category: feature
labels: [part-file, persistence, disk-io, write-thread, performance, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-27
source: senior C++ performance and I/O review of part-file write and flush paths
---

# FEAT-095 - Move Part-File Durability Work Off Foreground Paths

## Summary

Part-file data writes already have an IOCP-backed write thread, but some
durability and metadata work can still run synchronously on foreground download
processing paths. On slow disks, removable storage, network-backed temp paths,
or antivirus-heavy systems, these calls can stall the UI/control loop.

## Current Evidence

- `CPartFile::Process` can call `FlushFileBuffers` after pending file activity.
- `CPartFile::SavePartFile` writes a temp `part.met` and promotes it atomically,
  but callers can still trigger metadata saves while processing buffers.
- Existing atomic replacement and backup behavior are good foundations; the
  target is latency reduction, not a persistence semantic rewrite.

## Intended Shape

1. Route part-file flush requests through `CPartFileWriteThread`.
2. Coalesce flush requests per part file while writes are pending.
3. Flush only after outstanding writes for that file have drained.
4. Coalesce dirty `part.met` saves through a metadata-writer queue where safe.
5. Preserve immediate synchronous saves for critical transitions that currently
   rely on immediate durability, such as completion, shutdown, or error paths,
   until each transition has explicit evidence.

## Scope Constraints

- Do not weaken crash-recovery guarantees without a documented replacement.
- Do not reorder part data writes ahead of metadata in a way that changes
  resume behavior.
- Do not change `.part`, `.part.met`, `.bak`, or hashset formats.
- Do not let a worker hold unsafe raw part-file ownership past shutdown.

## Acceptance Criteria

- [ ] Foreground download processing no longer calls `FlushFileBuffers`
      directly for routine delayed flushes.
- [ ] Per-file flush requests coalesce and execute after pending IOCP writes
      drain.
- [ ] Dirty `part.met` saves are coalesced where they are not critical
      transition saves.
- [ ] Critical transitions retain deterministic durability behavior.
- [ ] Forced write-error, disk-full, shutdown, pause/resume, and completion
      tests cover the new sequencing.
- [ ] ETW or app counters show reduced foreground disk-I/O stall time.

## Validation

- `python -m emule_workspace validate`
- part-file persistence and crash-recovery tests
- forced write-error and disk-full tests
- shutdown flush tests
- x64 Debug and Release app builds before commit
