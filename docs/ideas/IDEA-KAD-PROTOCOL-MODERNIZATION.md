# Idea: Kad Protocol Modernization And Parallel Overlay

Exploratory idea material. This is not an active implementation plan, release
scope, or current product claim unless a future `docs/active/` item explicitly
promotes a specific slice. Any forward implementation targets **emulebb-rust**
(the forward eD2K/Kad core); the eMuleBB MFC app is frozen, so the MFC code
observations below are reference, not a work plan for that app.

## Summary

This note captures two separate Kad modernization lanes:

- compatibility-preserving improvements for the current public eMule Kad
  network
- a deeper, speculative design for a parallel modern Kad-derived overlay

The distinction matters. The current eMule Kad network is shared infrastructure,
and small wire-level changes can damage interoperability, routing behavior,
search quality, and user trust. eMuleBB policy therefore requires stock
compatibility for current Kad behavior: packet shapes, opcode meanings,
state-machine behavior, peer interaction rules, persistence semantics, and
default network behavior must remain compatible unless a future active item
explicitly proves and promotes a protocol-adjacent change.

The compatible lane should make the existing network safer, more observable,
and more usable without changing what old peers see. The parallel-overlay lane
is the place to discuss larger architectural moves such as IPv6-native routing,
capability negotiation, stronger endpoint proofs, publish tokens, privacy
improvements, and a cleaner contact model.

## Current Constraints And Local Observations

The frozen eMuleBB MFC app keeps the classic Kad shape (these are reference
observations; forward changes land in emulebb-rust):

- contacts are IPv4-shaped, with `CContact` carrying a `uint32` IP, UDP port,
  TCP port, Kad version, UDP key, and verification state
- routing uses classic XOR distance over 128-bit Kad IDs
- the active routing bin size and lookup fanout are defined by classic
  constants such as `K = 10` and `ALPHA_QUERY = 3`
- incoming request flood control is implemented locally through per-IP and
  per-opcode token-bucket tracking
- bootstrap persistence still centers on `nodes.dat`, with later additions for
  validation, bootstrap-only snapshots, and Fast Kad sidecar metadata
- Fast Kad already learns response times and recent healthy contact state for
  faster bootstrapping

Those details point to the most useful modernization direction: improve
admission, endpoint verification, scheduling, evidence, bootstrap freshness,
and diagnostics first. Treat wire-level changes as a separate design effort.

## Design Principles

1. Preserve current Kad network compatibility by default.
2. Never send packet bodies to old peers that they may misparse as classic
   Kad2.
3. Prefer local scoring and local evidence over global reputation.
4. Require reachability proof before granting routing or publish weight.
5. Keep IPv4 and IPv6 transport state separate even if the user sees one Kad
   service.
6. Version every extension and make unknown extensions ignorable.
7. Add observability before changing runtime behavior.
8. Treat protocol changes as network migrations, not local refactors.

## Lane A: Compatible Kad Improvements

### Dual-Stack Readiness Without Wire Drift

The best near-term IPv6 work is not to reinterpret classic IPv4 fields. It is
to prepare the local architecture for address-family separation while keeping
classic `kad4` untouched.

Useful compatible work:

- introduce internal endpoint abstractions that can represent IPv4 and IPv6
  without changing classic packet bodies
- keep persisted IPv4 bootstrap data separate from any future IPv6 bootstrap
  state
- report local bind, interface, and reachability decisions clearly
- expose diagnostics that distinguish IPv4 UDP reachability, IPv4 TCP
  reachability, IPv6 UDP reachability, and IPv6 TCP reachability
- ensure current Kad source publish and lookup behavior remains byte-compatible
  while the app becomes address-family-aware internally

This prepares for future `kad6` without making the current public network parse
experimental fields.

### Stronger Endpoint Verification

Current Kad already uses UDP keys and challenge-style verification. That should
be tightened as a compatibility-preserving local policy.

Recommended direction:

- classify contacts as `seen`, `challenged`, `verified`, `stable`, and
  `decayed`
- require recent endpoint proof before promoting contacts into primary routing
  slots
- give lower routing value to contacts that only appeared through unsolicited
  traffic
- treat identity flips for the same endpoint as suspicious
- decay verification after long silence or after observed endpoint changes
- prefer verified contacts in closest-node responses and bootstrap seed
  selection

