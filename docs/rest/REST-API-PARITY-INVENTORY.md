# eMuleBB REST API Migrated Action Inventory

**Status:** current completed parity ledger
**Contract:** [REST-API-OPENAPI.yaml](REST-API-OPENAPI.yaml)
**Scope:** controller-relevant runtime capabilities historically reachable
through WebServer command handlers, plus explicit exclusions for
presentation-only, frozen template UI, or host-level actions.

This inventory is not a functional parity promise for the legacy
template-based WebServer UI. That engine is frozen and compile-only until
removal; its HTML pages, templates, sessions, and page interaction state are
not supported and are not release gates.

## Classification Rules

| Status | Meaning |
|---|---|
| `implemented` | Current `main` exposes the route through the OpenAPI contract and matching native route seam. |
| `obsolete` | Intentionally excluded from REST because it is deprecated web-page presentation state, session plumbing, binary streaming, host OS control, or outside the adapter's declared purpose. |

This ledger currently has no deferred rows. Future controller-relevant gaps should
be tracked as active item IDs before being added here as pending work.

## Contract-Wide Release Requirements

| Requirement | Status | Notes |
|---|---|---|
| REST base path is `/api/v1` | implemented | Existing REST already uses this root. |
| Auth uses `X-API-Key` only | implemented | No REST sessions, no cookie login, and no low-rights REST mode. |
| REST inherits WebServer bind, HTTPS, and allowed-IP exposure controls | implemented | REST remains in-process on the existing listener. |
| JSON success envelope is `{ data, meta }` | implemented | Landed on native `main`; aMuTorrent also unwraps this shape. |
| JSON collection envelope is `{ data: { items: [...] }, meta }` | implemented | Only `GET /shared-files` and `GET /upload-queue` expose `offset`/`limit` pagination metadata; other list routes are intentionally unpaged. |
| JSON error envelope is `{ error: { code, message, details? } }` | implemented | Native errors now use `{ error: { code, message } }`; `details` remains optional for future richer validation. |
| Field names are `camelCase` | implemented | Pre-release aliases were removed from public route parsing; final names include `searchId`, `categoryId`, `deleteFiles`, and `*KiBps` speed fields. |
| Mutations return the updated resource when practical | implemented | Preference, category, transfer property, shared-file metadata, and shared-directory mutations now return the updated model. Async/operation routes return operation envelopes. |
| Bulk endpoints use HTTP 200 with per-item results | implemented | Transfer delete and multi-link add use `{items:[...]}` per-item result envelopes. |
| Destructive file deletion requires explicit confirmation | implemented | Transfer deletes require `deleteFiles: true`; shared-file deletes require an explicit boolean because `false` means unshare/exclude without deleting the local file. `delete_files` is no longer public API. |
| aMuTorrent consumes this OpenAPI surface statically | implemented | The integration branch unwraps native envelopes and consumes final resource/operation routes and field names. |
| Native REST commands are serialized through the UI thread | implemented | `/api/v1` dispatch uses a synchronous main-window command before touching UI-owned eMule state, with exception containment at the dispatch boundary. |
| OpenAPI and smoke registry stay in sync | implemented | The Python smoke unit tests parse `REST-API-OPENAPI.yaml` and fail if route coverage drifts from the documented contract. |

## Application And Preferences

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| Show app/version/runtime information | `GET /app` | implemented | Returns app identity, build flavor, lifecycle state, and static capabilities while REST is accepting requests. |
| Show global status/statistics summary | `GET /status`, `GET /stats`, `GET /snapshot` | implemented | Status, stats, and snapshot routes use stable v1 envelopes. |
| Update WebServer gzip preference | none | obsolete | HTML/WebServer gzip is page-serving presentation behavior, not a native controller preference. |
| Update WebServer refresh interval | none | obsolete | HTML/WebServer refresh timing remains in `[WebServer] PageRefreshTime`; controller UIs own their own polling cadence. |
| Update max download speed | `PATCH /app/preferences` | implemented | Uses `downloadLimitKiBps`; valid range is `1..4294967294` to match finite UI limits and avoid the unlimited sentinel. |
| Update max upload speed | `PATCH /app/preferences` | implemented | Uses `uploadLimitKiBps`; same range as download. |
| Update max sources per file | `PATCH /app/preferences` | implemented | Uses `maxSourcesPerFile`; valid range is `1..2147483647` for UI and INI integer round-trip. |
| Update max connections | `PATCH /app/preferences` | implemented | Uses `maxConnections`; valid range is `1..2147483647`. |
| Update max connections per five seconds | `PATCH /app/preferences` | implemented | Uses `maxConnectionsPerFiveSeconds`; valid range is `1..2147483647`. |
| Start app shutdown | `POST /app/shutdown` | implemented | Keeps eMule-process shutdown only. Excluded from live destructive mutation loops. |
| Host shutdown or reboot from web UI | none | obsolete | User explicitly excluded OS shutdown/reboot from REST. |
| HTML login/logout/session state | none | obsolete | REST uses API-key auth only and must never fall back to HTML session behavior. |
| HTML template, sort, column, refresh presentation state | none | obsolete | Controller UIs own their own presentation state. |

