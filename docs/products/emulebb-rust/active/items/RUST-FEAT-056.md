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
- The workstream now has checksum-pinned SDK/NDK, Java, Gradle, ADB and Android
  CLI inputs, a non-root offline Docker toolchain probe, and Android Rust
  validation shared by local WSL/Docker and required GitHub CI.
- `arm64-v8a` and `x86_64` pass canonical Clippy/diagnostics checks, workspace
  test linking, release executable linking, and ELF CPU/Bionic/16KB audits.
  These are compile checks; target unit tests have not been executed.
- APK production, JNI integration, application lifecycle, signing, emulator
  qualification and physical-device qualification remain unfinished.
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
- One universal release APK contains `arm64-v8a` and `x86_64`. The same signed
  artifact receives emulator and physical-device qualification.
- Fire OS support must not depend on Google Play Services.

## Distribution Boundary

- The initial supported distribution is a signed APK published with GitHub
  release assets. Google Play, Amazon Appstore, and Android App Bundle delivery
  require separate decisions.
- The application must not require unrestricted `MANAGE_EXTERNAL_STORAGE`.
- Automatic launch at boot and recovery after Android force-stop are out of
  scope; the operating system remains authoritative for those states.
- No 32-bit Android ABI is required.

## Compile Foundation Evidence

The 2026-11-09 checkpoint is pushed on `chore/local-validation-batches` and has
not been merged or published. Build orchestration
[`bb0e542`](https://github.com/emulebb/emulebb-build/commit/bb0e542152da6d58a28ffd69a5b8b6451e7cbcf4)
owns the reviewed inputs and both local/hosted entrypoints:
`python -m emule_workspace validate-rust-android` locally and
`validate-rust-android-ci` on explicit hosted checkouts. Both retain source
identities and explicitly record `runtimeExecution: not-run`.

Rust [`3ddf47ac`](https://github.com/emulebb/emulebb-rust/commit/3ddf47ac1847760898d759189ffca90c66de4dca)
passed the full local pre-push gate and
[required GitHub CI](https://github.com/emulebb/emulebb-rust/actions/runs/42556994416),
including both Android ABIs on fresh AMD64 runners. Its
[CodeQL run](https://github.com/emulebb/emulebb-rust/actions/runs/42556997395)
also passed. Local compile receipts remain below
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-android`.

Harness [`e99192f`](https://github.com/emulebb/emulebb-build-tests/commit/e99192f92a0dc12f912fa5aa1bce69851e8d0e5a)
adds the universal-APK native-payload audit with 12 passing regression tests.
It checks both ABI payloads, bounded ZIP inventory, 16KB alignment, CRC and
hashes, and delegates ELF validation to the packaging owner. It has not yet
audited a produced eMuleBB APK and does not establish signing or runtime proof.

The local Android target directory contains accumulated debug and incremental
output across builds. Reducing that footprint is follow-up CI hardening; both
fresh hosted compile jobs passed, so this measurement is not a demonstrated
runner-capacity blocker. Keep complete checks when changing build profiles.

Build [`1c70c15`](https://github.com/emulebb/emulebb-build/commit/1c70c15403ccc65ea47d0ac065864a8e127b5644)
adds separately pinned emulator/API-28/current-16KB inputs and the local
`prepare-rust-android-emulator` software probe. Real WSL Docker execution passed
as a non-root user with networking disabled, a read-only root, dropped
capabilities and the exact image content ID. Both installed guest-image
metadata sets passed API/revision/ABI/variant checks. The probe caught and
fixed owner-only modes in the old AOSP archive and now uses the intended
headless emulator mode. Owner changes require the tools-only probe before
push, without implicitly downloading guest images. Receipts below
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/android-emulator` record
`runtimeExecution: not-run`; that tool-only check did not boot guests or qualify
an APK.

The shared guest-boot owner uses native non-root Docker with KVM, no networking,
and a fresh writable run directory. `probe-rust-android-guest --image min` or
`--image current` runs it locally where KVM is available; the GitHub adapter
uses the same owner and harness. This WSL host has no `/dev/kvm`, so software
installation/version/metadata checks run locally and accelerated boots run on
GitHub. Emulator preparation now needs only the emulator, the existing shared
ADB pin and the selected guest image; it no longer prepares compiler inputs.
Public evidence excludes private AVDs and emulator runtime logs and explicitly
records `applicationQualification: not-run`.

Build [`bea48fd`](https://github.com/emulebb/emulebb-build/commit/bea48fd5a083a45d1c542f66bb00aa3ba7dba5f9)
and harness [`0b878d7`](https://github.com/emulebb/emulebb-build-tests/commit/0b878d74a90c64b5ae7c538e9753278912aff6fd)
passed both [hosted KVM guest boots](https://github.com/emulebb/emulebb-build/actions/runs/42575803289):
stable API 28 with 4096-byte pages and stable API 37 with 16384-byte pages,
both native x86_64. The minimum guest exposed an unavailable `getconf PAGE_SIZE`
query; the shared harness now reads the kernel's ELF64 `AT_PAGESZ` entry over
binary-preserving ADB, without publishing auxiliary-vector process addresses.
Local evidence includes the complete harness suite plus 36 focused boot/parser
tests and the offline WSL Docker runtime-tool probe. APK production, signing,
application lifecycle and release integration remain open.

The operator has no physical test devices available. Android ARM64, Fire OS
and ChromeOS device qualification remains pending; emulator or compile success
must not satisfy those acceptance criteria.

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

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_secure-ident.md` section 5 / 7 (existing): Weak stock RSA/SHA1 is an accepted interoperability boundary. Key pinning has a closed owner; native-target build/runtime and cross-client proof have existing owners.
- `emulebb-rust-prompt_audit_findings_reachability.md` section 2.4 / 4.2-3 (existing): ABI verification and native-target compile/runtime proof belong to existing FFI and platform items. Android is parallel and non-gating for Beta 3; do not replace proven C libraries with a narrower pure-Rust fallback to avoid qualification.
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section portable-delivery (existing): The unsupported-platform arm still rejects completed delivery. Android/FreeBSD/other Unix issues already own platform viability. Do not adopt the audit's check-then-rename suggestion: it can race and clobber data.
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section android-route-inventory (existing): Android still receives an empty default-route interface inventory. Its existing support item must define supported route discovery or an honest explicit-bind-only contract; Android APK/signing remains on hold.
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section extended-lanes (existing): The audit's no-musl/no-Android-CI claim is stale: both musl architectures and Android compile/ELF lanes now exist. Keep the owning feature issues open for their remaining runtime/package evidence; cross-compilation is not complete platform certification.

### Scoped Follow-up Acceptance

- [ ] Do not replace on-wire primitives locally.
- [ ] Retain key pin/restart/credit preservation proof.
- [ ] Keep Android evidence non-gating for Beta 3.
- [ ] Mechanical C/Rust layout proof uses exact vendored headers.
- [ ] Keep musl and Android compile proof distinct from runtime/device NAT proof.
- [ ] Choose a platform primitive preserving no-replace and crash/durability guarantees.
- [ ] Prove destination collision and concurrent publication without clobbering.
- [ ] Record unsupported filesystems explicitly rather than silently weakening safety.
- [ ] Prove representative device route discovery or document explicit-bind constraints.
- [ ] Never infer VPN confinement from a missing route inventory.
- [ ] Reuse current lanes and identify missing runtime/device proof only.
- [ ] Track optional platform failures visibly without gating Beta 3.
