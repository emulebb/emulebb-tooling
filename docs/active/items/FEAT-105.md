---
id: FEAT-105
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/119
title: Add stopped upload state for shared files
status: OPEN
priority: Minor
category: feature
labels: [shared-files, uploads, priority, release-controls, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-02
source: operator request for a shared file state that prevents uploads without unsharing
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/119. This local document is retained as an engineering spec/evidence record.

# FEAT-105 - Add stopped upload state for shared files

## Summary

Add a per-file state that keeps a complete file in the local Shared Files list
while making it ineligible for upload service, similar to a `Stopped` upload
priority.

This is distinct from unsharing. The file should remain known, hashed, visible
in Shared Files, and easy to re-enable later, but upload admission should not
serve it while the stopped state is active.

## Intended Shape

- Add a visible per-file upload eligibility state, likely as an additional
  upload-priority value such as `Stopped`.
- Make the state reversible from Shared Files and upload-related context menus.
- Persist the state with existing known/shared-file metadata where practical.
- Keep the file visible in Shared Files with clear status text/iconography.
- Ensure upload queue admission, waiting-queue handling, and active-upload
  cleanup respect the stopped state.
- Decide explicitly whether stopped files should be published to ED2K servers,
  Kad, and remote shared-file inventories; prefer not advertising them as
  available sources while they cannot be served.

## Scope Constraints

- Do not delete, unshare, move, rename, or rehash the file when stopped.
- Do not mutate global upload limits or client scoring for unrelated files.
- Do not introduce protocol-incompatible availability claims.
- Do not make stopped files disappear from local Shared Files management UI.
- Do not treat stopped as a download pause state; this applies only to serving
  complete shared files to other peers.
- Do not change default behavior for existing shared files.

## Candidate Implementation Notes

- Reuse the existing upload-priority plumbing if it can safely carry one extra
  non-serving state without confusing normal priority comparisons.
- If current priority enums are too protocol-adjacent, add a separate local
  boolean/state and keep priority unchanged for wire-visible metadata.
- On transition to stopped:
  - remove matching active upload clients from the upload queue
  - remove or skip waiting-queue clients whose requested file is stopped
  - refresh Shared Files, Uploading, and Queue list rows
- On transition back to a serving priority, restore normal publish/admission
  behavior without requiring a full shared-files reload.
- Audit REST and web controller surfaces so the state is visible and reversible
  where shared-file priorities are already exposed.

## Acceptance Criteria

- [ ] A complete shared file can be marked stopped without being unshared.
- [ ] Stopped files remain visible and identifiable in the Shared Files UI.
- [ ] Stopped state persists across restart.
- [ ] Upload admission does not start new uploads for stopped files.
- [ ] Existing active uploads for a file are removed when that file is stopped.
- [ ] Waiting-queue entries for stopped files are handled predictably.
- [ ] ED2K/Kad publishing behavior for stopped files is explicit and does not
      advertise unservable sources by default.
- [ ] Re-enabling the file restores normal upload eligibility.
- [ ] Other shared files continue to upload normally.
- [ ] REST/web shared-file controls expose the state if they expose upload
      priority today.

## Validation

- focused native tests for stopped-file upload eligibility predicates
- focused queue/admission tests for active and waiting clients requesting a
  stopped file
- manual UI smoke for stop, restart persistence, re-enable, and active-upload
  removal
- x64 Debug and Release app builds before implementation commit
