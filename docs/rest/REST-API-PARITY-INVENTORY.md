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

- **`implemented`**
  - Meaning: Current `main` exposes the route through the OpenAPI contract and matching
             native route seam.

- **`obsolete`**
  - Meaning: Intentionally excluded from REST because it is deprecated web-page
             presentation state, session plumbing, binary streaming, host OS control, or
             outside the adapter's declared purpose.

This ledger currently has no deferred rows. Future controller-relevant gaps should
be tracked as active item IDs before being added here as pending work.

## Contract-Wide Release Requirements

- **REST base path is `/api/v1`**
  - Status: implemented
  - Notes: Existing REST already uses this root.

- **Auth uses `X-API-Key` only**
  - Status: implemented
  - Notes: No REST sessions, no cookie login, and no low-rights REST mode.

- **REST inherits WebServer bind, HTTPS, and allowed-IP exposure controls**
  - Status: implemented
  - Notes: REST remains in-process on the existing listener.

- **JSON success envelope is `{ data, meta }`**
  - Status: implemented
  - Notes: Landed on native `main`; aMuTorrent also unwraps this shape.

- **JSON collection envelope is `{ data: { items: [...] }, meta }`**
  - Status: implemented
  - Notes: Only `GET /shared-files` and `GET /upload-queue` expose `offset`/`limit`
           pagination metadata; other list routes are intentionally unpaged.

- **JSON error envelope is `{ error: { code, message, details? } }`**
  - Status: implemented
  - Notes: Native errors now use `{ error: { code, message } }`; `details` remains
           optional for future richer validation.

- **Field names are `camelCase`**
  - Status: implemented
  - Notes: Pre-release aliases were removed from public route parsing; final names
           include `searchId`, `categoryId`, `deleteFiles`, and `*KiBps` speed fields.

- **Mutations return the updated resource when practical**
  - Status: implemented
  - Notes: Preference, category, transfer property, shared-file metadata, and
           shared-directory mutations now return the updated model. Async/operation
           routes return operation envelopes.

- **Bulk endpoints use HTTP 200 with per-item results**
  - Status: implemented
  - Notes: Transfer delete and multi-link add use `{items:[...]}` per-item result
           envelopes.

- **Destructive file deletion requires explicit confirmation**
  - Status: implemented
  - Notes: Transfer deletes require `deleteFiles: true`; shared-file deletes require an
           explicit boolean because `false` means unshare/exclude without deleting the
           local file. `delete_files` is no longer public API.

- **aMuTorrent consumes this OpenAPI surface statically**
  - Status: implemented
  - Notes: The integration branch unwraps native envelopes and consumes final
           resource/operation routes and field names.

- **Native REST commands are serialized through the UI thread**
  - Status: implemented
  - Notes: `/api/v1` dispatch uses a synchronous main-window command before touching
           UI-owned eMule state, with exception containment at the dispatch boundary.

- **OpenAPI and smoke registry stay in sync**
  - Status: implemented
  - Notes: The Python smoke unit tests parse `REST-API-OPENAPI.yaml` and fail if route
           coverage drifts from the documented contract.

## Application And Preferences

- **Show app/version/runtime information**
  - REST target: `GET /app`
  - Status: implemented
  - Impact and notes: Returns app identity, build flavor, lifecycle state, and static
                      capabilities while REST is accepting requests.

- **Show global status/statistics summary**
  - REST target: `GET /status`, `GET /stats`, `GET /snapshot`
  - Status: implemented
  - Impact and notes: Status, stats, and snapshot routes use stable v1 envelopes.

- **Update WebServer gzip preference**
  - REST target: none
  - Status: obsolete
  - Impact and notes: HTML/WebServer gzip is page-serving presentation behavior, not a
                      native controller preference.

- **Update WebServer refresh interval**
  - REST target: none
  - Status: obsolete
  - Impact and notes: HTML/WebServer refresh timing remains in `[WebServer]
                      PageRefreshTime`; controller UIs own their own polling cadence.

- **Update max download speed**
  - REST target: `PATCH /app/preferences`
  - Status: implemented
  - Impact and notes: Uses `downloadLimitKiBps`; valid range is `1..4294967294` to match
                      finite UI limits and avoid the unlimited sentinel.

- **Update max upload speed**
  - REST target: `PATCH /app/preferences`
  - Status: implemented
  - Impact and notes: Uses `uploadLimitKiBps`; same range as download.

- **Update max sources per file**
  - REST target: `PATCH /app/preferences`
  - Status: implemented
  - Impact and notes: Uses `maxSourcesPerFile`; valid range is `1..2147483647` for UI
                      and INI integer round-trip.

