---
id: RUST-CI-031
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/164
title: Build persisted full-tunnel protocol parity soaks
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, tests, harness, diagnostics, protocol, ed2k, kad, vpn, soak, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-24
source: 2026-10-24 operator request for long-running persisted eD2K and Kad parity diagnostics
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/164. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-031 - Build persisted full-tunnel protocol parity soaks

## Summary

Provide a supported, restartable Rust-versus-MFC diagnostics workflow for
arbitrarily long eD2K and Kad investigation against explicitly selected
operator-owned persisted profiles. The workflow must use hide.me in full-tunnel
mode, keep both P2P planes fail-closed through VPN Guard, use loopback for local
control, import the MFC profile into an empty Rust profile exactly once, and
reuse a valid nonempty Rust profile thereafter.

The workflow is a diagnostic discovery lane, not unbounded certification
evidence. Repeatable bounded captures remain the authority for a parity claim.

## Current State

- The canonical dual-client launchers now expose an explicit full-tunnel mode,
  perform a read-only hide.me preflight, use IPv4 loopback for control, and
  require VPN Guard Block configuration before client launch.
- The full-tunnel lane accepts an explicitly selected operator-owned Rust
  profile outside `EMULEBB_WORKSPACE_OUTPUT_ROOT`; split-tunnel runs retain the
  managed-output boundary.
- An empty persisted Rust profile is imported transactionally from the selected
  MFC profile, while a populated profile must contain the current Rust settings
  and metadata files and is then reused without reimport.
- Temporary MFC `preferences.ini` overlays use a durable output-root journal,
  exact-byte restore after process exit, and stale-run recovery after old soak
  processes are stopped.
- A dedicated persisted-soak controller now starts the canonical dual-client
  launcher detached and until stopped, records exact launcher and watcher
  identities, reports dual process/REST/VPN health, rotates watcher evidence,
  and requests graceful teardown before an exact-identity forced fallback.
- Packet and semantic diagnostics cover substantial protocol surface. The
  common event stream now has a v2 process/run/segment envelope and bounded
  writers on active Rust and MFC branches, while connection/session/action
  correlation, unified server/client-UDP coverage, and required-family gates
  remain incomplete.
- The Rust diagnostic dump endpoint now produces a versioned, bounded local
  investigation bundle with status, runtime diagnostics, settings provenance,
  recent-log fingerprints, and tails plus integrity summaries for unified,
  eD2K peer TCP, eD2K client UDP, eD2K server, and Kad UDP artifacts. Its
  existing redaction is transitional and must not suppress evidence needed by
  this explicitly local, non-published test lane.
- Active Rust and MFC branches use one process-wide retained-event sequence,
  family-local stream sequences, rotate-before-write segments, persisted-run
  retention, and observable writer/drop/error health.
- Legacy packet dump families remain separate unbounded files. Arbitrary-length
  authorization therefore remains blocked until current v2 integration lands,
  packet evidence is bounded or retired from the long-soak gate, and guarded
  live validation proves the complete path.

## Landed Evidence

- `emulebb/emulebb-tooling#56` defined the persisted full-tunnel lane, external
  profile exception, loopback-control rule, and evidence limitations.
- `emulebb/emulebb-build-tests#18` added the read-only full-tunnel preflight,
  explicit topology selection, loopback control binding, and fail-closed guard
  requirement. Local validation: 2,297 passed, 1 skipped, 1 deselected; all PR
  checks passed.
- `emulebb/emulebb-build-tests#19` added transactional import-if-empty,
  validated reuse, external-profile scoping, and preflight-before-mutation
  ordering. Local validation: 2,303 passed, 1 skipped, 1 deselected; all PR
  checks passed.
- `emulebb/emulebb-build-tests#20` added durable exact-byte MFC preference
  overlays, stale-run recovery, and restore evidence in both canonical
  launchers. Local validation: 2,308 passed, 1 skipped, 1 deselected; all PR
  checks passed.
- `emulebb/emulebb-build-tests#21` added the canonical stop-file contract and
  detached dual-client controller with exact process identities,
  restart-safe status, loopback REST and full-tunnel health checks, bounded
  rotating watcher evidence, and graceful/forced stop semantics. Local
  validation: 2,319 passed, 1 skipped, 1 deselected; all PR checks passed.
- `emulebb/emulebb-rust#165` replaced the status-only dump with
  `emulebb.diagnostic-bundle.v1`, bounded artifact tails, explicit
  missing/schema/parse/sequence evidence, stable sensitive-value
  fingerprints, and an honest `fullMemoryIncluded: false` result. Local
  validation: 125 REST tests and 431 core tests passed; format, Clippy, all
  platform build/test jobs, CodeQL, dependency policy, and live REST/OpenAPI
  conformance passed.
- The post-merge diagnostics audit identified the next implementation order:
  one authoritative segmented event writer with process-wide and stream-local
  sequencing; bounded rotation and retention with writer/drop counters;
  unified eD2K server and client-UDP coverage; then stable connection, request,
  search, and transfer correlation fields.
