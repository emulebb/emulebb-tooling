---
id: RUST-REF-006
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/9
title: Consolidate Rust NAT and runtime safety internals
status: IN_PROGRESS
priority: Major
category: refactor
labels: [rust, nat, safety, concurrency, maintainability]
milestone: release-0.1.0-beta.1
created: 2026-07-11
source: Operator-approved Rust development hygiene review 2026-07-11
---

# RUST-REF-006 - Consolidate Rust NAT and runtime safety internals

## Summary

Remove obsolete NAT backends now that MiniUPnPc is the sole supported provider,
then harden synchronous runtime state and native-code boundaries without
changing eD2K/Kad behavior.

## Scope

- Remove the deprecated `rupnp` backend, its `ssdp-client` dependency, personal
  Git patches, and the unimplemented `upnp_igd` stub.
- Keep a bounded configuration migration path that accepts MiniUPnPc and rejects
  retired backend identifiers with a clear error.
- Adopt non-poisoning `parking_lot::Mutex` for short synchronous runtime state;
  keep asynchronous locks only where a guard must cross `.await`.
- Fail closed explicitly for security-sensitive state instead of relying on
  mutex poisoning.
- Audit every unsafe boundary, especially `Gateway: Send`, and enable
  `unsafe_op_in_unsafe_fn` plus documented-unsafe-block enforcement.
- Narrow broad dead-code and unused-import suppressions after reference and
  feature-matrix proof.

## Acceptance Criteria

- [x] MiniUPnPc is the only compiled and configurable UPnP provider.
- [x] `rupnp`, `ssdp-client`, and the unimplemented IGD provider are absent from
      source, manifests, and the lockfile.
- [ ] Short synchronous runtime state cannot cascade through mutex poisoning.
- [ ] Security-sensitive failure paths are explicitly fail-closed.
- [ ] Every unsafe block and unsafe implementation has a concrete safety proof.
- [ ] Broad lint suppressions are removed or reduced to justified items.

## Validation

- NAT provider unit tests plus MiniUPnPc discovery/map/release coverage.
- Supported workspace Rust format, Clippy, build, tests, Kad swarm, and VPN leak
  gates.