## Categories

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| List categories | `GET /categories` | implemented | Returns the category collection envelope. |
| Create category | `POST /categories` | implemented | Required for aMuTorrent category management. |
| Edit category | `PATCH /categories/{categoryId}` | implemented | Default category id `0` remains protected. |
| Delete category | `DELETE /categories/{categoryId}` | implemented | Must preserve normal eMule constraints. |
| Category tab refresh | `GET /categories` plus UI polling | obsolete | Web UI tab refresh action is presentation-only. |
| Set category priority | `PATCH /categories/{categoryId}` | implemented | Category create/update accepts final `priority` values. |

## Transfers

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| List downloads | `GET /transfers` | implemented | Current REST already returns transfer rows. |
| Show one download | `GET /transfers/{hash}` | implemented | Current route exists. |
| Add ED2K URL | `POST /transfers` | implemented | Accepts `link` or `links` and always returns the per-item operation envelope. |
| Pause transfer | `POST /transfers/{hash}/operations/pause` | implemented | Returns the stable per-item operation envelope. |
| Resume transfer | `POST /transfers/{hash}/operations/resume` | implemented | Returns the stable per-item operation envelope. |
| Stop transfer | `POST /transfers/{hash}/operations/stop` | implemented | Returns the stable per-item operation envelope. |
| Cancel transfer | `DELETE /transfers/{hash}` with `deleteFiles: true` | implemented | Native eMule cancel removes partial `.part` state; adapters must not send `deleteFiles:false` for incomplete transfers. |
| Delete transfer local files | `DELETE /transfers/{hash}` with `deleteFiles: true` | implemented | `deleteFiles` is the preferred spelling. |
| Clear completed transfers | `POST /transfers/operations/clear-completed` | implemented | Uses the existing main-window clear-completed path. |
| Rename incomplete transfer | `PATCH /transfers/{hash}` | implemented | Current main includes rename support for incomplete files only. |
| Set transfer priority | `PATCH /transfers/{hash}` | implemented | Final enum is `auto`, `verylow`, `low`, `normal`, `high`, and `veryhigh`; shared-file release priority is separate. |
| Set transfer category | `PATCH /transfers/{hash}` | implemented | Supports category id/name; final naming must be `categoryId`/`categoryName`. |
| File recheck | `POST /transfers/{hash}/operations/recheck` | implemented | Returns the accepted-operation envelope after queuing the native recheck. |
| Preview transfer | `POST /transfers/{hash}/operations/preview` | implemented | Route validates preview readiness before launching the existing preview command. |
| Get transfer sources | `GET /transfers/{hash}/sources` | implemented | Current route exists. |
| Get one transfer source | `GET /transfers/{hash}/sources/{clientId}` | implemented | Uses the same stable source selector as peer operations. |
| Get transfer part/source detail | `GET /transfers/{hash}/details` | implemented | Native route returns transfer, part, and source detail; aMuTorrent hydrates transfer detail from it. |
| Browse source | `POST /transfers/{hash}/sources/{clientId}/operations/browse` | implemented | Uses source user hash as the stable selector where available. |
| Add/remove friend from transfer peer | `POST /transfers/{hash}/sources/{clientId}/operations/add-friend`, `.../remove-friend`, plus `/friends` | implemented | Transfer-source peer operations use the same stable `clientId` selector exposed by source rows. |
| Ban/unban transfer peer | `POST /transfers/{hash}/sources/{clientId}/operations/ban`, `.../unban` | implemented | Mirrors pro-user source context-menu controls. |
| Remove transfer source | `POST /transfers/{hash}/sources/{clientId}/operations/remove` | implemented | Removes the source through the normal download queue removal path. |
| Hide transfer columns or update transfer table sort | none | obsolete | Presentation state belongs to aMuTorrent or any other controller. |

