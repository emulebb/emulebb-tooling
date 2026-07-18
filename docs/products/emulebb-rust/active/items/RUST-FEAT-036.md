---
id: RUST-FEAT-036
workflow: local
title: Settings UI v2 - profile settings and beta-ready controls
status: OPEN
priority: Critical
category: feature
labels: [settings, rest, ui, beta, profile]
milestone: release-0.1.0-beta.1
created: 2026-07-13
source: operator direction after Rust profile/settings consolidation
---

# RUST-FEAT-036 - Settings UI v2

## Summary

Make the Rust daemon settings surface beta-ready without turning it into a
legacy preference mirror. The canonical model is:

- `--profile <dir>` selects the profile directory.
- `<dir>/emulebb-rust-settings.toml` is bootstrap-only and owns REST bind/auth.
- `<dir>/emulebb-rust-metadata.db` is the SQLite profile repository.
- `emulebb-settings` owns typed settings DTOs, defaults, and validation helpers.
- `/api/v1/app/settings` exposes DB-backed daemon settings.

There are no compatibility aliases, old-name remaps, schema migrations, or
version bumps for development-phase cleanup. If an operator-local profile must
be preserved during development, update that local SQLite file explicitly.

## Product Rule

Do not split the product into hidden preferences/config/settings surfaces.

- User-facing daemon settings live in SQLite and are exposed through
  `/api/v1/app/settings`.
- REST bind/auth stays in the fixed bootstrap TOML because the REST server needs
  it before it can serve the settings API.
- Existing resources such as shared directories, categories, servers, and Kad
  operations are settings sections in the UI, not duplicate setting keys.
- The UI should use regular, explicit controls. Reuse `emulebb-settings`
  validation/default metadata where it is already available or simple to add,
  but do not block the UI on a generic metadata renderer.
- Protocol parity remains mandatory for eD2K/Kad behavior; local REST/UI shape
  should stay Rust-native and clean.

## Current DB-Backed Settings

`AppSettings` currently exposes:

- `core`: bandwidth, connection budgets, upload queue policy, server behavior,
  protocol toggles, and credit-system behavior.
- `daemon`: incoming directory, P2P bind IP/interface, and eD2K user hash.
- `ed2k`: listen port, obfuscation, timeouts, reconnect policy, source budgets,
  upload queue tuning, download limit, UDP reask, identity advertisement, server
  import behavior, and dead-server retry budget.
- `kad`: listen port, local-store behavior, publishing, firewall checks, buddy,
  routing maintenance, and snoop-queue tuning.
- `nat`: UPnP/NAT behavior.
- `vpnGuard`: VPN guard mode and allow-list.
- `ipFilter`: IP filter enable/path/level.

## Missing Beta-Facing Controls

Expose these before beta through regular Settings UI controls or existing
section resources:

- Downloads/storage: `incomingDir` and related path validation.
- Sharing: manage shared folder roots as a primary section. Every root is a
  monitored folder tree; do not expose single-file sharing or a non-recursive
  sharing mode.
- Categories and category paths: already supported by REST; manage with clear
  path semantics.
- eD2K listen port and Kad listen port: settings that require restart or
  explicit reconnect where live apply is not available.
- P2P bind IP/interface: network safety setting, restart-required unless live
  rebind is implemented.
- VPN Guard: enabled, mode, allowed public CIDRs, and current verdict/status.
- IP filter: enabled, path, level, reload/status.
- REST bind/API key: bootstrap security section, restart-required, backed by the
  fixed profile TOML.
- Server repository/import: existing server routes as a clear settings section
  backed by SQLite.
- Kad bootstrap nodes/import: existing Kad routes as a clear settings section.

## Advanced Settings

Expose only behind an advanced section if they are surfaced for beta:

- Kad shared-file publishing toggle.
- Kad republish interval.
- Kad UDP/TCP firewall check toggles and intervals.
- Kad buddy and routing-maintenance toggles.
- Kad local-store capacities/TTLs.
- Kad snoop-queue tuning.
- eD2K dead server retries.
- Server keepalive/session rotation.
- UDP source reask toggle.
- NAT/UPnP backend settings.

## Profile-Only / Not Normal UI

Do not put these in the normal Settings UI for beta:

- The profile directory itself.
- The fixed profile file names.
- Internal transfer/piece-store paths.
- Low-level Kad index capacities unless an explicit diagnostics mode needs them.
- Diagnostic probe terms and parity-harness knobs.
- Identity spoof/advertising toggles.

