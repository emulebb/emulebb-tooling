# Review 2026-04-18 — eMuleAI vs Main Hardening Pass

## Scope

Focused comparison of:

- `analysis\emuleai`
- current `workspaces\v0.72a\app\eMule-main`

The pass intentionally focused on:

- networking
- performance
- file-handling
- security-adjacent hardening
- concrete bug fixes, races, and logical flaws

Theme and translation work was intentionally ignored.

The branch goal remained the default workspace rule: stay as close as possible to stock
eMule behavior and only promote narrow, high-value fixes.

## Already Landed On Main

The comparison first revalidated what current `main` already absorbed and therefore should
not be reopened as backlog work:

- `REF-007` — MIME magic-table refresh plus WebM / Matroska split
- `FEAT-020` — peer geolocation landed with DB-IP rather than GeoLite2
- `FEAT-022` — startup config override via `-c`
- `FEAT-026` — shared startup cache / known-file lookup index / `sharedcache.dat`
- `FEAT-027` — startup sequencing and trace-backed profiling
- `FEAT-028` — Shared Files list virtualization and hardening
- `BUG-029` — long-path tail hardening across config/media/GeoLocation/shell edges
- `BUG-025` / `BUG-026` / `BUG-027` already cover eMuleAI's matching:
  - hash-open diagnostic corruption
  - Close All Search Results crash
  - destructive IP-filter promotion failure

## New Confirmed Backlog Promotions

### BUG-030 — obfuscated server login capability advertisement

eMuleAI contains a narrow guard that suppresses `REQUESTCRYPT` / `REQUIRECRYPT` in the
server login packet when the main server socket is already obfuscated. Current `main`
still advertises those flags unconditionally from preferences, and the eMuleAI rationale
matches a plausible current-tree networking symptom: fully obfuscation-capable server
lists can require multiple attempts before login succeeds.

### BUG-031 — transient lock/share retry for shared-file hashing

Current `main` still performs only a single open attempt when hashing a newly discovered
shared file. eMuleAI adds a bounded retry on `ERROR_SHARING_VIOLATION` and
`ERROR_LOCK_VIOLATION`, which is a narrow, stock-preserving improvement for files still
being copied or moved into shared folders.

### BUG-032 — `known2.met` lock timeout during AICH hashset save

Current `main` still lets `CAICHRecoveryHashSet::SaveHashSet()` give up after five seconds
waiting for the global `known2.met` mutex. eMuleAI removes that timeout. This looks like a
real false-failure race rather than a feature difference.

## Revalidated But Not Promoted

Several eMuleAI release-note items were rechecked but were not promoted into new backlog
items in this pass:

- duplicate shared files rehashed on startup / duplicate-files history interactions
- uploads disappearing while shared files reload
- shared-files status-counter crash
- long UI freezes before hashing large shared folders
- upload speedometer visual quirks

Reason:

- current `main` already has large landed share/startup/list-control changes on that same
  surface (`FEAT-026` / `FEAT-027` / `FEAT-028` / `BUG-029`)
- the remaining eMuleAI fixes in that area are intertwined with broader worker-thread,
  virtual-list, duplicate-history, or watcher behavior
- there was not enough direct current-tree evidence to promote a new narrow stock-friendly
  bug item yet

Those areas should be revalidated again only if a live repro appears on current `main`.

## Explicit Non-Promotions

The following eMuleAI areas were intentionally not promoted because they are too feature-
drifty for the current branch goal:

- uTP transport
- NAT traversal / buddy extensions
- threaded shared-files reload and filesystem watcher
- source saver / source cache product features
- dark mode and theme work
- translation-system changes

## Outcome

This pass refreshed the active backlog to match current `main` and promoted only the
remaining narrow hardening deltas that still look worth bringing in:

- [BUG-030](../items/BUG-030.md)
- [BUG-031](../items/BUG-031.md)
- [BUG-032](../items/BUG-032.md)

It also closed or corrected stale backlog state for already-landed work on `main`.
