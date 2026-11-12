---
id: RUST-BUG-186
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/328
title: Avoid JVM-dependent TLS verification in Android CLI HTTPS clients
status: IN_PROGRESS
priority: Major
category: bug
labels: [bug, rust, distribution-expansion, parallel-non-gating]
milestone: post-beta-polish
created: 2026-11-12
source: Operator-observed Android Termux startup failure and source-confirmed TLS verifier mismatch
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/328. This local document owns the durable engineering contract and retained evidence.

# RUST-BUG-186 - Avoid JVM-dependent TLS verification in Android CLI HTTPS clients

## Confirmed Failure

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
[#226 / RUST-FEAT-056](RUST-FEAT-056.md) Android owner. This is a Major
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

- [ ] Execute a source-bound reproduction on Android; record ABI, runtime and
      artifact SHA-256 rather than treating cross-compilation as execution.
- [ ] Prove trusted HTTPS succeeds through the shared setup, while untrusted,
      wrong-host and invalid-validity certificates return ordinary errors.
- [ ] Exercise both discovery and core URL-import consumers; prove fresh-profile
      startup reaches authenticated REST readiness without this panic.
- [ ] Prove unavailable-network and unusable-root cases fail without disabling
      verification. Packaged roots must be nonempty and parse successfully.
- [ ] Preserve both ABI compile/ELF checks and applicable desktop regressions.
- [ ] Retest the reported physical phone with a source-bound replacement when
      accessible. No Android device was connected to ADB at intake.
- [ ] Complete at least two inspections, repair findings and reinspect the
      final source. Keep exact revisions and supported validation receipts.

Persisted Android execution and TLS fixtures belong to the existing harness and
Builder owners. Use controlled endpoints; do not add an unsolicited public
network campaign or inline launch/monitoring scripts. Emulator proof must be
identified separately from physical-device proof. Until runtime acceptance is
recorded, this remains an unqualified repair rather than a closed bug.
