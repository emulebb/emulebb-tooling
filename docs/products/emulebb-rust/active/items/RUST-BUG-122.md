---
id: RUST-BUG-122
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/125
title: Make completed-download delivery isolated and transactional
status: OPEN
priority: Critical
category: bug
labels: [rust, ed2k, persistence, filesystem, lifecycle, beta]
product: emulebb-rust
phase: Phase 1
milestone: rust-v0.1.0-beta.3
created: 2026-10-15
source: 2026-10-15 Beta 3 completed-download delivery audit after RUST-BUG-121
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/125. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-122 - Make completed-download delivery isolated and transactional

## Summary

Make the transition from a verified hash-named piece store to an
operator-facing completed file one isolated, persisted lifecycle transaction.
The verified payload, delivered file, SQLite row, REST view, retry worker, row
removal, and destructive deletion must agree across ordinary edits, restarts,
concurrent control requests, and power loss.

This is focused Beta 3 stabilization work. Schema, API, configuration, and
internal ownership boundaries may break where that produces a coherent
long-term model instead of preserving the current hybrid behavior.

## Product Boundary

The Rust product is a headless local eD2K/Kad client, not an indexer or remote
coordinator. Its completed-download contract is therefore fundamental:

- bytes accepted under an ED2K hash must remain authoritative for upload;
- users must receive a normal file in Incoming or the selected category;
- REST state must describe persisted reality after restart;
- retries and removal must never strand the only usable copy or leave an
  untracked file after reporting success.

The current same-volume hard-link optimization crosses the trust boundary
between the immutable verified store and mutable operator-owned content.

## Confirmed Critical Defects

### Writable delivery aliases verified upload authority

- `deliver_payload_file` hard-links `pieces.bin` into the destination when both
  paths are on one volume.
- Upload serving later reads the retained hash-named piece store and trusts its
  persisted verified ranges without rehashing each read.
- Editing, truncating, tagging, or repairing the delivered file therefore
  mutates the same inode and can make the client upload changed bytes under the
  old ED2K hash.
- Cross-volume delivery already has independent-copy semantics, so behavior
  also changes based only on storage topology.

### Missing or corrupt source can be committed as delivered

- An absent `pieces.bin` is treated as the zero-byte special case without first
  requiring `expected_size == 0`.
- A newly installed hard link or copy is accepted without validating its size
  and ED2K hash; verification is used only when adopting an already-existing
  collision candidate.
- A missing non-empty source can therefore create an empty completed file, and
  a truncated or externally modified source can be committed as delivered.

### Persisted completed transfers disappear after restart

- Startup hydration intentionally skips completed manifests and initializes the
  in-memory transfer map empty.
- Transfer listing and bulk clear walk only that in-memory map, while direct
  lookup lazily hydrates a persisted row.
- Immediately after restart, a completed transfer is absent and bulk clear is a
  successful no-op; looking it up by hash makes it appear in later list calls.

### Recorded delivered paths are neither verified nor retried

- A recorded path is accepted as `AlreadyDelivered` when any filesystem object
  exists there; regular-file type, size, fingerprint, and hash are not checked.
- The production retry selector includes only rows whose delivered path is
  null, so a deleted, moved, replaced, symlinked, or directory occupant is never
  reconciled after restart.
- Public state derives `completed` from the stored path, not filesystem reality.

### Delivery races destructive deletion

- Delivery has its own lock but drops the manifest lock while copying and
  installing the destination.
- Destructive deletion does not acquire the delivery lock. It reads the old
  delivered path, removes visible/internal storage, and removes the SQLite row
  as separate operations.
- A concurrent large delivery can install its destination after deletion saw no
  delivered path, then fail its phase-two manifest reload. The delete request
  reports success while an untracked operator-facing file remains.
- A crash after filesystem deletion but before SQLite deletion leaves a
  completed catalog row with neither internal nor delivered authority.

### Row-only removal can permanently suppress delivery

- Failed delivery leaves a verified transfer in `completing`.
- Row removal checks only the manifest's whole-file completion bit, marks the
  row removed, and does not require a reconciled delivered file.
- Retry selection excludes removed rows, so a direct REST delete can permanently
  hide a completed download whose only remaining copy is internal `pieces.bin`.

### Filesystem and SQLite durability are misordered

- Delivery syncs copied file contents and the pending-intent file, but does not
  sync parent directories after link/create/rename or intent replacement.
- SQLite uses WAL with `synchronous=FULL` and can durably commit
  `delivered_path` before the destination directory entry is durable.
- The inverse crash window can preserve an unrecorded destination while losing
  the intent, causing retry to create a suffixed duplicate.

## Confirmed Major Gaps

- Completed-manifest rewrites refresh `completed_at_ms` and download-history
  completion time even when no incomplete-to-complete transition occurred.
- Failure to delete `delivery.pending` is returned after the manifest commit as
  a delivery failure, while retry selection excludes the now-delivered row.
- Process termination can leave full-size `.ed2k-delivering-*` sibling files;
  no startup reconciliation owns or removes them.
- Cross-volume `tempfile` creation can publish a different Unix permission mode
  than same-volume delivery. Output permissions have no explicit product rule.
- Relative Incoming paths remain anchored to process working directory and can
  redirect future completed files after a service-layout change.
- Destination directory identity is not held across check and install, leaving
  a local symlink/junction replacement race in writable parent directories.

