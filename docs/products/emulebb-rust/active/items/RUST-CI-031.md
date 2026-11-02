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

## Active Bounded Slice: `client-udp.queue-full`

This is the only implementation slice in progress. It starts from the merged,
protected-main-green `client-udp.v4` baseline and must not broaden its claim to
any other client-UDP variant.

- **Sole claim:** admit only `client-udp.queue-full`. Version negotiation,
  clear transport, the happy-path ACK, file-not-found, encryption, and
  unsolicited handling remain independently measured catalog IDs.
- **Selected clients:** the emulebb Rust diagnostics build and the emulebb MFC
  diagnostics oracle must each act once as requester and once as responder in
  the same deterministic local campaign.
- **Authority:** stock eMule `CClientUDPSocket::ProcessPacket` behavior for
  `OP_REASKFILEPING` and `OP_QUEUEFULL`, the downloader-side pending-request
  gate and `UDPReaskACK(0)` state transition, and the accepted
  `stock.client-udp.corpus` clear `c5 93` queue-full frame. A responder answers
  queue-full only when it still shares the requested file, cannot locate the
  sender in its upload waiting queue, has no same-IP ambiguity, and
  `waitingUserCount + 50 > queueSize`.
- **Deterministic start and stimulus:** establish the requester as a real V4
  queued download source and a real responder-side upload waiter, remove that
  exact waiter through the existing upload operation while retaining the
  requester's source registration, and arm an exact, one-shot,
  diagnostics-build-only queue-pressure prerequisite for the same file and UDP
  endpoint. Then wake the existing source through the canonical queued-source
  reask control so the ordinary scheduler emits one production
  `OP_REASKFILEPING`.
- **Proof obligation:** causally join fixture receipt, exact waiter removal,
  due scheduler decision, request send terminal, responder receive/decode,
  stock queue-full decision facts, one clear zero-payload `OP_QUEUEFULL`, reply
  send terminal, requester receive under a matching pending request, and final
  application to the same source. The final state must retain the source, set
  remote queue-full, set rank zero, count a received reply rather than a
  failure, clear the pending request, and schedule the next reask. No ACK,
  file-not-found, timeout, or unrelated packet may satisfy the claim.
- **Implementation boundary:** evolve the existing canonical
  `scripts/emulebb-rust-reask-cross-client.py` runner and its reducer into a
  scenario-aware client-UDP owner without compatibility aliases or a parallel
  runner. The narrow queue-pressure fixture may establish decision facts but
  must be authenticated, diagnostics-build-only, exact, expiring, one-shot,
  and incapable of injecting or directly applying a packet. MFC changes remain
  diagnostics/test control only. Do not change ed2k-server or derive a verdict
  from public-soak observations.
- **Green condition:** a real bilateral run produces one immutable receipt, an
  independent registrar re-derives the exact result and provenance, and the
  catalog admits exactly `client-udp.queue-full`. Coverage then becomes 29/100
  overall and 2/9 for the still-partial `client-udp` group. Every changed
  repository must pass its scoped full gate before coordinated pull requests
  are opened.

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
- `ed2k-server` remained untouched and upstream-clean throughout the completed
  slice against its CI-reviewed upstream pin `3742f9e4`. The latest fetched
  upstream now has one newer commit, `97f97ff`; updating that reviewed pin is a
  separate upstream-sync delivery and is not mixed into this evidence receipt.

## Active Slice Checkpoint

The `client-udp.queue-full` contract was bound on 2026-11-02 before code
changes. All participating repositories started clean from protected `main` on
the single shared branch `feature/client-udp-queue-full-evidence`:

- Rust `00f723080448d77e2d5e2630a78a0702580a1507`;
- MFC `6806e9d73c3b3338bccfa4f560403f8df94cd8d0`;
- build-tests `74da5c164e1d3a8fd76560c9c50e0bcb1283c0a2`; and
- tooling `4042e685ff5acb0980e75a1099c9c9381632807c`.

Source review confirms that both clients already implement the stock decision,
clear `OP_QUEUEFULL` frame, correlated pending-reply gate, rank-zero update,
remote-queue-full state, and next-reask scheduling. Both also expose ordinary
upload-waiter removal. The missing capability is only a narrow deterministic
way to create near-full queue decision facts without launching at least 1,951
network clients against the production minimum queue size of 2,000. The active
implementation therefore adds the exact expiring one-shot prerequisite defined
above, extends causal diagnostics where the existing stream cannot prove its
consumption, and then generalizes the current V4-only reducer into the one
canonical client-UDP scenario reducer.

The bounded implementation and real proof are now complete on the shared branch:

- Rust commits `05e9e70d`, `dfd1a472`, `ac6fc442`, and `c84632d9` implement the
  exact expiring prerequisite, expose the final queue-full application health,
  and keep its diagnostics-only opcode import feature-gated;
- MFC commits `638855a3`, `90587116`, and `b7abc28b` implement the matching
  diagnostics-only prerequisite and converged application diagnostics, with
  diagnostics Release x64, Debug x64, and plain Release x64 builds green;
- build-tests commits through `22448af` make the one canonical runner and
  registrar scenario-explicit, prove the bilateral causal chain, and admit only
  `client-udp.queue-full`; and
- the real local campaign at
  `output-root:artifacts/emulebb-rust-reask-cross-client/20261102T150409Z-emulebb-main-release-16096/emulebb-rust-reask-cross-client-result.json`
  passed with `publicTraffic=false` against Rust `ac6fc442` and MFC `b7abc28b`.

The independent registrar re-derived receipt
`rust-mfc-client-udp-queue-full-20261102t150409z` with artifact SHA-256
`d55e6455348e8cbf66db533fea7f26c591ad76091397113c92178a7c4ea508d1`.
Both directions recorded one real waiter removal with confirmed absence, one
exact consumed queue-pressure prerequisite, byte-identical V4 requests,
byte-identical clear zero-payload `c5 93` replies, no ACK or file-not-found
substitute, and matching healthy final state. Catalog validation is green at
29/100 overall and 2/9 for `client-udp`.

The final shared-branch gate matrix is green on 2026-11-02:

- Rust `quick` passed policy, 128 policy tests, formatting, full-workspace
  Clippy with warnings denied, the packet-diagnostics target, 29 WebUI unit
  tests, 17 browser tests, type checking, and the production WebUI build;
- Rust `ci-test` passed fresh debug and release workspace builds, the release
  packet-diagnostics build, the full workspace test and doctest sweep, and all
  three observed-egress VPN leak tests;
- build-tests passed the OpenAPI route-drift check and its full default suite
  with 3,285 passed, one skipped, and one explicitly deselected test;
- tooling passed public-presence, taxonomy, structure, roadmap, and strict
  MkDocs checks; and
- MFC passed diagnostics Release x64 (`20261102T144834Z`), Debug x64
  (`20261102T145000Z`), and plain Release x64 (`20261102T145020Z`) builds. The
  exact staged diagnostics binary was also exercised by the admitted bilateral
  campaign.

## Next Step

Commit and push this final checkpoint, verify all four shared-branch worktrees
are clean, and open the coordinated pull requests. Do not start another
protocol slice on this branch.
