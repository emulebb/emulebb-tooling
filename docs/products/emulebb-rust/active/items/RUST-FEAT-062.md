---
id: RUST-FEAT-062
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/233
title: Persist Kad routing state in SQLite and keep met files import-only
status: OPEN
priority: Major
category: feature
labels: [rust, kad, sqlite, persistence, nodes-dat, server-met]
milestone: post-beta-polish
created: 2026-11-05
source: operator-approved profile continuity design 2026-11-05
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/233. This local document owns the durable engineering contract.

# RUST-FEAT-062 - Persist Kad routing state in SQLite and keep met files import-only

## Summary

Make SQLite the durable authority for accepted Kad routing contacts while the
bounded live routing table remains in memory. Treat `nodes.dat` and
`server.met` strictly as compatibility import formats: parse and validate the
payload, merge its logical records, and discard the source bytes. Neither file
is profile state and the daemon must never create, refresh, or restore it.

This replaces the current `nodes.dat` startup, explicit-import, and graceful-
shutdown persistence paths. It also formalizes the existing `server.met`
behavior, which already imports server rows into SQLite without retaining the
payload.

## Current State

Reviewed against product revision `7b295bda` after RUST-REF-017 merged. The
current schema is 54, with verified library content independent of downloads.
Kad snapshot persistence remains open work in this item.

- `server.met` URL import parses servers and merges them into the SQLite server
  repository. There is no canonical profile-local `server.met`.
- `nodes.dat` is currently both an interchange format and durable state. The
  daemon loads it at startup, explicit import writes it to the profile, and
  graceful shutdown replaces it with a bounded routing sample.
- The Kad routing table is bounded and memory-resident. Its contacts contain
  substantially more useful state than a basic endpoint, including verified
  status and UDP anti-spoofing key material.
- The beta persistence policy requires one exact current schema and explicitly
  forbids migrations, legacy reads, repair branches, and silent profile reset.
- The daemon's `discovery_bootstrap` path still seeds and loads a profile-local
  `nodes.dat`; core network control still writes it after import and shutdown.
  These are the remaining persistence paths to replace. Preserve the current
  accepted-contact count returned by a live import.

## Required Design

### Runtime and durable authorities

- The live Kad routing table remains the runtime authority while Kad is
  running. SQLite is its restart snapshot, not an unbounded observation log.
- Persist the routing table's accepted bounded contact set. A checkpoint must
  delete rows no longer represented by the accepted snapshot so stale contacts
  do not accumulate indefinitely.
- Keep open sockets, pending RPCs, searches, lookup queues, timers, retry
  scheduling, publish state, and other transient work in memory only.
- Restore usable, non-expired contacts from SQLite before Kad bootstrap begins.
  Configured bootstrap endpoints and built-in fallback seeds remain available
  when the durable set is empty or insufficient.
- Represent a bootstrap endpoint whose node identity is not yet learned as
  logical bootstrap data rather than fabricating a routing-table identity.

### SQLite contact semantics

The current schema must represent every field needed to restore the accepted
routing semantics without serializing a Rust struct or copying `nodes.dat`:

- Kad node ID when known;
- normalized IPv4 address and UDP/TCP ports;
- advertised Kad protocol version;
- UDP anti-spoofing key and the public IPv4 address to which it is bound;
- verified status;
- HELLO source UDP port, received-HELLO state, and requested-response-ACK state;
- observed UDP and TCP firewall flags;
- routing contact type and active probe type;
- bootstrap/import provenance where it affects bootstrap behavior;
- expiry, creation, last-seen, and last-type-change timestamps needed by the
  current routing policy.

The implementation may normalize this into more than one table, but it must
use typed columns and explicit constraints. It must not store an opaque
`nodes.dat` blob or a serialized in-memory contact as the durable model.

### Checkpoint lifecycle

- Mark the durable snapshot dirty when accepted routing contacts or their
  persistence-relevant metadata change.
- Coalesce dirty changes into periodic checkpoints every 15 minutes. A clean
  interval does no SQLite write. Explicit import and graceful shutdown are
  immediate checkpoints outside that periodic cadence.
- Checkpoint on graceful shutdown before the networking runtime is discarded.
- A successful explicit `nodes.dat` import commits its normalized logical
  contacts immediately, even if Kad is stopped. If Kad is running, merge the
  same normalized records into the live routing table.
- Use one transaction per checkpoint/import so readers see the previous or the
  complete new snapshot, never a partial contact set.
- A periodic write failure is visible in diagnostics and leaves the snapshot
  dirty for a bounded retry. A shutdown write failure is reported but must not
  resurrect a met-file fallback.

