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

Close eight ED2K interoperability and state-machine gaps found by the 2026-10-11
static audit and its implementation review. Stock/community eMule wire behavior remains authoritative;
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
8. Kad-relayed `OP_CALLBACK` treats a retained `DhtNode` as proof that Kad is
   running and parses malformed payloads before checking live Kad state, so a
   stopped Kad runtime can still originate a callback or lose a valid peer or
   held-buddy session.

## Why This Matters

The first four defects affect advertised ED2K connectivity or public-network
input handling and block a trustworthy beta callback path. The remaining four
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
- Typed server command failures have request-local outcomes; uncorrelated
  notices do not mutate request state, and only connection-fatal framing or
  transport failures end the authenticated server session.
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
- [x] Callback tickets are route-scoped, identity-checked, expiring, and
      cancelled on known send/reject failure without losing unconsumed A4AF work.
- [x] Every callback connect-out applies shared IP-filter and peer-ban admission
      before opening a socket.
- [x] Kad-relayed `OP_CALLBACK` checks live Kad state before parsing on both
      ingress paths and rechecks before queueing a callback connect-out.
- [x] Null, uncorrelated `OP_REJECT` notices mutate no command state and preserve
      login, pending operations, negotiated capabilities, and the authenticated
      server session; typed replies and per-request deadlines remain authoritative.
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

Unconsumed callback-session work is retained by `emulebb-rust@adbfa489`.
Inbound ownership is represented by an RAII session claim: successful file
outcomes acknowledge only that hash across joined routes, while cancellation,
panic, or an early return synchronously restores the remaining A4AF set for a
fresh bounded dispatch epoch. Active sessions no longer expire on the short
handshake lease; same-hash routes can join one peer session, fallback admission
pins the observed HELLO hash, and both pending and live-session merges enforce
the 256-file bound transactionally. Late send completion has an explicit
`Settled` outcome and stale permits cannot mutate a newer retry generation.
All 29 focused callback-store tests and all 971 `emulebb-ed2k` library tests
pass, along with `cargo check -p emulebb-core --all-targets`, formatting, and
whitespace checks. Strict Clippy still reaches only the seven pre-existing
unrelated `unfulfilled-lint-expectations`. Listener adoption and per-route
reservation/cancellation remain in progress.

Inbound listener adoption is implemented by `emulebb-rust@4f764be7`. After a
validated HELLO response and secure-ident probe are written, the listener
constructs the callback identity from the observed user hash, server-scoped
client ID, mandatory server trailer, IPv4 peer address, and advertised ED2K TCP
port. It adopts matching ticket work through the RAII session claim, acknowledges
only successful per-file outcomes, continues A4AF after completion/NNP/FNF, and
returns the unconsumed tail for a new dispatch after incomplete/queued outcomes
or task failure. The legacy client-ID intent store remains only as an `Ok(None)`
fallback until all three request producers migrate. Wire tests prove server
provenance against a colliding LowID, ticket priority over the legacy queue,
same-socket A4AF continuation, and tail retention after peer close. All 11
callback protocol tests and all 974 `emulebb-ed2k` library tests pass, together
with the core all-targets check, formatting, and whitespace checks; strict
Clippy remains blocked only by the same seven unrelated expectations. Per-route
reservation/cancellation is the remaining callback-ticket integration work.

Classic server callback production is migrated to route-scoped tickets by
`emulebb-rust@b857bec2`. Both connected-server `OP_CALLBACKREQUEST` and
cross-server UDP `OP_GLOBCALLBACKREQ` reserve admission before wire dispatch;
A4AF joins share one server-local peer ticket and one peer-scoped 20-minute
retry gate. A linear dispatch guard keeps queued or in-progress work claimable
and non-reapable, shares the ticket's exact absolute deadline with the
background server worker, conservatively arms admission on task abort or
ambiguous delivery, and rolls back only proven-not-sent outcomes. Successful
or ambiguous delivery restarts the bounded callback window and cooldown from
settlement, while failed delivery cancels the exact ticket and cooldown claim.
The server producer no longer writes the legacy client-ID intent queue.

