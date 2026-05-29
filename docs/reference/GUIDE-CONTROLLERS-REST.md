# Controllers And REST Guide

This guide explains how eMuleBB should be used with trusted local controllers,
automation, and compatibility adapters.

For a task-first product walkthrough of eMuleBB with aMuTorrent, Prowlarr,
Radarr, and Sonarr, start with the
[Stack Integration Guide](GUIDE-STACK-INTEGRATIONS.md). This page is the
controller behavior reference.

## REST Is The Preferred Controller Path

eMuleBB exposes JSON REST under `/api/v1` through the embedded WebServer
listener. REST is the preferred automation surface. The legacy template web UI
is frozen pending removal and is not a supported controller surface.

Contract references:

- [REST API contract](../rest/REST-API-CONTRACT.md)
- [REST API quickstart](../rest/REST-API-QUICKSTART.md)
- [OpenAPI contract](../rest/REST-API-OPENAPI.yaml)
- [Adapter contracts](../rest/REST-API-ADAPTERS.md)

The OpenAPI document is the route and schema source of truth. Human guides
explain how to operate the surface safely.

## Trust Model

REST is for trusted local or controlled-network automation.

Use:

- API key authentication with `X-API-Key`
- deliberate bind address and port
- firewall rules matching the exposure policy
- a controlled network path
- redacted diagnostics when sharing support data

Do not expose REST broadly on untrusted networks. HTTPS protects transport on
the configured path, but it does not make broad exposure safe by itself.

## Local-Only Setup Recipe

Use this recipe for a controller on the same machine:

1. Finish normal desktop setup first.
2. Open `Preferences > Web Server`.
3. Enable the WebServer/REST listener.
4. Bind to localhost or the intended local-only address.
5. Use a strong API key/password.
6. Keep Windows Firewall closed to external clients unless deliberately
   exposing the listener.
7. Read `GET /api/v1/app` or another status route before attempting mutations.
8. Add mutations only after status and preferences reads work.

Local-only is the preferred default for automation. Use a broader bind only
when the operator controls the network path and firewall policy.

## Controlled-Network Setup Recipe

Use this recipe for a LAN or VPN controller path:

1. Choose the exact bind address or interface policy.
2. Choose a port and document it with firewall/router rules.
3. Configure allowed IPs when available.
4. Use HTTPS certificate material if the network path is not strictly local.
5. Use a strong unique API key/password.
6. Test status reads from the controller host.
7. Test one harmless read from each intended adapter.
8. Test one reversible mutation before enabling unattended workflows.

If the machine also uses P2P bind settings, keep them conceptually separate
from WebServer/REST bind settings. P2P listener binding and WebServer binding
are different surfaces.

## WebServer HTTPS And Certificates

REST uses the embedded WebServer listener. HTTPS therefore follows WebServer
certificate settings:

- `UseHTTPS` enables HTTPS behavior.
- `HTTPSCertificate` points to the certificate file.
- `HTTPSKey` points to the private-key file.
- `BindAddr`, `Port`, `AllowedIPs`, and firewall policy still control exposure.

The app can generate a WebServer certificate from the command line:

```powershell
emulebb.exe --generate-webserver-cert --cert webserver.crt --key webserver.key --host localhost --host 127.0.0.1
```

Generate certificates deliberately, store private keys with the profile or
operator-owned secret material, and keep controller API keys out of shared
logs.

## Native Behavior Remains Authoritative

Controllers must preserve eMule semantics:

- search network choice matters
- categories matter
- paused vs started adds matter
- delete and cancel operations are meaningful and potentially destructive
- completed files and incomplete parts are different resources
- source, fake, trust, comment, and category data should not be discarded
- local path ownership belongs to the native profile

When a controller presents eMuleBB as a generic download client, the adapter
must still map back to native behavior correctly.

## Native REST Surface

Native `/api/v1` covers the supported controller model:

- app state, preferences, shutdown, and diagnostics
- global status, snapshots, and stats
- categories
- transfers, transfer details, and transfer sources
- shared files and shared directories
- uploads and upload queue
- servers
- Kad
- searches and search results
- friends
- logs

Use OpenAPI for exact route names, request bodies, response envelopes, and
error shapes.

