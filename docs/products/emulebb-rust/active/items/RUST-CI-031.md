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
  writers on Rust and MFC `main`. The harness selects one exact process run,
  enforces sequence and writer-health integrity, and rejects packet-only
  comparisons. Stable connection/session/action correlation remains incomplete.
- The authenticated Rust diagnostic bundle endpoint now returns strict inline
  `emulebb.diagnostic-bundle.v5` evidence with status, runtime diagnostics,
  settings provenance, recent logs, exact records plus integrity summaries
  from the unified `diag_event_v2` stream, and bounded deterministic operational
  snapshots for servers, shared files, searches and evidence-rich results,
  transfers, uploads, and the upload queue. Every collection reports its exact
  total, included, omitted, and limit values. The daemon no longer persists
  UUID-named bundles in the reusable profile. WebUI users download the exact
  inline JSON, while the soak harness owns bounded campaign persistence. The
  evidence is intentionally unredacted for this local, non-published test lane.
- Rust and MFC use one process-wide retained-event sequence,
  family-local stream sequences, rotate-before-write segments, persisted-run
  retention, and observable writer/drop/error health.
- The Rust writer now treats storage as an explicit authority: it enforces
  aggregate bytes, retained age, retained segment count, and minimum free
  space before growth; protects the active segment; accepts an exact oversized
  record only when the configured budget permits it; and exposes retained
  inventory, maximum growth, policy state, drop causes, and latched storage and
  writer-I/O faults. Invalid configured limits fail initialization instead of
  silently falling back to defaults.
- The canonical soak launcher now passes all six strict Rust diagnostic writer
  limits through an explicit child environment, rejects stale inherited writer
  settings, and verifies the exact reported policy, maximum growth, storage
  state, identity, counters, and fault latches before any public protocol
  action. The campaign-store policy and profile-local writer policy remain
  separate because they govern different volumes.
- Every active Rust protocol family now emits through the bounded unified
  stream. The peer-TCP, client-UDP, server TCP/UDP, and Kad-UDP legacy packet
  side-file writers are retired, and active harness consumers select exact
  `diag_event_v2` runs rather than discovering those files. The REST/OpenAPI
  contract now carries the complete 41-field writer-health payload.
  Rust and MFC eD2K client UDP record exact wire bytes, receive dispositions,
  and correlated socket-boundary send attempts and terminal outcomes in the
  same `diag_event_v2` family. The harness compares exact packet bytes, audits
  each side's lifecycle independently, and requires the family across complete
  captures while keeping narrow action windows sampling-tolerant.
  Rust server TCP and UDP diagnostics now preserve trace/state context and emit
  correlated socket-boundary send attempts plus exactly one success, failure,
  or cancellation terminal outcome. The Rust `ed2k_server_udp` family still
  lacks an aligned MFC comparator and is not yet cross-client parity evidence.
  The soak launcher now captures ready, low-cadence periodic, and final bundles
  into a bounded campaign stream while pruning manifest entries as their bundle
  files rotate. The persisted watcher now enables strict Rust and MFC writer
  monitoring only after the current campaign publishes readiness, persists the
  complete 41-field health payloads, and stops the launcher fail-closed on any
  contract, drop, write, retention, storage-policy, or writer-I/O fault. The
  launcher then captures final bundle evidence before teardown. Preflight now
  leaves the profile-resident writer rings intact and promotes only bounded,
  validated, hash-verified Rust/MFC run suffixes after proving both profile-bound
  process families are quiescent. Complete-run indexes and bounded observer
  state now have deterministic multi-day coverage, and the observer is
  integrated as an attach-only controller-owned sidecar. It can now schedule
  exact synchronized Rust/MFC searches through the reusable REST action engine
  under a manifest-only, disabled-by-default configuration with a minimum
  five-minute cadence. Local terms, labels, keys, and failures remain
  unredacted. The single current observer-state v4 contract is bound to the
  exact action configuration and can persist a reserved cycle, deterministic
  action/report identity, per-client create/result outcomes, diagnostic run
  identities, UTC deadline, and evidence-pending state across restart. Each
  client create is prepared durably before its public POST; restart ambiguity
  fails closed, and a skipped sibling is recorded explicitly rather than
  issuing or replaying a one-sided action.
  The action driver now exposes typed create/result phases, resumes a persisted
  search identifier without issuing another POST, and preserves exact errors
  and incomplete polling rows while retaining the legacy complete-cycle output.
  The attach-only observer now wires those transitions around live REST side
  effects, pins exact diagnostic process/run identities before each action,
  persists both prepared creates before the first POST, persists every terminal
  phase immediately, resumes known search IDs with GET-only polling, and
  recovers a missing evidence-pending marker without replaying an action. It
  intentionally stops at evidence pending. The diagnostic loader can now select
  the pinned `(client, processId, runId)` without falling forward to a newer run
  and returns stable exact-byte segment provenance plus strict envelope and
  process-sequence validation. The observer runtime now derives Rust
  `packet-dump` and MFC `logs` directories only from the persisted session's
  validated profile authority and rejects missing or malformed profile roots.
  Observer action reports now have deterministic sequence/action filenames,
  exact-byte idempotent replay, conflict rejection, and recovery from an exact
  interrupted temporary write under the existing bounded stream policy.
  Action evidence slicing now uses one immutable authoritative UTC window,
  rejects malformed, missing, non-UTC, and legacy-schema timestamps instead of
  silently dropping records, and lets the report diff consume the persisted
  window rather than reconstructing it from observation time.
  Exact segment snapshots now also retain whether the source ended with a line
  terminator and whether an allowed partial active tail was ignored, including
  the distinct complete-JSON-without-terminator case. A pure action-evidence
  boundary now loads only the manifest-pinned Rust and MFC writer runs, slices
  every segment against the authoritative persisted UTC window, and retains
  exact unredacted segment provenance and explicit tail-completeness findings.
  Global-search assessment now remains explicitly `not-assessable` without
  aligned MFC server-UDP evidence; Rust-only traffic cannot establish parity.
  Observer state and offline summaries retain dedicated `not-assessable` and
  `evidence-incomplete` totals instead of collapsing them into divergence or an
  unspecified fallback bucket.
  Arbitrary-length authorization remains blocked until that evidence is wired
  into the observer's single action report, report-first crashes are reconciled
  into cumulative state, the UTC deadline is reconciled, retained-window
  reporting is aligned, and guarded live validation proves the complete path.

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
  missing/schema/parse/sequence evidence, and stable sensitive-value
  fingerprints. Local
  validation: 125 REST tests and 431 core tests passed; format, Clippy, all
  platform build/test jobs, CodeQL, dependency policy, and live REST/OpenAPI
  conformance passed.