The first three major gaps belong to this item's persisted lifecycle work. Path
normalization, output permission policy, and directory-handle hardening remain
retained audit findings but must not broaden the first critical repair slices.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/deliver.rs`
- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs`
- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs`
- `crates/emulebb-core/src/delivery.rs`
- `crates/emulebb-core/src/disk_guard.rs`
- `crates/emulebb-core/src/transfer_control_api.rs`
- `crates/emulebb-core/src/transfer_create_api.rs`
- `crates/emulebb-core/src/transfer_state_api.rs`
- `crates/emulebb-core/src/views.rs`
- `crates/emulebb-metadata/src/transfer_store.rs`
- `crates/emulebb-metadata/src/download_history_store.rs`
- `crates/emulebb-daemon/src/lib.rs`
- `crates/emulebb-rest/src/handlers/transfers.rs`

## Intended Shape

- Keep the hash-named piece store as immutable verified upload authority.
  Materialize an independent copy, or a copy-on-write clone with proven write
  isolation; never expose a writable hard-link alias.
- Reserve delivery capacity according to the actual materialization contract.
  An always-copy design reserves one additional payload even on the same volume.
- Distinguish a legitimate zero-byte payload from missing internal storage and
  validate source plus installed output before persisted state advances.
- Persist explicit delivery and deletion lifecycle state instead of inferring
  authority from nullable path fields and in-memory retry errors.
- Reconcile persisted non-removed rows on startup before publishing the transfer
  view. List, direct lookup, retry, and clear must not depend on call order.
- Use one per-transfer lifecycle gate for delivery, output reconciliation, row
  removal, and destructive deletion.
- Persist destructive intent before removing either filesystem authority, then
  recover or complete the operation deterministically after restart.
- Sync filesystem namespace commits before the corresponding SQLite transition.
  Post-commit intent cleanup is best-effort, observable, and retryable.
- Preserve completion timestamps across metadata-only rewrites and delivery;
  set them only on an actual incomplete-to-complete transition.

### Persisted delivery-state model

Schema version 34 stores one explicit state on every transfer:

- `not_applicable` — a share-in-place file; `source_path_id` is required and
  `delivered_path_id` is forbidden;
- `pending` — a download whose operator-facing copy has not been committed;
  both source and delivered paths are forbidden, including while incomplete;
- `delivered` — a download with a committed operator-facing copy;
  `delivered_path_id` is required and `source_path_id` is forbidden.

The database CHECK constraint and metadata upsert validation enforce the same
state/path matrix. Completion and final-rehash state are intentionally
orthogonal: a download is pending from creation, and an operator-triggered
rehash may temporarily clear completion without discarding a valid delivery
record.

## Ordered Implementation Slices

1. **Payload isolation and validation** — add failing alias/missing-source tests,
   replace hard-link delivery with isolated atomic materialization, update disk
   reservation, and validate installed bytes before commit.
2. **Persisted completed visibility** — make listing and bulk-clear operate on
   persisted non-removed transfers with deterministic startup semantics, while
   preserving bounded large-library behavior.
3. **Delivery reconciliation state** — introduce explicit persisted delivery
   state, verify recorded outputs, retry missing/mismatched destinations, and
   reclaim owned stale temporary artifacts.
4. **Lifecycle serialization** — use one per-transfer gate and a persisted
   deletion intent across delivery, row removal, and destructive deletion.
5. **Durability ordering** — add directory-sync barriers and deterministic
   failpoints for intent, destination, manifest, and deletion transitions.
6. **Temporal correctness** — preserve completion/history timestamps across
   non-transition manifest updates and make post-commit cleanup non-reversing.

Each slice lands as its own Rust commit with focused tests. Do not combine the
schema/state-machine change with unrelated path-policy or UI work.

## Completed Temporal-Correctness Slice

Rust PR #128 merged to protected `main` by rebase on 2026-10-16.

The merged Rust commit is limited to persisted completion time:

- detect an actual incomplete-to-complete transition before overwriting the
  known-file completion bit;
- preserve `transfers.completed_at_ms` across completed metadata rewrites,
  delivery-state changes, and temporary completed-to-incomplete demotion;
- advance `download_history.last_completed_at_ms` only on a real completion
  transition while still allowing descriptive metadata to refresh;
- add deterministic metadata regressions for first completion, metadata-only
  rewrites, demotion, and a later recompletion.

Filesystem namespace sync barriers and stale owned-artifact reclamation remain
separate follow-up commits so their crash semantics are reviewed independently.

## Active Delivery-Attempt And Durability Slice

Branches: `fix/rust-bug-122-delivery-attempts` and
`docs/rust-bug-122-delivery-attempts`.

This final focused slice replaces ambiguous filesystem inference with persisted
provenance, then closes the remaining namespace-durability boundaries in five
granular Rust commits:

1. add a typed SQLite delivery-attempt record keyed by transfer, with a random
   attempt identifier, exact staging and target paths, and an explicit phase;
2. persist attempt provenance before staging, use an attempt-specific no-clobber
   staging name, and never adopt a pre-existing destination by content equality;
3. recover or reclaim only exact artifacts whose ownership is proven by the
   persisted attempt; preserve legacy `.ed2k-delivering-*` files when provenance
   is absent;
4. resolve any active delivery attempt before destructive deletion removes the
   transfer directory, and make post-commit intent cleanup non-reversing;
5. sync destination and transfer-root namespace changes before their associated
   SQLite transitions, with deterministic crash-boundary regressions.

The recovery contract is deliberately conservative: an installed destination
may be inferred only from a durable staged attempt whose exact staging path has
disappeared and whose exact target verifies. `AlreadyExists` always preserves
the unrelated target and selects another suffix. Cleanup never globs temporary
names and never deletes an artifact without persisted provenance.

### Independent Review Blockers

Rust draft PR #129 (`https://github.com/emulebb/emulebb-rust/pull/129`)
remains draft after independent review found that the initial attempt model is
not yet strong enough to authorize ownership-sensitive recovery or deletion:

- `staged` proves that a staging file was verified, but does not prove that the
  exact target was installed; a missing staging file plus byte-identical foreign
  target must therefore never be adopted or deleted;
- installation currently removes the staging hard link before the delivered
  manifest commits, discarding the strongest native-identity proof and opening
  classify-to-unlink and verify-to-fingerprint replacement races;
- destructive deletion still treats content equality as ownership and can
  remove a byte-identical operator replacement;
- hard-link-only publication excludes filesystems without hard-link support;
- Windows namespace operations do not yet have an enforceable write-through
  ordering equivalent to the Unix parent-directory sync barrier;
- a raced `NotFound` during delivered-file deletion must still re-establish the
  namespace durability barrier before SQLite finalization.

The required redesign separates content validity from ownership proof, retains
or persists native target identity through manifest commit, uses atomic
platform publication without requiring hard-link support, and adds deterministic
tests for every install, cleanup, and deletion crash boundary before the PR can
leave draft.

### Review Resolution Checkpoint (2026-10-16)

The publication-side blockers are now closed in four granular Rust commits:

- `f7618dbe` adds schema 39 `published` delivery attempts and explicit
  `owned`/`unowned` delivered-path authority across metadata and ED2K models;
- `0ce4bbea` replaces hard-link-only publication with native atomic no-replace
  moves on Linux, macOS, and Windows, including explicit collision and
  unsupported-filesystem outcomes plus namespace barriers;
- `fc6f9984` keeps the verified staging handle open through publication,
  captures and persists a post-move fingerprint before manifest advancement,
  and records interrupted staged-without-staging recovery as `unowned` rather
  than granting destructive ownership;
