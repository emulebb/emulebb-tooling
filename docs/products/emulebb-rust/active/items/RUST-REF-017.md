---
id: RUST-REF-017
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/235
title: Separate verified shared files from download transfers
status: IN_PROGRESS
priority: Major
category: refactor
labels: [rust, sqlite, sharing, transfers, api]
milestone: post-beta-polish
created: 2026-11-05
source: Beta shared-library domain review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/235. This record owns the durable engineering scope and evidence.

# RUST-REF-017 - Separate verified shared files from download transfers

## Goal

Make a completed local file a verified library member under a recursive
explicit or implicit Incoming/category root. A download transfer exists only
while bytes are being acquired, verified, or delivered. Keep stock eMule
partial-file sharing, ED2K/Kad publication, and upload integrity.

## Design Boundaries

- One current SQLite schema; an incompatible profile fails startup and requires
  a fresh profile. There is no product migration, alias, fallback, or legacy
  transfer representation.
- Verified content owns MD4/AICH identity and reusable hashsets. Native path
  identity and fingerprint guard reuse; multiple paths may belong to one hash.
- Root membership owns sharing eligibility. Explicit roots and implicit
  Incoming/category roots can overlap without canceling each other. Offline
  roots withdraw publication immediately and rejoin after verification.
- A completed download is delivered once, admitted to the library, and removed
  from active transfers. Crash-safe retirement reclaims only its owned internal
  piece store; delivered output and path-independent download history survive.
- Custom ignores are case-insensitive file-name glob patterns across roots.
  Built-in safety ignores remain configurable. There is no exact-file unshare.
- REST, OpenAPI, embedded WebUI, metadata schema, and tests change together.

## Acceptance

1. A root scan or live watcher shares eligible complete files without creating
   download rows. Multiple paths for one hash preserve independent membership.
2. A completed network download becomes a local share and leaves the transfer
   list. Restart and cleanup preserve its bytes and history without rehashing
   the delivered copy.
3. A partial download remains servable only for verified parts; source exchange,
   server offers, and Kad publication use the correct content or transfer view.
4. A replaced file, directory, or fingerprint cannot inherit verified status or
   be deleted by stale transfer cleanup.
5. Pattern ignores affect scans, direct admission, and live watching. The REST
   and WebUI contract contains no exact-file exclusion path.
6. Fresh-schema tests, local Kad transfer tests, REST contract tests, WebUI
   tests, formatting, and scoped lint checks pass.

## Progress

The `feature/shared-library-domain` Rust branch has granular pushed commits for
the verified local-content boundary, independent publication, implicit roots,
completion promotion, crash-safe piece-store retirement, and pattern ignores.
The clean schema is version 54. Persisted transfers are download-only:
`source_path_id`, `shared_file_sources`, and the `not_applicable` delivery state
are gone. A read-only protocol view may still describe a verified local file,
but that view is rejected by transfer persistence. Transfer deletion preserves
same-hash verified local content. Completion flags, acquired-hashset flags,
partial hashsets, and verified ranges are owned by the transfer row and cascade
on its deletion. Offline roots retire membership rows; a
successful rescan is required before they can rejoin publication, and the
health worker retries an incomplete rejoin. Metadata, core, eD2K, and REST
tests plus scoped lint checks pass. WebUI unit, browser, typecheck, and build
checks pass. An isolated Windows/WSL run with a stock ED2K direct-source link
confirmed the managed server offer, an active seeder upload, full 1 MiB leecher
receipt, transfer retirement into the shared library, and the delivered file's
SHA256. The local network assigns both clients LowID, so server-only discovery
did not transfer bytes; the direct-source hint supplies a deterministic peer
address for this upload proof.

