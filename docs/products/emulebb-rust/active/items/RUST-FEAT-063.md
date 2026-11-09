---
id: RUST-FEAT-063
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/234
title: Carry semantic profile state into a fresh current-schema profile
status: OPEN
priority: Major
category: feature
labels: [rust, profile, export, import, sqlite, docker, portability]
milestone: post-beta-polish
created: 2026-11-05
source: operator-approved profile continuity design 2026-11-05
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/234. This local document owns the durable engineering contract.

# RUST-FEAT-063 - Carry semantic profile state into a fresh current-schema profile

## Summary

Provide an explicit semantic export/import workflow that carries important
eMuleBB Rust state from a source version into a fresh profile created by a
target version. The source binary reads only the source profile's exact current
schema and exports logical records. The target binary reads that versioned
bundle and writes only its own exact current schema.

This is deliberately not a SQLite schema upgrader. The target must never open,
copy, attach, migrate, or infer the source `metadata.db`, and normal daemon
startup must never perform automatic conversion.

## Current Baseline

RUST-REF-017 merged at product revision `7b295bda` with schema 54. Verified
content, native local-file instances, configured roots, and root membership
have separate ownership from active downloads. A current-session filesystem
check gates library eligibility after restart. This item must preserve those
boundaries when defining its semantic bundle.

The export/import commands remain future work. The earlier ad-hoc schema-44 to
schema-45 Python importer was retired during this reconciliation; it provides
no current-schema import path. Establish the first supported bundle with the
new implementation. Existing beta databases still require an entirely fresh
profile, with no retroactive database reader or migration added by this item.

## User Workflow

The daemon binary gains two offline operations, with final help text and names
following the existing Clap command style:

1. `export-profile --output <bundle>` runs with `--profile <source>` under the
   binary version that owns the source schema.
2. `import-profile --bundle <bundle>` runs with `--profile <target>` under the
   desired target binary and creates the target profile.

The target profile path must not already contain a user profile. Import is not
a merge, overlay, repair, or reset facility. The normal daemon must be stopped
for both operations, and the command must refuse a profile that is locked or
otherwise live.

This workflow supports container replacement by running the old image's export
against the old profile, then running the new image's import into a new mounted
profile directory. Switching the stack to the new directory remains an
explicit operator action after validation.

## Bundle Contract

- Produce one self-describing portable artifact with a stable magic/type,
  bundle-format version, exporter product version, source schema version,
  creation time, domain inventory, record counts, and content digests.
- Encode logical domain records with explicit field names and types. Do not
  embed the SQLite database, SQLite pages/WAL files, Rust memory layouts, or raw
  SQL statements.
- The byte-level archive/record encoding must be documented with the first
  implementation, deterministic for identical semantic input, streamable with
  bounded memory, and resistant to duplicate entries, unsafe paths, oversized
  records, truncation, and decompression bombs.
- Integrity digests detect corruption only. They are not authentication,
  encryption, or tamper-proofing.
- Version compatibility belongs to the bundle decoder. Supporting a declared
  older bundle format must not add an older database reader to product code.
- Unknown required domains or fields fail before target mutation. Optional
  extensions may be skipped only when the bundle explicitly marks them
  optional and the final import report names them.

## Export Semantics

- Open the source profile through the source binary's normal exact-schema
  persistence layer and obtain a consistent read snapshot.
- Require the source daemon to be stopped so SQLite and small profile files
  describe one bounded point in time.
- Normalize values into the bundle contract rather than exposing table and
  column names as the public compatibility format.
- Write to a temporary output and publish the completed bundle only after all
  records, counts, and digests are final. Never replace an existing output
  silently.
- Print a domain/count summary and a prominent plaintext-secret warning.

## Fresh-Target Import Semantics

- Require a non-existent or provably unused target profile destination. A
  generated bootstrap profile is acceptable only when the importer created it
  in the same operation and it contains no operator state.
- Validate the complete manifest, format compatibility, digests, record limits,
  identities, foreign-key relationships, required secrets, settings values,
  and duplicate rules before publishing a target profile.
- Build the target in a staging directory using the target binary's normal
  current-schema writers. Apply SQLite records transactionally and write small
  profile files atomically.