## Execution Plan

1. **Settings inventory**
   - Keep a machine-readable inventory of every beta-facing setting and classify
     it as normal control, advanced control, existing section resource,
     bootstrap-only, or not-user-facing.
   - Add a policy/test guard so beta-facing fields cannot be forgotten when
     `DaemonProfile`, `AppSettings`, `Ed2kSettings`, `KadSettings`,
     `VpnGuardSettings`, or `IpFilterSettings` changes.

2. **REST settings contract**
   - Keep `/api/v1/app/settings` as the canonical DB-backed settings resource.
   - Keep OpenAPI aligned with implementation in the same change.
   - Do not document or keep unimplemented schema routes.

3. **Settings section routing**
   - Treat existing routes as settings sections:
     `/shared-directories`, `/categories`, `/servers`, `/kad`, and diagnostics
     or status endpoints where relevant.
   - Avoid duplicating those resources inside `AppSettings`.

4. **Regular UI controls**
   - Bind explicit UI controls to `AppSettings` and existing section routes.
   - Add dirty state, inline validation, save/revert, and restart-required
     indicators.
   - Add an advanced toggle and keep advanced controls out of the normal flow.

5. **Beta settings coverage**
   - Add Settings UI sections for downloads/storage, sharing, categories,
     servers, Kad, network/binding, VPN Guard, IP filter, REST/security, and
     advanced tuning.
   - Every visible control must call a real API or clearly show that restart is
     required. No inert fields.

6. **Validation**
   - `emulebb-settings` tests cover defaults, field names, bounds, and update
     validation.
   - REST route tests prove invalid fields and invalid values fail from shared
     validators.
   - UI compile/tests prove every visible settings section renders.
   - OpenAPI conformance includes `/api/v1/app/settings` and the section
     resources used by the UI.

## Acceptance Criteria

- [ ] All beta-facing settings above are represented in `AppSettings`,
      bootstrap TOML, or an existing section resource.
- [ ] No beta-facing setting is hidden only in TOML except REST bind/auth.
- [ ] UI uses regular controls backed by real APIs.
- [ ] Restart-required settings are explicit and cannot be mistaken for
      live-applied settings.
- [ ] Existing settings-adjacent resources are reachable from the Settings UI.
- [ ] No inert compatibility fields or legacy preference names are introduced.
- [ ] REST OpenAPI matches implementation and test coverage.

## Implementation Notes

- 2026-07-18: Added scan-friendly Diagnostics summary metrics in the embedded
  WebUI for process, file counts, shared hashing/reload progress, upload counts,
  and eD2K/Kad publish phases while preserving the raw runtime JSON panel for
  deep inspection.
- 2026-07-18: Marked shadowed `ed2k.safeServerConnect` and
  `ed2k.addServersFromServer` settings surface entries as not-user-facing, with
  a guard test. The visible Settings controls remain the canonical `core.*`
  server toggles used by runtime state.
- 2026-07-18: Added an advanced WebUI Search settings section for existing
  eD2K keyword, exact-hash keyword, and source server attempt budgets. The
  controls PATCH the existing `ed2k` settings object and stay hidden until
  Advanced is enabled.
- 2026-07-18: Added advanced WebUI controls for existing eD2K network budget
  settings: new outgoing connections per five seconds and half-open connection
  cap. Labels intentionally distinguish these protocol-level caps from the
  higher-level `core` connection controls.
- 2026-07-18: Added advanced WebUI controls for existing eD2K transfer tuning:
  session rotation, concurrent download cap, eD2K source cap, parallel download
  peer cap, and startup download byte budget. These PATCH the existing `ed2k`
  settings section and keep labels distinct from the higher-level `core` caps.
- 2026-07-18: Added an advanced WebUI Uploads section for existing
  `ed2k.uploadQueue` tuning settings: startup slots, elasticity, byte budgets,
  underfill thresholds, waiting/granted/upload timeouts, session transfer target,
  and session time limit. The controls PATCH the nested `ed2k.uploadQueue`
  settings object.
- 2026-07-18: Added advanced WebUI controls for existing Kad tuning settings:
  bootstrap contact floor, local-store enable, publish contact fanout, and UDP/TCP
  firewall-check intervals. Low-level Kad store capacities, TTLs, and snoop queue
  fields remain not-user-facing per the settings surface inventory.
