# ed2k-server Active Backlog — Issue Index

> **Historical status:** Retired from active planning on 2026-10-02. Preserved as provenance only.

This directory is the local engineering spec layer for the active Phase 1
production-hardening program. Workflow state lives in
[`emulebb/ed2k-server` issues](https://github.com/emulebb/ed2k-server/issues)
and the public [eMuleBB Suite project](https://github.com/orgs/emulebb/projects/3)
with `Product = ed2k-server` and `Phase = Phase 1`.

## Current snapshot

**Source of truth:** `EMULEBB_WORKSPACE_ROOT\repos\ed2k-server` (`master` branch).
**Reviewed baseline:** `604b2579160fd76680243aed472d58d9d8772dec`.
**Lifecycle:** active production-hardening candidate; not production-approved.
**Harness status:** not selected. `goed2k-server` remains the deterministic
shared-harness server until a separate integration decision.
**Milestone:** `production-readiness`.

## ID taxonomy

Items use `ED2KSRV-<CLASS>-<NNN>`, where `CLASS` is `BUG`, `FEAT`, `REF`, or
`CI`. IDs are allocated per class and never reused.

## Priority order

1. Close remotely triggerable resource-safety and admission risks.
2. Make every advertised protocol capability truthful.
3. Establish a clean-room differential corpus against Go and observed
   Lugdunum behavior.
4. Add production lifecycle, observability, load, soak, and canary evidence.

## Active backlog

| ID | Priority | Title |
|---|---|---|
| [ED2KSRV-BUG-001](ed2k-server/items/ED2KSRV-BUG-001.md) | Critical | Bound packed-frame decompression |
| [ED2KSRV-BUG-002](ed2k-server/items/ED2KSRV-BUG-002.md) | Critical | Enforce configured client and publication limits |
| [ED2KSRV-BUG-003](ed2k-server/items/ED2KSRV-BUG-003.md) | Critical | Bound TCP and UDP work admission and rate limits |
| [ED2KSRV-BUG-004](ed2k-server/items/ED2KSRV-BUG-004.md) | Critical | Make advertised protocol capabilities truthful |
| [ED2KSRV-BUG-005](ed2k-server/items/ED2KSRV-BUG-005.md) | Critical | Bound protocol parser strings and collections |
| [ED2KSRV-CI-001](ed2k-server/items/ED2KSRV-CI-001.md) | Major | Build a clean-room differential protocol corpus |
| [ED2KSRV-CI-002](ed2k-server/items/ED2KSRV-CI-002.md) | Major | Qualify load, soak, and controlled canary gates |
| [ED2KSRV-CI-003](ed2k-server/items/ED2KSRV-CI-003.md) | Critical | Resolve dependency advisories and enforce an advisory gate |
| [ED2KSRV-FEAT-001](ed2k-server/items/ED2KSRV-FEAT-001.md) | Major | Add graceful shutdown and supervised task lifecycle |
| [ED2KSRV-FEAT-002](ed2k-server/items/ED2KSRV-FEAT-002.md) | Major | Add production observability and restart recovery |
| [ED2KSRV-FEAT-003](ed2k-server/items/ED2KSRV-FEAT-003.md) | Major | Make source selection bounded and fair |

Dependencies are recorded in each item. Resource-safety items are the first
production gate; open high/critical dependency advisories also block a
production recommendation. Load/canary qualification must exercise the final
resource limits.
