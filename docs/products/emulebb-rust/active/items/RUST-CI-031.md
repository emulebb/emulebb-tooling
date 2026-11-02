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

- **28/100** coverage IDs with a proven `parity` verdict;
- **5/17** groups complete;
- **72/100** IDs explicitly `evidence-incomplete`;
- **0** recorded divergences, which makes no claim about uncovered IDs; and
- **21** classified protocol assets: 6 canonical, 11 support, 2 product-only,
  2 historical, and 0 duplicate.

Complete groups are:

- `server-session` - 4/4;
- `server-query-reply` - 9/9;
- `server-tcp-metadata` - 2/2;
- `server-udp-metadata` - 2/2; and
- `lowid-callbacks` - 4/4.

Partial covered groups are `client-udp` at 1/9, `peer-startup-profiles` at
3/11, `queue-upload-state` at 1/5, and `transfer-blocks` at 2/4. Every other
group is currently uncovered. Reproduce the authoritative report from
`repos/emulebb-build-tests` with:

```powershell
python scripts\validate-protocol-catalog.py --format text
```

The catalog embeds the exact receipt IDs and provenance for every admitted
claim. Detailed superseded checkpoints remain available in Git history rather
than accumulating in this active item.

## Active Bounded Slice: `client-udp.v4`

This is the only implementation slice in progress. Its implementation and
evidence admission are complete; branch-wide delivery validation and the
coordinated pull-request handoff remain.

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
- The current `client-udp.v4` slice is admitted by receipt
  `rust-mfc-client-udp-v4-20261102t123752z`. It advances only that ID; the
  remaining eight client-UDP IDs stay `evidence-incomplete`.
- `ed2k-server` remained untouched and upstream-clean throughout the completed
  slice against its CI-reviewed upstream pin `3742f9e4`. The latest fetched
  upstream now has one newer commit, `97f97ff`; updating that reviewed pin is a
  separate upstream-sync delivery and is not mixed into this evidence receipt.

## Active Slice Checkpoint

The unmerged `client-udp.v4` workstream has completed its bounded proof:

- the canonical runner executes both Rust-requester/MFC-responder and
  MFC-requester/Rust-responder directions in one deterministic local campaign,
  using real HighID publication, real production upload slots, ordinary
  scheduler and transport paths, and no public traffic;
- both directions emitted request bytes
  `c5907a95c62c0a406c3fd822ed7de2429f8f0100000100` and ACK bytes
  `c59100000100`, then applied the same part status, complete-source state, and
  queue rank through exact causal chains;
- the independent registrar rechecked raw bytes, causal order, application
  state, control semantics, HighID and slot preconditions, stock-corpus digest,
  source revisions, executable hashes, and immutable artifact location rather
  than trusting the campaign's `ok` field;
- tamper tests reject changed wire bytes, broken causal order, and changed
  source provenance;
- the obsolete 35-minute inverse log-string capture was removed after its only
  direction was subsumed by the bilateral canonical campaign; no compatibility
  shim remains; and
- the catalog admits only `client-udp.v4`, at 28/100 overall and 1/9 for the
  still-incomplete `client-udp` group.

The real evidence is:

- artifact:
  `C:\var\build\emulebb_out\artifacts\emulebb-rust-reask-cross-client\20261102T123752Z-emulebb-main-release-16288`;
- report SHA-256:
  `0cec92b67d903bfca9aa5e94ef8bb7161613a84217f4dca9fa0a55eeff26f290`;
- Rust source `938bce6cf18971e900cbb78a2c92f2dc585e1a3f`, executable
  `8ced5390b7739cf0b6649d5306f15fa05873d572a8ff4f700b7a86d6c5e25b34`;
- MFC source `64b531b67a4e7bfc8b567d00edaf7a60e49a250d`, executable
  `90e441b7f38c8558c4830d277f029ddeb5216b3590304f4c7f5e4880148194c3`;
  and
- runner revision `027cd63bdf543d3b28d59994624bc25ffe04ea8e`.

The proof exposed and fixed four product-significant Rust defects: modern MFC
HELLO UDP-version learning, one-part source completeness inference when stock
omits `OP_FILESTATUS`, protocol-source retention across a 29-minute reask, and
receive-before-reply diagnostic ordering. MFC changes remained limited to
diagnostic control and converged evidence naming. The pushed granular commits
are Rust `dda3b341`, `0675bd76`, `e6373e5c`, and `938bce6c`; MFC `56564044`
and `64b531b6`; and build-tests `1f2437a`, `d9c8df6`, `be28902`, `027cd63`,
`7be201a`, `057667d`, `52ad4c8`, `0a3d988`, and `301a7ef`.

The complete local delivery gate is green:

- Rust: 1,238 package tests passed; the diagnostics client build passed with
  zero warnings at
  `C:\var\build\emulebb_out\logs\builds\20261102T122933Z-build-clients`;
- MFC: diagnostics Release plus standard Debug and Release builds passed with
  zero warnings at build runs `20261102T122126Z`, `20261102T123515Z`, and
  `20261102T123532Z`;
- build-tests: 3,271 tests passed, one POSIX-only test skipped on Windows, and
  one intentionally deselected test; all 13 changed Python files pass Ruff;
  the catalog validation passes at 28/100;
- tooling: the strict docs publish gate passes; and
- every participating repository is clean, pushed, and on the sole shared
  `feature/client-udp-v4-evidence` branch. The server fork is clean on `master`,
  and its upstream-owned paths exactly match the reviewed pin.

## Next Step

Open coordinated Rust, MFC, build-tests, and tooling pull requests. Monitor the
exact PR heads and protected-main checks through completion. After merge, delete
the shared workstream branch locally and remotely. Select and bind the next
catalog slice separately; do not silently extend this receipt to any remaining
client-UDP variant.