- **Update max connections**
  - REST target: `PATCH /app/preferences`
  - Status: implemented
  - Impact and notes: Uses `maxConnections`; valid range is `1..2147483647`.

- **Update max connections per five seconds**
  - REST target: `PATCH /app/preferences`
  - Status: implemented
  - Impact and notes: Uses `maxConnectionsPerFiveSeconds`; valid range is
                      `1..2147483647`.

- **Start app shutdown**
  - REST target: `POST /app/shutdown`
  - Status: implemented
  - Impact and notes: Keeps eMule-process shutdown only. Excluded from live destructive
                      mutation loops.

- **Host shutdown or reboot from web UI**
  - REST target: none
  - Status: obsolete
  - Impact and notes: User explicitly excluded OS shutdown/reboot from REST.

- **HTML login/logout/session state**
  - REST target: none
  - Status: obsolete
  - Impact and notes: REST uses API-key auth only and must never fall back to HTML
                      session behavior.

- **HTML template, sort, column, refresh presentation state**
  - REST target: none
  - Status: obsolete
  - Impact and notes: Controller UIs own their own presentation state.

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

- **List downloads**
  - REST target: `GET /transfers`
  - Status: implemented
  - Impact and notes: Current REST already returns transfer rows.

- **Show one download**
  - REST target: `GET /transfers/{hash}`
  - Status: implemented
  - Impact and notes: Current route exists.

- **Add ED2K URL**
  - REST target: `POST /transfers`
  - Status: implemented
  - Impact and notes: Accepts `link` or `links` and always returns the per-item
                      operation envelope.

- **Pause transfer**
  - REST target: `POST /transfers/{hash}/operations/pause`
  - Status: implemented
  - Impact and notes: Returns the stable per-item operation envelope.

- **Resume transfer**
  - REST target: `POST /transfers/{hash}/operations/resume`
  - Status: implemented
  - Impact and notes: Returns the stable per-item operation envelope.

- **Stop transfer**
  - REST target: `POST /transfers/{hash}/operations/stop`
  - Status: implemented
  - Impact and notes: Returns the stable per-item operation envelope.

- **Cancel transfer**
  - REST target: `DELETE /transfers/{hash}` with `deleteFiles: true`
  - Status: implemented
  - Impact and notes: Native eMule cancel removes partial `.part` state; adapters must
                      not send `deleteFiles:false` for incomplete transfers.

- **Delete transfer local files**
  - REST target: `DELETE /transfers/{hash}` with `deleteFiles: true`
  - Status: implemented
  - Impact and notes: `deleteFiles` is the preferred spelling.

- **Clear completed transfers**
  - REST target: `POST /transfers/operations/clear-completed`
  - Status: implemented
  - Impact and notes: Uses the existing main-window clear-completed path.

- **Rename incomplete transfer**
  - REST target: `PATCH /transfers/{hash}`
  - Status: implemented
  - Impact and notes: Current main includes rename support for incomplete files only.

- **Set transfer priority**
  - REST target: `PATCH /transfers/{hash}`
  - Status: implemented
  - Impact and notes: Final enum is `auto`, `verylow`, `low`, `normal`, `high`, and
                      `veryhigh`; shared-file release priority is separate.

- **Set transfer category**
  - REST target: `PATCH /transfers/{hash}`
  - Status: implemented
  - Impact and notes: Supports category id/name; final naming must be
                      `categoryId`/`categoryName`.

- **File recheck**
  - REST target: `POST /transfers/{hash}/operations/recheck`
  - Status: implemented
  - Impact and notes: Returns the accepted-operation envelope after queuing the native
                      recheck.

- **Preview transfer**
  - REST target: `POST /transfers/{hash}/operations/preview`
  - Status: implemented
  - Impact and notes: Route validates preview readiness before launching the existing
                      preview command.

- **Get transfer sources**
  - REST target: `GET /transfers/{hash}/sources`
  - Status: implemented
  - Impact and notes: Current route exists.

- **Get one transfer source**
  - REST target: `GET /transfers/{hash}/sources/{clientId}`
  - Status: implemented
  - Impact and notes: Uses the same stable source selector as peer operations.

- **Get transfer part/source detail**
  - REST target: `GET /transfers/{hash}/details`
  - Status: implemented
  - Impact and notes: Native route returns transfer, part, and source detail; aMuTorrent
                      hydrates transfer detail from it.

- **Browse source**
  - REST target: `POST /transfers/{hash}/sources/{clientId}/operations/browse`
  - Status: implemented
  - Impact and notes: Uses source user hash as the stable selector where available.

