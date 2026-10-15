---
id: RUST-BUG-121
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/123
title: Make ED2K runtime startup and retirement transactional
status: IN_PROGRESS
priority: Critical
category: bug
labels: [rust, ed2k, lifecycle, concurrency, nat, beta]
product: emulebb-rust
phase: Phase 1
milestone: rust-v0.1.0-beta.3
created: 2026-10-15
source: 2026-10-15 Beta 3 runtime-ownership audit after RUST-BUG-120
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/123. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-121 - Make ED2K runtime startup and retirement transactional

## Summary

Give each ED2K/Kad runtime one explicit ownership transaction from construction
through retirement. A failed start must roll back NAT state and partial runtime
resources, while a successful runtime must own every descendant task and every
shared-state writer until an awaitable retirement barrier completes.

This is Beta 3 stabilization work. Internal APIs and lifecycle structure may
break so disconnect, reconnect, and failed-start outcomes are deterministic.

## Current State

- `EmulebbCore::connect_ed2k_endpoint` starts the NAT manager and publishes its
  mapped ports before several later fallible operations: bind-interface
  resolution, Kad runtime initialization, and eD2K TCP listener binding.
- Those later failures return before an `Ed2kRuntime` is installed. `NatManager`
  has no drop-time cancellation, so its spawned reconcile task, gateway
  mappings, status, and already-published advertised ports can survive a failed
  connect with no runtime handle available to stop them.
- Even explicit `NatManager::stop` aborts its worker without awaiting the join
  handle, so the API does not establish a task-completion barrier before it
  releases mappings and returns.
- `Ed2kRuntime::tasks` owns the top-level server-loop task, but that loop spawns
  a server-description poller and parallel server-session tasks of its own.
  `disconnect_ed2k` aborts the top-level handle directly. Dropping the nested
  `JoinHandle`s detaches those descendants instead of aborting and joining them.
- A selected parallel server attempt retains an activated session token. If its
  parent loop is aborted, the detached selected session can keep processing
  `OP_IDCHANGE` and write server public-IP evidence through the core-lifetime
  `ExternalReachability` after disconnect cleared it or a new runtime started.
- Every runtime generation receives a clone of the same core-lifetime
  `ExternalReachability`, and writes carry no runtime or producer generation.
  Cancellation ordering is therefore the only stale-write defense.
- `disconnect_ed2k_server` sets the server gate, notifies the loop, clears public
  state, and returns without waiting for the selected session to be canceled
  and joined. The retiring session can briefly republish connection state or
  server public-IP evidence after the successful disconnect response.

## Why This Matters

A headless local client must make control-plane lifecycle calls truthful. After
a failed start or successful disconnect, the daemon must not retain hidden NAT
mappings, network activity, stale HighID identity, or a writer capable of
mutating the next session. These races undermine deterministic recovery and can
make REST status disagree with live sockets and advertised wire identity.

## Representative Sites

