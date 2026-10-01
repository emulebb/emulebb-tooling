# IDEA: eD2K Extension Interoperability And Evolution

> **Exploratory proposal only.** This is a dated interoperability audit and a
> possible long-term direction, not an approved protocol standard, active
> implementation plan, or release commitment. Any implementation slice must be
> promoted through the owning project's normal issue and review process.
>
> Evidence refreshed 2026-10-01. Revalidate every implementation claim against
> current upstream source before using it as a merge or deployment decision.

## Executive Summary

The stock eD2K client/server protocol remains the common interoperable base.
Login, server status, search, IPv4 source exchange, callbacks, file offers,
large-file support, and protocol obfuscation continue to work between stock
eMule-family clients and the reviewed Rust server.

The newer features do not yet form one shared extension protocol:

- eMuleAI has the broadest working client-to-client extension set: extended
  source exchange, IPv6 metadata, eServer Buddy relay, uTP, and QUIC.
- aMule recognizes much of the eMuleAI vocabulary and contains experimental
  transport and server-NAT-T pieces, but it deliberately advertises no
  eMuleAI capability bits and does not provide a complete enabled path.
- the Rust server implements its own server-assisted NAT traversal and an
  opt-in IPv6 source-record extension. Neither currently has a complete,
  verified client consumer among the reviewed releases.
- `OP_SERVERIDENT` is extensible at the encoding level, but current stock
  eMule, aMule, and eMuleAI do not treat it as a general capability bus.

The safest evolution model is therefore **stock protocol plus small,
independently versioned extension families**. Each family needs explicit
discovery in every required direction, precise lifetime and validation rules,
stock fallback, and cross-project packet tests. A capability must not be
advertised until the complete behavior it promises is usable.

Negotiated `OP_OFFERFILES` pacing is a good first extension because it can use
unknown-safe named tags without changing the offer packet format. It should
remain a bounded implementation issue while a broader shared document records
the conventions that later extensions reuse.

## Evidence Baseline

This snapshot compares the following revisions:

| Implementation | Reviewed revision | Role in this audit |
|---|---|---|
| eMule Community 0.72a | [`ac3d52e`](https://github.com/irwir/eMule/commit/ac3d52eafd88e9f6d9e0c2204c6dbead18db750b) | Current stock-client baseline |
| aMule | [`9f372c1`](https://github.com/amule-org/amule/commit/9f372c1ca2a78cad771a356feafe89c868dc86f7) | Cross-platform client and compatibility work |
| eMuleAI 1.6 | [`a2f05dc`](https://github.com/eMuleAI/eMuleAI/commit/a2f05dc8db772a11ca874adf0a16baaf30560519) | Vendor-extension reference client |
| Rust eD2K server 0.9.76 | [`78b1e4f`](https://github.com/andrey23127/ed2k-server/commit/78b1e4fde6a0e018975ab18e3d1d1f077e48c83a) | Open server implementation |

The managed `emulebb/ed2k-server` fork was at `f97d9c5`, exactly the reviewed
upstream code plus its repository-onboarding commit. Lugdunum 17.15 behavior is
used as the historical server reference where the meaning of legacy limits is
otherwise ambiguous.

The coordination discussions are
[aMule #1699](https://github.com/amule-org/amule/issues/1699) and
[ed2k-server #19](https://github.com/andrey23127/ed2k-server/issues/19).
Those discussions remain open; this document records proposals and points of
agreement without presenting an unsettled wire contract as final.

## Terms And Compatibility Model

This document distinguishes three capability states:

- **Supported:** the implementation contains a complete compatible behavior.
- **Enabled:** the operator or build has allowed that behavior for this run.
- **Usable now:** the required local endpoint, remote endpoint, route, and
  negotiated peer/server state are all available.

A single bit must not ambiguously mean all three. IPv6 support, for example,
does not prove that a client has a public IPv6 address, that the address is
reachable, or that the current peer can consume an extended source record.

It also distinguishes three rollout stages:

1. **Parse:** accept and validate the remote field without changing outbound
   behavior.
2. **Advertise:** claim support only after the full local path works.
3. **Act:** select the extension only after the remote side explicitly claims
   compatible support for the same version.

Unknown optional tags should be ignored. Missing, malformed, contradictory, or
unsupported capability data must select stock behavior rather than a partial
extension.

## Practical Interoperability At This Snapshot

| Pair | Stock operations | Extension result |
|---|---|---|
| Stock eMule and Rust server | Interoperable | No Rust NAT-T or IPv6-only source records |
| eMuleAI and Rust server | Interoperable | IPv6 negotiation is close but defective; Rust NAT-T is unused |
| aMule and Rust server | Interoperable | No complete server NAT-T or IPv6-source path |
| eMuleAI and eMuleAI | Interoperable | Full eMuleAI extension set when enabled |
| aMule and eMuleAI | Interoperable | Mostly stock fallback; limited experimental one-way opportunities |
| aMule and aMule | Interoperable | Normal builds remain effectively stock on these extensions |

The usual failure mode is safe feature loss: a capability is absent, so both
sides fall back to stock behavior. The dangerous case is a variable-length
wire record sent to a receiver that was incorrectly classified as capable. An
IPv6 source record is 16 bytes longer than its stock form; one wrong decision
can misalign every following record in the packet.

## `OP_SERVERIDENT` As A Capability Carrier

`OP_SERVERIDENT` already contains a typed tag list, and unknown tags are
skipped by legacy clients. This makes named tags a practical server-to-client
extension carrier without changing the packet envelope.

Its present use is much narrower than its encoding allows:

- stock eMule's direct handler acts on server name and description;
- current aMule's direct handler likewise consumes name and description;
- current eMuleAI consumes name and description and logs unknown fields;
- the Rust server sends name, description, version, maximum users, soft/hard
  file values, UDP flags, obfuscation ports, and optional IPv6 fields.

Clients may learn some of those standard fields through `server.met` or UDP
server-status replies instead. That does not make the live
`OP_SERVERIDENT` packet a negotiated policy channel.

Consequences:

- adding a named tag is backward-compatible but has no effect until a client
  explicitly parses and acts on it;
- `OP_SERVERIDENT` is server-to-client only, so any feature that requires the
  server to know client support also needs a client-login field;
- negotiated values should be connection-scoped unless a specification
  explicitly defines safe persistence and expiry;
- numeric tag IDs should be reserved only through cross-project agreement;
  string-named tags avoid the existing unofficial numeric collisions.

## Legacy Offer Limits And Pacing

### `ST_SOFTFILES`

`ST_SOFTFILES` is the connected client's accumulated indexing budget in the
historical Lugdunum behavior. Accepted shares accumulate for the connection.
Once the budget is full, later records are ignored and the client may receive
a message explaining that some shares were not accepted.

This is not formally a packet-size or packet-rate field. Stock-derived clients
nevertheless use it as a conservative batch heuristic:

```cpp
uint32 limit = server->GetSoftFiles();
if (limit == 0 || limit > 200)
    limit = 200;
```

That behavior makes `min(ST_SOFTFILES, 200)` the practical legacy batch size,
but does not redefine the server's accumulated indexing budget.

### `ST_HARDFILES`

Historical Lugdunum checks `ST_HARDFILES` against the declared count at the
start of an individual `OP_OFFERFILES` packet, before parsing its records. The
ordinary and compressed handlers differ at the equality boundary, so a
portable client should keep every batch **strictly below** the advertised hard
value.

The historical meanings are therefore:

```text
ST_SOFTFILES   accumulated per-connection indexing budget
ST_HARDFILES   legacy per-message hard safety boundary
pacing         records per batch and time between batches
```

These meanings can appear equivalent when a client sends one share-list
packet. They diverge as soon as a client publishes the list in many batches.

The Rust server is deliberately moving toward a different hard-limit policy:
a per-client total of distinct currently sourced files, truncating new records
at the limit without disconnecting and permitting refreshes of already indexed
hashes. At the reviewed public commit, the advertised soft/hard configuration
was not enforced and the old `> 4000` check had an empty body. The maintainer
subsequently reported the hard-limit correction deployed and planned for the
next public push; that not-yet-published code was not available for this source
audit. The maintainer also stated that Rust `soft_limit_files` remains
advertisement-only.

This is a real semantic divergence, not merely different implementation code.
Any shared specification must say whether its use of soft/hard values describes
historical Lugdunum semantics, a new server policy, or only client-side safety.

### Live-Network Observation

The public `server.met` feed was read in memory on 2026-10-01. Its 13 entries
advertised generic ranges of:

- soft limits: **5,000 to 1,000,000** files;
- hard limits: **7,500 to 10,000,000** files.

Several servers advertised equal values or a hard value only slightly above
soft, while others advertised a much larger hard boundary. Server identities
and addresses are intentionally not retained here. The feed is volatile, and
advertisement alone does not prove that a server enforces the stated values.

The range proves that neither legacy field communicates an acceptable record
rate. It also means a 60,000-file target is possible only when the selected
server's indexing budget is at least that large.

### Current Pace And Target

Stock eMule, aMule, eMuleAI, and eMuleBB use a maximum legacy batch of 200
records and a one-minute republish interval. At that pace, 60,000 candidates
require 300 batches and roughly five hours.

The proposed initial accelerated policy is:

```text
batch maximum        200 records
minimum interval     500 ms
local maximum rate   400 records/second
```

For 60,000 candidates:

```text
300 batches
(300 - 1) * 500 ms = 149.5 seconds
```

This is about two minutes and thirty seconds between the first and last batch,
leaving substantial margin below a five-minute objective. Keeping the familiar
200-record packet bounds per-packet parsing and indexing spikes; reducing the
interval raises throughput without creating much larger packets.

## Candidate Offer-Pacing Version 1

This section records the current eMuleBB proposal. It is **not yet an agreed
wire standard**.

A capable server would send one complete set in post-login `OP_SERVERIDENT`:

| Field | Type | Candidate rule |
|---|---|---|
| `ST_SOFTFILES` | Numeric-tag `uint32` | Non-zero candidate budget |
| `ST_HARDFILES` | Numeric-tag `uint32` | Greater than the negotiated batch maximum |
| `offerfiles_v` | Named-tag `uint32` | Exactly `1` |
| `offerfiles_batch_max` | Named-tag `uint32` | Greater than zero |
| `offerfiles_min_interval_ms` | Named-tag `uint32` | Greater than zero |

The five-field advertisement is atomic. A missing or duplicate field, wrong
type, zero value, unsupported version, or inconsistent relationship invalidates
the extension. Invalid or absent capability data selects the legacy policy of
200 files and 60,000 ms.

The effective batch size is:

```text
min(
    remaining ST_SOFTFILES candidate budget,
    offerfiles_batch_max,
    ST_HARDFILES - 1,
    local client batch cap
)
```

The client counts candidate records sent, not presumed accepted records. There
is no per-record result in version 1, so content filtering can produce fewer
indexed files than the candidate budget without telling the client which
records should replace them.

The first accelerated batch is allowed only after the complete advertisement
has been parsed. Subsequent batches use a monotonic clock, obey the server's
minimum interval, and also obey a local maximum rate. The policy is cleared on
disconnect or server change and is not persisted into `server.met`.

### Server-Side Requirements

A production server needs more than a per-client interval check:

- per-client record-rate accounting;
- a server-wide processing ceiling for reconnect waves;
- fair scheduling between active publishers;
- bounded queues and TCP backpressure;
- enforcement derived from the same connection policy advertised to the
  client;
- counters for accepted, filtered, over-budget, malformed, and deferred
  records.

TCP buffering and scheduler delays can cause separately sent frames to arrive
together. Arrival adjacency is not proof that the client violated its sending
interval. A compliant batch should be queued, deferred, or naturally slowed by
TCP backpressure rather than silently discarded because global processing is
busy. Without acknowledgements, the client cannot reliably detect such loss.

Content filtering, exhausted candidate budget, malformed records, a batch
above the negotiated maximum, the hard safety boundary, and deliberate flooding
remain valid rejection cases.

### Unresolved Coordination Points

The Rust maintainer's first proposal used shorter names (`offer_v`,
`offer_batch`, and `offer_interval_ms`) plus `offer_burst`. The revised eMuleBB
proposal uses the `offerfiles_*` prefix and omits a client-visible burst
entitlement. The following points still require explicit agreement:

- final tag names;
- whether version 1 has a burst field;
- historical per-message versus new per-client hard-limit semantics;
- whether a hard value of zero can mean disabled in an accelerated policy;
- exact server behavior under temporary global overload;
- which values may be enabled by default after concurrent-publisher testing.

aMule's maintainer supports implementing a draft while making wire agreement a
prerequisite for merge and activation. They also support keeping the bounded
publication issue separate from a broader extension-framework discussion.

## Peer Capability Surfaces

### eMuleAI Capability Word

eMuleAI advertises `CT_MOD_MISCOPTIONS` (`0xAA`) in peer hello metadata. The
reviewed implementation assigns:

| Bit | Meaning | eMuleAI behavior |
|---:|---|---|
| 0 | Extended source exchange | Advertised and used |
| 1 | uTP NAT traversal | Advertised when enabled and allowed |
| 2 | IPv6 | Advertised |
| 3 | Serving Buddy pull | Advertised and used |
| 4 | QUIC NAT traversal | Advertised when enabled and runtime-ready |

aMule parses and stores those five bits but its
`LocalAdvertisedModMiscOptions()` returns zero. It deliberately masks later
bits because other implementations have already assigned conflicting meanings
to parts of the remaining word. This makes the field a useful legacy eMuleAI
compatibility input, not a safe unbounded registry for future ED2K features.

eMuleAI also emits `ET_MOD_VERSION`. Compatibility code must account for the
fact that some mod-detection policies treat vendor capability tags without a
matching mod identity as suspicious.

### Reserved UDP Frame Multiplexing

Both current eMuleAI and aMule recognize `OP_UDPRESERVEDPROT2` (`0xB2`) as a
container with an inner frame type:

| Type | Meaning | Current interoperability |
|---:|---|---|
| `0x00` | uTP payload | eMuleAI complete; aMule experimental |
| `0x01` | QUIC payload | eMuleAI complete; aMule scaffolding |
| `0x02` | Transport capabilities | eMuleAI; aMule does not complete negotiation |
| `0x03` | Capability acknowledgement | eMuleAI; aMule does not complete negotiation |
| `0xFF` | Key material | Vendor transport path |

aMule has optional uTP datagram, inbound-stream, and outbound-dial seams, with
`ENABLE_UTP` off by default. QUIC is optional scaffolding under
`ENABLE_QUIC`, also off by default. Because aMule advertises none of the peer
capability bits, eMuleAI will not normally select those transports toward it.
An experimental aMule build may recognize eMuleAI's advertisement and initiate
some uTP behavior, but that is not symmetric, default interoperation.

## NAT-Traversal Divergence

Three mechanisms solve overlapping LowID reachability problems:

### Classic Kad Buddy

This is the stock-compatible baseline. It remains the universal fallback where
Kad state and buddy availability permit it.

### eMuleAI eServer Buddy

eMuleAI implements a client-side same-server relay using private peer opcodes in
the `0xB3`-`0xBB` range, Serving Buddy metadata, external UDP discovery, hole
punching, and transport negotiation. It uses stock server callback behavior and
does not require a modified Lugdunum server.

It can select QUIC and fall back to uTP. This path is complete primarily for
eMuleAI-to-eMuleAI traffic. aMule records parts of the capability vocabulary but
does not implement the relay behavior.

### Rust Server-Coordinated NAT-T

The Rust server defines a separate path:

| Opcode | Direction | Purpose |
|---:|---|---|
| `0x60` | Client to server, TCP | Hole-punch request |
| `0x61` | Server to client, TCP | Peer endpoint information |
| `0x62` | Server to client, TCP | Failure response |
| `0x9F` | Client to server, UDP | NAT-T keepalive/liveness |
| `0xB3` | Peer to peer, UDP | Hole-punch datagram |

The server currently infers support from a non-zero `CT_EMULE_UDPPORTS` login
tag instead of an explicit protocol-version capability. Stock eMule, current
eMuleAI, and current aMule do not negotiate this server path during login.
aMule has matching experimental payload codecs under
`ENABLE_NATT_SERVER_COORDINATION`, but no login advertisement, dispatch, or
network integration.

The reused `0xB3` value is not automatically a collision because the protocol
envelope, direction, and transport provide context. It still demonstrates why
an extension registry must record the entire namespace rather than only the
byte value.

Long term, these mechanisms should be complementary rather than forced into one
transport:

1. use a negotiated same-server direct/server-assisted path when available;
2. use eServer or Kad buddy rendezvous where appropriate;
3. retain stock callback and TCP behavior as the final fallback.

Selection requires explicit mode/version negotiation. A UDP-port tag alone
does not prove support for the Rust opcode family.

## IPv6 Divergence

### Shared Vocabulary

The implementations overlap on several unofficial fields:

| Field | Value | Intended role |
|---|---:|---|
| `CT_EMULE_SERVINGBUDDYIPV6` | `0xA0` | Serving-buddy IPv6 address |
| `CT_MOD_YOUR_IP` | `0xAD` | Peer-reported local address |
| `CT_MOD_IP_V6` / `ST_IPV6` | `0xAE` | Client or server IPv6 by direction |
| `ST_IPV6_STATUS` | `0xAB` | Server verdict on client IPv6 state |
| source sentinel | `0xFFFFFFFF` | Inline IPv6-only source record |

`0xAE` is used in different packet directions and tag namespaces. That is
decodable but must be documented explicitly. A registry entry needs carrier,
direction, type, and lifetime; a symbolic name and number are insufficient.

### Rust Server Extension

When enabled, the Rust design accepts `CT_MOD_IP_V6` during client login,
advertises IPv6 source support in its server flags, can publish server IPv6
metadata in `OP_SERVERIDENT`, and sends an IPv6-only source as:

```text
client id    0xFFFFFFFF
TCP port     uint16
address      16 raw IPv6 bytes
```

The extension is gated per requesting client because sending the longer record
to a stock parser would misalign the rest of the source list.

### eMuleAI Compatibility Defect

eMuleAI sends `CT_MOD_IP_V6` to a server when it has a public IPv6 address. It
does not set the separately documented `0x1000` client capability flag, while
the reviewed Rust server treats the address tag itself as sufficient evidence
that the client can parse inline IPv6 sources.

eMuleAI recognizes the `0xFFFFFFFF` source sentinel and consumes the following
16 bytes, but its current parser shadows the outer address variable:

```cpp
CAddress IPv6;
...
CAddress IPv6 = CAddress(abyIPv6);
```

The constructed source therefore receives the still-empty outer address. The
packet remains byte-aligned, but the IPv6 endpoint is discarded and the source
is unusable or misrepresented. See the reviewed
[`PartFile.cpp`](https://github.com/eMuleAI/eMuleAI/blob/a2f05dc8db772a11ca874adf0a16baaf30560519/srchybrid/PartFile.cpp#L3584-L3590).

aMule does not implement the inline sentinel source record. It parses several
peer/Kad IPv6 hints and has experimental typed-address work, but current routing
and identity integration remains incomplete.

An IPv6 source version cannot be called interoperable until all participants
agree on:

- the authoritative client capability signal;
- whether the address tag and capability flag must be coupled;
- source-record byte order and placement relative to optional fields;
- supported versus enabled versus reachable state;
- IPv4 preference and LowID callback fallback;
- malformed and contradictory input handling;
- cross-client golden vectors and live transfer proof.

## Other Reviewed Capabilities

### Extended Source Exchange

eMuleAI implements variable source metadata including IPv6, server, and buddy
information and advertises bit 0 in `CT_MOD_MISCOPTIONS`. aMule recognizes the
claim but does not advertise or implement the corresponding complete exchange.
The Rust index server is not a participant in peer source-exchange framing.

### Rust HighID Verification

The Rust server optionally verifies a claimed HighID identity by performing a
client-to-client hello/hash check. A positive wrong-hash result can downgrade a
later login; silence alone does not. This improves server trust behavior
without introducing a new client wire format.

### Rust Search Behavior

The Rust server adds source-count ranking, configurable result limits, subtoken
indexing, and unknown-word handling. These are server policy and quality
improvements over the historical baseline, not negotiated client capabilities.
They should not consume capability IDs unless the reply format itself changes.

### aMule Kad And Control Work

Recent aMule work includes an optional Kad `0x0A` preference, AICH-related
handling, parser hardening, and expanded REST/EC control surfaces. These are
important implementation improvements but are separate from the server and
peer extension framework described here.

## Capability-Claim Correctness

An advertised capability is a safety contract. At this snapshot:

- aMule follows the conservative side of that rule by parsing claims while
  advertising zero until its consumer paths are complete;
- eMuleAI actively advertises its vendor capabilities and implements their
  peer paths, but its server IPv6 source consumer contains the defect above;
- Rust `SERVER_UDP_FLAGS` advertises `RELATEDSEARCH` (`0x0040`) although the
  reviewed source explicitly says it is not implemented;
- the reviewed public Rust commit advertises soft/hard file values without
  enforcing either in the offer handler; the maintainer reports a later
  hard-limit fix, not yet available in public source, while soft remains
  advertise-only.

The long-term rule should be:

> Parse defensively; advertise only a complete enabled behavior; act only after
> compatible negotiation; clear the claim when the connection context ends.

Flags that overstate implementation should be cleared until the behavior and
tests exist. Configuration values may still be exposed as informational
metadata, but they must not be described as enforced policy when they are not.

## Long-Term Extension Framework

### Preserve The Stock Base

Stock eD2K remains the mandatory fallback. Extensions must not alter packet
interpretation for a participant that did not explicitly negotiate them.

```text
Stock eD2K
  + offer policy v1
  + IPv6 sources v1
  + server NAT-T v1
  + peer NAT-T transports v1
  + extended source exchange v1
```

These are independent families, not one monolithic "modern client" bit.
Implementations can adopt them at different rates without pretending to
support unrelated behavior.

### Use Direction-Appropriate Discovery

| Direction | Preferred carrier | Reason |
|---|---|---|
| Server to client | Named `OP_SERVERIDENT` tags | Unknown-safe server policy advertisement |
| Client to server | Explicit login tags or flags | Server must know what replies are safe |
| Peer to peer | Hello tags plus versioned frame negotiation | Both endpoints select transport/metadata |

`CT_MOD_MISCOPTIONS` bits 0-4 should be treated as the frozen legacy eMuleAI
set. New shared features should not claim arbitrary remaining bits without a
registry and named owner.

### Define Every Extension Completely

Each extension record should contain:

- stable family name and version;
- carrier, direction, protocol envelope, and transport;
- exact type, byte order, and length;
- whether the value means supported, enabled, or usable;
- negotiation lifetime and reset events;
- validation and contradiction rules;
- sender and receiver resource limits;
- malformed-input and overload behavior;
- stock fallback;
- privacy and abuse considerations;
- golden packets and known passing implementations.

### Keep The Registry Version-Controlled

A public wiki or discussion is useful for collaboration, but the authoritative
contract should ultimately be version-controlled Markdown plus machine-readable
packet vectors. Discussions can propose changes; reviewed commits should state
what implementations can depend on.

The registry should record contextual reuse instead of pretending every opcode
byte is globally unique. At minimum, its key is:

```text
protocol envelope + transport + direction + carrier/opcode/tag + version
```

### Test Interoperability, Not Only Parsers

Every extension should have:

- encode/decode golden vectors in every participating implementation;
- malformed, duplicate, truncated, oversized, and unsupported-version cases;
- absence and invalid-capability fallback tests;
- reconnect and server-switch lifetime tests;
- concurrency and reconnect-wave tests for server policy;
- packet captures proving stock peers receive stock records;
- at least one bidirectional live scenario between independent projects.

For variable-length records such as IPv6 sources, include multi-record packets
so a length mistake cannot hide behind a single final record.

## Recommended Sequence

1. **Correct current claims and consumers.** Clear unimplemented advertised
   bits, publish the Rust hard-limit fix, describe soft enforcement honestly,
   and fix the eMuleAI IPv6 shadowing defect.
2. **Settle offer pacing v1.** Agree names, validation, lifetime, hard/soft
   interpretation, overload handling, and default-off rollout between aMule
   and the Rust server.
3. **Validate the pace under load.** Exercise 200 records every 500 ms with
   concurrent publishers and reconnect waves before recommending production
   defaults. Prove 60,000 candidates complete within five minutes when the
   server budget permits.
4. **Specify IPv6 sources v1.** Resolve the capability signal and source-record
   contract, then require cross-client golden and live tests.
5. **Add explicit server NAT-T discovery.** Do not infer a protocol version from
   a UDP-port tag. Complete one client and server path before advertising it.
6. **Document fallback selection.** Treat server-assisted, eServer Buddy, Kad
   Buddy, stock callback, QUIC, uTP, and TCP as negotiated alternatives with
   deterministic fallback rather than competing private forks.

## Current Decision Record

- Keep the concrete aMule publication issue open and bounded.
- Keep the server companion discussion linked and resolve its differences
  before merge or activation.
- Do not make the broader framework a prerequisite for the first extension;
  capture only the reusable rules that offer pacing actually needs.
- Do not change the `OP_OFFERFILES` record format for pacing version 1.
- Prefer named `OP_SERVERIDENT` tags and complete-set validation.
- Keep accelerated publication default-off until interoperability and load
  evidence exists.
- Treat all other content in this document as analysis and candidate direction,
  not active eMuleBB scope.

## Related Workspace Notes

- [NAT Traversal And uTP](IDEA-NAT-TRAVERSAL-UTP.md) contains the earlier,
  narrower transport analysis.
- [aMule Reference Watchlist](IDEA-AMULE-WATCHLIST.md) records the older aMule
  reference posture.
- [IPv6 Kad Network](IDEA-IPV6-KAD-NETWORK.md) explores the broader IPv6/Kad
  problem beyond server source records.
- [Kad Protocol Modernization](IDEA-KAD-PROTOCOL-MODERNIZATION.md) discusses
  compatibility risks in a separate protocol family.
