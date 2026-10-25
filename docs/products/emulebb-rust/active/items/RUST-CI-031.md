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
- The Rust diagnostic dump endpoint now produces a versioned, bounded local
  investigation bundle with status, runtime diagnostics, settings provenance,
  recent logs, and exact records plus integrity summaries from the unified
  `diag_event_v2` stream only. Bundle v3 deliberately excludes legacy side-file
  dumps. Its evidence is intentionally unredacted for this local,
  non-published test lane.
- Rust and MFC use one process-wide retained-event sequence,
  family-local stream sequences, rotate-before-write segments, persisted-run
  retention, and observable writer/drop/error health.
- Every active Rust protocol family now emits through the bounded unified
  stream. The peer-TCP, client-UDP, server TCP/UDP, and Kad-UDP legacy packet
  side-file writers are retired, and active harness consumers select exact
  `diag_event_v2` runs rather than discovering those files. Diagnostic bundle
  snapshots still accumulate without directory retention.
  Rust and MFC eD2K client UDP record exact wire bytes, receive dispositions,
  and correlated socket-boundary send attempts and terminal outcomes in the
  same `diag_event_v2` family. The harness compares exact packet bytes, audits
  each side's lifecycle independently, and requires the family across complete
  captures while keeping narrow action windows sampling-tolerant.
  Rust server TCP and UDP diagnostics now preserve trace/state context and emit
  correlated socket-boundary send attempts plus exactly one success, failure,
  or cancellation terminal outcome. The Rust `ed2k_server_udp` family still
  lacks an aligned MFC comparator and is not yet cross-client parity evidence.
  Arbitrary-length authorization remains blocked until controller output,
  `daemon.out`, campaign archives, repeated bundle persistence, and aggregate
  disk reserve are bounded, then guarded live validation proves the complete
  path.

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
- `emulebb/emulebb-tooling#59` through `#62` aligned the common-v2 product
  contract, segmented filenames and writer-health evidence, and the explicit
  local-only unredacted trace policy.
- The operator-reported concurrent IP-filter work was reconciled after its
  compilation completed: the Rust checkout and only registered worktree were
  clean at `95f14c80`, and no local or remote IP-filter topic branch or
  uncommitted delta was available to include. The existing exact-source
  IP-filter SHA-256 diagnostics from Rust #171 remain present; any later
  materialized IP-filter delta must be reviewed and landed as its own granular
  Rust slice.
- No public live client was launched for these foundation slices; guarded live
  and tunnel-down acceptance evidence remains outstanding.

## Storage Audit - 2026-10-24

- The unified Rust event ring is bounded by segment size, rotation age, and
  retained segment count, but it has no aggregate-byte, retained-age, or
  minimum-free-space authority. The active segment is allowed to exceed its
  target for one exact oversized record, which is correct for evidence
  integrity but must be included in reserve calculations.
- The persisted soak watcher rotates its JSONL history, but detached launcher
  and watcher stdout/stderr append forever. The watcher also prints every
  sample to its unbounded stdout log, duplicating the bounded JSONL stream.
- Rust `daemon.out` appends for the complete lifetime of one persisted run and
  is only evacuated before a later launch. Rust daily application-log rotation
  bounds file count but not bytes generated within one day.
- Every new campaign creates timestamped archive and report trees with no byte,
  age, campaign-count, or free-space policy. Moving profile evidence to the
  output volume can require a cross-volume copy without destination-space
  preflight, and evacuating every retained segment defeats cross-run writer
  retention by preserving successive copies forever.
- Each diagnostic bundle is individually bounded, but every confirmed request
  persists a unique UUID-named file under the Rust profile and no retention
  policy removes old bundles. The persisted soak currently captures no bundles;
  adding periodic capture before storage ownership changes would create a new
  unbounded path.
- The persisted preflight and watcher do not enforce free-space reserve or
  observe Rust/MFC writer drop, write-error, or retention-error health. A full
  disk can therefore leave the controller apparently healthy until a secondary
  failure becomes visible.
- The optional converged observer also grows five-minute checkpoints,
  per-action reports, and an all-actions summary indefinitely. Diagnostic
  segments must remain immutable and exact; enabling diagnostic tail trimming
  is not an acceptable storage design.
- Arbitrarily long discovery needs compact all-run family/opcode/outcome and
  integrity indexes plus budget-aware preservation of selected immutable raw
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
- Extend the landed persisted-controller storage enforcement through watch,
  stop, and status. The launch path now proves feasibility without mutation and
  applies and verifies the policy before control-file mutation or process start;
  the remaining lifecycle paths must fail closed on reserve or evidence-
  integrity loss.
- Extend the Rust common writer with aggregate-byte, retained-age, and
  minimum-free-space policy plus observable fault/drop accounting. Keep the
  active segment protected and preserve exact oversized records.
- Transfer diagnostic-bundle persistence ownership to the bounded campaign
  store so repeated endpoint captures do not grow the Rust profile directory.
- Bound detached controller logs and `daemon.out`, then make persisted watcher
  health fail closed on disk pressure and Rust/MFC writer-integrity faults.
- Replace preflight evacuation of every profile segment with hashed,
  identity-preserving promotion of selected closed segments and compact
  manifests under the shared campaign budget.
- Add sparse bundle capture at ready/start, low-cadence periodic checkpoints,
  writer or health faults, and final stop. Do not capture on every 60-second
  health sample.
- Add compact complete-run eD2K/Kad family, opcode, outcome, sequence, and
  writer-health indexes with budget-aware pinning of diagnostically interesting
  exact raw segments.
- Converge the optional observer onto the same bounded store and prove stable
  disk use with deterministic multi-day simulation before any guarded public
  soak is authorized.
- Add aligned MFC and harness coverage for Rust's `ed2k_server_udp` family
  before treating server UDP observations as cross-client parity evidence.
- Protocol and soak traces, bundles, manifests, and diagnostic payloads are
  explicitly local test evidence and will not be published. They must preserve
  exact file, peer, user, hash, endpoint, search, and packet data whenever that
  data helps reconstruct eD2K or Kad behavior. Redaction and privacy-driven
  field omission are not requirements for this lane; completeness is.
- Arbitrarily long public live soaks remain unauthorized while controller logs,
  campaign archives, repeated bundle snapshots, and free-space enforcement are
  unbounded. No live client has been launched during these implementation
  slices.

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
- [x] The diagnostic dump API produces a bounded, exact, unredacted local
      investigation bundle rather than a status-only placeholder.
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