- `emulebb/emulebb-build-tests#22` and `#23` landed run-aware segmented trace
  selection and the strict common-v2 parity gate. Current comparisons select
  one process identity, enforce segment and sequence continuity, require
  lossless writer health and semantic action coverage, and keep v1 only behind
  the explicit legacy MFC adapter.
- `emulebb/emulebb#179` landed the MFC segmented `diag_event_v2` writer,
  process/family sequencing, global retention, writer health, and complete
  unredacted eD2K/Kad payloads.
- `emulebb/emulebb-rust#166` landed the shared segmented diagnostics crate,
  strict `diag_event_v2`, exact unredacted bundle evidence, eD2K server/client
  UDP/peer TCP and Kad UDP wire coverage, decode/drop/flood/send/receive
  outcomes, and successful peer-obfuscation transcripts. Local validation
  passed the full workspace, 1,180 diagnostic eD2K tests, 78 diagnostic Kad-net
  tests, 75 diagnostic daemon tests, strict Clippy, formatting, and all required
  Linux/macOS/Windows, CodeQL, dependency, and live REST/OpenAPI checks.
- `emulebb/emulebb-build-tests#24` removed the no-op Rust `fullMemory` request
  and echoed result from contract smoke, Windows VM smoke, and local
  dump/crash smoke while preserving the unrelated crash-dump preference in the
  local swarm harness. All 20 required PR checks passed.
- `emulebb/emulebb-tooling#63` removed `fullMemory` from the Rust-only OpenAPI
  request and documented the complete diagnostic result. The shared and MFC
  contracts remain unchanged.
- `emulebb/emulebb-rust#167` removed `fullMemory` and
  `fullMemoryIncluded` end to end from the request, route metadata, response,
  bundle, tests, and Web UI. Legacy clients now receive strict unknown-field
  validation. Local validation passed 127 REST tests, the complete core suite,
  strict Clippy, 28 Web UI unit tests, typecheck, and production build; all
  required Linux/macOS/Windows, CodeQL, dependency, and live REST/OpenAPI checks
  passed.
- `emulebb/emulebb-rust#168` added exact successful eD2K client UDP wire and
  decoded-payload records to the bounded `ed2k_client_udp` `diag_event_v2`
  family. Independent review also found and fixed receive diagnostics using the
  local public IP rather than the remote sender IP for obfuscation. Local
  validation passed 1,181 diagnostic eD2K tests plus strict default and feature
  Clippy; all required Linux/macOS/Windows, CodeQL, dependency, and live
  REST/OpenAPI checks passed.
- `emulebb/emulebb-rust#169` completed Rust client-UDP receive outcome evidence
  for filtered, banned, non-IPv4, undecodable, malformed, unknown,
  unregistered, unsolicited, and reask-disabled traffic; centralized the four
  production send paths; added pre-await attempt records and correlated
  success, failure, and cancellation outcomes; and classified reask, buddy
  relay, direct-callback, port-test, and unknown protocol phases. Local
  validation passed 1,186 diagnostic eD2K tests, the complete core diagnostic
  suite, exact workspace Clippy, and formatting; all required
  Linux/macOS/Windows, CodeQL, dependency, and live REST/OpenAPI checks passed.
- `emulebb/emulebb-rust#170` separated each reask's logical source endpoint
  from its direct or buddy-relayed wire destination and moved pending-reply
  mutation behind confirmed local UDP send success. Local send errors and
  abandoned work now remain retryable without becoming false remote timeouts or
  influencing TCP fallback. Local validation passed 1,188 diagnostic eD2K
  tests, the complete core diagnostic matrix, exact workspace Clippy, and
  formatting; all required Linux/macOS/Windows, CodeQL, dependency, and live
  REST/OpenAPI checks passed.
- `emulebb/emulebb#180` added the MFC `ed2k_client_udp` v2 emitter with exact
  unredacted wire bytes, accepted/ignored/dropped receive outcomes, stable
  socket-boundary send attempts, and exactly one success, failure, or
  cancellation terminal per attempt. Debug, Release, and diagnostics Release
  builds passed before each granular commit; all PR checks passed.
- `emulebb/emulebb-build-tests#25` added the dedicated mixed client-UDP packet
  and lifecycle diff, complete-capture required-family and per-side lifecycle
  gates, cross-client and offline-soak enforcement, compact failure summaries,
  native seam coverage, and the canonical single-schema contract. Local
  validation passed 2,368 Python tests with one skip and one deselection plus
  832 native parity tests; all PR checks passed.
- `emulebb/emulebb-tooling#69` published the bundle-v3 OpenAPI contract and made
  its bounded, unified-only `diag_event_v2` artifact policy explicit. Both local
  documentation gates and all PR checks passed.
- `emulebb/emulebb-rust#171` changed diagnostic bundles to unified-only v3,
  retired the client-UDP and Kad-UDP unbounded side-file writers, completed Kad
  flow, trace, state, outcome, tracker, and exact-byte context in
  `diag_event_v2`, and exposed the SHA-256 of the exact loaded IP-filter source.
  The full workspace suite, focused diagnostic suites, strict Kad Clippy, and
  formatting passed locally; all Linux, macOS, Windows, CodeQL, dependency,
  policy, and live REST/OpenAPI PR checks passed.
- `emulebb/emulebb-build-tests#26` moved Rust server startup-failure context to
  the selected current `diag_event_v2` run, accepted server TCP and server UDP
  records, and removed the harness dependency on the unbounded server side
  file before its retirement. Local validation passed 2,369 Python tests with
  one skip and one deselection; all PR checks passed.
