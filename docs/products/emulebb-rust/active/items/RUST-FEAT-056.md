---
id: RUST-FEAT-056
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/226
title: Deliver supported Android and Fire OS APKs with device harnesses
status: IN_PROGRESS
priority: Major
category: feature
labels: [rust, android, fire-os, mobile, packaging, webui, harness, portability, distribution-expansion]
milestone: post-beta-polish
created: 2026-11-04
source: operator-approved universal-platform expansion 2026-11-04
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/226. This local document owns the durable engineering contract.

# RUST-FEAT-056 - Deliver supported Android and Fire OS APKs with device harnesses

## Distribution Intake Acceptance

This is explicitly optional environment expansion with its existing phase;
unfinished APK/device work does not independently hold the core Client gate.
Every selected nightly Android compile/ELF check remains mandatory.

- [ ] Keep experimental native daemon bundles distinct from the separately
      authorized APK/JNI/foreground-service/signing implementation.
- [ ] Bind both ABI archives, manifests, tool inputs and ELF/compile proofs to
      the actual accepted nightly/source. Never relabel binaries or claim target
      execution from cross-compilation or linked-but-unexecuted tests.
- [ ] Require device/emulator lifecycle, storage, networking and default-route
      evidence before any Android/Fire OS runtime support claim. Remote browser
      control of another host proves no local daemon/device support.

## Summary

Deliver eMuleBB Rust as a signed, installable Android and Fire OS APK backed by
the existing Rust daemon and browser operations console. Add deterministic
emulator and physical-device harnesses that prove installation, foreground
lifecycle, authenticated WebUI operation, managed storage, local transfer,
restart, clean shutdown, and release provenance.

The Android product remains the same headless bounded monolith. Android owns a
minimal application shell and foreground service; it does not introduce a
second client implementation or a native recreation of the desktop UI.

## Authorized Experimental Nightly Slice

The operator selected experimental native daemon bundles for `arm64-v8a` and
`x86_64` as the initial Android nightly deliverable. The operator subsequently
authorized APK/JNI/service/signing implementation on 2026-11-13; publishing developer archives does not
close this APK feature or add a supported Android-platform claim.

Build fresh ELFs with the actual nightly version/channel and immutable source
identity through the pinned non-root NDK recipe. Publish bounded developer
archives, manifests, checksums, SPDX and compile/ELF evidence through the
GitHub-owned nightly pipeline. Do not relabel prior development binaries or
present compile checks as target test execution. Keep runtime/device execution
explicitly unqualified, including completed-file delivery and default-route
inventory on representative devices. The existing Windows/Linux/macOS, musl and OCI proof remains
mandatory; the Beta3 release and long-soak holds remain in effect.

The parent coordinates one workstream with separate Build and Rust checkout
owners. Run complete applicable hooks and hosted qualification under the current
[Delivery Policy](../../../../reference/DELIVERY-POLICY.md); explicit heavy
local proof remains serialized through the shared lock. Preserve inherited
workspace/output/Cargo state rather than restoring obsolete storage assumptions.

Acceptance for this slice is new, source-bound published nightly assets for both
Android ABIs with honest experimental status. Current compile-only CI reports
and source code for a producer are not publication proof. The full APK and
device acceptance criteria below remain open.

## Current State

- The 2026-11-13 operator authorization lifts the APK/signing hold for this
  workstream and selects the lean Android shell contract below. Implementation,
  package qualification and publication remain separate acceptance steps.
