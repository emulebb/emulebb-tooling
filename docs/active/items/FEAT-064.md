---
id: FEAT-064
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/20
title: Archived post-0.7.3 MFC future roadmap
status: DEFERRED
priority: Minor
category: feature
labels: [future-roadmap, product-scope, post-0.7.3, planning]
milestone: post-0.7.3
created: 2026-05-16
source: user future-release triage, local mod analysis, community feature scan
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/20. This local document is retained as an engineering spec/evidence record.

# FEAT-064 - Archived post-0.7.3 MFC future roadmap

## Summary

Maintain a curated archived roadmap for eMuleBB MFC after 0.7.3. This item is
the umbrella provenance record for the grouped roadmap and release-line split in
[`FUTURE-ROADMAP`](../FUTURE-ROADMAP.md).

The roadmap is intentionally selective: eMuleBB stays a Windows MFC desktop
client with REST support, and rejected ideas are recorded so they do not drift
back into the backlog accidentally.

The current line decision is that `0.7.x` is the legacy support series with a
frozen public surface after stable `0.7.3`. No MFC `0.8.0` modernization release
is active. Retained MFC `0.8.x` ideas are archive/provenance unless a later
operator decision reopens a narrow lane.

After the 2026-07-12 cleanup, the linked GitHub issue is closed as not planned
and Project #2 is `eMuleBB Roadmap MFC (archive)`. This local document is the
engineering scope/provenance record.

## Archived Lanes

- Connectivity modernization: IPv6 dual-stack and NAT/LowID relief.
- Search and trust clarity: fake-file confidence, Kad/search consistency, and
  local media plausibility evidence.
- UI power-user polish: dark mode, Per-Monitor DPI, category workflow polish,
  and keyboard/menu consistency.
- Security and operations: IP-filter policy, diagnostics, dependency hardening,
  and release-proof automation.
- Narrow anti-leecher review: CShield-style checks only where reasons are
  observable and false-positive risk is low.

## Explicitly Excluded

- Headless, server-only, cross-platform, daemon, or mobile-controller product
  scope.
- New REST feature expansion beyond maintenance and contract drift checks.
- PowerShare, Share Only The Need, release bonus, and similar historical
  releaser-control tracks.
- New broad large-library/performance roadmap scope beyond current active
  hardening.
- Metadata expansion beyond the external MediaInfo DLL release-line behavior.

## Acceptance Criteria

- [x] Active future roadmap exists under `docs/active/`.
- [x] Approved lanes are grouped instead of exploded into many new item files.
- [x] Rejected scope is written down explicitly.
- [ ] Any future promoted lane gets its own reviewed item, GitHub issue,
      project item, and validation plan.

## Validation

- Docs-only updates should pass `git diff --check`.
- Workspace validation should continue to accept the active docs tree.
