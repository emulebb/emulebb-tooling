---
id: RUST-BUG-134
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/159
title: Own MiniUPnPc URL allocations across fallible discovery
status: DONE
priority: Major
category: bug
labels: [rust, ffi, upnp, nat, memory, resource-ownership, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-23
source: 2026-10-23 Rust best-practices and safety audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/159. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-134 - Own MiniUPnPc URL allocations across fallible discovery

## Summary

Wrap every successfully initialized MiniUPnPc `UPNPUrls` value in an immediate
RAII owner so every fallible discovery and conversion path frees native URL
buffers exactly once.

## Current State

`gateway_from_url` and `build_gateway_from_devlist` pass zeroed `UPNPUrls`
storage to MiniUPnPc. Successful native calls populate heap-owned URL pointers,
but Rust does not place them under `Drop` ownership until `build_gateway`
returns a `Gateway`. Missing or unusable URL/service fields and other errors in
that interval return early without calling `FreeUPNPUrls`.

MiniUPnPc documents that nonzero `UPNP_GetValidIGD` results initialize the URL
structure and require `FreeUPNPUrls`; `UPNP_GetIGDFromUrl` likewise calls
`GetUPNPUrls` before returning success.

## Why This Matters

Discovery runs against network devices and malformed or unusual IGD metadata is
an expected failure boundary. Repeated retries must not leak native allocations
or make cleanup depend on every future early-return path remembering a manual
free.

## Representative Sites

- `crates/emulebb-miniupnpc/src/lib.rs` `gateway_from_url`.
- `crates/emulebb-miniupnpc/src/lib.rs` `build_gateway_from_devlist`.
- `crates/emulebb-miniupnpc/src/lib.rs` `build_gateway` and `Gateway::drop`.
- Vendored MiniUPnPc `miniupnpc.h` ownership contract.

## Intended Shape

- Introduce a private `OwnedUpnpUrls` or equivalent guard whose `Drop` invokes
  `FreeUPNPUrls` exactly once.
- Establish ownership immediately after a native call reports initialized URLs,
  before parsing or constructing Rust strings.
- Move the guard into `Gateway` only after all fallible validation succeeds.
- Represent the zero/uninitialized state explicitly enough that failure returns
  cannot double-free or free foreign storage.
- Keep raw pointers and release calls inside the smallest FFI ownership module.

## Scope Constraints

- Preserve MiniUPnPc discovery status mapping and eMuleBB NAT backend order.
- Do not paper over malformed gateway data with empty strings; validation should
  remain fallible and cleanup should remain unconditional.
- Do not add `Send` or `Sync` to the native gateway owner without a separate
  upstream thread-safety proof.
- This changes Rust ownership only, not UPnP wire behavior.

## Acceptance Criteria

- [x] Every native call that initializes `UPNPUrls` transfers it immediately to
      one RAII owner.
- [x] Every success, validation error, unexpected-status error, and constructor
      error frees the URLs exactly once.
- [x] Moving URLs into a live `Gateway` prevents the temporary guard from
      releasing them early.
- [x] Null, partial, and malformed gateway metadata remain recoverable errors
      without leaks or double frees.
- [x] No unsafe `Send`/`Sync` implementation is introduced for the gateway.

## Validation

- FFI seam tests with stubbed successful, partial, malformed, and unexpected
  discovery results plus an exact free-call counter.
- Repeated discovery-failure test under a native leak detector where available.
- Existing MiniUPnPc, NAT backend, and daemon startup tests on all supported
  operating systems.

## Resolution

- Wrapped MiniUPnPc URL allocations in an immediate RAII owner across every discovery outcome.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-miniupnpc`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`
