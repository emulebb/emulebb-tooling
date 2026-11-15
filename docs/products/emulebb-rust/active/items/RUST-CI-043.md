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

## Accepted automatic Docker setup completion

The operator requires automatic recovery/completion after interrupted fresh
container setup. The [master deployment contract](../../design/PUBLIC-FOUNDATION.md#docker-and-deployment)
owns private same-filesystem staging, a durable ownership journal before stage
creation, canonical per-key service under one lease, parent installation lock,
closed/synced database state, strict atomic no-replace publication and parent
sync. An existing final profile is never replayed or overwritten, including after
an interrupted publication. Unsupported atomic publication fails visibly and
retains owned work for automatic retry; no unsafe move fallback qualifies.

A package-private helper and typed actual-listener health receipt are planned;
there are no additional public daemon commands/flags or environment overrides.
Extend the existing Python package/container owners for every failure cut and
both image variants. This acceptance allocates implementation/proof, not a claim
that current Docker setup or either package variant has passed it.

## Registered current-contract checkpoint (2026-11-15)

The [#155 registered conformance/peer checkpoint](RUST-REF-016.md#registered-conformance-and-local-peer-checkpoint-2026-11-15)
retains the first failed campaign, its runtime drain repair and passing rerun at
Rust `b509524f` / tests `a96b5859` / tooling `26492515` / Builder `e93fca5`.
The rerun covered 83/105 current main operations, 43 expected errors and 22 explicit
unsafe skips, plus SSE and 6/6 delegated friend mutations with failure/retry and
clean-process/database proof. These are current-contract results, not
qualification of the unimplemented 59-field settings/CLI or full library/job
foundation. Upload progress under database contention and broad scale/platform
proof remain pending.

## Shared friend-owner dependency checkpoint (2026-11-15)

The [#155 scoped friend-owner checkpoint](RUST-REF-016.md#scoped-friend-owner-checkpoint-2026-11-15)
records implementation at Rust `ea0f9653`, focused Core/REST/integration proof
and selected-artifact OpenAPI validation. Historical discovery notes below
predate that worker implementation. This does not claim runtime Kad persistence,
the canonical settings/CLI redesign, all-SQL async conversion, actual upload
contention behavior or combined-scale qualification. Continue through the same
owner rather than add another persistence lane.

## Historical foundation discovery checkpoint (2026-11-15)

Round-one branch evidence: Rust `70e595a2`, build-tests `d14d5871` and
specification/policy baseline tooling `77b30a82`. These are pushed checkpoints,
not merged delivery; no PR is authorized before the operator returns.

The first scoped implementation adds independent durable discovery-initialization
state and atomic server-list initialization. Automatic server import accepts the
first validated nonempty fallback, preserves explicit empty/disabled operator
state, and does not overwrite a list changed while a fetch was in flight. The
existing Python harness uses selected-workstream fixtures and transactional
explicit server inputs, preserving deterministic public-bootstrap isolation.

Focused evidence recorded by the parent: metadata 104 unit plus 3 integration
checks; daemon 108 unit plus 15 integration checks with one ignored helper;
Python 80 passed with one POSIX-only skip. Two review rounds resulted in
operator-race and explicit-fixture repairs. Normal push checks passed with
output-root-relative receipts:

- `reports/local-check/emulebb-rust/20261115T185408Z-f63dbe33`
- `reports/local-check/emulebb-build-tests/20261115T185216Z-90fd5f42`

This does not qualify the full public foundation. Kad file persistence removal,
the coordinated settings/REST redesign, library/download/search changes and
combined-scale proof remain pending. The accepted #155-A bounded persistence
worker is still unimplemented and is a prerequisite for runtime Kad checkpoint
wiring; reuse that owner rather than introduce a competing actor. Bootstrap
state alone is not a claim that runtime Kad persistence is complete.

## Accepted Foundation Round One (2026-11-15)

The operator authorized implementation of the consolidated
[Public Foundation](../../design/PUBLIC-FOUNDATION.md). That specification
supersedes conflicting proposal-only common contracts and acceptance rules in
older review notes below. Existing delivered evidence remains historical proof,
not qualification of this new target. Coordinate with the current persistence
owner; use the existing Python harness. One persistent branch per involved
repo, granular commits and tested pushes; no PR, merge or publication until
the operator returns and reviews. Leaf inventory cleanup and actual validation
remain work, not claims of completion.

## Distribution Intake Acceptance

### Accepted Ready Bootstrap Slice

The operator authorized one canonical ready bootstrap for every release
package and first-fresh-profile initialization:
`emulebb-rust-settings.toml`, `[rest].bind_addr = "0.0.0.0:20017"` and
`api_key = "change_me_123change_me_123change_me_123"`. The repeated starter key
has 39 ASCII characters; retain the existing 32-byte minimum and normal API
authentication. The starter value is shared by ready packages. TOML uses only snake_case keys and
validates its current shape. A fresh database seeds TCP `20019` and UDP
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

### Generated Runtime Refresh Ownership

Executable-directory profiles are operator data even when created beside a
workspace-staged daemon. Registered runtime replacement and retirement must
prove the existing bundle's file inventory and directory ownership before any
destructive operation, independently of the current source revision. A valid
older generated bundle remains replaceable; missing/corrupt receipts, changed
members, unknown files and unknown directories require refusal and preservation.
Late backup cleanup removes only proven members and preserves/reports newly
appearing data rather than recursively deleting the directory. No profile is
moved, converted, reset or adopted as generated output.

The canonical operator stage currently has no ownership receipt. Its clean-build
path therefore refuses a nonempty runtime directory; ordinary non-clean/fresh
staging still replaces named generated artifacts. Operator refresh and persisted
launches use the existing harness with an explicit profile outside generated
runtime namespaces. Future Scoop launchers retain the same explicit stable
profile boundary described in [RUST-FEAT-147](RUST-FEAT-147.md). This guard is an
allocated #297 contribution; integration and final applicable gates remain
parent-owned and are not claimed by this specification update.

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
are permitted; validate only the current contract. The target and inventory record
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
- Keep generated identity in durable state and implementation constants outside public settings. Use camelCase JSON, snake_case TOML/SQL/Rust and kebab-case URL segments directly. Use canonical names without aliases, compatibility shims, fallback keys, remapping or retired-input handling/tests.
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
- [ ] Prove canonical naming and target defaults; validate the current contract without aliases, remapping or tests preserving removed names.
- [ ] Define Windows/Linux TCP/UDP binding, configured-port and advertisement checks using synthetic disposable profiles.
- [ ] Produce dependency-ordered implementation slices with existing issue ownership, acceptance and file reservations.
- [ ] Reconcile forward API/design references and submit the target for parent review. No implementation is claimed by this specification.

Target documentation and examples contain no historical values, comparison tables, aliases, semantic mappings, shims or compatibility mechanisms.

## Accepted Existing-Contract Repairs

The parent allocated bounded settings and ownership repairs on 2026-11-15, based on Rust
`23e685b87bb76db21489c9b1cc725dd0da4241c1`:

- Standalone `useServerPriorities` and `autoConnectStaticOnly` updates must
  count as nonempty settings changes, accept both boolean values, preserve
  omitted settings and retain their existing restart semantics.
- NAT `enabled` and `requireInitialMapping` accept booleans only. Explicit
  null or another JSON type must fail validation even alongside a valid
  sibling; legitimately nullable NAT addresses and paths remain clearable.
- Profile ownership ends when its final logical owner drops, after metadata
  connection teardown. A shared typed guard must release its already-owned
  descriptor without waiting for a subprocess's transient inherited descriptor.
  An inherited child must not explicitly unlock its parent's lease.

Qualification must cover PATCH/GET/SQLite/reopen persistence, unchanged
saved/live state after a rejected mixed update, retained profile/metadata clone
exclusion, duplicate-descriptor and constructor-error release, and controlled
Unix child non-unlock. Windows proof does not establish the Unix child case.
Preserve the atomic persistence and ordered runtime publication delivered by
#299. See the [allocation](https://github.com/emulebb/emulebb-rust/issues/297#issuecomment-6887481479).

PR [#334](https://github.com/emulebb/emulebb-rust/pull/334) delivered the
allocated boolean validation, strict NAT null handling and typed profile-lease
guard; it merged at `e735319bbd7b72cbd21dac6ef172d318b3543947`. PR
[#335](https://github.com/emulebb/emulebb-rust/pull/335) made fixture setup a
process-isolated copy without hardlinks and merged to Rust `main` at
`0840e9005fd2ab28e9cbe262054dd692262e5698`. The full local owner check passed
all six stages, including Windows, Linux and Android, and all 30 hosted checks
and four workflows passed. A fresh CI run on current `main` was still running
when this evidence was recorded; no result is inferred for that run.

This slice repairs the existing contract. It does not accept the broader
settings/revision/ETag proposal or authorize schema, default, bootstrap or
persistence-owner changes.

## Accepted Target Listener Defaults

The operator accepted these clean Beta3 target defaults. This review changes
no running client, current OpenAPI or current user instructions.

| Listener | Target default |
| --- | --- |
| REST/WebUI TCP | `0.0.0.0:20017` |
| P2P TCP | `20019` |
| P2P UDP | `20020` |

Ports are configurable. Higher numbers provide no security benefit. REST stays authenticated and binds `0.0.0.0:20017` by default. Specify one coherent P2P UDP owner from receive/send, NAT and advertisement paths; another public UDP listener needs a demonstrated protocol requirement.

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
