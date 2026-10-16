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
- [ ] Delivery and destructive deletion serialize and recover without orphan
      output, hidden-only success, or a row whose authorities are both absent.
- [ ] Filesystem namespace durability precedes SQLite advancement at every
      cross-domain commit boundary supported by the platform.
- [ ] Owned stale copy/intention artifacts are reclaimed without touching
      unrelated user files.
- [ ] Completion and history timestamps change only on a true completion
      transition.
- [ ] The canonical Rust quality gate and protected-main CI pass.

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

- `578e1237` removes same-volume hard-link delivery. Every completed download is
  now materialized through an independent temp-copy plus no-clobber install, so
  edits to the operator-facing file cannot mutate retained verified upload
  bytes. The aggregate disk guard now reserves the additional full payload on
  same-volume layouts as well as cross-volume layouts. A runtime regression
  test mutates the delivered file and proves `pieces.bin` remains unchanged; a
  core reservation test proves an empty same-volume download reserves both the
  piece store and delivered copy. Validation: all 1,073 `emulebb-ed2k` tests
  and all 410 `emulebb-core` unit tests plus integration/doc tests passed through
  the workspace harness.
- `c7287e2e` completes the payload-isolation/validation slice. Delivery now
  requires a regular source with the expected size before creating the
  destination, except for the explicit zero-byte/no-piece-store case. Every
  newly installed copy is rehashed with canonical ED2K semantics before the
  manifest can record it; failed verification removes the untrusted output.
  Runtime and helper regressions cover a missing non-empty piece store, a
  truncated source, a wrong installed hash, manifest non-advancement, and
  cleanup of the rejected destination. Validation: all 1,076 `emulebb-ed2k`
  tests and doc tests passed through the workspace harness.
- `cc528ca7` completes the persisted completed-transfer visibility slice. The
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
- `5e640bad` introduces the explicit persisted delivery lifecycle and bumps the
  clean-profile schema from 33 to 34. Downloads start `pending`, share-in-place
  rows are `not_applicable`, and only a verified output committed with its path
  becomes `delivered`. SQLite and the metadata API reject incoherent state/path
  combinations; pending retry selection now uses the state instead of nullable
  paths. Core and the ED2K runtime also use the state as delivery authority and
  return a first-class `NotRequired` outcome for share-in-place files.
  Validation: `cargo fmt --all --check`, all 48 `emulebb-metadata` tests, all
  1,076 `emulebb-ed2k` tests, and all 411 `emulebb-core` unit tests plus
  integration/doc tests passed through the workspace harness.
- `44cc0ba6` completes startup verification and deterministic reconciliation of
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
- `9b37e713` introduces one per-transfer lifecycle gate shared by delivery,
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
- `bf85f467` bumps the clean-profile schema from 34 to 35 and adds a terminal
  `delete_requested_at_ms` marker with a partial recovery index. The metadata
  contract now has explicit idempotent request, ordered pending-intent scan,
  and intent-gated finalization operations. Repeated requests preserve the
  original intent/update timestamps, ordinary manifest upserts cannot clear an
  intent, and finalization refuses an unmarked transfer. The existing metadata
  deletion transaction was factored through one shared known-file cleanup path.
  Validation: `cargo fmt --all --check` and all 49 `emulebb-metadata` tests plus
  doc tests passed through the workspace harness.
- `44fdbb06` makes a pending destructive deletion a terminal visibility
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
- `43a5cfc1` extracts one conservative delivered-output identity classifier
  shared by recorded-output reconciliation, pending-intent adoption, collision
  handling, and installed-output verification. It distinguishes a missing path
  from matching canonical bytes and a foreign occupant, keeps the native
  fingerprint fast path, falls back to a full ED2K hash, and rejects identity
  changes observed across hashing. This gives destructive cleanup the exact
  primitive needed to delete only the recorded file still owned by the
  transfer. Validation: `cargo fmt --all --check` and all 1,084
  `emulebb-ed2k` tests plus doc tests passed.
- `0421e046` makes the durable deletion intent the operation's commit point.
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
- `9a7f2059` completes pre-exposure recovery of durable destructive-deletion
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
- `9b8e27fc` closes silent adoption of untracked transfer-root content. A new
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
- `5edb4ad4` adds the pre-exposure transfer-root inventory without introducing
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
- `395c015f` adds a strict pre-exposure authority barrier for every persisted
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
The focused follow-up audit found the remaining authority gap in completed
downloads: the progressive runtime constructor catalogs completed rows before
any internal-storage validation, completed `pieces.bin` paths do not reject
symlinks/wrong types, and upload source selection ignores a separately verified
`delivered_path`. Next generalize the storage barrier to completed downloads and
defer initial completed-catalog hydration until their internal/delivered
authority is classified. Then add a verified delivered-output serving fallback
and a live reader-open guard so post-startup path replacement also fails closed.