A fresh review of the domain and workflow led to further branch commits. An
upload invalidation now withdraws a path only when its stored hash and native
fingerprint still match the failed read, so a concurrent watcher admission can
survive. Retired downloads are excluded from persisted completed offers and
their live offer is reconciled by hash. Clean-profile startup no longer handles
pre-SQL JSON resume manifests. Download pieces persist only `Missing` and
`Verified`; request and write progress is rebuilt from durable block evidence.
Malformed persisted block bitmaps fail loading instead of becoming a contiguous
prefix. REST lists only root members whose current stored fingerprint was
validated during this daemon session; restart clears that session gate and
progressive hydration or admission fills it. Watcher admissions, renames, and
removals refresh the affected hash instead of rebuilding the whole offer set.
REST path-ordered pages stream candidates into bounded application memory;
snapshot pages request a bounded hash page. Focused regressions, full metadata,
core, eD2K, and REST suites, REST contract tests, formatting, and scoped Clippy
passed across the review commits. A full root scan now commits memberships
before rebuilding offers once; refreshing each stale hash before that commit
made the 1,000-file watcher delete phase exceed its 10-minute limit while the
old memberships remained active. The corrected full-scan path has deletion and
replacement regressions, 463 passing core unit tests, and scoped Clippy.

The maintained SSD campaign passed on a fresh schema-54 profile with 100,000
files, 10,485,760,000 bytes, and 1,000 long paths. Its retained v6 report is
`rust-shared-library-io-20261105T234508Z-17904.json` under the configured
output root's `reports/emulebb-rust/shared-library-io/` directory (report
fingerprint `7f8b3bb46f6456dc`). The initial pass took 750.91 seconds. Watcher
create, modify, rename, and delete all passed in 56.19, 195.78, 198.61, and
157.17 seconds respectively; delete restored the 100,000-file catalog without
hashing. Both restarts exposed the validated 200-file cohort immediately and
hydrated the full 100,000-share catalog in 158.55 and 153.18 seconds. The
no-change reload hashed zero files in 41.08 seconds; the 1% mutation hashed
exactly 1,000 files and reused 99,000 in 79.54 seconds. All phase, watcher,
storage, REST, and global checks passed. The local Kad swarm integration test
again discovered shared-tree sources and completed two transfers after the
full-scan change.

A fresh domain review found one integrity fault in the verified-content upsert:
a second path with the same ED2K hash and size but a conflicting AICH identity
could replace the stored part hashsets while retaining the first path's AICH
root. The branch now rejects conflicting geometry, AICH root, or hashsets in
one transaction and leaves the first verified path untouched. The collision
regression, all 74 metadata tests, all 1,255 eD2K library tests, and scoped
metadata Clippy pass.

The serving-type follow-up is implemented as `Ed2kFileServingView`, a read-only
projection without download delivery, piece state, or retirement fields.
`Ed2kResumeManifest` is download-only and has no `source_path` or
`NotApplicable` delivery state. Download serialization rejects retired fields;
the protocol, upload presentation, shared metadata, and catalog hydration use
the serving view. Download code no longer branches around synthetic local
manifests. Upload part counts now use verified ranges, so fully written but
unverified parts are not reported as obtained. The 463 existing core and 1,255
existing eD2K unit tests, both new regressions, workspace compilation, scoped
Clippy, and the Kad discovery/transfer integration test passed.

The manual Kad bootstrap endpoint previously ignored its address and port after
validation. It now resolves an IPv4 endpoint, sends the requested bootstrap
exchange, performs the self lookup, and reports failure when no runtime is
available. A local integration test configures an unavailable startup seed and
proves that the explicit operation contacts the separately requested endpoint.
Live contact imports also report the number accepted by the DHT, rather than
the parsed count; the integration test covers a rejected duplicate-IP contact.

The live Kad proof passed again in run `20261106T095846Z`. The retained
report is `soak/rust-local-upload/20261106T095846Z/rust-local-upload-soak-result.json`
below the configured output root, with SHA256 fingerprint `cfe0ddef3ecfc469`.
It used product commit `f485d1d0` and harness commit `bc1c0d94`; the staged Linux
binary SHA256 was
`f5d4acf4f8f0237cb2e7099e1a288b2d4cdba55d8a6efea302215720c98c6e39`.

