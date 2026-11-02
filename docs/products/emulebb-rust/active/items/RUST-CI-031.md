---
id: RUST-CI-031
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/164
title: Consolidate deterministic eD2K and Kad protocol-parity testing
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, tests, harness, diagnostics, protocol, ed2k, kad, vpn, soak, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-24
source: 2026-10-24 operator request for long-running persisted eD2K and Kad parity diagnostics
---

> Workflow status is tracked in GitHub:
> https://github.com/emulebb/emulebb-rust/issues/164. This document is the
> durable engineering goal and progress record; the machine-readable catalog is
> the coverage authority.

# RUST-CI-031 - Consolidate deterministic eD2K and Kad protocol-parity testing

## Goal

Build one evidence-driven harness that determines and improves emulebb Rust
parity for the supported eD2K and Kad scope. Prove one bounded protocol variant
or state transition at a time with deterministic, causally joined evidence.
Consolidate scattered tests under canonical owners and retire or isolate legacy
MFC test paths after their unique coverage has a replacement.

This goal is complete only when:

- every supported catalog ID has one canonical deterministic owner and a
  causally proven verdict;
- every protocol test asset is classified as canonical coverage, shared
  support, duplicate, product-only coverage, or historical material;
- duplicate and retired MFC paths have been removed or isolated without losing
  unique states;
- exact build and executable provenance is enforced by immutable receipts; and
- the generated catalog report and complete harness validation are green.

Elapsed soak time, process success, emitted events, raw test count, trace
volume, or zero recorded divergences do not satisfy this goal. A parity or
divergence claim without complete comparable evidence is not a result.

## Governing Harness Policy

The [Harness And Live Policy](../../../../reference/HARNESS-LIVE-POLICY.md) is
the single durable policy for harness ownership, evidence semantics, client
roles, deterministic layers, public-network safety, persisted profiles, and
artifact handling. This item applies that policy; it does not create a second
policy or verdict model.

The policy fixes these roles:

- **emulebb Rust:** product under test;
- **emulebb MFC:** preferred observable runtime oracle, limited to diagnostics,
  deterministic test control, and buildability needed for oracle use;
- **stock eMule source and accepted goldens:** wire and state-machine intent;
- **frozen aMule 3.0.1 lane:** independent parity reference at an exact base and
  diagnostics-only patch revision;
- **aMule HEAD:** analysis and future interoperability only, never a current
  parity authority or gate;
- **ed2k-server:** upstream-clean deterministic dependency with no
  emulebb-specific protocol behavior; and
- **persisted public soak:** discovery and rare-state collection only, never a
  parity or release-certification authority.

The active common diagnostic envelope is `diag_event_v2`. Beta harness,
diagnostic, API, and configuration contracts may break together when that
produces the cleaner long-term design. No legacy schema readers, compatibility
aliases, or parallel verdict paths are retained.

## Evidence And Coverage Authority

`repos/emulebb-build-tests/manifests/protocol-parity-catalog.json` is the sole
machine-readable coverage authority. It records the supported variants,
starting state, stimulus, expected result, authorities, evidence layers,
canonical runner, build provenance, immutable receipts, and verdict. Named
campaigns select catalog entries; they do not define competing scope.

Use evidence in this order:

1. codec and transcript proof for exact bytes, fields, boundaries, and malformed
   variants;
2. deterministic local state-machine proof with controlled time and faults;
3. deterministic local cross-client proof, primarily Rust versus MFC; and
4. persisted public-network soak observations for discovery only.

The only verdicts are `parity`, `divergence`, `evidence-incomplete`,
`not-observed`, and `intentional-difference`. Missing, ambiguous, malformed,
dropped, or unattributable evidence is `evidence-incomplete`. An unexercised
transition is `not-observed`. Neither advances coverage.

Every implementation slice must bind, before code changes:

- exact catalog ID or IDs;
- protocol authority;
- deterministic starting state and stimulus;
- selected clients;
- required causal joins and expected result;
- canonical runner and implementation boundary; and
- focused and full green gates.

A slice is admitted only after a real deterministic run produces an immutable
receipt, an independent registrar validates its exact evidence and provenance,
the catalog records only the proven claim, and all changed repositories pass
their scoped gates.

## Current Measured State

The catalog currently validates at:

- **29/100** coverage IDs with a proven `parity` verdict;
- **5/17** groups complete;
- **71/100** IDs explicitly `evidence-incomplete`;
- **0** recorded divergences, which makes no claim about uncovered IDs; and
- **21** classified protocol assets: 6 canonical, 11 support, 2 product-only,
  2 historical, and 0 duplicate.

Complete groups are:

- `server-session` - 4/4;
- `server-query-reply` - 9/9;
- `server-tcp-metadata` - 2/2;
- `server-udp-metadata` - 2/2; and
- `lowid-callbacks` - 4/4.

Partial covered groups are `client-udp` at 2/9, `peer-startup-profiles` at
3/11, `queue-upload-state` at 1/5, and `transfer-blocks` at 2/4. Every other
group is currently uncovered. Reproduce the authoritative report from
`repos/emulebb-build-tests` with:

```powershell
python scripts\validate-protocol-catalog.py --format text
```

The catalog embeds the exact receipt IDs and provenance for every admitted
claim. Detailed superseded checkpoints remain available in Git history rather
than accumulating in this active item.

## Active Bounded Slice: `client-udp.file-not-found`

This is the only implementation slice in progress. It starts from the merged,
protected-main-green `client-udp.queue-full` baseline and must not broaden its
claim to any other client-UDP variant.

- **Sole claim:** admit only `client-udp.file-not-found`. Version negotiation,
  clear transport, the happy-path ACK, encryption, and unsolicited handling
  remain independently measured catalog IDs.
- **Selected clients:** the emulebb Rust diagnostics build and the emulebb MFC
  diagnostics oracle must each act once as requester and once as responder in
  the same deterministic local campaign.
- **Authority:** stock eMule `CClientUDPSocket::ProcessPacket` behavior for an
  `OP_REASKFILEPING` whose requested hash is absent from the responder's shared
  catalog, the matching clear zero-payload `OP_FILENOTFOUND` frame from
  `stock.client-udp.corpus`, and requester-side `UDPReaskFNF`: accept only a
  correlated pending reply, clear the pending request, dead-list the exact
  source for the stock 45-minute block, and remove it from the requested file.
- **Deterministic start and stimulus:** establish a real V4 queued download
  source and responder-side upload waiter while the harness-owned fixture is
  genuinely shared. Atomically move that fixture outside the responder's
  shared root, invoke the production shared-catalog reload, and prove the exact
  hash was present before withdrawal and absent afterwards. Then wake the
  existing source through the canonical queued-source reask control so the
  ordinary scheduler emits one production `OP_REASKFILEPING`.
- **Proof obligation:** causally join the exact withdrawal receipt, source
  registration, due scheduler decision, request send terminal, responder
  receive/decode, absent shared-catalog fact, one clear zero-payload
  `OP_FILENOTFOUND`, reply send terminal, requester receive under the matching
  pending request, reply application, `source_dead_listed` with the stock block
  duration, `source_dropped`, and final REST-visible absence of the exact
  source. No ACK, queue-full reply, source swap, timeout, unrelated packet, or
  merely recorded fixture can satisfy the claim.
- **Implementation boundary:** extend the existing canonical
  `scripts/emulebb-rust-reask-cross-client.py` runner, reducer, registrar, and
  catalog path with one explicit `file-not-found` scenario. Use the real
  shared catalog and harness-owned file movement; do not add packet injection
  or a file-not-found decision fixture. Rust protocol behavior already exists.
  MFC changes remain diagnostics-only convergence around its existing
  `UDPReaskFNF` path. Do not change ed2k-server or derive a verdict from public
  soak observations.
- **Green condition:** a real bilateral run produces one immutable receipt, an
  independent registrar re-derives the exact result and provenance, and the
  catalog admits exactly `client-udp.file-not-found`. Coverage then becomes
  30/100 overall and 3/9 for the still-partial `client-udp` group. Every
  changed repository must pass its scoped full gate before coordinated pull
  requests are opened.

## Delivery Discipline

Work one catalog slice at a time on one shared topic branch per participating
repository. Use granular commits and push every validated checkpoint. Do not
open coordinated pull requests until the entire slice is implemented, proven
by a real deterministic campaign, independently registered, and fully green.
After merge, delete the work-in-progress branches locally and remotely before
selecting the next slice.

