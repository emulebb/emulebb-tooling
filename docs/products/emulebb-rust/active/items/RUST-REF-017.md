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
passed across the review commits. The new pagination path has not yet been
measured against a 100,000-file post-refactor library.

Live Kad source discovery remains unproven in the current one-address Windows
harness. A local two-client run bootstrapped Kad and reached `kadConnected=true`,
but the seeder's publish gate reported `firewalledWithoutBuddyOrUdp` and sent
zero source publishes. Both clients had ED2K LowID; the Kad UDP firewall check
cannot use a helper on the same local IP (`emulebb-kad-dht` routing filter), so
the verified-open-UDP term in the stock publication gate never became true.

A second local diagnostic used the staged Linux client as seeder in WSL and the
staged Windows client as leecher on distinct IPs. Both clients bootstrapped Kad,
the server indexed the share, and the leecher accepted a plain eD2K link.
Neither transferred bytes: the seeder remained LowID and its stock Kad source
publication gate still reported `firewalledWithoutBuddyOrUdp`. The REST Kad
summary's `firewallState=open` did not establish the separate verified-open-UDP
condition required by that gate. A synthetic v6 contact could not bootstrap;
v9 contacts with obfuscation disabled did bootstrap but did not verify UDP.
An additional WSL interface could not route to the server or bootstrap its
helper peer, so that topology was removed from the persisted harness. The WSL
diagnostic uses an alternate metadata-enabled DrvFs mount for the Linux profile
key's required `0600` permissions, with profile bytes under the output root.

The remaining proof requires a reachable Kad firewall-check helper on another
IP, or a verified buddy, plus a completed Kad-discovered transfer and matching
delivered-file SHA256. Keep the stock publish gate and this item in progress
until that proof and final branch review are complete; then request one
implementation PR.
