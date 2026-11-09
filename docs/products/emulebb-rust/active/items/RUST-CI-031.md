---
id: RUST-CI-031
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/164
title: Consolidate deterministic eD2K and Kad protocol-parity testing
status: OPEN
priority: Major
category: ci
labels: [rust, tests, harness, diagnostics, protocol, ed2k, kad, vpn, soak, beta]
milestone: post-beta-compatibility
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

## Deferred Test-Quality Follow-ups

- Add parser round-trip, malformed-input, and state-transition property tests
  under the canonical codec or state-machine owner. Preserve fuzz findings as
  deterministic regression cases instead of depending on a later fuzz run.
- Use controlled time and explicit task-completion signals for async scenarios.
  Keep actual socket and OS watcher behavior in bounded integration lanes.
- Keep failures visible and retain their evidence; automatic reruns do not
  convert an unexplained failure into a valid proof.

These remain backlog work. The CI/CD parity cleanup does not expand production
protocol behavior or introduce a second harness or verdict model.

## Deferred Resume Checkpoint

This item is intentionally open but not in progress. Resume it after the Beta 3
workstream, with a review on or after 2026-12-01 so it is not forgotten. The
focused outcome is:

> Prove emulebb Rust parity for its explicitly supported eD2K and Kad behavior
> through one authoritative deterministic harness, one cataloged protocol state
> at a time, using causally joined Rust-versus-MFC evidence and independent
> stock/aMule authority. Public soaks discover states; they never prove parity.

On resume:

1. Restore the catalog's pinned support checkouts and rerun
   `python scripts\validate-protocol-catalog.py --format text`. At deferral the
   catalog contains 35 proven IDs out of 108, but local validation reports only
   an aMule HEAD analysis-checkout revision drift; do not update an authority
   pin merely to match incidental local checkout state.
2. Rerun only the cancelled macOS portability job from build-tests workflow run
   `41717413561`; every job that obtained a runner passed, while macOS was
   cancelled before executing a step.
3. Revalidate clean protected-main revisions Rust
   `3d313a7a4a475c2e6863a0e568267257fa267c35`, build-tests
   `a496d74b992cbd563a95d911e7e1c2e138891c4b`, and tooling
   `8b0a7dbfe3a12379ff4c1410108abe58fe21c947` against the then-current heads.
4. Select only `client-udp.unsolicited`, define its authority, deterministic
   starting state, stimulus, causal joins, and green condition, then create one
   shared topic branch for that bounded slice.

Do not expand the resumed work into general CI, storage, profile, hashing,
workspace, soak, or diagnostics improvements unless one directly blocks the
selected protocol proof. MFC remains a diagnostics oracle, `ed2k-server`
remains upstream-clean, and no process-success, packet-presence, trace-volume,
elapsed-soak, or zero-divergence observation can substitute for complete causal
evidence. Retain no legacy schema, compatibility shim, duplicate runner, or
parallel verdict path.

## Current Measured State

The catalog currently defines:

- **35/108** coverage IDs with a proven `parity` verdict;
- **5/20** groups complete;
- **73/108** IDs explicitly `evidence-incomplete`;
- **0** recorded divergences, which makes no claim about uncovered IDs; and
- **21** classified protocol assets: 6 canonical, 11 support, 2 product-only,
  2 historical, and 0 duplicate.

Complete groups are:

- `server-session` - 4/4;
- `server-query-reply` - 9/9;
- `server-tcp-metadata` - 2/2;
- `server-udp-metadata` - 2/2; and
- `lowid-callbacks` - 4/4.

Partial covered groups are `client-udp` at 8/9, `peer-startup-profiles` at
3/11, `queue-upload-state` at 1/5, and `transfer-blocks` at 2/4. Every other
group is currently uncovered. Reproduce the authoritative report from
`repos/emulebb-build-tests` with:

```powershell
python scripts\validate-protocol-catalog.py --format text
```

