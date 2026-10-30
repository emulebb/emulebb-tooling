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
  and requests graceful teardown before an exact-identity forced fallback. Its
  stop transaction now waits for both clients and the watcher, indexes the
  former active diagnostic segment on both sides, and reports failure rather
  than claiming a clean stop when the retained segment suffix is incomplete.
- Packet and semantic diagnostics cover substantial protocol surface. The
  common event stream now has a v2 process/run/segment envelope and bounded
  writers on Rust and MFC `main`. The harness selects one exact process run,
  enforces sequence and writer-health integrity, and rejects packet-only
  comparisons. Peer TCP now carries truthful clear-frame bytes plus peer/file
  hashes where available, Kad requests and lookup completions carry stable
  lifecycle keys, and the harness gates bilateral join-key coverage. Remaining
  correlation gaps must now be driven by guarded live evidence.
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
  unredacted. The single current observer-state v9 contract is bound to the
  exact action configuration and can persist a reserved cycle, deterministic
  action/report identity, per-client create/result outcomes, diagnostic run
  identities, strict UTC deadline, and evidence-pending state across restart.
  It also persists one durable success-counted parity gate with separate server
  and Kad targets, non-counting retryable outcomes, a sticky first confirmed
  divergence receipt, and the original green timestamp while action driving
  continues after either terminal gate state.
  A deadline cannot coexist with pending public work and is consumed atomically
  by reservation. Each client create is prepared durably before its public POST;
  restart ambiguity fails closed, and a skipped sibling is recorded explicitly
  rather than issuing or replaying a one-sided action.
  The action driver now exposes typed create/result phases, resumes a persisted
  search identifier without issuing another POST, and preserves exact errors
  and incomplete polling rows while retaining the legacy complete-cycle output.
  The attach-only observer now wires those transitions around live REST side
  effects, pins exact diagnostic process/run identities before each action,
  persists both prepared creates before the first POST, persists every terminal
  phase immediately, resumes known search IDs with GET-only polling, and
  recovers a missing evidence-pending marker without replaying an action. It now
  services every persisted pending action immediately on attach, before a fresh
  start delay or reached cycle limit can block recovery, and finalizes the
  immutable action report in the same call after driver completion. The
  recurring scheduler now initializes a missing deadline once, preserves an
  existing strict UTC deadline exactly across observer restart, reconciles the
  report-commit crash gap with the normal action interval, and replaces or
  clears the deadline after each action without inheriting a previous process's
  monotonic clock. The REST action driver now also exposes one bounded,
  no-wait search-result read and a typed one-shot phase that preserves exact
  local failures. The v9 state persists each client's immutable poll start and
  deadline, next attempt, attempt/error totals, latest attempt, latest observed
  count, and exact current and historical errors. The single-writer observer
  performs at most one due GET per loop, bounds it by the lesser of 30 seconds
  and the exact remaining UTC budget, classifies a response that finishes after
  the deadline as a deadline outcome, and retains terminal poll provenance in
  the immutable driver outcome. Checkpoint, stop, and health service therefore
  run between attempts instead of waiting behind a blocking result-poll loop.
  The legacy blocking poll composes the same one-shot primitive. The sole
  current `emulebb-build-tests.converged-soak-report.v3` contract now validates
  and embeds the exact bounded v9 observer state, reads only current action and
  checkpoint contracts, and describes the retained physical suffix separately
  from cumulative history. Whole-artifact rotation is reported as
  `omittedByRetention`, while retained count, byte, latest-file, campaign,
  action-sequence, or checkpoint-time inconsistencies retry boundedly during a
  concurrent update and otherwise fail closed. Retained action summaries read
  current nested assessments, aggregate v9 poll outcomes, and preserve exact
  per-action client poll provenance and errors without redaction. The
  diagnostic loader can now select the
  pinned `(client, processId, runId)`
  without falling forward to a newer run and returns stable exact-byte segment
  provenance plus strict envelope and process-sequence validation. The observer
  runtime now derives Rust
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
  The persisted-profile discovery lane is now authorized for until-stopped
  operation because non-stream artifacts are bounded and guarded live
  validation proved the complete start, gate, continued-action, and clean-stop
  path. Release certification still requires its separately bounded evidence.

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
  lossless writer health and semantic action coverage, and reject every schema
  other than the single current `diag_event_v2` contract.
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
- `emulebb/emulebb-build-tests#62` added report-first crash reconciliation. A
  deterministic final or prepared report is loaded and strictly validated
  against the exact pending action before any mutable active diagnostic segment
  is recaptured. The validated payload is replayed through the identity store to
  promote an exact prepared file when needed and recover current retention
  metadata. Ambiguous final-plus-temporary state and identity, window, driver,
  diagnostic-run, or assessment drift fail closed; only absence of a candidate
  permits fresh pinned-run capture. The recurring observer loop remains
  unchanged. Local validation passed 2,641 Python tests with one skip and one
  deselection; all 20 duplicated Windows harness, baseline, portability,
  dependency, analysis, and CodeQL checks passed. No client was launched.
- `emulebb/emulebb-build-tests#63` activated report-first finalization in the
  recurring attach-only observer. Driver completion now persists the exact
  evidence window and finalizes the immutable report in the same call. On
  attach, any persisted pending action bypasses both the configured start delay
  and a reached cycle limit, so incomplete phased work and report-first crash
  recovery run before another action can be reserved. Local validation passed
  2,642 Python tests with one skip and one deselection; all 20 duplicated
  Windows harness, baseline, portability, dependency, analysis, and CodeQL
  checks passed. No client was launched.
- `emulebb/emulebb-build-tests#64` advanced the single current observer-state
  contract to v5 and made `scheduler.nextActionAtUtc` strict scheduling
  authority. Deadlines must be explicit UTC, cannot coexist with pending public
  work, and are consumed atomically by cycle reservation, preventing restart
  recovery from confusing scheduled and in-flight work. Local validation passed
  2,646 Python tests with one skip and one deselection; all 20 duplicated
  Windows harness, baseline, portability, dependency, analysis, and CodeQL
  checks passed. No client was launched.
- `emulebb/emulebb-build-tests#65` moved recurring action scheduling from a
  process-local monotonic deadline to the persisted v5 UTC authority. Startup
  initializes a missing deadline once, preserves an existing deadline exactly,
  services due or pending work, reconciles the report-commit crash gap with the
  normal interval, replaces the deadline after action completion, and clears it
  when disabled or cycle-limited. Monotonic time remains limited to readiness,
  polling, and checkpoint cadence. Local validation passed 2,649 Python tests
  with one skip and one deselection; all 20 duplicated Windows harness,
  baseline, portability, dependency, analysis, and CodeQL checks passed. No
  client was launched.
