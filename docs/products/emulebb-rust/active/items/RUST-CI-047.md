---
id: RUST-CI-047
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/306
title: Unify application icons, native metadata and build identity
status: OPEN
priority: Minor
category: ci
labels: []
created: 2026-11-10
source: Operator-approved application identity and packaging polish
---

> GitHub issue [#306](https://github.com/emulebb/emulebb-rust/issues/306) and Project #3 own workflow state. This item owns the durable specification.

# RUST-CI-047 - Unify application icons, native metadata and build identity

## Problem And Scope

Native packages and the embedded WebUI need a consistent application identity.
The reviewed source has a generic AppImage icon, a Debian desktop icon reference
without an installed icon, missing Windows version resources, stale Slint wording
and incomplete desktop metadata. Source inspection does not establish final
package resource contents or platform acceptance.

Use the exact operator-selected proposal-1 ICO/PNG set, preserving approved
hashes and the original artwork. Coordinate with the public content and branding
owner [RUST-CI-046](RUST-CI-046.md); do not regenerate competing marks.

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
