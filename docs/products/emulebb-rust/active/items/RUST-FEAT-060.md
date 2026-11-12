---
id: RUST-FEAT-060
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/230
title: Support ChromeOS through Android and Crostini lanes
status: OPEN
priority: Minor
category: feature
labels: [rust, chromeos, android, linux, packaging, portability, distribution-expansion]
milestone: post-beta-polish
created: 2026-11-04
source: operator-approved universal-platform expansion 2026-11-04
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/230. This local document owns the durable engineering contract.

# RUST-FEAT-060 - Support ChromeOS through Android and Crostini lanes

## Distribution Intake Acceptance

This is optional environment expansion with unchanged phase ownership, not an
independent core Client or Beta 3 gate. APK/signing holds remain in force.

- [ ] Reuse existing GNU/musl and Android owners; do not create another daemon,
      protocol fork, Chrome extension or product-state authority.
- [ ] Distinguish Crostini operation from the future Android application lane.
      Experimental Android CLI bundles do not establish APK/device support.
- [ ] Qualify real Chromebook architecture/version/policy, storage exchange,
      ports, sleep/background behavior and lifecycle. Generic Linux/emulator
      evidence or remote browser control is insufficient; no device purchase is
      authorized by intake.

## Summary

Support ChromeOS through its maintained Android application and Linux/Crostini
execution environments. Reuse the Android APK and supported Linux daemon rather
than introducing a ChromeOS protocol fork, Chrome extension, or third product
state model.

## Current State

- ChromeOS is not a supported platform or retained runtime-evidence lane.
- Many Chromebooks can run Android applications, Linux/Crostini, or both, but
  architecture, filesystem exchange, port forwarding, sleep, and background
  behavior differ by device and administrator policy.
- RUST-FEAT-056 owns the APK. Its two Android Rust compile/ELF lanes now pass
  locally and on GitHub, but no APK or Android runtime is qualified yet.
- RUST-FEAT-057 adds native musl archives alongside glibc packages. The portable
  musl artifact can seed Crostini qualification without assuming the guest has
  the glibc version required by a hosted GNU build.
- Neither generic Linux nor Android emulator evidence qualifies a Chromebook.
  ChromeOS ARC and Crostini device evidence remains outstanding.
- No physical test devices are currently available. Keep representative x64
  and ARM64 ChromeOS checks pending until real hardware can be selected.

## Intended Shape

- Prefer the Android APK on devices with a supported Android runtime.
- Support the native Linux daemon inside Crostini where Linux development is
  enabled, using the normal authenticated WebUI in the Chrome browser.
- Publish one ChromeOS support matrix that records device architecture, ChromeOS
  channel/version class, Android runtime availability, and Crostini availability.
- Keep profiles independent when both lanes are installed; do not share a live
  SQLite database between Android and Crostini.

## Scope Constraints

- No Chrome extension or ChromeOS-specific protocol implementation.
- Managed devices that prohibit Android sideloading or Crostini are explicitly
  unsupported rather than bypassed.
- ChromeOS host paths and content-provider paths must cross documented storage
  boundaries; neither runtime may assume transparent access to the other.
- Public support requires real-device evidence, not an Android emulator or
  generic Debian container relabeled as ChromeOS.

## Acceptance Criteria

- [ ] The support matrix defines applicable Android and Crostini lanes for
      representative x64 and ARM64 Chromebooks.
- [ ] The signed APK installs through a documented supported path and proves
      foreground lifecycle, WebUI, storage import/export, local transfer,
      restart, and shutdown on ChromeOS Android.
- [ ] The supported Linux package installs in Crostini and proves profile
      persistence, WebUI access through Chrome, local transfer, restart/resume,
      and shutdown.
- [ ] Sleep/wake, network transition, ChromeOS update, application/container
      restart, and low-storage behavior have bounded evidence for each lane.
- [ ] User-visible import/export between ChromeOS files and the selected runtime
      preserves exact payload size and SHA-256.
- [ ] LAN/public exposure, port forwarding, NAT, and unsupported VPN behavior
      are explicit and never silently weakened by the ChromeOS boundary.
- [ ] The Android, Linux, and existing supported-platform gates remain green.

## Validation

- Persisted device harness selecting Android or Crostini by declared capability.
- Representative x64 and ARM64 Chromebook lifecycle and deterministic local-
  transfer smokes.
- Storage exchange, sleep/wake, network change, update, and restart campaigns.
- Exact APK/Linux artifact and device evidence with private identifiers scrubbed.

## Dependencies

RUST-FEAT-056 owns the Android artifact and device lifecycle. The supported
glibc or musl Linux package owns the Crostini daemon. This item owns only the
ChromeOS integration, support matrix, and device evidence.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_multi-platform.md` section platform-evidence (existing): Windows/Linux are Beta 3 gates. macOS and extended target qualification continue in parallel, with per-target limitations and no stronger support claim than retained runtime evidence.

### Scoped Follow-up Acceptance

- [ ] Required Windows/Linux proof is recorded under the candidate owner.
- [ ] Optional target status distinguishes compile, package and runtime evidence.