- `emulebb/emulebb-rust#172` preserved server trace/state correlation, added
  attempted and exactly-one-terminal send lifecycles for server TCP and UDP,
  routed plaintext and obfuscated login frames through the diagnostic-aware
  send contract, and retired the combined unbounded server packet side file.
  The full workspace suite and supported quick quality gate passed locally;
  all Linux, macOS, Windows, CodeQL, dependency, policy, and live REST/OpenAPI
  PR checks passed.
- `emulebb/emulebb-build-tests#27` migrated every active peer-TCP, client-UDP,
  Kad-UDP, server-startup, packet-coverage, offline-diff, secure-ident, Linux
  direct-smoke, and reflected-self-source consumer to exact selected
  `diag_event_v2` runs. Current validation rejects legacy packet side-file
  input rather than silently accepting it. Local validation passed 2,377
  Python tests with one skip and one deselection; all baseline, fast-harness,
  portability, dependency, and CodeQL PR checks passed.
- `emulebb/emulebb-rust#173` preserved peer-TCP trace/state correlation and
  retired the final Rust peer packet and obfuscation-handshake side-file
  writer. Packet, state, and handshake classification now occurs directly in
  the internal unified-event record. Local validation passed 1,190 diagnostic
  eD2K tests and 1,182 default-feature eD2K tests plus the supported quick
  quality gate; all Linux, macOS, Windows, CodeQL, dependency, policy, and live
  REST/OpenAPI PR checks passed.
- `emulebb/emulebb-build-tests#28` added the strict versioned `soak_storage`
  ignored-input contract, deterministic whole-file inventory and free-space
  seams, and a reusable `BoundedArtifactStore`. It protects active and pinned
  evidence, selects only complete closed artifacts oldest-first, and enforces
  maximum retained age, aggregate bytes, and minimum free-space reserve without
  redacting or mutating protocol records. Local validation passed 2,405 Python
  tests with one skip and one deselection; all baseline, fast-harness,
  portability, dependency, analysis, and CodeQL PR checks passed.
- `emulebb/emulebb-build-tests#29` moved converged reports and archives under
  the campaign-owned `soak/campaigns/<campaign-id>` boundary and left only
  stable pointers under `soak/last-run`. This prevents the storage authority
  from pruning profiles or unrelated operational state under the broader
  `soak` tree. Local validation passed 2,405 Python tests with one skip and one
  deselection; all required PR checks passed.
- `emulebb/emulebb-build-tests#30` made `soak_storage` mandatory for persisted
  sessions, assigned the campaign identity before launch, proved feasibility
  without mutation, and then applied and verified pruning under the campaign
  root before any control-file mutation or process start. The prior selected
  campaign and the new campaign remain protected. Launch fails closed on an
  impossible policy, deletion failure, post-delete reserve failure, or a
  last-run manifest that escapes the campaign root. Local validation passed
  2,411 Python tests with one skip and one deselection; all baseline,
  portability, dependency, analysis, CodeQL, and Windows harness PR checks
  passed.
- `emulebb/emulebb-build-tests#31` replaced append-only detached launcher and
  watcher logs with campaign-owned exact-byte supervisors. Each supervisor
  drains stdout and stderr concurrently, rotates to the configured hard
  segment and retention limits, fingerprints the actual supervised process,
  and fails closed by requesting graceful teardown before process-tree
  termination. Storage validation now budgets all four active controller
  output segments, and launch reuses one validated local-input snapshot across
  preflight and enforcement. Local validation passed 2,418 Python tests with
  one skip and one deselection; all baseline, portability, dependency,
  analysis, CodeQL, and Windows harness PR checks passed.
- `emulebb/emulebb-build-tests#32` moved the persisted Rust daemon's merged
  stdout/stderr into `campaigns/<campaign-id>/daemon-output` and applied the
  mandatory `daemon_output` segment and retention policy without wrapping or
  replacing the real daemon process identity. Exact bytes are drained
  asynchronously, sink failures stop Rust and fail the run, teardown includes
  output integrity, and the campaign manifest records the complete output
  contract. Local validation passed 2,426 Python tests with one skip and one
  deselection; all baseline, portability, dependency, analysis, CodeQL, and
  Windows harness PR checks passed.
- `emulebb/emulebb-build-tests#33` made the persisted session manifest the
  immutable storage authority for later lifecycle enforcement. It stores the
  canonical strict `soak_storage` payload, its deterministic SHA-256, the
  active campaign, the protected previous campaign, and launch planning and
  enforcement evidence. Parsing rejects policy tampering, malformed evidence,
  invalid campaign IDs, output-root mismatches, and campaign path escapes.
  Local validation passed 2,434 Python tests with one skip and one deselection;
  all baseline, portability, dependency, analysis, CodeQL, and Windows harness
  PR checks passed.
- `emulebb/emulebb-build-tests#34` made the watcher consume that immutable
  storage authority once and enforce aggregate campaign storage on every
  sample. Storage, context, evidence, heartbeat-authority, and watcher-liveness
  faults now fail closed: terminal evidence is persisted, both stop paths are
  requested, the complete owned process tree is verified or force-terminated,
  and status surfaces authoritative storage failure, stale evidence, or an
  unexpected watcher exit. Exact fallback process identity, late descendants,
  PID reuse, and terminal heartbeat behavior are covered. Local validation
  passed 2,461 Python tests with one skip and one deselection; all baseline,
  portability, dependency, analysis, CodeQL, and Windows harness PR checks
  passed. Independent fail-closed review found no remaining high- or
  medium-severity issue.
- `emulebb/emulebb-build-tests#35` made persisted launch planning reserve the
  full retained capacity of all four controller-output streams and the merged
  daemon-output stream against both aggregate bytes and minimum free space.
  The strict policy now rejects totals that cannot contain those streams,
  planning and enforcement verify the same reservation before any control-file
  mutation or process start, and persisted evidence records the auditable
  per-stream derivation. Exact-sliced process output needs no oversized-record
  slack. Local validation passed 2,470 Python tests with one skip and one
  deselection; all baseline, portability, dependency, analysis, CodeQL, and
  Windows harness PR checks passed. Independent capacity review confirmed the
  retention formula and absence of watcher double-counting.