- 2026-07-18: Added advanced WebUI controls for existing NAT tuning settings:
  pinned IGD IP, miniSSDPd socket, SSDP local port, discovery timeout, lease
  duration, renew margin, and external IP override. These stay behind the
  Advanced toggle and PATCH the existing `nat` settings section.
- 2026-07-18: Added advanced WebUI controls for existing eD2K timeout and retry
  settings: peer connect timeout, server connect timeout, callback timeout,
  reconnect interval, keepalive interval, and dead-server retries. These stay
  behind the Advanced toggle and PATCH the existing `ed2k` settings section.
- 2026-07-18: Reworked the WebUI Settings tab from a flat control grid into
  domain sections for Storage, Transfers, Network, Hostname Lookup, Servers, Kad,
  NAT, VPN Guard, and IP Filter. Each section still binds to real `AppSettings`
  fields and keeps metadata-driven advanced visibility, restart badges,
  validation, and save/revert behavior.
- 2026-07-18: Added inline WebUI validation for Settings numeric and listen-port
  controls. Invalid whole-number/range values now render field-level errors and
  disable Save before malformed `PATCH /api/v1/app/settings` requests can be
  sent; the settings e2e covers the invalid-port path.
- 2026-07-18: Added Settings-tab navigation for the existing section resources
  advertised by `GET /api/v1/app/settings/surface`, making Sharing,
  Categories, Servers, Kad, and Diagnostics reachable from Settings without
  duplicating those resources inside `AppSettings`. WebUI e2e coverage now
  proves the section-resource path opens a real section.
- 2026-07-18: Wired the embedded WebUI to `GET /api/v1/app/settings/surface`
  and used the metadata in the Settings view for advanced-control hiding,
  restart-required badges, dirty Save/Revert state, and e2e coverage of the
  operator flow.
- 2026-07-18: Exposed the DB-backed settings inventory through
  `GET /api/v1/app/settings/surface`. The route returns classified
  `/app/settings` field metadata and existing settings-section resources while
  keeping bootstrap-only TOML secrets out of REST. Rust route metadata, REST
  tests, and OpenAPI are aligned.
- 2026-07-18: Added a machine-readable settings surface inventory in
  `emulebb-settings` for all serialized `AppSettings` fields, plus existing
  settings-section resources. Added a daemon bootstrap TOML inventory for the
  REST bind/auth/WebUI-root fields. Tests now fail if either serialized settings
  field set grows without a classification.
- 2026-07-18: Added a first-class `GET /api/v1/diagnostics` power-user section
  resource. It exposes the same `RuntimeDiagnostics` object embedded in
  `GET /status`, with OpenAPI, route metadata, REST tests, WebUI model/refresh
  wiring, mock API coverage, and Diagnostics tab rendering aligned in the same
  slice.
- 2026-07-18: Added static OpenAPI drift coverage for destructive confirmation
  sentinels so operator actions such as shutdown, diagnostics capture/crash,
  log clearing, transfer clearing, and shared-root replacement remain documented
  as required explicit `true` confirmations.
- 2026-07-18: Tightened the embedded WebUI `AppSettings` API model from loose
  records to typed section shapes for core, daemon, eD2K, Kad, NAT, VPN Guard,
  and IP Filter settings. The Settings controls still use the same REST contract,
  but TypeScript now tracks the first-class fields that the UI edits.
- 2026-07-18: Added the IP Filter settings section resource. The Rust REST
  surface now exposes `GET /api/v1/ip-filter` for configured/reloadable status,
  level, and loaded range count, plus `POST /api/v1/ip-filter/operations/reload`
  to re-read the configured `ipfilter.dat` into the live shared filter. The
  Settings UI shows the runtime status and reload action next to the IP Filter
  controls, with OpenAPI and route/body validation aligned.
- 2026-07-18: Added redacted bootstrap REST/security inventory to
  `GET /api/v1/app/settings/surface` as `bootstrapSettings`. The Settings UI now
  shows the `rest.bindAddr`, `rest.apiKey`, and `rest.webRootDir` TOML-owned
  fields as restart-required Bootstrap REST entries without exposing secret
  values or making them mutable through REST.
- 2026-07-18: Tightened storage path validation for the beta Settings surface.
  `PATCH /api/v1/app/settings` now rejects empty `incomingDir` values before
  persistence and rejects existing non-directory incoming paths at the core
  boundary; shared-directory root replacement canonicalizes through the same
  long-path content boundary used by shared-tree scanning. OpenAPI documents
  `incomingDir` as a non-empty nullable path string.