The 2026-11-04 protocol-state audit expanded the authority from 100 to 108 IDs
and from 17 to 20 groups before product changes. The new incomplete boundaries
cover cumulative legacy server publication, established-peer mutable controls
and buddy receive liveness, and Kad ingress admission before mutation. The
previous client-UDP V1 slice remains admitted at 35 proven IDs; the denominator
increase records newly explicit obligations rather than a coverage regression.

The catalog embeds the exact receipt IDs and provenance for every admitted
claim. Detailed superseded checkpoints remain available in Git history rather
than accumulating in this active item.

## Latest Delivered Slice: `client-udp.v1`

This was the final bounded slice before deferral. It started from the merged,
protected-main-green V2 authority and proved the independently negotiated V1
contract. It must not broaden its claim to unsolicited replies, transport
obfuscation, or any other client-UDP state.

- **Sole claim:** admit only `client-udp.v1`. V1 and V2 have the same request
  and ACK byte shapes, but one advertised-version result cannot stand in for
  the other catalog claim. `client-udp.unsolicited` remains independently
  incomplete.
- **Selected clients:** emulebb Rust and the emulebb MFC diagnostics oracle each
  act once as requester and once as responder in the same deterministic local
  campaign. The immutable receipt must bind their exact source revisions and
  executable hashes. Version selection remains diagnostics-only and normal
  builds continue to advertise V4.
- **Authority:** stock eMule `CUpDownClient::UDPReaskForDownload`,
  `CClientUDPSocket::ProcessPacket`, and `SupportsUDP`. V1 is a supported,
  nonzero UDP version but fails both the `> 2` and `> 3` optional-tail gates. A
  V1 request is exactly `OP_EMULEPROT`, `OP_REASKFILEPING`, and the 16-byte file
  hash. A V1 ACK is exactly `OP_EMULEPROT`, `OP_REASKACK`, and the two-byte queue
  rank. Neither frame has a complete-source count or part status.
- **Deterministic start and stimulus:** reuse the canonical bilateral queued
  source setup, harness-owned shared fixture, real responder-side upload
  waiter, and ordinary scheduler wake control. Both diagnostics clients
  advertise V1 naturally and register the opposite client as a real V1 source
  before the harness wakes that exact source once. Rust selects V1 with
  `EMULEBB_DIAGNOSTIC_CLIENT_UDP_VERSION=1`; MFC selects it with the existing
  diagnostics-only `--diagnostic-client-udp-version=1` argument.
- **Proof obligation:** causally join V1 source registration, due scheduler
  decision, request send terminal, responder decode, ACK send terminal,
  requester correlation under the matching pending request, and queue-rank
  application in both directions. Compare exact request and ACK bytes across
  clients; prove complete-source count and part status are both absent and the
  same queue rank is applied. A non-V1 registration, contradictory frame,
  duplicate attempt, unsolicited reply, timeout, unrelated packet, or missing
  causal join makes the evidence incomplete.
- **Implementation boundary:** extend only the existing canonical
  `scripts/emulebb-rust-reask-cross-client.py` runner, generic ACK reducer,
  independent registrar, and catalog path with one explicit `v1` scenario.
  Add explicit Rust codec tests for the exact V1 request and ACK. Do not change
  production behavior, MFC source, registered peer state, `ed2k-server`, or the
  public soak. Do not inject packets, create a second runner, add a compatibility
  shim, or infer a verdict from process success.
- **Green condition:** a real bilateral run produces one immutable receipt,
  the independent registrar hash-checks and re-reduces the raw evidence, and
  the catalog admits exactly `client-udp.v1`. The expected measured state is
  35/100 overall and 8/9 for the still-partial `client-udp` group. Every changed
  repository must pass its scoped full gate before coordinated pull requests
  are opened.

The V2 baseline reached protected `main` on 2026-11-03 as Rust PR #219 at
`6a399358e6fae9039e4d2251cfe8ed12362d226f`, build-tests PR #93 at
`64891dd2e87f7764e606f649d10374ee91bcf4c8`, and tooling PR #144 at
`1fae7d2ccebed61efa18c9d6a4abcc1764392bef`; every exact post-merge workflow
passed and the shared V2 branches were removed locally and remotely. The
catalog validates at 34/100 overall and 7/9 for `client-udp` before this slice.

