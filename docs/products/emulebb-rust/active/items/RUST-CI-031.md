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

- **32/100** coverage IDs with a proven `parity` verdict;
- **5/17** groups complete;
- **68/100** IDs explicitly `evidence-incomplete`;
- **0** recorded divergences, which makes no claim about uncovered IDs; and
- **21** classified protocol assets: 6 canonical, 11 support, 2 product-only,
  2 historical, and 0 duplicate.

Complete groups are:

- `server-session` - 4/4;
- `server-query-reply` - 9/9;
- `server-tcp-metadata` - 2/2;
- `server-udp-metadata` - 2/2; and
- `lowid-callbacks` - 4/4.

Partial covered groups are `client-udp` at 5/9, `peer-startup-profiles` at
3/11, `queue-upload-state` at 1/5, and `transfer-blocks` at 2/4. Every other
group is currently uncovered. Reproduce the authoritative report from
`repos/emulebb-build-tests` with:

```powershell
python scripts\validate-protocol-catalog.py --format text
```

The catalog embeds the exact receipt IDs and provenance for every admitted
claim. Detailed superseded checkpoints remain available in Git history rather
than accumulating in this active item.

## Active Bounded Slice: `client-udp.encrypted`

This is the only delivery slice in progress. It starts from the merged,
protected-main-green `client-udp.clear` authority and proves the complementary
production obfuscated transport. It must not broaden its claim to UDP payload
version negotiation, unsolicited handling, or peer-TCP obfuscation.

- **Sole claim:** admit only `client-udp.encrypted`. V1, V2, V3, and unsolicited
  replies remain independently measured catalog IDs. The campaign reuses the
  already-proven V4 request and ACK payload shape but cannot admit another
  version claim.
- **Selected clients:** exact protected-main emulebb Rust revision `fb673418`
  and emulebb MFC diagnostics-oracle revision `367747a1` each act once as
  requester and once as responder in the same deterministic local campaign.
  MFC revision `367747a1` is the diagnostics-only correction over protected-main
  `0faeaa3c` required after the first real run proved that the oracle recorded a
  receive buffer after in-place decryption. Product-source changes remain out
  of scope unless another concrete diagnostic gap prevents proof; any such
  change must remain diagnostics-only.
- **Authority:** stock eMule client-UDP obfuscation keyed by the receiver user
  hash and sender public IPv4, with the stock eight-byte envelope around the
  clear `OP_EMULEPROT` frame. The encrypted datagram is intentionally
  randomized and therefore is not compared byte-for-byte across clients. The
  deobfuscated request and ACK must equal the already-proven clear V4 frames
  and decode to the same state transition.
- **Deterministic start and stimulus:** reuse the canonical bilateral queued
  source setup, harness-owned shared fixture, and real responder-side upload
  waiter. Enable the existing crypt preference in both ephemeral profiles;
  prove each client is HighID at its actual TEST-NET bind address and the
  registered source records `shouldCrypt=true`; then wake that exact source
  through the existing diagnostics control so the ordinary scheduler emits
  one production encrypted request and consumes one production encrypted ACK.
- **Proof obligation:** causally join source registration, due scheduler
  decision, request send terminal, responder decrypt/decode, ACK send terminal,
  requester decrypt under the matching pending request, and queue-rank/state
  application in both directions. Request and reply diagnostics must report
  `obfuscated=true`; each raw datagram must differ from its clear frame, add
  exactly the stock eight-byte overhead, and avoid a clear reserved protocol
  marker. The clear frames and decoded payloads must match across clients.
  Any contradictory plaintext packet, duplicate attempt, failed decryption,
  unsolicited reply, timeout, unrelated packet, or recorded-only fixture makes
  the evidence incomplete.
