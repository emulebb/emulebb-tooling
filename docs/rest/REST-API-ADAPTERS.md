# eMule BB REST Adapter Contracts

**Status:** beta 0.7.3 adapter subset contract
**Native contract:** [REST-API-CONTRACT.md](REST-API-CONTRACT.md)

## Purpose

Native `/api/v1` is the only clean JSON REST contract. The compatibility
adapters below exist so Arr-family tools can talk to eMule BB without forcing
native v1 to mimic qBittorrent or Torznab quirks.

The deprecated legacy template-based WebServer UI is frozen and compile-only
until removal. It is not an adapter contract, no functional HTML/template
behavior is supported, and no adapter or release campaign may add
template-specific tests for beta 0.7.3.

## qBittorrent-Compatible `/api/v2`

`/api/v2` is an Arr download-client compatibility subset, not a full
qBittorrent Web API clone. It uses qBittorrent-shaped content types, text
responses, session cookies, and form bodies where Arr clients expect them.

Reference surface used for compatibility decisions:

- qBittorrent Web API wiki, especially application, auth, and torrent routes:
  <https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-%28qBittorrent-4.1%29>
- Radarr qBittorrent download client schema fields as exposed by
  `/api/v3/downloadclient/schema`.

Supported routes:

| Method | Route | Auth | Contract role |
|---|---|---|---|
| `GET` | `/api/v2/app/webapiVersion` | no | Public qBit Web API version probe. |
| `POST` | `/api/v2/auth/login` | no | Form login using the configured eMule BB API key as password. |
| `GET` | `/api/v2/app/version` | yes | App version probe. |
| `GET` | `/api/v2/app/preferences` | yes | Minimal preference payload for Arr client tests. |
| `GET` | `/api/v2/torrents/categories` | yes | Category map. |
| `POST` | `/api/v2/torrents/createCategory` | yes | Create a native category from qBit form field `category`. |
| `GET` | `/api/v2/torrents/info` | yes | Transfer list, optionally filtered by `category`; rows include Arr import fields such as `save_path` and `content_path` from the native category path. |
| `GET` | `/api/v2/torrents/properties` | yes | One transfer's qBit-shaped properties by `hash`, including path, size, progress, and seeding-time fields consumed by Arr completed download handling. |
| `GET` | `/api/v2/torrents/files` | yes | One transfer's qBit-shaped file list by `hash`, including file `name`, `size`, and `progress`. |
| `POST` | `/api/v2/torrents/add` | yes | Add one Torznab-emitted eD2K link; accepts Arr qBit form fields that eMule ignores after validation. Magnet URLs are rejected. |
| `POST` | `/api/v2/torrents/delete` | yes | Delete/cancel transfers by `hashes`; always maps to native `deleteFiles: true`. |
| `POST` | `/api/v2/torrents/setCategory` | yes | Assign a native category by `hashes` and `category`. |
| `POST` | `/api/v2/torrents/pause` | yes | Pause transfers by `hashes`. |
| `POST` | `/api/v2/torrents/stop` | yes | Stop transfers by `hashes`. |
| `POST` | `/api/v2/torrents/resume` | yes | Resume transfers by `hashes`. |
| `POST` | `/api/v2/torrents/start` | yes | Start/resume transfers by `hashes`. |
| `POST` | `/api/v2/torrents/setShareLimits` | yes | Accepted no-op for Arr compatibility after validating `hashes`, `ratioLimit`, `seedingTimeLimit`, and `inactiveSeedingTimeLimit`. |
| `POST` | `/api/v2/torrents/topPrio` | yes | Accepted no-op for Arr compatibility after validating `hashes`. |
| `POST` | `/api/v2/torrents/setForceStart` | yes | Accepted no-op after validating `hashes` and optional boolean `value`. |

Unsupported qBittorrent families remain outside the adapter contract: RSS,
tracker editing, peer management, sync, logging, ban lists, global speed
controls, and full content-layout operations.

Hash mutation routes accept one to 100 pipe-delimited 32-character eD2K hashes
in qBittorrent's `hashes` form field. The `hashes=all` value is intentionally
not supported by the Arr adapter.

## Torznab `/indexer/emulebb/api`

The Torznab adapter is a Prowlarr/Radarr/Sonarr search bridge. It emits XML and
uses adapter-shaped status codes and bodies; it never returns native v1 JSON
envelopes.

Reference surface used for compatibility decisions:

- Torznab specification: <https://torznab.github.io/spec-1.3-draft/>
- Newznab search category conventions used by Arr clients:
  <https://newznab.readthedocs.io/en/latest/misc/api/>

Supported request shape:

| Field | Contract |
|---|---|
| `t` | `caps`, `search`, `tvsearch`, or `movie`; missing or empty defaults to `search`. |
| `apikey` | Optional query API key. If omitted, `X-API-Key` may authenticate the request. |
| `q` | Search text, normalized through native REST search validation. |
| `cat` | Comma-separated Torznab categories mapped to native eMule file families. |
| `season`, `ep`, `year` | Optional unsigned decimal filters bounded to `0..9999`. |
| `offset`, `limit` | Optional unsigned decimal paging controls. `limit` is bounded to `0..100`, with `0` using the default `100`; `offset` is bounded to `0..1000000`. Non-zero offsets page only a cached first-page result set for the same normalized query, category, media family, and native method set. If no cached result set exists, the adapter returns an empty accepted feed instead of launching a new native search for that later page. |

Unknown Torznab/Newznab extension query parameters are ignored after strict URL
decoding and duplicate-name rejection. This keeps compatibility with Arr-family
clients that send provider-specific IDs while still rejecting malformed escapes,
duplicate parameters after lowercase normalization, unsupported `t` values, and
invalid numeric fields.

Supported responses:

- `200 application/xml` for caps and accepted searches.
- `400 application/xml` for malformed query parameters or unsupported request
  types.
- `401 application/xml` for missing or invalid API keys.
- `503 application/xml` when the native REST API key is not configured or the
  native search bridge is still busy and no non-empty cached response exists.

Error responses use adapter-local Torznab XML rather than native REST JSON:
`<error code="HTTP_STATUS" description="..."/>`.

Movie and TV searches dispatch REST `video` searches through connected
`global` first and connected `kad` second, combining eD2K hashes from the
available networks. Other Torznab families keep the REST file-family mapping
and default automatic search policy used by `POST /api/v1/searches`: connected
eD2K resolves to `global`, Kad-only resolves to `kad`, and offline searches are
rejected as not connected. The
adapter-side result filter for extension, size, and Torznab family only narrows
returned rows; it does not replace the REST `type` field sent to REST v1.
