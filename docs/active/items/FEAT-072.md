---
id: FEAT-072
title: Reduce startup cache UI-thread blocking on large shared libraries
status: OPEN
priority: Minor
category: feature
labels: [startup, shared-files, performance, ui, cache]
milestone: post-beta-0.7.3
created: 2026-05-22
source: live large-library profiling against the operator-provided profile and startup dump analysis
---

# FEAT-072 - Reduce Startup Cache UI-Thread Blocking On Large Shared Libraries

## Summary

Live profiling of a large shared-library profile showed startup CPU and UI
responsiveness problems while `CSharedFileList` loads and applies shared-file
startup caches. A captured startup dump showed the main thread spending time in
filesystem path canonicalization while building startup-cache lookup keys.

This item tracks a compatibility-preserving cleanup: avoid filesystem
canonicalization for in-memory cache keys, add rate-limited startup progress
pumping inside long cache loops, and only consider a worker-backed cache
preloader after re-profiling the simpler fix.

## Intended Shape

- Use lexical, case-insensitive normalized path keys for `sharedcache.dat` and
  duplicate-path cache map lookup.
- Keep existing on-disk `.dat` formats unchanged.
- Keep real filesystem canonicalization for actual scan paths, validation, and
  cache rebuild/write paths where it is semantically required.
- Add a rate-limited startup progress pump, defaulting to the existing short UI
  yield cadence, inside long startup cache and shared-directory loops.
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
- [ ] focused native tests cover lexical cache-key behavior and progress-pump
      cadence
- [ ] a CPU-only live run against the large-library profile shows the captured
      `TryCanonicalizeExistingPath` startup hot stack is gone or materially
      reduced
