---
id: RUST-CI-043
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/297
title: Review configuration authority and REST contract coherence
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-directed configuration and persistence architecture review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/297. This local document owns the durable engineering specification and evidence.

# RUST-CI-043 - Review configuration authority and REST contract coherence

## Outcome

Review configuration ownership, key/value semantics, and the first-party REST contract before Beta 3. Produce a source-backed inventory and bounded implementation assignments; this item does not itself implement broad API or persistence changes.

## Operator direction

- Keep TOML small and stable: only the bootstrap configuration needed to start and locate the profile/services.
- SQLite owns mutable product settings and durable client state. Runtime-only sockets, timers, and queues remain in memory; downloaded payloads and diagnostic artifacts remain files.
- `server.met` and `nodes.dat` are read-only compatibility import inputs. The Rust client must never create, refresh, replace, or write them back.
- Avoid unnecessary configuration breakage on updates. Review the existing unstable-beta policy explicitly rather than silently adding aliases, migrations, or compatibility branches.
- Beta 3 publication and candidate certification remain on hold. Workspace and platform delivery continues in parallel.

## Acceptance criteria

- [ ] Inventory each bootstrap option and mutable setting: owner, storage, key/name, type, unit, default, validation, secret status, precedence, and restart behavior.
- [ ] Compare current files and behavior with the TOML/bootstrap and SQLite target; identify duplicate authorities and stale docs, including an explicit current-versus-target matrix.
- [ ] Trace settings through CLI, daemon, repository, REST DTOs, OpenAPI, validators, embedded WebUI, and automation consumers. Review route/resource names, methods, status/error shapes, pagination, nullability, and authentication.
- [ ] Propose one canonical setting definition/authority per value and clear boundaries for stable bootstrap configuration versus evolving REST and DB contracts.
- [ ] Define meaningful consistency checks and concrete upgrade examples. Any change to compatibility or fresh-profile policy is a separate, reviewable parent decision.
- [ ] Route findings to existing issues first; create independent implementation slices only for uncovered work, with file reservations and Windows/Linux plus architecture-sensitive acceptance where relevant.
- [ ] Reconcile the durable specification and owning product references after review. Do not claim implementation is complete because a review document exists.

## Existing owners and boundaries

- RUST-BUG-156 / #223 owns duplicate ED2K server settings authority.
- RUST-FEAT-062 / #233 owns Kad SQLite persistence and the remaining `nodes.dat` write paths; do not duplicate it.
- RUST-FEAT-063 / #234 owns explicit semantic export and fresh-target import,
  not automatic database upgrades. Review it before creating continuity work.
- The sibling DB-schema review covers physical/logical schema, query efficiency, and evolution. Coordinate shared contract findings through the parent.
- Scope is Rust client/daemon and its first-party REST/SPA, not rewriting stock MFC or upstream server fixtures.

Priority: Major. Client/Phase 0 review for Beta 3; release remains held.

## Initial Source Review

Reviewed Rust `edc59a003fff873e26d2c720bf9ca06f4b640871`. Bootstrap TOML already
contains a small REST startup block; mutable application settings are stored
in SQLite. This review must reconcile the existing implementation with the
target, rather than introduce a second configuration file.

The source-traced direct-core update ordering and per-section transaction risk
have one implementation owner: [RUST-BUG-184](RUST-BUG-184.md),
[issue #299](https://github.com/emulebb/emulebb-rust/issues/299). Coordinate it
with RUST-CI-044; do not commission separate API and DB fixes. Runtime proof is
still required. REST middleware rejects invalid numeric core settings before
the handler, so the direct-core example is not an HTTP partial-update witness.
Reproduce accepted-request storage failures through the real router. Review
work remains in progress; no behavior change is claimed.

The first pass traced 105 settings leaves against the backend surface registry,
OpenAPI, TypeScript types, and UI controls. Four TypeScript fields and seven
normal/advanced controls have candidate omissions; eleven other settings are
intentionally not user-facing. Verify the intended user surface before filling
gaps. Core and ED2K rate/source/connection controls need runtime-owner tracing
before removing duplicate-looking fields. This is separate from BUG-156's
already-owned server settings correction.

Top-level TOML rejects unknown fields, while the nested REST bootstrap type
does not declare the same rejection. Review typo handling and future extension
semantics explicitly; an ignored key is not a supported compatibility alias.

Generated static inventory and evidence are retained below
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/config-api-review/` in `review.md`,
`settings-inventory.json`, and `settings-inventory.csv`. Static extraction does
not prove runtime validators, request behavior, or end-to-end API coherence.