- Publish the staged profile only after all domains validate and commit. On
  failure, remove or quarantine the incomplete staging directory and leave the
  requested target path unusable as a profile.
- Produce a machine-readable and human-readable import summary with per-domain
  imported, skipped-optional, and rejected counts.
- Do not start networking, transfers, watchers, discovery, or the REST server
  as part of import.

## State Included

The bundle carries the following semantic state where the target version can
represent it:

- profile settings, including REST bind/authentication values and the existing
  REST API key from TOML; configured eD2K and Kad settings belong to the
  logical SQLite settings domains rather than additional bootstrap TOML keys;
- eD2K public user hash and secure-ident private key, preserving network
  identity rather than creating a new client identity;
- categories and their target paths, priorities, and current settings;
- friends;
- peer credit history and pinned secure-ident public keys;
- normalized eD2K server rows and their user-controlled metadata;
- normalized Kad routing contacts and bootstrap endpoints after
  RUST-FEAT-062, including persistence-relevant verification and UDP-key state;
- explicit shared-directory roots, pattern ignores, and built-in ignore
  overrides; configured Incoming and category destinations recreate their
  implicit roots through the target's current root-ownership rules;
- verified content identities, ED2K part/hashsets, AICH hashsets and master
  hashes, media metadata, and retained statistics, independently of downloads;
- native local-file identity and fingerprint evidence, with any exported
  membership recorded only as prior association evidence requiring normal
  target-daemon reconciliation;
- the imported-known-file cache used to avoid needless rehashing; and
- completed-download history and its retained logical metadata.

Paths retain their platform and lossless native representation and are not
required to exist during import. Never substitute a lossy display string for
native identity. A target must reject required paths it cannot represent.
Cross-host path remapping is not implicit; an operator may adjust target
settings after import before the first normal scan. Imported filesystem
identity and fingerprint evidence cannot establish current target eligibility.

## State Excluded

The bundle must not contain:

- active, queued, paused, stopped-incomplete, or otherwise unfinished
  transfers;
- partial payloads, piece stores, part maps, transfer source sets, source
  sessions, or retry state;
- active or retained search sessions and results;
- passive-cache-only peer/observation entries;
- Kad/eD2K publish queues, publish caches, lookup tasks, or discovery timers;
- scan failures, watcher queues, filesystem-event backlog, or transient scan
  progress;
- session-verified file gates, active serving/publication projections, or
  precomputed implicit-root memberships;
- logs, traces, crash dumps, diagnostics, metrics, or WebUI session state; or
- open connections, sockets, NAT leases, firewall observations not attached to
  a retained Kad contact, and other ephemeral runtime state.

`nodes.dat` and `server.met` are also excluded. They remain import-only
interchange formats under RUST-FEAT-062; this bundle carries their normalized
logical server and Kad state instead.

Exact-file exclusions and explicit per-file unshared state were removed by
RUST-REF-017. They are not bundle domains. Reject those retired fields rather
than translating them into pattern ignores or inventing a compatibility flag.

## Shared Payload Boundary

- Import restores sharing configuration and cached content/path evidence. It
  creates no active library memberships, session verification, or serving
  projection, and does not create completed transfer rows for local files.
- Import must not open, stat, enumerate, read, or hash any shared or completed
  payload path. It must therefore work when the payload volumes are offline.
- The first normal target-daemon scan owns reconciliation with the actual
  filesystem and exposes missing, changed, or moved payloads through existing
  behavior.
- Reuse cached hashes only through the target's current native-identity,
  fingerprint, and content-integrity checks. Matching evidence may avoid
  hashing; changed or insufficient evidence requires normal verification.
- Overlapping explicit and implicit roots reconcile independently. Only files
  admitted by the normal eligibility rules may enter upload, server-offer, or
  Kad-publication views. Exported membership evidence grants no eligibility.
- The bundle does not copy user payloads or transfer data.

## Secret Handling

The bundle intentionally has no password, encryption, or bundle-specific
permission-protection feature. Both export and import must state clearly that
the artifact contains secrets and private data, including:

- the REST API key;
- the eD2K secure-ident private key and public identity;
- peer trust/credit material;
- local and shared filesystem paths; and
- server, friend, sharing, and completed-download history.

