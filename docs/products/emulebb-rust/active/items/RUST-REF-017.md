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
The clean schema is version 52. Persisted transfers are download-only:
`source_path_id`, `shared_file_sources`, and the `not_applicable` delivery state
are gone. A read-only protocol view may still describe a verified local file,
but that view is rejected by transfer persistence. Transfer deletion preserves
same-hash verified local content. Offline roots retire membership rows; a
successful rescan is required before they can rejoin publication, and the
health worker retries an incomplete rejoin. Metadata, core, eD2K, and REST
tests plus scoped lint checks pass. Final local Kad and WebUI validation remains
before one implementation PR is requested.
