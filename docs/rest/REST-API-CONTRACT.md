# eMuleBB REST API Contract

**Status:** beta 0.7.3 broadband contract
**Source of truth:** [REST-API-OPENAPI.yaml](REST-API-OPENAPI.yaml)
**Adapter subsets:** [REST-API-ADAPTERS.md](REST-API-ADAPTERS.md)
**Migrated action inventory:** [REST-API-PARITY-INVENTORY.md](REST-API-PARITY-INVENTORY.md)
**Primary implementation:** `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\eMule-main\srchybrid\WebServerJson.cpp`
**Route seam:** `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\eMule-main\srchybrid\WebServerJsonSeams.h`

## Overview

`main` exposes an authenticated in-process JSON API from the existing eMule
WebServer listener. The broadband release contract is the resource-oriented
`/api/v1` surface described by the OpenAPI document above.

The API is designed for aMuTorrent and other trusted local controllers. The
beta 0.7.3 contract intentionally prioritizes consistency and aMuTorrent
completeness over preserving old command-style route names.

## Controller Boundary

aMuTorrent is the primary UI consumer and beta 0.7.3 proof target, but it is not
the authority for native route shape. The aMuTorrent eMuleBB adapter must
translate UI expectations to the clean `/api/v1` contract instead of requiring
native aliases, qBittorrent-compatible response shapes, or legacy command-style
routes.

Arr integrations are separate compatibility adapters. Prowlarr Torznab,
Radarr/Sonarr controller flows, and qBittorrent-compatible download-client
routes may keep adapter-specific quirks where those clients require them, but
shared parsing, validation, safety, and serialization should come from the same
native helpers wherever practical. Adapter compatibility must not broaden or
weaken the native `/api/v1` OpenAPI contract. Torznab movie and TV searches run
connected `global` and `kad` probes and combine results; non-media Torznab
families keep the native default `automatic` search policy.
qBittorrent-compatible transfer delete requests are adapted to native cancel
semantics and therefore forward `deleteFiles: true` to the shared transfer
delete command even when a qBit caller omits or clears its optional flag.

The `/api/v2` surface is a qBittorrent-compatible adapter for Arr download
client integration only. It is complete when Prowlarr, Radarr, Sonarr, and other
Arr clients can authenticate, test the client, add transfers, inspect transfer
state, mutate Arr-relevant transfer state, assign categories, and remove
transfers through the qBittorrent-shaped routes they call. It is not a promise
to implement the full qBittorrent Web API surface, including unrelated RSS,
tracker, peer-management, sync, logging, ban-list, global-speed, or complete
content-layout operations.

The legacy template-based WebServer UI is a frozen surface behind the same
listener. The release goal for that engine is compile preservation only until
it is removed. HTML templates, legacy page routes, and template interaction
state are not part of the REST v1 contract, not part of the adapter contract,
not supported, and not a release-gated behavior surface beyond avoiding shared
listener regressions.

## Contract Rules

- root every endpoint at `/api/v1/...`
- authenticate only with `X-API-Key`
- serve JSON only
- inherit the normal WebServer bind, HTTPS, and allowed-IP behavior
- use `camelCase` field names
- use lowercase compact exact tokens for enum-like string values, with no
  camelCase, snake_case, case folding, or aliases
- keep native priority families separate: transfer download priority uses
  `auto`, `verylow`, `low`, `normal`, `high`, and `veryhigh`; shared-file
  upload priority uses `auto`, `verylow`, `low`, `normal`, `high`, and
  `release`
- return success envelopes as `{ "data": ..., "meta": ... }`
- return unpaged collections as `{ "data": { "items": [...] }, "meta": ... }`
- return transfer add and transfer pause/resume/stop/delete operations as
  stable per-item operation envelopes, including the single-link and single-hash
  routes
- expose `offset`/`limit` pagination only on `GET /shared-files` and
  `GET /upload-queue`, with responses shaped as
  `{ "data": { "items": [...], "total": n, "offset": n, "limit": n }, "meta": ... }`
- expose `limit` without `offset` only for bounded snapshots/tails such as
  `GET /snapshot` and `GET /logs`
- expose shared-files startup readiness through `status.stats.sharedFilesReady`
  and `status.sharedStartupCache`; clients must not infer readiness from an
  empty `sharedFiles` array during startup warmup
- expose app lifecycle through `app.lifecycle` and `status.lifecycle` using
  lowercase compact state tokens: `starting`, `running`, `shuttingdown`, and
  `done`; the exit-confirmation dialog remains public `running` state
- reject mutating REST requests, diagnostic unsafe requests, and
  `POST /app/shutdown` while lifecycle is `starting`, and reject all REST
  requests once lifecycle is `shuttingdown` or `done`
- return errors as `{ "error": { "code": "...", "message": "...", "details": {} } }`
- return the updated resource from mutations when practical; asynchronous or
  native operation routes return explicit operation-result DTOs instead
