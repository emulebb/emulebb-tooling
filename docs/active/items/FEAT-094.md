---
id: FEAT-094
title: Improve UDP burst handling without lock-held backoff
status: OPEN
priority: Major
category: feature
labels: [udp, networking, sockets, performance, locks, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-27
source: senior C++ performance and I/O review of client and server UDP paths
---

# FEAT-094 - Improve UDP Burst Handling Without Lock-Held Backoff

## Summary

The client and server UDP paths can be made more responsive under bursty or
congested traffic without changing wire behavior. The two safe targets are
removing lock-held retry sleeps and draining a bounded number of datagrams per
socket event.

## Current Evidence

- `CClientUDPSocket::SendControlData` can sleep for 20 ms after
  `WSAEWOULDBLOCK` while still holding `sendLocker`.
- Client and server UDP receive handlers process one datagram per socket event,
  which increases wakeups and can fall behind during bursts.
- Hot-path malformed-packet logging can still format repeatedly under hostile
  traffic.

## Intended Shape

1. Change the UDP send retry path so would-block handling requeues or schedules
   retry without sleeping while `sendLocker` is held.
2. Add capped receive-drain loops for client UDP and server UDP events.
3. Keep each drain loop bounded by packet count and/or elapsed work budget to
   avoid starving the UI/message pump.
4. Add counters for receive batch size, queue drops, would-block sends, and
   retry requeues.
5. Rate-limit aggregate malformed-packet diagnostics where verbose logging can
   become a CPU or disk sink.

## Scope Constraints

- Preserve packet ordering for queued control packets.
- Do not spin on repeated `WSAEWOULDBLOCK`; one failed send should produce one
  bounded retry action.
- Do not alter UDP obfuscation, encryption gating, packet formats, Kad opcode
  behavior, or server/client retry policy.
- Do not let receive-drain loops monopolize the UI thread.

## Acceptance Criteria

- [ ] The client UDP sender never sleeps while holding `sendLocker`.
- [ ] Would-block send injection verifies one requeue/retry action, no spin,
      and preserved packet order.
- [ ] Client UDP and server UDP handlers drain bounded batches per wake.
- [ ] Burst tests at 1, 8, 64, and 256 datagrams per wake compare drops, CPU,
      and message-pump responsiveness.
- [ ] Malformed-packet flood tests show bounded logging overhead.

## Validation

- `python -m emule_workspace validate`
- UDP would-block injection tests
- local UDP burst tests for client and server sockets
- malformed Kad/server UDP flood tests with verbose logging on and off
- x64 Debug and Release app builds before commit