- `emulebb/emulebb-build-tests#66` added one bounded search-result snapshot
  read with no driver-side wait or sleep, plus a typed one-shot result phase
  that preserves incomplete rows and exact local REST failures. The existing
  blocking result poll now composes this primitive, retaining its last nonempty
  rows at timeout while providing the foundation for a single-writer
  incremental observer state machine. Local validation passed 2,654 Python
  tests with one skip and one deselection; all 20 duplicated Windows harness,
  baseline, portability, dependency, analysis, and CodeQL checks passed. No
  client was launched.
- `emulebb/emulebb-build-tests#67` advanced the sole current observer-state
  contract to v6 and made result polling restart-safe and incremental. Each
  client persists one authoritative UTC poll schedule, attempt/error history,
  latest count, and exact errors; the observer services at most one bounded GET
  per loop, uses the exact remaining deadline as its request budget, and treats
  a response finishing after that deadline as incomplete. Terminal provenance
  survives pending-state cleanup in the immutable driver outcome, direct
  terminal-result bypasses and impossible success histories are rejected, and
  checkpoint/stop/health work can run between result attempts. Local validation
  passed 2,666 Python tests with one skip and one deselection; all 20 duplicated
  Windows harness, baseline, portability, dependency, analysis, and CodeQL
  checks passed. No client was launched.
- `emulebb/emulebb-build-tests#68` replaced the stale offline summary with the
  sole current `emulebb-build-tests.converged-soak-report.v2` contract. It embeds
  exact validated v6 cumulative state, validates current retained action and
  checkpoint suffixes against their count, byte, latest-file, campaign,
  sequence, and UTC authorities, reports whole-artifact rotation as
  `omittedByRetention`, preserves exact unredacted per-client poll provenance,
  and retries boundedly across concurrent state changes before failing closed
  on a stable integrity mismatch. Local validation passed 2,671 Python tests
  with one skip and one deselection; all 20 duplicated Windows harness,
  baseline, portability, dependency, analysis, and CodeQL checks passed. No
  client was launched.
- `emulebb/emulebb-build-tests#69` advanced the sole current persisted-session
  status contract to `emulebb.persisted-soak-status.v2` and exposes the exact
  bounded v2 cumulative-plus-retained observer report through the canonical
  `persisted-soak-control.py status` entrypoint. Status permits normal startup
  before observer state exists, but once present requires the canonical session
  campaign directory and matching campaign identity; retained-window or report
  integrity failures propagate unchanged, so the unattended watcher treats them
  as terminal health loss and stops the campaign fail-closed. Local validation
  passed 2,674 Python tests with one skip and one deselection; all 20 duplicated
  Windows harness, baseline, portability, dependency, analysis, and CodeQL
  checks passed. No client was launched.
- `emulebb/emulebb-build-tests#70` merged two granular commits. It advanced the
  sole current storage policy to v8, reserved process-metric sample and summary
  streams, replaced the unbounded in-memory CSV rewrite with complete-record
  rotating JSONL, and maintains one atomic O(1)-memory cumulative summary.
  Oversized records and summaries fail closed. Local validation passed 2,678
  Python tests with one skip and one deselection; all 20 duplicated Windows
  harness, baseline, portability, dependency, analysis, and CodeQL checks
  passed. No client was launched and no VPN state was changed.
- `emulebb/emulebb-build-tests#71` resolved the P0 campaign-storage ownership
  mismatch. The launcher now constructs every bounded store through one
  campaign-only authority rooted at `soak/campaigns/`. A real pressure test
  prunes obsolete campaign evidence while proving `control/`, `last-run/`,
  `transactions/`, and generated `mfc-profile/` files retain their exact bytes.
  Local validation passed 2,678 Python tests with one skip and one deselection;
  all 20 duplicated Windows harness, baseline, portability, dependency,
  analysis, and CodeQL checks passed. No client was launched and no VPN state
  was changed.
- `emulebb/emulebb-build-tests#72` advanced the sole current storage policy to
  v9 and bounded preflight Rust and MFC outputs plus their singleton recovery
  manifest. Preflight now inventories stable exact files, reserves aggregate
  capacity before mutation, atomically copies and hash-verifies every
  destination, persists `prepared`/`copied`/`complete` transaction state, and
  removes sources only after all destinations verify. Interrupted copy and
  partial-removal retries converge without duplicate names; unsafe names,
  unexpected artifacts, source mutation, stream overflow, and Windows reparse
  escapes fail closed. Mutable checkpoints distinguish final durable growth
  from temporary atomic-write space, so replacement succeeds at an exact legal
  aggregate bound. Local validation passed 2,689 Python tests with one skip and
  one deselection; all 20 duplicated Windows harness, baseline, portability,
  dependency, analysis, and CodeQL checks passed. No client was launched and no
  VPN state was changed.
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
- The ignored operator input was subsequently migrated backup-first to
  storage-policy v8 with an 8 MiB by eight-file process-metric JSONL ring and a
  1 MiB singleton cumulative summary. The typed repository loader accepted the
  required v8 streams. No client was launched.
- The ignored operator input was subsequently migrated backup-first to
  storage-policy v9 with a 1 MiB singleton preflight transaction manifest, a
  64 MiB singleton Rust-output archive, and a 64 MiB by sixteen-file MFC-output
  archive. The typed repository loader accepted the required v9 streams. No
  client was launched.
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
  enabling it in the recurring observer loop. Build-tests #62 reconciles exact
  final and prepared report-first crashes before diagnostic recapture, and
  build-tests #63 activates immediate pending-action service and report
  finalization in the recurring loop. Build-tests #64 provides the strict v5 UTC
  deadline authority and atomic reservation consumption, and build-tests #65
  reconciles and services that authority in the recurring loop without relying
  on process-local action timing.
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

## Storage Audit - 2026-10-26

- Resolved by build-tests #71: every launcher, controller, and observer bounded
  store now uses the exact `soak/campaigns/` deletion authority. Pressure
  coverage prunes obsolete campaign evidence while proving `control/`,
  `last-run/`, `transactions/`, and generated `mfc-profile/` files are never
  inventory or deletion candidates. Arbitrarily long public soaks remain
  unauthorized because the remaining audited non-stream outputs are not yet
  fully bounded.
