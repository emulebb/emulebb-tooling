---
id: FEAT-088
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/78
title: Keep completed upload rows visible briefly
status: OPEN
priority: Minor
category: feature
labels: [ui, transfers, uploads, preferences, polish]
milestone: post-0.7.3
created: 2026-05-25
source: operator request to keep completed uploads visible for a configurable number of seconds
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/78. This local document is retained as an engineering spec/evidence record.

## Summary

Keep recently completed uploads visible in the Uploading list for a short,
configurable retention window so users can see that a transfer finished instead
of having the row disappear immediately.

The implementation should be UI-only. Upload queue removal, socket throttler
removal, slot accounting, Web/API active-upload state, and scheduling behavior
must remain immediate and stock-compatible.

## Intended Shape

When an upload leaves the active upload queue because it completed normally:

- capture a lightweight snapshot of the row fields needed for display
- replace or retain the list row as a completed-upload snapshot
- show the status as `Completed` or equivalent localized text
- keep the row visible for the configured retention duration
- expire the snapshot from the list during the existing transfer display refresh
  cycle

Default retention should be conservative, for example `30` seconds.

## Configuration

Add a preference for the completed upload row retention duration:

- unit: seconds
- default: `30`
- minimum: `0`, where `0` preserves current immediate-removal behavior
- maximum: bounded enough to avoid stale clutter, for example `300`
- storage: normal preferences persistence, with a clear INI key and preference
  metadata if exposed through REST/preferences schemas

If the first implementation does not expose a visible Preferences UI control,
the backing setting should still be named and clamped consistently so a UI
control can be added later without changing semantics.

## Scope Constraints

- Do not keep completed clients in `CUploadQueue::uploadinglist`.
- Do not keep sockets registered with the upload bandwidth throttler.
- Do not let completed snapshot rows affect active upload counts, slot
  selection, waiting queue ranking, WebServer upload list state, or REST active
  transfer state.
- Do not store raw client pointers in snapshot rows after the client leaves the
  upload lifecycle.
- Do not extend the lifetime of `CUpDownClient` objects solely for display.

## Candidate Implementation Notes

`CUploadListCtrl` currently stores `CUpDownClient*` as list item data and prunes
rows that are no longer live upload clients. This item likely needs a small row
model that can represent either a live client row or a completed-upload
snapshot.

The snapshot should copy only display data that is already visible or needed for
sorting/status, such as user name, file name, session upload bytes, duration,
client software/version, country, and completion timestamp. Avoid dereferencing
the original client after the upload has been removed.

## Acceptance Criteria

- [ ] Completed upload rows remain visible for the configured number of
      seconds, with `30` seconds as the default.
- [ ] Setting the duration to `0` restores current immediate-removal behavior.
- [ ] Completed rows display a clear completed status and then expire without
      user action.
- [ ] Queue scheduling, upload slot counts, throttler membership, WebServer
      active upload state, and REST active upload state do not treat completed
      snapshot rows as live uploads.
- [ ] Snapshot rows do not retain or dereference stale `CUpDownClient` pointers.
- [ ] A focused seam or unit test covers duration clamping and expiry behavior.