The security goal is not cryptographic identity. The goal is to make spoofing,
reflection abuse, routing-table pollution, and cheap churn less useful.

### Routing Diversity And Eclipse Resistance

The existing routing bin already limits repeated IPs and IPv4 subnets. A more
formal diversity policy would make eclipse attacks more expensive.

Compatible improvements:

- keep one-contact-per-IP and per-prefix limits for primary routing admission
- measure prefix concentration per bucket and per lookup result frontier
- maintain a replacement cache for candidates that are not yet safe to promote
- prefer long-lived, recently responsive, verified contacts over new churn
- penalize contacts whose Kad ID is suspiciously convenient relative to many
  unrelated lookup targets
- keep local negative evidence local; do not publish reputation claims to the
  network

For IPv6-capable work, diversity rules must become family-specific. IPv4 `/24`
logic does not translate directly to IPv6. Future IPv6 admission policy should
reason in terms of `/64`, and possibly broader configurable provider prefixes
when evidence shows clustering.

### Adaptive Lookup Scheduling

Classic Kad constants are simple and robust, but modern networks vary more than
the original design assumed. A compatible scheduler can keep the same lookup
semantics while improving pacing.

Useful behavior:

- start with conservative fanout
- increase fanout only when measured timeout and RTT evidence says it helps
- stop earlier when closest-node convergence is clear
- keep interactive user searches ahead of background source lookups
- avoid stampeding the same keyspace with many parallel searches
- use learned response-time estimates to tune pending cleanup windows
- keep hard caps so local scheduling does not become a flood amplifier

This follows the spirit of Fast Kad while preserving lookup semantics.

### Publish Flood Resistance

Fake source and keyword publishes are a practical Kad weakness. Compatible
hardening should focus on local acceptance rules and abuse throttling.

Recommended direction:

- rate-limit publish requests by endpoint, opcode, target key, and local load
- require source-publish metadata to be structurally complete before indexing
- reject impossible port, source-type, LowID, or buddy metadata combinations
- expire abusive routing contacts when flood evidence escalates
- keep publish rejection reasons observable in debug traces
- avoid using publish count as a direct trust score

Publish hardening should be careful not to reject valid older peers merely for
lacking future extension fields.

### Local Source Quality Evidence

Kad can provide discovery evidence, not safety. The client should avoid turning
Kad into a global reputation system, but it can present better local evidence.

Useful local scoring:

- independent publisher diversity
- age of the last source publish
- number of distinct names for the same hash
- agreement on file size, type, and AICH metadata where available
- endpoint reachability evidence for published sources
- prior local download success or failure for equivalent endpoints

This should be used to sort, annotate, deduplicate, or demote results. It
should not be presented as proof that a file is safe or authentic.

### Bootstrap Freshness And Integrity

Bootstrap material is a supply-chain surface. A stale or malicious `nodes.dat`
can herd new clients toward poor routing neighborhoods.

Compatible improvements:

- validate downloaded `nodes.dat` candidates before promotion
- preserve learned Fast Kad health metadata across imported bootstrap files
- track bootstrap snapshot freshness
- support signed bootstrap snapshots before treating remote bootstrap material
  as a default path
- require prefix and endpoint diversity in bootstrap candidates
- measure bootstrap success by verified live contacts, not raw candidate count
- keep bootstrap-only contact lists separate from durable routing-table state

The goal is to recover faster without creating a centralized trust bottleneck.

### Parser And Resource Hardening

Kad packet parsing should have explicit bounded behavior everywhere.

Recommended limits:

- maximum packet body size by opcode
- maximum tag count
- maximum tag value size
- maximum search expression depth
- maximum returned contacts per response
- maximum publish values per request
- duplicate tag policy per opcode
- strict integer range checks for ports, counts, and lengths
- graceful rejection before mutating durable state

This is low-drama work with high security value.

### Observability And Evidence

Before any behavior changes are promoted, Kad needs better evidence capture.

Useful traces:

- packet-level opcode counters by accepted, dropped, malformed, flood-limited,
  and unsolicited response categories
- lookup frontier traces with queried contacts, response times, and convergence
  state
- routing table snapshots with bucket, prefix, contact age, verification state,
  and replacement-cache state