Validation from committed code passes all 31 callback-store tests, all 7
background callback-dispatch classification tests, all 10 core source/cooldown
tests, all 983 `emulebb-ed2k` library tests, all 389 `emulebb-core` library
tests, `cargo check -p emulebb-core --all-targets`, formatting, and whitespace
checks. Strict Clippy reaches only the same seven pre-existing
`unfulfilled-lint-expectations`. Direct-UDP and Kad callback producers still
need the same ticket reservation/settlement migration before the legacy intent
store and listener fallback can be removed.

Direct-UDP callback production is migrated to route-scoped tickets by
`emulebb-rust@77fc35f5`. A type-6 source now reserves admission before queue or
cooldown ownership, requires its non-zero protocol user hash, joins A4AF work
on the same `(source UDP endpoint, user hash)` session, and shares the ticket's
exact absolute deadline and the download cancellation token with the bounded
client-UDP worker. Queue rejection, pre-send cancellation/expiry, and local UDP
send failure are proven-not-sent outcomes which cancel the exact ticket and
linear cooldown claim. Cancellation, expiry, or worker loss after queue
admission is delivery-ambiguous and conservatively arms the ticket and commits
the 45-second peer cooldown. The producer no longer writes the legacy client-ID
intent queue or logs queue admission as a sent datagram.

Validation from committed code passes all 16 direct-callback protocol/runtime
tests, the direct ticket A4AF route test, both direct peer-cooldown tests, all
991 `emulebb-ed2k` library tests, all 391 `emulebb-core` library tests,
`cargo check -p emulebb-core --all-targets`, formatting, and whitespace checks.
Strict Clippy reports only the same seven pre-existing
`unfulfilled-lint-expectations`; rerunning with that pre-existing lint allowed
passes both crates and all targets. Kad callback production remains to migrate
before removing the legacy intent store and listener fallback. Direct callback
transport is also still hosted by the UDP-reask worker, so disabling
`enable_udp_reask` currently suppresses this otherwise independent type-6
connect path; decouple that lifecycle in a separate granular change.

The endpoint-unknown Kad callback prerequisite is implemented by
`emulebb-rust@e745146d`. Generic Kad traversal now reports phase-2 local send
attempt/success counts, returns immediately when no responding contact can be
queried, and exposes a typed FINDSOURCE callback outcome under the caller's
absolute deadline and cancellation token. A callback sent before cancellation
is retained as dispatched; preflight cancellation/expiry, duplicate/busy search
admission, no route, and all-send failure remain distinguishable known-not-sent
outcomes for the producer to settle. All 125 `emulebb-kad-dht` library tests,
strict Clippy for that crate/all targets, formatting, and whitespace checks
pass. The core Kad producer consumes this outcome contract in the following
slice.

Kad callback production is migrated to route-scoped tickets by three granular
`emulebb-rust` commits. `4d75c957` replaces the callback constructor's permanent
lint allowance with a checked expectation. `aa78cc08` makes the typed Kad
dispatch outcome mandatory to consume. `09d9c9d3` reserves a Kad-buddy ticket
before cooldown or wire ownership, requires the source user hash, joins A4AF
files on one `(buddy id, normalized optional buddy endpoint, user hash)`
session, and excludes file identity from the peer-scoped 45-second cooldown.
Direct buddy sends classify local send failure as proven not sent and treat
cancellation or expiry after polling the transport as delivery-ambiguous.
Endpoint-unknown FINDSOURCE traversals share the exact ticket deadline and
download cancellation token, settle from the typed phase-2 send result, run
concurrently with faster direct/server/TCP routes, and remain supervised until
the owning download attempt can safely settle. Known-not-sent outcomes cancel
the exact ticket and linear cooldown claim; sent or ambiguous outcomes arm the
ticket and commit the cooldown from settlement. The Kad producer no longer
writes the legacy callback-intent queue.

Validation from committed behavior passes all 5 focused Kad-producer tests,
all 125 `emulebb-kad-dht` library tests, all 991 `emulebb-ed2k` library tests,
all 392 `emulebb-core` library tests, `cargo check -p emulebb-core
--all-targets`, formatting, and whitespace checks. Strict Clippy reports only
the same seven pre-existing `unfulfilled-lint-expectations`; allowing that
known baseline passes all core targets, and the explicit
`clippy::allow_attributes` gate passes. A separate read-only lifecycle review
found no remaining Kad producer blocker after FINDSOURCE supervision and the
post-drain cancellation guard. All three callback producers now use tickets;
the legacy intent store and listener fallback can be removed next.

