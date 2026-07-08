---
id: TMBB-FEAT-011
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/10
title: Profile import - allowlisted keys + path-rewrite into the install dir
status: OPEN
priority: Minor
category: feature
labels: [migration, profile-import, setup]
milestone: phase-2
created: 2026-06-16
source: suite bundle note 16 (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-011 - Profile import - allowlisted keys + path-rewrite into the install dir

## Summary

Optional import of an existing user profile: copy only an **allowlist of relevant keys** and **rewrite path parameters** to the self-contained install-dir layout. One-time **copy + rewrite**, never a link; the original is untouched.

## Why This Matters

Lets users bring an existing eD2K/qBittorrent library + settings into the self-contained bundle without losing state, keeping the install self-contained.

## Intended Shape

- Per-component allowlist of safe/relevant keys; path keys rewritten to install-dir paths.
- **P2P clients first** (eD2K profile for eMuleBB/rust + qBittorrentBB); rest later.
- **Cross-core mapping** (MFC profile <-> rust) is **TBD**.

## Acceptance Criteria

- [ ] Import copies only allowlisted keys and rewrites paths to the install dir.
- [ ] The original external profile is not modified.
- [ ] P2P clients supported in phase 1.

## Notes

- Cross-core (MFC<->rust) parked as TBD.
