# IDEA: Kad Publishing Pace And Cooperative Distributed Search

> **Exploratory design, captured 2026-10-03.** This is not an active
> implementation plan, release commitment, or statement of shipped behavior.
> Forward implementation would target **emulebb-rust**. Any slice that changes
> default scheduling or adds a compatible-client extension must be promoted to
> a separately reviewed active item with protocol-parity and live-network
> evidence.

## Purpose

The recent large-library startup work removed the barrier that delayed both
eD2K and Kad publication until a whole shared catalog had been materialized.
That improves when Kad publishing can begin, but it does not change the deeper
throughput limits of Kad publication or make the current public Kad search a
complete multi-term distributed-search implementation.

This note explores how to:

- improve time-to-first Kad visibility while retaining stock packet shapes
- make keyword publication cover a large library efficiently
- handle source publication honestly when the library is much larger than one
  node can keep fresh
- implement accurate distributed search using existing Kad request features
- turn passively observed Kad traffic into a durable local search index
- let explicitly compatible eMuleBB clients cooperate without disrupting stock
  eMule or aMule peers

The preferred design is compatibility-first: use the existing Kad protocol
well, add private local intelligence, and cooperate above Kad before considering
new public-network opcodes.

## Relationship To Existing Work

This idea builds on, but does not reopen, the completed startup fix documented
in
[RUST-BUG-106](../products/emulebb-rust/history/items/RUST-BUG-106.md). That
work established a bounded first publication cohort and progressive catalog
hydration. Its retained two-peer Kad evidence proves early scheduling and
connectivity, not full publish-acknowledgement depth.

Related current and exploratory material:

- [Kad/eD2K indexer design](../products/emulebb-rust/design/kad-ed2k-indexer.md)
  defines passive-first local indexing.
- [RUST-FEAT-002](../products/emulebb-rust/active/items/RUST-FEAT-002.md)
  owns the future autonomous Kad/eD2K FTS index.
- [RUST-FEAT-004](../products/emulebb-rust/active/items/RUST-FEAT-004.md)
  owns Torznab and the application-level federation surface.
- [RUST-BUG-104](../products/emulebb-rust/active/items/RUST-BUG-104.md)
  owns Kad AICH publisher provenance and consensus.
- [RUST-FEAT-040](../products/emulebb-rust/active/items/RUST-FEAT-040.md)
  owns end-to-end search metadata and provenance.
- [Kad protocol modernization](IDEA-KAD-PROTOCOL-MODERNIZATION.md) contains the
  broader compatible-Kad and parallel-overlay boundary.
- [Cooperative DHT cooperation](IDEA-COOPERATIVE-DHT-COOPERATION.md) contains
  analogous suite-level cooperation concepts, primarily from the BitTorrent
  side.

## Current Rust Baseline

The relevant implementation is intentionally close to stock eMule behavior.
Current code anchors are listed here so a later promotion can revalidate them
against `main` rather than treating this note as source truth.

### Publication Scheduling

`repos\emulebb-rust\crates\emulebb-core\src\lib.rs` currently defines:

- a two-second shared-file publication tick
- a 256-file scan window per tick
- one new keyword, source, and notes publication start per tick
- in-flight caps of three keyword, four source, and one notes operation
- one DHT traversal permit reserved beyond those eight publication operations
- a publication-class budget of two outgoing Kad packets per second
- up to 150 file entries in one keyword-target publication

`repos\emulebb-rust\crates\emulebb-core\src\kad_publish_schedule.rs` keeps the
stock-shaped intervals:

- keyword: 24 hours
- source: 5 hours
- notes: 24 hours

The default publication contact fanout is ten. Keyword entries are split into
stock-compatible packets of at most 50 entries per contact. A source publish is
different: one file hash is one DHT target and the stock source-publish request
does not batch unrelated file hashes.

### Publish Traversal

`repos\emulebb-rust\crates\emulebb-kad-dht\src\publish.rs` currently resolves
the closest contacts through a store traversal and then sends the publication
fanout. The search/traversal permit is retained through the publication helper's
return. This is simple and parity-oriented, but it couples these stages:

1. resolve the target neighborhood
2. send the first useful store packet
3. wait for all configured fanout results
4. free the traversal and per-kind in-flight capacity

That coupling increases time-to-first-visibility and makes slow durability
completion hold capacity that could prepare another target.

### Public Kad Search

