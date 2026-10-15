---
id: RUST-BUG-119
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/119
title: Harden ED2K server runtime lifecycle ownership
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, ed2k, server, lifecycle, concurrency, cancellation, beta]
product: emulebb-rust
phase: Phase 1
milestone: rust-v0.1.0-beta.3
created: 2026-10-15
source: 2026-10-15 ED2K server lifecycle stabilization audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/119. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-119 - Harden ED2K server runtime lifecycle ownership

## Summary

Make ED2K server planning, connection attempts, reachability, cancellation, and
background metadata work obey one explicit runtime/session ownership model. The
current implementation has individually well-tested components, but several
cross-component lifecycle paths can leave the runtime inert, publish stale
identity, let losing parallel attempts mutate shared session state, or bypass
cleanup when a live plan supersedes an attempt.

This is beta stabilization work. Internal APIs, settings schema, and runtime
ownership boundaries may change where that produces a simpler long-term
design.

## Current State

- With reconnect disabled, an ordinary connection loss returns from the server
  loop permanently while core retains the runtime handle. A later explicit
  connect request updates an orphaned plan channel and appears accepted without
  starting a new attempt.
- Learned public IP and mapped TCP/UDP ports survive server-session loss and
  explicit disconnect. NAT mapping disappearance also leaves the last mapped
  ports published, so later DHT and VPN-guard state can begin from stale
  reachability.
- Safe Server Connect attempts share mutable session identity, callbacks,
  publication state, and responder queues before a winner is chosen. A losing
  attempt can therefore change or clear global state and consume work.
- Superseding a connection plan drops the pinned session future externally,
  bypassing its normal cleanup and obscuring the retryable responder-interrupt
  contract for claimed background work.
- Server-description polling snapshots the startup plan and runs as a detached
  one-shot task. It does not follow later server additions, removals, enables,
  disables, or runtime restarts.

## Why This Matters