- The Android completed-file move accidentally selected the unsupported-target
  stub because Android has a distinct Rust `target_os` from Linux. The
  [source repair](https://github.com/emulebb/emulebb-rust/commit/5774d9ea)
  uses the existing rustix atomic no-replace rename on both Linux and Android,
  preserving collision handling, native file identity and durability barriers.
  There is no check-then-rename or overwrite fallback.
- [Process resource diagnostics](https://github.com/emulebb/emulebb-rust/commit/f5b18975)
  expose daemon resident memory and interval CPU usage through diagnostics,
  status, snapshot and diagnostic bundles, with readable WebUI cards. Native
  counters avoid Android's restricted global process inventory, honor runtime
  page sizes including 16 KiB, and run outside the async executor. CPU 100%
  means one occupied core; unavailable counters are null and displayed as n/a.
  The [OpenAPI contract](../../api/REST-API-OPENAPI.yaml) owns the field semantics.
- The 2026-11-13 source checkpoint passed 1,307 Windows transfer tests, 150 REST
  tests, 35 WebUI unit tests, 17 browser tests, WebUI type/build checks and both
  Android ABI Clippy, diagnostics, workspace test-link, release-link and ELF
  checks. Android evidence is retained under
  `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-android/dd5439c6d32841fe9685328ecacc1ed1/validation.json`
  and records `runtimeExecution: not-run`. These local checks do not execute
  file delivery or resource sampling on Android, qualify a device, or verify a
  newly published archive. Device/emulator storage and runtime proof remain open.
- Experimental native daemon archives for both ABIs were published by
  [nightly run 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692).
  Publication and compile/ELF proof do not establish Android runtime support.
- The reported Samsung Galaxy S24+ Termux launch exposed a JVM-dependent TLS
  panic. The [bounded native CLI repair](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-BUG-186.md)
  now has accepted [actual-source emulator evidence](https://github.com/emulebb/emulebb-build/actions/runs/43369243640):
  API 37/x86_64/16 KiB, source-built release-mode daemon on the development
  channel, six TLS cases, fresh EXE-directory profile, authenticated REST and
  graceful shutdown. This does not execute a published Android archive.
  The physical S24+ retest and separate Android unavailable/degraded-network
  execution are explicitly unproved and remain with this open owner under the
  operator's choice to use GitHub emulators for now. Six TLS cases are not a
  separate unavailable-network run.
- The supported platform contract includes Windows, Linux, and macOS only.
- The workstream now has checksum-pinned SDK/NDK, Java, Gradle, ADB and Android
  CLI inputs, a non-root offline Docker toolchain probe, and Android Rust
  validation shared by local WSL/Docker and required GitHub CI.
- `arm64-v8a` and `x86_64` pass canonical Clippy/diagnostics checks, workspace
  test linking, release executable linking, and ELF CPU/Bionic/16KB audits.
  These archive-specific receipts are compile checks; the separate x86_64
  emulator proof above executed only the six selected TLS cases.
- The Android shell and JNI implementation are committed on the active branch.
  Actual Kotlin compilation against the pinned SDK 37.2 and Android Gradle
  plugin 9.5.1 passed for Rust source `567c253b`; the compiler dependency graph
  exactly matched the reviewed SHA-256 verification metadata. The scoped receipt
  is below `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/android-apk/3724169c771f4d1d9d684d2d92bb6cb2/`.
  APK assembly, signing execution, full application emulator qualification and
  physical-device qualification remain open. Neither Kotlin compilation nor
  the bounded native CLI startup proof completes those steps.
- The daemon exposes its behavior through a reusable library, loopback REST,
  and the browser WebUI. Its `run_hosted` entrypoint accepts application-owned
  readiness and shutdown without installing process signal handlers.
- The selected API 37/x86_64 guest proved the conservative route hint and
  authenticated loopback REST startup. Representative-device routing, P2P
  socket/VPN confinement, storage, background execution, multicast and NAT
  behavior remain unqualified.

## Intended Shape

- Kotlin application sources live in `emulebb-rust/android/`; native lifecycle
  integration lives in the same Rust repository. There is no separate app repo.
- Minimum Android version is 14 (API 34), targeting the pinned current stable
  SDK. Existing native CLI bundle compatibility and gates remain intact.
- A minimal Kotlin application owns one foreground service and invokes the Rust
  daemon through a narrow JNI library boundary.
- The service supplies app-owned profile, database, log, transfer, and WebUI
  paths and exposes the authenticated listener on loopback by default.
- The packaged SPA remains the complete operations surface, opened in the
  system browser. There is no WebView or parallel native transfer/settings UI.
- The shell provides Start/Stop, actual lifecycle status, Open WebUI, REST
  bootstrap settings and a visible API key with Copy and Regenerate controls.
  TOML edits require a stopped service and use Rust's authoritative parser.
  Generate a random first-run key; never pass it in browser URLs or logs.
- Register browsable `ed2k://` file links with Android. Validate a bounded link
  through the canonical Rust parser, retain at most one pending link, and open
  the WebUI with its transfer form prefilled. Receiving a link must not start
  the service or queue a transfer. Preserve the handoff through authentication;
  require explicit Add confirmation and support cancellation and repeat intents.
- A persistent notification exposes running state and a clean stop action.
- A dedicated foreground-service process owns the Rust runtime. Use
  `specialUse` with an explicit continuous eD2K/Kad peer-hosting subtype;
  starting, readiness, shutdown and failure remain observable independently
  of the shell/browser lifecycle. Repeated Start cannot create duplicate runtimes.
- Private app storage owns metadata, TOML, credentials and logs. App-specific
  external storage owns incomplete payloads by default; completed delivery
  defaults to an eMuleBB directory under shared Downloads. The user grants
  all-files access, then uses ordinary filesystem paths through the WebUI.
  Do not add document-provider adapters or import/export copy workflows.
- Guide notification, all-files and battery-optimization permissions explicitly.
  All-files access is required to start. Denied notification visibility or
  battery exemption remains visible without preventing startup. Hold a partial
  wake lock while continuous service operation is enabled and release it on
  every stop/failure path. Permission revocation must preserve existing data.
- An off-by-default boot-resume setting resumes a previously enabled service
  after unlock. Explicit Stop, including REST shutdown, clears desired-running
  state. Force-stop remains authoritative; recover ordinary system termination
  with bounded backoff and expose persistent startup failures.
- Android private preferences own only desired service intent and boot-resume
  policy; TOML/SQLite remain the existing daemon configuration authorities.
- One universal release APK contains `arm64-v8a` and `x86_64`. The same signed
  artifact receives emulator and physical-device qualification.
- Fire OS support must not depend on Google Play Services.

## Distribution Boundary

- The initial supported distribution is a signed APK published with GitHub
  release assets. Google Play, Amazon Appstore, and Android App Bundle delivery
  require separate decisions.
- The operator explicitly selected `MANAGE_EXTERNAL_STORAGE` for the lean
  direct-path shell, superseding the original picker/import/export boundary.
- Optional resume after unlock on reboot is authorized; recovery after Android
  force-stop is not. The operating system remains authoritative.
- Add the universal signed APK to existing nightly qualification/publication
  without weakening existing gates. A dedicated long-lived APK signing key
  comes from GitHub secrets; missing signing input fails publication without
  debug-key fallback. Initial APKs remain experimental pending device proof.
- No 32-bit Android ABI is required.

## Android 14-17 Permission Contract

The operator requested an explicit permission review for every supported
version. The APK targets API 37 and runs on APIs 34, 35, 36 and 37. This source
review is not emulator or physical-device execution evidence.

- All four versions declare normal `INTERNET`, `ACCESS_NETWORK_STATE`,
  `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_SPECIAL_USE`, `WAKE_LOCK` and
  `RECEIVE_BOOT_COMPLETED` permissions for the actual socket, service and boot APIs.
- All four request `POST_NOTIFICATIONS`. Denial does not prevent a foreground
  service, but the shell must show reduced notification visibility. See
  [Android notification permission](https://developer.android.com/develop/ui/views/notifications/notification-permission).
- All four require the user-granted `MANAGE_EXTERNAL_STORAGE` special access
  before starting native shared-path operations. Denial blocks Start and
  revocation stops active operation without deleting data. See
  [all-files access](https://developer.android.com/training/data-storage/manage-all-files).
- All four declare `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` and guide the user
  through the separate exemption setting. Exemption is recommended, not a
  prerequisite to starting. Show `ActivityManager.isBackgroundRestricted()`
  independently: unrestricted battery use and Doze exemption are different
  controls. See [background optimization](https://developer.android.com/topic/performance/background-optimization)
  and [Doze](https://developer.android.com/training/monitoring-device-state/doze-standby).
- Runtime API 37 additionally requires `ACCESS_LOCAL_NETWORK` before Start,
  including native TCP/UDP and SSDP operations. Monitor revocation. APIs 34-36
  must not request that newer runtime permission. See
  [local network permission](https://developer.android.com/privacy-and-security/local-network-permission).
- No legacy storage/media, location, Bluetooth, nearby-Wi-Fi, overlay, exact
  alarm, package enumeration or APK installation permission is needed by the
  current implementation. Active MiniUPnP M-SEARCH receives unicast replies;
  the current PCP/NAT-PMP paths use directed gateway traffic. There is no
  passive multicast group subscription requiring a Wi-Fi multicast lock.
- Android 15 data-sync timeouts do not classify the selected special-use
  service. Android 16 job quotas apply to scheduling APIs, not the hosted Tokio
  runtime, which does not use those APIs. See
  [foreground service changes](https://developer.android.com/develop/background-work/services/fgs/changes).
- Task Manager Stop kills the application without lifecycle callbacks. Own
  daemon process exit history must prevent treating explicit user termination
  as an ordinary recoverable crash; stale exits preceding a later explicit
  Start must not disable that new session. See
  [user-initiated service stopping](https://developer.android.com/develop/background-work/services/fgs/handle-user-stopping).

Qualification covers each API 34-37 separately: notification denial/grant/
revocation; all-files denial/grant/running revocation; Doze with and without
exemption and actual idle-state assertions; boot resume on/off; explicit Stop,
force-stop and Task Manager Stop. API 37 adds local-network denial/grant/
revocation; earlier versions verify absence of that prompt. Restricted battery
mode must never be presented as qualified continuous or boot operation.

The operator authorized physical-phone testing over Wi-Fi on 2026-11-13.
Use an explicitly selected, authenticated ADB connection and preserve the
operator's ADB server and existing application data. Fresh-emulator reset,
uninstall, reboot and permission-revocation scenarios are not the physical-phone
smoke. Admit the installed artifact before use and confine transfer fixtures to
owned synthetic files; account for the daemon's implicit sharing of its incoming
directory before the first service start. Phone execution on one Android API
does not substitute for the full API 34-37 matrix or the 24-hour campaign.

Release signing material is retained in the operator's normal application-data
directory: `%LOCALAPPDATA%/eMuleBB/signing/android` on Windows, or
`~/.local/share/emulebb/signing/android` on Linux. It is outside workspace
cleanup ownership. Preserve its encrypted keystore, private
credentials and public identity together in an operator-controlled backup.
GitHub secrets are not a substitute for retaining the update signing identity.
The operator authorized generation and GitHub secret configuration on
2026-11-13; the retained signing identity has been generated and all four
Android signing secrets are configured. Directory ACL customization is not a
prerequisite; use ordinary per-user storage and the encrypted keystore.

## Compile Foundation Evidence

The 2026-11-09 compile foundation is now part of the merged and published
experimental native-bundle baseline. Its original Build orchestration
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

The operator has reported a Samsung Galaxy S24+ Termux failure; the exact
Android/Termux versions and artifact hash remain unknown, and no Android device
was connected to ADB at the 2026-11-12 intake. Android ARM64, Fire OS and ChromeOS
device qualification remains pending; emulator or compile success must not
satisfy those acceptance criteria.

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
- [ ] Direct shared-storage delivery and sharing preserve exact size and SHA-256;
      interruption, low-space, revoked-access, and collision paths recover.
- [ ] Optional boot resume, explicit Stop, REST shutdown and force-stop preserve
      the selected service intent and never create duplicate daemon ownership.
- [ ] A physical ARM64 screen-off run exceeding 24 hours proves the continuous
      service claim, including Doze and network transitions.
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
4. Shared-storage permissions, direct delivery and interruption recovery.
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
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section android-route-inventory (existing): The original intake found an empty Android default-route inventory. PR #329 repaired it with a conservative Android-only kernel route hint, covered by the narrow guest startup proof above. Representative-device/network acceptance stays open here; APK/signing implementation is separately authorized above.
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