- keep public response DTOs closed in OpenAPI; additive fields require an
  explicit OpenAPI update and matching contract tests in the same change
- expose one canonical public route for each operation; upload removal uses
  `POST /uploads/{clientId}/operations/remove`, not a duplicate `DELETE`
  alias
- validate method/path/body/query through the native route schema table before
  dispatching commands
- reject unknown JSON body fields and unknown or malformed query parameters with
  `400 INVALID_ARGUMENT`
- validate public rename text with the same UTF-8/control-character and
  255-character public filename limit used by REST-adjacent link conversion
- accept server.met and nodes.dat URL imports only as trimmed `http://` or
  `https://` URLs with a host, no whitespace, and a 2048-character limit
- require explicit booleans such as `deleteFiles: true` for destructive local
  file deletion
- use HTTP 200 for valid bulk requests with per-item results
- marshal native commands through the main UI thread before touching eMule
  state owned by dialogs, sockets, queues, and list controls
- keep the route execution model explicit in the native route seam; only
  static/direct-safe routes may bypass the UI-thread dispatch path
- reject pre-release alias spellings; public request fields are the final
  OpenAPI names such as `categoryId`, `searchId`, `deleteFiles`,
  `uploadLimitKiBps`, and `downloadLimitKiBps`

## Scope

The release API must cover controller-relevant runtime capabilities that were
historically reachable through WebServer command handlers: transfers, shared
files, shared directories, uploads, upload queue, servers, Kad, searches,
friends, logs, categories, statistics, preferences, and application shutdown.
That inventory tracks migrated behavior, not a promise that the deprecated
template UI keeps functioning. Operator diagnostic dump capture and crash-test
endpoints live under `/diagnostics`, require explicit diagnostic REST opt-in,
and remain outside broad automated mutation/stress loops.

The release API intentionally excludes:

- HTML sessions, login/logout, templates, sort state, column hiding, and other
  frozen legacy WebServer presentation state
- WebServer page-only preferences such as HTML gzip and refresh interval
- host operating-system shutdown and reboot
- binary shared-file streaming
- granular REST permissions or low-rights REST mode
- dynamic capability negotiation between eMuleBB and aMuTorrent

`PATCH /api/v1/shared-directories` replaces the configured shared-directory
roots and requires `confirmReplaceRoots: true`. Each root may be either a
non-empty string path or an object with a non-empty `path` and optional
`recursive` flag. Response-only directory state such as existence, monitoring,
or shareability is not accepted in the replacement request.

## Search Semantics

`POST /api/v1/searches` starts a native eMule search using the requested method:
`automatic`, `server`, `global`, or `kad`. The request may also select a native
search file type with the exact REST file-type token: empty string for any
type, `arc`, `audio`, `iso`, `image`, `pro`, `video`, `doc`, or
`emulecollection`. No aliases, alternate casing, or request-time type remapping
are accepted. The route maps those public tokens directly to the existing
eD2K/Kad search modes and file-type filters and must not change stock search
semantics for beta 0.7.3. `automatic` resolves from live network state:
connected eD2K uses `global`, Kad-only uses `kad`, and no connected network is
rejected as not connected. Search resources echo the resolved method and
selected REST type so
controllers can distinguish eD2K server/global searches from Kad searches and
audit the selected file filter without inferring from result timing or counts.

`GET /api/v1/searches` lists active native search sessions without expanding
their result rows. `GET /api/v1/searches/{searchId}` returns the current native
visible result snapshot for one search. Beta 0.7.3 intentionally does not
expose search result paging; search routes do not accept `limit` or `offset`,
and the strict route table rejects unknown query parameters. Controllers should
poll the search resource and treat `results` as a bounded native snapshot
governed by eMule's existing search-result retention and visibility behavior.
Each native result also carries the resolved search method and selected search
type when the result is returned through a search resource. `SearchResult.fileType`
is the raw native file-type tag reported for that row; `SearchResult.fileType`
remains row metadata and is not constrained to or remapped through the
search-filter token enum.

Search results expose grouped `SearchResult.evidence` instead of a single
risk score. Controllers must treat this as explanatory evidence, not a
safety guarantee:

- `riskEvidence` covers local fake-file, spam, rating, header, media-plausibility,
  and AICH-conflict warnings.
- `availabilityEvidence` covers source counts, complete-source counts, observed
  clients/servers, and Kad publisher counts.
- `nameEvidence` covers observed names, canonical names, ignored tokens, and
  meaningful name divergence groups.
- `kadPublisherEvidence` decodes Kad publish metadata into publisher count,
  different-name count, raw Kad value, and a low/normal/high evidence band.
- `integrityEvidence` covers AICH presence, multiple-AICH conflicts, pending or
  cached header checks, and claimed/detected file type evidence.

