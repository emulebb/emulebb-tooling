---
id: RUST-BUG-200
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/400
title: Preserve strict P2P interface identity through socket binding
status: OPEN
priority: Major
category: bug
labels: [rust, bug, parallel-non-gating]
milestone: post-beta-polish
created: 2026-11-27
source: Cross-platform stabilization review of Rust main 045d9a1d
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/400. This local document owns the durable engineering specification and evidence.

# RUST-BUG-200 - Preserve strict P2P interface identity through socket binding

## Summary

Carry the interface selected by a strict P2P configuration through TCP and UDP
socket setup. A named adapter and another adapter can share one IPv4 address.
The current code can then look up and pin the other adapter's index.

## Current State

On main `045d9a1d`, `resolve_p2p_bind_interface_ip` returns the address from
the named interface. `EgressBinding` carries the address and route mode.
`resolve_bind_if_index` chooses the first matching IPv4 address from a fresh
inventory. VPN Guard confirms address membership on the selected interface
independently of that socket lookup. This defect is established by source
inspection. Off-route traffic has yet to be observed.
[Interface selection](https://github.com/emulebb/emulebb-rust/blob/045d9a1d5d176132eb6eeea5add2b0bb50c686ab/crates/emulebb-daemon/src/bind_config.rs#L116) · [Socket index resolution](https://github.com/emulebb/emulebb-rust/blob/045d9a1d5d176132eb6eeea5add2b0bb50c686ab/crates/emulebb-ed2k/src/networking.rs#L240) · [VPN Guard](https://github.com/emulebb/emulebb-rust/blob/045d9a1d5d176132eb6eeea5add2b0bb50c686ab/crates/emulebb-core/src/vpn_guard.rs#L139)

## Acceptance Criteria

- [ ] Preserve the selected interface identity through TCP and UDP socket
      creation. Reversing an inventory with two instances of the same address
      leaves the selected interface unchanged.
- [ ] Reject ambiguous strict IP-only selections before emitting traffic.
      When the selected interface disappears, reacquire the configured
      interface explicitly before resuming.
- [ ] Observe traffic on the selected interface with a competing route present.
      With the selected interface withdrawn, verify zero off-route packets.
      Verify automatic direct routing separately.

## Validation

Use synthetic network inventories first. Exercise each native socket backend
before claiming platform support. [Android and Fire OS](RUST-FEAT-056.md) owns
legacy Android kernel capability evidence. [Native musl](https://github.com/emulebb/emulebb-rust/issues/227)
owns package-level runtime proof.