- No public live client was launched for these foundation slices; guarded live
  and tunnel-down acceptance evidence remains outstanding.

## In-Flight Implementation

- `emulebb/emulebb-build-tests#22` has landed run-aware segmented Rust trace
  selection, ordered multi-segment loading, transitional v2 compatibility, and
  the first shared v2 schema notes. Local validation passed 2,329 tests with 1
  skipped and 1 deselected; both supported Windows harness jobs and the
  portability, security, and dependency checks passed. The permissive
  dual-schema behavior is superseded by the strict common-v2 work in #23.
- `emulebb/emulebb-rust#166` remains open while the common-schema correction
  lands. Its branch adds the dependency-neutral `emulebb-diagnostics` crate,
  the incompatible `diag_event_v2` envelope, one process-wide and family-local
  sequence authority, size/age rotation, global persisted-directory retention,
  writer health in REST/bundles, and active-run multi-segment bundle capture.
- The `diag_event_v2` identity contract is `(processId, runId, segmentId)`.
  `seq` is process-wide retained-event order and `streamSeq` is retained-event
  order within one family. Files are named
  `emulebb-rust-diag-<processId>-<runId>-<segmentId>.jsonl`.
- Independent review blocked the first merge attempt because retention was
  initially per random run, bundle capture selected one globally newest file,
  live partial lines could be reported as corruption, and the harness accepted
  only `diag_event_v1`. The Rust branch now bounds segments across restarts,
  protects the active segment, revalidates size after rollover, aggregates only
  the active run, and ignores a racing unterminated active tail.
- The first migration design left MFC on `diag_event_v1` while Rust emitted
  `diag_event_v2`. That is rejected as a steady-state design: v2 is the single
  current common envelope for both clients, and v1 may survive only behind an
  explicitly named legacy-input adapter. Current parity and soak gates must not
  silently accept either version.
- `emulebb/emulebb#179` is draft with MFC commits `9dbb9952`, `2271d8fc`, and
  `77ec3524`. The branch emits the common v2 envelope through a dedicated
  per-launch segmented writer with unique create-new files, rotate-before-write
  byte/age bounds, committed process/family sequences, global retention,
  atomic writer health, final-close error persistence, and complete unredacted
  eD2K/Kad packet payloads. Required Debug x64, Release x64, and diagnostics
  Release x64 builds passed; all PR checks are green.
- `emulebb/emulebb-build-tests#23` is open with commits `9747790` and
  `6fd86b5`. It makes v2 the only current schema, selects exactly one Rust or
  MFC run, rejects stale-process fallback, malformed complete lines, mixed
  identities, segment/sequence gaps, and foreign schemas, validates matching
  lossless MFC writer health, gives derived reports their own schemas, and
  confines v1 to the explicit legacy MFC adapter. Local validation passed 2,340
  tests with 1 skipped and 1 deselected; PR checks are running.
- PR #179 remains draft until #23 lands and the MFC artifact-name policy is
  updated. Rust PR #166 remains unmerged until its current API conformance
  failure is resolved and local-bundle redaction is removed.
- Protocol and soak traces, bundles, manifests, and diagnostic payloads are
  explicitly local test evidence and will not be published. They must preserve
  exact file, peer, user, hash, endpoint, search, and packet data whenever that
  data helps reconstruct eD2K or Kad behavior. Redaction and privacy-driven
  field omission are not requirements for this lane; completeness is.
- Legacy packet dump families remain unbounded. Arbitrarily long public live
  soaks are still unauthorized, and no live client has been launched during
  these implementation slices.

## Why This Matters

Long-running public-network observation is needed to expose rare eD2K and Kad
state-machine behavior, but an unbounded run magnifies routing, profile
mutation, disk-growth, and false-parity risks. A supported workflow must fail
closed before launch, preserve operator state, bound its local evidence, and
distinguish observed parity from merely unobserved behavior.

## Representative Sites

- `repos/emulebb-build-tests/scripts/converged-soak-live.py`
- `repos/emulebb-build-tests/scripts/launch-soak.py`
- `repos/emulebb-build-tests/scripts/rust-soak-control.py`
- `repos/emulebb-build-tests/emule_test_harness/soak_launch.py`
- `repos/emulebb-build-tests/emule_test_harness/hideme_split_tunnel.py`
- `repos/emulebb-build-tests/emule_test_harness/mfc_profile_import.py`
- `repos/emulebb-build-tests/emule_test_harness/diag_event_diff.py`
- `repos/emulebb-build-tests/emule_test_harness/packet_trace_diff.py`
- `repos/emulebb-rust/crates/emulebb-rest/src/handlers/app.rs`
- eD2K and Kad packet/event writers under `repos/emulebb-rust/crates/`

## Intended Shape

### Full-tunnel safety

- Add a read-only hide.me full-tunnel preflight that requires the provider
  active, split tunneling disabled, the expected adapter and route present,
  and no silent direct fallback.
- Bind both P2P planes through the hide.me interface, configure VPN Guard Block
  for both clients, and record periodic route, binding, and guard evidence.
- Use loopback for both REST control planes and keep the inherited environment
  unchanged.