- publish acceptance/rejection traces with non-sensitive reason codes
- bootstrap traces showing candidate source, selected contacts, response rate,
  and verified-contact yield
- search-result provenance showing whether evidence came from eD2K, Kad
  keyword search, Kad source search, cached local data, or merged evidence

Protocol-adjacent changes should carry parity evidence against the community
baseline before release claims.

## Lane B: Parallel Modern Kad Overlay

The deeper-change design should be a parallel overlay, not a mutation of the
classic public Kad network. This note uses `kad-ng` as a placeholder name.
Actual naming would need a separate active design.

### High-Level Shape

`kad-ng` would be a modern, explicitly versioned DHT overlay that preserves the
eMule use case but does not pretend to be classic Kad2 on the wire.

Core model:

- classic `kad4` remains the current Kad2 network
- future `kad6` or `kad-ng` runs as a separate overlay with separate routing,
  bootstrap, contact encoding, and capability state
- search and publish are merged above the overlay layer
- old peers never receive `kad-ng` packets
- new peers may participate in both classic Kad and `kad-ng`

This avoids a fork of the existing network while allowing meaningful design
cleanup.

### Contact Model

A modern contact should carry:

- node ID
- endpoint family
- one or more endpoints
- UDP and TCP reachability state per endpoint
- protocol version
- capability bits
- endpoint proof state
- last successful query time
- observed RTT
- local health score
- prefix-diversity metadata
- optional public key or stable identity key if the design adopts signed node
  records

The key design choice is whether node identity is still a 128-bit eMule-style
Kad ID, or whether `kad-ng` derives a larger routing ID from a signed identity.

Conservative option:

- keep a 128-bit routing ID for eMule compatibility and simpler migration
- keep endpoint proofs local and unsigned

Deeper option:

- introduce a signed node record
- derive the routing ID from the public identity key
- bind endpoint advertisements to signed records plus short-lived reachability
  proofs

The deeper option improves Sybil resistance only slightly by itself because
identities remain cheap. Its real value is preventing endpoint and capability
spoofing, enabling signed mutable records, and simplifying migration across
addresses.

### Capability Negotiation

`kad-ng` should use explicit capability negotiation from the first hello.

Capabilities might include:

- IPv4 endpoint support
- IPv6 endpoint support
- token-backed publish
- encrypted packet envelope
- signed node records
- source announce records
- mutable metadata records
- relay/rendezvous assistance
- compact batch lookup responses
- privacy-preserving search mode

Unknown capabilities must be ignored. Required capabilities must be explicit.
The extension model should use bounded TLV or another structured encoding with
test vectors.

### Endpoint Proofs

Modern Kad should not accept durable routing or publish claims from unverified
endpoints.

Recommended proof model:

- stateless challenge cookies bound to source endpoint, node ID, operation,
  and time window
- proof required before routing-table promotion
- stronger proof required before source publish acceptance
- separate proof state for each endpoint family
- short proof lifetime for publish rights
- longer but decaying proof lifetime for routing liveness

This is similar to secure DHT token ideas used elsewhere, adapted to eMule's
source and keyword publish model.

### Publish Tokens

`kad-ng` should require publish tokens.

Flow:

1. publisher performs a lookup or announce-preflight near the target key
2. candidate storing nodes return short-lived publish tokens
3. publisher submits source, keyword, or note records with the token
4. storing node verifies token binding before accepting the record

Token binding should include:

- target key
- publisher endpoint
- operation family
- expiration time
- local secret epoch

This does not prove a file is legitimate, but it prevents blind/off-path
publishing and makes bulk poisoning more expensive.

### Record Types

Classic Kad mixes several eMule-specific record shapes. A parallel overlay can
make record types explicit.

Candidate record families:

- file source record: file hash, endpoint, ports, reachability flags, source
  type, optional buddy/rendezvous data
- keyword index record: normalized keyword, file hash, name evidence, size,
  type, AICH or stronger hash evidence where available
- note/comment record: file hash, rating/comment payload, language or metadata
  hints, size limits
- node record: signed or token-backed endpoint advertisement
- capability record: optional self-description, kept small and bounded

Every record type needs a maximum size, TTL, duplicate policy, and validation
rule.

### Search Model

`kad-ng` search should separate routing lookup from result aggregation.

Modern behavior:

- disjoint lookup paths for better resilience
- bounded parallelism
- convergence-based stop conditions
- deduplication by file hash and endpoint
- result provenance from each overlay
- local quality scoring that never becomes global trust
- optional privacy-preserving mode for sensitive keyword searches

Keyword search remains hard because the query itself is revealing. A modern
overlay can reduce unnecessary exposure but cannot make public DHT keyword
search private without major tradeoffs.

### Privacy Bounds

Privacy claims should be modest and explicit.

Reasonable improvements:

- encrypt or authenticate packets between upgraded peers where negotiation
  allows it
- reduce metadata leakage in diagnostic logs
- avoid publishing more endpoint data than needed
- support query pacing and disjoint paths to reduce single-observer visibility
- separate local UI trust hints from network-visible reputation

Unreasonable claims:

- anonymous downloads
- anonymous keyword search over a public DHT
- global spam immunity
- strong Sybil resistance without a real cost or trust model

### NAT And Reachability

`kad-ng` should treat reachability as a first-class state machine.

States:

- IPv4 UDP reachable
- IPv4 TCP reachable
- IPv6 UDP reachable
- IPv6 TCP reachable
- UDP-only
- relay/rendezvous-assisted
- unknown
- recently failed

Possible modern behaviors:

- use IPv6 direct reachability when available
- coordinate UPnP, PCP, and NAT-PMP outside the DHT record format
- allow rendezvous hints only as optional assistance
- avoid making relay behavior mandatory
- keep LowID compatibility separate from DHT routing identity

The design should help users escape LowID where possible without turning the
DHT into a general relay network.

### Abuse Resistance

`kad-ng` should assume identities are cheap.

Defenses should therefore be layered:

- endpoint proof before routing weight
- per-prefix diversity limits
- replacement caches
- token-backed publish
- adaptive rate limits
- local reputation only
- decay and quarantine for high-churn contacts
- disjoint lookup paths to reduce localized eclipse impact
- signed bootstrap snapshots
- strict parser limits

No single defense solves Sybil attacks. The practical goal is to raise the cost
of useful abuse while preserving open participation.

### Bootstrap And Migration

A parallel overlay needs a careful bootstrap path:

- keep classic Kad fully functional
- ship with no hard dependency on a central bootstrap service
- support signed bootstrap snapshots
- support cross-overlay hints only as hints
- persist `kad-ng` bootstrap state separately
- expose separate health counters
- allow user rollback by disabling the overlay without damaging classic Kad

Migration should be staged:

1. internal endpoint abstraction
2. diagnostics and bind selection
3. controlled `kad-ng` packet spec and fixtures
4. private testnet bootstrap
5. lookup and routing conformance tests
6. source publish and search fixtures
7. dual-overlay result aggregation
8. live opt-in preview
9. default-on only after evidence shows safety and value

### What Kad-NG Should Not Do

Avoid:

- pretending to be classic Kad while changing semantics
- mandatory global reputation
- centralized identity authority
- blockchain-style storage or consensus
- unbounded metadata records
- making relay traffic a default obligation
- changing eD2K file identity semantics
- treating AI or spam scoring as network truth
- making old peers second-class on the current public network

## Recommended Priority

For eMuleBB, the practical priority remains:

1. compatible parser, routing, and publish hardening
2. better Kad diagnostics and evidence traces
3. endpoint and address-family abstractions
4. signed/fresh bootstrap handling
5. IPv6-native parallel overlay design
6. publish-token design for the parallel overlay
7. opt-in `kad-ng` testnet

The deep design is worth writing down now, but it should not distract from the
safer compatible work that improves the current network immediately.

## Open Questions

- Should a modern overlay keep 128-bit routing IDs or derive a larger ID from a
  signed identity key?
- Should IPv6 Kad be a dedicated `kad6` overlay, or should `kad-ng` handle both
  IPv4 and IPv6 from the start?
- What record TTLs best match eMule source churn without increasing stale
  results?
- How much endpoint proof is enough before accepting a source publish?
- Can keyword search privacy be improved meaningfully without harming
  discoverability?
- Which metrics prove that adaptive lookup scheduling improves user outcomes
  rather than only reducing packet counts?
- What evidence threshold is required before an opt-in overlay becomes a
  supported release feature?