## Preference Mutation

REST exposes a curated mutable subset of preferences. It is intentionally not a
general `preferences.ini` editor.

Rules:

- use `GET /api/v1/app/preferences` to read the REST preference subset
- use `PATCH /api/v1/app/preferences` only for documented mutable fields
- unsupported names are rejected
- out-of-range values are rejected
- exact mutable field names are documented in OpenAPI and summarized in
  [Preferences Guide](GUIDE-PREFERENCES.md)

Direct config-file edits are a separate maintenance path, not REST behavior.

## Search And Download Recipe

For native REST search workflows:

1. Confirm the app is connected to the intended network.
2. Create a search with the intended method and type.
3. Read the search session until results are available.
4. Inspect filename, size, source, comment, fake/trust, and category data.
5. Download a selected result through the documented operation route.
6. Track the resulting native transfer by hash.
7. Use pause, resume, stop, or delete operations deliberately.

Do not discard native metadata just because a controller has a simpler UI.
eMule search quality depends on several signals, not only on a title match.

```mermaid
sequenceDiagram
    participant Controller
    participant REST as eMuleBB REST /api/v1
    participant Search as Native search
    participant Queue as Download queue

    Controller->>REST: POST /searches
    REST->>Search: start native eD2K/Kad search
    Search-->>REST: searchId and resolved method
    REST-->>Controller: Search envelope
    Controller->>REST: GET /searches/{searchId}
    REST->>Search: read visible results
    Search-->>REST: filenames, hashes, sources, evidence
    REST-->>Controller: Search result snapshot
    Controller->>REST: POST /searches/{searchId}/results/{hash}/operations/download
    REST->>Queue: add selected native transfer
    Queue-->>REST: accepted hash or per-item failure
    REST-->>Controller: Operation envelope
    Controller->>REST: GET /transfers/{hash}
    REST-->>Controller: Native transfer state
```

## Transfer Management Recipe

For controller-managed transfers:

1. List transfers and identify the hash.
2. Read transfer detail before destructive actions.
3. Preserve category and paused/started semantics.
4. Use explicit delete confirmation when files may be removed.
5. Use source operations only when the controller has a stable source selector.
6. Treat failed add-transfer items as real failures, not partial success.
7. Reconcile controller state with native desktop state after batch actions.

Native eMule distinction between cancel, delete, stop, pause, and completed
cleanup matters. Compatibility adapters must not flatten those into one action.

## Shared Files And Directories Recipe

For sharing automation:

1. Read current shared directories.
2. Replace shared directories only with a complete intended set.
3. Reload shared directories after external config changes.
4. Read shared files with paging where applicable.
5. Use explicit confirmation for destructive shared-file removal.
6. Keep local path visibility and privacy in mind before exposing data through
   controllers.

The desktop app owns shared-library scanning, hashing, and cache validation.
Controllers request state changes; they do not own the scan engine.

## aMuTorrent

aMuTorrent integration uses native REST and adapter behavior. Prove the basics
before running long workflows:

- app status reads correctly
- preferences read correctly
- search dispatch works
- add/download flow reaches eMuleBB
- upload and queue data remain meaningful when consumed
- typed error envelopes are handled

If browser/UI tests fail, compare aMuTorrent assumptions with the current
OpenAPI contract and live REST smoke evidence.

aMuTorrent should treat the desktop app as the authority. It may present a
modern controller workflow, but category, search, transfer, shared-file,
upload-queue, and lifecycle semantics still come from native eMuleBB state.

## Arr, qBit, And Torznab Adapters

Adapter surfaces let Arr-family tools, qBittorrent-compatible workflows, and
Torznab consumers talk to eMuleBB. These are compatibility layers, not the
native contract.

Expectations:

- native `/api/v1` remains authoritative
- qBit-compatible actions preserve eMule delete/category semantics
- Torznab search family mapping resolves to supported native search types
- adapter errors remain typed and predictable
- adapter routes should not invent behavior the native app cannot represent

For Arr-style automation, validate both search/indexer behavior and download
client behavior. A working Torznab search does not prove transfer management is
correct.

The most common manual setup values are:

| Surface | Value |
|---|---|
| Prowlarr indexer type | Generic Torznab |
| Prowlarr base URL | `http://HOST:PORT/indexer/emulebb` |
| Prowlarr API path | `/api` |
| Prowlarr API key | eMuleBB REST/Web API key |
| Movie category | `2000` |
| TV category | `5000` |
| Radarr/Sonarr download client type | qBittorrent |
| qBit host and port | eMuleBB WebServer/REST host and port |
| qBit username | `emule` |
| qBit password | eMuleBB REST/Web API key |
| Radarr category | `emulebb-radarr` |
| Sonarr category | `emulebb-sonarr` |

The qBittorrent-compatible download-client surface is an eMuleBB/eD2K subset.
It is meant for Arr clients consuming eMuleBB Torznab results and adding
`ed2k://` URLs back to eMuleBB. It is not a full qBittorrent clone: `.torrent`
uploads, BitTorrent magnet links, HTTP torrent URLs, tracker/RSS APIs, peer
management, sync APIs, and `hashes=all` mutations are outside the supported
controller contract.

Release packages may include helper scripts under `eMuleBB\scripts`:
`register-amutorrent.ps1` for aMuTorrent eMuleBB client registration,
`register-prowlarr.ps1` for the Prowlarr indexer, and
`register-arr-stack.ps1 -Target Radarr|Sonarr` for one selected Arr download
client plus optional Prowlarr application sync per run. The scripts are
conveniences over the same documented adapter surfaces; they do not add a
separate protocol.

## Lifecycle

REST has lifecycle restrictions. During startup and shutdown, unsafe operations
can be rejected to protect native app state.

Controllers should:

- handle lifecycle errors as retry/stop conditions
- avoid hammering during startup
- stop mutating after shutdown begins
- tolerate temporary unavailability during profile or listener changes
- retry reads more freely than mutations

Unattended controllers should use bounded retry with backoff. A tight retry loop
during startup can make diagnostics harder.

## Legacy WebServer

The legacy WebServer template UI is frozen pending removal. It receives no
product support, no feature work, and no controller compatibility guarantees.

REST and the documented qBit/Torznab adapters are the supported controller
surfaces. REST should remain useful even when legacy templates are absent.

## Diagnostics

For controller failures, collect:

- route, method, status code, and response body
- whether the route exists in OpenAPI
- app lifecycle state
- WebServer enabled/bind/port settings
- API key configuration
- adapter name and version, when applicable
- recent REST and app logs
- redacted diagnostic snapshot

Do not share API keys, private keys, or full raw profile dumps unless the
recipient is trusted and the exposure is understood.

### Unsafe Diagnostic REST

The native REST contract includes diagnostic dump and crash-test routes:

- `POST /api/v1/diagnostics/dumps`
- `POST /api/v1/diagnostics/crash-tests`

These endpoints are intentionally unsafe for ordinary controller exposure. They
are disabled unless diagnostic REST endpoints are explicitly enabled, and they
require request confirmation fields: `confirmDump: true` or
`confirmCrash: true`.

Keep them localhost-only or on a tightly controlled operator network. Use dump
capture for release proof and support evidence; use crash tests only for
diagnostic harnesses. Do not expose these routes through broad LAN, public
reverse-proxy, or Arr-controller paths.

For snapshot, dump, and redaction details, see
[Diagnostics Guide](GUIDE-DIAGNOSTICS.md).

## Troubleshooting

REST unavailable:

1. Confirm WebServer/REST is enabled.
2. Check bind address and port.
3. Check firewall and allowed IP policy.
4. Confirm the app is not starting or shutting down.
5. Try a local status request from the same machine.

Auth failure:

1. Confirm the current API key.
2. Confirm the `X-API-Key` header is sent.
3. Check whether the profile regenerated an empty/missing key.
4. Remove stale controller secrets after a profile restore.

Route or schema failure:

1. Compare the route with OpenAPI.
2. Check field casing exactly.
3. Remove unsupported aliases.
4. Confirm adapter mapping is not using stale qBit/Torznab assumptions.

Mutation rejected:

1. Check lifecycle state.
2. Check whether the target resource still exists.
3. Check destructive confirmation fields.
4. Check native state in the desktop app.
5. Retry only if the response indicates a temporary condition.