- deterministic runtime regressions cover staged recovery, publication before
  and after the `published` SQLite boundary, byte-identical foreign target
  collision, long Windows paths, and ambiguous staged deletion preservation.

Focused validation currently passes: 55 metadata tests, 24 delivery runtime
tests, both filesystem durability tests, and core/ED2K all-target compile
checks.

### Deletion Review Resolution Checkpoint (2026-10-16)

The final design blocker is now closed in three additional granular Rust
commits:

- `c68a2074` adds schema 40 `prepared`/`moved` output-tombstone metadata with
  exact native paths, source and moved fingerprints, idempotent transitions,
  and ownership-gated creation;
- `982c7898` replaces classify-then-unlink with a persisted same-directory
  tombstone transaction, atomic no-replace rename, post-move identity
  checkpoint, retryable reclamation, and final transfer-row removal only after
  the owned namespace object is gone. It also applies the same tombstone-first
  ordering to the internal transfer directory;
- `8702bb53` retains strict pre-exposure startup recovery and adds periodic
  daemon retries so transient sharing and antivirus failures converge without
  requiring a process restart.

Deterministic regressions cover every output tombstone crash boundary, a
byte-identical replacement racing between verification and rename, foreign
tombstone collisions, Windows sharing violations, long paths, interrupted
published attempts, unowned output preservation, and transfer-directory
tombstone recovery. Focused validation passes with 57 metadata tests, 35
delivery runtime tests, core and daemon all-target checks, and strict
metadata/ED2K/core/daemon Clippy. Draft Rust PR #129 now has no known design
blocker; it remains draft only until the full repository gate, fresh independent
review, and protected-main CI are complete.

### Full Local Gate Checkpoint (2026-10-16)

The canonical `python tools/rust_quality_gate.py ci` gate now passes from a
clean committed Rust tree. It covers client policy plus 111 policy tests,
formatting, workspace-wide all-target strict Clippy, packet diagnostics, 28
WebUI unit tests, 16 Chromium end-to-end tests, fresh debug and release builds,
the complete workspace suite including 1,142 ED2K, 415 core, 70 daemon, and 57
metadata unit tests plus integration and documentation tests, and all three
observed VPN egress tests. The first run exposed one stale legacy assertion that
still expected post-install verification; `9324a162` updates it to assert the
stronger pre-publication rejection contract, and the full gate then passed.

### Fresh Independent Review Blockers (2026-10-16)

Rust PR #129 remains draft and unmergeable after a fresh full-diff review found
four ownership/crash-safety blockers that the green suite did not exercise:

- canonical-payload recovery can replace an owned delivered fingerprint with a
  merely content-valid foreign replacement without demoting deletion ownership;
- a `prepared` delivery attempt has no proven staging identity, but recovery and
  deletion currently unlink any object occupying its recorded staging path;
- publication hashes staging before the final rename but does not rehash the
  retained handle after that final mutation window before persisting `owned`;
- output-tombstone recovery assumes native file identity remains stable across
  rename on every supported filesystem, so an unstable provider can make a
  crash-before-checkpoint job permanently block startup.

The same review found two required robustness follow-ups: one blocked deletion
must not starve later pending jobs, and `delivered + owned` must require a
fingerprint whose size matches the transfer. It also noted a residual
check-then-unlink race in final randomized tombstone reaping. Resolve each item
with a focused regression and granular Rust commit, rerun the canonical gate,
and obtain another clean independent review before marking the PR ready.

### Fresh Review Resolution Checkpoint (2026-10-16)

All fresh-review findings are now closed in eight granular Rust commits:

- `76afc11c` demotes an owned delivered output to `unowned` whenever canonical
  payload recovery proves only content, not the exact recorded native identity;
- `6ba65065` preserves any occupant of a `prepared` staging path because that
  phase has not captured identity authority yet;
- `1cc7e599` rehashes the retained staged handle after atomic publication and
  before persisting `published`/`owned`, with a Unix mutation-window failpoint;
- `cc12a789` verifies an uncheckpointed moved tombstone by ED2K hash and stable
  opened-handle/path binding before adopting a rename-changed native identity;
- `43b70919` processes every pending deletion in a sweep and aggregates failures
  so one blocked job cannot starve later durable work;
- `f98fad47` bumps the clean schema to 41 and requires every owned delivered
  output to carry a fingerprint whose size matches the transfer;
- `49144ea8` adds a final pre-unlink identity recheck plus a deterministic
  tombstone replacement failpoint;
- `7698ab79` keys destructive-delete test hooks by native path so parallel
  same-content fixtures cannot consume one another's race injection.

Focused validation passes: 39 delivery runtime tests, 16 managed-payload
reconciliation tests, 58 metadata tests plus documentation tests, strict
ED2K/metadata Clippy, formatting and diff checks, and core/daemon all-target
checks. A second independent full-diff review and the canonical full gate remain
required before protected-main CI and merge.

### Second Independent Review Checkpoint (2026-10-16)

The canonical `python tools/rust_quality_gate.py ci` gate passes after all eight
fresh-review fixes. The first rerun was interrupted by a transient Windows lock
on the Rolldown native module during the second `npm ci`; an unchanged rerun
completed client policy plus 111 policy tests, formatting, workspace-wide
all-target strict Clippy, packet diagnostics, 28 WebUI unit tests, 16 Chromium
end-to-end tests, fresh debug and release builds, the complete workspace test
suite, integration and documentation tests, and all three observed VPN egress
tests.

The second independent full-diff review nevertheless found three high-severity
merge blockers:

- destructive deletion persists the database intent before fallible delivery-
  attempt cleanup, but hides the live cache/catalog entry only afterward; a
  staging cleanup failure can therefore leave a durably deleted transfer live
  and potentially served until restart;
- crash-before-checkpoint output-tombstone recovery accepts a byte-identical
  replacement when native identity changed, which treats content equality as
  ownership and can delete a foreign replacement;
- startup propagates pending-deletion cleanup failures as fatal, so a persistent
  sharing lock or deliberately preserved ambiguous tombstone can create an
  indefinite daemon restart loop before the runtime retry sweep starts.

The review also found two medium-severity gaps: transfer-directory tombstones
have no persisted identity before recursive recovery deletion, and the Unix
post-publication mutation hook is keyed only by content hash so parallel
same-content fixtures can consume the wrong hook. The final path-based unlink
still has a low-severity check-to-unlink race that the current failpoint does not
exercise. Prior ownership demotion, prepared-staging preservation, post-move
rehash, deletion-sweep starvation, and schema 41 owned-fingerprint findings are
closed. Rust PR #129 remains draft and must not merge until these remaining
findings are resolved in granular commits, the canonical gate passes again, a
third independent review is clean, and fresh protected-main CI passes.