`repos\emulebb-rust\crates\emulebb-core\src\kad_public_search.rs` currently:

- selects the first valid query word as the primary keyword
- hashes only that keyword to choose the DHT target
- sends an unrestricted keyword request at start position zero
- collects up to 200 unique hashes

The existing result-side filter only enforces extension, size bounds, and
minimum availability. It does not enforce every remaining query term or all
supported metadata fields for Kad results.

The protocol and local storage layers already understand more. A stock
`SEARCH_KEY_REQ` can carry:

- the high-bit marker indicating a restrictive expression
- a 15-bit start-position offset
- a Boolean/string/metatag/numeric restrictive expression

`repos\emulebb-rust\crates\emulebb-index\src\kad_search_expr.rs` already parses
and evaluates those expressions for the local Kad store. The missing part is
using the same stock request shape from the public search path and validating
remote responses with the same semantics.

### Passive Storage And Indexing

Valid inbound keyword, source, and notes publishes are accepted into the local
Kad store and persisted in the Kad publish cache. Passive replay workers also
reissue selected snooped requests and index a small number of returned keyword
results.

The accepted inbound keyword-publish path does not currently project every
valid filename/hash/size observation directly into the persistent FTS file
index. Closing that gap can improve search coverage without sending another
network packet.

## Capacity Model

The main architectural constraint is source publication, not keyword
publication.

### Source Publication

At the current start cadence, one source start every two seconds is an admission
ceiling of 1,800 files/hour. The packet budget is tighter when the default ten
contact fanout is included.

| Quantity | Optimistic value | Meaning |
|---|---:|---|
| Source starts admitted | 1,800/hour | Scheduler ceiling before completion pressure |
| Store-only throughput at 2 pps and fanout 10 | 720 files/hour | Excludes lookup packets, timeouts, and retries |
| First pass over 100,000 files | about 139 hours | About 5.8 days at the optimistic store-only ceiling |
| Records refreshable inside 5 hours | about 3,600 | Optimistic sustainable fresh-source set |
| Rate needed for 100,000 records per 5 hours | 5.56 files/second | Requires at least 55.6 store packets/second at fanout 10 |

The real figures are lower because lookup traffic shares the publication class,
not every contact responds promptly, and the four-operation source in-flight cap
can remain full.

Even allowing publication to consume the entire default global eight-packet
budget would give a store-only ceiling of 2,880 files/hour, or 14,400 source
records within five hours. Kad also needs that global capacity for interactive
search, maintenance, firewall/buddy work, and harvesting.

The resulting design conclusion is firm:

> One normal public Kad endpoint cannot continuously maintain fresh source
> records for a 100,000-file library under the current stock-shaped replication
> model. Concurrency tuning alone cannot change that.

### Keyword Publication

Keyword publication has much better leverage. One target can carry up to 150
file mappings. A full batch becomes three 50-entry packets per contact, or 30
store packets for ten contacts. At two publication packets/second, that is an
optimistic 15 seconds of store traffic for 150 searchable mappings, excluding
the lookup.

Keyword scheduling should therefore optimize mappings made searchable per unit
of network work. Common, high-coverage keywords are efficient. Rare terms are
important for recall but need fairness rather than first priority.

## Design Goals

1. Preserve stock Kad opcodes, field meanings, hashing, TTLs, and receiving-peer
   expectations by default.
2. Minimize time from a file entering the live catalog to its first useful
   keyword visibility.
3. Keep interactive searches responsive while background publication is busy.
4. Prefer high-yield keyword work without permanently starving rare terms.
5. Keep source advertisements truthful: only an endpoint that serves or relays
   a file may advertise itself as that source.
6. Use passive observations before spending active public-network traffic.
7. Preserve provenance, expiry, and independent-observer semantics across local
   and cooperative indexes.
8. Make large-library behavior explicit and measurable instead of claiming that
   a growing queue is equivalent to useful publication.

## Non-Goals

- Reducing the 5-hour source or 24-hour keyword intervals merely to inflate
  counters.
- Sending unknown or repurposed Kad UDP opcodes to stock peers.
- Treating a copied cooperative observation as an independent publisher vote.
- Allowing a non-serving cooperative node to masquerade as the source endpoint.
- Replacing ED2K file identity or weakening MD4/AICH verification boundaries.
- Making a new compatible-client mode the default without explicit promotion
  and live-network evidence.

