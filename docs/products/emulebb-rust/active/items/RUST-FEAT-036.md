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
  but do not block the UI on a schema-driven renderer.
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
- Shared directories: already supported by REST; manage as a primary section.
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
