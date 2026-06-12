---
id: FEAT-115
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/154
title: Add per-volume storage policy hints and diagnostics
status: OPEN
priority: Minor
category: feature
labels: [storage, disk-io, diagnostics, preferences, hdd, ssd, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-10
source: operator I/O and filesystem performance review
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/154. This local document is retained as an engineering spec/evidence record.

# FEAT-115 - Add per-volume storage policy hints and diagnostics

## Summary

Record and expose conservative storage hints for the volumes eMuleBB uses for
config, temp, incoming, and shared files. The goal is to make I/O policy
decisions and diagnostics volume-aware without adding risky automatic behavior
that depends on imperfect drive detection.

## Intended Shape

- Build a small storage-profile snapshot for each active volume:
  - role: config, temp, incoming, shared, or mixed
  - filesystem and sparse-file support where available
  - rotational, SSD/NVMe, removable, network, or unknown class where Windows
    reports it reliably
  - free-space floor and current free-space state
  - whether the same volume hosts multiple eMuleBB roles
- Use these hints as conservative inputs for future I/O policy such as
  hash/verify throttling, share-scan throttling, sparse-file guidance, and
  preallocation guidance.
- Prefer diagnostics and operator visibility before any automatic behavior
  change.
- Keep unknown or conflicting Windows storage signals conservative.

## Scope Constraints

- Do not change defaults solely because Windows reports a drive type.
- Do not require administrator privileges or vendor-specific storage APIs.
- Do not treat drive-type detection as security or correctness authority.
- Do not create noisy UI prompts for every storage profile.
- Do not persist machine-specific absolute paths in product docs or release
  evidence.

## Acceptance Criteria

- [ ] eMuleBB can produce a bounded diagnostic snapshot of active storage
      volumes and their roles.
- [ ] Unknown or conflicting drive signals are represented explicitly as
      unknown, not guessed.
- [ ] The snapshot can identify mixed-role volumes, such as temp and incoming
      sharing the same drive.
- [ ] Sparse-file and full-allocation guidance can cite volume facts without
      changing neutral defaults.
- [ ] Future I/O schedulers can consume the snapshot without duplicating volume
      probing code.
- [ ] Diagnostics avoid leaking unnecessary user-private path detail.

## Validation

- focused tests for volume-role grouping from configured paths
- source checks for no mandatory admin-only API dependency
- manual diagnostics review on SSD, HDD, removable, and unknown storage where
  available
- x64 Debug and Release app builds before implementation commit