## Lane A: Compatibility-Preserving Publisher

### Durable Work Queues

Replace repeated discovery of work from a bounded catalog scan with persisted,
bounded queues or priority indexes.

Maintain three logical queues:

- keyword targets, coalesced across all matching files
- individual source targets
- individual notes targets

The existing per-file/per-keyword publication clocks remain authoritative for
whether work is due. The queue is an efficient view of due work, not a second
truth source.

A useful publication state model is:

```text
due -> queued -> resolving -> visible-quorum -> replicating -> durable
                    |               |                |
                    +-> deferred <--+---- failed ----+
```

Keep separate timestamps for attempt, first acknowledgement, visibility quorum,
and durability completion. Do not silently redefine the stock-compatible
republish clock when adding these diagnostic states.

### Keyword Coverage Scoring

Represent due keyword work by keyword target, not by whichever file happens to
be visited first in the scan window. For each target, collect up to 150 due file
mappings and score the work approximately as:

```text
new or overdue mappings / estimated lookup-and-packet cost
```

Useful score inputs:

- never-published mappings before republish work
- number of due mappings that fit the next batch
- age of the oldest due mapping
- observed target/contact load
- recent failure and timeout history
- whether a nearby target was just resolved and can provide routing seeds

Use aging or deficit-round-robin fairness so low-yield rare keywords eventually
run. Keep existing keyword extraction and wire-visible term semantics unchanged
until a separate behavior item proves a better normalization policy.

### Source Priority And Large-Library Mode

For normal libraries, retain the stock-compatible default rotation. For a
separately promoted large-library mode, prioritize source records by current
value:

1. newly shared and never-attempted files
2. files selected from a recent local or federated search
3. files for which a download or source-resolution action is pending
4. files receiving recent upload demand
5. rare or low-observed-availability files
6. background rotation with age-based fairness

A 100,000-file library cannot keep every source record alive, so the mode must
admit that it maintains a hot set. It should report hot-set size, coverage, and
oldest queued age rather than presenting a never-ending full-library pass as
freshness.

### Two-Stage Publication

Split user-visible publication progress into two goals:

1. **Visibility quorum:** send to the closest small initial set and receive a
   bounded acknowledgement quorum.
2. **Durability fill:** complete the configured fanout through a background
   replication queue.

This does not reduce the eventual fanout. It lets the client declare that a
target is minimally searchable before every slow or failed contact finishes.
The durability queue must remain bounded and must not allow a fast producer to
create an unbounded packet backlog.

Potential implementation refinements:

- stream stores to contacts once their membership in the stable closest set is
  sufficiently certain
- decouple traversal permits from post-lookup store acknowledgement tracking
- prioritize the closest contacts first
- retain explicit target ownership until durability or bounded timeout so
  duplicate work does not race
- retry only the missing durability portion rather than repeating successful
  contacts

The exact initial quorum is a promotion-time decision. Three attempts with two
acknowledgements is a plausible experiment, not a decision in this note.

### Routing Seed Reuse And Locality

Cache recently successful contact sets as bounded, expiring routing seeds.
They should accelerate a new stock lookup, not permanently replace lookup and
closest-node convergence.

For source hashes and keyword targets:

- sort or bucket queued targets by XOR-prefix locality
- process a small burst from one neighborhood before rotating
- seed each traversal with recently responsive nearby contacts
- fall back to the routing table immediately when cached seeds are stale or
  fail
- never treat a previously closest contact as indefinitely authoritative

This should reduce lookup work for adjacent targets without changing a packet
seen by remote clients.

### Adaptive Packet Budget

Keep the conservative publication budget as the floor. Permit publication to
borrow otherwise unused global capacity only when all of these are healthy:

- no queued interactive search
- verified UDP reachability
- stable response latency
- high acknowledgement ratio
- low timeout and retry rate
- acceptable remote publish load
- no inbound or outbound flood-control escalation

Use additive increase and multiplicative decrease. A timeout burst, load spike,
or interactive request should reduce publication capacity immediately.

Interactive and maintenance work need hard reservations, not merely a total
semaphore size that background harvesting can also consume. Publication may
borrow idle capacity but may not reserve it ahead of interactive demand.

Adaptive rate control improves ordinary catalogs and time-to-quorum. It does
not make the 100,000-source freshness target feasible from one node.

## Lane B: Proper Distributed Kad Search

### Query Planning

