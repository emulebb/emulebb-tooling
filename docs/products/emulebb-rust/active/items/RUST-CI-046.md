---
id: RUST-CI-046
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/305
title: Complete coordinated public presence and release download guidance
status: IN_PROGRESS
priority: Minor
category: ci
labels: []
milestone: post-beta-polish
created: 2026-11-10
source: Operator-approved public-presence refresh
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/305. GitHub Project #3 owns placement; this document owns the durable specification.

# RUST-CI-046 - Complete coordinated public presence and release download guidance

## Outcome

Give users and developers equally clear routes through the organization website,
organization profile, Rust README and canonical product guides. Lead with the
headless eD2K/Kad client, browser console and REST API. Keep the maintained MFC
client accessible through a secondary route, and preserve existing translations.

Replace relative development ETAs with **Active beta**, current CI-gated nightly
testing and **Beta 3** as the next target, without a date. Beta3 publication and
long soak remain on hold; this communication work does not change product gates.

## Scope And Ownership

- Tooling owns canonical downloads/platform, getting-started, API-consumer and
  contributor guides, navigation, shared public-presence contract and generators.
- Rust owns a concise README and contributor entry, plus future grouped release
  download tables generated from actual candidate inventory.
- Existing Pages and organization-profile repositories consume the shared
  contract through their existing deployment workflows. Use managed optional
  topology and OUTPUT-only staging; [Build #30](https://github.com/emulebb/emulebb-build/issues/30)
  owns workspace support.
- Use only the operator-selected proposal-1 donkey assets. Keep the source
  artwork unchanged, readable small icons, safe social-card margins and accessible
  contrast. Do not claim a GitHub social image is uploaded until verified.
- Native resources, package icons and application build identity belong to
  [RUST-CI-047](RUST-CI-047.md), not this content change.

## Evidence Boundaries

Published nightly `0.1.0-beta.2.nightly.20261110.g78f74541` binds product and
workflow source `78f74541ad9985ccc5cfe6987e1c2e3b41134249`. Publication run
[42761216405, attempt 2](https://github.com/emulebb/emulebb-rust/actions/runs/42761216405/attempts/2)
completed 31 jobs and published 81 assets. Bound reports cover native packages,
musl and both OCI variants/CPUs. Independent metadata/hash verification did not
execute the large packages locally. Later main revisions do not inherit that proof.

Android assets are experimental native CLI developer bundles, not APKs or proven
device runtime. Keep configured, built, published, smoke-tested and deep live
evidence distinct. Do not invent minimum OS/RAM requirements, speed comparisons,
current-head 100k-file results, VPN leak safety or long-soak reliability.

## Acceptance

- [ ] Publish four complete, linked user/API/contributor journeys and explain
      every runnable versus supporting asset family and platform requirement.
- [ ] Reconcile first-launch authentication, bootstrap TOML versus SQLite,
      monitored sharing and explicit fresh-profile/rollback guidance with source.
- [ ] Update website, organization profile and Rust README consistently, keeping
      translations, useful inbound anchors and the secondary MFC route.
- [ ] Integrate approved branding with narrowly scoped policy exceptions and
      verify desktop/mobile layouts, keyboard access and table overflow.
- [ ] Generate future release-note tables from actual candidate assets, container
      digests and conditional Android inventory; test without an artificial release.
- [ ] Pass scoped generator/contract/link/locale checks, documentation and roadmap
      checks, strict MkDocs and normal required delivery gates.
- [ ] Merge in dependency order, publish through existing workflows, and verify
      all three public surfaces. Preparation and committed source are not publication.

## Coordination

Shared contracts/generators precede consumers. Keep content, website and native
packaging file reservations separate. Preserve CI045 producer/consumer immutable
source bindings and all release/security gates. The future Indexer/Arr phases,
Android APK/signing and runtime behavior remain outside this slice.