- `crates/emulebb-core/src/network_api.rs`
- `crates/emulebb-core/src/lib.rs`
- `crates/emulebb-core/src/ed2k_net_drivers.rs`
- `crates/emulebb-ed2k/src/nat.rs`
- `crates/emulebb-ed2k/src/reachability.rs`
- `crates/emulebb-ed2k/src/ed2k_server/loop_runtime.rs`
- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs`

## Intended Shape

- Build the runtime under an explicit candidate owner. Any error before install
  rolls back NAT reconciliation, releases mappings, stops partial tasks, and
  revokes candidate-owned reachability before returning.
- Make NAT shutdown idempotent and completion-aware, with final-owner drop as a
  synchronous cancellation safety net rather than the normal cleanup path.
- Give the installed runtime one root cancellation primitive and one owned task
  scope. Descendant server pollers and connection attempts must be registered
  with that scope or cooperatively drained by their parent; dropping a parent
  future must not detach live child tasks.
- Bind shared-state mutation to generation-scoped writer capabilities. Retiring
  a runtime invalidates its generation before cancellation begins, so a late
  producer completion is a no-op rather than a write into the next runtime.
- Give the selected server session its own retirement boundary. Server-only
  disconnect must invalidate the selected generation, cancel it, and wait for
  publication rights to end before returning success.
- Prefer cooperative cancellation and bounded joins. Use abort only as a final
  fallback after publication rights have already been revoked.

## Scope Constraints

- Preserve stock eD2K/Kad wire behavior and current public-IP/port precedence.
- Do not serialize the data plane behind one global async mutex.
- Do not rely on task timing, sleeps, or `clear_all` ordering as correctness.
- Keep NAT lease-expiry policy, UDP-only remap re-login behavior, STUN evidence
  expiry, and Kad firewall-round coherence in separate follow-up items.
- Do not broaden this item into general task ownership for unrelated indexing,
  library scanning, or transfer-delivery workers.

## Acceptance Criteria

- [ ] A deterministic failure after successful initial NAT reconciliation leaves
      no NAT manager task, gateway mapping, advertised port, or installed runtime.
- [ ] NAT stop does not return before its reconcile worker has terminated, and
      dropping the final manager owner cannot detach a live reconcile loop.
- [ ] Every runtime-owned reachability writer is generation-scoped; writes and
      clears from a retired generation cannot mutate current state.
- [ ] Full disconnect invalidates publication rights, cooperatively stops and
      joins all server-loop descendants, then clears runtime-owned state.
- [ ] Server-only disconnect does not return until the selected server session
      can no longer republish connection state, identity, or startup side effects.
- [ ] Reconnect can install a new generation immediately without interference
      from an older runtime or selected server session.
- [ ] Deterministic paused-task tests cover failed startup, full disconnect,
      server-only disconnect, and stale-writer rejection without timing sleeps.

## Validation

- Focused `emulebb-ed2k` server-loop, reachability, and NAT-manager tests.
- Focused `emulebb-core` startup, disconnect, and reconnect lifecycle tests.
- Repository formatting and Clippy checks after each implementation slice.
- Full Rust quality gate and required protected-main CI before merge.

## Implementation Progress

- Active Rust branch: `fix/rust-bug-121-transactional-runtime`.
- Slice 1: make NAT shutdown completion-aware and roll back failed startup.
- Slice 2: make server-loop descendant ownership cancellation-safe.
- Slice 3: fence reachability publication by runtime/server generation and make
  server-only disconnect an awaitable retirement barrier.
- Record each validated Rust commit and focused test result here before moving
  to the next slice.
- `bbce3b2c` makes NAT stop abort and await its reconcile worker before mapping
  release, with final-owner drop as an abort safety net. Validation: all 1,065
  `emulebb-ed2k` unit tests and doc tests passed through the workspace harness.
- `358b820a` owns pre-install NAT and reachability in an explicit startup
  candidate. Required NAT errors and every later interface, Kad, or TCP-bind
  failure now clear candidate publications, stop and join NAT, and release the
  selected mapping before returning the original error. Validation: all 405
  `emulebb-core` unit tests plus its integration and doc tests passed.
- `ac1a5643` replaces detachable description/parallel-session handles with
  abort-on-drop ownership, gives pending attempts an explicit retired state,
  and cooperatively cancels and joins every parallel loser on all normal exits.
  A forced outer-abort test proves descendant sockets close. Validation: all
  1,067 `emulebb-ed2k` unit tests and doc tests passed.
- `2b2eb329` makes the installed runtime own the server supervisor separately.
  Full disconnect signals shutdown, waits up to two seconds for cooperative
  descendant drainage, then aborts and still joins as a bounded fallback before
  clearing runtime state. Validation: all 407 `emulebb-core` unit tests plus its
  integration and doc tests passed, including barrier and timeout tests.
- `86572bc0` introduces non-clonable runtime/server reachability leases and
  cloneable generation-fenced writers. Old runtime and server writers now have
  explicit `RejectedStale` outcomes and cannot overwrite or clear a newer
  generation in focused tests. Validation: all 1,069 `emulebb-ed2k` unit tests
  and doc tests passed.
- `a246be43` installs the runtime lease through the startup transaction, stores
  it in `Ed2kRuntime`, and retires it before full-disconnect task signaling.
  NAT, STUN, and Kad firewall producers now receive only generation-fenced
  writers; rollback also proves its retained writer becomes `RejectedStale`.
  Validation: all 407 `emulebb-core` unit tests plus its integration and doc
  tests passed through the workspace harness.

## Notes

The audit also established important boundaries that should remain intact:

- Pending parallel attempts are activation-gated before publishing public IP or
  selected-session side effects; the stale-writer risk is the already-activated
  winner when its parent task is aborted.
- Cooperative server-loop exit cancels and awaits the server-description poller;
  the leak arises when the core aborts the parent before that cleanup executes.
- STUN, NAT-port synchronization, and Kad firewall-check loops are top-level
  runtime tasks and are individually aborted and awaited today. Generation
  fencing remains required as defense in depth and for future nested producers.

Implement in granular commits: failed-start rollback first, descendant task
ownership second, then generation-scoped publication and server-only retirement.
