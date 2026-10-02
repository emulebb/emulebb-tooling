---
id: RUST-FEAT-037
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/22
title: Capability-aware PCP, NAT-PMP, and MiniUPnPc traversal
status: DONE
priority: Major
category: feature
labels: [rust, nat, pcp, nat-pmp, upnp, vpn, packaging]
milestone: post-beta-polish
created: 2026-10-03
source: Operator-approved NAT traversal plan after issue 19 live investigation
---

# RUST-FEAT-037 - Capability-aware PCP, NAT-PMP, and MiniUPnPc traversal

## Summary

Replace the Rust-only SSDP/SOAP implementation with a capability-aware native
stack shared through managed forks. Rust tries route-filtered PCP v2, PCP v1,
and NAT-PMP v0 through `emulebb-libpcpnatpmp`, then falls back to the updated
`emulebb-miniupnp` fork. The MFC runtime and preference order remain unchanged.

GitHub owns workflow status for this item. This document remains the durable
scope, constraints, and validation record.

## Product Contract

- An empty backend order resolves to `pcp_natpmp`, then `upnp_miniupnpc`.
- Automatic PCP discovery follows the selected IPv4 route and source address.
- An optional explicit PCP server accepts an IPv4 address only; PCP/NAT-PMP
  stays on the protocol-defined UDP port 5351.
- Runtime status identifies negotiated `pcp_v2`, `pcp_v1`, `nat_pmp_v0`, or
  `upnp_igd` protocol state.
- Required mapping failures roll back the provider attempt. Preferred mapping
  failures retain required mappings and remain visible as diagnostics.
- Startup, background renewals, and operator REST refreshes serialize through
  one reconcile boundary. Startup performs exactly one initial reconcile.
- A network without PCP/NAT-PMP is a supported capability result. Automatic
  mode must continue to MiniUPnPc; if neither service exists, bounded failure
  must remain truthful and leave no partial mapping state.

## Scope

- Update and pin the shared MiniUPnP fork used by Rust and MFC builds.
- Extend the shared libpcpnatpmp fork with route-aware discovery, explicit
  server selection, negotiated-protocol reporting, and safe flow cleanup.
- Add Rust `-sys` and safe wrapper crates, with native Windows, Linux, and macOS
  build integration.
- Remove the Rust in-tree SSDP/SOAP `upnp_igd` provider and its HTTP/XML
  dependency stack.
- Keep MFC source, preferences, provider order, and runtime behavior unchanged.
- Keep REST, settings metadata, OpenAPI, WebUI, diagnostics, CI, release pins,
  SBOM, and source provenance aligned with the new stack.
- Repair persisted Rust backend orders containing the removed `upnp_igd`
  identifier to the new default once; reject new submissions containing it.

## Acceptance Criteria

- [x] Deterministic native tests prove successful PCP v2 and NAT-PMP v0
      mapping/release flows.
- [x] Default order, isolated-provider order, required/preferred mapping
      semantics, fallback, and serialized initial reconcile have Rust tests.
- [x] `upnp_igd`, `reqwest`, and `roxmltree` are absent from the active Rust NAT
      implementation and the `emulebb-ed2k` dependency graph.
- [x] REST/OpenAPI/WebUI expose the optional PCP server and negotiated protocol.
- [x] CI and release workflows pin both shared native forks.
- [x] Native package SBOM and source provenance include both forks.
- [x] Windows-native direct live matrix completes with protocol obfuscation
      disabled.
- [x] WSL + Docker + plain OpenVPN live matrix completes with protocol
      obfuscation disabled.
- [x] Docker + Gluetun live matrix completes with protocol obfuscation disabled.
- [x] Every live lane records default automatic, PCP-only, MiniUPnPc-only, and
      forced-PCP-failure fallback cases as supported or cleanly unsupported.

## Validation

- `python -m emule_workspace test rust-unit`
- `python tools/rust_quality_gate.py quick`
- `python -m pytest tests/test_release.py -q`
- `python -m pytest tests/python/test_nat_live_matrix.py tests/python/test_rust_openvpn_smoke.py tests/python/test_rust_gluetun_smoke.py tests/python/test_rust_linux_direct_smoke.py -q`
- Windows direct, plain OpenVPN, and Gluetun persisted live harness reports.

## Evidence

- The shared libpcpnatpmp fork records route-aware discovery and ownership
  cleanup in commits `a71e7b7`, `2b8649a`, and `a6e787f`.
- The updated shared MiniUPnP fork is pinned at merge commit `4e7a109`.
- The full Rust Release test suite and quick Rust quality gate pass locally.
- The Windows-native matrix passed at
  `reports/rust-windows-direct-smoke/20261002T230010Z/report.json`: automatic,
  MiniUPnPc-only, and forced PCP failure mapped both ports through MiniUPnPc;
  PCP-only was cleanly unsupported. Protocol obfuscation was disabled and the
  daemon shut down gracefully.
- The WSL Docker + plain OpenVPN matrix passed at
  `reports/rust-openvpn-proof/20261002T225200Z-nat-matrix.json`: all four cases
  were cleanly unsupported by the VPN service, automatic/fallback errors named
  both attempted providers, protocol obfuscation was disabled, and isolated
  Compose teardown was clean.
- The Docker + Gluetun matrix passed at
  `reports/rust-gluetun-proof/20261002T230000Z-nat-matrix.json`: all four cases
  were cleanly unsupported, automatic/fallback errors named both providers,
  protocol obfuscation was disabled, the tunnel-down leak count was zero, and
  isolated Compose teardown was clean.
- Windows and Linux beta.2 packages were built from clean provenance. The Linux
  WSL translation record is
  `reports/rust-linux-package-launch/20261002T224829Z/wsl-boundary.json`; the
  local amd64 Docker test image matched executable SHA-256
  `3b565a5c57a6e7a5908eb41b79f7982e833643eac472b80df882a2df3389df1a`.
