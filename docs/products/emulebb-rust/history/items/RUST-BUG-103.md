---
id: RUST-BUG-103
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/24
title: Classify ED2K server failures before dead-server accounting
status: DONE
priority: Major
category: bug
labels: [rust, ed2k, server, resilience, parity]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against eMule 0.72a and current aMule 3.1
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/24. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-103 - Classify ED2K server failures before dead-server accounting

## Summary

Separate server-attributable connection failures from local DNS, bind,
interface, routing, shutdown, and established-session failures before applying
dead-server retry accounting. The current Rust event surface collapses these
conditions into `ConnectFailed`; with the default dead-server threshold of one,
a local or transient failure can immediately disable a healthy server.

## Current State

- `crates/emulebb-ed2k/src/ed2k_server/server_events.rs` exposes one
  `ConnectFailed` outcome.
- `crates/emulebb-ed2k/src/ed2k_server/loop_runtime.rs` emits that outcome for
  session errors after connection as well as connection/DNS failures.
- `crates/emulebb-core/src/server_api.rs` increments the server's failure count
  and disables it at the configured threshold.
- `crates/emulebb-settings/src/lib.rs` defaults that threshold to one retry.
- Stock eMule increments dead-server state only on its server-dead path in
  `ServerConnect.cpp`. Current aMule likewise distinguishes refusal/server-dead
  evidence from local address, bind, timeout, and other transport conditions.

## Why This Matters

One local network fault can poison the durable server list and reduce discovery
after connectivity returns. The effect is especially severe behind the
fail-closed VPN guard, where loss of the protected interface is expected local
state and must never be attributed to every configured server.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_server\server_events.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_server\loop_runtime.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-core\src\server_api.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-settings\src\lib.rs`
- `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main\srchybrid\ServerConnect.cpp`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\ServerSocket.cpp`

## Intended Shape

- Replace the undifferentiated failure signal with a typed outcome carrying at
  least server refusal/dead, DNS resolution, local bind/interface, network
  timeout/unreachable, established-session disconnect, protocol rejection, and
  intentional shutdown.
- Increment durable dead-server attempts only for evidence attributable to the
  remote endpoint under the documented stock-compatible policy.
- Apply transient retry/backoff to local or ambiguous network failures without
  poisoning the server record.
- Preserve enough structured diagnostics to explain why a server was retried,
  deferred, or disabled.

## Scope Constraints

- VPN-guard refusal and protected-interface loss are local failures and must
  remain fail closed.
- Do not turn every protocol/session error into proof that the server is dead.
- Keep retry pacing bounded and avoid tight reconnect loops.
- If behavior intentionally differs from both stock clients, document and test
  the explicit policy rather than encoding it as an accidental event collapse.

## Acceptance Criteria

- [x] Failure events preserve the phase and cause needed for accounting.
- [x] Remote refusal/server-dead evidence increments the durable failure count
      and can disable a server at threshold one.
- [x] DNS failure, local bind failure, missing VPN interface, local shutdown,
      and an established-session disconnect do not mark a server dead.
- [x] Transient/ambiguous failures receive bounded backoff and remain eligible
      for a later connection attempt.
- [x] Diagnostics expose the classified reason and the resulting accounting
      action.
- [x] Persisted state remains compatible or has an explicit migration.

## Validation

- Table-driven unit tests for every typed failure category and threshold values
  one and greater than one.
- Loop-runtime integration tests covering pre-connect, handshake, established,
  and intentional-stop phases.
- Local stock/current-aMule comparison using refusal, DNS failure, interface
  withdrawal, session reset, and successful reconnect fixtures.

## Notes

This item concerns failure attribution. Server selection heuristics and general
source pacing remain separate concerns.

## Resolution

- Added typed ED2K server failure phase/reason data spanning resolve, socket
  setup, connect, handshake, and established phases. Only a confirmed remote
  connection refusal is dead-server evidence; DNS, local bind/interface,
  timeout/unreachable, protocol rejection, established disconnect, transport,
  and intentional shutdown paths do not poison server health.
- Kept the existing bounded reconnect pacing and cancellation behavior. A
  successful connection still resets the live failure count, while ignored
  failures remain eligible for later selection.
- Added structured `phase`, `reason`, `action`, and `detail` diagnostics at the
  accounting seam. The policy intentionally narrows stock eMule's broad
  Winsock bucket to avoid attributing local/VPN failures to a remote server.
- Preserved the existing server database/settings representation; no
  persistence migration or REST schema change was required.
- Added Windows direct, WSL/OpenVPN, and Docker/Gluetun certification. The VPN
  lanes prove NAT-PMP and MiniUPnPc over `tun0`, fail-closed interface loss,
  unchanged health for every enabled server, zero off-tunnel packets, and
  recovery through the persisted profile.

## Evidence

- Implementation: `emulebb-rust` commit
  `730fe53241a591491fc640430da0771e737b7b7a`.
- Live/certification harness: `emulebb-build-tests` commit
  `3ab65aab9ccb`.
- Full Rust unit/integration/doc-test lane:
  `python -m emule_workspace test rust-unit` (passed).
- Full harness suite: `2134 passed, 6 deselected`.
- Clean Release diagnostics build: zero warnings.
- Native Windows, UPnP off:
  `reports/rust-windows-direct-smoke/20261004T172130Z/report.json` (passed;
  ED2K/Kad connected, NAT disabled with zero mappings, intentional disconnect
  left all 12 enabled servers at `failedCount = 0`).
- Native Windows, forced MiniUPnPc:
  `reports/rust-windows-direct-smoke/20261004T172253Z/report.json` (passed;
  `upnp_miniupnpc`, `upnp_igd`, two mappings, High ID, ED2K/Kad connected, and
  unchanged server health).
- WSL + plain OpenVPN:
  `reports/rust-openvpn-smoke/20261004T175700Z/report.json` (passed; four of
  four strict NAT cases supported, classified `local_bind_interface` ignored,
  all 12 enabled servers unchanged before and after recovery, zero off-tunnel
  packets, clean teardown).
- Docker + Gluetun:
  `reports/rust-gluetun-smoke/20261004T180000Z/report.json` (passed; four of
  four strict NAT cases supported, classified `local_bind_interface` ignored,
  all 11 enabled servers unchanged before and after recovery, zero off-tunnel
  packets, clean teardown).
- Linux DEB SHA-256:
  `50d411c6b232a68d16cac2cb4fd890c7335c90abf8dcd247b813422b4e124b73`.
- OCI archive SHA-256:
  `b7d7a8e834742bc94c60b5129a19e711fec573db7c534d8d6263cce944bbe352`;
  packaged daemon SHA-256:
  `36b964a07d93a7f60f047511b1e0f48fe2926db7a827503eea61196cb5349f45`.