- 2026-07-18: Added the VPN Guard settings section resource. The Rust REST
  surface now exposes `GET /api/v1/vpn-guard` for startup block state, egress
  verification, public IP, and bound STUN/HTTP probe outcomes; Settings renders
  the live verdict beside the existing VPN Guard controls without duplicating
  status inside `AppSettings`.
- 2026-07-18: Added the Network settings section resource. The Rust REST surface
  now exposes `GET /api/v1/network` for P2P port, bind-resolution, active
  interface, and nested VPN Guard status; Settings renders the live bind verdict
  beside restart-required P2P bind controls instead of duplicating runtime
  network status inside `AppSettings`.
- 2026-07-18: Added the NAT settings section resource. The Rust REST surface now
  exposes `GET /api/v1/nat` for gateway discovery, active mappings, observed
  external addresses, refresh time, and last error; Settings renders live mapping
  health beside restart-required NAT controls without duplicating manager state
  inside `AppSettings`.
- 2026-07-18: Tightened Settings section-resource reachability. In-page section
  resources such as NAT, VPN Guard, and IP Filter now focus their concrete
  Settings sections when opened from the advertised section-resource list, and
  the WebUI smoke covers those resource-button paths before navigating to
  Diagnostics.
- 2026-07-18: Added REST coverage proving every Settings section resource
  advertised by `GET /api/v1/app/settings/surface` resolves to an authenticated
  live REST v1 GET route and returns a `data` envelope, so future section
  resources cannot remain UI-only or docs-only links.
- 2026-07-18: Extended the Rust OpenAPI static route checker to parse
  `SETTINGS_SECTION_RESOURCES` from `emulebb-settings` and fail when an
  advertised Settings section resource is not documented as a GET operation in
  the Rust OpenAPI artifact.
- 2026-07-18: Tightened Settings section-resource OpenAPI response shapes. The
  static checker now rejects generic or inline section-resource success schemas
  and requires each advertised Settings section resource to expose a named
  closed `data` DTO; category, shared-directory, and server collection envelopes
  now reference named `CategoryList`, `SharedDirectoryList`, and `ServerList`
  DTO schemas without changing the wire shape.
- 2026-07-18: Added a VPN Guard power-user probe operation. The Rust REST
  surface now exposes `POST /api/v1/vpn-guard/operations/probe`, which runs the
  bound dual-plane egress probe when the runtime has a probeable VPN Guard CIDR
  gate and returns the refreshed `VpnGuardStatus` envelope. The Settings UI now
  offers the same probe action beside the VPN Guard controls.
- 2026-07-18: Added a NAT power-user refresh operation. The Rust REST surface
  now exposes `POST /api/v1/nat/operations/refresh`, which asks the live NAT
  manager for one reconcile pass and returns the refreshed `NatStatus` envelope.
  Mapping failures stay diagnostic by landing in `lastError`, so the Settings UI
  can show the live gateway/mapping result without treating a missing IGD as a
  transport-level API failure.
- 2026-07-18: Added Logs to the advertised Settings section resources. The
  existing `GET /api/v1/logs` and `POST /api/v1/logs/operations/clear` operator
  surface is now discoverable from `GET /api/v1/app/settings/surface`, and the
  Settings UI opens the existing Logs tab instead of duplicating retained log
  state inside `AppSettings`.
- 2026-07-18: Added `GET /api/v1/events/status` as an adapter-friendly live
  event-stream diagnostics resource. Controllers can now inspect SSE capacity,
  subscriber count, queued events, and cursor state without opening the
  long-lived stream or fetching full runtime diagnostics; capabilities advertise
  this as `transfers.sse.status`.
- 2026-07-18: Tightened `PATCH /api/v1/app/settings` semantics to be true
  field-level partial updates for every non-core settings section. Power-user
  scripts can now change one NAT, Kad, eD2K, daemon, VPN Guard, or IP Filter
  field without accidentally restoring omitted fields to defaults; explicit JSON
  `null` still clears nullable fields. OpenAPI now documents named
  `*SettingsUpdate` request DTOs separately from full settings response DTOs.
- 2026-07-18: Aligned the embedded WebUI with the partial settings PATCH
  contract. The Settings save path now builds sparse `AppSettingsUpdate`
  payloads from changed form fields only, and no longer sends the shadowed
  not-user-facing eD2K server toggles when saving the canonical `core.*`
  controls. WebUI e2e coverage asserts the exact sparse payload.
