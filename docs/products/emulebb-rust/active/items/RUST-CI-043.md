---
id: RUST-CI-043
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/297
title: Review configuration authority and REST contract coherence
status: IN_PROGRESS
priority: Critical
category: ci
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-directed configuration and persistence architecture review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/297. This local document owns the durable engineering specification and evidence.

# RUST-CI-043 - Review configuration authority and REST contract coherence

## Outcome

This is the highest-priority Client review, ahead of normal Client work. Produce a complete source-backed target specification and bounded implementation queue. Authorization is review and specification only; review completion and implementation completion are separate outcomes.

## Operator direction

- Keep TOML strictly process/profile/control-service bootstrap: listener, authentication and necessary bootstrap paths. Restart requirements alone do not justify placing a product setting in TOML.
- SQLite owns mutable product settings and durable client state. Runtime-only sockets, timers, and queues remain in memory; downloaded payloads and diagnostic artifacts remain files.
- `server.met` and `nodes.dat` are read-only compatibility import inputs. The Rust client must never create, refresh, replace, or write them back.
- Keep generated identity in durable state and implementation constants outside public settings. Use operator-facing domains and mechanical casing: camelCase JSON, snake_case TOML/SQL/Rust and kebab-case URL segments.
- Preserve the exact-schema/fresh-profile policy and old profiles for explicit rollback. This review does not authorize profile evolution work.
- Beta 3 publication and candidate certification remain on hold. Workspace and platform delivery continues in parallel.

## Acceptance criteria

- [ ] Inventory every target setting: domain, canonical name, owner, storage, type, unit, default, validation, secret handling, public visibility and application/restart behavior.
- [ ] Trace CLI/bootstrap, typed definitions, persistence, runtime consumers, REST, OpenAPI and SPA to each actual authority.
- [ ] Select and justify the settings representation using validation, atomicity, maintainability and query needs; exclude unrelated database redesign.
- [ ] Specify one domain-grouped GET/atomic PATCH resource; keep collections, runtime status and actions in dedicated resources.
- [ ] Define exact routes, payloads, omission/null/reset semantics, errors, authentication, secret exclusion and saved/effective/restart state.
- [ ] Require complete validation before persistence, one transaction, no runtime change after failed persistence and explicit post-commit application outcomes.
- [ ] Define fresh-profile, parsing, unknown-field, validation, atomicity, persistence-failure, restart, secret and API/OpenAPI/SPA consistency tests.
- [ ] Define Windows/Linux TCP/UDP binding, configured-port and advertisement checks using synthetic disposable profiles.
- [ ] Produce dependency-ordered implementation slices with existing issue ownership, acceptance and file reservations.
- [ ] Reconcile forward API/design references and submit the target for parent review. No implementation is claimed by this specification.

Target documentation and examples contain no historical values, comparison tables, aliases, semantic mappings, shims or compatibility mechanisms.

## Recommended Listener Defaults

These values belong to the proposed target. This review does not change a running client, current OpenAPI or current user instructions.

| Listener | Target default |
| --- | --- |
| REST/WebUI TCP | `127.0.0.1:20017` |
| P2P TCP | `20019` |
| P2P UDP | `20020` |

Ports are configurable. Higher numbers provide no security benefit. REST stays authenticated and loopback-bound by default. Specify one coherent P2P UDP owner from receive/send, NAT and advertisement paths; another public UDP listener needs a demonstrated protocol requirement.

## Existing owners and boundaries

- RUST-BUG-156 / #223 owns duplicate ED2K server settings authority.
- RUST-FEAT-062 / #233 owns Kad SQLite persistence and the remaining `nodes.dat` write paths; do not duplicate it.
- RUST-BUG-184 / #299 owns atomic settings persistence and ordered runtime publication. Do not commission a second atomicity implementation.
- The sibling DB-schema review covers physical/logical schema, query efficiency, and evolution. Coordinate shared contract findings through the parent.
- Scope is Rust client/daemon and its first-party REST/SPA, not rewriting stock MFC or upstream server fixtures.

Priority: Critical, first Client/Phase 0 review. Beta3 release remains held.

## Review Evidence Boundary

Trace the exact selected source and proposed atomic-settings work independently.
Static extraction is not executed validation, a profile read or a completed
implementation. Do not inspect operator profiles or run network/soak work for
this specification. Meaningful implementation verification uses synthetic
disposable profiles through the supported harness after parent allocation.