The V1 stock contract and implementation boundary were reviewed on 2026-11-03.
Rust and MFC already expose strict diagnostics-only selectors accepting V1, and
the canonical reducer already models the stock `> 2` and `> 3` gates. No product
defect or MFC/server source dependency is known at slice start. The single
shared workstream branch was `feature/client-udp-v1-evidence` in Rust,
build-tests, and tooling only.

The protocol proof and catalog-admission portions of the green condition are
now satisfied. Canonical run
`20261103T200530Z-emulebb-main-release-11272` clean-built every subject from a
clean source tree and passed both Rust-requester/MFC-responder and
MFC-requester/Rust-responder directions. Both transitions independently
advertised and registered V1, emitted the exact request `c590 + hash16` and ACK
`c5910100`, omitted complete-source count and part status, and causally applied
queue rank 1 with equal state semantics. The independent registrar re-reduced
the 3,821,677-byte raw evidence object with SHA-256
`9481580abb8d6cb3022cc03417d92f2d9dbabf073544cae45c27987ce39d90e3`
and emitted receipt `rust-mfc-client-udp-v1-20261103t200530z`, bound to result
SHA-256 `a690921d345c279bbbb6a4bda4f5d5443389e86e32814ff61bf4bc38c93b6b30`.
The receipt binds Rust `3f51f2792b8a43e184016ba667e2b006f1321058`, MFC
`e85415047c6648a2ce40d1b1ec7689987f2612ea`, runner
`8775705f896cf12dc5f6856864e10eb5694c9897`, and upstream-clean server
`d6a6dd672815a13265393ff22622c7fd97b58eee`. The catalog admitted 35/100 IDs
overall and 8/9 for `client-udp` at delivery.

The full local green condition is now satisfied at the exact pushed Rust head
`3f51f2792b8a43e184016ba667e2b006f1321058` and build-tests head
`8988b9c7ab94c1b9629d2c3ebef1b7938c8e9223`. Rust passed policy, 128 policy
tests, rustfmt, warning-denied workspace Clippy, diagnostics compilation, 29
WebUI unit tests, 17 browser tests, typecheck, production WebUI build, fresh
Debug and Release workspace builds, the Release diagnostics build, all locked
workspace and doc tests, and 3/3 serialized VPN egress tests. Build-tests passed
3,362 tests with one expected POSIX-only skip and one configured deselection;
every changed Python file passes Ruff and format checks, and catalog validation
reports exactly 35/100 and 8/9 client UDP. The strict tooling documentation
build also passes. MFC and `ed2k-server` remained clean and unchanged.

The product and evidence changes reached protected `main` on 2026-11-03 after
their exact pull-request heads passed every required hosted check. Rust PR #220
was squash-merged as `f40aa063432361cd34330de87ac28d613d7d8281`, and
build-tests PR #94 was rebase-merged with protected-main tip
`dc04bcd520ce1dd3d9b2602cd5fe9e62261aafb4`. Tooling PR #145 was the final
coordinated delivery member and rebase-merged as
`7a5c55a0026d6e135d830d54bcedd04d17ca410e`. Rust's exact post-merge CI and
CodeQL workflows passed on every platform, including live REST/OpenAPI
conformance. Tooling's exact post-merge workflows also passed. Build-tests run
`41717413561` passed both Windows harness suites plus Linux and Windows
portability; its macOS portability job was cancelled before receiving a runner
and remains a resume action. The shared topic branches were removed locally and
remotely, and all participating repositories returned cleanly to their
protected default branches.

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
- The completed `client-udp.v3` slice is admitted by receipt
  `rust-mfc-client-udp-v3-20261103t180856z`, result SHA-256
  `8b66f9f58a4dcbc8f1ca3e5161065a63ad8b8e16af3a36de6b7b73b20c06c20a`,
  and raw-evidence SHA-256
  `40927f27775c2ca70526e51cf26e2bd19f4b6d1ae8851e764f8a6eb1350bb694`.
  Rust PR #218, MFC PR #192, build-tests PR #92, and tooling PR #143 merged with
  every scoped and hosted gate green; their shared branch was deleted locally
  and remotely before the V2 slice was selected. That campaign found and fixed
  the real Rust defect that discarded the peer's negotiated UDP version and
  incorrectly fell back to V4.
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
  legacy registration path; and