- Process-metric samples and their cumulative summary are bounded and reserved
  by build-tests #70. Preflight archives and their recoverable transaction
  manifest are bounded by build-tests #72. The remaining campaign writers
  requiring explicit bounds are CPU profiling outputs, last-run and control
  records, external-profile growth, exact MFC diagnostic policy, and MFC
  non-diagnostic logs, performance artifacts, and crash dumps.
- The next safety order is: add fail-closed external-profile growth guards
  without deleting operator state; pin exact MFC diagnostics policy; reserve
  CPU-profile streams; bound control records; bound first-import staging; then
  constrain MFC non-diagnostic artifacts.

## Harness Implementation Checkpoint - 2026-10-26

- Work remains isolated on `feature/persisted-protocol-parity-soak` in
  `emulebb-rust`, `emulebb-build-tests`, `emulebb-tooling`, and the MFC
  workspace. Every coherent slice is committed and pushed; no implementation
  pull request is open.
- Rust diagnostics now correlate Kad RPC lifecycles and lookup completions,
  carry peer/file join keys on peer TCP, and record every supported peer TCP
  packet rather than sampling bulk opcodes.
- MFC diagnostics now emit aligned server TCP/UDP `diag_event_v2` records,
  record every peer TCP packet, report truthful plaintext versus obfuscated
  transport, preserve the complete clear frame, and carry matching peer/file
  join keys.
- Harness analysis now requires bilateral Kad evidence, server-UDP parity, and
  peer TCP join-key coverage. Packet parsing requires the full clear frame and
  accepts absent raw wire bytes only for an explicitly obfuscated transport.
- Live indexing scans the real Rust `packet-dump/` and MFC `logs/` directories.
  The v2 diagnostic checkpoint retains complete closed-segment aggregates and
  join-key presence across rotation. Stop finalization runs only after both
  clients and the watcher exit, consumes the former active segment, rejects a
  missing retained suffix, and is retry-idempotent after partial persistence.
- Build-tests validation is green at `2708 passed, 1 skipped, 1 deselected`.
  The focused scanner/index/controller suite is green at `104 passed`, and all
  packet-contract consumers are green at `426 passed`.
- Rust validation at the current branch head is green for formatting, strict
  clippy, and `1192` packet-diagnostics tests. MFC validation at the current
  branch head is green for Debug x64, Release x64, and diagnostics Release x64.
- The real persisted-soak preflight is green with loopback REST, hide.me full
  tunnel, split tunneling disabled, VPN Guard Block, exact diagnostics binaries,
  and the requested MFC/Rust profile paths.
- Campaign `20261026T171120Z` exposed a Windows first-import promotion failure:
  Python committed SQLite transactions without deterministically closing the
  handles. Build-tests commit `7b22c35` closes every metadata connection before
  atomic profile promotion.
- Campaign `20261026T171510Z` proved profile promotion but exposed two later
  startup defects. The observer required the Rust diagnostic directory before
  the launcher could create it, and the imported database omitted current Rust
  transfer invariants.
- Backtrace campaign `20261026T171904Z` localized the Rust abort to
  `manifest_from_row`: imported transfers lacked mandatory
  `transfer_name_state` rows. Build-tests commit `eb8675a` now seeds the current
  profile singleton and transfer-name state, validates those invariants without
  repair or compatibility fallback, and rejects any invalid nonempty profile.
  Commit `08bd3ae` moves diagnostic-directory existence into the observer's
  bounded readiness loop so first-time import cannot race observer startup.
- Campaign `20261026T174343Z` proved both fixes: clean import completed, the
  observer survived the absent-first-diagnostic-directory interval, and Rust
  remained alive. Rust still missed the REST readiness deadline because the
  importer had incorrectly left all `1798` share-in-place files visible in the
  transfer list, forcing synchronous full-manifest hydration before REST bind.
  Build-tests commit `6bcbb8f` now persists imported share-in-place rows as
  removed from the transfer list, matching native Rust local ingest while
  retaining them in the progressively hydrated shared catalog. The focused
  metadata/import suite is green at `60 passed`.
- Campaign `20261026T180304Z` then exposed a native MFC REST contract defect:
  JSON responses omitted the required `X-Contract-Version: 2.0.0` header.
  MFC commit `cfa03345` now emits the header from the common native JSON
  success/error response boundary. Debug x64, Release x64, and diagnostics
  Release x64 are green with zero warnings.
- Campaign `20261026T181317Z` reused the corrected persisted Rust profile and
  proved Rust high-ID eD2K plus Kad v2 packet/RPC activity, MFC high-ID server
  connectivity, MFC diagnostics readiness, and the corrected MFC REST
  contract. The mandatory Rust ready bundle then timed out three times because
  persisted shared-catalog hydration synchronously reparsed uncached media with
  Symphonia across the imported library, starving REST-critical work.
- Rust commit `366a67c3` makes persisted catalog hydration database-only,
  accepts only current-version cached media, leaves stale cache rows untouched,
  and keeps bulk imported promotion cached-only while preserving eager media
  extraction for newly ingested files. Validation is green for formatting,
  all `1184` eD2K tests, all `435` core tests, the imported-promotion
  regression, and the Release x64 diagnostics build with zero warnings.
- Build-tests commit `b39424a` removed the unused MFC v1 diagnostic adapter and
  its tests. There is no legacy event translation, alias, or fallback in the
  active soak path; focused validation passed `156` tests.
- Campaign `20261026T183806Z` proved prompt Rust startup and bundle capture but
  exposed a redundant MFC Kad-start action after the persisted profile had
  already enabled Kad. Build-tests commit `cd87d85` now applies both network
  enablement preferences before launch and waits for observed Kad state instead
  of issuing a duplicate UI-thread mutation. The full suite passed at
  `2708 passed, 1 skipped, 1 deselected`.
- Campaign `20261026T185023Z` then reached dual-client readiness and isolated
  the next blocker: MFC emitted segmented v2 diagnostics but returned `404` for
  the observer's required `GET /api/v1/diagnostics` writer-health probe.
- MFC commit `fb6b0c34` exposes that route as a direct, writer-lock-safe read,
  emits the exact current 41-field health object from the live writer, reports
  retained inventory and disk headroom, and bounds closed segments by count,
  bytes, and age. Debug x64, Release x64, and diagnostics Release x64 all build
  successfully through the workspace orchestrator.
- Tooling commit `9fb14a0` defines the maintained MFC diagnostics response and
  exact writer-health schema. Build-tests commit `fa46889` makes the native
  route inventory and direct-dispatch boundary enforce that contract; focused
  route, schema, writer, and observer validation passed `65` tests.