- `emulebb/emulebb-tooling#80` aligned the strict OpenAPI
  `DiagnosticWriterHealth` schema with all 41 always-present Rust fields and
  the nullable seven-value storage block reason. Exact required/property
  coverage, YAML parsing, and the persisted live REST/OpenAPI harness passed.
- `emulebb/emulebb-rust#174` extracted deterministic segment retention and
  added aggregate-byte, retained-age, retained-count, and minimum-free-space
  enforcement; full-segment growth reservation; exact oversized-record budget
  checks; cause-specific drops; latched storage-authority and writer-I/O
  faults; fail-closed configuration parsing; complete writer-health REST and
  bundle diagnostics; and the merged tooling contract pin. Local validation
  passed 20 diagnostics tests, 131 REST tests, the full Rust workspace suite,
  strict Clippy, formatting, and live REST/OpenAPI conformance. All required
  Linux, macOS, Windows, CodeQL, policy, dependency, workflow-lint, and live
  conformance checks passed. The broader product-family quality command reached
  only the unrelated pre-existing generated-artifact audit failures for the
  build-tests `.venv` executables and Rust `webui/node_modules`.
- `emulebb/emulebb-build-tests#36` introduced the breaking
  `emulebb-build-tests.soak-storage-policy.v2` contract with a dedicated Rust
  diagnostic writer policy, passed the complete policy through an explicit
  child-process environment without mutating the controller environment, and
  made exact `diag_event_v2` writer readiness a prerequisite for public
  actions. Applied policy and startup writer health are persisted in campaign
  evidence. Local validation passed 2,481 Python tests with one skip and one
  deselection; all baseline, portability, dependency, analysis, CodeQL, and
  Windows harness PR checks passed.
- The ignored operator input was migrated backup-first to the selected
  operator-owned persisted Rust profile and storage-policy v2. The configured
  profile-local writer ring is bounded to 8 GiB with 64 MiB segments, 128
  retained segments, seven-day retained age, and a 20 GiB free space floor.
  The typed repository loader accepted the result. No client was launched.
- `emulebb/emulebb-tooling#83` replaced the Rust-only path-returning diagnostic
  dump contract with authenticated inline `emulebb.diagnostic-bundle.v4`
  capture. The breaking API uses `POST /api/v1/diagnostics/bundles` with an
  exact `confirmCapture` sentinel and returns the strict bundle directly.
- `emulebb/emulebb-rust#175` removed daemon-owned bundle files and the retired
  dump wrapper, returned bundle v4 inline, embedded the strict summary, and made
  the WebUI download the exact response through the browser. Local validation
  passed 131 REST tests, the full workspace suite, strict Clippy, formatting,
  29 WebUI unit tests, type checking, and the production WebUI build. All
  Linux, macOS, Windows, policy, dependency, CodeQL, workflow-lint, and live
  REST/OpenAPI checks passed.
- `emulebb/emulebb-build-tests#37` introduced storage-policy v3 with a dedicated
  bounded diagnostic-bundle stream, atomic whole-JSON persistence, aggregate
  reservation and enforcement, and oldest-first retention. The canonical soak
  launcher captures strict bundle v4 evidence at ready and final phases before
  teardown and records exact paths, byte counts, hashes, deletions, and retained
  inventory in the run manifest. Local focused validation passed 234 tests;
  the full suite passed 2,484 tests with one skip and one deselection after the
  two compilation-timeout cases passed in isolation. Both Windows harness lanes
  and all baseline, portability, dependency, analysis, and CodeQL checks passed.
- `emulebb/emulebb-build-tests#38` schedules bundle v4 capture at the configured
  low cadence after readiness, keeps stop deadlines ahead of periodic capture,
  and prunes manifest entries when the bounded ring rotates their files. The
  effective interval is persisted in preflight evidence, and capture failures
  remain terminal while final evidence and teardown continue. Local validation
  passed 2,488 Python tests with one skip and one deselection; all Windows
  harness, baseline, portability, dependency, analysis, and CodeQL checks
  passed.
- `emulebb/emulebb-build-tests#39` centralized the exact 41-field
  `diag_event_v2` writer-health integrity contract, published a persisted
  `running` boundary only after client bring-up and ready-bundle capture, and
  added complete Rust/MFC writer snapshots to detached watcher evidence. Writer
  faults after readiness are terminal and request graceful launcher stop, which
  preserves the final bundle before teardown; startup remains tolerant while
  the last-run manifest is `starting`. Local validation passed 2,501 Python
  tests with one skip and one deselection. All baseline, portability,
  dependency, analysis, CodeQL, and duplicated Windows harness checks passed;
  one infrastructure-only GitHub API checkout timeout passed on failed-job
  rerun.
- `emulebb/emulebb-build-tests#40` added exact per-client REST evidence for
  blocking VPN Guard state and active `hide.me` P2P binding, then made
  post-readiness route, Guard, binding, process-count, writer-integrity, and
  unexpected launcher loss terminal. Diagnostics transport unavailability is
  distinct from writer-integrity failure; REST and diagnostics availability
  stop only after three consecutive samples, with same-campaign streaks
  restored across watcher restart. Every terminal class requests graceful stop
  and therefore reaches the final pre-teardown bundle capture. Local validation
  passed 2,507 Python tests with one skip and one deselection; all duplicated
  Windows harness, baseline, portability, dependency, analysis, and CodeQL
  checks passed.
- `emulebb/emulebb-build-tests#41` replaced preflight evacuation of the Rust
  profile ring with bounded promotion of validated quiesced Rust and MFC
  `diag_event_v2` run suffixes. Storage-policy v4 reserves per-client segment
  capacity; exact bytes are copied atomically without removing the profile
  source, source and destination SHA-256 are verified, and the compact manifest
  records process/run/segment identity, retained and promoted coverage, omitted
  prefix counts, byte counts, mtimes, and hashes. Preflight re-enumerates the
  profile-bound process families and fails before promotion if either remains
  live. Local validation passed 2,516 Python tests with one skip and one
  deselection; all duplicated Windows harness, baseline, portability,
  dependency, analysis, and CodeQL checks passed.