- build-tests `15121b2` - pin and materialize the exact upstream-clean
  ed2k-server evidence authority in fast-harness CI after the first PR head
  correctly failed catalog validation because that new authority checkout was
  absent. Validation was not weakened or bypassed.

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

- build-tests `15121b2`: full suite 3339 passed, 1 skipped, and 1 configured
  deselection; changed-file Ruff and the protocol-catalog validator pass at
  32/100 overall and 5/9 for `client-udp` with zero duplicate assets; the
  replacement PR head passes 20/20 checks across 7/7 workflow runs;
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
upstream-clean. Coordinated PRs are build-tests #91, MFC #191, build #22, and
tooling #142. Their code heads are green; this tracker-only tooling update must
complete its replacement documentation checks before merge.

## Next Step

Open the coordinated Rust, build-tests, and tooling pull requests, require all
protected-main checks at the exact heads, then merge and delete the shared
workstream branch locally and remotely before selecting the next slice.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_protocol_01.md` section 9.3-5 / 10.4 (existing): Hello/tag boundary, Kad framing, and flood exemptions belong to the existing canonical coverage owner. Reference freshness and unused decompiler material do not justify pulling support repos or adding server patches.
- `emulebb-rust-prompt_audit_findings_server-reply.md` section 6.2-4 (existing): Untraced downstream source filtering and partially reviewed UDP bodies are evidence gaps, not confirmed vulnerabilities.
- `emulebb-rust-prompt_audit_findings_udp-reask.md` section 2.1 documentation citation (existing): Rust's explanatory memcpy expression is an equivalent reconstruction, not the literal source expression. Clarify the citation during canonical protocol-evidence work without changing wire behavior.
- `emulebb-rust-prompt_audit_findings_udp-reask.md` section 4.1-4 / 5.3 (existing): Failure-ratio fallback is already implemented with total>3 and failed/total>0.3; remaining transport/obfuscation validation is evidence work rather than implementing a missing timer.
- `emulebb-rust-prompt_audit_findings_secure-ident.md` section 5 / 7 (existing): Weak stock RSA/SHA1 is an accepted interoperability boundary. Key pinning has a closed owner; native-target build/runtime and cross-client proof have existing owners.
- `emulebb-rust-prompt_audit_findings_credits-queue.md` section 6.1-3 / 7.3 (existing): Callback entitlement and disconnected promotion are implemented; the missing end-to-end oracle derivation is a canonical evidence gap, not a proven missing zero-score check.
- `emulebb-rust-prompt_audit_findings_kad-routing-maint.md` section 6 / 7.3 (existing): The report requests optional timer/fill-boundary goldens and acknowledges untraced quality constants. Existing routing maintenance and canonical evidence owners cover this work.
- `emulebb-rust-prompt_audit_findings_obfuscation.md` section 2.2 (design): Inbound length is one byte and bounded to 255 bytes. Server padding above its preferred cap is already logged. Blindly clamping a read can desynchronize RC4/frame state; no automatic cap change should follow this audit.
- `emulebb-rust-prompt_audit_findings_obfuscation.md` section 2.3 (existing): A named classification helper remains staged, but production Kad decrypt already falls through to a registered foreign raw-datagram handler. This disproves the blanket unwired-transport premise; correctness needs mixed-key/protocol evidence before rewiring.
- `emulebb-rust-prompt_audit_findings_obfuscation.md` section 5 (existing): The report inspected constants without proving all server UDP key derivation/state transitions or replaying encrypted exchanges.
- `emulebb-rust-prompt_audit_findings_aich-trust.md` section 6.1,6.3 / 7.3 (existing): Existing tests cover one vote per subnet; hand-derived mask boundaries and large-file/cross-client proof remain evidence extensions, owned by current AICH and canonical protocol items.
- `emulebb-rust-prompt_audit_findings_hashset-largefile.md` section 5 (existing): The report did not run a live exchange. Preserve the existing part-count, AICH geometry and bitmap outcomes through canonical boundaries rather than creating a second parity suite.
- `emulebb-rust-prompt_audit_findings_reachability.md` section 2.5-8 / 4.4 (existing): Generation fences, mapping startup ordering and long-path boundaries are positive confirmations; unresolved timer/cross-client derivations belong to existing evidence work.
- `emulebb-rust-prompt_audit_findings_dos-resilience.md` section 2.5 (existing): Do not add a second contradictory source cap without tracing admission. Attach bounded-source ownership proof to canonical client-UDP evidence.
- `emulebb-rust-prompt_audit_findings_fuzz-malformed.md` section 3.2 (existing): Attach bounded fuzz/property target plus deterministic regressions to canonical protocol evidence; overlaps testing-harness report.
- `emulebb-rust-prompt_audit_findings_fuzz-malformed.md` section 3.3 (existing): Keep stream length/packed/truncation proof in canonical codec owner, not another test ledger.
- `emulebb-rust-prompt_audit_findings_fuzz-malformed.md` section 3.4 (existing): Attach normalization fuzz/property proof to existing decoder and filename owners. Overlaps search6.1 and testing-harness traversal gap.
- `emulebb-rust-prompt_audit_findings_search.md` section 3.3 (design): Strict UTF-8 rejection would change wire acceptance. Require stock malformed-string evidence before changing it.
- `emulebb-rust-prompt_audit_findings_search.md` section 6.1 (existing): Physical proximity of helpers is not a vulnerability. Preserve original display names separately from filesystem-safe leaves; add end-to-end traversal/percent-decoding proof instead of sanitizing metadata early.
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section kad-catalog-domains (existing): The catalog still lacks independently named bootstrap/three-way-HELLO/maintenance domains. Extend the existing parity-consolidation owner rather than open a second harness program.
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section wire-goldens (existing): The blanket claim that all records use FNV-only evidence is stale: newer stock records already carry fixtureBase64 and SHA-256 validation. Reconcile remaining FNV records and explicit full-frame golden ownership within CI-031.
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section crypt-capability-regression (existing): requires_crypt_layer is still hardcoded to zero. Resolve the behavior claim with the protocol audit and stock authority before changing the bit; add the exact capability regression in the canonical parity slice.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A5-buddy (existing): Silent-buddy expiry is already #103. Verify that no callback is relayed for an unrelated buddy within the canonical buddy slice; the aMule report alone does not establish that Rust currently cross-relays.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A7-udp-verification (existing): Some firewall responder verification already has a 180-second TTL. Determine which aMule UDP verification state is meant before asserting a missing equivalent; prove the exact corresponding expiry transition.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A8-direct-callback-publish (existing): The report requests verification of a specific capability combination, not a demonstrated defect. Add it to the existing source-publish parity slice against stock authority.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A9-tag-layout (existing): UTF-8 decoding support exists. Verify the buddy-hash byte layout and negotiated tag cases with exact packet fixtures rather than infer a bug from an aMule changelog.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A19-obfuscation (existing): RC4 speed changes require measurement under the existing hot-path owner. Obfuscated-server timeout/fallback is a protocol transition to verify through the parity catalog, not an automatic downgrade feature.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section security-parser-freeze (existing): The applicable Kad freeze and decoder/downloader allocation assertions need concrete regressions under existing bounds/parity owners. The report incorrectly cites RUST-CI-032 as Kad flood work; current #258 owns dependency-aware early checks.

### Scoped Follow-up Acceptance

- [ ] Check existing catalog/test ownership before adding goldens.
- [ ] Cover only supported boundaries with stock-derived expected bytes and causal receipts.
- [ ] Trace decoded sources through actual IP/ban/admission owner.
- [ ] Register only missing source-admission and UDP state variants in existing coverage owner.
- [ ] Explain equivalence to stock's offset-10 overwrite/copy.
- [ ] Retain endpoint and untouched-tail goldens.
- [ ] Retain success/failure/timeout threshold and recovery cases.
- [ ] Verify mixed clear/encrypted reasks under canonical scenarios.
- [ ] Do not replace on-wire primitives locally.
- [ ] Retain key pin/restart/credit preservation proof.
- [ ] Keep Android evidence non-gating for Beta 3.
- [ ] Cover disconnected LowID selection, entitlement consumption, and slot pacing.
- [ ] Use controlled time for recent-rate windows and fairness decisions.
- [ ] Retain one-hour rearm, sparse-leaf fill boundary and fair due-leaf scheduling proof.
- [ ] Avoid replacing named causal evidence with raw test counts.
- [ ] Determine whether stock limits are send-side preferences or receive rejection rules before any change.
- [ ] If enforcement is justified, reject/drain coherently rather than partially consuming padding.
- [ ] Exercise Kad NodeID, receiver-key, eD2K encrypted and plaintext datagrams on one socket.
- [ ] Prove valid families reach their owner once and malformed collisions remain bounded.
- [ ] Attach supported server UDP and encrypted callback variants to existing deterministic owners.
- [ ] Use independent /20 byte-order fixtures and 16/32-bit proof boundaries.
- [ ] Avoid duplicate evidence tickets or duplicating payload reads.
- [ ] Include exact-part, empty, large-file and unavailable-set variants in canonical evidence.
- [ ] Preserve stale-writer rejection and mapped-port-before-login ordering.
- [ ] Attach only missing firewall/timer state evidence to the canonical owner.
- [ ] Every insertion is admitted through bounded source ownership; churn/removal/restart tests retain the invariant.
- [ ] Expose an isolated fixed-identity decrypt/classify hook and retain malformed/crash regressions.
- [ ] Raw framed streams and bounded decompression exercise lengths, truncation and multiple frames.
- [ ] Malformed entities/percent/encoding inputs stay bounded; every materialization path applies final leaf safety.
- [ ] Any future decoder change must preserve approved stock wire behavior.
- [ ] Percent-decoded separators cannot escape the selected destination; all output paths use the safe leaf allocator.
- [ ] Add bounded catalog IDs and canonical deterministic owners for the three domains.
- [ ] Register the required causal evidence layers and immutable receipts.
- [ ] Unproven transitions remain explicitly incomplete.
- [ ] Inventory remaining digest-only records.
- [ ] Reference full bytes/framing or document their authoritative golden owner.
- [ ] Do not replace existing SHA-256 fixtures with weaker summaries.
- [ ] Verify supported/requested/required combinations against the accepted contract.
- [ ] A deterministic hello fixture pins the outcome.
- [ ] Expire by successfully decoded inbound activity.
- [ ] Test silent half-open replacement/backoff and rejection of an unrelated buddy's callback.
- [ ] Map the upstream state to the Rust owner.
- [ ] Test stale and mismatched verification without accepting unrelated packets.
- [ ] A controlled fixture proves whether and how the source is published.
- [ ] Record the exact source type and buddy/callback tags.
- [ ] Cover buddy hash layout, UTF-8 and legacy fallback fixtures.
- [ ] Malformed tag handling remains bounded.
- [ ] Benchmark before adopting crypto-loop changes.
- [ ] Prove accepted retry/fallback semantics and avoid weakening required obfuscation.
- [ ] Map each reachable freeze/allocation path to its earliest bound.
- [ ] Test counted vectors, compressed data and block/part limits with finite resources.
- [ ] Do not use Rust memory safety or a closed body-limit issue as proof against OOM.