For a multi-term query, choose one significant term as the Kad target and put
the remaining conditions into the existing restrictive expression.

Instead of always choosing the first word:

- estimate document frequency from the local FTS index and recent Kad evidence
- choose the rarest valid significant term as the primary target
- if no estimate exists, use a deterministic heuristic such as the longest
  significant term
- retain the current first-word path as a compatibility fallback while the new
  planner is opt-in or being validated

For a synthetic query such as `alpha beta`, if `beta` is rarer, hash `beta` for
the DHT target and require `alpha` in the restrictive payload. Files are already
published under their significant keywords, so this changes query planning, not
the Kad protocol.

### Stock Restrictive Expressions

Build the existing Kad search expression for:

- all non-primary query terms
- quoted terms where supported by stock semantics
- file type
- extension
- minimum and maximum size
- minimum availability and complete sources where represented
- bitrate and duration
- codec, title, album, and artist where the published tags support them

Set the restrictive-expression marker in `start_position` and send the normal
`SEARCH_KEY_REQ`. Evaluate the same expression against returned raw names and
tags before converting them into the public result model. This protects against
nonconforming or poisoned responses and keeps sender- and receiver-side
semantics aligned.

### Demand-Driven Pagination

Use the existing start-position offset to request later pages when the first
page is insufficient.

Stop paging when one of these is true:

- the requested unique-result target has been reached
- a page adds no new hashes
- responders return fewer entries than a full page
- the search deadline or packet budget is exhausted
- the operator cancels the search

Do not page every popular keyword automatically. Rarest-term planning and the
restrictive expression should reduce the need first.

### Correct Concurrency And Coalescing

The current streaming search path collapses a busy semaphore and a duplicate
target into the same empty-stream result. This is not sufficient for a public
search surface.

Distinguish:

- **identical request already running:** attach the caller to the result stream
  or completed short-lived cache
- **same target, different expression or page:** share the lookup frontier if
  practical, but keep separate result predicates
- **temporarily busy:** queue with interactive priority and a bounded deadline,
  or return an honest busy state
- **closed/stopping:** return an explicit unavailable state

The complete search identity includes target, restrictive payload,
start-position page, search family, and relevant result limit. Target alone is
not enough to decide that two searches are duplicates.

### Result Merge And Provenance

Merge primarily by ED2K hash, but preserve observations rather than flattening
them immediately.

For each observation retain:

- source network and mechanism: local share, ED2K server, Kad store, Kad search,
  passive replay, or cooperative peer
- responding Kad contact where appropriate
- publisher identity or publisher address evidence where valid
- name, size, type, media tags, source counts, and AICH candidate
- first-seen, last-seen, and expiry times
- whether the record was observed directly or received through cooperation

Merge rules should:

- require size consistency for one hash and surface conflicts
- retain alternate names with independent provenance
- avoid summing duplicated source counts from different result routes
- decay availability instead of preserving a peak forever
- count only independent original observations toward AICH or publisher
  consensus
- never treat a cooperative replica as another network vote

### Source Resolution

Keyword search should discover files without immediately launching a source
lookup for every result. Run source resolution for:

- results visible in the current shortlist
- a result selected for download
- an explicit operator request for more availability
- a cooperative result whose source evidence is stale

For a locally shared file returned through a cooperative search, the owning
client can schedule an immediate normal stock source publication before or in
parallel with source resolution. This is publish-on-demand, not a delegated
source identity.

### Hybrid User Search

Add an explicit `federated` or `hybrid` method rather than silently changing the
existing parity-oriented `automatic` selection at first.

```text
local FTS
   + ED2K connected/global search
   + Kad restrictive search
   + compatible-peer indexes
   -> provenance-aware merge by ED2K hash
```

The local index should return immediately. Network sources can enrich the same
logical search asynchronously. The user-visible status must distinguish local
completion, Kad progress, ED2K progress, compatible-peer progress, and partial
failure.

## Lane C: Passive-First Search Index

### Direct Projection From Accepted Publishes

When a keyword publish passes the normal firewall, tolerance, structural,
capacity, and anti-spam checks, project its filename/hash/size/tag observation
into the persistent file index in the same accepted-packet path.

Source publishes should update expiring availability evidence. Notes publishes
should update bounded note/rating observations. None of these observations
should bypass the local Kad store's validity decision.

This produces useful index growth from traffic the node already receives. It is
the cheapest search improvement available because it adds no active query.

