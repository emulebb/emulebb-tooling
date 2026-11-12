---
id: RUST-FEAT-147
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/324
title: Distribute verified Windows daemon packages through Scoop
status: OPEN
priority: Major
category: feature
labels: [rust, distribution-expansion]
milestone: ""
created: 2026-11-12
source: Operator-approved universal-daemon intake and Scoop-first delivery
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/324. Project #3 owns placement; this item owns the engineering contract.

# RUST-FEAT-147 - Distribute verified Windows daemon packages through Scoop

## Outcome And Ownership

Provide the first new package-manager lane for the same universal headless
daemon. Build/packaging owns delivery; product owns the deployment/update
contract; the parent owns integration and any external publication decision.
This intake records accepted scope, not an implemented Scoop channel.

## Required Behavior

- Generate x64/ARM64 manifests from immutable verified release inventory and
  checksums. Include the complete adjacent WebUI and preserve build identity,
  SBOM and GitHub-workflow provenance.
- Preserve current profile resolution. Keep mutable profiles, downloaded data
  and secrets outside versioned installation directories; no second settings
  authority or package-specific TOML model is introduced.
- Use explicitly selected beta versions. Do not silently follow a moving
  nightly, start networking/services on installation, migrate/reset a database
  or erase state during update/uninstall.
- Preserve matching old binary/profile pairs for explicit rollback. An
  incompatible profile fails visibly and needs a fresh profile; do not promise
  unfinished-transfer continuation across incompatible schemas.

## Acceptance And Evidence

- [ ] Both Windows CPUs select the correct immutable ZIP and verify its bytes.
- [ ] Clean install preserves the daemon/WebUI layout and passes authenticated
      REST/WebUI, deterministic transfer, restart/resume and clean shutdown.
- [ ] Compatible update and explicit binary/profile rollback pass; an
      incompatible-profile scenario refuses startup without conversion or reset.
- [ ] Uninstall/reinstall preserve profile, payload and secret ownership, with
      representative paths and permissions covered by retained evidence.
- [ ] Manifest generation/validation and native execution use existing build
      and harness owners, exact source/material identities and required checks.
- [ ] User guidance explains version selection, update, rollback and preserved
      data without overstating support or granting automatic publication.

## Dependencies And Boundaries

[#297](RUST-CI-043.md) owns deployment/config authority; [#298](RUST-CI-044.md)
owns schema boundaries; [#234](RUST-FEAT-063.md) owns semantic profile continuity.
Preparation may precede that future continuity implementation using the accepted
fresh-profile contract. Linux-service implementation is not a prerequisite.
Reliability remains the leading product lane; implementation starts only after
the parent accepts ownership and the shared contract.

This is explicit optional distribution expansion, outside the mandatory core
Client-to-Indexer gate and not a new Beta 3 blocker. Every applicable CI,
native qualification and publication check remains mandatory. Bucket hosting,
community submission, WinGet/installer work, signing and paid infrastructure
are separate decisions. Beta 3 promotion and APK/signing holds remain intact.