Work outside the active boundary is permitted only when it directly blocks the
selected proof. Record the dependency, make the smallest sufficient repair,
and return to the same slice. General diagnostics, orchestration, storage, soak,
or cleanup work does not advance protocol coverage by itself.

## Delivered Foundation

- The canonical persisted Rust-versus-MFC discovery soak performs read-only
  hide.me full-tunnel preflight, requires VPN Guard Block on both P2P planes,
  keeps local control on loopback, imports a truly empty Rust profile once,
  reuses a valid nonempty profile, and preserves backup-first MFC overrides.
- The soak can run until explicitly stopped with exact process identities,
  restart-safe control, bounded evidence, writer-health enforcement, and
  graceful teardown. It remains discovery-only.
- Rust and MFC emit one strict, unredacted, bounded `diag_event_v2` stream with
  run/process identity, exact packet bytes, causal keys, sequence integrity,
  writer health, and explicit drops or faults. Packet-only or incomplete runs
  are rejected.
- The harness has one catalog, strict verdict semantics, immutable receipts,
  independent registration, classified test assets, and generated coverage
  reporting.
- The latest completed slice, `lowid.buddy-callback`, is registered by receipt
  `rust-mfc-transfer-20261102t084332z`. Coordinated Rust PR #213, MFC PR #185,
  build-tests PR #86, and tooling PR #137 merged with protected-main checks
  green; their shared workstream branches were deleted.
- The completed `client-udp.v4` slice is admitted by receipt
  `rust-mfc-client-udp-v4-20261102t123752z`. It advances only that ID; the
  remaining eight client-UDP IDs stay `evidence-incomplete`.
- Rust PR #214, MFC PR #186, build-tests PR #87, and tooling PR #138 merged the
  `client-udp.v4` slice with protected-main checks green. Its shared feature
  branches were deleted locally and remotely before this slice was selected.
- The completed `client-udp.queue-full` slice is admitted by receipt
  `rust-mfc-client-udp-queue-full-20261102t150409z`, artifact SHA-256
  `d55e6455348e8cbf66db533fea7f26c591ad76091397113c92178a7c4ea508d1`.
  Rust PR #215, MFC PR #188, build-tests PR #88, and tooling PR #139 merged
  with protected-main and post-merge checks green. Their shared branch was
  deleted locally and remotely before this slice was selected.
- `ed2k-server` remained untouched and upstream-clean throughout the completed
  slice against its CI-reviewed upstream pin `3742f9e4`. The latest fetched
  upstream now has one newer commit, `97f97ff`; updating that reviewed pin is a
  separate upstream-sync delivery and is not mixed into this evidence receipt.

## Active Slice Checkpoint

The `client-udp.file-not-found` contract was bound on 2026-11-02 before code
changes. All participating repositories started clean from protected `main` on
the single shared branch `feature/client-udp-file-not-found-evidence`. Granular
validated checkpoints are pushed at:

- Rust `056a91d0`: retain exact UDP FNF source identity and remove the exact
  source from both the runtime registry and persisted transfer model;
- MFC `be2a0f79`: trace FNF reply application, stock dead-list insertion, and
  source removal without changing protocol behavior;
- build-tests `6258a80`: run and independently register the bilateral real-file
  withdrawal scenario with exact causal joins; and
- tooling `b835d56`: bind the slice contract before implementation.

The first retained bilateral campaign proved that MFC sent the exact clear
zero-payload `OP_FILENOTFOUND` and Rust received and applied it, but exposed an
IP-only Rust source lookup that could not identify the correct source when an
address had multiple candidates. Rust checkpoint `38742ea6` fixed the lookup by
the exact TCP endpoint and learned user hash.

The second retained campaign then proved Rust's reply application,
`source_dead_listed` with the stock 2700-second block, and `source_dropped`, but
the exact source remained visible through REST because its persisted transfer
hint survived the protocol drop. Rust checkpoint `056a91d0` now removes that
exact persisted relation for both UDP and TCP/AICH file-not-found outcomes.
These failed campaigns are blocker evidence only; neither admits catalog
coverage.

## Next Step

Build the Rust diagnostics client from exact checkpoint `056a91d0`, rerun the
same bilateral deterministic campaign, and independently register the immutable
receipt only if both directions satisfy the full causal contract. Then admit
exactly `client-udp.file-not-found`, run every changed repository's scoped full
gate, and open coordinated pull requests only when the whole slice is green.
