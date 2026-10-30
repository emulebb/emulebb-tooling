---
id: RUST-FEAT-052
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/183
title: Promote eMuleBB Rust beta across public surfaces
status: DONE
priority: Minor
category: feature
labels: [rust, beta, documentation, website, releases, public-presence]
milestone: rust-v0.1.0-beta.3
created: 2026-10-29
source: operator-approved public positioning plan 2026-10-29
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/183. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-052 - Promote eMuleBB Rust beta across public surfaces

## Summary

Make eMuleBB Rust the leading product on the organization profile, root site,
repository landing page, and canonical documentation. Present it as an active
beta with public `0.1.0-beta.2` and Beta 3 in development, with nightly builds
as the primary testing channel and the formal Beta 2 release as the secondary
download.

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
  product page English-only. Only the organization homepage and FAQ are
  localized.

## Scope

- Extend the public-presence contract with one required Rust product record and
  use it in generated public surfaces.
- Rebalance the canonical tooling docs, generated organization profile, root
  website, and Rust repository landing page toward the Rust beta.
- Update only future nightly release-note generation; do not rewrite already
  published release descriptions.
- Update GitHub organization and repository metadata and remove only the
  `experimental` repository topic.

## Scope Constraints

- Do not change WebUI product behavior or copy.
- Do not change product versions or select a Beta 3 candidate.
- Do not add screenshots or localized Rust product pages.
- Do not weaken the compatibility-unstable beta policy for API, configuration,
  or persistence.

## Acceptance Criteria

- [x] Principal public surfaces identify eMuleBB Rust as Active beta, public
      `0.1.0-beta.2`, working toward Beta 3.
- [x] Principal Rust surfaces include the exact live-network evidence statement.
- [x] Nightlies are the primary CTA and the formal Beta 2 release is secondary.
- [x] `/rust/` is English-only, canonical, present once in the sitemap, and
      publishes Rust `SoftwareApplication` structured data.
- [x] Localized homepage and FAQ source strings do not describe Rust as
      experimental or exploratory.
- [x] The MFC client remains a visible secondary Windows maintenance lane.
- [x] Existing published release descriptions and WebUI content are unchanged.
- [x] Generated profile, site, docs, taxonomy, and focused Rust release tests
      pass.

## Validation

- Public-presence contract validation and deterministic profile render/check.
- Tooling taxonomy, documentation structure, and MkDocs publication checks.
- Root-site render/check, static-site validation, canonical/sitemap/schema
  checks, and representative locale inspection.
- Focused Rust nightly-release tests and repository policy checks.
- GitHub metadata readback after the authorized remote updates.

## Notes

Implemented and locally validated 2026-10-30. Validation passed for the public-
presence contract and generated organization profile, tooling taxonomy and
structure checks, strict MkDocs publication, root-site generation and static
validation, and all 16 focused Rust nightly-release tests. The issue is in the
`rust-v0.1.0-beta.3` milestone and the organization Roadmap project.
