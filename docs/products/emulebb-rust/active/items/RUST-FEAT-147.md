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

## Accepted Implementation Boundary

The parent accepted [the currently implemented deployment contract](https://github.com/emulebb/emulebb-rust/issues/324#issuecomment-6830047076)
at Rust `080a5dea70186da31dab958757b5b8c0fd883f82`, schema 68. Implementation
starts after #327; this item remains OPEN until its own code and native
qualification pass. The first deliverable is a reviewable generator/manifest
and executable lifecycle evidence, not external bucket publication.

- Use explicitly selected immutable inventory and SHA-256 values; the verified
  [Nightly 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692)
  supplies x64/ARM64 Windows ZIP evidence. Preserve the complete adjacent WebUI,
  binary identity, SBOM and workflow provenance. Do not track a moving nightly.
- Keep existing profile selection: `--profile` overrides the Windows default
  `%LOCALAPPDATA%/emulebb-rust`. Never redirect that default into a versioned
  Scoop installation, working directory or package-managed `persist` folder.
- Package scripts add no settings/profile authority, rewrite no bootstrap key
  or default, and automatically start no daemon or service. The complete
  #297 target remains unaccepted; its proposed defaults are not prerequisites
  for packaging the current daemon.
- Install/update/uninstall do not create, convert, reset or delete operator
  databases, profiles, secrets or payloads. Compatible updates and explicit
  rollback preserve matching binary/profile pairs; incompatible startup fails
  visibly without promising unfinished-transfer carry-forward.
- Reuse Builder/Harness qualification on disposable profiles. ARM64 runtime
  acceptance requires real native execution, not a manifest or cross-build.

External bucket hosting/community submission, signing, installers/WinGet,
service enablement and paid infrastructure remain separate decisions.

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
- Use explicitly selected immutable release versions. Do not silently follow a moving
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