- Campaign `20261026T190612Z` reused the unchanged persisted Rust profile and
  was the first until-stopped run to reach strict dual-writer enforcement. MFC
  and Rust each reported current `diag_event_v2` process/run/segment identity,
  zero drops and errors, satisfied storage policy, hide.me binding, and VPN
  Guard Block across four observer checkpoints. One transient Rust REST timeout
  cleared on the next watcher sample. The final analyzer read `11,355` Rust and
  `10,645` MFC records. MFC continuously reported zero download sources, which
  explains the absent MFC client-UDP family without weakening that evidence
  gate.
- Build-tests commits `d68ae82` and `c2f1dff` make analyzers snapshot the exact
  opened prefix of an append-only active segment and compare Windows path and
  handle metadata portably. Focused run/index/analyzer validation passed `62`
  tests. The first stop exposed the cross-API timestamp defect; a retry with the
  fix finalized and pinned both former active segments with full run-start
  coverage and no writer-health violation.
- Live traces exposed known opcodes mislabeled as `UNKNOWN`: Kad1 routing
  request `0x20` in Rust and eD2K server-description request/response
  `0xA2`/`0xA3` in MFC. Rust commit `52397089` names the known deprecated Kad1
  routing request/response while leaving those packets behaviorally unsupported.
  MFC commit `6252f525` names the same known legacy Kad set plus server UDP
  descriptions. Build-tests commit `f383dce` guards the cross-client source
  contract. Both Rust Kad crates pass, and MFC Debug x64, Release x64, and
  diagnostics Release x64 builds are green.
- Campaign `20261026T193217Z` proved the rebuilt Rust trace names deprecated
  Kad routing opcode `0x20`, then exposed an uncaught diagnostic-health timeout
  before its first synchronized action. Build-tests commit `9644065` records
  that timeout as a connectivity skip, keeps the observer alive, and preserves
  repeated watcher failure as the fail-closed authority. Focused observer and
  controller validation passed `138` tests.
- Campaign `20261026T193907Z` then exposed one duplicated REST version prefix
  in the action driver. Build-tests commit `fdf7eed` defines exactly one
  canonical `/api/v1` client root and resource-relative action paths, with no
  fallback or compatibility alias. Focused validation passed `228` tests; the
  campaign finalized `4,599` MFC and `6,194` Rust records with full run-start
  coverage and no writer-health violation.
- Campaign `20261026T195054Z` proved synchronized server-search creation and
  result completion on both clients. It also drove MFC through twelve segment
  rotations within minutes, proving the watcher incorrectly treated reduced
  current growth inside a healthy rolling retention ring as a terminal fault.
  Build-tests commit `8e21761` now validates the active-segment, retained-count,
  retained-byte, and free-space bounds without requiring a whole fresh segment
  of instantaneous headroom; `160` focused tests pass.
- The exact finalized trace diff was unbounded and emitted megabyte-scale
  repeated mismatch evidence. Build-tests commit `de4808e` replaces that
  contract with only `diag_event_diff_v2`: exact totals plus at most `32`
  representative local details per category. The same finalized trace pair now
  produces a bounded `99,986`-byte report; `123` focused tests pass.
- Campaign `20261026T200004Z` stopped before launching either client because a
  rotated legacy MFC packet-text log exceeded the preflight artifact limit by
  one bounded log line. The common `diag_event_v2` segments already carry the
  canonical full packet evidence. MFC commit `3becf005` removes that duplicate
  producer and moves its remaining invalid-sub-opcode detail into full,
  unredacted `diag_event_v2` records. Build-tests commit `488e214` forbids the
  retired writer and schemas. The complete source-parity suite passes `194`
  tests, and MFC Debug x64, Release x64, and diagnostics Release x64 builds are
  green.
- Build-tests commit `2bb88c5` lets canonical stop finalize a campaign that
  failed before either diagnostic writer started, while still requiring exact
  finalization once writer health becomes authoritative. Commit `cdb566b`
  admits only the MFC logger's exact 64-KiB maximum line overshoot during
  preflight archival. The combined controller and input-policy suites pass
  `96` tests.
- Campaign `20261026T201442Z` archived the three existing legacy packet-text
  files once and proved the rebuilt MFC client creates no replacement. Both v2
  writers, REST APIs, hide.me bindings, VPN Guard Block, watcher, observer, and
  storage stayed healthy. Canonical stop finalized fifteen MFC segments and
  retained bounded evidence pins. Its first synchronized zero-result search
  exposed one harness false negative: the classifier unconditionally required
  `OP_SEARCHRESULT` even when both clients authoritatively completed with zero
  results.
- Build-tests commit `f67de86` makes server-search result traffic optional only
  when both driver result counts are exactly zero; the shared
  `OP_SEARCHREQUEST` remains mandatory. Adjacent action, report, summary, and
  observer-state validation passes `123` tests.
- Campaign `20261026T202726Z` proved the corrected zero-result classifier, then
  stopped cleanly so the observer could load the canonical packet-projection
  contract. Both former active v2 segments finalized from run start with no
  writer-health violation; the retained Rust segment was pinned by policy.
- Build-tests commit `68cee4a` gives the derived eD2K TCP packet view the exact
  `ed2k_tcp_packet_view_v2` schema and its bounded comparison report the exact
  `ed2k_packet_diff_v2` schema. The action slicer accepts only that view or the
  canonical `diag_event_v2` envelope; the retired packet schema and schema-less
  fallback remain unsupported. Focused diagnostic, action, offline, observer,
  and controller validation passes `263` tests. The complete fast suite passes
  `2,722` tests with one skip and two unrelated existing failures: the Rust REST
  route inventory contains `/api/v1/events` beyond the current MFC/golden
  contract, and the release golden still expects `90` routes while the current
  inventory has `91`.
- Campaign `20261026T204411Z` was the first indefinite run using the unchanged
  persisted profiles and committed observer. Both clients, v2 writers, watcher,
  observer, hide.me full tunnel, VPN Guard Block, and bounded storage were
  healthy with no findings. Its first synchronized server search completed on
  both clients with zero poll errors and zero results. The action report records
  `coverage-parity`, bilateral mandatory `OP_SEARCHREQUEST`, optional absent
  `OP_SEARCHRESULT`, conformant diagnostics, and packet report schema
  `ed2k_packet_diff_v2`.
