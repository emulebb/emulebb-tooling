---
id: RUST-BUG-109
workflow: local
title: Close ED2K callback and server state-machine parity gaps
status: IN_PROGRESS
priority: Critical
category: bug
labels: [rust, ed2k, callbacks, servers, protocol-parity]
milestone: rust-v0.1.0-beta.2
created: 2026-10-11
source: 2026-10-11 ED2K static parity audit against community eMule, aMule, ed2k-server, and Lugdunum 17.15
---

# RUST-BUG-109 - Close ED2K callback and server state-machine parity gaps

## Summary

Close seven ED2K interoperability and state-machine gaps found by the 2026-10-11
static audit. Stock/community eMule wire behavior remains authoritative;
maintained eMuleBB MFC improvements are retained where they strengthen callback
admission or preserve upload grants, and the implementation remains Rust-native.

This record is the durable execution tracker for the remediation wave. Each
acceptance item is implemented and validated as a separate granular
`emulebb-rust` commit. The beta line permits internal API, configuration, and
schema breaks when they produce the better long-term design; no compatibility
shim is required by this item.

## Current State

The audit found these unresolved behaviors at the starting revision
`emulebb-rust@8ebb595b6c8515659df3101dfb1225c35d46a3af`:

1. Server, Kad, and direct-UDP callback connect-outs return after HELLO and drop
   the transport instead of becoming a live peer transfer session.
2. UDP `OP_GLOBFOUNDSOURCES` chaining is handled inside the generic source-set
   decoder, which accepts unmarked concatenation and returns one aggregate error
   that discards an already-valid prefix when a later marked segment is malformed.
3. Pending LowID callback intents are unbounded and claimed only by client ID,
   without route provenance, expected-identity validation, expiry, or failure
   cancellation.
4. Server-relayed and Kad-relayed callback connect-outs bypass the shared IP
   filter and peer-ban admission policy.
5. A normal server `OP_REJECT` tears down the authenticated server connection.
6. Malformed TCP search/source responses tear down the server connection rather
   than failing only the affected request.
7. Disconnected LowID upload waiters can use direct UDP callback only; the
   maintained MFC shared-server callback lane is absent.

## Why This Matters

The first four defects affect advertised ED2K connectivity or public-network
input handling and block a trustworthy beta callback path. The remaining three
discard useful authenticated state or reachable upload peers in ways that
diverge from community eMule/aMule behavior.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/firewall_helper.rs`
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs`
- `crates/emulebb-ed2k/src/ed2k_transfer/callback.rs`
- `crates/emulebb-ed2k/src/ed2k_server/result_decoder.rs`
- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs`
- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs`
- `crates/emulebb-ed2k/src/ed2k_tcp/upload_promote.rs`
- `crates/emulebb-core/src/lib.rs`
- `crates/emulebb-core/src/kad_callback_initiator.rs`

## Intended Shape

- One peer-session owner handles accepted sockets, direct outbound downloads,
  and callback-established outbound sockets after transport negotiation.
- Callback authorization is a shared admission boundary, not duplicated or
  omitted per callback route.
- Callback correlation uses an expiring route-scoped ticket and verifies the
  strongest available peer identity before consuming pending work.
- UDP chained-result decoding explicitly requires embedded protocol/opcode
  markers and preserves a valid prefix when a later segment is malformed.
- Server command failures have request-local outcomes; only connection-fatal
  framing or transport failures end the authenticated server session.
- Upload promotion retains enough peer provenance to select direct TCP, direct
  UDP callback, shared-server callback, or an explicit unreachable result.

## Scope Constraints

- Keep the six approved/deferred entries in `policy/rust-client-omissions.toml`
  unchanged; this item does not revive SX1, preview, chat, or IPv6 support.
- Do not add legacy aliases or temporary compatibility layers for superseded
  internal Rust APIs.
- Keep public-network parsing bounded and avoid holding callback or queue locks
  across network I/O.
- Do not add live/soak/profile launch logic; any later live proof must use the
  persisted harness in `emulebb-build-tests`.
- Preserve one coherent behavior change per implementation commit, including
  its focused regression tests.

## Acceptance Criteria

- [x] Callback connect-outs transfer ownership to a live peer session and can
      serve a file request after HELLO on server, Kad, and direct-UDP routes.
