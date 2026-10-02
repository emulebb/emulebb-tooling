---
id: ED2KSRV-CI-001
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/6
title: Build a clean-room differential protocol corpus
status: WONT_DO
priority: Major
category: ci
labels: [testing, protocol, compatibility, clean-room]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-CI-001 - Build a clean-room differential protocol corpus

## Summary

Create a shared, synthetic packet/scenario corpus that compares the Rust server
with the deterministic Go harness and records observable Lugdunum behavior where
needed. The corpus is the compatibility oracle for hardening work.

## Scope Constraints

- Lugdunum is an observed-behavior reference only; decompiled implementation
  code must not be copied or translated.
- Shared harness implementation belongs in `repos/emulebb-build-tests`.
- Adding a candidate lane does not replace `goed2k-server` as the selected
  deterministic server.
- Fixtures contain no private endpoints, user data, or real media titles.

## Acceptance Criteria

- [ ] The corpus covers login, ID assignment, search, offer-files, sources, callbacks, compression, obfuscation, UDP status/search/sources, and malformed input.
- [ ] Rust and Go can execute the same applicable scenarios with machine-readable results.
- [ ] Lugdunum observations record inputs/outputs and provenance without derived implementation code.
- [ ] Differences are classified as defect, intentional extension, unsupported behavior, or oracle limitation.
- [ ] CI runs the safe offline corpus for every server change.

## Notes

This item supplies proof for `ED2KSRV-BUG-001`, `ED2KSRV-BUG-004`, and
`ED2KSRV-FEAT-003`.