- **Implementation boundary:** add one explicit `encrypted` scenario to the
  existing canonical `scripts/emulebb-rust-reask-cross-client.py` runner,
  reducer, independent registrar, and catalog path. Make profile crypt mode a
  scenario-owned input and remove the obsolete synthetic-public-IP comment;
  the current hairpin topology already reports each client's actual TEST-NET
  bind address. Do not add packet injection, a second runner, compatibility
  controls, public-soak verdicts, or any ed2k-server change.
- **Green condition:** a real bilateral run has produced one immutable receipt,
  the independent registrar hash-checks and re-reduces the raw evidence, and
  the catalog admits exactly `client-udp.encrypted`. The expected measured
  state is now realized at 32/100 overall and 5/9 for the still-partial
  `client-udp` group.
  Every changed repository must pass its scoped full gate before coordinated
  pull requests are opened.

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

Coordinated pull requests were opened only after that complete local green
condition:

- Rust PR #217 at `ae01da50`: 15/15 checks and 2/2 head workflows green;
- MFC PR #190 at `ac8c33f0`: 8/8 checks and 4/4 head workflows green;
- build-tests PR #90 at `2720dc6`: 20/20 checks and 7/7 head workflows green;
  the macOS portability job was twice cancelled by the runner before setup
  with zero steps or logs, while its Windows and Linux peers passed, then the
  policy-permitted same-head retry passed; and
- tooling PR #141 at `4dc29c1`: 11/11 checks and 6/6 head workflows green.

All four heads are clean and mergeable. No protocol or evidence change was
made to obtain the green result.

Rust PR #217, MFC PR #190, and build-tests PR #90 were rebase-merged while
preserving their granular commits. Their exact protected-main revisions and
post-merge results are:

- Rust `fb673418fd42946f56893081c43494fc1172ed7a`: 2/2 workflows green;
- MFC `0faeaa3cb5807ca27805636cdad1cc86406b273f`: 2/2 workflows green; and
- build-tests `80c7e67b832e41480196fed9506936d76bac8dbd`: 4/4 workflows green.

Tooling PR #141 rebase-merged as
`151d83deaf9eaacb524e0e926ff301ebe3351360`; all 4/4 exact post-merge
workflows passed. The shared `feature/client-udp-clear-evidence` branches were
deleted locally and remotely, and every participating checkout was synchronized
to clean `main` before the encrypted slice was selected.

## Encrypted Slice Evidence Checkpoint

The canonical runner and independent registrar were extended on the single
shared branch `feature/client-udp-encrypted-evidence`. Granular pushed commits
are:

- build-tests `7488867` - add the explicit encrypted scenario, strict reducer,
  independent raw-evidence re-reduction, registration route, and adversarial
  tests;
- MFC `367747a1` - preserve the exact pre-decryption client-UDP wire datagram and
  classify user-hash obfuscation from the wire/decrypted length boundary;
- build-tests `79bfc10`, `b0a4a00`, and `c492408` - bind canonical clean builds
  to clean, unchanged product and orchestrator revisions; remove executable and
  source overrides from the authoritative runner; and require those causal
  receipts in the independent registrar;
- build `178ac00` - keep WSL server clean/build/stage operations in one
  filesystem view after the authoritative build exposed a deterministic DrvFS
  staging race;
- build-tests `317f48b` - run every campaign-owned Rust peer from the single
  clean-built diagnostics executable rather than retaining a hidden dependency
  on a separately staged regular binary; and
- build-tests `bd88344` - replace the earlier non-causal encrypted receipt with
  the first independently validated authoritative-build receipt;
- build-tests `9f39f81` - allow this build-owning runner to prepare retained
  report paths before the canonical MFC executable exists, while preserving the
  mandatory clean build, exact-path validation, and binary hash before launch;
  and
- build-tests `bcc0e76` - replace the superseded encrypted receipt with a fresh
  campaign from the corrected runner. Neither earlier receipt is retained as a
  legacy registration path.

