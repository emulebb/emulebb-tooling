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

- **27/100** coverage IDs with a proven `parity` verdict;
- **5/17** groups complete;
- **73/100** IDs explicitly `evidence-incomplete`;
- **0** recorded divergences, which makes no claim about uncovered IDs; and
- **21** classified protocol assets: 6 canonical, 11 support, 2 product-only,
  2 historical, and 0 duplicate.

Complete groups are:

- `server-session` - 4/4;
- `server-query-reply` - 9/9;
- `server-tcp-metadata` - 2/2;
- `server-udp-metadata` - 2/2; and
- `lowid-callbacks` - 4/4.

Partial covered groups are `peer-startup-profiles` at 3/11,
`queue-upload-state` at 1/5, and `transfer-blocks` at 2/4. Every other group is
currently uncovered. Reproduce the authoritative report from
`repos/emulebb-build-tests` with:

```powershell
python scripts\validate-protocol-catalog.py --format text
```

The catalog embeds the exact receipt IDs and provenance for every admitted
claim. Detailed superseded checkpoints remain available in Git history rather
than accumulating in this active item.

## Active Bounded Slice: `client-udp.v4`

This is the only implementation slice in progress.

- **Sole claim:** admit only `client-udp.v4`. The fixture's clear transport is
  a controlled start condition, not proof of `client-udp.clear`. Versions 1-3,
  encryption, queue-full, file-not-found, and unsolicited handling remain
  separate catalog IDs.
- **Selected clients:** the emulebb Rust diagnostics build and the emulebb MFC
  diagnostics oracle must each complete the same version-4 direct client-UDP
  reask transition under controlled local queue state.
- **Authority:** stock eMule `UDPReaskForDownload` and
  `ClientUDPSocket::ProcessPacket` behavior plus the accepted
  `stock.client-udp.corpus` record. The V4 request carries file hash, part
  status, and complete-source count; its ACK carries responder part status and
  queue rank.
- **Proof obligation:** join the exact queued source and V4 capability to the
  due scheduler decision, one production-originated `OP_REASKFILEPING`, its
  send terminal, the responder's exact receive/decode, one exact
  `OP_REASKACK`, and application of its part status and queue rank to the same
  source. Compare exact bytes and all version-gated fields against the stock
  corpus and between clients in one immutable run.
- **Implementation boundary:** extend the existing canonical
  `scripts/emulebb-rust-reask-cross-client.py` runner and production
  diagnostics only where causal evidence is missing. Replace the legacy
  log-string verdict with exact `diag_event_v2` evidence. Do not add a parallel
  runner, generic packet-injection API, public-soak claim, MFC product behavior,
  or ed2k-server protocol behavior.
- **Green condition:** an independent registrar validates one immutable receipt
  and admits exactly `client-udp.v4`; measured coverage becomes 28/100 while
  `client-udp` remains honestly partial at 1/9; every changed repository passes
  its scoped full gate.

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
- `ed2k-server` remained untouched and upstream-clean throughout the completed
  slice.

## Active Slice Checkpoint

The unmerged `client-udp.v4` workstream has reached the following bounded
checkpoint:

- Rust and MFC expose the same diagnostics-only control for waking one exact,
  already queued direct V4 source through each client's ordinary production
  scheduler and transport path;
- both controls reject ambiguous, LowID, pending, fallback, or
  identity-mismatched sources and do not create sources or inject packets;
- the harness owns one strict reducer that requires the complete bilateral
  request/ACK/application causal chain, exact packet bytes, exact identity and
  send-attempt joins, stock-corpus agreement, and matching normalized state;
- focused Rust, MFC, and harness tests for those checkpoints are green and the
  granular commits are pushed on the shared workstream branch; and
- no catalog claim has been admitted: the canonical runner is not yet
  bilateral, no immutable campaign receipt exists, and `client-udp.v4` remains
  `evidence-incomplete`.

## Next Step

Upgrade only the existing canonical
`scripts/emulebb-rust-reask-cross-client.py` runner to execute the two local
directions in one campaign: Rust requester to MFC responder, then MFC requester
to Rust responder. Drive each exact queued source once through the converged
diagnostics control, derive the verdict solely from the strict reducer, and
remove the legacy log-string verdict. Then execute the real campaign,
independently register its immutable receipt, admit only `client-udp.v4`, and
run every changed repository's complete scoped gate before opening coordinated
pull requests.