## Shared Files And Shared Directories

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| List shared files | `GET /shared-files` | implemented | Current REST has shared-file listing. |
| Show one shared file | `GET /shared-files/{hash}` | implemented | Current route exists. |
| Add one shared file by path | `POST /shared-files` | implemented | Returns a shared-file create operation result because hashing may be asynchronous. |
| Unshare one file | `DELETE /shared-files/{hash}` | implemented | Uses final `deleteFiles` naming and returns the delete-result envelope. |
| Delete shared local file | `DELETE /shared-files/{hash}` with `deleteFiles: true` | implemented | Native deletion requires explicit `deleteFiles:true`; default delete only unshares/excludes where allowed. |
| Set shared-file upload priority | `PATCH /shared-files/{hash}` | implemented | Supports `auto`, `verylow`, `low`, `normal`, `high`, and native upload `release`. |
| Update shared-file comment/rating | `PATCH /shared-files/{hash}` | implemented | Current main supports comment/rating for completed shared files. |
| Get ED2K link | `GET /shared-files/{hash}/ed2k-link` | implemented | Metadata only; binary file streaming remains excluded. |
| Show known file comments | `GET /shared-files/{hash}/comments` | implemented | Returns the local known-file comment/rating metadata as a comments collection. |
| Binary file download from WebServer `getfile` | none | obsolete | User explicitly excluded binary shared-file streaming. |
| Reload shared files | `POST /shared-files/operations/reload` and `/shared-directories/operations/reload` | implemented | Final contract names both operation routes. |
| List shared directories | `GET /shared-directories` | implemented | Current REST supports configured roots. |
| Replace shared directory roots | `PATCH /shared-directories` | implemented | Request roots accept compact string paths or `{path, recursive}` objects; current live E2E covers persistence. |
| Auto-share folder live monitor add/remove file events | `GET /shared-files` plus live E2E | implemented | Live REST test coverage exists in `emulebb-build-tests`; final contract stays resource-based. |
| Shared-files sort/column state | none | obsolete | Presentation-only. |

## Uploads And Queue

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| List active uploads | `GET /uploads` | implemented | Current REST exposes uploads; aMuTorrent currently drops this data in its data pipeline. |
| List upload queue | `GET /upload-queue` | implemented | Current REST exposes queue. |
| Show one active upload | `GET /uploads/{clientId}` | implemented | Returns the selected upload row plus existing score breakdown state for controller drill-down. |
| Show one queued upload | `GET /upload-queue/{clientId}` | implemented | Returns the selected waiting-queue row plus existing score breakdown state for controller drill-down. |
| Remove upload client | `POST /uploads/{clientId}/operations/remove` | implemented | Stable selectors are either user hash or `address:port` when no hash exists; the duplicate `DELETE /uploads/{clientId}` alias was removed before v1 freeze. |
| Give release slot | `POST /uploads/{clientId}/operations/release-slot` | implemented | Uses the normal upload-queue removal path for active slots. |
| Upload context menu ban/unban | `POST /uploads/{clientId}/operations/ban`, `.../unban` | implemented | Same peer-control command family as transfer sources. |
| Upload friend actions | `POST /uploads/{clientId}/operations/add-friend`, `.../remove-friend` | implemented | Idempotent add returns an existing friend when already present. |
| Upload queue remove/release/friend/ban actions | `POST /upload-queue/{clientId}/operations/...` | implemented | Queue routes share the same stable peer selector and operation vocabulary. |

## Servers

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| List servers | `GET /servers` | implemented | Returns the server collection envelope. |
| Show server status | `GET /status`, `GET /servers` | implemented | Final contract folds status into resource rows and `/status`. |
| Connect to best server | `POST /servers/operations/connect` | implemented | Final route is resource-operation shaped and returns server status. |
| Connect to specific server | `POST /servers/{serverId}/operations/connect` | implemented | `serverId` is URL-encoded `address:port`. |
| Disconnect or stop connecting | `POST /servers/operations/disconnect` | implemented | Covers both disconnect and stop-connecting runtime commands. |
| Add server | `POST /servers` | implemented | Final create supports `address`, `port`, `name`, `priority`, `static`, and `connect`. |
| Remove server | `DELETE /servers/{serverId}` | implemented | Existing route exists. |
| Add server to static list | `PATCH /servers/{serverId}` with `static: true` | implemented | Static membership is handled as a server property. |
| Remove server from static list | `PATCH /servers/{serverId}` with `static: false` | implemented | Static membership is handled as a server property. |
| Set server priority low/normal/high | `PATCH /servers/{serverId}` | implemented | Priority is handled as a server property. |
| Update server.met from URL | `POST /servers/operations/import-met-url` | implemented | Marshalled through the existing UI interaction path. |

## Kad

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| Show Kad status | `GET /kad` | implemented | Current status route exists. |
| Start Kad | `POST /kad/operations/start` | implemented | Final route returns Kad status. |
| Stop Kad | `POST /kad/operations/stop` | implemented | Final route returns Kad status. |
| Recheck Kad firewall | `POST /kad/operations/recheck-firewall` | implemented | Returns Kad status plus firewall-check operation flags. |
| Bootstrap Kad | `POST /kad/operations/bootstrap` | implemented | Requires `{address, port}` and validates the port range before dispatch. |
| Update nodes.dat from URL | `POST /kad/operations/import-nodes-url` | implemented | Marshalled through the existing validated nodes.dat import path. |