- `emulebb/emulebb-build-tests#42` added restart-safe complete-run indexing for
  exact closed Rust and MFC `diag_event_v2` segments. The strict
  `emulebb-build-tests.diagnostic-run-checkpoint.v1` cursor preserves the
  compact family, event, severity, outcome, opcode, process-sequence,
  family-sequence, segment-continuity, and exact 41-field writer-health state;
  rejects parse, identity, envelope, and gap violations; and distinguishes
  from-run-start coverage from a retained suffix. Storage-policy v6 adds
  dedicated bounded per-client index and evidence-pin streams. Interesting
  anomaly segments and their boundary context are copied byte-for-byte under a
  priority budget with SHA-256 verification and checkpoint-atomic swap
  recovery. Local validation passed 2,549 Python tests with one skip and one
  deselection; all duplicated Windows harness, baseline, portability,
  dependency, analysis, and CodeQL checks passed.
- `emulebb/emulebb-build-tests#43` added storage-policy v7 reservations for
  observer actions, checkpoints, summaries, and future sidecar process output.
  It also added the strict
  `emulebb-build-tests.converged-observer-state.v1` reducer: exact cumulative
  action, verdict, checkpoint, driver, and retention counters with bounded
  recent samples and restart-safe canonical persistence. A deterministic
  logical three-day simulation covers 864 checkpoints, 144 actions, mid-run
  summary reload, exact cumulative results, and bounded retained files. Local
  validation passed 2,553 Python tests with one skip and one deselection; all
  duplicated Windows harness, baseline, portability, dependency, analysis,
  and CodeQL checks passed.
- `emulebb/emulebb-build-tests#44` added a new attach-only converged observer
  and made it a default controller-owned sibling of the sole client-owning
  `launch-soak.py` process. The observer waits for the existing campaign,
  captures complete Rust and MFC diagnostic-writer health into the v7 bounded
  checkpoint and cumulative-summary streams, honors the shared stop contract,
  and has exact PID-plus-creation-time identity, bounded stdout/stderr,
  startup rollback, status findings, and graceful or exact forced teardown.
  The legacy second-launcher path is not reused. Local validation passed 2,560
  Python tests with one skip and one deselection; all 20 duplicated Windows
  harness, baseline, portability, dependency, analysis, and CodeQL checks
  passed. No client was launched.
- `emulebb/emulebb-build-tests#45` extracted synchronized REST search/download
  driving, candidate policy, typed client endpoints, and action correlation
  state into `emule_test_harness.converged_action_driver`. The legacy soak
  runner now delegates to that engine instead of owning a duplicate
  implementation, and retained local action reports/logs keep exact labels and
  keys rather than privacy-redacted placeholders. Local validation passed 2,564
  Python tests with one skip and one deselection; all 20 duplicated Windows
  harness, baseline, portability, dependency, analysis, and CodeQL checks
  passed. No client was launched.
- `emulebb/emulebb-build-tests#46` integrated search-only synchronized action
  scheduling into the attach-only observer. Controller start options resolve an
  exact term snapshot from explicit values or `generic_open`, persist it in the
  single current `emulebb.persisted-soak-session.v3` manifest, and keep it off
  the process command line. Action driving is disabled by default, requires the
  observer and watcher lifecycle, enforces a 300-second minimum cadence, rotates
  terms deterministically, records exact failures in cumulative state, and
  gives the observer no client ownership. Local validation passed 2,576 Python
  tests with one skip and one deselection; all 20 duplicated Windows harness,
  baseline, portability, dependency, analysis, and CodeQL checks passed. No
  client was launched.
- `emulebb/emulebb-build-tests#47` preserved independent Rust and MFC search
  create and result-poll outcomes in the shared action engine. Both creates are
  issued before either result poll; one-sided success retains its exact search
  ID, result count, completion state, and unredacted error from the failing
  side; incomplete bounded polling is not reported as a completed cycle; and an
  unsafe download request without an explicit candidate policy is rejected
  before any public action. Local validation passed 2,581 Python tests with one
  skip and one deselection; every final baseline, portability, harness,
  dependency, analysis, and CodeQL check succeeded. No client was launched.
- `emulebb/emulebb-build-tests#48` replaced the observer summary with the single
  current `emulebb-build-tests.converged-observer-state.v2` contract. State is
  bound to a canonical action-configuration SHA-256, enforces strict next-cycle
  continuity and a restart-safe UTC deadline, assigns a deterministic
  campaign/cycle action ID and report sequence, and persists exact per-client
  create/result timestamps, search IDs, incomplete polling, errors, and exact
  Rust/MFC diagnostic process/run identities. Evidence cannot become pending
  until both client outcomes and the matching driver outcome are terminal, and
  only a report with the same action ID, cycle, and sequence may clear the
  pending action. Duplicate reservations and phase writes, ambiguous creates,
  skipped or repeated cycles, premature evidence, configuration drift, and the
  legacy direct-report bypass fail closed. Local validation passed 2,588 Python
  tests with one skip and one deselection; all 20 duplicated Windows harness,
  baseline, portability, dependency, analysis, and CodeQL checks passed. No
  client was launched.
- `emulebb/emulebb-build-tests#49` split search creation and bounded result
  polling into typed terminal phases. A caller can supply a previously persisted
  search ID to resume without another POST; blank IDs and inconsistent phase
  values fail closed. Exact unredacted per-client errors, incomplete polling
  status, and retained result rows survive the phase boundary, while the legacy
  automatic-cycle output delegates through the new API unchanged. Local
  validation passed 2,590 Python tests with one skip and one deselection; all 20
  duplicated Windows harness, baseline, portability, dependency, analysis, and
  CodeQL checks passed. No client was launched.