- 2026-07-18: Tightened REST body validation for the partial settings PATCH
  contract. Empty top-level settings updates, empty section update objects, and
  empty nested update objects such as `daemon.hostnameLookup` and
  `ed2k.uploadQueue` now fail before the handler, matching the OpenAPI
  `minProperties` contract.
- 2026-07-18: Tightened REST body validation for non-core partial settings
  updates. Unknown fields inside `daemon`, `ed2k`, `kad`, `nat`, `vpnGuard`,
  `ipFilter`, and nested update objects now fail in the route-body layer with
  deterministic `unknown settings.<path> field` errors, matching the OpenAPI
  closed-object contract before serde or handler parsing.
- 2026-07-18: Tightened hostname lookup settings update validation. The REST
  body layer now rejects `daemon.hostnameLookup.cacheTtlSecs` and
  `maxLookupsPerTick` values below `1`, plus `tickIntervalSecs` values below
  `5`, matching the OpenAPI minima before settings are persisted.
- 2026-07-18: Tightened VPN Guard mode as a finite Rust-native settings enum.
  The default DB-backed setting now uses `off`, OpenAPI documents `off` and
  `block`, REST PATCH rejects other mode strings before persistence, and the
  embedded WebUI renders the mode as a selector instead of a free text field.
- 2026-07-18: Tightened Kad settings update validation for values that the
  runtime previously clamped after persistence. REST PATCH and OpenAPI now
  require `bootstrapMinRoutingContacts`, `republishIntervalSecs`, and
  `publishContactFanout` to be at least `1`, and Kad UDP/TCP firewall check
  intervals to be at least `60` seconds. The embedded Settings UI uses the same
  floors before saving.
- 2026-07-18: Tightened configured port settings so REST PATCH and OpenAPI reject
  `0` for eD2K listen, Kad listen, and NAT SSDP local ports while preserving
  JSON `null` as the explicit clear value. The Settings UI already used the same
  `1..65535` range.
- 2026-07-18: Tightened the API-only Kad local-store and snoop-queue controls so
  REST PATCH and OpenAPI reject `0` for TTL, capacity, rate-budget, cooldown,
  deduplication, and stop-after-results fields. These values were already
  clamped to `1` by daemon construction; the contract now rejects ineffective
  writes before persistence.
- 2026-07-18: Aligned the embedded Settings UI with documented eD2K zero-policy
  controls. Advanced users can now save `0` for eD2K keepalive, concurrent
  download cap, new-connection rate cap, half-open cap, and per-file source cap,
  matching the REST/OpenAPI contract and runtime semantics for disabled or
  uncapped limits.
- 2026-07-18: Tightened eD2K min-one peer/search budgets. REST PATCH and OpenAPI
  now reject `0` for `maxParallelDownloadPeers`,
  `keywordServerAttemptBudget`, `exactHashKeywordServerAttemptBudget`, and
  `sourceServerAttemptBudget`, matching the runtime paths that already force
  those values to at least one effective attempt or peer.
- 2026-07-18: Tightened `ed2k.deadServerRetries` to the stock retry range.
  REST PATCH, OpenAPI, and the embedded Settings UI now require `1..10`, matching
  the eD2K runtime contract for non-static server removal after consecutive
  connect or ping failures.
- 2026-07-18: Tightened eD2K upload-queue settings around the runtime-effective
  bounds. REST PATCH and OpenAPI now reject clamped-away startup slot, elasticity,
  underfill, timeout, and session-transfer values, while the Settings UI now
  preserves zero-policy controls for an empty retained waiting queue, disabled
  session-transfer rotation, and disabled session-time rotation.
- 2026-07-18: Tightened NAT backend-order settings around the Rust-native backend
  set. REST PATCH, OpenAPI, and the embedded Settings UI now accept only
  `upnp_miniupnpc` entries while preserving an empty order as the runtime default
  order.
- 2026-07-18: Tightened NAT timing settings so REST PATCH and OpenAPI reject `0`
  for discovery timeout, lease duration, and renew margin. This matches the
  embedded Settings UI and prevents persisted values that the UPnP runtime clamps
  away during discovery or refresh scheduling.
- 2026-07-18: Tightened NAT address settings as nullable IPv4 strings. REST
  PATCH, OpenAPI, and the embedded Settings UI now reject malformed
  `nat.bindIp`, `nat.igdIp`, and `nat.externalIpOverride` values before the UPnP
  adapter has to reinterpret or fail them later.