- Campaign `20261026T211001Z` produced server coverage parity and the first
  synchronized nonzero Kad comparison. A transient observer-summary read raced
  one atomic state replacement and caused a false watchdog stop; build-tests
  commit `0d6f6f9` makes those read races retryable without weakening terminal
  evidence failures.
- Rust commit `14dfa6a5` and MFC commit `36771381` emit one correlated
  `lookup_started` and `lookup_complete` record per REST-created Kad keyword
  search. Build-tests commit `acb5d0c` requires exact per-client search IDs,
  terminal counts, directional `KADEMLIA2_SEARCH_KEY_REQ`/`SEARCH_RES` packets,
  and both lifecycle milestones; packet-only fallback is not supported.
- Campaign `20261026T214153Z` proved the rebuilt lifecycle clients and strict
  server action gate before the operator shut down the host. On resume, canonical
  stop finalized both run-start diagnostic indexes with no writer-health gap;
  the missing Kad cycle was an operator interruption, not a product failure.
- Build-tests commit `9feeb19` gates each action before reservation: server and
  global searches require both `ed2kConnected`, while Kad requires both
  `kadConnected`. A disconnected network records an exact readiness skip and
  cannot issue either search POST.
- Cold campaign `20261027T100112Z` proved that the persisted MFC profile can
  spend more than sixty seconds loading its 53,900 known shared files before
  REST readiness. Build-tests commit `ed09ac8` centralizes the dual-client REST
  startup ceiling at 300 seconds for both direct and persisted launchers; the
  ceiling returns immediately when each client is ready.
- Campaign `20261027T100510Z` produced server coverage parity and a synchronized
  Kad action whose REST pages each returned 100 rows. Exact lifecycle records
  reported the uncapped totals instead: Rust `338`, MFC `331`. This exposed a
  harness semantic defect, not absent lifecycle evidence: the driver discarded
  the shared REST `total` and compared `lookup_complete.resultCount` with page
  length. Build-tests commit `579ec1b` removes the ambiguous `resultCounts`
  shape, records `returnedCounts` separately from authoritative `resultTotals`,
  advances observer state to exact schema v7, and correlates Kad completion only
  with each client's total. No v6 state adapter or field fallback exists.
- Campaign `20261027T103720Z` stayed healthy at the process, REST, writer,
  watcher, observer, hide.me full-tunnel, VPN Guard Block, and bounded-storage
  layers with zero diagnostic drops. MFC Kad and Rust Kad remained active, but
  MFC eD2K stayed disconnected after sending one server login request with no
  reply. Canonical stop finalized both diagnostic indexes and retained the
  pre-stop packet-coverage report. The previous diagnostics exposed packets but
  not the exact server-connection failure transition, so the evidence could not
  distinguish timeout, close, or native connection rejection.
- Build-tests commit `dd47083` aligns the canonical Rust diagnostics route with
  the current REST inventory and release golden. Commit `87afc2c` advances the
  observer to exact schema v8 and separates scheduling position from completed
  action cycles, so a disconnected server readiness skip advances to Kad rather
  than starving every later method. The complete harness suite passed `2,738`
  tests with one skip and one deselection after the scheduler change.
- MFC commit `0a7d7fac` and Rust commit `5965b0c2` now emit the same strict
  `ed2k_tcp/connection_state` lifecycle: attempt start, transport connection,
  login acceptance, native failure or timeout, and close, correlated by
  positive attempt ID and exact server endpoint. Diagnostics Release MFC and
  diagnostics Rust builds are green; the Rust eD2K unit suite passed `1,185`
  tests.
- Build-tests commit `c8da227` makes bilateral server-connection lifecycle
  evidence mandatory for a complete run, validates exact keys, bodies,
  transitions, state continuity, severities, and transport mode, and exposes
  bounded attempt, event, outcome, and violation summaries in packet coverage,
  cross-client, and offline-soak reports. The complete harness suite passed
  `2,741` tests with one skip and one deselection.
- Campaign `20261027T112504Z` proved the new lifecycle contract on live data:
  Rust recorded two attempts and seven transitions, MFC one attempt and three
  transitions, with zero lifecycle violations. Its first synchronized server
  action reached `coverage-parity` with zero result-poll errors and zero writer
  drops. An operator analysis output was then written into the observer-owned
  `report` root; the strict bounded store rejected the foreign artifact and the
  observer stopped rather than accepting an ambiguous retained window.
  Canonical teardown was clean and finalized both diagnostic indexes, but the
  observer summary correctly remains invalid because repeated checkpoint
  attempts had already made its retained counts inconsistent.
- Build-tests commit `9819232` rejects analyzer JSON output in an
  observer-owned report root, directs analysis to the campaign sibling
  directory, advances persisted status to exact schema v3, and reports bounded
  `observerReportError` evidence plus a terminal `observer-report-invalid`
  finding instead of crashing status or post-stop rendering. The complete
  harness suite passed `2,743` tests with one skip and one deselection.
- Campaign `20261027T114408Z` is the current clean indefinite v8 run. Both
  clients, REST APIs, v2 writers, observer, watcher, hide.me full tunnel, VPN
  Guard Block, and bounded storage are healthy. Its first server action reached
  `coverage-parity` with zero errors or writer drops. Live analysis written to
  the safe campaign `analysis` directory leaves observer state valid and proves
  the bilateral server lifecycle gate with zero violations.
- Build-tests commit `c7f8323` updates shared-file inspection to the current
  Rust keyset-cursor API while keeping the MFC offset contract explicit, and
  changes the hash-settled proof to poll lightweight runtime counters rather
  than repeatedly counting the full catalog. Live evidence shows MFC hashing
  complete with zero active files. Rust reused `52,431` persisted entries and
  is completing `10,610` new or changed entries with zero hash or stat failures;
  the canonical long waiter is active before the restart-reuse proof.
- Build-tests commit `ddf9824` adds the explicit persisted-profile
  `reload-shared-directories` operation so an interrupted one-time
  reconciliation can be resumed without rewriting roots or profiles. MFC
  commit `d201cf4c` raises its diagnostic writer from eight retained segments
  and `512 MiB` to the same 128-segment, `8 GiB`, seven-day window used by
  Rust. The previous strict index failure was real evidence loss caused by the
  shorter writer window; the gap detector remains strict. Rebuilt MFC reports
  the new limits live with zero retention deletions. Campaign
  `20261027T123202Z` is reconciling `9,115` Rust entries while reusing `53,926`,
  with zero hash or stat failures. The complete harness suite passed `2,745`
  tests with one skip and one deselection before the explicit reload command;
  its focused suite passes `93` tests afterward.
