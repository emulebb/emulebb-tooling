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

- **31/100** coverage IDs with a proven `parity` verdict;
- **5/17** groups complete;
- **69/100** IDs explicitly `evidence-incomplete`;
- **0** recorded divergences, which makes no claim about uncovered IDs; and
- **21** classified protocol assets: 6 canonical, 11 support, 2 product-only,
  2 historical, and 0 duplicate.

Complete groups are:

- `server-session` - 4/4;
- `server-query-reply` - 9/9;
- `server-tcp-metadata` - 2/2;
- `server-udp-metadata` - 2/2; and
- `lowid-callbacks` - 4/4.

Partial covered groups are `client-udp` at 4/9, `peer-startup-profiles` at
3/11, `queue-upload-state` at 1/5, and `transfer-blocks` at 2/4. Every other
group is currently uncovered. Reproduce the authoritative report from
`repos/emulebb-build-tests` with:

```powershell
python scripts\validate-protocol-catalog.py --format text
```

The catalog embeds the exact receipt IDs and provenance for every admitted
claim. Detailed superseded checkpoints remain available in Git history rather
than accumulating in this active item.

## Completed Bounded Slice Awaiting Delivery: `client-udp.clear`

This is the only delivery slice in progress. It starts from the merged,
protected-main-green `client-udp.file-not-found` baseline and establishes the
explicit plaintext transport authority needed before encrypted client-UDP is
attempted. It must not broaden its claim to version negotiation, encryption,
or unsolicited handling.

- **Sole claim:** admit only `client-udp.clear`. V1, V2, V3, encrypted
  transport, and unsolicited replies remain independently measured catalog
  IDs. The campaign may use the already-supported V4 payload shape, but that
  fact cannot admit another V4 claim.
- **Selected clients:** exact committed emulebb Rust diagnostics revision
  `ae01da50` and emulebb MFC diagnostics-oracle revision `ac8c33f0` each act
  once as requester and once as responder in the same deterministic local
  campaign. Their only product-source changes expose the already-computed
  per-source `shouldCrypt` decision; packet behavior is unchanged.
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
  runner, or product compatibility controls. The live diagnostics were
  insufficient to prove the transport choice, so both clients now emit the
  existing per-source crypt decision in `udp_reask_source_registered`; no
  protocol behavior changed. Do not change ed2k-server or derive a verdict
  from public soak observations.
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

## Completed Slice Checkpoint

The `client-udp.clear` contract was bound on 2026-11-02 before code changes and
implemented on the single shared branch `feature/client-udp-clear-evidence`.
Granular pushed commits are:

- Rust `ae01da50` - expose the production UDP-reask crypt decision in the
  source-registration diagnostic;
- MFC `ac8c33f0` - expose the corresponding oracle decision;
- build-tests `13af840` - add the clear-only reducer, canonical runner route,
  hashed raw reducer-input artifact, independent re-reduction, registrar, and
  adversarial tests;
- build-tests `ddc7de5` - preserve legitimate prior scheduler skips while
  retaining strict contradictory crypt-registration and duplicate-packet
  rejection;
- build-tests `2720dc6` - register the independently validated receipt and
  advance the catalog; and
- tooling `ca754e7` - bind this contract before implementation.

The first real campaign correctly failed because MFC records an expected
`reask_window_not_open` scheduler observation before the controlled eligible
decision. The reducer had over-tightened uniqueness beyond the transport
boundary. The focused correction now selects the exact eligible scheduler
state while still counting every same-identity crypt registration and wire
attempt, and a regression test fixes that distinction.

The succeeding real bilateral campaign is immutable at
`output-root:artifacts/emulebb-rust-reask-cross-client/20261102T202501Z-emulebb-main-release-10912/emulebb-rust-reask-cross-client-result.json`:

- receipt ID `rust-mfc-client-udp-clear-20261102t202501z`;
- report SHA-256
  `c99c90d1ca3d83038f463f773d9b94078ff3b35a2668af88494a95d783ae24a7`;
- raw reducer-input SHA-256
  `594451a0c600638fc41516a9ff073ed31beb102e18ee4fbad3f8ab4af0c16e75`;
- Rust executable SHA-256
  `4effb2103108173782b9183682621529217a7e29d4bd09b2f7fa2bbd4385799f`;
- MFC executable SHA-256
  `36222d2e3aa9fb6c3ad0b2843a8290e5c49a2561b26d20af31ff6389248925ac`;
- both directions recorded `shouldCrypt=false`, plaintext/non-obfuscated
  request and ACK observations, byte-identical frames, and identical applied
  queue-rank/complete-source state; and
- the independent registrar hash-checked and re-reduced the raw records before
  producing the sole `client-udp.clear` claim.

The catalog validates at 31/100 overall and 4/9 for `client-udp`. No other
client-UDP ID is admitted. `ed2k-server` remains untouched and upstream-clean.

Final local gates at the exact pushed heads are green:

- Rust canonical `python tools/rust_quality_gate.py ci`, including policy,
  rustfmt, Clippy with warnings denied, diagnostics build, 29 WebUI unit tests,
  17 Playwright tests, fresh Debug and Release workspace builds, all workspace
  and doc tests, and three serialized VPN leak tests;
- MFC Release x64 diagnostics and Debug x64 app builds;
- build-tests full suite: 3313 passed, one POSIX-only skip, one configured
  deselection, plus a separately green protocol-catalog validator; and
- tooling strict docs publish check.

## Next Step

Open the coordinated Rust, MFC, build-tests, and tooling pull requests, monitor
every required workflow, merge while preserving the granular commits, verify
exact post-merge main workflows, and delete the shared feature branches locally
and remotely. Do not select the next catalog slice until that delivery is
complete.
