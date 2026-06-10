---
id: FEAT-114
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/153
title: Add storage-aware hash and verify throttling
status: OPEN
priority: Minor
category: feature
labels: [hashing, verification, disk-io, storage, hdd, performance, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-10
source: operator I/O and filesystem performance review
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/153. This local document is retained as an engineering spec/evidence record.

# FEAT-114 - Add Storage-Aware Hash And Verify Throttling

## Summary

Make background hash and verification work yield more deliberately to active
downloads and uploads on the same storage volume, especially on mechanical and
SMR disks. The goal is smoother transfer I/O, not maximum hash throughput.

This complements `FEAT-076`, which covers safe parallel hashing across
independent volumes and SSDs. This item covers throttling, priority, and
same-volume contention control.

## Intended Shape

- Track which volume backs each hash, verify, temp, incoming, and shared-file
  operation where practical.
- Keep hash/verify workers conservative on a single rotational or unknown
  volume when active transfers are using that volume.
- Allow SSD/NVMe and independent-volume workloads to keep higher bounded
  throughput when contention is low.
- Lower thread priority or insert cooperative yield windows for long sequential
  hash/verify passes.
- Pause, slow, or defer expensive verification when upload/download latency on
  the same volume is already high.
- Expose diagnostics explaining when hash/verify work was delayed because of
  storage contention.

## Scope Constraints

- Do not change ED2K, AICH, or known-file hash semantics.
- Do not make drive-type detection mandatory; unknown storage must fall back to
  conservative behavior.
- Do not block explicit user-requested hashing forever because transfers are
  active.
- Do not introduce unbounded queues or worker creation.
- Do not hide real hash failures behind throttling diagnostics.

## Acceptance Criteria

- [ ] Hash/verify work can identify or conservatively group work by backing
      volume.
- [ ] Same-volume hash/verify activity is throttled when active transfers are
      competing on HDD, SMR, removable, network, or unknown storage.
- [ ] SSD/NVMe and independent-volume cases retain bounded parallelism where
      safe.
- [ ] User-visible progress remains responsive and cancellation still works.
- [ ] Diagnostics report throttled, delayed, and resumed hash/verify work.
- [ ] Existing hash outputs, known-file records, and AICH persistence remain
      byte-compatible.

## Validation

- focused scheduler tests for same-volume and cross-volume decisions
- native tests or harness probes for cancellation and progress behavior
- source checks proving hash bytes and persistence formats are unchanged
- HDD/SSD live smoke where available
- x64 Debug and Release app builds before implementation commit