- The maintained MFC profile and valid Rust persisted profile continue to be
  reused in place. Explicit stopped-profile hash refresh is backup-first and
  may update current hashsets and native fingerprints in place; profile reset,
  compatibility conversion, and automatic startup reimport remain forbidden.
- Campaign `20261027T131236Z` proved MFC hashing settled at `53,900` shared
  files with zero active hashing. Rust completed a `9,115`-entry pass, then
  immediately queued `4,939` unchanged whole-second files again. The exact
  defect was the Windows fingerprint policy: runtime fingerprints lacked the
  filesystem ChangeTime and the reuse gate inferred safety from nonzero
  subsecond values, permanently rejecting valid whole-second timestamps.
- Build-tests commit `e234ed2` added a clean-stop, finalized-diagnostics hash
  backup operation. The stopped campaign produced a verified backup containing
  MFC `known.met`, `known2_64.met`, and a consistent Rust SQLite snapshot with
  `58,221` known files before any repair write.
- Build-tests commits `771ef53`, `87cbfbe`, and `7b5bde6` make the canonical
  profile importer write Rust-compatible Windows ChangeTime fingerprints, add
  an explicit idempotent persisted-profile hash upsert that preserves Rust
  runtime counters and UI state, and seal existing Rust-only hashes only when
  persisted identity, size, and modified time still match exactly. The live
  refresh matched `51,565` MFC records across `51,644` source paths and safely
  upgraded another `15,562` Rust-only fingerprints. All `67,206` persisted
  shared-source fingerprints are current, with zero mismatches, missing
  fingerprints, unavailable files, or invalid encodings.
- Rust commit `41c49f43` reads Windows LastWriteTime and ChangeTime from the
  same open handle and makes Windows reuse depend on exact identity, size,
  modified time, and ChangeTime rather than timestamp precision inference.
  Package validation passed `67` metadata tests, `1,187` ED2K tests, `436` core
  tests plus core integrations, and a zero-warning Release diagnostics build.
- Campaign `20261027T155645Z` completed the first restart after fingerprint
  repair. Rust scanned `63,065` sources, reused `63,041`, and hashed only `24`
  genuinely new files, with zero changed files, missing fingerprints, stat
  failures, or hash failures. MFC remained settled at `53,900` shared files and
  zero active hashing. Clean teardown finalized both diagnostic indexes, and a
  second verified stopped-profile hash backup captured `58,254` Rust known
  files with a successful SQLite quick check.
- Build-tests commit `f45acbc` advances the strict reload-settlement proof to
  schema v3 and requires the reload to be neither running nor pending, hashing
  to be idle at zero, and failure counters to remain zero across three stable
  samples. It also exposes explicit planned-hash and missing-fingerprint bounds
  rather than accepting an early idle snapshot during startup hydration. The
  complete harness suite passes `2,759` tests with one skip and one deselection.
- Campaign `20261027T160917Z` provided the second strict zero-plan restart:
  Rust scanned and reused all `63,065` sources with zero planned or completed
  hashes and zero missing fingerprints, while MFC again reported `53,900`
  shared files and zero active hashing.
- Rust commit `373b922d` emits one terminal `buddy_request` decision for every
  inbound Kad buddy request, including accepted, local firewall state,
  self-endpoint, existing-buddy, firewall-check collision, and response-send
  failure outcomes. Build-tests commit `08618b6` compares the exact `outcome`
  and `reason` fields instead of accepting presence-only Kad decisions. Rust
  core validation passed `438` unit tests plus the core integration suite.
- Build-tests commits `6437842`, `8fa46b9`, and `0ea5293` make the persisted
  controller carry separate explicit Rust and MFC server endpoints, reconnect
  either disconnected client before an action, retry diagnostic-writer health,
  inspect ordered persisted MFC server candidates through the canonical profile
  importer, and record both endpoints in the run manifest. The complete harness
  suite passed `2,765` tests with one skip and one deselection.
- Campaign `20261027T171323Z` proved a further persisted restart with Rust
  reusing all `63,065` scanned source rows, zero planned or completed hashes,
  zero missing fingerprints, and three stable idle samples. Its unique shared
  catalog contained `58,228` files; MFC remained at `53,900` shared files with
  zero active hashing. A verified post-stop backup retained MFC `known.met`
  (`53,900` entries), `known2_64.met`, and a Rust SQLite snapshot with `58,264`
  known files and a successful quick check.
- The same campaign showed that connected-server search results are
  server-local evidence: Rust and MFC emitted the same clear
  `OP_SEARCHREQUEST`, but only the independently selected MFC server replied.
  A synchronized Kad action independently returned `360` Rust and `341` MFC
  total results, proving both public Kad paths while the observer retained exact
  uncapped totals. The observer then spent minutes copying every interim MFC
  diagnostic-pin candidate even though policy retained only four final files.
- Build-tests commit `d732838` selects the final bounded diagnostic-pin winners
  before file I/O. Its regression proves an over-budget context segment is not
  copied merely to be replaced immediately; focused controller and adjacent
  observer/index validation passed `89` and `110` tests respectively.
- Rust commit `5c25e01c` removes the competing wrapper-level ED2K keyword
  deadline and makes the connected session the sole on-wire timeout authority.
  The typed outcome now distinguishes `Replied` from `TimedOut`, preserves
  completed-search `statusReason=server-timeout`, emits the reason in terminal
  scheduler diagnostics, and records a terminal server-session `timed_out`
  phase while keeping the connection alive. Full ED2K and core unit validation
  passes `1,189` and `438` tests.
- Campaign `20261027T173650Z` was stopped through the canonical persisted
  controller after its Kad cycle exposed a false Rust completion: Rust emitted
  a started and zero-result terminal lookup without a phase-2
  `KADEMLIA2_SEARCH_KEY_REQ`, while MFC dispatched the request and received
  results. Both persisted profiles retained their proven idle hashing state.
- Rust commit `99d6834b` replaces best-effort routing-table admission and silent
  concurrency rejection with awaited routing authority, a concrete search
  permit, and typed start failures across keyword, source, and notes searches.
  The public queue now retries retryable admission failures instead of treating
  a closed stream as a zero-result completion.
- Rust commit `65622ac7` carries an authoritative traversal completion receipt
  through every public Kad search. Diagnostics now record the terminal reason,
  routing seeds, responding contacts, phase-2 attempted and sent counts, raw
  and accepted result counts, and elapsed time. A zero-result terminal is
  successful only after a phase-2 search packet was sent and the traversal
  completed normally. Full validation passed `132` Kad and `438` core unit
  tests, Kad clippy with warnings denied, formatting, and changed-crate checks.
