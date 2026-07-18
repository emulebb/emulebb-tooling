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
