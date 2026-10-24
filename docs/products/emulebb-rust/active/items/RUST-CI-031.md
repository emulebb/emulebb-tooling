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
- Detached controller/status/watch behavior still needs to be unified around
  this dual-client workflow; the existing detached wrapper remains Rust-only.
- Packet and semantic diagnostics cover substantial protocol surface, but they
  lack a common run/session/action correlation envelope, complete unified
  server and client-UDP events, bounded rotation, and strict missing-family or
  sequence-gap gates.
- The diagnostic dump endpoint captures only a small status document and does
  not yet produce a complete bounded protocol-investigation bundle.

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
- No public live client was launched for these foundation slices; guarded live
  and tunnel-down acceptance evidence remains outstanding.

## Why This Matters

Long-running public-network observation is needed to expose rare eD2K and Kad
state-machine behavior, but an unbounded run magnifies routing, profile
mutation, privacy, disk-growth, and false-parity risks. A supported workflow
must fail closed before launch, preserve operator state, bound its evidence,
and distinguish observed parity from merely unobserved behavior.

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
- Produce a bounded, redacted diagnostic bundle containing the full REST
  snapshot, settings provenance, network/guard state, counters, recent errors,
  and packet/event tails.
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
- [ ] The canonical dual-client workflow supports detached until-stopped runs,
      self-describing status, periodic health checks, and graceful teardown.
- [ ] Packet/event evidence rotates within configured byte and age budgets and
      reports record, parse, sequence, and dropped-event gaps.
- [ ] Required eD2K and Kad diagnostic families carry enough stable correlation
      to reconstruct causal sessions and harness actions without exposing live
      private data.
- [ ] The diagnostic dump API produces a bounded, redacted investigation bundle
      rather than a status-only placeholder.
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
  detection, redaction, and strict comparison outcomes.
- Deterministic local eD2K/Kad fixtures and protocol goldens.
- Explicit operator-approved public validation with tunnel-down blocking,
  guarded dual startup, loopback control, clean stop, recovered stop, and
  retained sanitized evidence.

## Notes

- Implementation should land as granular, independently validated pull
  requests in `emulebb-tooling`, `emulebb-build-tests`, and `emulebb-rust`.
- Update this checklist as each coherent slice lands; keep transient run logs
  out of this item and retain only stable conclusions or evidence references.