### Persisted profile lifecycle

- Accept explicit ignored-local MFC and Rust profile inputs through the
  persisted Python workflow.
- Import the complete MFC profile only when the Rust target is truly empty.
- Validate and reuse a nonempty current-schema Rust profile without automatic
  reset or reimport. Keep any supported test/soak schema repair explicit,
  bounded, and backup-first.
- Snapshot every MFC profile file changed by temporary harness overrides and
  restore those overrides during normal and recovered teardown.

### Controller and evidence

- Extend the converged soak path rather than creating ad-hoc launch or
  monitoring logic.
- Support a detached until-stopped run with a manifest, exact process identity,
  health/watch state, graceful stop, bounded forced fallback, and restart-safe
  status reporting.
- Rotate diagnostic segments, detect parse and sequence gaps, enforce disk
  thresholds, and retain compact campaign summaries plus selected
  representative payloads.

### Diagnostics and parity

- Add common run, process sequence, connection/session, action/request/search,
  and transfer correlation fields across relevant Rust diagnostics.
- Complete unified event coverage for eD2K server traffic, client UDP, peer
  capability negotiation, retries/timeouts, disconnects, and Kad lifecycle
  transitions.
- Produce a bounded, unredacted local diagnostic bundle containing the full
  REST snapshot, settings provenance, network/guard state, counters, recent
  errors, and packet/event tails.
- Treat missing required families, unknown schemas, parse failures, sequence
  gaps, and absent comparable keys as explicit inconclusive or failing evidence
  instead of parity success.

## Scope Constraints

- Stock/community eMule remains the authority for wire behavior. Maintained
  eMuleBB MFC is the operational comparator, and current aMule is a distinct
  interoperability evidence lane.
- Supported scope is IPv4 eD2K/Kad behavior minus the registered permanent
  omissions. Intentional extensions such as `offerfiles-v1` remain separate
  negotiated/fallback lanes.
- This item may break harness schemas, diagnostic schemas, REST APIs, or test
  profile configuration during the beta phase when the resulting design is
  cleaner and the owning contracts and tests change together.
- `diag_event_v2` is the only current common event envelope for both Rust and
  MFC. Legacy v1 input, if retained at all, is isolated from current validation
  behind an explicit compatibility adapter.
- Runtime traces and bundles are unredacted local test artifacts. They may
  contain exact identifiers and raw public-network payloads and must never be
  uploaded, attached to public issues, or committed.
- Tracked files never contain operator profile paths, private network values,
  live search terms, file names, hashes, or raw public-network payloads.
- The harness must not mutate hide.me settings or inherited workspace
  environment variables.
- Arbitrarily long runs do not replace bounded, repeatable parity and release
  proof.

## Acceptance Criteria

- [x] The harness/live policy defines the persisted full-tunnel diagnostic soak
      lane and its evidence limitations.
- [ ] Preflight fails before launch unless hide.me is active, split tunneling is
      off, loopback control is available, and both P2P planes can bind the
      selected interface.
- [ ] Both clients start with VPN Guard Block and a controlled tunnel-down proof
      demonstrates zero off-tunnel public P2P traffic.
- [x] A truly empty Rust profile is imported once from the selected MFC profile;
      a valid nonempty Rust profile is reused without reimport or reset.
- [x] Temporary MFC harness overrides are backup-first and recoverable after
      graceful stop, launcher failure, or stale-manifest recovery.
- [x] The canonical dual-client workflow supports detached until-stopped runs,
      self-describing status, periodic health checks, and graceful teardown.
- [ ] Packet/event evidence rotates within configured byte and age budgets and
      reports record, parse, sequence, and dropped-event gaps.
- [ ] Required eD2K and Kad diagnostic families carry exact local evidence and
      enough stable correlation to reconstruct causal sessions and harness
      actions without privacy-driven omissions.
- [x] The diagnostic dump API produces a bounded investigation bundle rather
      than a status-only placeholder; removing its transitional redaction is
      still required.
- [ ] The parity matrix covers server, peer-transfer, source/queue, and Kad
      lifecycle behavior while excluding registered omissions and separating
      negotiated extensions.
- [ ] Staged validation passes deterministic local fixtures, fail-closed VPN
      tests, guarded short live runs, restart recovery, and progressively longer
      soaks before an until-stopped run is authorized.

## Validation

- Static policy, environment-override, live-bind, and profile-path gates.
- Unit tests for provider-state parsing, full-tunnel preflight, empty/reuse
  profile selection, transactional overrides, manifests, rotation, gap
  detection, evidence completeness, and strict comparison outcomes.
- Deterministic local eD2K/Kad fixtures and protocol goldens.
- Explicit operator-approved public validation with tunnel-down blocking,
  guarded dual startup, loopback control, clean stop, recovered stop, and
  retained local-only evidence.

## Notes

- Implementation should land as granular, independently validated pull
  requests in `emulebb-tooling`, `emulebb-build-tests`, and `emulebb-rust`.
- Update this checklist as each coherent slice lands; keep transient run logs
  out of this item and retain only stable conclusions or evidence references.
