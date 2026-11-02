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

- **30/100** coverage IDs with a proven `parity` verdict;
- **5/17** groups complete;
- **70/100** IDs explicitly `evidence-incomplete`;
- **0** recorded divergences, which makes no claim about uncovered IDs; and
- **21** classified protocol assets: 6 canonical, 11 support, 2 product-only,
  2 historical, and 0 duplicate.

Complete groups are:

- `server-session` - 4/4;
- `server-query-reply` - 9/9;
- `server-tcp-metadata` - 2/2;
- `server-udp-metadata` - 2/2; and
- `lowid-callbacks` - 4/4.

Partial covered groups are `client-udp` at 3/9, `peer-startup-profiles` at
3/11, `queue-upload-state` at 1/5, and `transfer-blocks` at 2/4. Every other
group is currently uncovered. Reproduce the authoritative report from
`repos/emulebb-build-tests` with:

```powershell
python scripts\validate-protocol-catalog.py --format text
```

The catalog embeds the exact receipt IDs and provenance for every admitted
claim. Detailed superseded checkpoints remain available in Git history rather
than accumulating in this active item.

## Active Bounded Slice: `client-udp.clear`

This is the only implementation slice in progress. It starts from the merged,
protected-main-green `client-udp.file-not-found` baseline and establishes the
explicit plaintext transport authority needed before encrypted client-UDP is
attempted. It must not broaden its claim to version negotiation, encryption,
or unsolicited handling.

- **Sole claim:** admit only `client-udp.clear`. V1, V2, V3, encrypted
  transport, and unsolicited replies remain independently measured catalog
  IDs. The campaign may use the already-supported V4 payload shape, but that
  fact cannot admit another V4 claim.
- **Selected clients:** the unchanged emulebb Rust diagnostics build and the
  unchanged emulebb MFC diagnostics oracle must each act once as requester and
  once as responder in the same deterministic local campaign.
- **Authority:** stock eMule client-UDP framing when crypt is not requested:
  one clear `OP_EMULEPROT` datagram containing `OP_REASKFILEPING`, followed by
  one clear `OP_REASKACK` reply. The exact bytes and plaintext classification
  in `stock.client-udp.corpus` remain the wire authority; the live clients must
  prove the same transport choice through their production send and receive
  paths.
- **Deterministic start and stimulus:** reuse the canonical bilateral queued
  source setup with the harness-owned shared fixture and a real responder-side
  upload waiter. Disable obfuscation through the existing ephemeral profile
  configuration for both clients, prove the registered source has no crypt
  capability/request/requirement, then wake the existing source through the
  canonical queued-source reask control so the ordinary scheduler emits one
  production request and consumes one production ACK.
- **Proof obligation:** causally join source registration, due scheduler
  decision, request send terminal, responder receive/decode, ACK send terminal,
  requester receive under the matching pending request, and queue-rank/state
  application in both directions. Request and reply diagnostics must report
  `obfuscated=false`; exact datagram bytes must begin with clear
  `OP_EMULEPROT` plus the expected opcode and match the decoded payload. No
  encrypted frame, queue-full, file-not-found, timeout, unrelated packet, or
  merely recorded fixture can satisfy the claim.
- **Implementation boundary:** add one explicit `clear` scenario to the
  existing canonical `scripts/emulebb-rust-reask-cross-client.py` runner,
  reducer, independent registrar, and catalog path. Reuse the existing real
  V4 queued-source campaign rather than adding packet injection, a second
  runner, or product compatibility controls. Rust and MFC source changes are
  out of scope unless the live diagnostics are insufficient to prove the
  transport choice. Do not change ed2k-server or derive a verdict from public
  soak observations.
- **Green condition:** a real bilateral run produces one immutable receipt,
  the independent registrar re-derives the exact result and provenance, and
  the catalog admits exactly `client-udp.clear`. The resulting measured state
  is 31/100 overall and 4/9 for the still-partial `client-udp` group. Every
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
- The completed `client-udp.file-not-found` slice is admitted by receipt
  `rust-mfc-client-udp-file-not-found-20261102t173926z`, artifact SHA-256
  `b420db82edd4f12a447e44a080c42166eda917ef9189e3d7e2f1133c0d92f808`.
  Rust PR #216, MFC PR #189, build-tests PR #89, and tooling PR #140 merged as
  main commits `99715671`, `2373b49b`, `cd9e4e27`, and `bab8fa13`; every exact
  post-merge workflow passed. Their shared branch was deleted locally and
  remotely before this slice was selected.
- Build-orchestration PR #21 merged as protected-main-green `ef13ef8b`: aMule
  3.0.1 at `02db0d7f` is now the frozen parity source, aMule HEAD is
  analysis-only, the obsolete tracing worktree is retired, and deterministic
  lanes resolve the current MFC oracle build. Its WIP branch was deleted before
  this slice was selected.
- `ed2k-server` remained untouched and upstream-clean throughout the completed
  slice against its CI-reviewed upstream pin `3742f9e4`. The latest fetched
  upstream now has one newer commit, `97f97ff`; updating that reviewed pin is a
  separate upstream-sync delivery and is not mixed into this evidence receipt.

## Active Slice Checkpoint

The `client-udp.clear` contract was bound on 2026-11-02 before harness code
changes. The participating build-tests and tooling repositories started clean
from protected `main` on the single shared branch
`feature/client-udp-clear-evidence`. Rust and MFC remain on their exact green
main revisions because this slice must first prove whether the existing
diagnostics are sufficient.

The implementation starts by separating the clear-transport verdict from the
already-admitted V4 payload-shape verdict. The canonical runner must emit one
new scenario schema, and the reducer and registrar must reject any artifact
that lacks bilateral plaintext request/reply wire evidence or attempts to admit
another client-UDP ID.

## Next Step

Implement the explicit `clear` scenario in the canonical runner, reducer, and
independent registrar; validate it with focused tests; build exact current-main
Rust and MFC diagnostics binaries; run the real bilateral campaign; and admit
only `client-udp.clear` if every causal and provenance gate passes. Do not open
pull requests before the immutable receipt, 31/100 catalog snapshot, and all
changed-repository gates are green.