### Second-Review Resolution Checkpoint (2026-10-18)

Five granular Rust commits resolve every high- and medium-severity finding from
the second independent review:

- `22e9e86d` keys post-publication race hooks by native target path instead of
  shared content hash, so parallel same-content fixtures cannot cross-talk;
- `6ee34f0e` hides cache, checkpoint, and shared-catalog visibility immediately
  after durable deletion acceptance, before any fallible attempt cleanup;
- `ef46d082` requires native identity continuity before adopting an
  uncheckpointed output tombstone, preserving byte-identical replacements;
- `13395fbc` reports per-transfer startup cleanup failures as retryable pending
  work while keeping intent enumeration and database failures fatal;
- `aabbb846` advances the clean-profile schema to 42 and atomically records the
  owned transfer-directory identity with first deletion intent. Recovery never
  adopts a later path, rejects changed original/tombstone identities, and
  preserves non-directory and share-in-place occupants.

Focused validation passes: all 61 metadata tests, all 41 delivery-runtime tests,
the core startup ordering regression, affected ED2K/core/daemon compile checks,
formatting, and diff checks. The earlier Linux/macOS CI failures were reproduced
as test-hook cross-talk or an invalid cross-platform timestamp expectation and
are addressed by `22e9e86d`.

The unchanged canonical `python tools/rust_quality_gate.py ci` rerun passes at
Rust head `aabbb846`: client policy plus 111 policy tests, formatting,
workspace-wide all-target strict Clippy, packet diagnostics, 28 WebUI unit
tests, 16 Chromium end-to-end tests, WebUI production build, fresh debug and
release workspace/diagnostics builds, the complete workspace and documentation
test suites, and all three observed VPN egress tests.

One low-severity platform limitation remains documented rather than disguised
as an atomicity fix. Rust/Unix exposes no portable unlink-by-open-handle
primitive: both final output-tombstone unlink and recursive transfer-directory
reaping necessarily retain a narrow identity-check-to-path-delete race against
a hostile process already able to mutate those directories. Crash/restart and
accidental replacement safety are closed by persisted identity, no-follow
opens, randomized output tombstones, repeated identity checks, and fail-closed
retry. Eliminating the adversarial race would require platform-specific
handle-relative recursive deletion or a stronger private-filesystem boundary;
it is an explicit Beta 3 residual, subject to the third independent review, not
an unverified claim of portability.

The remaining merge sequence is the third independent full-diff review,
topic-branch push, fresh protected-main CI/CodeQL, then rebase merge. Rust PR
#129 remains draft until those steps are green.

## Acceptance Criteria

- [x] User edits to a delivered file cannot change bytes served from the
      verified piece store.
- [x] Missing, truncated, or corrupt internal payloads fail delivery without
      creating or committing a false completed output.
- [x] Installed output is a verified regular file before persisted state moves
      to delivered.
- [x] Restarted list, direct lookup, retry, and bulk clear are independent of
      endpoint call order.
- [x] Missing or mismatched recorded outputs enter deterministic reconciliation
      rather than remaining falsely completed.
- [x] Row removal cannot suppress delivery of a verified-but-undelivered file.
- [x] Delivery and destructive deletion serialize and recover without orphan
      output, hidden-only success, or a row whose authorities are both absent.
- [x] Filesystem namespace durability precedes SQLite advancement at every
      cross-domain commit boundary supported by the platform.
- [x] Owned stale copy/intention artifacts are reclaimed without touching
      unrelated user files.
- [x] Completion and history timestamps change only on a true completion
      transition.
- [x] The canonical Rust quality gate and protected-main CI pass.

## Validation Plan

- Runtime tests for hard-link mutation isolation, zero-byte versus missing
  non-empty sources, truncated sources, installed-output verification, and
  collision no-clobber behavior.
- Core/metadata restart tests for completed listing, direct lookup, bulk clear,
  pending retries, removed rows, and timestamp preservation.
- Deterministic paused-task tests for delivery versus row removal and destructive
  deletion, including failure between filesystem and SQLite transitions.
- Failpoint/process-boundary tests for pending intent, destination rename,
  directory sync, manifest commit, cleanup, and deletion recovery.
- Platform coverage for Windows long paths and Unix directory durability; real
  cross-volume coverage where the workspace harness provides it.

## Audit Evidence

- Existing tests cover sanitization, collision suffixing, same-process delivery
  concurrency, empty downloads, long paths, and direct intent adoption.
- Existing restart delivery coverage calls materialization directly and bypasses
  the production retry selector.
- Existing deletion coverage is sequential, completed-clear coverage uses a
  same-process in-memory store, and current history tests accept timestamp
  refresh after metadata-only rewrites.
- No existing GitHub issue matched delivery hard-link aliasing, completing-row
  removal, or persisted delivery reconciliation when this item was created.

## Progress

- `1a1e428c` removes same-volume hard-link delivery. Every completed download is
  now materialized through an independent temp-copy plus no-clobber install, so
  edits to the operator-facing file cannot mutate retained verified upload
  bytes. The aggregate disk guard now reserves the additional full payload on
  same-volume layouts as well as cross-volume layouts. A runtime regression
  test mutates the delivered file and proves `pieces.bin` remains unchanged; a
  core reservation test proves an empty same-volume download reserves both the
  piece store and delivered copy. Validation: all 1,073 `emulebb-ed2k` tests
  and all 410 `emulebb-core` unit tests plus integration/doc tests passed through
  the workspace harness.
- `f2b024fb` completes the payload-isolation/validation slice. Delivery now
  requires a regular source with the expected size before creating the
  destination, except for the explicit zero-byte/no-piece-store case. Every
  newly installed copy is rehashed with canonical ED2K semantics before the
  manifest can record it; failed verification removes the untrusted output.
  Runtime and helper regressions cover a missing non-empty piece store, a
  truncated source, a wrong installed hash, manifest non-advancement, and
  cleanup of the rejected destination. Validation: all 1,076 `emulebb-ed2k`
  tests and doc tests passed through the workspace harness.
