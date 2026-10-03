# emulebb-rust Large-Library I/O and Portability Review

**Reviewed:** 2026-10-03

**Scope:** shared-directory enumeration, incremental planning, MD4/AICH hashing,
media metadata, SQLite persistence, watcher ingestion, startup publication,
long paths, Unicode, and Windows/Linux/macOS behavior.

## Assessment

The tested Windows path is functionally sound and physically efficient when
reading payloads. The combined hash implementation reads MD4 and AICH in one
sequential pass, unchanged libraries avoid payload reads, shared files remain in
place, and connectivity/publication no longer wait for the complete library.

The next performance work belongs primarily in SQLite/catalog mutation rather
than the payload hash loop. Cross-platform equivalence also needs native storage
and path identity instead of string-based proxies, and watcher reconciliation
needs an explicit I/O budget.

## Retained Evidence

The deterministic SSD fixture contained 100,000 files totaling 10.49 GB,
including 1,000 long paths up to 420 display characters.

- Cold ingestion completed with no hash or scan failures. It took about 905
  seconds, read about 10.75 GB physically, and wrote about 16.13 GB physically.
  The final SQLite database was about 134 MB.
- Warm reload reused all 100,000 files in about 2.06 seconds without payload
  hashing.
- The one-percent mutation rehashed 1,000 files/100 MB in about 66.5 seconds,
  with about 25.56 GB of process reads and 399.8 MB of physical writes.
- The LAN startup witness observed 8,596 shareable files while 91,407 hashes
  remained. The local eD2K server accepted the first 200 records and Kad
  keyword/source workers were active before ingestion completed.
- The two-peer Kad topology did not provide a completed STORE acknowledgement;
  it proves worker overlap, not remote Kad replication.

Retained reports:

- `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-shared-library-io-20261003T153209Z-11012.json`
- `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-shared-library-lan-startup-20261003T183046Z-16340.json`

## Improvements Present on Current Main

- MD4 and AICH share one sequential payload read with progress accounting.
- Share-in-place avoids copying a large source library into the transfer store
  and avoids one transfer directory per shared file.
- Directory walks reuse their metadata result. Only planned hash targets are
  re-statted immediately before their payload read.
- Windows resolves one physical-disk key per root, then uses one hasher per disk
  and concurrency only across distinct disks.
- Path, size, and mtime reuse skips unchanged payloads; prior unchanged failures
  are also cached.
- Persisted catalogs hydrate incrementally and a cold empty profile builds a
  bounded small-first publication cohort before the exhaustive walk.
- Blocking scan, hash, and SQLite work is kept off asynchronous runtime workers.
- Media parsing is bounded, cover-art loading is disabled, and persisted media
  metadata avoids repeated extraction on warm startup.
- Windows shared-directory paths use verbatim long-path form, while UI/API paths
  return normal display form.
- Watcher events settle before hashing, duplicate path actions coalesce, and a
  paired rename is metadata-only when content identity remains unchanged.

## Priority Findings

### 1. Metadata writes dominate cold ingestion

Each newly hashed share performs a `synchronous=FULL` manifest transaction and
normally a separate media-metadata update. The measured physical-write volume is
far larger than the final database and makes small-file libraries commit-bound.
Use bounded batching without weakening download crash consistency, and decouple
derived media enrichment from first publication.

Tracked by [RUST-REF-008](items/RUST-REF-008.md).

### 2. Stale-source mutation appears to repeat large SQLite scans

`shared_file_sources` is queried/deleted by `known_file_id` without a dedicated
index and stale hashes are removed individually. Add the index, batch stale
deletion, and record query-plan/statement evidence before attributing all logical
reads.

Tracked by [RUST-REF-008](items/RUST-REF-008.md).

### 3. Unix roots do not identify independent storage domains

The non-Windows disk key uses the first path component. Absolute Linux/macOS
paths therefore collapse to `/` and one global hasher. Use native device identity
and prove same-device serialization plus cross-device concurrency.

Tracked by [RUST-REF-009](items/RUST-REF-009.md).

### 4. Unicode display normalization is being used as path identity

NFKC and platform-wide case rules can merge distinct legal names. The native
path BLOB currently contains display-string bytes rather than a lossless native
encoding, and non-UTF-8 Unix names cannot pass all string boundaries. Separate
native identity from Unicode display/search values and incorporate stable file
identity where available.

Tracked by [RUST-BUG-107](items/RUST-BUG-107.md).

### 5. Watcher safety can become whole-tree I/O amplification

The Windows two-action threshold protects against silent watcher overflow but
can turn ordinary multi-file activity into repeated full reconciliations. Direct
watcher hashing is also globally serial rather than storage-domain-aware. Use one
bounded trailing reconciliation generation and the common per-domain queue.

Tracked by [RUST-REF-010](items/RUST-REF-010.md).

### 6. Scale evidence is Windows/ASCII-heavy

The 100k fixture proves long ASCII paths, while Unicode is covered only by
smaller focused tests. Native path lengths, normalization/case collisions,
multi-mount scheduling, and macOS watcher recovery need capability-aware scale
evidence.

Tracked by [RUST-CI-008](items/RUST-CI-008.md).

## Secondary Findings

- The cold cohort entry bound counts directories and errors, so a directory-heavy
  prefix can yield few or no publishable files. Candidate limits are per root and
  selection is not fair across storage domains.
- The full scan materializes and duplicates path/key/domain strings for the
  complete tree before normal hashing starts. This is acceptable at 100k but
  should become per-domain staged work before targeting substantially larger
  libraries.
- Symlinked files/directories are not followed. Hard links and other aliases do
  not use file identity for initial deduplication. The intended policy should be
  explicit.
- The 180 KiB hash buffer is not a current priority: physical-read evidence
  already shows an effective one-pass payload path. Revisit it only after
  database amplification is removed and profiling shows syscall overhead.
- The macOS watcher test describes the platform as compile/test-only while the
  release workflow emits macOS packages. Support policy and evidence must agree.

## Recommended Order

1. Index and batch stale-source deletion, then repeat the one-percent mutation.
2. Batch initial manifest persistence and make media enrichment asynchronous,
   then repeat the cold/warm 100k SSD campaign.
3. Correct Unix storage-domain identity and add controlled two-device proof.
4. Migrate path identity to a lossless native representation.
5. Bound watcher reconciliation and reuse the per-domain scheduler.
6. Add the Unicode/native-length fixture cohorts and run the cross-platform
   matrix before bounded multi-HDD media evidence.