- [x] Chained UDP `OP_GLOBFOUNDSOURCES` replies require validated `E3 9B`
      separators, retain valid prefix sets after a malformed later segment, and
      have Lugdunum-shaped tests.
- [ ] Callback tickets are route-scoped, identity-checked, expiring, and
      cancelled on known send/reject failure without losing unconsumed A4AF work.
- [ ] Every callback connect-out applies shared IP-filter and peer-ban admission
      before opening a socket.
- [ ] `OP_REJECT` fails or downgrades only the relevant command while preserving
      the authenticated server session.
- [ ] Malformed TCP search/source replies fail only the affected operation and
      preserve the server session.
- [ ] Upload promotion can use a connected shared server for eligible LowID
      waiters and retains the queue grant through callback completion/timeout.
- [ ] Focused tests, formatting, Clippy, policy checks, and the applicable
      workspace test gate pass from committed state.

## Validation

Static comparator evidence is rooted in community eMule `0f867145`, aMule
`6b1d2d0b`, ed2k-server `57c30957`, and the Lugdunum 17.15 decompile.

Callback-session ownership is implemented by these granular `emulebb-rust`
commits:

- `0156cd72` adopts established callback transports in the ordinary peer
  dispatcher and binds `HELLOANSWER` identity/capability state.
- `4eb00568` introduces the bounded listener-owned session supervisor and moves
  the server callback route onto it.
- `718e7d15` moves the direct-UDP callback route onto the supervisor.
- `7ca14320` moves inbound and outbound-buddy Kad callback routes onto the
  supervisor.
- `1ca3debe` removes the obsolete handshake-only public path and converts the
  callback protocol tests to exercise the production supervisor.

Validated from committed code with the focused callback suite (8 passed),
listener suite (24 passed), buddy-link test, direct-callback core tests (3
passed), `cargo check -p emulebb-core --all-targets`, `cargo fmt --all --
--check`, and `git diff --check`. The crate-wide strict Clippy command is
currently blocked by seven pre-existing unrelated
`unfulfilled-lint-expectations` in server/NAT modules; it reported no finding in
the callback-session changes.

UDP source-result framing is implemented by `emulebb-rust@120f0360`.
The generic source-set decoder now leaves all trailing bytes untouched; the UDP
aggregate decoder alone recognizes embedded `E3 9B` continuation markers,
ignores unmarked tails, and retains already-decoded sets when a later marked
segment is malformed. The Lugdunum-shaped regression cases and the complete
result-decoder suite pass (10 tests).

Callback-ticket route identity prerequisites are implemented by two granular
`emulebb-rust` commits. `91ee28dc` retains the mandatory HELLO trailer's server
endpoint and rejects truncated trailers; all 36 HELLO-related tests pass.
`9f5dd7ac` introduces one canonical discovered-source identity: server LowIDs
are scoped by `(server endpoint, client-id)`, Kad LowIDs use their user hash,
and HighIDs remain globally deduplicated by dialable endpoint. Both server and
core aggregation preserve colliding LowIDs from different servers, and the
20-minute callback request gate is server-scoped. The focused aggregation,
source-policy, buddy-reask tests and `cargo check -p emulebb-core --all-targets`
pass.

The bounded callback admission store is implemented by
`emulebb-rust@63e12c01`. Tickets carry a typed server, Kad-buddy, or direct-UDP
route; match a non-zero HELLO user hash before any route fallback; scope
hashless server LowIDs by `(server endpoint, client-id)`; merge bounded A4AF
work; expire without eviction; and use linear dispatch permits plus
generation-checked leases so send cancellation cannot invalidate a fast
inbound claim. Reserved-versus-armed state survives claim release and lease
expiry, including a callback which arrives before the dispatch caller records
send success. All 15 focused ticket-store tests,
`cargo check -p emulebb-core --all-targets`, formatting, and whitespace checks
pass. Listener claim adoption, per-route reservation/cancellation, and explicit
return of unconsumed A4AF work remain in progress.

## Notes

Implementation order follows dependency pressure: establish callback session
ownership first, then chained UDP decoding, callback tickets, shared admission,
recoverable server failures, and shared-server upload promotion. If a later
slice reveals that two findings require one atomic abstraction change, retain
separate behavioral commits on top of the shared refactor rather than combining
unrelated protocol outcomes.