- `9f39a64c` completes the persisted completed-transfer visibility slice. The
  metadata/runtime boundary now exposes only non-removed transfer-list
  manifests, excluding the potentially 100k-entry completed shared catalog.
  Core hydrates those rows through one idempotent barrier shared by list,
  direct lookup, startup resume, and bulk clear; the daemon completes hydration
  before opening REST. A restart regression proves a delivered transfer is
  listed without a prior hash lookup, can be bulk-cleared from a fresh core,
  preserves its operator file, and remains absent after another restart.
  Validation: all 48 `emulebb-metadata` tests, all 1,076 `emulebb-ed2k` tests,
  all 411 `emulebb-core` unit tests plus integration/doc tests, and all 70
  `emulebb-daemon` tests plus doc tests passed through the workspace harness.
- `02869dae` introduces the explicit persisted delivery lifecycle and bumps the
  clean-profile schema from 33 to 34. Downloads start `pending`, share-in-place
  rows are `not_applicable`, and only a verified output committed with its path
  becomes `delivered`. SQLite and the metadata API reject incoherent state/path
  combinations; pending retry selection now uses the state instead of nullable
  paths. Core and the ED2K runtime also use the state as delivery authority and
  return a first-class `NotRequired` outcome for share-in-place files.
  Validation: `cargo fmt --all --check`, all 48 `emulebb-metadata` tests, all
  1,076 `emulebb-ed2k` tests, and all 411 `emulebb-core` unit tests plus
  integration/doc tests passed through the workspace harness.
- `68868d70` completes startup verification and deterministic reconciliation of
  recorded delivered outputs. Before REST starts, the daemon now enumerates
  every active completed download in `pending` or `delivered` state; candidate
  discovery fails startup instead of publishing an unverified transfer view.
  Recorded regular files with an exact safe native fingerprint take the fast
  path, while changed, missing, coarse, or unavailable identities fall back to
  a full canonical ED2K hash. Byte-identical replacements are adopted with a
  refreshed fingerprint. Missing, non-file, wrong-size, wrong-hash, or
  unverifiable outputs are first persisted back to `pending`, then re-delivered
  through the collision-safe path; unrelated occupants remain untouched and a
  verified suffix is selected. Failed redelivery remains visibly pending for
  the existing retry worker. Restart and runtime regressions cover replaced,
  missing, byte-identical, and failed-redelivery cases. Validation: `cargo fmt
  --all --check`, all 48 `emulebb-metadata` tests, all 1,080 `emulebb-ed2k`
  tests, all 412 `emulebb-core` unit tests plus integration/doc tests, and all
  70 `emulebb-daemon` tests plus doc tests passed through the workspace harness.
- `d28ea3b0` introduces one per-transfer lifecycle gate shared by delivery,
  row-only removal, and destructive deletion. Destructive deletion now removes
  the recorded delivered output inside the ED2K runtime while holding the same
  gate as materialization, closing the in-process orphan race. Row-only removal
  rejects a completed download whose delivery state is still `pending`, so a
  failed or concurrent delivery cannot be hidden from retries; share-in-place
  and fully delivered rows remain removable without deleting their files.
  Deterministic lock-held regressions prove both removal operations wait for
  the gate, and a core regression proves rejected row removal leaves the
  transfer visible as `completing`. Validation: `cargo fmt --all --check`, all
  1,082 `emulebb-ed2k` tests, and all 413 `emulebb-core` unit tests plus
  integration/doc tests passed through the workspace harness.
- `52e023be` bumps the clean-profile schema from 34 to 35 and adds a terminal
  `delete_requested_at_ms` marker with a partial recovery index. The metadata
  contract now has explicit idempotent request, ordered pending-intent scan,
  and intent-gated finalization operations. Repeated requests preserve the
  original intent/update timestamps, ordinary manifest upserts cannot clear an
  intent, and finalization refuses an unmarked transfer. The existing metadata
  deletion transaction was factored through one shared known-file cleanup path.
  Validation: `cargo fmt --all --check` and all 49 `emulebb-metadata` tests plus
  doc tests passed through the workspace harness.
- `6c28d59e` makes a pending destructive deletion a terminal visibility
  partition instead of an ordinary transfer state. Normal manifest, startup
  hydration, transfer timestamp/count, completed catalog, publish, share,
  share-in-place reload, delivered-reuse, and delivery-reconciliation queries
  now suppress intent-marked rows; one explicit deletion-only manifest read is
  retained for recovery. Full manifest rewrites and piece checkpoints cannot
  mutate an intent-marked transfer, and ED2K job creation or explicit
  replacement acquires the lifecycle gate and rejects recreation while intent
  is pending. Regressions cover every metadata surface, duplicate shared-source
  reload, and both runtime recreation paths. Validation: `cargo fmt --all
  --check`, all 49 `emulebb-metadata` tests, all 1,083 `emulebb-ed2k` tests,
  `cargo check --workspace`, all 413 `emulebb-core` unit tests, and every core
  integration/doc test passed. The existing shared-directory persistence
  binary still exposes a parallel-only SQLite lock flake in its default test
  runner; its seven tests pass with `--test-threads=1`, and the failing case
  passes in isolation.
- `31f14a1d` extracts one conservative delivered-output identity classifier
  shared by recorded-output reconciliation, pending-intent adoption, collision
  handling, and installed-output verification. It distinguishes a missing path
  from matching canonical bytes and a foreign occupant, keeps the native
  fingerprint fast path, falls back to a full ED2K hash, and rejects identity
  changes observed across hashing. This gives destructive cleanup the exact
  primitive needed to delete only the recorded file still owned by the
  transfer. Validation: `cargo fmt --all --check` and all 1,084
  `emulebb-ed2k` tests plus doc tests passed.
- `bd4c1086` makes the durable deletion intent the operation's commit point.
  The ED2K runtime now persists intent under the lifecycle and manifest gates
  before touching either filesystem authority, immediately evicts manifest and
  catalog visibility, and finalizes SQLite only after cleanup. Matching or
  missing recorded outputs are removed/accepted, while a foreign replacement
  is preserved. Any cleanup or finalization failure leaves the terminal intent
  hidden and retryable instead of reversing the user's deletion; repeated
  cleanup resumes from the deletion-only manifest reader. Regressions cover the
  lifecycle gate, both-authority removal, foreign-file preservation, restart
  resumption, and a forced mid-cleanup failure followed by idempotent retry.
  Validation: `cargo fmt --all --check`, all 1,087 `emulebb-ed2k` tests plus doc
  tests, and the three focused `emulebb-core` destructive-deletion tests passed.
