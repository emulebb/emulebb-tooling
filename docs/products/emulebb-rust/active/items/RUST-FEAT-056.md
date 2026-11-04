---
id: RUST-FEAT-056
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/226
title: Deliver supported Android and Fire OS APKs with device harnesses
status: OPEN
priority: Major
category: feature
labels: [rust, android, fire-os, mobile, packaging, webui, harness, portability]
milestone: post-beta-polish
created: 2026-11-04
source: operator-approved universal-platform expansion 2026-11-04
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/226. This local document owns the durable engineering contract.

# RUST-FEAT-056 - Deliver supported Android and Fire OS APKs with device harnesses

## Summary

Deliver eMuleBB Rust as a signed, installable Android and Fire OS APK backed by
the existing Rust daemon and browser operations console. Add deterministic
emulator and physical-device harnesses that prove installation, foreground
lifecycle, authenticated WebUI operation, managed storage, local transfer,
restart, clean shutdown, and release provenance.

The Android product remains the same headless bounded monolith. Android owns a
minimal application shell and foreground service; it does not introduce a
second client implementation or a native recreation of the desktop UI.

## Current State

- The supported platform contract includes Windows, Linux, and macOS only.
- Build and release orchestration has no Android target, NDK, Gradle, APK,
  signing, ADB, or emulator lane.
- The daemon exposes its behavior through a reusable library, loopback REST,
  and the browser WebUI, but its lifecycle is currently process/signal based.
- Android storage, background execution, route selection, socket binding,
  multicast, NAT, and VPN behavior have not been runtime-proven.

## Intended Shape

- A minimal Kotlin application owns one foreground service and invokes the Rust
  daemon through a narrow JNI library boundary.
- The service supplies app-owned profile, database, log, transfer, and WebUI
  paths and exposes the authenticated listener on loopback by default.
- The packaged SPA remains the complete operations surface, opened in a WebView
  or system browser without parallel Android transfer or settings state.
- A persistent notification exposes running state and a clean stop action.
- App-private storage owns runtime metadata and incomplete transfers. Android
  document flows import payloads into the managed shared library and export
  completed files to a user-selected destination.
- Release APKs support `arm64-v8a`; `x86_64` remains a required emulator lane.
- Fire OS support must not depend on Google Play Services.

## Distribution Boundary

- The initial supported distribution is a signed APK published with GitHub
  release assets. Google Play, Amazon Appstore, and Android App Bundle delivery
  require separate decisions.
- The application must not require unrestricted `MANAGE_EXTERNAL_STORAGE`.
- Automatic launch at boot and recovery after Android force-stop are out of
  scope; the operating system remains authoritative for those states.
- No 32-bit Android ABI is required.

## Networking And Safety Constraints

- Direct routing is the initial supported public-network mode. Mobile carrier
  NAT is not expected to provide inbound HighID reachability.
- Android must never silently reinterpret or weaken VPN Guard. Unsupported
  interface or VPN selections fail closed before public P2P traffic is emitted.
- Wi-Fi UPnP/NAT-PMP must either be runtime-proven or explicitly rejected by
  the Android settings surface; configuration must not appear successful while
  doing nothing.
- Background execution, Doze, network transitions, multicast requirements,
  and process termination receive explicit evidence.

## Acceptance Criteria

- [ ] Pinned Rust, Android SDK, NDK, and Gradle inputs build `arm64-v8a` release
      and `x86_64` emulator artifacts reproducibly.
- [ ] MiniUPnPc, libpcpnatpmp, SQLite, TLS, interface enumeration, and every
      native dependency have explicit Android compile and runtime dispositions.
- [ ] Canonical orchestration produces the signed APK, bundled WebUI, manifest,
      checksums, SBOM, and provenance below the workspace output root.
- [ ] The foreground service starts one Rust runtime with an app-private
      profile and an authenticated loopback WebUI.
- [ ] Notification stop, REST shutdown, application stop, restart, and ordinary
      process termination leave SQLite and transfer state recoverable.
- [ ] Backgrounding the UI does not stop an active transfer while the service
      remains authorized to run.
- [ ] Document import and completed-file export preserve exact size and SHA-256,
      and interruption, low-space, revoked-access, and collision paths recover.
- [ ] An emulator smoke proves install, REST/OpenAPI, WebUI assets, SQLite,
      local transfer, restart/resume, and shutdown.
- [ ] An ARM64 physical-device smoke proves the same lifecycle against a local
      workspace-owned peer.
- [ ] A bounded physical-device Wi-Fi campaign records direct-mode eD2K/Kad
      startup, route selection, network transitions, and teardown.
- [ ] Fire OS installation, foreground lifecycle, WebUI, storage exchange, and
      transfer behavior pass without Google Play Services.
- [ ] Existing Windows, Linux, macOS, container, quality, and supply-chain gates
      remain green.

## Validation

- Android cross-compilation and Android-specific Rust tests.
- Gradle lint and release assembly from pinned inputs.
- Deterministic Python ADB/emulator package smoke with retained provenance.
- ARM64 Android and representative Fire OS physical-device smokes.
- Storage, low-space, restart, update, background, network-transition, and
  unsupported-VPN tests.
- Existing full Rust quality and native release matrices.

## Delivery Slices

1. NDK compile-and-launch spike using an ADB-controlled standalone daemon.
2. Deterministic emulator harness and two-peer local transfer.
3. Foreground-service APK with JNI lifecycle and bundled WebUI.
4. Managed storage import/export and interruption recovery.
5. Android and Fire OS physical-device evidence.
6. Signed release integration and supported-platform policy update.

## Dependencies

`repos/emulebb-rust` owns runtime and application behavior,
`repos/emulebb-build` owns build/signing/release orchestration, and
`repos/emulebb-build-tests` owns the persisted device harness. Coordinate the
storage boundary with RUST-REF-009 rather than adding an Android-only transfer
implementation.