- 2026-07-18: Tightened `daemon.p2pBindIp` PATCH handling to match its typed
  settings DTO and existing OpenAPI `ipv4` format. REST route-body validation and
  the embedded Settings UI now reject malformed bind-IP text before persistence.
- 2026-07-18: Tightened `daemon.ed2kUserHash` as a canonical eD2K identity
  override. REST PATCH and OpenAPI now require a marker-normalized
  32-character lowercase hex user hash, preserving `null` as the explicit clear
  value and rejecting values the daemon would otherwise normalize or reject at
  network bootstrap.
- 2026-07-18: Tightened nullable text/path settings that previously accepted
  ineffective empty strings. REST PATCH and OpenAPI now require non-empty
  `daemon.p2pBindInterface`, `nat.minissdpdSocket`, and `ipFilter.path` values
  when present, while preserving `null` as the explicit clear value.
- 2026-07-18: Tightened `vpnGuard.allowedPublicIpCidrs` to the core VPN Guard
  CIDR policy. REST PATCH, OpenAPI, and the embedded Settings UI now accept an
  empty string as "no CIDR gate" or a whitespace/comma/semicolon-separated list
  of public IPv4 CIDRs or host addresses; malformed, IPv6, and non-public ranges
  are rejected before persistence.
- 2026-07-18: Aligned the `NatStatus.ssdpLocalPort` response schema with the
  nullable configured-port contract. OpenAPI now advertises `null` or `1..65535`
  instead of allowing an impossible configured port `0`.
- 2026-07-18: Aligned the bulk transfer-add request schema with the REST link
  validator. OpenAPI now advertises the existing `links` ceiling of 100 eD2K
  links per request instead of only requiring a non-empty array.
- 2026-07-18: Tightened WebUI transfer-add link validation to match the REST and
  OpenAPI batch contract. The Transfers view now blocks non-eD2K, whitespace,
  overlong, and over-100-link batches before sending `POST /api/v1/transfers`.
- 2026-07-18: Tightened WebUI validation for core numeric settings to match the
  shared REST/OpenAPI core settings schema maxima. The Settings UI now rejects
  out-of-range power-user values such as `core.maxConnections` before sending a
  PATCH that the daemon would refuse.
- 2026-07-18: Aligned the category priority OpenAPI schema with the REST
  validator and Rust model. Numeric category priorities and category ids now
  advertise the `u32` ceiling instead of only documenting the lower bound.
- 2026-07-18: Tightened WebUI section-resource operation port validation.
  Server add and Kad bootstrap forms now enforce `1..65535` before sending
  requests, matching the REST/OpenAPI request contracts for those existing
  section resources.
- 2026-07-18: Tightened WebUI section-resource URL import validation. Server
  list and Kad nodes import forms now require HTTP(S) URLs with a host before
  sending requests, matching the shared `UrlImportRequest` REST/OpenAPI
  contract.
- 2026-07-18: Tightened WebUI friend-create validation. The Friends view now
  requires canonical lowercase eD2K user hashes and bounded display names before
  sending `POST /api/v1/friends`, matching the REST/OpenAPI request contract.
- 2026-07-18: Tightened WebUI category validation. Category create and row-edit
  controls now block empty names and unsupported priority values before sending
  `POST` or `PATCH` requests, while preserving the REST/OpenAPI string priority
  names and power-user numeric `u32` priority path.
- 2026-07-18: Aligned WebUI search creation with the Rust-native REST search
  type tokens. The Search view now sends `""`, `arc`, `doc`, `iso`, `image`,
  `pro`, `audio`, `video`, or `emulecollection` instead of unsupported friendly
  aliases, and normalizes/validates query text before `POST /api/v1/searches`.
- 2026-07-14: `RUST-FEAT-036 keep ED2K servers in SQLite profile` removed normal
  daemon TOML server ownership. Enabled SQLite profile servers decide whether an
  ED2K server session can be configured.
- 2026-07-14: Profile naming was consolidated around `--profile`,
  `emulebb-rust-settings.toml`, `emulebb-rust-metadata.db`,
  `/api/v1/app/settings`, and `emulebb-settings`.

## Next Implementation Slice

Start with the backend/UI inventory:

1. classify every current `AppSettings` and bootstrap TOML field;
2. decide normal vs advanced vs restart-required controls;
3. test it against OpenAPI and the UI;
4. then fill the missing Settings UI sections.