- `fe89bf57` completes pre-exposure recovery of durable destructive-deletion
  intents. Startup scans the ordered intent set immediately after core
  construction and strictly resumes each deletion before transfer hydration,
  delivery reconciliation, REST binding, or network/background task startup.
  Interactive deletion retains its accepted-and-retry-later contract, while
  startup propagates cleanup/finalization failures with the transfer hash and
  refuses to expose a profile until every intent is complete. Recovery remains
  independently idempotent per hash, so earlier intents may finish before a
  later blocker stops startup. Restart regressions cover successful cleanup,
  an empty no-op scan, a forced cleanup failure that preserves the intent, and
  successful retry; a core regression proves recovered rows cannot enter
  hydration or delivery reconciliation. Validation: `cargo fmt --all --check`,
  all 1,088 `emulebb-ed2k` tests, all 414 `emulebb-core` unit tests, all 70
  `emulebb-daemon` tests plus doc tests, and `cargo check --workspace` passed.
- `3c6f6eba` closes silent adoption of untracked transfer-root content. A new
  download with no persisted manifest now inspects its canonical hash path
  under the per-transfer lifecycle/manifest gates. It reclaims only the empty
  directory produced by the pre-commit crash window, plus the one exact retired
  `resume-manifest.json` artifact from pre-SQL builds. A non-empty directory,
  regular file, or symlink is rejected without touching its bytes, so a later
  download can no longer overwrite or gradually incorporate an unmanaged
  `pieces.bin`. Regressions prove empty recovery, retired-manifest cleanup,
  non-empty payload preservation, regular-file preservation, and absence of a
  manifest after rejection. Validation: `cargo fmt --all --check`, all 1,091
  `emulebb-ed2k` tests plus doc tests, and `cargo check --workspace` passed.
- `b6856ae4` adds the pre-exposure transfer-root inventory without introducing
  destructive quarantine policy. Metadata now exposes the exact download rows
  which own internal hash paths, including hidden pending-deletion rows while
  excluding share-in-place sources. After strict deletion recovery and before
  transfer hydration/REST/network startup, the runtime scans only direct child
  names which are canonical lowercase ED2K hashes. Empty/pre-SQL residue is
  reclaimed; non-empty directories, regular files, symlinks, and inspection
  failures are preserved and logged per hash, with aggregate daemon counts.
  Noncanonical operator content is ignored. Each candidate is lifecycle- and
  manifest-locked and ownership is rechecked after locking, so a stale scan can
  never remove a concurrently committed transfer directory. Validation: `cargo
  fmt --all --check`, all 49 `emulebb-metadata` tests, all 1,092
  `emulebb-ed2k` tests plus doc tests, all 414 `emulebb-core` unit tests, all 70
  `emulebb-daemon` tests plus doc tests, and `cargo check --workspace` passed.
- `dd500281` adds a strict pre-exposure authority barrier for every persisted
  incomplete download. Under the per-transfer lifecycle and manifest locks,
  startup now recreates only metadata-owned missing hash directories, inspects
  `pieces.bin` with no symlink following, and fails closed while preserving any
  directory, symlink, or other wrong-type occupant. Missing payloads and any
  payload shorter than the highest persisted contiguous or bitmap-backed byte
  demote every claimed piece, clear derived verified ranges/final-rehash state,
  persist the repair, and evict stale catalog authority before transfer
  hydration or network publication. The all-progress demotion is deliberate:
  once truncation is observed, file extent alone cannot prove that an earlier
  prefix still belongs to the persisted ED2K identity. Intact partial payloads
  retain their progress, and the operation is idempotent. Six restart-focused
  regressions cover missing payloads, truncation, intact partials, missing
  directories, wrong payload types, and wrong transfer-directory types.
  Validation: `cargo fmt --all --check`, `git diff --check`, strict Clippy for
  `emulebb-ed2k`, `emulebb-core`, and `emulebb-daemon`, all 1,098
  `emulebb-ed2k` unit tests plus doc tests, all 414 `emulebb-core` unit tests,
  all 70 `emulebb-daemon` unit tests, and `cargo check --workspace` passed.
- `eb9ce9e0` closes the operator-recheck gap for incomplete downloads. Recheck
  now reuses the canonical whole-payload part computation to MD4-validate every
  persisted `Verified` piece even when other pieces are still missing. It keeps
  intact verified pieces publishable, demotes missing/truncated or mismatching
  pieces, distinguishes absent bytes from retained corrupt bytes for ICH state,
  and refuses to apply a stale result if geometry, hash authority, or piece
  state changes while disk hashing runs. Completed/fully present payloads retain
  the existing final-rehash barrier. The regression now covers clean partial
  recheck, missing internal payload, restored progress, and subsequent
  corruption. Validation: `cargo fmt --all --check`, `git diff --check`, all
  1,098 `emulebb-ed2k` unit tests plus doc tests, and Clippy with warnings denied
  after exempting the repository's seven unrelated pre-existing
  `unfulfilled_lint_expectations` diagnostics passed.
- `6cbab433` removes completed-catalog construction from the progressive daemon
  constructor. The daemon-facing runtime now starts with an empty completed
  catalog, runs destructive-deletion, transfer-root, payload, transfer-row, and
  delivery reconciliation first, then explicitly hydrates one bounded cohort
  before REST binding or ED2K/Kad startup. Only the remaining pages hydrate in
  the background. This prevents completed metadata, media-path inspection, and
  upload publication from outrunning startup authority checks while preserving
  bounded large-library startup. A regression proves the progressive runtime
  exposes zero entries until explicit initial hydration, then advances the
  keyset cursor without duplicate work. Validation: `cargo fmt --all --check`,
  `git diff --check`, strict Clippy for `emulebb-ed2k`, `emulebb-core`, and
  `emulebb-daemon`, all 1,098 ED2K unit tests, all 414 core unit tests, and all
  70 daemon unit tests passed.
- `e9d83291` fixes canonical upload-source precedence when an explicit
  redownload coexists with a same-hash shared-file row. Once a download has any
  verified internal range, upload readers now use only its hash-owned
  `pieces.bin` and its persisted verified-range map; an unrelated shared path
  can no longer override those bytes merely because its current length still
  matches. The shared-source fallback remains available only while the new
  download has no verified canonical bytes, preserving intentional
  share-while-redownloading behavior. The regression completes a redownload,
  rewrites the old shared source in place with equal-length foreign bytes, and
  proves uploads still return the canonical payload. Validation: `cargo fmt
  --all --check`, `git diff --check`, strict ED2K Clippy, the existing explicit
  redownload fallback regression, and all 1,099 ED2K unit tests passed.