### Expiry And Storage Model

The FTS view must not turn transient Kad records into permanent facts.

Recommended logical tables or equivalent normalized state:

- files keyed by ED2K hash with stable merged display fields
- file observations with origin, original observer, and expiry
- keyword observations with target and expiry
- source observations with endpoint and five-hour freshness
- AICH candidates keyed by independent publisher/observer
- alternate names and metadata conflicts

FTS rows can remain materialized for search, but ranking and result presentation
should use the freshness and provenance tables. Expired data may remain as
historical local evidence only if it is clearly excluded from current
availability claims.

### Passive Replay

Keep passive replay demand-ranked and rate-limited:

- replay popular observed keyword requests to deepen coverage
- replay source requests only when source freshness is useful
- coalesce replay with an identical interactive request
- let interactive work consume the result of an in-progress replay
- avoid a dedicated full-file-hash source sweep

The replay scheduler and publication scheduler should share one priority-aware
public-network budget rather than independently believing that spare capacity
exists.

## Lane D: Compatible-Client Cooperation

### First Choice: Application-Level Federation

The recommended compatible-client design does not modify public Kad. Explicitly
paired eMuleBB instances communicate through an authenticated application
channel such as HTTPS, a narrow federation API, or the planned Torznab surface.

Each member keeps:

- its own stable normal Kad node ID
- its own routing table and public Kad socket
- its own local Kad store and provenance-aware FTS index
- its own serving/source identity

Distinct normal Kad IDs naturally place members in different areas of the XOR
keyspace. Each node passively receives publishes and searches near its own ID,
so pooling their indexes provides broader coverage than duplicating one node's
active crawl.

### Membership And Trust

Start with explicit operator-managed pairing:

- mutual TLS or a pinned community/member key
- a stable federation member ID distinct from the Kad node ID
- bounded request and response sizes
- nonces and replay protection
- per-member quotas and audit counters
- no shared private filesystem paths or local profile data

Public-DHT rendezvous and automatic trust-set discovery can be considered later.
They add poisoning and membership-abuse problems before the core search value is
proven.

### Distributed Query Execution

For a small cooperative group, fan a query to each member's local FTS index and
merge the responses. For a larger group:

1. derive the normal Kad keyword target
2. rank cooperative members by XOR distance between their stable Kad ID and the
   target, then by health/load
3. send the active public-Kad query to one selected executor, with one or two
   replicas for failover
4. let all members query the resulting cooperative cache
5. coalesce identical active searches across the group

A member close to the target is likely to have stronger passive observations
for that region and useful nearby contacts. This is an optimization, not a new
claim of DHT authority.

An alternative assignment mechanism is rendezvous hashing over the cooperative
member set. It gives stable ownership during membership changes. A promoted
design could combine stable rendezvous ownership with XOR-distance preference.

### Observation Exchange

Exchange bounded signed observation batches, not flattened final truth. A
record should carry at least:

```text
record_id
file_hash
name and size observation
metadata tags or normalized fields
observed_via
original observer/publisher provenance
first_seen and last_seen
expires_at
sender member id
signature or authenticated-channel binding
```

The receiver must distinguish:

- direct local network observation
- direct observation reported by another trusted member
- a replicated copy forwarded by another member

Only the first two can add independent evidence, and only when their original
provenance is distinct. Forwarding the same record through five members must
not create five votes.

### Cooperative Work Partitioning

Compatible clients can divide expensive search and replay work safely:

- one owner replays a popular keyword target
- replicas take over after owner expiry or failure
- passive observations are routed to the target's cooperative owners
- query caches use Kad-aligned expiry and bounded negative caching
- document-frequency sketches can be shared to improve rarest-term planning

This reduces duplicate public-DHT traffic while increasing total keyspace
coverage.

### Publication Cooperation Boundary

Search/index work and source publication have different trust constraints.

Inbound Kad source storage derives the advertised source address from the UDP
sender. A cooperative helper therefore must not source-publish on behalf of a
different endpoint unless it genuinely serves or relays the file.

Safe models:

- **Publish-on-demand:** the search coordinator asks the actual owner to emit a
  normal stock source publish for a selected file.
- **Real serving partition:** multiple reachable eMuleBB instances divide a
  shared library, and each assigned instance actually serves the files it
  advertises.
- **Real replication:** multiple instances possess and serve a file; each may
  advertise itself independently.