- `emulebb/emulebb-build-tests#50` replaced observer-state v2 with the single
  current v3 contract after a crash-window audit found that outcome-only
  persistence could replay a POST whose response had not been saved. V3 records
  a prepared create before each public POST, requires a separate terminal
  succeeded or failed transition, supports an exact fail-closed skipped sibling,
  and rejects driver completion until both client paths are terminal. A prepared
  create survives restart as explicit ambiguity and cannot be issued again.
  Local validation passed 2,591 Python tests with one skip and one deselection;
  all 20 duplicated Windows harness, baseline, portability, dependency,
  analysis, and CodeQL checks passed. No client was launched.
- `emulebb/emulebb-build-tests#51` wired observer-state v3 around the phased
  REST action driver. The observer pins exact healthy diagnostic process/run
  identities before side effects, persists both prepared creates atomically
  before the first POST, persists each terminal create and result phase
  immediately, resumes persisted successful search IDs with GET-only polling,
  preserves partial result counts, and converts restart-visible prepared
  creates to exact ambiguity without replay. A crash after driver persistence
  but before the evidence marker is recovered without another POST or poll.
  The cycle stops safely at evidence pending until exact diagnostic extraction
  and report persistence land. Local validation passed 2,593 Python tests with
  one skip and one deselection; all 20 duplicated Windows harness, baseline,
  portability, dependency, analysis, and CodeQL checks passed. No client was
  launched.
- `emulebb/emulebb-build-tests#52` added exact diagnostic run selection by
  client, process ID, and run ID without newest-run fallback. One stable run
  snapshot now retains every selected segment's resolved path, exact byte count,
  modification time, SHA-256 digest, and parsed records while enforcing segment
  continuity, exact record envelopes, positive stream/process sequences, and
  contiguous process sequence across rotated and active segments. The existing
  latest-run compatibility loader delegates to the same strict implementation.
  Local validation passed 2,597 Python tests with one skip and one deselection;
  all 20 duplicated Windows harness, baseline, portability, dependency,
  analysis, and CodeQL checks passed. No client was launched.
- `emulebb/emulebb-build-tests#53` added typed Rust and MFC diagnostic
  directories to the observer runtime. The directories are derived only from
  the persisted preflight profile authority as Rust `packet-dump` and MFC
  `logs`; malformed authority, unknown profile fields, empty paths, and missing
  profile roots fail before evidence loading. Local validation passed 2,603
  Python tests with one skip and one deselection; all 20 duplicated Windows
  harness, baseline, portability, dependency, analysis, and CodeQL checks
  passed. No client was launched.
- `emulebb/emulebb-build-tests#54` replaced timestamp-named observer action
  artifacts with deterministic sequence/action identities. Exact canonical
  payload replay is accepted as already committed, changed payload reuse is
  terminal conflict, and an exact interrupted temporary write is recovered
  without duplication while conflicting or ambiguous temporary state fails
  closed. Local validation passed 2,607 Python tests with one skip and one
  deselection; all 20 duplicated Windows harness, baseline, portability,
  dependency, analysis, and CodeQL checks passed. No client was launched.
- `emulebb/emulebb-build-tests#55` added an immutable strict UTC action-window
  contract and migrated the scheduler, action diff, and offline consumer to it.
  Slicing now rejects missing, malformed, non-UTC, unsupported, and legacy
  timestamps instead of silently omitting evidence; current `diag_event_v2`
  records must use `ts`, and `diff_action` accepts the observer's authoritative
  persisted window. Local validation passed 2,614 Python tests with one skip
  and one deselection; all 20 duplicated Windows harness, baseline,
  portability, dependency, analysis, and CodeQL checks passed. No client was
  launched.
- `emulebb/emulebb-build-tests#56` added exact per-segment tail provenance to
  diagnostic snapshots. Each snapshot now distinguishes a line-terminated
  source, a complete unterminated JSON record, and an allowed malformed active
  tail that was ignored; exact run snapshots preserve those flags beside the
  existing path, bytes, modification time, digest, and records. Local
  validation passed 2,616 Python tests with one skip and one deselection; all
  20 duplicated Windows harness, baseline, portability, dependency, analysis,
  and CodeQL checks passed. No client was launched.
- `emulebb/emulebb-build-tests#57` added pure exact-run action evidence capture.
  It accepts only manifest-pinned Rust and MFC process/run identities, performs
  strict per-segment slicing against the authoritative UTC action window, never
  falls forward to a newer run, and reports exact unredacted paths, byte counts,
  modification times, SHA-256 values, record counts, writer identities, and tail
  provenance. Missing runs, malformed timestamps, parse or identity failures
  remain terminal harness errors; ignored malformed tails and complete records
  without a line terminator are explicit incomplete evidence. Local validation
  passed 2,621 Python tests with one skip and one deselection; all 20 duplicated
  Windows harness, baseline, portability, dependency, analysis, and CodeQL
  checks passed. No client was launched.
- `emulebb/emulebb-build-tests#58` removed the Rust-only global-search parity
  path. Global search is now explicitly `not-assessable` until aligned MFC
  server-UDP evidence exists, and offline campaign assessment propagates that as
  inconclusive rather than parity or protocol divergence. The single current
  observer state is now v4 with dedicated `not-assessable` and
  `evidence-incomplete` totals and histograms. Local validation passed 2,625
  Python tests with one skip and one deselection; all 20 duplicated Windows
  harness, baseline, portability, dependency, analysis, and CodeQL checks
  passed. No client was launched.
- `emulebb/emulebb-build-tests#59` completed action-specific diagnostic-family
  assessment. Explicit server searches now require `ed2k_tcp`, explicit Kad
  searches require `kad_udp`, and global searches compare direct
  `ed2k_server_udp` records rather than adapting them through the TCP packet
  view. Missing required Rust families are `evidence-incomplete`; missing
  aligned MFC server-UDP evidence remains `not-assessable`. Kad assessment no
  longer depends on synthetic TCP packet lists. Local validation passed 2,627
  Python tests with one skip and one deselection; all 20 duplicated Windows
  harness, baseline, portability, dependency, analysis, and CodeQL checks
  passed. No client was launched.
