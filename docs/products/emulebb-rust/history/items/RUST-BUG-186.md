---
id: RUST-BUG-186
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/328
title: Avoid JVM-dependent TLS verification in Android CLI HTTPS clients
status: DONE
priority: Major
category: bug
labels: [bug, rust, distribution-expansion, parallel-non-gating]
milestone: post-beta-polish
created: 2026-11-12
source: Operator-observed Android Termux startup failure and source-confirmed TLS verifier mismatch
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/328. This local document owns the durable engineering contract and retained evidence.

# RUST-BUG-186 - Avoid JVM-dependent TLS verification in Android CLI HTTPS clients

## Closure And Accepted Emulator Evidence

[PR #329](https://github.com/emulebb/emulebb-rust/pull/329) merged the repair
as Rust `6429b952eac6f19ee9bf084d3a84d5649dfba0c2`. The final local full gate
ran on `b73e16e7497766b6ad5f75a19b28b03aa18d9d79`, whose tree the parent
verified identical to that merge. Do not relabel that local commit as an
actual-main local run. Actual-main CI, CodeQL and optional-platform qualification
passed separately.

The accepted [Android run 43369243640](https://github.com/emulebb/emulebb-build/actions/runs/43369243640)
executed an API 37/x86_64/16 KiB KVM guest. Its source-built daemon was release
mode on the development channel, with version `0.1.0-beta.2` and exact source
`6429b952`. This is not execution of a published nightly Android archive.
The retained acceptance record is
`reports/android-cli-runtime/43369243640/acceptance.json`; its official artifact
`14012363557` has SHA-256
`d798afa103e375067d22365fd5dbcf0c39ed6587538178bd17923c52243a590b`.
The compiled/exported/ADB-verified production ELF has SHA-256
`e10192bd063b14494ea0b44b778bbcd788f4e185af05cfd7ed84f97dc134f68e`.
All six selected causal TLS tests each passed once with zero failures/ignored
tests. Fresh startup from a different shell directory created a private
snake_case EXE-directory profile, rejected unauthenticated REST, accepted the
configured key, reported the exact expected identity and shut down gracefully.

Android's missing default-route inventory was also repaired in this batch.
Two fixed IPv4 UDP connect/local-address lookups send no datagrams and must
agree before their source can map uniquely to the same detected inventory.
Unavailable, disagreeing or ambiguous hints stay empty; explicit binds and VPN
Guard remain unchanged and fail closed. This is a conservative route hint, not
a VPN, reachability or public-network qualification.

The operator chose GitHub emulators for now. The physical Samsung Galaxy S24+
retest and separate Android unavailable-network execution are explicitly
**unproved and deferred to open
[#226 / RUST-FEAT-056](../../active/items/RUST-FEAT-056.md)**. Neither is checked
as passed. The six accepted cases establish unusable-root and TLS error handling,
not a separate Android degraded-network run. Published archive execution,
physical/ARM runtime, APK/JNI/signing, WebUI, transfer/delivery and VPN acceptance
remain outside this bounded fix. This is an explicit acceptance-scope split;
all applicable local and hosted gates for the selected batch passed.
The parent accepted the [published nightly](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.2.nightly.20261113.g6429b952)
from source `6429b952`, produced by
[run 43375379055](https://github.com/emulebb/emulebb-rust/actions/runs/43375379055).
The public-byte and cryptographic receipt is
`reports/nightly-publication-review/43375379055/final-acceptance.json`.
Issue #328 is closed for this bounded repair. The
[explicit #226 follow-up](https://github.com/emulebb/emulebb-rust/issues/226#issuecomment-6846364871)
retains the unproved offline/degraded-network, physical-device, published-archive,
UI, transfer and VPN outcomes.

## Original Confirmed Failure

The experimental native daemon reaches HTTPS discovery seeding and panics in
rustls-platform-verifier 0.7.1 because its Android verifier requires a JVM and
application context absent from a standalone Termux process. Reqwest 0.13.5
selects that verifier by default. Core URL imports construct the same default
client and share the risk.

The operator reported a Samsung Galaxy S24+, source
`a1422a45bb5fb91dc475a8771c36c869ab298774`, nightly
`rust-v0.1.0-beta.2.nightly.20261112.ga1422a45`, schema 68 and failure at
`2026-11-12T20:20:57Z`. Android/One UI and Termux versions and downloaded asset
SHA-256 remain unknown. This establishes neither authenticated REST readiness
nor transfers, routing, VPN safety or supported Android operation.

## Scope And Trust Contract

Repair the native CLI under the existing
[#226 / RUST-FEAT-056](../../active/items/RUST-FEAT-056.md) Android owner. This is a Major
first-launch blocker in optional environment expansion; it does not independently
hold the Windows/Linux core Client gate. Both selected Android ABI compile/ELF
checks remain mandatory. APK/JNI/service/signing and Beta 3 promotion stay held.

Use a small shared, fallible HTTP client setup for discovery bootstrap and core
URL imports. On Android, explicitly select maintained, nonempty packaged Mozilla
roots through reqwest's root-store verifier; desktop platform trust stays
unchanged. The already locked `webpki-root-certs` 1.0.10 provides full DER roots
under CDLA-Permissive-2.0 from the maintained rustls/webpki-roots project and
Mozilla CCADB. Confirm exact source and license during implementation review.

Root updates require a reviewed dependency update and rebuilt bundle. This CLI
strategy does not read Android/Termux user or private roots, `SSL_CERT_FILE`, or
an operator-specific CA path. Unsupported private chains fail with ordinary TLS
errors. A future APK may separately initialize JVM platform trust; this repair
does not implement that design.

Preserve certificate, hostname and validity checks and each caller's timeout,
redirect, response-bound and normal network-failure behavior. Do not use
certificate merging as an assumed replacement for Android platform trust,
accept invalid certificates, downgrade HTTPS, catch panics to conceal the fault,
or remove discovery verification. No new bootstrap configuration is needed.

## Acceptance And Evidence

- [x] Execute a source-bound reproduction on Android; record ABI, runtime and
      artifact SHA-256 rather than treating cross-compilation as execution.
- [x] Prove trusted HTTPS succeeds through the shared setup, while untrusted,
      wrong-host and invalid-validity certificates return ordinary errors.
- [x] Exercise both discovery and core URL-import consumers; prove fresh-profile
      startup reaches authenticated REST readiness without this panic.
- [x] Prove unusable-root cases fail without disabling verification. Packaged
      roots are nonempty and parse successfully in the accepted Android cases.
- [ ] Separate Android unavailable-network execution remains unproved and is
      explicitly deferred to open #226; ordinary TLS errors do not prove it.
- [x] Preserve both ABI compile/ELF checks and applicable desktop regressions.
- [ ] Retest the reported physical phone with a source-bound replacement when
      accessible. This remains unproved and deferred to open #226; no Android
      device was connected to ADB at intake.
- [x] Complete at least two inspections, repair findings and reinspect the
      final source. Keep exact revisions and supported validation receipts.

Persisted Android execution and TLS fixtures belong to the existing harness and
Builder owners. Use controlled endpoints; do not add an unsolicited public
network campaign or inline launch/monitoring scripts. Emulator proof must be
identified separately from physical-device proof. The source-built emulator
proof above is accepted separately from physical-device and archive-specific
runtime proof.
