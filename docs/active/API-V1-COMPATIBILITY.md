# /api/v1 — One Capability-Gated Contract

Status: governance. Rewritten 2026-06-16 (capability model). **Supersedes the
prior "two divergent lineages" split** (2026-06-15): there is **one** `/api/v1`
contract; implementations differ by the **capabilities** they advertise, not by a
separate spec.

## Why one contract (not two)

The split model declared a frozen MFC spec and a forward rust spec with **no
interchangeability**. But we want the opposite: a single controller (TrackMuleBB)
that drives **both** eMuleBB MFC and emulebb-rust, with guaranteed alignment,
while emulebb-rust adds indexing endpoints the MFC will never implement. A
divergent-spec model cannot give that. A **capability-gated single contract** can:
the MFC is simply a **subset** that advertises fewer capabilities.

## The model

- **One canonical OpenAPI document.** emulebb-rust is the **superset / source of
  truth**; the MFC implements a subset of the same spec. The indexing endpoints
  live in this one spec, tagged as the `indexing.*` capability — the MFC just does
  not advertise them.
- **Per-operation capability tags.** Each operation carries
  `x-capability: <group.feature>` and `x-since: <contract-version>` extensions, so
  the spec itself records which capability (and since which version) each
  operation belongs to. Examples: `core.search`, `core.transfers`, `core.shared`,
  `core.kad`, `indexing.snoop`, `indexing.torznab`, `arr.qbit-compat`.
- **Runtime discovery.** Every implementation answers:
  ```json
  GET /api/v1/capabilities
  { "contractVersion": "1.2.0",
    "capabilities": ["core.search","core.transfers","core.shared","core.kad"] }
  ```
  - eMuleBB MFC returns `core.*` only (its frozen subset).
  - emulebb-rust returns `core.* + indexing.* + arr.*` (and grows additively).
- **The soft-frozen MFC includes `/capabilities` too (decision 2026-06-16).** The
  capabilities endpoint is a **contract-discovery primitive, not a product
  capability**, so it is allowed as contract maintenance under the MFC soft freeze.
  This is precisely what guarantees clean evolution: **every** core — frozen or
  forward — is discoverable the same way, so the controller never special-cases a
  product and new cores/capabilities slot in without touching it. (Tracked for the
  MFC as `FEAT-122`.)
- **Capability negotiation in the controller.** TrackMuleBB reads `/capabilities`
  on connect, builds a feature set, and **only calls operations whose capability
  is advertised**. The UI hides unsupported features (e.g. no indexer/Torznab tab
  for an MFC core). No `if (client == "mfc")` branching — behaviour is
  capability-driven.

## Versioning

- The contract is versioned as a **contract semver** (`contractVersion` /
  `x-contract-version`), independent of any product release tag.
- **Additive** endpoints/fields (e.g. new indexing operations) bump the **minor**;
  breaking changes bump the **major** with a documented migration.
- The MFC, frozen, advertises whatever it shipped (a stable subset at a pinned
  `contractVersion`); it never grows. emulebb-rust leads the version forward.
- Controllers target a **contract-version range + capabilities**, never a product
  tag, and degrade by capability.

## Alignment guarantee = conformance tests (not the spec alone)

The spec declares the contract; **CI conformance proves alignment**:

- **emulebb-rust** validates its live `/api/v1` responses against the **full**
  canonical OpenAPI (drift check in rust CI).
- **eMuleBB MFC** validates its live responses against the **subset it advertises**
  (only the operations for its `/capabilities`).
- **Subset invariant:** `capabilities(MFC) ⊆ capabilities(rust) ⊆ capabilities(spec)`.
- **Capabilities-endpoint contract:** every implementation must answer
  `/capabilities`, and every advertised capability must map to operations present
  and conformant.

Tooling: a property-based/contract validator against the OpenAPI (e.g.
Schemathesis, Dredd, or `openapi-core`), run per advertised capability. This
replaces the hand-maintained compatibility matrix.

## Implementation matrix (informational; the tests are authoritative)

| Capability group | eMuleBB MFC | emulebb-rust |
|---|---|---|
| `core.*` (search, transfers, shared, kad) | ✅ (frozen subset) | ✅ |
| `indexing.*` (autonomous Kad/eD2K index, Torznab) | — (never) | ✅ (additive) |
| `arr.qbit-compat` (qBittorrent-compatible download client) | adapter (frozen) | ✅ |
| Contract version | pinned (frozen) | leads (semver) |

Legend: ✅ advertised + conformant · — not advertised (controller hides it).

## Consequences

- **One controller suffices.** Because the MFC is just a low-capability `/api/v1`
  client, TrackMuleBB drives it for free via capability negotiation — so
  **aMuTorrent is deprecated** as a separate controller (see
  [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md) / [PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md)).
- emulebb-rust can add indexing (and future) capabilities **additively** without
  any obligation to the MFC and without breaking the controller.
- MFC support is **free fallout of the generic path**, not a feature investment —
  the MFC stays frozen.

## Next steps (tracked, not done here)

- [ ] Add `x-capability` + `x-since` to the canonical OpenAPI and a
      `GET /api/v1/capabilities` operation (emulebb-rust owns the spec).
- [ ] emulebb-rust CI: capability-aware conformance/drift check (extend the
      existing REST contract item).
- [ ] eMuleBB MFC: add `GET /api/v1/capabilities` (advertising its frozen `core.*`
      subset) under the soft freeze as contract maintenance, plus a conformance run
      against that subset. Tracked as `FEAT-122`.
- [ ] TrackMuleBB: capability negotiation + UI gating (see `TMBB-FEAT-*`).

Related: [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md),
[PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md),
[REST-API-CONTRACT](../rest/REST-API-CONTRACT.md),
`emulebb-rust/docs/rest/REST-API-OPENAPI.yaml` (canonical superset).