These failures cluster around recovery paths rather than the happy path. They
can make the control plane report a running network that cannot reconnect,
carry obsolete network identity into a new session, duplicate or lose shared
library work, and make live server configuration only partially effective.
Those are release-blocking reliability risks for a headless beta client.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server/loop_runtime.rs`
- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs`
- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs`
- `crates/emulebb-ed2k/src/ed2k_server/types.rs`
- `crates/emulebb-ed2k/src/ed2k_server/background.rs`
- `crates/emulebb-ed2k/src/ed2k_server/server_description_poll.rs`
- `crates/emulebb-core/src/network_api.rs`
- `crates/emulebb-core/src/ed2k_net_drivers.rs`
- `crates/emulebb-ed2k/src/reachability.rs`

## Intended Shape

- Keep the server runtime alive as a control-plane owner until explicit runtime
  shutdown. Reconnect policy controls automatic attempts, not whether future
  directed commands can be handled.
- Treat learned public identity and NAT mappings as leases with explicit
  producers and invalidation events. Session loss clears server-learned
  identity; mapping loss clears mapped ports without erasing independent active
  probe evidence.
- Give every connection attempt isolated pre-commit state. Only the selected
  winner may publish identity, run startup side effects, consume shared work,
  or become the active session.
- Make attempt cancellation cooperative and cleanup-complete. Claimed
  responder work must be acknowledged, returned, or classified as a retryable
  interruption before the attempt terminates.
- Make server-description work consume the same live plan generations as
  connection scheduling and bind its lifetime to the runtime owner.

## Scope Constraints

- Preserve stock ED2K wire behavior and current server-selection policy unless
  a separately tracked compatibility decision explicitly changes them.
- Do not solve lifecycle defects with whole-runtime restarts, detached cleanup,
  arbitrary sleeps, or duplicated control channels.
- Do not let an inactive or losing connection attempt mutate externally visible
  network state or drain shared responder queues.
- Keep active-probe evidence independent from server-session and NAT-mapping
  leases so invalidating one producer does not erase stronger current evidence.
- Land and validate each lifecycle slice separately with a granular commit.

## Acceptance Criteria

- [x] Reconnect-disabled runtimes remain commandable, accurately report idle
      state, and honor a later explicit connect without full runtime restart.
- [x] Server-session loss and explicit disconnect invalidate server-learned
      identity; NAT mapping loss invalidates mapped ports; focused tests prove
      stale reachability cannot seed later subsystems.
- [x] Parallel connection attempts isolate mutable pre-commit state and only
      the selected winner can publish identity, startup side effects, callbacks,
      catalog work, or responder consumption.
- [x] Live-plan cancellation completes session cleanup and preserves the
      documented retryable-interruption semantics for claimed background work.
- [x] Server-description polling follows live plan generations, handles server
      mutations, and terminates with the owning runtime.
- [ ] Focused ED2K and core suites pass after every slice, followed by the
      repository's required broader validation before merge.

## Validation

- Rust commit `143cd3f8` keeps serial and parallel reconnect-disabled loops
  alive for explicit plan/reconnect commands. Deterministic tests cover an
  established session drop and exhausted parallel attempts before a later
  directed connection.
- `cargo fmt --all -- --check` passed for `143cd3f8`.
- `python -m emule_workspace test rust-unit --package emulebb-ed2k --config Debug --build-output-mode ErrorsOnly` passed for `143cd3f8`: 1,057 unit tests and 0 doc-test failures.
- Rust commit `4ad0c35b` separates server and fallback public-IP evidence,
  refreshes fallback evidence independently, and makes each NAT snapshot revoke
  mappings that disappeared or became invalid.
- Rust commit `0cbeb48a` invalidates server evidence whenever a serial or
  parallel server session retires, preserves independent fallback/NAT/Kad
  evidence during server-only disconnect, and clears all reachability only
  after full-runtime task cancellation and NAT shutdown.
- `cargo fmt --all -- --check` passed for the reachability lifecycle slice.
- `python -m emule_workspace test rust-unit --package emulebb-ed2k --config Debug --build-output-mode ErrorsOnly` passed for `0cbeb48a`: 1,058 unit tests and 0 doc-test failures.
- `python -m emule_workspace test rust-unit --package emulebb-core --config Debug --build-output-mode ErrorsOnly` passed for `0cbeb48a`: 404 unit tests plus all enabled integration and doc-test suites.
- Rust commit `218d9611` gives parallel server attempts private pre-activation
  state. A deterministic loser-injection test proves that only the selected
  winner publishes login identity and server-list side effects.
- `cargo fmt --all -- --check` passed for `218d9611`.
- `python -m emule_workspace test rust-unit --package emulebb-ed2k --config Debug --build-output-mode ErrorsOnly` passed for `218d9611`: 1,059 unit tests and 0 doc-test failures.
- Rust commit `446e4e35` adds cooperative per-session cancellation and completes
  retryable interruption for claimed responder work before a superseding live
  plan starts its replacement session.
- `cargo fmt --all -- --check` passed for `446e4e35`.
- `python -m emule_workspace test rust-unit --package emulebb-ed2k --config Debug --build-output-mode ErrorsOnly` passed for `446e4e35`: 1,060 unit tests and 0 doc-test failures.
- Rust commit `0c04aa1f` makes server metadata polling consume live plan and
  session generations, discard superseded transaction events, stop promptly on
  plan/session/runtime retirement, and join its task at runtime shutdown.
- `cargo fmt --all -- --check` passed for `0c04aa1f`.
- `python -m emule_workspace test rust-unit --package emulebb-ed2k --config Debug --build-output-mode ErrorsOnly` passed for `0c04aa1f`: 1,061 unit tests and 0 doc-test failures.
- Add focused deterministic tests at each ownership boundary before or with its
  implementation commit.
- Run `python -m emule_workspace test rust-unit --package emulebb-ed2k --config Debug --build-output-mode ErrorsOnly` after ED2K slices.
- Run `python -m emule_workspace test rust-unit --package emulebb-core --config Debug --build-output-mode ErrorsOnly` after core reachability/runtime slices.
- Run repository-required formatting, lint, unit, integration, and policy gates
  before merging the implementation PR.

## Notes

Delivery order is the checklist order: retain the commandable runtime first,
then fix reachability leases, isolate parallel attempts, make cancellation
cooperative, and finally bind metadata polling to live plans. Update this item
after each validated implementation commit so the remote branch remains a
recoverable progress record.
