---
id: RUST-FEAT-054
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/183
title: Prioritize nightly eMuleBB Rust public presence
status: IN_PROGRESS
priority: Minor
category: feature
labels: [rust, beta, documentation, website, releases, public-presence]
milestone: rust-v0.1.0-beta.3
created: 2026-10-29
source: operator-approved nightly-first public positioning plan 2026-10-30
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/183. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-054 - Prioritize nightly eMuleBB Rust public presence

## Summary

Make eMuleBB Rust nightlies the public front-door download and testing path.
Treat Beta 2 as stale, immutable release history rather than a current call to
action. State that Beta 3 is expected after a few more weeks of implementation
and stabilization.

## Product Language

- Use **eMuleBB Rust** as the display name and retain `emulebb-rust` for
  repository and technical identifiers.
- Use the exact evidence statement: **Repeatedly tested on live eD2K/Kad
  networks.**
- Do not advertise the product itself as experimental or exploratory. Preserve
  feature-specific experimental warnings where the feature evidence requires
  them.
- Keep the MFC Windows client visible as a secondary stable maintenance lane.
- Keep eMuleBB Rust, its repository documentation, release notes, and `/rust/`
  product page English-only.
- Freeze localized home and FAQ pages to minimal evergreen copy without
  versions, beta targets, ETAs, or time-sensitive release status.

## Scope

- Keep the public-presence contract's Beta 2 fields as archival metadata while
  removing them from current-facing generators.
- Add the approved Beta 3 directional ETA to the contract.
- Rebalance the canonical tooling docs, generated organization profile, root
  website, and Rust repository landing page toward nightly builds.
- Remove Beta 2 from current CTAs, navigation, summaries, FAQ answers, SEO
  metadata, and Rust structured release data.
- Preserve the existing website layout and professional dark theme.

## Scope Constraints

- Do not change WebUI product behavior or copy.
- Do not change product versions or select a Beta 3 candidate.
- Do not add screenshots or localized Rust product pages.
- Do not weaken the compatibility-unstable beta policy for API, configuration,
  or persistence.

## Acceptance Criteria

- [ ] Nightlies are the first and only current Rust download/testing CTA.
- [ ] Current-facing copy tells users to choose the newest dated nightly from
      GitHub Releases.
- [ ] Beta 2 appears only as archival or technical history.
- [ ] Current English Rust surfaces include the approved Beta 3 directional ETA.
- [ ] Principal Rust surfaces retain the exact live-network evidence statement.
- [ ] `/rust/` stays English-only and removes Beta 2 structured release data.
- [ ] Localized home and FAQ pages contain no versions, beta targets, or ETAs.
- [ ] The existing site layout and professional dark theme remain unchanged.
- [ ] Contract, profile, site, docs, and focused Rust validation pass.

## Validation

- Public-presence contract validation and deterministic profile render/check.
- Tooling taxonomy, documentation structure, and MkDocs publication checks.
- Root-site render/check, static-site validation, canonical/sitemap/schema
  checks, and representative locale inspection.
- Focused Rust nightly-release tests and repository policy checks.
- GitHub metadata readback after the authorized remote updates.

## Notes

Earlier public-presence commits used `RUST-FEAT-052`, but that identifier
already belongs to issue #146. Issue #148 owns `RUST-FEAT-053`. Historical
commit messages are not rewritten; this follow-up and its durable tracking use
`RUST-FEAT-054`.