Unknown evidence is neutral, not positive; clients must not display it as
trusted or safe. Search creation does not clear existing searches as a side
effect; controllers must call
`DELETE /api/v1/searches` with `confirmDeleteAllSearches: true` when they need a
clean search set.

`POST /api/v1/searches/{searchId}/results/{hash}/operations/download` starts a
download from one visible search result by lowercase 32-character eD2K hash and
returns an operation result with the accepted search id and hash. It does not
pretend to return a `Transfer` resource before the native download queue has
materialized one.

`DELETE /api/v1/transfers/{hash}` cancels an incomplete native transfer. eMule
does not preserve partial `.part` state on cancel, so controllers must send
`deleteFiles: true` for incomplete transfers and treat that as native cancel
semantics rather than an optional disk-delete toggle. The route validator
rejects `deleteFiles: false` before dispatch.

Selected peer reads are available for controller drill-down through
`GET /transfers/{hash}/sources/{clientId}`, `GET /uploads/{clientId}`, and
`GET /upload-queue/{clientId}`. These routes use the same `clientId` selector
as peer operations and expose read models only; chat/message APIs and peer
shared-file browse result retrieval remain outside the beta 0.7.3 native v1
contract.
Transfer source rows expose `downloadState` with the same lowercase compact
token policy as the rest of v1; native debug labels are not part of the REST
contract.

## Implementation Status

The OpenAPI contract is the implemented target contract for the current
beta 0.7.3 pass. Native route-seam tests cover the route schema table, strict
validation behavior, and the internal route execution model. The Python smoke
harness includes OpenAPI route consistency checks, validates success/error
envelopes, and reports whether each native route is direct or UI-thread
dispatched. aMuTorrent's eMuleBB adapter consumes the same final field names
while keeping aMuTorrent's own public routes stable.

The live smoke harness validates route coverage and response envelopes against
OpenAPI. The strict DTO policy is enforced by tests that reject open-ended
public response schemas except for explicitly documented extension maps such as
`error.details` and `app.capabilities`.

## Search Refactoring Notes

Future cleanup should keep the current wire contract unchanged while reducing
implementation duplication: the native REST command seam can collapse toward the
exact type string contract instead of maintaining a parallel enum, and the
Torznab family-to-search-type mapping still resolves to REST tokens accepted by
`/api/v1/searches`.

## Controller Compatibility Matrix

| Consumer | Surface | Contract boundary | Proof lane |
|---|---|---|---|
| Native REST clients | `/api/v1` | OpenAPI is authoritative; adapters do not define route names or envelopes. | REST smoke, OpenAPI drift, live completeness |
| aMuTorrent | `/api/v1` through its own adapter | Translates UI expectations to final native fields and unwraps native envelopes. | aMuTorrent browser smoke |
| Prowlarr Torznab | Torznab XML adapter | Keeps Torznab XML/error shape adapter-local while reusing native parsing and search commands. | Prowlarr live |
| Radarr/Sonarr | Torznab plus qBit-compatible download client | Uses Arr-facing compatibility routes without broadening `/api/v1`. | Radarr/Sonarr live |
| qBittorrent-compatible clients | `/api/v2` | Implements the Arr-needed qBit subset only; qBit text/session errors stay adapter-shaped. | qBit route completeness and Arr live |

Adapter subset details are documented in [REST-API-ADAPTERS.md](REST-API-ADAPTERS.md).

## Execution Model

The native route table records whether a route is direct or UI-thread
dispatched. `GET /api/v1/app` is currently the only direct route because it
serves application identity, lifecycle, build metadata, and static
capabilities. Lifecycle gating is evaluated before direct execution, so direct
routes are still rejected after shutdown begins. Runtime reads, mutations,
destructive operations, and adapter bridges remain UI-thread dispatched until
ownership is proven safe at the implementation layer.
The same lifecycle command policy is reused by qBit-compatible and Torznab
bridge calls that invoke native REST commands in-process, so adapter bridges do
not bypass startup/shutdown safety gates.

Use [REST-API-PARITY-INVENTORY.md](REST-API-PARITY-INVENTORY.md) for the
completed WebServer-to-REST action parity ledger. Runtime route completeness is expected to
match [REST-API-OPENAPI.yaml](REST-API-OPENAPI.yaml).

## Retired Before Public Release

The following earlier command-style routes are not part of the final broadband
release contract and should not be used by aMuTorrent:

- `/api/v1/app/version`
- `/api/v1/stats/global`
- `/api/v1/transfers/add`
- `/api/v1/transfers/pause`
- `/api/v1/transfers/resume`
- `/api/v1/transfers/stop`
- `/api/v1/transfers/delete`
- `/api/v1/uploads/list`
- `/api/v1/uploads/queue`
- `/api/v1/servers/list`
- `/api/v1/servers/status`
- `/api/v1/search/start`
- `/api/v1/search/results`
- `/api/v1/search/stop`
- `/api/v1/log`
