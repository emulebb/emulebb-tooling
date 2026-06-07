# eMuleBB REST Adapter Contracts

**Status:** 0.7.3 RC1 adapter subset contract
**Native contract:** [REST-API-CONTRACT.md](REST-API-CONTRACT.md)

## Purpose

Native `/api/v1` is the only clean JSON REST contract. The compatibility
adapters below exist so Arr-family tools can talk to eMuleBB without forcing
native v1 to mimic qBittorrent or Torznab quirks.

The machine-readable adapter contract registry is
`ADAPTER_CONTRACT_ROUTES` in `repos/emulebb-build-tests/scripts/rest-api-smoke.py`.
It is generated from the qBittorrent route seam and Torznab route/parser seams,
then tested against this document and the live adapter stress probes.

The deprecated legacy template-based WebServer UI is frozen and compile-only
until removal. It is not an adapter contract, no functional HTML/template
behavior is supported, and no adapter or release campaign may add
template-specific tests for 0.7.3 RC1.

## qBittorrent-Compatible `/api/v2`

`/api/v2` is an Arr download-client compatibility subset, not a full
qBittorrent Web API clone. It uses qBittorrent-shaped content types, text
responses, session cookies, and form bodies where Arr clients expect them, but
the accepted acquisition payload is still eMuleBB's native eD2K model.
qBittorrent-compatible paths are matched case-insensitively after URL path
validation, so canonical qBittorrent spellings such as `webapiVersion`,
`createCategory`, `setCategory`, and `setForceStart` are accepted alongside the
lowercase-normalized routes listed below.

Reference surface used for compatibility decisions:

- qBittorrent Web API wiki, especially application, auth, and torrent routes:
  <https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-%28qBittorrent-4.1%29>
- Radarr qBittorrent download client schema fields as exposed by
  `/api/v3/downloadclient/schema`.

Supported routes:

| Method | Route | Auth | Contract role |
|---|---|---|---|
| `GET` | `/api/v2/app/webapiversion` | no | Public qBit Web API version probe. |
| `POST` | `/api/v2/auth/login` | no | Form login with username `emule` and the configured eMuleBB API key as password. |
| `GET` | `/api/v2/app/version` | yes | App version probe. |
| `GET` | `/api/v2/app/preferences` | yes | Minimal preference payload for Arr client tests. |
| `GET` | `/api/v2/torrents/categories` | yes | Category map. |
| `POST` | `/api/v2/torrents/createcategory` | yes | Create a native category from qBit form field `category`. |
| `GET` | `/api/v2/torrents/info` | yes | Transfer list, optionally filtered by `category`. |
| `GET` | `/api/v2/torrents/properties` | yes | One transfer's qBit-shaped properties by `hash`. |
| `GET` | `/api/v2/torrents/files` | yes | One transfer's qBit-shaped file list by `hash`. |
| `POST` | `/api/v2/torrents/add` | yes | Add one Torznab-emitted eD2K link or controlled eMuleBB magnet. |
| `POST` | `/api/v2/torrents/delete` | yes | Delete/cancel transfers by `hashes`. |
| `POST` | `/api/v2/torrents/setcategory` | yes | Assign a native category by `hashes` and `category`. |
| `POST` | `/api/v2/torrents/pause` | yes | Pause transfers by `hashes`. |
| `POST` | `/api/v2/torrents/stop` | yes | Stop transfers by `hashes`. |
| `POST` | `/api/v2/torrents/resume` | yes | Resume transfers by `hashes`. |
| `POST` | `/api/v2/torrents/start` | yes | Start/resume transfers by `hashes`. |
| `POST` | `/api/v2/torrents/setsharelimits` | yes | Accepted no-op for Arr compatibility. |
| `POST` | `/api/v2/torrents/topprio` | yes | Accepted no-op for Arr compatibility. |
| `POST` | `/api/v2/torrents/setforcestart` | yes | Accepted no-op after validating `hashes` and optional boolean `value`. |

Compatibility summary:

| Area | Status | Notes |
|---|---|---|
| App/auth probes | Supported | Enough for Arr qBittorrent client setup and health checks. |
| Categories | Supported | Native eMuleBB categories are exposed through qBit-shaped routes. |
| Transfer list/details | Supported subset | Rows are shaped for Arr queue and completed-download handling. |
| Add transfer | Supported subset | Accepts eD2K links and controlled eMuleBB magnets. |
| Pause/resume/delete | Supported subset | `delete` maps to native destructive transfer-file deletion semantics. |
| Priority/share-limit/force-start | Accepted no-op | Validated for Arr compatibility; no torrent seeding policy exists. |
| RSS/search/tracker/peer/sync/log APIs | Unsupported | These qBittorrent families are outside the adapter contract. |
| `hashes=all` | Unsupported | Hash mutations require one to 100 explicit eD2K hashes. |

For add-transfer calls, raw eD2K links are accepted. Torznab emits BTIH-shaped
magnets with `x.emulebb-ed2k` so Arr validates them as torrent-style links while
eMuleBB converts them back to eD2K. `.torrent` uploads, unrelated BitTorrent
magnet links, and HTTP torrent URLs are rejected.

- **`GET`**
  - Route: `/api/v2/app/webapiversion`
  - Auth: no
  - Contract role: Public qBit Web API version probe.

- **`POST`**
  - Route: `/api/v2/auth/login`
  - Auth: no
  - Contract role: Form login with username `emule` and the configured eMuleBB
                   API key as password.

- **`GET`**
  - Route: `/api/v2/app/version`
  - Auth: yes
  - Contract role: App version probe.