The seeder obtained an unbiased verified-open UDP result and passed the stock
source-publication gate, with one source publication and two acknowledged
contacts. The leecher disconnected from its eD2K server before accepting a
plain link without source hints. One Kad search returned the published type-6
source; the leecher sent `OP_DIRECTCALLBACKREQ` and accepted the ticketed inbound
callback. All 1,048,576 bytes transferred, the completed file entered the
verified library, and the download row retired. The exported delivered file's
SHA256 matched
`46d3a0d94568dcb37cd04aa69392e41436247cb1ea4d185b4787497c857e435b`.

This proof uses two staged Linux Rust daemons in WSL and a bounded Python Kad
rendezvous/firewall fixture on the existing Windows virtual interface. The
fixture carries no file payload and initiates no download. It returns a
successful firewall verdict only before receiving UDP from the requester;
subsequent biased requests are cancelled, preserving the stock rule. The local
seed is stored as an endpoint-only bootstrap setting, allowing the actual
response to teach its node ID instead of preloading an invented identity.
The selected network interface and one-ID-per-IP routing rule remain enforced.
This establishes the local product workflow; public-network and cross-client
Kad parity require their own evidence.

Fresh isolated profiles use bounded native Linux tmpfs filesystems because
this host's DrvFS rejects the atomic no-replace rename required by delivery.
The product retains that filesystem guarantee. The harness preserves storage
reserve headroom, archives both profiles before unmounting, and exports the
delivered file for host-side SHA256 verification. Both profile archives were
retained and the successful run reported no fixture, archive, or mount cleanup
errors. Windows and Linux release builds passed at the tested product commit.

The implementation and scoped acceptance evidence are in review in the single
[product implementation PR](https://github.com/emulebb/emulebb-rust/pull/237)
and its [harness companion](https://github.com/emulebb/emulebb-build-tests/pull/96).
Both retain the granular commits on `feature/shared-library-domain`. Keep this
item in progress until review and merge complete.

PR preparation aligned hosted CI with immutable companion revisions for the
breaking beta contract. It also updated the harness body-field inventory from
the retired exclusions route to `/shared-directories/ignores/defaults/{ruleKey}`.
All 120 contract parser tests and the complete router/OpenAPI metadata comparison
passed. The latest focused helper, upload, profile, wire, and server tests passed
108 tests, with one POSIX-only permission test skipped on Windows; formatting,
scoped Python lint, and the strict documentation build also passed.

The first hosted full-matrix review exposed a Unix filename regression: local
catalog and serving projections recomputed names with lossy Unicode conversion.
They now use the existing reversible native-name projection consistently across
catalogs, serving views, history, and reload diagnostics. The Unix regression
also checks the serving and publication names before and after restart. All 74
metadata tests, the Windows local-share tests, and scoped Clippy passed; current
Windows and Linux staged release builds completed with zero warnings.

The full harness review also found SQL seed helpers that still fabricated local
shares as completed transfers. Those helpers and the fingerprint-upgrade path
are removed. Stock imports populate only the pathless import cache; the daemon
owns native-file validation and library membership. Download seed/read helpers
use transfer-owned flags, hashsets, and verified ranges. Obsolete soak-schema
upgrade tooling is retired. Local library diagnostics and priority updates now
use local instances and verified content rather than removed source tables or
download completion flags. The affected import/download tests passed 72 tests,
REST conformance passed 28, and soak diagnostics passed 94.

A broader local harness run passed 3,369 tests and reported five environment
failures: stale canonical-checkout REST contracts, worktree-relative MFC document
paths, and an unrelated local aMule authority revision mismatch. Hosted harness
validation uses the pinned canonical companion checkouts; no authority checkout
or operator profile was changed to conceal those local limitations.