- `bf09f7f0` adds the metadata inventory required by the completed-storage
  barrier. One SQL-filtered query now returns every internally managed download
  manifest, including incomplete, completed, and operator-hidden completed
  rows, while excluding share-in-place identities and already-hidden pending
  destructive deletions. Regressions prove the partition across share-in-place,
  incomplete, completed removed-row, and deletion-intent states. Validation:
  `cargo fmt --all --check`, `git diff --check`, strict metadata Clippy, all 49
  metadata unit tests, and metadata doc tests passed.
- `43d5b512` hardens the durable delivery crash-window pointer before it is used
  as completed-payload recovery authority. `delivery.pending` now stores exact
  platform-native path bytes through the shared `NativePath` codec instead of
  lossy UTF-8 text, and reads distinguish a missing marker from I/O failure,
  empty content, or invalid native encoding. Delivery therefore fails closed
  instead of silently abandoning a corrupt intent, and non-Unicode Unix paths
  have an explicit round-trip regression. Validation: `cargo fmt --all
  --check`, `git diff --check`, strict ED2K Clippy, the crash-window adoption
  regression, and all 1,099 ED2K unit tests passed.
- `0adae526` generalizes startup storage reconciliation across every internally
  managed download, including completed and operator-hidden rows. Completed
  `pieces.bin` content is now whole-file ED2K verified before catalog exposure;
  missing, truncated, oversized, or same-length-corrupt canonical payloads are
  restored only from a separately verified delivered output. If no valid
  recovery remains, completion and every piece claim are demoted, a removed row
  is revived for redownload, and delivery authority is cleared without touching
  a foreign delivered occupant. Invalid regular canonical occupants are moved
  to durable quarantine names before replacement or reset rather than truncated
  or overwritten; wrong filesystem types and transfer-directory identity swaps
  fail startup untouched. A valid `delivery.pending` marker is adopted even
  when the canonical payload is already intact and the transfer row is hidden,
  closing the restore-before-metadata crash window. Regressions cover missing
  directories, incomplete extent loss, exact-length completed corruption,
  verified restoration, hidden-row intent adoption, demotion, upload reads,
  share-in-place exclusion, and wrong path types. Validation: `cargo fmt --all
  --check`, `git diff --check`, strict Clippy for `emulebb-ed2k`,
  `emulebb-core`, and `emulebb-daemon`, all 1,106 ED2K unit tests, all 414 core
  unit tests, and all 70 daemon unit tests passed.
- `fc4c08de` bumps the clean schema to 36 and adds a dedicated canonical
  `payload_fingerprint`, explicitly separate from shared-source and delivered
  output authority. Stable successful final rehash and restoration paths record
  it; completion-pending, failure, incomplete, demoted, and share-in-place rows
  clear or forbid it. Startup uses the fingerprint only as a cache key: a
  precise safe match skips hashing, while missing, stale, or coarse baselines
  force whole-file ED2K verification and persist a refreshed identity. Tests
  cover SQL round trips and invalid states, completion lifecycle transitions,
  missing and stale baselines, restoration, hidden-row pending intent,
  corruption, demotion, and share-in-place exclusion. Validation: `cargo fmt
  --all --check`, `git diff --check`, `cargo check --workspace --all-targets`,
  strict Clippy for metadata, `emulebb-ed2k`, `emulebb-core`, and
  `emulebb-daemon`, 49 focused metadata tests, four completion-rehash tests, 15
  payload-reconciliation tests, all 1,108 ED2K unit tests, all 414 core unit
  tests, and all 70 daemon unit tests passed.
- `251bdba3` hardens the live final-completion barrier around one authoritative
  payload handle. Native fingerprints now come from the same no-follow handle
  used to identify and size the file on Unix and Windows; final rehash runs
  under lifecycle and manifest serialization, withdraws the pending payload
  from the shared catalog, hashes that handle, and verifies both handle
  stability and its current path binding before publication. Filesystem
  authority failures preserve verified pieces in a retryable pending state
  instead of misclassifying them as content corruption. Missing payloads reset
  atomically and idempotently for redownload, while oversized regular files are
  quarantined rather than truncated. Completed and incomplete catalog hydration
  now revalidates current manifest state under the per-hash lock, refuses stale
  pending snapshots, and does not overwrite live upload counters. Regressions
  cover restart finalization, earlier-piece mutation, pre-finalization catalog
  exclusion, oversized and missing payload recovery, wrong path types, Unix
  symlinks, stale completed hydration, and stale incomplete hydration.
  Validation: `cargo fmt --all --check`, `git diff --check`, strict Clippy for
  `emulebb-ed2k`, all 1,112 ED2K unit tests, all 414 core unit tests, all 70
  daemon unit tests, and `cargo check --workspace --all-targets` passed. Plain
  `-D warnings` remains blocked only by seven unrelated pre-existing
  `unfulfilled-lint-expectations`, so the strict ED2K run allowed that lint and
  denied every other warning.
- `d70694b0` binds share-in-place ingest hashing, file size, and the persisted
  source fingerprint to one no-follow open handle. The combined MD4/AICH builder
  now accepts that existing reader instead of reopening the pathname. Ingest
  verifies exact handle metadata before and after hashing and verifies that the
  current path still resolves to the same native identity before publication;
  a missing precise identity is a hard failure rather than an unfingerprinted
  share. Exact in-operation equality remains distinct from the conservative
  `safely_matches` cache-reuse rule, so valid coarse-timestamp files can still
  be freshly hashed. Windows holds the ingest source with read sharing only,
  excluding concurrent writers and path deletion for the full hash operation;
  Unix rejects symlinks and detects path replacement after hashing. Regressions
  cover the shared reader hash-builder, normal progress reporting, Windows
  writer exclusion, deterministic Unix path replacement, and Unix symlink
  rejection without manifest or catalog publication. Validation: `cargo fmt
  --all --check`, `git diff --check`, strict Clippy for `emulebb-ed2k`, the
  focused ingest and combined-hashset tests, and all 1,113 ED2K unit tests
  passed.
