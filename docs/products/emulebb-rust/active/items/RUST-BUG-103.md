---
id: RUST-BUG-103
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/24
title: Classify ED2K server failures before dead-server accounting
status: OPEN
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

- [ ] Failure events preserve the phase and cause needed for accounting.
- [ ] Remote refusal/server-dead evidence increments the durable failure count
      and can disable a server at threshold one.
- [ ] DNS failure, local bind failure, missing VPN interface, local shutdown,
      and an established-session disconnect do not mark a server dead.
- [ ] Transient/ambiguous failures receive bounded backoff and remain eligible
      for a later connection attempt.
- [ ] Diagnostics expose the classified reason and the resulting accounting
      action.
- [ ] Persisted state remains compatible or has an explicit migration.

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