- `emulebb/emulebb-build-tests#60` added the single current pure observer
  action-report contract,
  `emulebb-build-tests.observer-action-report.v1`. It combines the pending
  action identity, exact phased driver outcome, manifest-pinned diagnostic
  source provenance, and method-specific protocol assessment without copying
  raw action-window records into the report. Exact incomplete-tail provenance
  forces an `evidence-incomplete` top-level verdict even when the retained
  subset otherwise reaches parity. Successful, one-sided, and both-failed
  driver outcomes all produce deterministic reports, and the strict validator
  rejects schema, identity, window, provenance, aggregate-count, and assessment
  drift. Local validation passed 2,634 Python tests with one skip and one
  deselection; all 20 duplicated Windows harness, baseline, portability,
  dependency, analysis, and CodeQL checks passed. No client was launched.
- `emulebb/emulebb-build-tests#61` added a narrow report-first pending-action
  finalization transaction. It reconstructs only the persisted UTC window and
  manifest-pinned writer identities, captures exact evidence, builds the #60
  report, persists the immutable action first, commits cumulative state second,
  records action-retention metadata third, and persists the singleton summary
  last. A report persistence failure cannot commit state or summary. The
  transaction is intentionally not invoked by the observer loop until
  report-first crash reconciliation is available. Local validation passed 2,636
  Python tests with one skip and one deselection; all 20 duplicated Windows
  harness, baseline, portability, dependency, analysis, and CodeQL checks
  passed. No client was launched.
- `emulebb/emulebb-rust#176` advanced the single current inline bundle contract
  to `emulebb.diagnostic-bundle.v5` and added bounded exact operational
  snapshots for servers, shared files, searches and their evidence-rich
  results, transfers, uploads, and the upload queue. Hash-map-backed searches
  and transfers are sorted before newest-tail retention; catalog and queue
  surfaces retain deterministic prefixes; every bound exposes exact omission
  counts; and search evidence retains raw names, source identities, AICH, and
  observation rows without redaction. The canonical quick gate, release builds,
  full workspace tests, WebUI unit/end-to-end/build checks, and all three VPN
  egress tests passed locally. All required Linux, macOS, Windows, CodeQL,
  dependency, policy, and live REST/OpenAPI checks passed. No client was
  launched.
- The ignored operator input was migrated backup-first to storage-policy v4
  with a 4 MiB by 48-artifact diagnostic-bundle ring and a 64 MiB by four-file
  diagnostic-segment ring for each client. The typed repository loader accepted
  the policy and selected persisted profile. No client was launched.
- The ignored operator input was subsequently migrated backup-first to
  storage-policy v6 with an 8 MiB singleton diagnostic index and a 64 MiB by
  four-file diagnostic evidence-pin ring for each client. The typed repository
  loader accepted both the example and ignored local inputs. No client was
  launched.
- The ignored operator input was subsequently migrated backup-first to
  storage-policy v7 with bounded observer action, checkpoint, and singleton
  summary streams plus capacity for future observer stdout and stderr. The
  typed repository loader accepted both the example and ignored local inputs.
  No client was launched.
- `emulebb/emulebb-tooling#59` through `#62` aligned the common-v2 product
  contract, segmented filenames and writer-health evidence, and the explicit
  local-only unredacted trace policy.
- The operator-reported concurrent IP-filter work was reconciled after its
  compilation completed. Commit `3a34079c` (`feat(ipfilter): expose loaded
  source digest`) was already in `main` ancestry and therefore remained in the
  base of Rust #174; there was no additional uncommitted IP-filter delta to
  recover.
- No public live client was launched for these foundation slices; guarded live
  and tunnel-down acceptance evidence remains outstanding.

## Storage Audit - 2026-10-25

- Resolved by Rust #174: the unified Rust event ring now enforces segment size,
  rotation age, retained segment count, aggregate bytes, retained age, and
  minimum free space. The active segment remains protected, and exact
  oversized records are accepted only when the full growth fits the storage
  policy. The writer publishes its maximum permitted growth for harness
  reservation and monitoring.
- The persisted soak watcher rotates its JSONL history. Detached launcher and
  watcher stdout/stderr and the Rust daemon's merged stdout/stderr are
  campaign-owned exact-byte bounded streams, and the watcher now enforces the
  aggregate campaign policy on every sample. Build-tests #39 also makes the
  post-readiness Rust/MFC writer-health contract part of every watcher sample
  and fails closed on storage, watch-evidence, or writer-integrity loss. Rust
  daily application-log rotation bounds file count but not bytes generated
  within one day.
- Resolved by build-tests #41: profile diagnostic rings remain in place across
  campaigns. After stale-process cleanup, preflight proves both profile-bound
  process families are gone, strictly validates the selected retained run
  suffix, reserves campaign storage, atomically copies exact whole segments,
  verifies source and destination hashes, and publishes compact identity and
  coverage metadata. The bounded per-client promotion rings are part of the
  aggregate byte, age, and free-space policy.
- Resolved by tooling #83, Rust #175, and build-tests #37: bundle capture is now
  inline and caller-owned, the daemon creates no bundle directory in the
  reusable profile, and the soak harness persists exact immutable JSON into a
  dedicated campaign stream with per-artifact, retained-count, aggregate-byte,
  age, and free-space enforcement. Ready, low-cadence periodic, and final
  captures are now bounded. Every classified post-readiness terminal health or
  integrity fault now requests the same final pre-teardown capture.
- Persisted preflight now reserves the full retained capacity of every standard
  protected process-output stream, and the watcher enforces actual campaign
  bytes and free space throughout the run. The launcher independently injects
  and verifies the bounded Rust profile-writer policy before public actions.
  Other non-stream active outputs such as profiling data do not yet have a
  complete growth reservation.
