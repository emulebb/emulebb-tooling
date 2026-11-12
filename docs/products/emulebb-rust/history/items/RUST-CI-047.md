---
id: RUST-CI-047
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/306
title: Unify application icons, native metadata and build identity
status: DONE
priority: Minor
category: ci
labels: []
milestone: post-beta-polish
created: 2026-11-10
source: Operator-approved application identity and packaging polish
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/306. GitHub Project #3 owns placement; this document owns the durable specification.

# RUST-CI-047 - Unify application icons, native metadata and build identity

## Closure And Evidence

The parent closed [#306](https://github.com/emulebb/emulebb-rust/issues/306#issuecomment-6829948064)
after independently inspecting actual public assets from
[Nightly 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692),
source `080a5dea70186da31dab958757b5b8c0fd883f82`, channel `nightly`, version
`0.1.0-beta.2.nightly.20261112.g080a5dea`.

Both Windows packages passed resource/version/CPU/source/channel, long-path
manifest and approved seven-frame ICO checks. Both GNU CPU packages passed
DEB/AppImage hicolor, desktop/AppStream, root AppImage icon and WebUI PNG checks.
The scoped actual package members/text contained no retired Slint payload or
claims. Four public strict Windows/GNU runtime reports bound those inspected
archives to CLI/REST identity, profile ownership and rendered Windows About.

The public assets, signed subject hashes and independent audit are retained
under `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/nightly-publication-review/43242135692`.
Archive inspection executed no product locally and did not borrow an older
candidate's channel evidence. The original scope below is retained provenance;
its queued wording and unchecked checklist do not describe current workflow.

## Problem And Scope

Native packages and the embedded WebUI need a consistent application identity.
The reviewed source has a generic AppImage icon, a Debian desktop icon reference
without an installed icon, missing Windows version resources, stale Slint wording
and incomplete desktop metadata. Source inspection does not establish final
package resource contents or platform acceptance.

Use the exact operator-selected proposal-1 ICO/PNG set, preserving approved
hashes and the original artwork. Coordinate with the public content and branding
owner [RUST-CI-046](../../active/items/RUST-CI-046.md); do not regenerate competing marks.

## Acceptance

- [ ] Embed the approved multiresolution Windows ICO; install matching Linux
      hicolor icons and WebUI favicon/touch icon assets.
- [ ] Supply accurate Windows product/file descriptions, organization, original
      filename and copyright. Keep numeric version fields valid, full beta/nightly
      identity descriptive, the long-path manifest intact and diagnostics distinct.
- [ ] Install coherent desktop/keywords and validated AppStream metadata with
      real project/license/release links. Remove generic icons and stale Slint
      copy; do not invent screenshots or validation evidence.
- [ ] Align executable properties, `--version`, existing REST application
      identity, WebUI About and package metadata on version, commit, CPU and
      channel. Avoid another app-info endpoint or uncontrolled build timestamps.
- [ ] Preserve checksums, SBOM/provenance and prepared-image exact-source
      contracts. A new image dependency requires actual produced/verified evidence.
- [ ] Inspect native Windows PE resources/manifest and packaged Linux files,
      then complete supported scoped/full gates and independent hosted checks.

## Boundaries

This item is queued; no native resource/package implementation is claimed here.
Keep source changes in independently reserved managed checkouts. Android APK/JNI,
signing, Beta3 publication and long soak remain on hold. Do not broaden support
claims or weaken existing platform/security/publication gates for visual polish.
