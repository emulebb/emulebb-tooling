---
id: FEAT-069
title: Shared-file include and exclude pattern rules
status: OPEN
priority: Minor
category: feature
labels: [sharing, filters, regex, privacy, file-handling]
milestone: post-beta-0.7.3
created: 2026-05-21
source: aMule issue #604 triage against current shared-file policy
---

## Summary

Add optional include/exclude pattern rules for shared-file discovery so users
can avoid sharing uninteresting or frequently changing sidecar files from large
shared trees.

This extends the existing explicit single-file exclude/share model with
operator-owned pattern rules.

## Current Mainline Evidence

Current sharing policy supports listed shared directories, category/incoming
directories, explicit single-file sharing, and explicit single-file exclusion.
It does not provide include/exclude pattern rules for discovered files.

Candidate code areas:

- `CSharedFileList::ShouldBeShared(...)`
- `CSharedFileList::AddFilesFromDirectory(...)`
- `SharedFileIntakePolicy`
- preferences persistence for share rules

## Scope

- Add a small, documented rule format for include and exclude patterns.
- Apply rules only to shared-file discovery/intake.
- Prefer safe wildcard or compiled regex behavior with validation and clear
  error reporting.
- Treat include rules as optional narrowing rules; exclude rules should win over
  broad directory sharing unless the file is in a mandatory incoming/category
  surface.

## Non-Goals

- Do not change eD2K/Kad publish packet shape.
- Do not change existing single-file share/exclude semantics.
- Do not silently unshare already-published files without a reload/rescan flow
  applying the new rules.

## Upstream Signal

aMule issue #604 requests regular-expression based excludes for files such as
`.nfo`, `readme.txt`, and other sidecar content inside large shared trees.

## Acceptance Criteria

- [ ] Rule syntax is documented and invalid rules are rejected safely.
- [ ] Exclude patterns prevent matching discovered files from being shared.
- [ ] Include patterns can narrow sharing to desired file classes.
- [ ] Existing explicit single-file exclusions still work.
- [ ] Tests cover include, exclude, precedence, invalid pattern, and reload
      behavior.
