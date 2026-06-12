---
id: FEAT-072
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/69
title: Reduce startup cache UI-thread blocking on large shared libraries
status: OPEN
priority: Minor
category: feature
labels: [startup, shared-files, performance, ui, cache]
milestone: post-0.7.3
created: 2026-05-22
source: live large-library profiling against the operator-provided profile and startup dump analysis; 2026-05-27 senior C++ performance and I/O review
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/69. This local document is retained as an engineering spec/evidence record.

# FEAT-072 - Reduce startup cache UI-thread blocking on large shared libraries

## Summary

Live profiling of a large shared-library profile showed startup CPU and UI
responsiveness problems while `CSharedFileList` loads and applies shared-file
startup caches. A captured startup dump showed the main thread spending time in
filesystem path canonicalization while building startup-cache lookup keys.

This item tracks a compatibility-preserving cleanup: avoid filesystem
canonicalization for in-memory cache keys, add rate-limited startup progress
pumping inside long cache loops, and only consider a worker-backed cache
preloader after re-profiling the simpler fix.

The 2026-05-27 performance review added two concrete follow-ups to this lane:
startup-cache load should reject malformed or oversized cache files before
large vector reservations, and long-path preparation caching should avoid
full-cache churn during very large scans if profiling shows eviction pressure.

## Intended Shape

- Use lexical, case-insensitive normalized path keys for `sharedcache.dat` and
  duplicate-path cache map lookup.
- Keep existing on-disk `.dat` formats unchanged.
- Keep real filesystem canonicalization for actual scan paths, validation, and
  cache rebuild/write paths where it is semantically required.
- Add a rate-limited startup progress pump, defaulting to the existing short UI
  yield cadence, inside long startup cache and shared-directory loops.
- Add a global startup-cache file-record cap and file-size sanity checks before
  reserving cache vectors.
- Instrument long-path prepared-path cache hit/miss or eviction behavior before
  replacing its full-clear behavior with bounded eviction.
- Re-profile before moving broader `CSharedFileList` startup work onto a worker
  thread.

## Scope Constraints

- Do not change `.met`, `.part.met`, `sharedcache.dat`, or duplicate-cache file
  schemas.
- Do not change shared-file policy, duplicate detection policy, hashing policy,
  or network behavior.
- Do not move MFC UI state or shared-list owner state directly onto a worker
  thread.
- Treat a background cache preloader as a follow-up only if the key and pump
  cleanup does not remove the observed startup freeze.

## Acceptance Criteria

- [ ] startup cache lookup and insertion no longer call filesystem
      canonicalization just to form map keys
- [ ] existing `sharedcache.dat` and duplicate-cache files remain readable
      without migration
- [ ] startup progress remains responsive during large cache load and shared
      directory rehydration loops
- [ ] malformed or oversized startup caches are rejected before large memory
      reservations
- [ ] long-path prepared-path cache changes are driven by hit/miss or eviction
      evidence, not by speculation
- [ ] focused native tests cover lexical cache-key behavior and progress-pump
      cadence
- [ ] a CPU-only live run against the large-library profile shows the captured
      `TryCanonicalizeExistingPath` startup hot stack is gone or materially
      reduced
