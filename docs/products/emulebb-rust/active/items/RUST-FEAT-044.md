---
id: RUST-FEAT-044
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/87
title: Implement follow-majority filename selection for downloads
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, download, filename, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K download-completeness audit 2026-10-12 vs community-0.72, emulebb-mfc
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/87. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-044 - Implement follow-majority filename selection for downloads

## Summary

Add the MFC follow-majority filename behavior: while a download is incomplete,
tally the file names reported by live sources and auto-rename the transfer to
the name that clears a configured minimum vote count and required percentage.
Rust currently keeps a single `display_name` and reconciles only the last
peer-reported name.

## Current State

- Rust: `OP_REQFILENAMEANSWER` reconciles the peer name into the single job
  `display_name` via `reconcile_job_metadata`
  (`crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs:175`), which overwrites
  the existing name (trim + non-empty) with no consensus
  (`ed2k_tcp/download/session.rs:740-750`).
- The transfer model stores one name: `Ed2kTransferJob.display_name`
  (`model.rs:20`), `Ed2kResumeManifest.display_name` (`model.rs:399`).

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `PartFile.cpp:6276-6304` `GetMajoritySourceFileName` collects live
  `cur_src->GetClientFilename()` names and runs `SelectMajorityName` with
  `GetFollowMajorityFilenameMinimumVotes()` and
  `GetFollowMajorityFilenameRequiredPercent()`.
- `PartFile.cpp:6305-6345` `ApplyFollowMajorityFilename` renames via
  `SetFileName(selection.Name, true)` and `SavePartFile()`, skipping
  `PS_COMPLETE` / `PS_COMPLETING`.
- `PartFile.cpp:6348` `SetFollowMajorityFilename`, `:6371`
  `DisableFollowMajorityFilenameForManualRename`.
- `PartFile.h:168-170,450,513` - per-file flag and entry points.
- Persisted as the `BBFollowMajorityFilename` tag in part.met
  (`PartFile.cpp:132,1488,1836`); default from
  `GetFollowMajorityFilenameForNewDownloads()` (`PartFile.cpp:956`).

## Why This Matters

Conflicting source names are common on ED2K; the majority name is usually the
correct one. Rust currently lets the last source to answer win, so a single
mislabelled source can rename the download.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/model.rs` - single `display_name`
- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs` -
  `reconcile_job_metadata`
- `crates/emulebb-ed2k/src/ed2k_tcp/download/session.rs` -
  `OP_REQFILENAMEANSWER` arm
- `workspaces/workspace/app/emulebb-main/srchybrid/PartFile.cpp` -
  `GetMajoritySourceFileName`, `ApplyFollowMajorityFilename`

## Intended Shape

- Keep per-source name observations (see RUST-FEAT-045).
- Select the majority name with configurable minimum votes and required
  percentage; rename only when the selected name differs from the current one
  and the transfer is neither complete nor completing.
- Disable the behavior on a manual operator rename, mirroring
  `DisableFollowMajorityFilenameForManualRename`.
- Persist the enabled flag per transfer (manifest), not globally.

## Scope Constraints

- No wire change: this is local naming policy over existing source-name data.
- Do not rename completed deliveries.
- Reuse the RUST-FEAT-046 normalized names for voting so mojibake variants
  collapse to the same identity.

## Acceptance Criteria

- [ ] A majority name above the configured threshold renames an incomplete
      transfer and is persisted.
- [ ] A manual rename disables further automatic renames for that transfer.
- [ ] Complete and completing transfers are never renamed.
- [ ] The minimum-votes and required-percent knobs are config-driven and
      tested.

## Validation

- Unit tests for the vote selector (ties, thresholds, empty/valid-name
  filtering).
- A session/state-machine test feeding several source names and asserting the
  selected majority name is adopted.

## Notes

Depends on RUST-FEAT-045 (per-source name observations) and composes with
RUST-FEAT-046 (intake normalization).
