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

## Distribution Intake Acceptance

### Accepted Ready Bootstrap Slice

The operator authorized one canonical ready bootstrap for every release
package and first-fresh-profile initialization:
`emulebb-rust-settings.toml`, `[rest].bind_addr = "127.0.0.1:20017"` and
`api_key = "change_me_123change_me_123change_me_123"`. The repeated starter key
has 36 ASCII characters; retain the existing 32-byte minimum and normal API
authentication. It is a public starter value, not a privately generated secret;
replace it before external API exposure. TOML uses only snake_case keys and
rejects obsolete/unknown shapes. A fresh database seeds TCP `20019` and UDP
`20020` even when its bootstrap was supplied by the package, without replacing
existing database preferences or user bootstrap files.

Packages retain the complete adjacent WebUI and a mode-0600 ready TOML; writable
portable directories use the executable directory by default on every platform;
`--profile .` is equivalent only when shell CWD equals that directory. Any
explicit profile can be created fresh, but malformed settings and schema/lease
errors remain hard failures. There are no home/XDG/Local AppData fallbacks.
Installed desktop/container launchers pass documented explicit writable profile
paths; direct read-only selection fails. Android developer bundles retain their
experimental qualification limits. This is an allocated implementation slice,
not proof of integration, package runtime success or completion of this review;
the remaining settings/revision/ETag proposal stays separately unaccepted.

- [ ] Define one daemon/WebUI deployment contract for portable, package-manager
      and future supervised installs: profile/key/data ownership, installation-
      relative WebUI lookup, permissions, listeners, logs and clean shutdown.
- [ ] Keep basic stable bootstrap TOML distinct from mutable SQLite state;
      package/service wrappers add no settings authority or replacement API bridge.
- [ ] Review install/update/uninstall and explicit enablement with
      [Scoop](RUST-FEAT-147.md) and the [service review](RUST-CI-049.md). Do not
      change defaults, start networking or implement a service through intake.

## Outcome

This is the highest-priority Client review, ahead of normal Client work. Produce a complete source-backed target specification and bounded implementation queue. Authorization is review and specification only; review completion and implementation completion are separate outcomes.

## Parent Review Refresh (2026-11-12)

