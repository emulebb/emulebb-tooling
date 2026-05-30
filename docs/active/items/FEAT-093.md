---
id: FEAT-093
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/83
title: Safely raise WebServer accepted-client concurrency
status: OPEN
priority: Minor
category: feature
labels: [webserver, rest, performance, threading, hardening, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-27
source: BUG-127 follow-up review of `kMaxAcceptedClientThreads == 1`
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/83. This local document is retained as an engineering spec/evidence record.

# FEAT-093 - Safely Raise WebServer Accepted-Client Concurrency

## Summary

Review and, if safe, raise the WebServer accepted-client worker cap from one
active request thread to a small bounded value. The current cap serializes the
native REST and legacy WebServer request path; that protects existing shared
state assumptions, but it also lets one slow client monopolize the WebServer
for up to the accepted-client I/O timeout.

## Current Shape

- `srchybrid/WebSocketHttpSeams.h` sets
  `kMaxAcceptedClientThreads == 1`.
- `srchybrid/WebSocket.cpp` accepts TCP clients on the listener thread and
  starts `WebSocketAcceptedFunc` only when the tracked accepted-client thread
  count is below the cap.
- `srchybrid/WebServer.cpp::_ProcessURL` still contains the historical warning
  that request threads access main eMule state without broad synchronization.
- Some WebServer state has been hardened, such as session and bad-login storage
  guarded by `m_WebStateLock`, but not every request path is proven safe for
  parallel execution.

## Motivation

Raising the cap would improve REST/controller responsiveness:

- one slow HTTPS handshake, upload, download, or stalled client would no longer
  block every other WebServer request;
- browser and controller clients could issue a small number of parallel REST
  requests without connection rejection;
- high-latency requests would stop serializing unrelated low-latency status
  calls.

## Risk

Do not change the cap as a one-line edit. The likely hazards are:

- shared per-request state such as `CWebServer::m_uCurIP` can be overwritten by
  concurrent accepted-client workers;
- REST or legacy WebServer handlers may read or mutate app-owned objects outside
  the UI thread without snapshots or owner-thread marshalling;
- additional accepted-client workers increase shutdown complexity because
  `StopSockets()` must wait for all workers before SSL and WebServer state can
  be freed;
- mbedTLS session cache/ticket globals and response queues must remain safe
  under concurrent accepted workers.

## Proposed Direction

1. Audit all `WebServerJson`, qBit/Arr compatibility, and remaining
   `_ProcessURL` paths for shared mutable state touched from accepted-client
   threads.
2. Remove or localize shared per-request state such as `m_uCurIP`; pass request
   IP through immutable `ThreadData` instead.
3. Ensure mutations are UI-thread marshalled or guarded by explicit owner
   locks. Prefer immutable snapshots for read-heavy REST list endpoints.
4. Add a configurable or constexpr bounded cap with an intentionally modest
   default, for example `2` or `4`, after the audit proves the request paths.
5. Extend REST/WebSocket stress tests to cover concurrent requests, slow
   clients, HTTPS handshakes, shutdown while accepted workers are active, and
   restart after accepted-client churn.

## Acceptance Criteria

- [ ] The reason for the current single-thread cap is documented from code
      review and test evidence.
- [ ] No shared per-request WebServer state is required for correct REST or
      compatibility request handling.
- [ ] REST mutations either marshal to the owning thread or use documented
      synchronization.
- [ ] Concurrent accepted-client stress covers at least the chosen new cap.
- [ ] Shutdown/restart tests pass while accepted-client workers are active.
- [ ] The cap is raised only after the above evidence is recorded.

## Related Items

- [FEAT-014](FEAT-014.md) - REST API follow-up and schema documentation.
- [FEAT-068](FEAT-068.md) - Bound REST large-list memory and latency.
- [REF-043](REF-043.md) - Drop the legacy HTML Web Interface and keep REST as
  the supported controller surface.