- **`GET`**
  - Route: `/api/v2/app/preferences`
  - Auth: yes
  - Contract role: Minimal preference payload for Arr client tests.

- **`GET`**
  - Route: `/api/v2/torrents/categories`
  - Auth: yes
  - Contract role: Category map.

- **`POST`**
  - Route: `/api/v2/torrents/createcategory`
  - Auth: yes
  - Contract role: Create a native category from qBit form field `category`.

- **`GET`**
  - Route: `/api/v2/torrents/info`
  - Auth: yes
  - Contract role: Transfer list, optionally filtered by `category`; rows include Arr
                   import fields such as `save_path` and `content_path` from the native
                   category path.

- **`GET`**
  - Route: `/api/v2/torrents/properties`
  - Auth: yes
  - Contract role: One transfer's qBit-shaped properties by `hash`, including path,
                   size, progress, and seeding-time fields consumed by Arr completed
                   download handling.

- **`GET`**
  - Route: `/api/v2/torrents/files`
  - Auth: yes
  - Contract role: One transfer's qBit-shaped file list by `hash`, including file
                   `name`, `size`, and `progress`.

- **`POST`**
  - Route: `/api/v2/torrents/add`
  - Auth: yes
  - Contract role: Add one Torznab-emitted eD2K link or controlled eMuleBB magnet;
                   accepts Arr qBit form fields that eMule ignores after validation.
                   Controlled magnets use a padded BTIH value plus `x.emulebb-ed2k`
                   to survive Prowlarr/Radarr torrent validation before eMuleBB
                   converts the request back to native eD2K. `.torrent` uploads,
                   unrelated BitTorrent magnet links, and HTTP torrent URLs are
                   rejected because this adapter keeps qBit-shaped automation on
                   eMuleBB's native eD2K acquisition model.

- **`POST`**
  - Route: `/api/v2/torrents/delete`
  - Auth: yes
  - Contract role: Delete/cancel transfers by `hashes`; always maps to native
                   destructive transfer-file deletion semantics.

- **`POST`**
  - Route: `/api/v2/torrents/setcategory`
  - Auth: yes
  - Contract role: Assign a native category by `hashes` and `category`.

- **`POST`**
  - Route: `/api/v2/torrents/pause`
  - Auth: yes
  - Contract role: Pause transfers by `hashes`.

- **`POST`**
  - Route: `/api/v2/torrents/stop`
  - Auth: yes
  - Contract role: Stop transfers by `hashes`.

- **`POST`**
  - Route: `/api/v2/torrents/resume`
  - Auth: yes
  - Contract role: Resume transfers by `hashes`.

- **`POST`**
  - Route: `/api/v2/torrents/start`
  - Auth: yes
  - Contract role: Start/resume transfers by `hashes`.

- **`POST`**
  - Route: `/api/v2/torrents/setsharelimits`
  - Auth: yes
  - Contract role: Accepted no-op for Arr compatibility after validating `hashes`,
                   `ratioLimit`, `seedingTimeLimit`, and `inactiveSeedingTimeLimit`.

- **`POST`**
  - Route: `/api/v2/torrents/topprio`
  - Auth: yes
  - Contract role: Accepted no-op for Arr compatibility after validating `hashes`.

- **`POST`**
  - Route: `/api/v2/torrents/setforcestart`
  - Auth: yes
  - Contract role: Accepted no-op after validating `hashes` and optional boolean
                   `value`.

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

- **`t`**
  - Contract: `caps`, `search`, `tvsearch`, or `movie`; missing or empty defaults to
              `search`.

- **`apikey`**
  - Contract: Optional query API key. If omitted, `X-API-Key` may authenticate the
              request.

- **`q`**
  - Contract: Search text, normalized through native REST search validation.

- **`cat`**
  - Contract: Comma-separated Torznab categories mapped to native eMule file families.

- **`season`, `ep`, `year`**
  - Contract: Optional unsigned decimal filters bounded to `0..9999`.

- **`offset`, `limit`**
  - Contract: Optional unsigned decimal paging controls. `limit` is bounded to `0..100`,
              with `0` using the default `100`; `offset` is bounded to `0..1000000`.
              Non-zero offsets page only a cached first-page result set for the same
              normalized query, category, media family, and native method set. If no
              cached result set exists, the adapter returns an empty accepted feed
              instead of launching a new native search for that later page.

Unknown Torznab/Newznab extension query parameters are ignored after strict URL
decoding and duplicate-name rejection. This keeps compatibility with Arr-family
clients that send provider-specific IDs while still rejecting malformed escapes,
duplicate parameters after lowercase normalization, unsupported `t` values, and
invalid numeric fields.

Result download links are valid BitTorrent-infohash-shaped magnets for Arr
compatibility: `xt=urn:btih:<32-hex-ed2k-md4>00000000`, `dn`, `xl`, and
`x.emulebb-ed2k=<32-hex-ed2k-md4>`. The padded BTIH shape lets Prowlarr/Radarr
accept and proxy the result as a torrent-style release. The qBittorrent-compatible
adapter requires the matching `x.emulebb-ed2k` value and then converts the request
back into the native `ed2k://|file|...|/` link.

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

Operational timing:

| Search family | Observation window | Why |
|---|---:|---|
| Generic search | 12 seconds | Keeps interactive Torznab tests bounded. |
| Movie and TV search | 45 seconds | Allows the adapter to combine broader video results across networks. |

Only one live bridge search should be active for the same adapter path at a
time. When the bridge is still busy and no useful cached page exists, clients
receive `503 application/xml`. Non-zero `offset` pages reuse a cached first-page
result set and do not launch a new native search.