- **Add/remove friend from transfer peer**
  - REST target: `POST /transfers/{hash}/sources/{clientId}/operations/add-friend`,
                 `.../remove-friend`, plus `/friends`
  - Status: implemented
  - Impact and notes: Transfer-source peer operations use the same stable `clientId`
                      selector exposed by source rows.

- **Ban/unban transfer peer**
  - REST target: `POST /transfers/{hash}/sources/{clientId}/operations/ban`, `.../unban`
  - Status: implemented
  - Impact and notes: Mirrors pro-user source context-menu controls.

- **Remove transfer source**
  - REST target: `POST /transfers/{hash}/sources/{clientId}/operations/remove`
  - Status: implemented
  - Impact and notes: Removes the source through the normal download queue removal path.

- **Hide transfer columns or update transfer table sort**
  - REST target: none
  - Status: obsolete
  - Impact and notes: Presentation state belongs to aMuTorrent or any other controller.

## Shared Files And Shared Directories

- **List shared files**
  - REST target: `GET /shared-files`
  - Status: implemented
  - Impact and notes: Current REST has shared-file listing.

- **Show one shared file**
  - REST target: `GET /shared-files/{hash}`
  - Status: implemented
  - Impact and notes: Current route exists.

- **Add one shared file by path**
  - REST target: `POST /shared-files`
  - Status: implemented
  - Impact and notes: Returns a shared-file create operation result because hashing may
                      be asynchronous.

- **Unshare one file**
  - REST target: `DELETE /shared-files/{hash}`
  - Status: implemented
  - Impact and notes: Uses final `deleteFiles` naming and returns the delete-result
                      envelope.

- **Delete shared local file**
  - REST target: `DELETE /shared-files/{hash}` with `deleteFiles: true`
  - Status: implemented
  - Impact and notes: Native deletion requires explicit `deleteFiles:true`; default
                      delete only unshares/excludes where allowed.

- **Set shared-file upload priority**
  - REST target: `PATCH /shared-files/{hash}`
  - Status: implemented
  - Impact and notes: Supports `auto`, `verylow`, `low`, `normal`, `high`, and native
                      upload `release`.

- **Update shared-file comment/rating**
  - REST target: `PATCH /shared-files/{hash}`
  - Status: implemented
  - Impact and notes: Current main supports comment/rating for completed shared files.

- **Get ED2K link**
  - REST target: `GET /shared-files/{hash}/ed2k-link`
  - Status: implemented
  - Impact and notes: Metadata only; binary file streaming remains excluded.

- **Show known file comments**
  - REST target: `GET /shared-files/{hash}/comments`
  - Status: implemented
  - Impact and notes: Returns the local known-file comment/rating metadata as a comments
                      collection.

- **Binary file download from WebServer `getfile`**
  - REST target: none
  - Status: obsolete
  - Impact and notes: User explicitly excluded binary shared-file streaming.

- **Reload shared files**
  - REST target: `POST /shared-files/operations/reload` and
                 `/shared-directories/operations/reload`
  - Status: implemented
  - Impact and notes: Final contract names both operation routes.

- **List shared directories**
  - REST target: `GET /shared-directories`
  - Status: implemented
  - Impact and notes: Current REST supports configured roots.

- **Replace shared directory roots**
  - REST target: `PATCH /shared-directories`
  - Status: implemented
  - Impact and notes: Request roots accept compact string paths or `{path, recursive}`
                      objects; current live E2E covers persistence.

- **Auto-share folder live monitor add/remove file events**
  - REST target: `GET /shared-files` plus live E2E
  - Status: implemented
  - Impact and notes: Live REST test coverage exists in `emulebb-build-tests`; final
                      contract stays resource-based.

- **Shared-files sort/column state**
  - REST target: none
  - Status: obsolete
  - Impact and notes: Presentation-only.

## Uploads And Queue

- **List active uploads**
  - REST target: `GET /uploads`
  - Status: implemented
  - Impact and notes: Current REST exposes uploads; aMuTorrent currently drops this data
                      in its data pipeline.

- **List upload queue**
  - REST target: `GET /upload-queue`
  - Status: implemented
  - Impact and notes: Current REST exposes queue.

- **Show one active upload**
  - REST target: `GET /uploads/{clientId}`
  - Status: implemented
  - Impact and notes: Returns the selected upload row plus existing score breakdown
                      state for controller drill-down.

- **Show one queued upload**
  - REST target: `GET /upload-queue/{clientId}`
  - Status: implemented
  - Impact and notes: Returns the selected waiting-queue row plus existing score
                      breakdown state for controller drill-down.

