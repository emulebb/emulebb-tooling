---
id: FEAT-021
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/61
title: SourceSaver — persist download source lists between sessions
status: OPEN
priority: Minor
category: feature
labels: [download, sources, persistence, recovery]
milestone: ~
created: 2026-04-10
source: eMuleAI (SourceSaver.cpp/h, CSourceSaver class, 2026)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/61. This local document is retained as an engineering spec/evidence record.

# FEAT-021 - SourceSaver — persist download source lists between sessions

## Summary

When eMule restarts, all active sources for in-progress downloads are lost. The client must
re-discover sources from Kad, server queries, and passive source exchange — a process that
can take minutes to hours for rare files. eMuleAI's `CSourceSaver` persists the source list
for each in-progress download to disk and reloads it on startup, dramatically reducing the
time to resume transfers after a restart.

## eMuleAI Reference Implementation

**Source files:**
- `eMuleAI/SourceSaver.cpp` / `SourceSaver.h` — `CSourceSaver` class

GitHub references from eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed):

- periodic save/load entry points:
  [`SourceSaver.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/SourceSaver.cpp#L44),
  [`SourceSaver.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/SourceSaver.cpp#L74),
  [`SourceSaver.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/SourceSaver.cpp#L155)
- restored-source injection:
  [`SourceSaver.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/SourceSaver.cpp#L135)
- source expiry helpers:
  [`SourceSaver.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/SourceSaver.cpp#L251)

**Per-source data persisted:**
```cpp
class CSourceData {
    CAddress  sourceIP;       // IPv4/IPv6 peer address
    uint32    sourceID;       // eDonkey user ID
    uint16    sourcePort;     // TCP port
    uint32    serverip;       // server IP (for ID-sourced peers)
    uint16    serverport;     // server port
    CString   expiration;     // absolute timestamp when source expires
    uint8     nSrcExchangeVer; // source exchange version
};
```

**File format:** Per-file XML or binary format keyed by file hash, stored in the temp/config
directory. `CalcExpiration(int nDays)` computes an ISO timestamp for source TTL.

**Lifecycle:**
- `Process(CPartFile* file)` — saves sources for a given download to disk
- `DeleteFile(CPartFile* file)` — removes the saved source file on download completion
- Called periodically from the main timer loop (e.g., every N minutes)
- On startup, loaded before Kad bootstrap completes

## Implementation Considerations

1. **CAddress dependency**: `CSourceSaver` uses `CAddress` (eMuleAI's IPv4/IPv6 abstraction).
   Adapting to `uint32` + optional IPv6 struct is straightforward.

2. **Source exchange version**: Persist `nSrcExchangeVer` to avoid re-negotiating on reload.

3. **TTL / expiration**: Sources older than N days should not be loaded. eMuleAI uses a
   configurable expiration window (`CalcExpiration(int nDays)`).

4. **Integration point**: `CDownloadQueue::Process()` or `CPartFile::InitializeFromFile()`
   for load; `CDownloadQueue::Process()` timer for save.

5. **Rare-file benefit**: For files with <10 sources globally, losing the source list on
   restart can mean hours of re-discovery. SourceSaver eliminates this.

6. **Source validity**: Saved sources are hints, not guarantees. The connection attempt must
   still succeed and the source must still have the file. Invalid saved sources are cleaned
   up naturally when the connection fails.

7. **Persistence compatibility**: This should not alter `.part.met` identity or
   downgrade behavior. Prefer a separate cache file or future local database
   table with versioning, TTL, and bounded size. Saved sources are advisory
   startup hints only.

## Relationship to Existing Items

- **BUG-011** (Done: shareddir list race): no direct relationship, but same Preferences
  file infrastructure.
- **FEAT-002** (SafeKad CGNAT fix): SafeKad reduces source loss from firewall transitions;
  SourceSaver addresses session boundaries.

## Acceptance Criteria

- [ ] `CSourceSaver::Process(CPartFile*)` saves source list to a per-file binary/XML in
  the temp directory
- [ ] Sources loaded on startup before Kad is ready
- [ ] Sources with expired TTL not loaded
- [ ] `DeleteFile()` called on download completion (no stale files left)
- [ ] No regression if source file is missing, corrupted, or empty
- [ ] Preferences toggle: enable/disable source saving; configurable TTL (default: 7 days)
- [ ] Maximum sources per file capped (e.g., 200) to prevent unbounded file growth
- [ ] persisted source hints are stored outside core `.met` files unless a
      separately approved metadata-format change exists
