---
id: FEAT-081
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/76
title: Add a bounded source-hostname resolver pool only if profiling shows backlog
status: DEFERRED
priority: Trivial
category: feature
labels: [download-queue, dns, resolver, threading, profiling, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-24
source: review of background parallel processing opportunities after REF-030 landed
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/76. This local document is retained as an engineering spec/evidence record.

# FEAT-081 - Add A Bounded Source-Hostname Resolver Pool Only If Profiling Shows Backlog

## Summary

`REF-030` has already replaced the old download-source window-message resolver
with a worker-thread `getaddrinfo()` model. Current `main` uses one resolver
worker and drains completed source addresses from the download queue.

Do not expand this preemptively. A small bounded resolver pool is only worth
adding if live profiling shows hostname-resolution backlog under real source
intake.

## Intended Shape

- Instrument pending and completed hostname-resolution queue depth.
- Record resolution latency and backlog age in diagnostics.
- Add a small configurable or hard-capped worker count only if profiling proves
  the single worker is a bottleneck.
- Continue draining results on the download queue owner path.
- Keep IPv6 result handling aligned with the IPv6 roadmap rather than sneaking
  in transport behavior changes.

## Scope Constraints

- Do not reintroduce `WSAAsyncGetHostByName`.
- Do not mutate `CDownloadQueue`, `CPartFile`, or client state from resolver
  workers.
- Do not create unbounded resolver threads.
- Do not change source scoring, source limits, or connection policy.

## Acceptance Criteria

- [ ] resolver queue-depth and latency diagnostics exist
- [ ] profiling evidence proves whether a pool is needed
- [ ] if implemented, worker count is bounded and cancellation remains clean
- [ ] add-source-by-hostname behavior remains unchanged
- [ ] tests cover shutdown while resolutions are pending

## Validation

- `python -m emule_workspace validate`
- focused resolver seam tests
- live profile with many hostname-based sources, if available
- x64 Debug and Release app builds before commit
