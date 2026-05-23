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

## Acceptance Criteria

- [ ] stale low-progress downloads can be reported without deleting anything
- [ ] deletion mode requires explicit operator opt-in and preserves eD2K links
- [ ] majority-name rename can be enabled globally and overridden per download
- [ ] existing manual rename/delete flows remain unchanged when disabled