The commands must not print secret values. Documentation must instruct the
operator to store, transport, and delete the artifact accordingly, without
claiming that integrity digests protect confidentiality. Normal target-profile
permission validation remains unchanged after import.

## Compatibility and Failure Rules

- Product database compatibility remains exact-current-schema only. No schema
  migration, legacy SQL, fallback read, repair, or automatic startup conversion
  is permitted.
- The exporter fails visibly when its binary does not own the source schema.
  The importer fails visibly when it does not support the declared bundle
  format or cannot represent required semantic state.
- Invalid settings and retired fields are hard errors, including fields marked
  optional by a bundle. They are not silently aliased, defaulted, mapped to
  glob patterns, or written as unknown target fields.
- Identity, cryptographic-key, hashset, and relationship inconsistencies fail
  the whole import before profile publication.
- A failed import never mutates an existing operator profile and never leaves a
  partially valid target at the requested destination.

## Acceptance Criteria

- [ ] The source-version exporter reads only its exact source schema and emits
      a documented, versioned, integrity-checked semantic bundle.
- [ ] The target-version importer creates only a fresh current-schema profile
      and never opens or copies the source database.
- [ ] Import rejects existing/populated targets and live or locked source and
      target profiles.
- [ ] Round-trip fixtures preserve eD2K identity and private key, REST API key,
      representable settings, categories, friends, credits/pinned keys, server
      rows, Kad contacts/bootstrap endpoints, sharing topology and overrides,
      ED2K/AICH known-file hashes, imported-known cache, and completed history.
- [ ] Fixtures prove that all active/incomplete transfers, part state, sources,
      searches, passive-only cache, publish state, failures, logs, diagnostics,
      and ephemeral runtime state are absent.
- [ ] Import succeeds with all shared payload volumes unavailable and tests
      prove it performs no payload enumeration, stat, read, or hashing.
- [ ] Import creates neither eligible shared memberships nor local-file
      download rows. Normal scanning admits unchanged matching files using
      cached hashes, verifies changed files, and leaves offline or ignored
      paths ineligible for serving and publication.
- [ ] Overlapping explicit/implicit roots, lossless native paths, independent
      same-hash file instances, and completed history survive a round trip
      without importing transient eligibility or active download state.
- [ ] Retired exact-file exclusion/unshared fields are rejected, including
      optional occurrences, rather than translated into pattern ignores.
- [ ] Corrupt, truncated, duplicated, oversized, unsupported, or internally
      inconsistent bundles fail before target publication.
- [ ] Export and import display the secret-bearing-artifact warning without
      printing any secret value.
- [ ] Windows, Linux, and the supported container lane interpret the same
      fixture deterministically.
- [ ] Normal startup still rejects an incompatible database and offers no
      automatic upgrade path.

## Validation

- Unit tests for bundle manifest/record encoding, deterministic output,
  required/optional field handling, limits, digests, duplicate detection, and
  unsafe archive input.
- Per-domain source-export and target-import tests through persistence APIs,
  including full identity and ED2K/AICH hashset round trips.
- Failure-injection tests before and during staged SQLite/file writes proving no
  requested target profile is published partially.
- Filesystem-spy tests proving import never touches shared payload paths.
- Establish a current-format golden fixture in the first implementation;
  retain prior supported exporter bundles as new versions are introduced.
  Test those bundles without adding an older database reader to the target.
- Import-to-normal-scan tests for safe unchanged-file hash reuse, changed-file
  verification, offline roots, ignore patterns, overlapping roots, native path
  representation, and zero serving/publication eligibility before admission.
- Cross-platform CLI tests for Windows, Linux, and the supported container
  entrypoint, including locked-profile and existing-target refusal.
- A manual container replacement rehearsal that keeps the old profile intact,
  imports into a new volume/path, validates identity/hash counts, and proves a
  rollback consists only of selecting the old profile again.

## Dependencies

RUST-FEAT-062 is a hard prerequisite. It establishes SQLite as the durable Kad
authority and guarantees that `nodes.dat` and `server.met` are import-only, so
the carry-forward bundle transports logical contacts and server rows instead of
met files. The completed RUST-REF-017 defines the library and download
ownership model; its [retained record](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-REF-017.md)
owns the design and validation evidence for those boundaries.