The parent [refreshed shared boundaries](https://github.com/emulebb/emulebb-rust/issues/297#issuecomment-6830059979)
against Rust `080a5dea70186da31dab958757b5b8c0fd883f82`, current schema 68:
one daemon/SQLite authority, minimal stable bootstrap TOML, mutable settings and
durable state in SQLite, transient work in memory and payloads/logs as files.
Read-only met import is the target; #233 still owns removing existing
`nodes.dat` persistence. This review remains In Progress.

Atomic settings [#299](https://github.com/emulebb/emulebb-rust/pull/316) is
merged and closed. Preserve its qualified transaction and owned ordered
commit/publication guarantees; the original partial-write finding is not a
current unfixed defect without a new reproduction. Proposed domain documents,
revisions and representation ETags remain separate target work.

The [complete target](../../design/SETTINGS-TARGET.md) and
[inventory](../../design/SETTINGS-INVENTORY.json) are not accepted for
implementation. The operator chose clean snake_case TOML keys `bind_addr`,
`api_key`, `web_root_dir` and target REST `20017` / P2P TCP `20019` / UDP `20020`.
No aliases, compatibility shims, fallback keys, remapping or silent ignoring
are permitted; obsolete shapes must fail. The target and inventory record
this accepted boundary; other proposed bootstrap/leaf/API
changes remain unaccepted. No current reader, OpenAPI, instructions or defaults are
changed by review. The original source-15020b76 inventory below has not thereby
become a complete current-head runtime qualification.

The accepted [155-A contract](https://github.com/emulebb/emulebb-rust/issues/155#issuecomment-6830001541)
owns the first bounded friend-persistence slice, not global storage completion.
[Scoop's current deployment contract](https://github.com/emulebb/emulebb-rust/issues/324#issuecomment-6830047076)
can proceed after #327 using the selected immutable daemon's actual contract.
The accepted clean Beta3 defaults require implementation and qualification;
package wrappers must not emulate them through mappings or compatibility code.
Neither acceptance authorizes another settings authority, schema rewrite or
profile conversion. Unproven acceptance criteria below remain open.

## Operator direction

- Keep TOML strictly process/profile/control-service bootstrap: listener, authentication and necessary bootstrap paths. Restart requirements alone do not justify placing a product setting in TOML.
- SQLite owns mutable product settings and durable client state. Runtime-only sockets, timers, and queues remain in memory; downloaded payloads and diagnostic artifacts remain files.
- `server.met` and `nodes.dat` are read-only compatibility import inputs. The Rust client must never create, refresh, replace, or write them back.
- Keep generated identity in durable state and implementation constants outside public settings. Use camelCase JSON, snake_case TOML/SQL/Rust and kebab-case URL segments directly. Reject obsolete names; never add aliases, compatibility shims, fallback keys or semantic mappings.
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
- [ ] Prove canonical naming and target defaults; reject obsolete spellings and unknown fields without aliases, fallback reads, remapping or silent ignoring.
- [ ] Define Windows/Linux TCP/UDP binding, configured-port and advertisement checks using synthetic disposable profiles.
- [ ] Produce dependency-ordered implementation slices with existing issue ownership, acceptance and file reservations.
- [ ] Reconcile forward API/design references and submit the target for parent review. No implementation is claimed by this specification.

Target documentation and examples contain no historical values, comparison tables, aliases, semantic mappings, shims or compatibility mechanisms.

## Accepted Target Listener Defaults

The operator accepted these clean Beta3 target defaults. This review changes
no running client, current OpenAPI or current user instructions.

| Listener | Target default |
| --- | --- |
| REST/WebUI TCP | `127.0.0.1:20017` |
| P2P TCP | `20019` |
| P2P UDP | `20020` |

Ports are configurable. Higher numbers provide no security benefit. REST stays authenticated and loopback-bound by default. Specify one coherent P2P UDP owner from receive/send, NAT and advertisement paths; another public UDP listener needs a demonstrated protocol requirement.

## Existing owners and boundaries

- RUST-BUG-156 / #223 owns duplicate ED2K server settings authority.
- RUST-FEAT-062 / #233 owns Kad SQLite persistence and the remaining `nodes.dat` write paths; do not duplicate it.
- RUST-BUG-184 / #299 delivered atomic settings persistence and ordered runtime publication. Preserve it; do not commission a second atomicity implementation.
- RUST-BUG-178 / #280 owns warning and acknowledgement for the authenticated raw private diagnostic bundle. Preserve its exact API-key/full-fidelity contract; settings-resource secret exclusion does not assign export redaction or a logger rewrite here. Once-only fresh-key provisioning is an explicit bootstrap handoff, with any UX change requiring separate acceptance.
- The sibling DB-schema review covers physical/logical schema, query efficiency, and evolution. Coordinate shared contract findings through the parent.
- Scope is Rust client/daemon and its first-party REST/SPA, not rewriting stock MFC or upstream server fixtures.

Priority: Critical, first Client/Phase 0 review. Beta3 release remains held.

## Target Review Deliverables

- [Target specification](../../design/SETTINGS-TARGET.md): ownership, structured
  domain storage decision, exact proposed GET/atomic PATCH contract, shared UDP
  ownership, implementation slices and required verification.
- [Target inventory](../../design/SETTINGS-INVENTORY.json): typed target product
  controls, private bootstrap, internal policy/state classification and source
  evidence.

These deliverables are submitted for parent review. Acceptance remains open
until that review resolves the target decisions; implementation and executed
qualification are not claimed. The original source-only inventory used Rust
`15020b7663a6771bc2d6e8282416ea36a7d7c163`. The refresh above records current
shared boundaries and the separately delivered atomic-settings implementation,
without accepting or regenerating every proposed target value.

## Source Inspection Boundary

Trace the exact selected source and proposed atomic-settings work independently.
Static extraction is not executed validation, a profile read or a completed
implementation. Do not inspect operator profiles or run network/soak work for
this specification. Meaningful implementation verification uses synthetic
disposable profiles through the supported harness after parent allocation.