## Searches

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| Start search | `POST /searches` | implemented | Returns `{id, query, method, type, status, results}` for async polling. |
| List search sessions | `GET /searches` | implemented | Returns active search sessions without expanding result rows. |
| Get search results | `GET /searches/{searchId}` | implemented | aMuTorrent should poll this until stable and verify the echoed `method` and `type`. |
| Stop/delete one search | `DELETE /searches/{searchId}` | implemented | Final route deletes the search session. |
| Delete all searches | `DELETE /searches` | implemented | Uses the existing delete-all-searches UI action. |
| Start search with method/type/min/max/availability/extension filters | `POST /searches` | implemented | Method, type, size, and extension filters are parsed by the native command seam. |
| Add selected search result to downloads | `POST /searches/{searchId}/results/{hash}/operations/download` | implemented | Returns an operation result with the accepted search id and hash. |
| Clear searches before new search | `DELETE /searches` | implemented | Explicit clear is required; `POST /searches` no longer accepts `clearExisting` before v1 freeze. |
| Search page sort, table layout, and refresh | none | obsolete | Presentation-only. |

## Logs

| Migrated capability | REST target | Status | Impact and notes |
|---|---|---|---|
| Show recent log lines | `GET /logs` | implemented | Current REST has bounded recent logs. |
| Warning when process runs elevated | `GET /logs` plus app startup warning | implemented | Startup warning was added earlier; REST exposes recent log buffer. |
| Detailed build warnings | none | obsolete | Build logs are workspace artifacts, not runtime REST data. |

## Explicit Non-Goals

| Legacy or possible action | Status | Rationale |
|---|---|---|
| Binary shared-file streaming through REST | obsolete | Metadata and ED2K links are enough for controller integration; local file serving changes risk profile. |
| Host OS shutdown/reboot | obsolete | Not needed by aMuTorrent and too destructive for the trusted local API. |
| Deprecated template sessions and low-rights mode | obsolete | REST is all-in behind `X-API-Key`. |
| Dynamic capability negotiation | obsolete | eMuleBB and aMuTorrent ship together; static contract compliance is simpler and stricter. |
| Granular REST permissions | obsolete | User explicitly chose all-in API-key behavior. |

## aMuTorrent Gap Checklist

| Area | Status | Work required |
|---|---|---|
| Endpoint adapter route names | implemented | aMuTorrent now prefers final operation/resource routes for transfers, servers, shared reload, and search-result download. |
| Response envelopes | implemented | Native REST now always emits `{data, meta}` success envelopes and `{error:{code,message,details}}` errors; aMuTorrent unwraps both. |
| Torznab search method policy | implemented | Prowlarr/Torznab movie and TV searches dispatch REST `video` searches through connected `global` first and connected `kad` second, combining connected-network results; other families keep the native automatic policy. |
| qBittorrent transfer delete semantics | implemented | qBit-compatible delete requests always forward native transfer cancel with `deleteFiles:true`; eMule does not provide a partial-state-preserving delete for incomplete transfers. |
| Shared-file deletion | implemented | Shared deletes call `/shared-files/{hash}` instead of transfer delete helpers. |
| Uploads in data pipeline | implemented | `/uploads` rows remain preserved through the eMuleBB manager fetch result. |
| Transfer detail hydration | implemented | aMuTorrent hydrates peers plus part/source detail from `/transfers/{hash}/details`. |
| Search polling | implemented | aMuTorrent stores the returned `id` and polls `/searches/{searchId}` for results. |
| Browser smoke | implemented | `emulebb-build-tests` now owns `amutorrent-browser-smoke.py`, launched from the aggregate live E2E suite. |

## Arr And qBittorrent-Compatible Adapter Boundary

The `/api/v2` routes are a compatibility adapter for Arr download-client
integration. Completeness for this surface means the Arr suite can authenticate,
test the qBittorrent-shaped client, add releases, inspect downloads, update
Arr-relevant transfer state, assign categories, pause/resume/start/stop where
Arr expects those verbs, and remove transfers.

The `/api/v2` adapter is not a full qBittorrent Web API clone. Unrelated
qBittorrent features such as RSS, tracker editing, peer-management, sync,
logging, ban lists, global speed controls, and full content-layout operations
remain outside the release contract unless a future Arr compatibility need makes
one of them part of the adapter purpose.

## Release Gate

The completed REST parity surface is kept current by these supported workspace entrypoints:

| Gate | Status |
|---|---|
| eMule app validation/build/tests | implemented |
| Native REST route and contract tests | implemented |
| Live eMule REST E2E completeness lane | implemented |
| aMuTorrent Node eMuleBB tests | implemented |
| Live aMuTorrent browser smoke against eMuleBB | implemented |
