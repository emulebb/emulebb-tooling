---
id: FEAT-079
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/74
title: Save known and cancelled metadata from immutable background snapshots
status: OPEN
priority: Minor
category: feature
labels: [known-met, persistence, metadata, background-worker, performance, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-24
source: review of background parallel processing opportunities; 2026-05-27 senior C++ performance and I/O review
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/74. This local document is retained as an engineering spec/evidence record.

# FEAT-079 - Save known and cancelled metadata from immutable background snapshots

## Summary

`known.met` and `cancelled.met` persistence is now safer than stock because
writes are staged and promoted atomically, but the save path still serializes
live known-file maps on the caller path. On very large profiles, that can become
a UI or main-loop latency spike even when the write itself is safe.

Move the expensive file serialization to a background worker by first building
an immutable save-record snapshot on the owner thread, then letting the worker
write and atomically promote the metadata file.

## Current Evidence

- `CKnownFileList::Process` periodically requests `known.met` persistence.
- `CKnownFileList::Save` still serializes `known.met` and `cancelled.met` on
  the caller path even though temp-file promotion is now safer.
- Large libraries can turn that whole-list serialization into an avoidable
  latency spike.
- The atomic temp/replace behavior is valuable and should be preserved; the
  review target is caller-thread latency, not format or durability drift.

## Intended Shape

- Keep `CKnownFileList` and live `CKnownFile` ownership on the current owner
  thread.
- Build immutable save records from the live maps under the existing ownership
  rules.
- Pass only value records to a background writer.
- Keep the current temp-file and atomic promotion behavior.
- Coalesce repeated save requests while one save is in flight.
- Report worker completion/failure through diagnostics without blocking the UI.
- Apply save success/failure state back on the owner path so worker failures do
  not mutate live known-file structures directly.

## Scope Constraints

- Do not change `known.met`, `cancelled.met`, or `known2.met` formats.
- Do not let the worker hold raw `CKnownFile*` or mutate known-file maps.
- Do not allow shutdown to exit before required final metadata writes are either
  completed or explicitly skipped by existing shutdown policy.
- Do not combine this with SQLite or broad metadata-store redesign; that remains
  separate local-state planning.

## Acceptance Criteria

- [ ] known/cancelled save requests build immutable records before dispatch
- [ ] background writer writes temp files and promotes atomically
- [ ] repeated save requests coalesce without losing a required final save
- [ ] shutdown behavior remains deterministic
- [ ] stale snapshot handling is explicit when live maps change during an
      in-flight save
- [ ] binary golden files prove unchanged `known.met` and `cancelled.met`
      output for representative profiles
- [ ] native tests cover coalescing, worker failure, atomic promotion, and
      shutdown/final-save decisions
- [ ] large-profile profiling shows reduced caller-thread latency during
      periodic metadata saves

## Validation

- `python -m emule_workspace validate`
- focused native persistence tests for snapshot save records
- large synthetic known-file map save latency test
- x64 Debug and Release app builds before commit
