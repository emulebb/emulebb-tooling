---
id: RUST-FEAT-065
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/253
title: Expose AICH trust integrity and recovery health to operators
status: OPEN
priority: Minor
category: feature
labels: [rust, aich, diagnostics, rest, webui]
milestone: post-beta-polish
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/253. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-065 - Expose AICH trust integrity and recovery health to operators

## Summary

Make AICH authority, optional recovery availability, integrity disagreement, and
request/reuse behavior inspectable through the daemon's existing diagnostic and
operations surfaces. A known root is not proof that complete recovery leaves
exist, that the root is authoritative, or that current local bytes match it.
This is operator visibility work, not a new protocol capability or a replacement
for the correctness fixes in RUST-BUG-164 through RUST-BUG-167.

## Current Findings and Ownership

The reviewed Rust branch `58595576` has root/hashset fields, completion state,
diagnostic packet events, import rejection summaries, and log messages for
unavailable optional recovery caches or conflicting computed AICH. These do
not establish one typed operator contract for trust provenance, proof coverage,
current conflict, and retry disposition. Revalidate the actual current DTOs,
OpenAPI, events, and WebUI before proposing field names; do not duplicate a
surface that already reports one of these facts.

RUST-BUG-164 owns trust provenance, authority, and reconsideration. This item
only projects that state. RUST-BUG-165 owns integrity conflict outcomes,
RUST-BUG-166/167 own answer/request state, and RUST-REF-020 owns incoming proof
reuse. RUST-REF-008/009 own general disk and hashing measurements.

## Intended Operator Contract

Provide read-only summaries with the following distinctions where applicable:

- Root absent, candidate/untrusted, consensus-trusted, accepted import,
  explicit operator-link, or locally computed authority, with current freshness
  and conflict disposition from the owning trust model.
- Root only, usable part hashes, validated partial received proofs, complete
  recovery set, missing optional recovery, and rejected/conflicting cache data.
- Current integrity disagreement versus optional-cache write failure. A cache
  failure does not imply payload corruption or require a global transfer halt.
- Queued, dispatched, busy/unavailable, retry/cooldown, timed out, succeeded,
  canceled, stale, and fallback recovery outcomes, with a concise reason.
- Attempts, validated/invalid answers, retries, proof reuse, responder saturation,
  bytes salvaged, and bytes requiring redownload using defined accounting units.

Build summaries from current owned state or maintained counters. A status poll
must never hash payloads, load every recovery set, walk the filesystem, or run
unbounded per-file queries. Detail views may perform indexed bounded lookups;
make unknown/unavailable state explicit rather than guessing from a root field.
Use cached observations and revisions when reporting asynchronous work.

Fit the existing REST version, OpenAPI, and SPA operations model. Explain
recovery availability and an actionable conflict/failure reason to operators;
keep internal tables, tree identifiers, and worker implementation out of the
ordinary workflow. Do not invent a native GUI, separate database, or profile
repair button. Any new durable state follows exact-current-schema policy.

Keep event rates and metric cardinality bounded. Aggregate reason categories;
do not label process metrics by arbitrary peer IP, path, or file hash. Existing
authorized detail surfaces may identify the selected transfer under their
normal privacy contract. Retained evidence uses neutral filenames and synthetic
peer addresses, never operator payload titles or private paths.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs`, `aich_trust.rs`,
  `aich_answer_cache.rs`, `completion_rehash.rs`, and `salvage.rs`.
- `crates/emulebb-ed2k/src/ed2k_tcp/aich_salvage.rs` and download session events.
- `crates/emulebb-daemon/src/profile_import.rs`: existing rejection counters.
- `crates/emulebb-core/src/rest_model.rs`, `views.rs`, transfer/share adapters,
  and existing runtime diagnostic aggregation.
- `crates/emulebb-rest` DTO/handler/OpenAPI adapters and embedded SPA consumers.
- `docs/products/emulebb-rust/api/REST-API-OPENAPI.yaml`.

## Acceptance Criteria

- [ ] Tests distinguish absent/candidate/consensus/import/link/local roots and
      root-only/partial/complete recovery availability without payload reads.
- [ ] Trusted digest conflict, unavailable/busy responder, and optional-cache
      write failure produce different typed outcomes and operator explanations.
- [ ] Retry, saturation, reuse, and salvage counters have tested reset/lifetime,
      units, duplicate handling, and bounded cardinality.
- [ ] Repeated status polling remains responsive under blocked disk/SQLite work
      and large-library metadata; it does not rebuild trees or scan all files.
- [ ] REST/OpenAPI and rendered operations views agree on all reported states,
      including unknown values during shutdown or asynchronous completion.
- [ ] Logging, fixtures, screenshots, and retained reports respect privacy and
      do not expose implementation detail as a required operator decision.

## Validation and Dependencies

Use synthetic state/DTO/contract tests and rendered UI cases for actual operator
decisions. Inject busy, invalid, conflict, and write-failure outcomes from the
owning layers rather than maintaining a parallel diagnostic state machine.
Coordinate with RUST-REF-016 for nonblocking metadata access. Reuse existing
diagnostic delivery and RUST-CI-031 evidence rather than adding a separate
monitoring service.