- Build-tests commit `1404969` requires an explicit Rust `outcome=completed`
  before counting `lookup_complete` as Kad lifecycle coverage while preserving
  the current MFC record shape with no outcome field. Focused action and
  offline differential validation passed `100` tests.

## Harness Preflight Checkpoint - 2026-10-30

- Build-tests PR [#80](https://github.com/emulebb/emulebb-build-tests/pull/80)
  merged at `00467b7600288989797703785f10b4a2eab2fdc7`.
- Persisted-soak preflight now proves both loopback REST ports and every Rust
  and MFC TCP/UDP P2P port can bind on the selected full-tunnel interface
  before either client launches. The result retains structured bindability
  evidence in the preflight payload.
- The focused harness matrix passed `155` tests. The complete deterministic
  harness matrix passed `2,788` tests with one platform skip and one deselected
  live lane.
- No live client, VPN, or public-network action was launched. Tunnel-down,
  dual-client, rotation, action-parity, and clean-stop evidence remains open.

## Exact Bundle And Bandwidth Checkpoint - 2026-10-30

- The previous persisted campaign reached teardown but failed because its final
  Rust bundle required `4,325,190` bytes against a `4,194,304`-byte stream
  contract. This was an evidence-finalization defect, not a protocol result.
- Build-tests commit `e308380` replaced the live-wire input contract with one
  canonical v2 schema. It requires one shared upload limit, removes the prior
  schema and Sonarr fallback paths, and applies the same configured value to
  Rust and MFC. The operator-local campaign input now selects `8 KiB/s` so a
  long search-focused soak cannot generate high-rate upload traces.
- Rust commit `54ab0191e9dae2c531b8649e9cec4f757690b052` replaced diagnostic
  bundle v5 with the sole current `emulebb.diagnostic-bundle.v6` contract. The
  request supplies an explicit byte budget, the endpoint serializes the exact
  response once, deterministically removes only duplicated snapshot rows when
  necessary, reports every budget omission, and rejects an oversized mandatory
  core. The segmented `diag_event_v2` stream remains the complete packet and
  semantic evidence authority.
- Build-tests commit `913320f45efc0c6c27931c8f5f7f2ac19ec1e2a4` requests the
  configured stream budget and persists the exact server bytes without JSON
  reserialization. Focused harness validation passed `424` bandwidth-contract
  tests and `197` exact-bundle/storage/controller tests. Rust validation passed
  `140` REST tests, strict Clippy, and formatting.
- No PR is open. The common work-in-progress branch is
  `feature/persisted-soak-parity-gate`; it remains intentionally unmerged until
  the complete live parity slice and clean finalization are green.

## Persisted Profile Smoke Checkpoint - 2026-10-30

- The canonical Rust diagnostics build completed without warnings or failures,
  and the persisted controller preflight proved full-tunnel hide.me routing,
  loopback control, VPN Guard Block, profile validity, selected-port
  bindability, and feasible bounded storage before launch. This lane assumes
  hide.me carries all application traffic; it does not implement or maintain a
  split-tunnel workflow.
- The first rebuilt dual-client campaign reused both persisted profiles and the
  same exact public eD2K server endpoint. Rust reused `51,644` persisted source
  identities, hashed `11,423` genuinely new source identities, and completed
  the `142,596,946,563`-byte plan with zero hash failures. Both clients retained
  the shared `8 KiB/s` upload cap.
- One synchronized server search and one synchronized Kad search completed on
  both clients with action-owned diagnostic coverage parity and zero driver
  errors or connectivity skips. Public result counts were not used as the
  parity authority.
- Graceful controller stop finalized both diagnostic indexes and persisted
  three exact `emulebb.diagnostic-bundle.v6` responses between `600,744` and
  `657,340` bytes against the `4,194,304`-byte budget, with no truncation or
  reported omission.
- The stopped profiles were backed up through the canonical hash-state command.
  Both MFC hash stores were checksummed, and the Rust metadata database passed
  SQLite quick-check before the backup was accepted.
- The next launch proved the restart invariant: the persisted Rust profile
  reached a complete shared catalog with `plannedHashCount=0`,
  `sharedHashingCount=0`, and no new, changed, missing-fingerprint, or failed
  hash entries.
- A focused observer audit found that the existing finite `maxCycles` setting
  counts terminal attempts rather than successful per-method parity cycles.
  The current long-running campaign is useful discovery evidence but is not the
  final four-server plus four-Kad green gate until that contract is replaced by
  success-counted, retry-tolerant, sticky-failure state.
- The Rust eD2k server remains CI and deterministic test infrastructure only.
  This work does not evolve its product scope or use it as the public soak
  target.

## Durable Parity Gate Checkpoint - 2026-10-30

- Build-tests commit `4dd78f32209cc16635a6f8e4fcaadc0bb9341a80`
  aligned deterministic live fixtures with the current required bandwidth,
  search-network, passive-cache-origin, and passive-replay contracts. Commit
  `f4c542530b035a8e32f58188c2be54d2764ed7b6` replaced attempt-counted action
  limits with the durable gate and removed the replaced action-term, method,
  source-profile, and maximum-cycle CLI/configuration shapes without adapters.
- The sole current action report is
  `emulebb-build-tests.observer-action-report.v3`, observer state is
  `emulebb-build-tests.converged-observer-state.v9`, aggregate report is
  `emulebb-build-tests.converged-soak-report.v3`, persisted session is
  `emulebb.persisted-soak-session.v5`, and controller status is
  `emulebb.persisted-soak-status.v4`. The dedicated
  `emulebb.persisted-soak-gate-status.v1` command exits successfully only for a
  green gate.
- The complete deterministic harness matrix passed `2,810` tests with one
  platform skip and one deselected live lane. Focused observer, state, report,
  and controller validation passed `190` tests. No compatibility schema or
  parser is retained.
- Campaign `20261030T193743Z` reused both persisted profiles under full-tunnel
  hide.me and VPN Guard Block, kept the common upload cap at `8 KiB/s`, and
  re-proved the Rust restart invariant with `plannedHashCount=0`,
  `hashedCount=0`, `sharedHashingCount=0`, and a complete shared catalog.
- The campaign reached four successful synchronized eD2K server cycles and four
  successful synchronized Kad cycles with zero retryable outcomes, zero driver
  errors, zero connectivity skips, and zero confirmed divergences. The gate
  command changed from exit `1` while pending to exit `0` when green. A ninth
  post-green server cycle completed successfully, increasing the retained
  server count to five and proving action driving continues after green.
- Canonical graceful stop ended both clients and all three controller
  processes. The final Rust index covered one closed segment and `38,980`
  records; the MFC index covered three closed segments and `48,887` records.
  Both writer histories reported zero violations, with one Rust and three MFC
  evidence pins retained for exact anomaly context.
- Two final Rust `emulebb.diagnostic-bundle.v6` responses were persisted as
  exact server bytes: `560,478` and `664,615` bytes against the
  `4,194,304`-byte limit. Both budgets matched the file byte count exactly and
  reported no truncation.
- The completed slice merged in dependency order as Rust PR
  [#206](https://github.com/emulebb/emulebb-rust/pull/206), build-tests PR
  [#81](https://github.com/emulebb/emulebb-build-tests/pull/81), and tooling PR
  [#132](https://github.com/emulebb/emulebb-tooling/pull/132). All required
  checks passed, each repository returned to synchronized clean `main`, and the
  local and remote `feature/persisted-soak-parity-gate` branches were deleted.

## Extended Parity Soak Checkpoint - 2026-10-30

- Campaign `20261030T215509Z` started from the merged harness through the
  canonical persisted controller after full-tunnel hide.me, VPN Guard Block,
  loopback control, selected P2P port, profile, executable, and bounded-storage
  preflight all passed.
- The controller reused the selected persisted MFC and Rust profiles, selected
  the same exact public eD2K server endpoint for both clients, retained the
  shared `8 KiB/s` upload cap, and launched the observer and watcher detached
  for an until-stopped run.
- MFC completed its expected slower persisted-profile startup. Both client
  processes, REST endpoints, diagnostic writers, Guard Block checks, observer,
  watcher, storage policy, and full-tunnel route checks then reported healthy
  with no findings. Both writers reported zero drops, encoding errors, write
  errors, or storage-policy faults.
- The durable gate reached green at `2026-10-30T22:44:59.000212+00:00` after
  four successful eD2K server cycles and four successful Kad cycles, with zero
  retryable outcomes and zero confirmed divergences. Before the gate completed,
  both diagnostic writers rotated naturally at least once and continued with
  zero dropped events, encoding errors, write errors, or storage-policy faults.
  The campaign continued through five successful cycles per method, then stopped
  through the canonical controller. Both clients, the observer, launcher, and
  watcher were verified stopped, and both diagnostic indexes finalized over
  three closed segments per client after two natural rotations.
- The final observer summary retained all ten action reports and thirteen
  checkpoints with zero retryable outcomes, divergences, connectivity skips,
  driver errors, incomplete-evidence classifications, or storage/writer faults.
  A canonical stopped-profile hash-state backup also completed with the MFC
  known-file state and Rust metadata database passing their integrity checks.
- Full-window packet analysis found one concrete evidence gap rather than a
  search-gate failure: MFC recorded one conformant inbound eD2K client-UDP reask,
  while Rust recorded six undecodable shared-socket datagrams and no conformant
  client-UDP packet or tracked reask attempt. The synchronized driver scheduled
  no downloads, so the run never deliberately exercised Rust source, queue, or
  UDP-reask state. Existing server TCP/UDP, peer TCP, Kad UDP, upload-path, and
  action-owned server/Kad evidence remained present.
- Deprecated Kad1 background opcodes seen only by MFC are not Rust scope and do
  not justify product changes. The next parity proof therefore uses the existing
  sequential solo-capture model with one operator-approved direct transfer,
  identical campaign fixtures, the configured persisted profile for each
  client, and the shared low upload cap. This avoids simultaneous HighID identity
  contention and generates deliberate source/queue/client-UDP evidence.
- Build-tests commits `472ad28` and `5dcbfe7` make that capture fail closed on
  missing persisted-profile authority, apply the live-wire bandwidth limit to
  both clients, remove dynamic public-result fixture selection, and snapshot the
  approved direct transfer once per campaign. Focused tests passed, followed by
  the complete harness suite: `2,817` passed, one skipped, one deselected.

## Next Implementation

- Treat request encoding, parser behavior, lifecycle decisions, timeout cause,
  packet correlation, and connection continuity as parity authority. Public
  result counts may differ and are comparable only when both clients used the
  same exact server endpoint.
- Run a serial or endpoint-swapped live A/B before treating a missing
  `OP_SEARCHRESULT` as a Rust protocol defect. Connected-server result counts
  from different public endpoints are not a valid parity assertion; request
  encoding, parser behavior, timeout cause, and connection continuity are.
- Preserve MFC zero hashing and the Rust zero-plan restart invariant while
  protocol parity work continues. Any future nonzero plan must identify
  genuinely changed or new files rather than another compatibility workaround.
- Run the approved direct-transfer action sequentially against Rust and MFC on
  their configured persisted profiles. Hold each client long enough for source,
  queue, and UDP-reask behavior, retain exact unredacted action windows, and then
  compare the paired recordings offline by deterministic action identifier.
- Keep the proven server/Kad search gate unchanged. Treat the sequential transfer
  capture as a separate protocol-coverage proof; do not weaken required-family
  or diagnostic-conformance gates when an action did not generate the family.
- Confirm the rebuilt traces name deprecated Kad routing and server-description
  UDP opcodes on both clients without changing unsupported Kad1 behavior.
- Run the complete diagnostic analyzer and offline action diff after both solo
  recordings exist. Implement only concrete protocol or correlation gaps
  demonstrated by exact traces, each as a separate tested commit.
- Keep the next run until-stopped once the action-driven proof is clean. Do not
  open a pull request until the complete significant slice is green and the
  operator explicitly requests it. This slice makes no VPN-safety claim until a
  separate controlled tunnel-down proof is completed.

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
- `diag_event_v2` is the only common event envelope for both Rust and MFC.
  Current harness code rejects every other diagnostic schema; there is no
  legacy input adapter or fallback path.
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
- [x] Preflight fails before launch unless hide.me is active, split tunneling is
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

- Further implementation stays as granular commits on one topic branch per
  participating repository for the active workstream.
  Open one PR per repo only after the whole significant slice is complete and
  fully green; do not create parallel WIP branches or per-commit PRs.
- Update this checklist as each coherent slice lands; keep transient run logs
  out of this item and retain only stable conclusions or evidence references.
