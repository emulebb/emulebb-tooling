---
id: RUST-REF-008
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/96
title: Reduce large-library metadata and scan I/O amplification
status: OPEN
priority: Major
category: refactor
labels: [rust, sharing, performance, io, sqlite, storage]
milestone: post-beta-polish
created: 2026-10-03
source: 100k SSD campaign, interrupted multi-HDD campaign, and 2026-10-03 I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/96. This local document is retained as the durable engineering spec and evidence record.

# RUST-REF-008 - Reduce large-library metadata and scan I/O amplification

## Comparative Measurement Acceptance

- [ ] Compare cold/warm 100,000-file ingestion and bounded watcher mutation with
      matched current-stable aMule/Rust inputs on the same storage/settings.
- [ ] Record elapsed time, logical versus physical I/O, commit/query counts,
      peak/steady RSS, API latency percentiles and correctness/restart outcomes.
- [ ] Preserve shared MD4/AICH reads and existing persisted harness ownership.
      Measurements select bounded repairs here; historical throughput does not
      establish overall superiority or authorize an unbounded real-media scan.

## Summary

Reduce the database, catalog, and filesystem-metadata amplification that now
dominates large-library cold ingestion and mutation. The combined MD4/AICH
payload path is already close to one physical read of the library; the next
large gain is to preserve that behavior while avoiding per-file durable commits,
repeated membership work, and unnecessary media-enrichment I/O.

Retain bounded, representative multi-HDD measurement as the final proof lane.
Do not restart an unbounded real-media scan under this item.

## Current State

The deterministic 100,000-file SSD fixture passed initial scan, warm reload,
one-percent mutation, long-path, watcher, persistence, and cleanup checks:

- The 10.49 GB cold library produced about 10.75 GB of physical reads, showing
  that MD4 and AICH already share one effective payload pass.
- Cold ingestion took about 905 seconds and produced about 16.13 GB of physical
  writes even though the final database was about 134 MB.
- A warm unchanged reload reused all 100,000 files in about 2.06 seconds without
  payload hashing.
- Rehashing a 1,000-file, 100 MB mutation reported about 25.56 GB of process
  reads and about 399.8 MB of physical writes.

The shared-library domain refactor in `RUST-REF-017` replaced the old
share-in-place transfer manifest and `shared_file_sources` table with
`verified_local_content`, `local_file_instances`, and
`shared_file_memberships`. The old stale-source lookup hypothesis is therefore
retired. Measure the current local-content commits, root membership updates,
and optional media enrichment before assigning process logical reads to a cause.

The cold-cohort entry limit currently counts directories and errors, which can
starve publishable files in directory-heavy prefixes and is not fair across
storage domains. The exhaustive planner also materializes duplicate path, key,
and domain strings for the complete tree before ordinary hashing begins.

An intentionally stopped real-media HDD campaign committed 4,947 unique hashes
covering about 589 GB with no invalid hash or scan failures. That is sufficient
correctness evidence, not authorization for another complete media-library run.

## Why This Matters

The schema consolidation implements a bounded portion of this item: indexed
catalog lookups, a revision-controlled session projection for library pages,
incremental search/transfer/Kad persistence, membership reconciliation without
blanket withdrawal, and FTS updates only when indexed text changes. Synthetic
regressions cover 100,000 distinct files and 100,000 aliases, stable child rows,
transaction rollback, and invalidation across connections. Strict tables,
checked numeric mappings, compact composite keys, and complete child-key index
coverage strengthen the current storage contract.

This does not complete the bounded writer, filesystem scheduling, optional
media-enrichment, or physical-I/O measurement work below. The schema remains
current-only; these changes add no end-user upgrade or migration path.

