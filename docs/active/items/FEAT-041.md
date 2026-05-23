---
id: FEAT-041
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/17
title: Download Inspector automation for stale downloads and majority-name rename
status: OPEN
priority: Minor
category: feature
labels: [downloads, inspector, cleanup, rename, automation, emuleai]
milestone: ~
created: 2026-04-25
source: `analysis\emuleai` v1.4 release notes
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/17. This local document is retained as an engineering spec/evidence record.

## Summary

Track the eMuleAI v1.4 Download Inspector additions as a future product
feature candidate:

- criteria-based handling of old low-progress downloads
- log-only or safe-delete modes based on age and progress rules
- optional backup of deleted downloads' eD2K links
- automatic rename to the majority observed filename, with a global and
  per-download control

## Scope Constraints

This is beyond the current low-drift hardening line. If implemented, it should
be opt-in, auditable, and conservative by default.

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- v1.4 release-note entry for Download Inspector stale-download deletion,
  eD2K-link backup, and majority-name rename:
  [`Release_Notes.txt`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/Release_Notes.txt#L7).
- Part-file rename and per-download state hooks:
  [`PartFile.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/PartFile.cpp#L573).
- Download-list context/UI integration:
  [`DownloadListCtrl.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/DownloadListCtrl.cpp#L3898).
- Preference storage fields:
  [`Preferences.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/Preferences.h#L862).

## eMuleBB Direction

Majority-name following has already been implemented in eMuleBB as a separate
safe feature slice. The remaining eMuleAI idea worth preserving here is the
Download Inspector automation around stale low-progress files.

The eMuleBB version should start as report-only. Any automatic deletion mode
must be disabled by default, must preserve the original eD2K link before
removing a download, and must explain the exact age/progress criteria that
matched. This avoids turning a cleanup helper into a silent data-loss feature.

## Acceptance Criteria

- [ ] stale low-progress downloads can be reported without deleting anything
- [ ] deletion mode requires explicit operator opt-in and preserves eD2K links
- [ ] majority-name rename can be enabled globally and overridden per download
- [ ] existing manual rename/delete flows remain unchanged when disabled
- [ ] report-only mode produces enough evidence to review a candidate delete
      before enabling destructive cleanup