The obsolete client-ID-only callback intent path is removed by
`emulebb-rust@db9eb2b0`. `Ed2kCallbackIntent`, its unbounded runtime store, and
the public register/claim API no longer exist. An inbound HELLO starts download
work only after a route-scoped ticket claim; otherwise the connection remains
in the ordinary listener dispatcher and can still serve uploads. The listener
regression now creates the same LowID on two server routes, proves that only the
HELLO's server route is adopted, and proves that the other route remains
independently claimable. A repository-wide search confirms that no producer or
consumer still depends on the removed API.

Validation from committed behavior passes all 98 callback-related
`emulebb-ed2k` tests, all 990 `emulebb-ed2k` library tests, all 392
`emulebb-core` library tests plus its integration and doc tests, the core and
workspace all-target checks, formatting, and whitespace checks. Strict Clippy
still reports exactly the same seven unrelated
`unfulfilled-lint-expectations`; allowing that known baseline passes both
affected crates with warnings denied and the explicit
`clippy::allow_attributes` gate. A separate read-only review confirmed that
unmatched inbound peers retain normal upload handling, route-scoped adoption is
unchanged, all three producers use tickets, and the cross-server LowID test
covers the removed fallback's isolation hazard.

Direct UDP callbacks are decoupled from the optional source-reask lifecycle by
four granular `emulebb-rust` commits. `16b68df4` introduces a dedicated typed
sender over the shared Kad UDP socket, with exact pre-send versus
delivery-ambiguous settlement and fail-closed obfuscation when the public IP is
unknown. `ffaeec42` moves the core type-6 producer to that sender, requires a
live Kad runtime independently of `enable_udp_reask`, and runs the public-IP
fallback for Kad direct callbacks even when source reask is disabled.
`619ecb66` removes the obsolete direct-callback command, outcome, and worker
branch from the reask runtime. `7168ed62` keeps the sole client-UDP ingress
handler and its core event consumer active for `OP_DIRECTCALLBACKREQ` and
`OP_PORTTEST` while suppressing actual source-reask and buddy-relay traffic;
core rechecks the stock `Kademlia::IsRunning() && IsFirewalled()` gate at event
dispatch time.

Regressions prove that the outbound 21-byte callback wire request and both
plaintext and obfuscated inbound callback requests work with
`enable_udp_reask=false`, that source-reask packets remain ignored in that
mode, and that a stopped Kad runtime rejects a callback without consuming its
rate-limit slot. Validation passes all 12 callback-focused `emulebb-ed2k`
tests, all 7 callback-focused `emulebb-core` tests, all 987 `emulebb-ed2k`
library tests, all 394 `emulebb-core` library tests plus its integration tests,
both doc-test suites, affected-crate all-target checks, formatting, and
whitespace checks. Strict Clippy passes for both affected crates and all targets
with warnings denied, the seven known unrelated unfulfilled expectations
allowed, and `clippy::allow_attributes` denied.

Shared callback connect-out admission is implemented by
`emulebb-rust@6dd1a8b4`. Server `OP_CALLBACKREQUESTED`, Kad-relayed
`OP_CALLBACK` from both ordinary peer and held-buddy sockets, and direct-UDP
`OP_DIRECTCALLBACKREQ` all converge on the listener-owned callback-session
supervisor. Immediately before opening TCP, that boundary rejects non-IPv4 or
live-IP-filtered endpoints and applies the peer-ban store's IP-or-known-user-hash
semantics. Because `IpFilter` clones share their mutable backing, queued callback
work observes filter reloads; a ban recorded after queue admission is likewise
rechecked without holding policy locks across network I/O.

Pure admission tests cover filtered, IP-banned, hash-banned, and accepted
identities. Socket-level regressions prove that none of the server, Kad, or
direct-UDP origins reaches a bound filtered listener and that a hash-only ban on
an otherwise unbanned endpoint opens no socket. Validation passes all 5 focused
admission/socket tests, all 992 `emulebb-ed2k` library tests and its doc tests,
affected-crate all-target checks, formatting, and whitespace checks. Strict
Clippy passes for both affected crates and all targets with warnings denied, the
seven known unrelated unfulfilled expectations allowed, and
`clippy::allow_attributes` denied. An independent read-only route review found
no callback connect-out bypass and no local callback-ticket settlement hazard;
it also confirmed the boundary matches community eMule and aMule's final common
`TryToConnect` IP-filter/ban recheck.

