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

## Allocated native download cut (phases 2b/2c)

Implement the accepted [native download contract](../../design/PUBLIC-FOUNDATION.md#native-rest-openapi-and-webui)
directly with the job/storage cut. Source-discriminated creation, job-keyed
resources, canonical `name`, seconds-based timestamps, constrained PATCH,
compact cursor pages and the four exact action paths are one coordinated
producer/consumer change. Keep other resource redesign in phase four. The
master owns the public field/status vocabulary; do not introduce a second DTO
catalog here or claim the target YAML is a qualified implemented contract while
the producer remains incomplete.
The immediate consumer cut also replaces snapshot download rows with fixed
counts and SSE row payloads with job-ID change/removal notifications, using the
existing stream/reset mechanism. Sources/comments remain separate bounded pages;
other snapshot resources stay outside this cut. The [metadata provider checkpoint](RUST-CI-044.md#metadata-provider-checkpoint-2026-11-16)
does not yet make ED2K/Core/API consumers or the full application build-ready.

Creation uses the existing eD2K parser with its AICH/source hints. Active duplicate
admission preserves the existing job; a new explicit attempt receives a new job
ID. Historical completion and verified content facts remain authoritative even
if local output disappears. Observed state is separate from desired intent;
name PATCH cannot rename completed jobs or an active fixed delivery attempt.
Heavy detail exposes actual delivery path/ownership separately from job name.

The Core job cut also needs an actual observed source-identity diagnostic for
the existing cross-client proof. Terminal retirement deliberately deletes job
source children, so postcompletion verification cannot require those rows or
invent replacements. Reuse the current-run diagnostic collector and emit a
`sched/source_identity` observation after the peer hash is known, carrying
`keys.downloadId`, `keys.fileHash`, `keys.peer` and `keys.peerHash` from the
captured job/session. Keep process/run attribution and actual endpoint/hash
checks. Missing identity data is evidence-incomplete, not proof.

The existing cross-client runner must require its diagnostics capability before
launch for this full source proof. Nonretired coherent source rows remain a
separate valid evidence source; verified-content/hashset facts are reported
separately from job rows and do not establish peer identity. Content display
labels are not identity. This producer observation and its actual combined
campaign remain unimplemented/unqualified by the harness consumer changes;
add no product table, polling race or independent diagnostic actor for them.

Accepted action batches always use 207 and concrete per-item outcomes in request
order, even when every item fails. Admission must transfer all bounded work to
the existing owner before the request can be abandoned; no request-owned loop,
per-endpoint actor or all-or-nothing rollback. Keep standard error objects and
existing envelope metadata/contract-version headers. Distinguish malformed
request refusal from shared-capacity refusal before any job mutation.

The Core input facade must replace the current split link validators/parser
with one bounded protocol parser: honor the declared scheme casing, UTF-8 and
percent-decoded names, AICH/source hints, and an explicitly documented byte
limit. Resolve the current raw-space and UTF-8/UTF-16/character-limit differences
before producer qualification. Align known-size validation with positive job
sizes, SQLite's representable range and the current 256-GiB execution limit;
unknown remains null. Bound names without silently rewriting an explicit name.
Producer metadata must declare the exact finite success-code set for every
public method/path, rather than keeping per-route multi-status exceptions.

Extend existing Rust/Python and WebUI owners for create/duplicate/redownload and
size conflicts, PATCH invariants, completion after output loss, early/late
byte-bounded cursor pages, mixed and all-failed batches, saturation, and caller
abort around SQL/publication/handoff and concurrent drains. Couple routes,
typed DTOs, OpenAPI, UI and fixtures in the later producer/consumer pass; none
of this allocation is implemented-contract or runtime qualification evidence.

## Native download contract provider checkpoint (2026-11-16)

Tooling `f6f0ed8f` specifies the target 19 download operations and bounded source
filename windows. Tests `c66bb508` extends the existing schema/conformance owners
and reads operation metadata through the existing YAML loader. The supported
three-owner gate passed **271 tests**, with only
`test_selected_rust_route_contract_matches_selected_openapi` deselected for this
provider-only run; that producer-coupled check remains active and required after
the Rust REST cut. Evidence is under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/native-download-contract-harness-round-2`
(`pytest.log`, `junit.xml`). Strict documentation publication checks also passed
under `reports/native-download-openapi-docs-round-2/docs-publish.log`.

These are target specification and harness providers, not live conformance or
full-application build proof. ED2K/Core/REST/WebUI and remaining campaign callers
still require their coordinated implementation and qualification.

Tests `98a7a5d3` ports the existing REST campaign's download/category and friend
source callers to returned job IDs, 207 item outcomes, paged lists and persisted
physical storage evidence. Its existing unit owner passed **22 tests** under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/native-download-campaign-unit-round-2`
(`pytest.log`, `junit.xml`). First start selects an explicit category temp root;
this is unit qualification of the campaign, not execution against the pending
Rust producer.

The normal Tests push hook subsequently ran the producer comparison and failed
that check with 293 other tests passing; retained evidence is
`reports/local-check/emulebb-build-tests/20261116T123825Z-a223100d/02.log`.
The test remains required. Checker provider `e7b7ad0c` also removes two incorrect
generic assumptions: validate each declared success status rather than requiring
exactly one, and require 404 for named resource paths rather than collections or
batch actions. The four-owner provider gate then passed **294 tests**, with only
the still-unconverted producer comparison deselected, under
`reports/native-download-contract-harness-round-3`. The Tests commits remain
local until producer parity permits their normal push.

Tests `7fb5dd8f` updates the existing package smoke to job IDs, retained terminal
completion and verified inclusive part geometry; its unit owner passed 74 tests.
Tests `f8afd082` ports the existing local Rust peer helper and deterministic
mixed-client caller, including their bilateral diagnostics, and accepts verified
Unowned delivery without granting deletion authority. Five existing unit owners
passed **307 tests** under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/native-download-local-ed2k-unit-round-1`
(`pytest.log`, `junit.xml`). MFC transfer calls remain unchanged. These are unit
and caller-provider checks, not an executed native package or peer campaign.

Tests `2b90b369` ports the existing WebUI and Android peer proofs to captured
download IDs, native pages/actions and retained completed jobs. The shared
request helper can require an exact success status; these action callers require
HTTP 207 as well as successful per-item outcomes. Cleanup authority requires an
actual 201 creation receipt with a validated canonical ID, hash and size;
unchanged duplicates or malformed receipts never authorize job removal. Android
completion still requires exact path/bytes across restart and accepts verified
Owned or Unowned output without granting destructive ownership.

The supported three-owner gate passed **153 tests** after the early fixture,
path-mismatch and cleanup-authority repairs; independent reinspection accepted
the latter. Final evidence is under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/native-download-webui-android-unit-round-3`
(`pytest.log`, `junit.xml`). The first two failed logs remain retained; round one
also had a post-freeze mock edit and cannot establish frozen-source acceptance.
This six-file commit remains local with the other Tests consumers until actual
producer parity permits the normal push. No browser, daemon, ADB or device
campaign was executed by these unit checks.

## Settings/CLI dependency order (phase 3)

The master supplies the consequential product decisions for this cut. Begin
with the existing `emulebb-settings` typed definitions and surface catalog:
make the accepted 59 leaves/five groups the shared owner of defaults,
validation, scalar parsing and application metadata. The Core-only 13-leaf
catalog is partial groundwork, not another authority. Follow with the Metadata
profile store's complete default/custom markers and one durable revision;
resolve default-marked values at load without SQL writes. REST CAS and offline
per-key writes share whole-candidate validation and one transaction.

After that service exists, add offline `settings get/set/reset` directly under
the existing profile lease, without loading the bootstrap TOML or starting the
daemon. Extend the daemon's existing separate-process ownership tests for lease
conflicts and stdout/path behavior. Switch runtime, REST and WebUI consumers
together, preserving the existing tracked save/commit/publication owner and
reporting saved/effective/application state. Then remove the runtime CLI
overrides and update their actual callers and diagnostics directly.

Docker provisioning follows the same service and default markers; its current
service runner still supplies the runtime overrides. Reuse the existing
package/runtime harness owners to test interruption recovery, preservation of
edits, final-profile-relative paths and unsupported no-replace publication.
Do not add package SQL, a second settings writer or a new runner. This ordering
is a source-reviewed allocation, not implemented or executed qualification.

The shared harness preparation owner is
`emule_test_harness/rust_client.py::write_rust_profile`; replace its direct saved
settings writes with the selected binary's canonical offline service. Separate
settings SQL callers in the existing REST CI and upload-soak scenarios must use
that same service. Keep fresh current-schema construction and genuine server/
Kad fixtures distinct from settings writes. Current Rust transfer/name fixture
helpers in `rust_metadata.py` must become job-native rather than opening or
converting another schema. Preserve actual MFC import inputs and their limited
scope. Harness interface/address options are orchestration inputs, not daemon
overrides to delete indiscriminately; Docker process-text assertions, package
help checks and Android error expectations need direct current-contract updates.

## Allocated category contract cut (phase 2a)

The [master category contract](../../design/PUBLIC-FOUNDATION.md#downloads-and-categories)
owns the current category slice: immutable names as public IDs,
`tempDir`/`destinationDir` nullable overrides, editable comment, nullable
transfer assignment, and deletion that clears only matching references without
filesystem changes or ID renumbering. Existing category routes and name
selectors remain; the embedded WebUI, DTOs, OpenAPI and existing Python owners
must change together. Duplicate case-insensitive names on creation return HTTP 409
`CATEGORY_NAME_CONFLICT`, invalid fields 400 and missing category IDs 404;
persistence faults use the shared native mapping. Transfer queries omit
`category` for All; this slice does not add an uncategorized-only selector.

The operator selected the same name rules as tags: 1-64 ASCII letters/digits/
hyphens, starting with a letter or digit, without trimming or rewriting;
uniqueness uses SQLite `NOCASE` and cached ASCII case-insensitive matching.
Names are immutable; create a new category and reassign explicitly. PATCH edits
only paths/comment. Category resources expose only their
four documented fields, with `/categories/{categoryName}` addressing and a
single nullable `category` name on download inputs/resources. Lookup is ASCII
case-insensitive and returns saved spelling. Numeric SQL keys remain internal;
transfer-level priority removal remains in the later job cut.
The [#155 registered category checkpoint](RUST-REF-016.md#registered-category-checkpoint-2026-11-16)
records the exact Rust `22573afd` / tests `c1ad2912` / tooling `5be25fc4` /
Builder `e93fca5` staged bundle and passing real campaign: main 83/105 operations,
SSE, friend/Kad fault-retry/restart checks and the new category lifecycle/sharing
phase. All owned daemons ended gracefully. The first failed runtime report and
its direct public-phase/live-consumer repairs remain recorded there. Earlier
`eac34a72` contract evidence below remains historical. Prepared-ingest/hash/scan
resource bounds and broader jobs/settings/CLI/REST work remain outstanding;
neither this checkpoint nor earlier focused passes complete the overall scope.

## Native Rust contract-gate consolidation

Tests `66e51fef` removes the duplicate MFC-derived Rust route gate, exception
registries and global source-text field assertions. Existing overnight and
release-campaign callers now invoke the required selected-source owner
`test_rust_openapi_routes.py::test_selected_rust_route_contract_matches_selected_openapi`
directly. Actual MFC behavior and its tests are unchanged. Independent review
accepted the consolidation; the supported two-owner unit gate passed **36 tests**
under `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/native-rest-gate-consolidation-unit-round-1`
(`pytest.log`, `junit.xml`). The actual producer check remains required and
unqualified while REST conversion is pending; no skip or exception hides it.

The removed Deserialize source scan was a static heuristic. The selected gate
compares actual route/body/response metadata with OpenAPI, not real serde
acceptance or serialization. Phase-four acceptance must extend the existing
`rust_rest_conformance.py` and `rust-rest-openapi-ci.py` owners to exercise valid
request variants and documented optional fields through the actual router,
including `deny_unknown_fields`, and validate response DTOs on the wire.
Static metadata agreement does not satisfy those runtime obligations.

## Registered runtime and local-suite evidence (2026-11-16)

The [#233 registered runtime checkpoint](RUST-FEAT-062.md#registered-kad-runtime-checkpoint-2026-11-16)
records the passing supported build and REST CI campaign for the exact Rust
`d5c2cfbe` / tests `0531be83` / tooling `eac34a72` / Builder `e93fca5` bundle.
It qualifies current conformance/SSE, six delegated friend fault/retry frontdoors
and real Kad SQLite fault/retry, graceful reopen and same-profile restart.
The report records graceful termination of all owned daemons; friend-only
`quick_check` evidence is distinct from Kad reopen/restart assertions.

The [#233 local-suite checkpoint](RUST-FEAT-062.md#runtime-coupling-local-suite-checkpoint-2026-11-16)
records green final uncommitted working material: full supported Rust-unit suite,
eight existing Python owners and WebUI unit/browser/typecheck/build checks,
after retained fixture/lifetime and shutdown-failure repairs. Those local suites
preceded the exact committed-stage campaign above. The prepared 100k library
fixture remains preparation, not runtime or combined 100k-job qualification. The canonical settings/CLI and
other public-foundation pieces remain their existing implementation scope.

## Accepted automatic Docker setup completion

The operator requires automatic recovery/completion after interrupted fresh
container setup. The [master deployment contract](../../design/PUBLIC-FOUNDATION.md#docker-and-deployment)
owns private same-filesystem staging, a durable ownership journal before stage
creation, canonical per-key service under one lease, parent installation lock,
closed/synced database state, strict atomic no-replace publication and parent
sync. The private helper reads typed markers internally and sets packaged paths
only for default-marked leaves through that same service; custom values,
including staged operator edits, are preserved. No previous-default comparison,
value guessing, new public flag or second SQL authority is introduced. An existing final profile is never replayed or overwritten, including after
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