- Resolved as a storage foundation by build-tests #43: observer actions,
  checkpoints, and the singleton cumulative summary now have strict bounded
  stream budgets, and deterministic multi-day restart simulation proves exact
  cumulative state with a bounded retained detail window. Build-tests #44 wires
  passive checkpoints and summaries to those owners through an attach-only
  sidecar while keeping the launcher as the sole client owner. Build-tests #45
  extracted synchronized action driving and correlation from the legacy
  second-launcher script into reusable package code. Build-tests #46 integrated
  search-only scheduling into the sidecar with exact manifest-owned terms and
  cumulative cycle state. Build-tests #47 preserves exact independent
  per-client action outcomes. Build-tests #48 provides the strict current state
  schema and pure crash-safe transitions for pending actions. Build-tests #49
  provides the resumable typed create/result execution phases. Build-tests #50
  closes the pre-POST ambiguity gap with the single current state v3 contract,
  and build-tests #51 wires that contract around REST side effects with exact
  run pinning and immediate phase persistence. Build-tests #52 provides exact
  run loading with immutable source provenance and no fallback to a newer run;
  build-tests #53 binds its source directories to manifest-owned profile
  authority; build-tests #54 provides deterministic idempotent report storage
  with exact replay and conflict detection; build-tests #55 provides strict
  authoritative UTC window slicing without silent timestamp loss; build-tests
  #56 exposes exact tail termination and ignored-partial-tail provenance; and
  build-tests #57 provides pure exact-run action evidence capture with bounded
  report metadata and in-memory action-window records. Build-tests #58 replaces
  observer state v3 with the single current v4 contract, adds explicit
  inconclusive verdict buckets, and prevents Rust-only global-search evidence
  from becoming parity. Build-tests #59 completes action-specific family
  selection for server, global, and Kad searches, including direct server-UDP
  assessment and Kad assessment without a TCP proxy. Build-tests #60 provides
  the single current pure observer report contract and strict validator, and
  build-tests #61 provides the report-first finalization transaction without
  enabling it in the recurring observer loop. Report-first startup
  reconciliation, loop integration, and UTC deadline reconciliation still
  require integration.
  Diagnostic segments remain immutable and exact; enabling diagnostic tail
  trimming is not an acceptable storage design.
- Resolved by build-tests #42: arbitrarily long discovery now maintains compact
  complete-run family/event/severity/outcome/opcode and integrity indexes plus
  budget-aware preservation of selected immutable raw anomaly and context
  segments. Retaining all raw traffic forever is neither required nor safe.

The long-term owner is a harness-level `SoakStoragePolicy` and
`BoundedArtifactStore` with mandatory total-byte, maximum-age, and
minimum-free-space limits. It protects the active campaign, prunes only closed
unpinned artifacts oldest-first, rotates non-protocol process logs, checks
reserve before launch and promotion, and stops the run as inconclusive when the
reserve or evidence-integrity contract cannot be maintained. Evidence remains
unredacted; bounding is performed by rotating or deleting whole immutable
artifacts, never by field omission or mutation of `diag_event_v2` records.

## Next Implementation

- The `diag_event_v2` identity contract is `(processId, runId, segmentId)`.
  `seq` is process-wide retained-event order and `streamSeq` is retained-event
  order within one family. Files are named
  `emulebb-rust-diag-<processId>-<runId>-<segmentId>.jsonl`.
- Exercise the aligned `ed2k_client_udp` family in guarded bounded captures and
  use the new missing-family, exact-wire, and lifecycle findings to drive the
  next protocol-parity gaps. `diag_event_v2` remains the only current event
  envelope; `ed2k_client_udp` is a family within it, not a second schema.
- Use the complete-run indexes and pinned exact raw evidence from build-tests
  #42 to select and reconstruct the next deterministic and guarded parity gaps;
  retained-suffix coverage remains explicitly incomplete.
- Reconcile report-first crashes on startup before recapturing mutable active
  segments, then permit build-tests #61 to run from the observer loop. Build-tests
  #54 already makes persistence idempotent by stable action ID and sequence:
  identical replay is already committed, while different payload for the same
  identity is terminal corruption. Startup must locate the deterministic report
  path, validate the matching payload through build-tests #60, replay it through
  the existing identity store to recover exact retention metadata, commit it
  against the pending action, and never recapture or create a duplicate artifact.
  If no report exists, #61 may capture the pinned runs and finalize normally. A
  client restart, writer-run change, missing segment, parse failure, malformed
  timestamp, or ignored incomplete active tail must remain incomplete or terminal
  evidence; the observer must never silently switch to the newest run.
- After evidence/report commit clears the pending action, reconcile and persist
  the next UTC deadline before recurring scheduling is enabled. Startup must
  service the persisted deadline without relying on a previous process's
  monotonic clock and must never replay an ambiguous, completed, or one-sided
  public action. The sidecar must continue to never clean, launch, or stop either
  client.
- Keep checkpoint service independent of long result polling and finalize a
  pending evidence window before issuing another action. REST action failures
  remain evidence and may continue the soak; trace loading, report persistence,
  sequence, identity, or retention failures are harness-integrity failures that
  stop new actions and fail closed after the existing retry threshold.
- Add bounded download scheduling only after its safety policy, pending-action
  state, and restart reconciliation contract are explicit; a restarted observer
  must not replay a completed or one-sided public action.
- Update report summarization to combine exact cumulative observer state with
  the retained detail window and identify intentional rotation as omitted by
  retention rather than missing evidence.
- Add aligned MFC and harness coverage for Rust's `ed2k_server_udp` family
  before treating server UDP observations as cross-client parity evidence.
- Protocol and soak traces, bundles, manifests, and diagnostic payloads are
  explicitly local test evidence and will not be published. They must preserve
  exact file, peer, user, hash, endpoint, search, and packet data whenever that
  data helps reconstruct eD2K or Kad behavior. Redaction and privacy-driven
  field omission are not requirements for this lane; completeness is.
- Arbitrarily long public live soaks remain unauthorized while synchronized
  action output, retained-window reporting, remaining non-stream artifacts,
  and guarded live behavior are not fully bounded and validated. No live
  client has been launched during these implementation slices.

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
- [x] The diagnostic bundle API returns exact, unredacted local investigation
      evidence inline for bounded caller-owned persistence.
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