Live Kad callback gating is implemented by `emulebb-rust@db62b65b`. The
ordinary inbound-client and held-buddy paths now carry the live `DhtNode`
rather than treating a retained object or cached Kad ID as proof that Kad is
running. A shared pre-parse gate ignores `OP_CALLBACK` while Kad is stopped,
matching community eMule, maintained eMuleBB MFC, and aMule ordering; the shared
authorization boundary rechecks after decoding and again after the asynchronous
file-ownership lookup before queueing the connect-out. This preserves valid TCP
sessions on malformed stopped-Kad traffic and closes stop-time races without
weakening the existing uCheck, file-ownership, endpoint, IP-filter, or ban
guards. Lugdunum has no comparable Kad client path: its apparent `0x99`
occurrences are ED2K UDP global-search responses, while its callbacks are classic
server relays.

Focused regressions prove that callback acceptance follows live Kad state and
that malformed stopped-Kad callbacks leave both an ordinary listener session
and a held-buddy connection alive. Validation passes all 995 `emulebb-ed2k`
library tests, all 394 `emulebb-core` library tests plus its integration tests,
both doc-test suites, affected-crate all-target checks, formatting, and
whitespace checks. Strict Clippy passes for both affected crates and all targets
with warnings denied, the seven known unrelated unfulfilled expectations
allowed, and `clippy::allow_attributes` denied.

Stock-compatible `OP_REJECT` handling is implemented by three granular
`emulebb-rust` commits. `5513fb0d` changes the shared/background packet handler
to treat `OP_REJECT` as an uncorrelated notice, preserving both a pending login
and a typed background request; it also removes the unsafe reject-triggered
offer-pacing downgrade. `8eb3ee31` applies the same rule to the one-shot keyword,
source, and callback sessions, while retaining `OP_CALLBACK_FAIL` as the typed
callback failure. It also makes the callback response grace deadline reach its
intended success outcome when no explicit failure arrives. `f48d99cc` removes
the semantic `last_tx_opcode`, the reject-only conservative offer mode, its
fallback-delay machinery, and the now-unused private protocol-rejection
constructor. `last_tx` remains solely as an idle/keepalive timestamp.

Community eMule, maintained eMuleBB MFC, and aMule all log `OP_REJECT` and return
success from their packet handlers without disconnecting or mutating a pending
request. Their protocol declarations describe opcode `0x05` as a null packet:
it carries no request ID, rejected opcode, hash, client ID, or other correlator.
Consequently the old latest-transmit inference was not merely divergent but
racy: an offer rejection can queue during the 80 ms offer quiet period, after
which a search overwrites the latest opcode before the queued rejection is
read. ed2k-server defines the constant but supplies no correlatable producer,
and the Lugdunum decompile supplies no rejection payload contract or evidence
for latest-transmit attribution. The safe Rust model therefore completes
requests only from their typed responses, cancellation, deadline, or transport
closure; it never eagerly guesses which command a null reject concerned.

Focused regressions cover reject-before-`OP_IDCHANGE`, a pending background
keyword search, negotiated offer pacing, one-shot keyword and source searches,
and callback reject versus typed `OP_CALLBACK_FAIL`. Empty and nonempty reject
payloads are both nonfatal. Validation from committed state passes all 999
`emulebb-ed2k` library tests, all 394 `emulebb-core` library tests plus both
crates' integration and doc tests, affected-crate all-target checks, formatting,
and whitespace checks. Strict Clippy passes for both affected crates and all
targets with warnings denied, the seven known unrelated unfulfilled
expectations allowed, and `clippy::allow_attributes` denied.

## Notes

Implementation order follows dependency pressure: establish callback session
ownership first, then chained UDP decoding, callback tickets, shared admission,
recoverable server failures, and shared-server upload promotion. If a later
slice reveals that two findings require one atomic abstraction change, retain
separate behavioral commits on top of the shared refactor rather than combining
unrelated protocol outcomes.