- `83806b47` closes the live upload-authority gap after publication. Completed
  canonical payloads and share-in-place sources are opened without following
  symlinks and must still match their persisted native fingerprint before any
  bytes are served. Windows source readers hold read-only sharing so writers and
  deletion cannot race a live read; Unix readers verify the same handle again
  after the read. Missing or replaced authority is withdrawn from the catalog;
  canonical completion is moved back to final-rehash-pending, while invalid
  share-in-place identity is cleared until rehash. Managed incomplete payloads
  cannot use whole-file timestamps because later pieces legitimately mutate the
  same file, so each advertised ED2K part is read into one stable snapshot and
  MD4-validated before its fragments are served. A still-invalid part is
  durably requeued and removed from catalog ranges, while stale open/read
  failures are revalidated under the manifest lock before any demotion. Cached
  writer handles are invalidated first so redownload cannot write into a
  detached inode after atomic `pieces.bin` replacement. Startup and live
  catalog admission now share one authority predicate: completed canonical
  entries require a payload fingerprint, completed source-backed entries
  require a source fingerprint, incomplete entries require acquired MD4
  authority plus verified ranges, and final-rehash-pending entries are never
  exposed. Live relocation updates canonical manifest identity immediately;
  identity-changing relocation de-offers until rehash, and relocating a
  secondary duplicate source no longer rewrites canonical path, name, or
  catalog metadata. Shared-source fallback now accepts only present sources
  whose current no-follow fingerprint safely matches persisted evidence.
  Regressions cover trusted and identity-changing relocation, same-path source
  replacement, secondary-source relocation, Windows writer exclusion, Unix
  post-open mutation, completed canonical replacement, incomplete-part
  corruption, missing payload, stale missing-path recovery, catalog hydration
  without MD4 authority, and atomic partfile replacement followed by canonical
  redownload. Validation: `cargo fmt --all --check`, `git diff --check`, 49
  metadata unit tests, 414 core unit tests, all 1,123 ED2K unit tests, focused
  authority regressions, `cargo check -p emulebb-ed2k`, and strict Clippy for
  metadata, ED2K, and core with every warning denied except the repository's
  unrelated pre-existing `unfulfilled-lint-expectations` diagnostics passed.
- `11995e10` serializes synchronous and detached shared-directory reloads through
  one core-owned async gate. Detached requests still coalesce through the
  existing running/pending state, but neither API can now overlap catalog and
  manifest persistence with another reload in the same runtime. A deterministic
  regression holds the gate, schedules both APIs, proves both remain blocked,
  and verifies that the detached worker drains after release. Validation: the
  focused coordinator regression, strict core Clippy, formatting, and diff
  checks passed.
- `d41daea8` repairs the Windows CI failure that exposed a second persistence
  boundary beyond the in-core gate. `upsert_transfer_manifest` previously began
  a deferred WAL transaction, read destructive-deletion authority, then tried
  to upgrade to a writer after another SQLite connection could commit. SQLite
  correctly rejected that stale snapshot immediately with
  `SQLITE_BUSY_SNAPSHOT`; the configured busy timeout cannot retry an unsafe
  snapshot upgrade. Manifest upserts now begin `IMMEDIATE`, acquiring writer
  authority before their first read. A two-connection regression holds an
  existing writer, proves the manifest upsert waits, then commits and verifies
  the contender succeeds. Validation: 50 metadata unit tests, 415 core unit
  tests plus all core integration/doc tests, 20 consecutive runs of the exact
  Windows restart regression, strict metadata/core all-target Clippy,
  formatting, and diff checks passed.
- Rust PR #126 merged to protected `main` by rebase on 2026-10-16. All required
  CI and CodeQL checks passed, including Linux, macOS, Windows, cargo-deny,
  strict format/Clippy policy, workflow lint, and live REST/OpenAPI conformance.
- `cfe73bfc` makes persisted completion time transition-driven instead of
  rewrite-driven. One shared authoritative-download predicate excludes
  final-rehash-pending and share-in-place rows; prior state is captured before
  the known-file completion bit changes. Transfer completion time survives
  metadata-only updates, delivery-state rewrites, and temporary demotion, while
  a later authoritative recompletion advances both transfer and history time.
  Transition time is monotonic against retained transfer/history evidence, and
  legacy completed rows with a null transfer timestamp repair from history
  without refreshing it. Deterministic regressions cover first completion,
  metadata and delivery rewrites, demotion/recompletion, final-rehash and
  share-in-place boundaries, legacy repair, manifest recreation, and wall-clock
  rollback. Validation: 53 metadata tests, 1,123 ED2K tests, 415 core unit tests
  plus all core integration/doc tests, strict metadata Clippy, formatting, diff
  checks, and independent review with no remaining findings passed. Rust PR
  #128 merged to protected `main` by rebase on 2026-10-16 after all required CI
  and CodeQL checks passed, including Linux, macOS, Windows, cargo-deny, strict
  format/Clippy policy, workflow lint, and live REST/OpenAPI conformance.

Payload isolation, validation, persisted completed-transfer visibility, the
explicit delivery state model, and startup output reconciliation are complete.
In-process lifecycle serialization and the verified-but-undelivered removal
rule are also complete. Continue with schema 35 persisted destructive-deletion
intent integration: the normal/runtime visibility partition, shared output
identity classifier, intent-first retryable cleanup, and strict pre-exposure
startup recovery are complete. Unmanaged transfer paths can no longer be
silently adopted by a future download, and startup now reconciles safe orphan
residue while preserving/reporting unknown bytes. Persisted incomplete rows can
no longer resume or publish progress unsupported by their internal payload.
The focused follow-up audit found and closed the completed-download startup
authority gap: completed catalog exposure is deferred until reconciliation,
canonical verified download bytes beat same-hash shared-source rows, and every
managed internal payload now reaches startup in one of three explicit states:
verified canonical authority, restored canonical authority, or demoted
redownload state with uncertain bytes quarantined. Startup now skips whole-file
rehashing only when a precise persisted canonical-payload identity safely
matches; missing, stale, or coarse baselines still rehash and refresh. Final
completion now hashes one verified no-follow handle and stale hydration cannot
republish its pending state. Share-in-place ingest now derives its hash and
fingerprint from one verified no-follow handle and excludes Windows writers
during hashing. Live canonical, share-in-place, and incomplete upload reads now
fail closed against replaced or corrupt authority and reconcile persisted and
catalog state before reuse. Schema 39 delivery ownership, schema 40 output-
tombstone recovery, and schema 41 owned-fingerprint invariants close most
namespace-durability and owned-artifact reclamation boundaries. The second
independent review's deletion ordering, startup availability, tombstone
identity, and test-isolation blockers are closed in five granular commits;
schema 42 makes transfer-directory ownership durable and immutable with first
delete intent. The unavoidable portable path-delete race is documented as a
low-severity Beta 3 residual. The item remains implementation-active; Rust PR
#129 stays draft pending the canonical gate, third independent review, and
fresh protected-main CI.