- **Explicit relay:** a helper may advertise itself only if it implements the
  necessary callback/data relay and is genuinely a usable source endpoint.

Unsafe model:

- a metadata-only helper emits a source publish that causes receivers to store
  the helper's address even though it cannot provide the file

Keyword metadata delegation is less directly tied to data serving, but it still
changes publisher-diversity and anti-spam provenance. Keep keyword publication
owner-local initially; share the indexed observation through the authenticated
federation instead.

### Minimal Compatible-Client Extension

If application-level federation is insufficient, a later optional extension
could use an existing eD2K peer connection:

- advertise one ignorable capability in the compatible-client hello metadata
- send new framed search/result messages only after mutual capability
  confirmation
- authenticate the federation identity independently of the public Kad ID
- apply the same quotas, expiry, and provenance rules as the HTTPS design
- fall back completely to stock behavior when the peer lacks the capability

Do not begin with a custom Kad UDP opcode. Unknown UDP traffic can interact
poorly with stock parsing and flood controls, and it makes a private federation
indistinguishable from a public Kad fork.

## Security And Integrity Requirements

### Remote Kad Data

Treat every public-network record as untrusted:

- enforce packet, tag, string, expression-depth, and result-count limits
- validate filename and file-size consistency
- retain conflicting observations instead of accepting last-writer-wins
- decay and expire source availability
- keep AICH candidates tied to independent provenance
- do not infer content safety from popularity

### Cooperative Data

Trusted transport does not make the underlying Kad observation true. It only
identifies which member reported it.

- preserve original evidence and direct/replica status
- reject expired and malformed batches
- prevent replay with batch sequence/nonces
- limit observations per query and per member
- quarantine members producing structurally invalid or impossible claims
- make trust removal local and reversible

### Privacy

- never transmit local filesystem paths
- do not transmit unrelated library entries in response to a narrow query
- keep membership private by default
- minimize source endpoint sharing beyond what is already public or necessary
- log identifiers in a bounded, scrubbed form suitable for diagnostics

## Observability

Before changing default behavior, record enough information to prove where time
and capacity are going.

### Publishing Metrics

- due and queued targets by kind
- oldest and percentile queue age
- new mappings/files made visible per minute
- lookup duration and packets per target
- time to first store attempt, first acknowledgement, quorum, and durability
- attempted, acknowledged, timed-out, and rejected contacts
- remote load distribution
- routing-seed cache hit and success rates
- rate-budget saturation and borrowed-capacity duration
- hot-set size and estimated source-freshness coverage

### Search Metrics

- local first-result latency
- complete local, ED2K, Kad, and federation durations
- chosen primary keyword and estimated document frequency
- restrictive versus unrestricted request count
- pages and unique results per page
- remotely rejected results after local expression validation
- duplicate/coalesced query count
- busy wait, timeout, and cancellation count
- shortlist-to-source-resolution conversion

### Cooperative Metrics

- local versus remote-index hits
- public Kad searches avoided through cooperative cache hits
- query owner and failover count
- observations sent, received, deduplicated, expired, and rejected
- direct versus replicated provenance counts
- member latency, error rate, quota use, and trust state

## Phased Promotion Path

Each phase should be independently promotable and reversible.

### Phase 0: Measurement

- add queue-age, time-to-first-ack, durability, and public-search busy metrics
- retain current scheduling and packets
- establish 10k- and 100k-file modeled/fixture baselines

### Phase 1: Search Correctness

- implement stock restrictive-expression encoding
- validate Kad results locally with the same expression
- distinguish busy from duplicate requests
- coalesce only identical requests
- add demand-driven pagination
- optionally evaluate rarest-term primary selection behind a feature flag

### Phase 2: Passive Index Completion

- project accepted inbound keyword publishes into the provenance-aware FTS
- attach source and notes observations with expiry
- preserve conflicts and original observation identity
- merge local-index and network results asynchronously

### Phase 3: Publisher Scheduling

- introduce durable due-work queues
- coalesce keyword targets and score mapping coverage
- add routing-seed reuse and XOR-prefix locality
- separate visibility quorum from durability completion
- prove bounded queues and interactive-search priority

### Phase 4: Optional Large-Library Mode

- add demand-ranked source hot-set publication
- allow measured adaptive publication-bandwidth borrowing
- expose explicit freshness coverage rather than full-library claims
- retain the stock-compatible scheduler as the default until evidence supports a
  policy change