The first real campaign was correctly retained as `evidence-incomplete` at
`output-root:artifacts/emulebb-rust-reask-cross-client/20261102T215244Z-emulebb-main-release-11536/emulebb-rust-reask-cross-client-result.json`,
SHA-256 `101ea92f68eca6a01947e9f918b4b47665864e2160176461dd3ae4950bd537aa`.
Both production transitions applied, but MFC's receive diagnostic took its raw
snapshot after `DecryptReceivedClient` had rewritten the encrypted region in
place and inferred transport from Kad-only verify keys. The result joined an
encrypted eight-byte header to a clear payload and could not prove in-flight
wire identity. No protocol behavior failed or changed.

MFC commit `367747a1` fixed only that oracle boundary. A succeeding bilateral run
proved the protocol claim, but its report merely combined staged executable
hashes with current repository HEADs and therefore did not causally prove which
source revision built each binary. That receipt was superseded rather than
grandfathered. A later causally bound campaign passed, but independent review
found that its runner still required an already-staged MFC executable before
reaching the clean build it owned. Build-tests `9f39f81` corrected that ordering
without introducing an alternate binary or build path, and the evidence was
rerun rather than grandfathered. The final authoritative campaign is immutable
at
`output-root:artifacts/emulebb-rust-reask-cross-client/20261102T223823Z-emulebb-main-release-7472/emulebb-rust-reask-cross-client-result.json`:

- receipt ID `rust-mfc-client-udp-encrypted-20261102t223823z`;
- report SHA-256
  `d7a35823b5e39a8d925ac6b3c7358348f6cdff7df832669aa1330d80d92c0471`;
- raw reducer-input SHA-256
  `61b173587bf5afc797c38ca17a5cd0f953eb8912075e896e809622bb4189e93e`;
- Rust executable SHA-256
  `5e96ab23ddb678e829e352b4549ce2d5f7a08d34b1171a63089851c07653ae3c`
  from protected-main `fb673418`;
- MFC executable SHA-256
  `7c08aa3461800d7924d751d0cd94d54e595c271a585b9c6fb65a777bbda7f299`
  from diagnostics revision `367747a1`;
- ed2k-server executable SHA-256
  `ffb5655198a882156627e0ff6d5d5a3a94ce02a423023f3b94f0bd8c00569886`
  from clean upstream-aligned source `d6a6dd67`;
- runner revision `9f39f81` and clean build-orchestrator revision `178ac00`;
- both directions recorded `shouldCrypt=true`, exact eight-byte stock
  obfuscation overhead, nonreserved odd markers, byte-identical sender/receiver
  ciphertext per datagram, identical decoded V4 request/ACK frames, and the same
  applied queue-rank/complete-source state; and
- the independent registrar hash-checked and re-reduced the raw records before
  producing the sole `client-udp.encrypted` claim.

The final pushed heads satisfy the local delivery gates:

- build-tests `bcc0e76`: full suite 3339 passed, 1 skipped, and 1 configured
  deselection; changed-file Ruff and the protocol-catalog validator pass at
  32/100 overall and 5/9 for `client-udp` with zero duplicate assets;
- MFC `367747a1`: exact Release diagnostics and Debug x64 app gates pass, and
  the retained bilateral campaign proves the diagnostics runtime path;
- build `178ac00`: the canonical hosted gate plus the changed build-client area
  passes 35 tests, and the real clean Release ed2k-server build passes with zero
  warnings. The repository-wide raw pytest command still exposes 12 unrelated
  failures already present outside this branch's server-staging scope;
- tooling: the strict documentation publication gate passes; and
- independent read-only review found no remaining material issue after the
  fresh campaign and receipt replacement.

Rust required no source change. `ed2k-server` was clean-built and hash-bound by
the canonical runner, while its repository remained untouched and
upstream-clean.

## Next Step

Open the coordinated MFC, build, build-tests, and tooling pull requests for this
complete encrypted client-UDP slice, monitor their required checks, merge only
when green while preserving granular commits, then delete the shared work-in-
progress branches and synchronize the participating checkouts. Rust and
`ed2k-server` have no source changes and must not receive empty delivery
branches.
