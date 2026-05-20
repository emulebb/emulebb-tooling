---
id: FEAT-064
title: Curated post-0.7.3 future release roadmap
status: OPEN
priority: Minor
category: feature
labels: [future-roadmap, product-scope, post-beta-0.7.3, planning]
milestone: post-beta-0.7.3
created: 2026-05-16
source: user future-release triage, local mod analysis, community feature scan
---

## Summary

Maintain a curated future roadmap for eMule BB after beta `0.7.3`. This item is
the umbrella tracking record for the grouped roadmap in
[`FUTURE-ROADMAP`](../FUTURE-ROADMAP.md).

The roadmap is intentionally selective: eMule BB stays a Windows MFC desktop
client with REST support, and rejected ideas are recorded so they do not drift
back into the backlog accidentally.

After GitHub migration, this local document is the engineering scope record.
Workflow state for the umbrella and promoted slices is tracked in GitHub issues
and the public `eMule BB Roadmap` org project.

## Approved Lanes

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