- **Remove upload client**
  - REST target: `POST /uploads/{clientId}/operations/remove`
  - Status: implemented
  - Impact and notes: Stable selectors are either user hash or `address:port` when no
                      hash exists; the duplicate `DELETE /uploads/{clientId}` alias was
                      removed before v1 freeze.

- **Give release slot**
  - REST target: `POST /uploads/{clientId}/operations/release-slot`
  - Status: implemented
  - Impact and notes: Uses the normal upload-queue removal path for active slots.

- **Upload context menu ban/unban**
  - REST target: `POST /uploads/{clientId}/operations/ban`, `.../unban`
  - Status: implemented
  - Impact and notes: Same peer-control command family as transfer sources.

- **Upload friend actions**
  - REST target: `POST /uploads/{clientId}/operations/add-friend`, `.../remove-friend`
  - Status: implemented
  - Impact and notes: Idempotent add returns an existing friend when already present.

- **Upload queue remove/release/friend/ban actions**
  - REST target: `POST /upload-queue/{clientId}/operations/...`
  - Status: implemented
  - Impact and notes: Queue routes share the same stable peer selector and operation
                      vocabulary.

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

- **Start search**
  - REST target: `POST /searches`
  - Status: implemented
  - Impact and notes: Returns `{id, query, method, type, status, results}` for async
                      polling.

- **List search sessions**
  - REST target: `GET /searches`
  - Status: implemented
  - Impact and notes: Returns active search sessions without expanding result rows.

- **Get search results**
  - REST target: `GET /searches/{searchId}`
  - Status: implemented
  - Impact and notes: aMuTorrent should poll this until stable and verify the echoed
                      `method` and `type`.

- **Stop/delete one search**
  - REST target: `DELETE /searches/{searchId}`
  - Status: implemented
  - Impact and notes: Final route deletes the search session.

- **Delete all searches**
  - REST target: `DELETE /searches`
  - Status: implemented
  - Impact and notes: Uses the existing delete-all-searches UI action.

- **Start search with method/type/min/max/availability/extension filters**
  - REST target: `POST /searches`
  - Status: implemented
  - Impact and notes: Method, type, size, and extension filters are parsed by the native
                      command seam.

- **Add selected search result to downloads**
  - REST target: `POST /searches/{searchId}/results/{hash}/operations/download`
  - Status: implemented
  - Impact and notes: Returns an operation result with the accepted search id and hash.

- **Clear searches before new search**
  - REST target: `DELETE /searches`
  - Status: implemented
  - Impact and notes: Explicit clear is required; `POST /searches` no longer accepts
                      `clearExisting` before v1 freeze.

- **Search page sort, table layout, and refresh**
  - REST target: none
  - Status: obsolete
  - Impact and notes: Presentation-only.

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

- **Endpoint adapter route names**
  - Status: implemented
  - Work required: aMuTorrent now prefers final operation/resource routes for transfers,
                   servers, shared reload, and search-result download.

- **Response envelopes**
  - Status: implemented
  - Work required: Native REST now always emits `{data, meta}` success envelopes and
                   `{error:{code,message,details}}` errors; aMuTorrent unwraps both.

- **Torznab search method policy**
  - Status: implemented
  - Work required: Prowlarr/Torznab movie and TV searches dispatch REST `video` searches
                   through connected `global` first and connected `kad` second,
                   combining connected-network results; other families keep the native
                   automatic policy.

- **qBittorrent transfer delete semantics**
  - Status: implemented
  - Work required: qBit-compatible delete requests always forward native transfer cancel
                   with `deleteFiles:true`; eMule does not provide a
                   partial-state-preserving delete for incomplete transfers.

- **Shared-file deletion**
  - Status: implemented
  - Work required: Shared deletes call `/shared-files/{hash}` instead of transfer delete
                   helpers.

- **Uploads in data pipeline**
  - Status: implemented
  - Work required: `/uploads` rows remain preserved through the eMuleBB manager fetch
                   result.

- **Transfer detail hydration**
  - Status: implemented
  - Work required: aMuTorrent hydrates peers plus part/source detail from
                   `/transfers/{hash}/details`.

- **Search polling**
  - Status: implemented
  - Work required: aMuTorrent stores the returned `id` and polls `/searches/{searchId}`
                   for results.

- **Browser smoke**
  - Status: implemented
  - Work required: `emulebb-build-tests` now owns `amutorrent-browser-smoke.py`,
                   launched from the aggregate live E2E suite.

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