### Import and merge rules

- Keep the existing authenticated URL-import routes:
  `POST /api/v1/kad/operations/import-nodes-url` and
  `POST /api/v1/servers/operations/import-met-url`.
- Do not add unauthenticated, local-path, multipart-upload, or arbitrary raw-
  byte REST surfaces in this item.
- Apply existing payload-size, URL, parser, and contact/server validation before
  any durable mutation.
- Deduplicate Kad contacts by stable node identity and resolve endpoint
  collisions deterministically. Invalid or unusable records do not enter the
  durable snapshot.
- Merge without downgrading a stronger existing record. In particular, an
  import must not erase verified status, a usable learned UDP key and its bound
  address, a newer supported protocol version, or fresher runtime observations.
- Imported metadata may fill missing fields. Conflicting weaker imported state
  does not overwrite stronger live or durable state.
- `server.met` continues to merge normalized server rows through the existing
  server repository rules. The source bytes are discarded after parsing.

### No met-file persistence

- Remove profile-local `nodes.dat` reads and writes from daemon startup,
  explicit import, trusted discovery seeding, and shutdown.
- Trusted first-run discovery may download and parse a `nodes.dat` or
  `server.met` source, but it must commit only normalized logical rows and
  discard the bytes.
- Do not write `nodes.dat` or `server.met` as a cache, backup, export, recovery
  artifact, or compatibility fallback.
- Existing operator-owned met files are not deleted automatically. The daemon
  simply stops treating them as live profile state.

## Compatibility and Scope Constraints

- Evolve the checked-in current SQLite schema directly. This item provides no
  migration for profiles created by an older schema.
- The target process opens only the exact schema it was built for. Do not add
  legacy table probes, fallback reads, repair, or automatic profile reset.
- Keep verified library content, local-file identity, root membership, and
  download ownership established by RUST-REF-017 unchanged. This item owns only
  the Kad persistence boundary and met-file imports.
- Do not change Kad wire behavior, contact-admission policy, routing-table
  capacity, REST authentication, or server-selection policy except where the
  persistence boundary requires it.
- Do not turn the SQLite snapshot into the future autonomous observation index.
  RUST-FEAT-002 owns that separate logical domain.
- Do not add met-file export. If a diagnostic representation is later needed,
  it must be explicitly designed as a diagnostic artifact rather than profile
  authority.

## Acceptance Criteria

- [ ] A fresh current-schema profile can bootstrap, learn Kad contacts, stop,
      and restore its accepted routing snapshot from SQLite with no
      profile-local `nodes.dat`.
- [ ] The durable model retains the verification, UDP-key, endpoint, version,
      firewall/HELLO, routing classification, provenance, and freshness fields
      required to restore current routing behavior.
- [ ] Dirty state checkpoints after 15 minutes, clean state performs no write,
      and graceful shutdown checkpoints before discarding the runtime.
- [ ] Explicit `nodes.dat` URL import is durable immediately whether Kad is
      running or stopped.
- [ ] Import tests prove identity/endpoint deduplication and prove that weaker
      imported data cannot downgrade verified, UDP-key, version, or freshness
      state.
- [ ] Server and Kad imports retain their authenticated URL surfaces and parser
      limits while discarding the source payload.
- [ ] Startup, trusted seeding, explicit import, periodic checkpoint, and
      shutdown tests prove that neither `nodes.dat` nor `server.met` is written.
- [ ] An incompatible database still fails visibly under the exact-schema
      policy; no migration or met-file fallback is introduced.
- [ ] Existing Kad/server deterministic integration and WebUI smoke tests remain
      green with messages updated to describe import rather than file saving.

## Validation

- Focused metadata-store tests for the current schema, constraints, bounded
  snapshot replacement, and transaction rollback.
- Kad routing tests covering snapshot extraction/restoration, dirty tracking,
  expiry, and complete persistence-relevant field round trips.
- Import tests for every accepted `nodes.dat` layout, duplicate identities,
  endpoint conflicts, invalid records, and stronger-record preservation.
- Daemon lifecycle tests with a temporary profile proving SQLite-only startup,
  periodic checkpoint, graceful shutdown, and empty-profile trusted seeding.
- REST and WebUI tests for both authenticated URL imports and updated user-
  visible success text.
- A repository search and filesystem assertion proving no product path writes
  `nodes.dat` or `server.met`.

## Dependencies

This item is a prerequisite for RUST-FEAT-063. Semantic profile carry-forward
must transport logical Kad contacts and server rows rather than met files.