Per-file WAL flushes and repeated metadata scans make a library of many small
files much slower than its payload size suggests. If the profile database and
shared library occupy the same mechanical disk, alternating payload reads and
database flushes can also create avoidable seeks. This is the largest measured
remaining large-library I/O cost.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/ingest.rs`
  `ingest_local_file_inner`
- `crates/emulebb-metadata/src/local_file_store.rs`
  `upsert_verified_local_content`
- `crates/emulebb-metadata/src/shared_membership_store.rs`
  `replace_root_memberships`
- `crates/emulebb-metadata/src/schema.sql` local content and membership tables
- `crates/emulebb-core/src/shared_directories.rs`
  `forget_stale_shares` and `hash_reload_targets`
- `repos/emulebb-build-tests/emule_test_harness/rust_shared_library_io.py`

## Intended Shape

- Profile local-instance lookup and membership replacement under a 100k-file
  mutation before changing indexes or batching boundaries.
- Introduce a bounded single metadata-writer path for initial share ingestion.
  Preserve `synchronous=FULL`, but commit small file/time-bounded groups instead
  of one transaction per file. Keep the first publishable cohort responsive.
- Do not let a large transaction monopolize the shared SQLite connection; record
  commit latency and keep REST/network metadata operations responsive.
- Publish the hash/name/size entry before optional media enrichment. Persist
  derived media fields through the bounded writer, or combine them with the
  local-content transaction when doing so does not delay first publication.
- Instrument SQLite transaction count, WAL bytes, statement/page reads, media
  probe bytes, and stale-removal work so logical-read amplification is attributed
  rather than inferred.
- Extend the existing Python harness with per-physical-disk file and byte
  ceilings, deterministic selection, resumable checkpoints, and redacted
  per-disk evidence.
- Make cold-cohort selection count publishable files and schedule fairly across
  storage domains. Stage exhaustive work per domain instead of retaining a
  duplicate whole-tree string graph before hashing starts.

## Scope Constraints

- Preserve one sequential payload hash stream per mechanical storage domain.
- Do not weaken download-manifest crash consistency or change ED2K/AICH results.
- Do not delay connectivity or the progressive startup publication delivered by
  `RUST-BUG-106`.
- Real-media runs are read-only and bounded by default. Do not retain private
  media names, complete paths, or content-derived details in committed evidence.
- Storage-domain mapping and native path identity are owned by
  `RUST-REF-009` and `RUST-BUG-107`; watcher rescan policy is owned by
  `RUST-REF-010`.
- Do not tune the 180 KiB hash buffer until metadata amplification is removed
  and profiling identifies syscall overhead as a material remaining cost.

## Acceptance Criteria

- [ ] A 1,000-file mutation has no per-hash full-table work in the current
      local-instance and membership schema, verified by query plans and counters.
- [ ] Initial share persistence uses bounded batching while keeping verified
      local content crash-consistent and the first publication cohort prompt.
- [ ] Optional media enrichment does not block a newly hashed file from entering
      the live publication catalog.
- [ ] The harness records payload bytes, process/physical reads and writes,
      SQLite transactions/WAL growth, wall time, throughput, and failures.
- [ ] A repeated 100k SSD cold/warm/mutation campaign shows a material reduction
      in cold physical writes and mutation logical reads against the retained
      baseline without increasing payload physical reads materially.
- [ ] The Python harness can select deterministic bounded cohorts per physical
      HDD and resume them from checkpoints.
- [ ] A bounded multi-HDD report proves one sequential hasher per mechanical
      storage domain and concurrency only across independent domains.

## Validation

- Metadata schema/query-plan tests for local-instance lookup and membership
  replacement.
- Crash/restart tests around partial batches and first-cohort publication.
- Hash/ingest equivalence tests preserving MD4, ED2K part hashes, AICH, media
  metadata, long paths, and catalog contents.
- Python harness tests for counters, cohort limits, checkpoints, and redaction.
- Bounded SSD comparison followed by bounded multi-HDD evidence below
  `EMULEBB_WORKSPACE_OUTPUT_ROOT`.

## Accepted Hot-Path Cache Follow-up (2026-11-06)

The approved async-I/O backlog review identified repeated ignore-policy work in
`shared_file_api.rs::share_native_local_file_with_progress`: each file can call
`load_shared_file_ignore_policy`, read the custom/default rules from SQLite, and
compile a new glob set. The bulk scan has a policy snapshot, but that does not
eliminate this per-file ingest boundary. At 100K files, repeated small queries
and compilation are amplification even when payload hashing is already one pass.

Own the compiled-policy cache here, with a configuration revision and explicit
invalidation on every rule change. A job may use an immutable snapshot with a
defined revision-change/replan policy, or read the current cached policy at
admission; do not silently freeze rule edits until a long hash campaign ends.
No per-file SQLite query or glob compilation should be needed on the unchanged
policy path. Keep the same cache usable by reload, direct API, and watcher
ingestion instead of adding an independent cache to every caller.

RUST-REF-016 owns the execution boundary for reading/persisting rules and
publishing invalidation. RUST-REF-019 owns executor placement for large index
construction/sorting; retain one ownership boundary for query amplification
and one for CPU scheduling. This is post-beta backlog work and does not require
another unbounded real-media run.

- [ ] Rule reads/compilations scale with configuration revisions and jobs, not
      the number of files hashed under an unchanged policy.
- [ ] A rule edit atomically invalidates the cache and has tested semantics for
      queued/in-flight work without publishing a stale policy generation.
- [ ] Synthetic measurements record query count, compile count, commit latency,
      CPU time, and payload bytes before/after without weakening durability.

## Accepted Combined-Hash and Recovery Persistence Follow-up (2026-11-07)

The AICH/I/O review was revalidated against main `e3372aba` and branch
`58595576`. Normal local ingest already reads a 184,320-byte buffer once,
updates MD4, and calculates each SHA-1 leaf from those same bytes. It retains
packed recovery leaves and part roots; final download verification does the
same in its existing whole-file pass. These are synchronous buffered readers
inside blocking workers, awaited by async callers. Native async disk I/O or
two independent digest streams is not a prerequisite for good HDD throughput.

Preserve that combined reader. Full-part recovery leaves occupy 1,060 bytes
per 9,728,000 payload bytes, about 0.011 percent before SQLite pages, indexes,
and WAL. Do not mistake their compact data size for the cost of committing
them individually across a large library.

The current normal ingest path calls `upsert_verified_local_content`, then
`store_aich_recovery_set`, then optional media extraction/update. The first
two storage operations open separate transactions; the worker awaits media
work before returning to its next file and before its caller finishes catalog
publication. Bounded profile-exchange import batches are already implemented;
they do not batch normal local ingestion. Multiple physical-disk workers still
converge on one metadata connection. Instrument current behavior before
attributing the historical read/write amplification to a particular query.

Extend the one bounded persistence owner from RUST-REF-016 with file-count,
byte-count, and elapsed-time batch ceilings. Bound retained path/fingerprint,
hashset, and recovery allocations, not only item count. Keep interactive reads,
transfer checkpoints, and first-cohort publication responsive. Publish a new
entry after its mandatory content/path evidence is durably committed and
root-admitted; optional enrichment must not delay that transition.

Retain atomicity for each complete recovery set, including aliases with
enriched part hashes. An invalid/conflicting optional set must roll back only
that set while retaining mandatory content and accepted neighboring sets.
SQLite transaction-abort errors may end the containing transaction, not merely
a savepoint: preserve the `58595576` fix and test both conflict and abort paths.
Separate storage unavailability from invalid input; never report a failed
durable commit as a successfully rejected optional record. Any retry must be
bounded and idempotent without a hidden payload rehash.

The completion path changed after the earlier review: `e0e68ad6` attempts to
save available computed recovery before publishing completion so a crash does
not leave a successful cached-tree computation unretained. Optional cache
failure still permits durable valid MD4 completion. Preserve both invariants;
do not reinstate the older completion-before-cache crash window as a batching
optimization. RUST-BUG-165 separately owns trusted digest disagreement, which
is an integrity conflict rather than an optional-storage failure.

Use the existing small magic sniff to skip irrelevant media parsers and retain
format-specific safety bounds. Where useful, feed bounded prefix/trailer
evidence already encountered by the mandatory reader to enrichment instead of
reopening every file. Account separately for remaining media seeks and bytes.
Do not turn this into a second metadata parser or force enrichment to wait
behind an entire library before publishing any result.

Additional acceptance criteria:

- [ ] Cold normal ingest commits bounded groups rather than mandatory and
      recovery metadata once per file; measurements distinguish commit count,
      mutex/queue wait, SQL work, WAL bytes, fsync latency, and payload reads.
- [ ] Optional recovery conflict and transaction-abort injection preserve
      accepted MD4 content and neighbor sets, with no partial complete-set rows
      and no false successful commit on storage failure.
- [ ] Crash injection before/after successful recovery storage and completion
      preserves the latest recovery-retention ordering and bounded restart work.
- [ ] Media enrichment is bounded and outside the first-publication critical
      path; irrelevant formats retain their tiny sniff rather than a 2-MiB read.
- [ ] Existing import enrichment and sparse-reimport tests retain richer MD4/
      AICH evidence without payload reads or alias/path rebinding.
- [ ] A current-head bounded cold/warm/mutation report replaces assumptions
      drawn from the older 100K baseline and separates logical from physical I/O.

RUST-REF-009 owns shared disk admission; RUST-REF-019 owns CPU placement;
RUST-REF-021 owns delivery verification reads; RUST-REF-022 owns incomplete
recheck ranges. Keep one owner for each boundary. No broad operator-library
campaign or new implementation is authorized by this backlog update.

## Notes

The retained SSD baseline is
`${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-shared-library-io-20261003T153209Z-11012.json`.
The startup-publication overlap report is
`${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-shared-library-lan-startup-20261003T183046Z-16340.json`.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section evidence-gap (existing): Owning harness/current-head evidence must distinguish raw local captures from scrubbed shared artifacts; coordinate with testing-harness report.
- `emulebb-rust-prompt_audit_findings_media-metadata.md` section 3.2 (existing): Existing REF008 explicitly owns bounded optional enrichment and extra reads. Avoid timeout wrappers that merely abandon a still-running blocking task.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section scale-proof (existing): The aMule scaling wave is inspiration, not evidence of the same defect in Rust. Existing storage-domain, scan-I/O, async SQLite/filesystem/CPU and upload-performance items own the remaining work.

### Scoped Follow-up Acceptance

- [ ] Shared evidence omits operator-private values; raw captures never become public issue attachments by default.
- [ ] Measure probe bytes/work and make optional enrichment bounded outside first-publication critical path.
- [ ] Use bounded representative benchmarks and latency evidence.
- [ ] Reuse existing 100k fixture and cross-platform owners.
- [ ] Required Beta 3 Windows/Linux evidence is selected under #142; optional platforms remain parallel.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

**Reviewable branch spec:** https://github.com/emulebb/emulebb-tooling/blob/fix/stock-hash-share-tree/docs/products/emulebb-rust/active/items/RUST-REF-008.md