### Phase 5: Application-Level Federation

- pair compatible clients explicitly
- query remote FTS indexes
- coalesce public Kad searches across members
- preserve signed/authenticated provenance and expiry
- add owner-directed publish-on-demand
- integrate with Torznab/Prowlarr only after the native federation semantics are
  stable

### Phase 6: Optional Peer Extension

- specify a capability-negotiated eD2K peer extension only if the application
  channel leaves a proven gap
- keep classic Kad UDP unchanged
- require mixed-client degradation and abuse tests before live use

## Validation Strategy

### Unit And Property Tests

- expression encoder/parser round trips for Boolean, string, metatag, 32-bit,
  and 64-bit numeric terms
- depth, size, malformed-expression, and unsupported-tag rejection
- primary-keyword planning determinism
- pagination termination and deduplication
- queue fairness, aging, and starvation bounds
- visibility/durability state transitions
- rate-controller increase, decrease, and interactive preemption
- provenance merge without synthetic independent votes

### Deterministic Local Integration

- multiple local Rust Kad nodes covering publication, restrictive search,
  pagination, timeouts, and partial fanout
- mixed compatible/non-compatible clients proving stock fallback
- search coalescing with same target/different expressions
- source publish-on-demand emitted only by the actual serving node
- federation member loss and replica takeover

### Compatibility Evidence

- golden packet fixtures for every request shape
- stock/community eMule and current aMule mixed-client checks where applicable
- proof that non-compatible peers receive only established Kad/eD2K packets
- byte-level confirmation that restrictive search uses the existing protocol
- load and flood-control evidence before raising any public-network rate

### Large-Library Evidence

Use the existing persisted Python harnesses in `repos\emulebb-build-tests` for
live soak/profile work. Required reports should distinguish:

- catalog availability
- publication starts
- first acknowledgement/quorum
- durable fanout completion
- searchable keyword mappings
- fresh source records
- user-visible search latency

Workers being active is not sufficient proof of useful Kad coverage.

## Rejected Shortcuts

- **Raise all caps globally:** creates backlog and public-network pressure
  without fixing source-record economics.
- **Lower source TTL/republish interval:** increases churn and reduces the chance
  that the queue can catch up.
- **Publish each source to only one contact permanently:** improves counters but
  damages availability and resilience.
- **Delegate source publishing to metadata-only helpers:** advertises the wrong
  network endpoint.
- **Overload filenames/tags with cooperation data:** pollutes the public index
  and creates parsing/poisoning ambiguity.
- **Use a well-known Kad keyword as a federation rendezvous:** exposes and
  pollutes membership while remaining easy to poison.
- **Add an unnegotiated Kad opcode:** risks stock-client flood and compatibility
  behavior.
- **Treat gossip copies as votes:** creates false popularity and invalid AICH
  consensus.

## Decisions For The Next Design Session

1. Is the immediate objective faster keyword discoverability, stronger source
   freshness, accurate search, or a specific weighted combination?
2. Should large-library source hot-set behavior be opt-in, automatically enabled
   above a threshold, or remain purely operator-configured?
3. What visibility quorum should be tested before durability fill continues in
   the background?
4. Should rarest-term Kad planning replace first-term planning, or begin behind
   an experimental search mode?
5. Should the first federation surface be a narrow native API, Torznab, or both
   over one shared internal query model?
6. Is manual member pairing sufficient for the intended deployments?
7. Must every shared file be continuously source-visible, or is searchable
   metadata plus publish-on-demand an acceptable large-library contract?
8. How many actual serving instances are expected in a cooperative deployment,
   and can they access disjoint or replicated portions of the library?
9. Which implementation slice should be promoted first: search correctness,
   passive FTS projection, publisher queueing, or federation?

## Recommended Starting Decision

The highest-return, lowest-risk order is:

1. correct stock restrictive search, pagination, coalescing, and busy handling
2. directly index accepted passive Kad publishes with provenance and expiry
3. coalesce and prioritize keyword-target publication
4. introduce time-to-visibility quorum and bounded durability fill
5. add demand-based source hot-set behavior for very large libraries
6. federate compatible clients through an authenticated application channel
7. consider a negotiated peer extension only after the no-Kad-change design is
   proven insufficient

This sequence improves what users can find before attempting to make one node
perform a source-publication workload the stock Kad economics cannot sustain.
