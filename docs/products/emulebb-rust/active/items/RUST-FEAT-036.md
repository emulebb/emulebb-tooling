---
id: RUST-FEAT-036
workflow: local
title: Settings UI v2 - shared schema, startup config, and beta-ready settings coverage
status: OPEN
priority: Critical
category: feature
labels: [settings, preferences, rest, ui, beta, configuration]
milestone: release-0.1.0-beta.1
created: 2026-07-13
source: operator direction after RUST-FEAT-SETTINGS shared preference schema slice
---

# RUST-FEAT-036 - Settings UI v2

## Summary

Make the Rust daemon settings surface beta-ready without turning it into a
legacy preference mirror. `emulebb-preferences` now owns the live preference
schema and `/api/v1/app/preferences/schema` exposes it. The next step is to
finish the Settings product surface: live preferences, startup/network/security
configuration, and existing settings-adjacent resources must appear in one
coherent Rust-native UI.

## Product Rule

Do not force every setting into `Preferences`.

- `/api/v1/app/preferences` is for live daemon preferences that can be applied
  and persisted through the running core.
- Startup/network/security configuration needs an explicit restart-required
  settings resource, not hidden live-preference fields.
- Existing resources such as shared directories, categories, servers, and Kad
  operations are settings sections in the UI, not duplicate preference keys.
- Protocol parity remains mandatory for eD2K/Kad behavior; local REST/UI shape
  should stay Rust-native and clean.

## Current Exposed Live Preferences

The shared `PREFERENCE_SPECS` table currently covers:

- transfer bandwidth and connection budgets: `uploadLimitKiBps`,
  `downloadLimitKiBps`, `maxConnections`, `maxConnectionsPerFiveSeconds`,
  `maxSourcesPerFile`;
- upload queue policy: `uploadClientDataRate`, `maxUploadSlots`,
  `uploadSlotElasticPercent`, `queueSize`;
- server behavior: `autoConnect`, `reconnect`, `safeServerConnect`,
  `addServersFromServer`;
- protocol toggles: `networkKademlia`, `networkEd2k`;
- safety/scoring: `creditSystem`.

This is the correct live-preference base, but it is not the whole beta settings
surface.

## Missing Beta-Facing Settings

These must be exposed before beta, either as live preferences or as explicit
restart-required/startup settings:

- `incomingDir` - global completed-download directory.
- Shared directories - already supported by REST; must be managed in the
  Settings UI as a primary section.
- Categories and category paths - already supported by REST; must be managed in
  Settings UI with clear path semantics.
- eD2K listen port and Kad listen port - startup/network settings,
  restart-required.
- P2P bind IP/interface - setup/network safety setting, restart-required.
- VPN Guard - enabled, mode, allowed public CIDRs, current verdict/status.
- IP filter - enabled, path, level, reload/status.
- REST bind/API key - setup/security section, restart-required and handled
  carefully.
- Server bootstrap list/import - existing server routes should become a clear
  settings section.
- Kad bootstrap nodes/import - existing Kad routes should become a clear
  settings section.

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

## Config-Only For Now

Do not put these in the normal Settings UI for beta:

- `runtimeDir`.
- Internal transfer/piece-store paths.
- Low-level Kad index capacities unless an explicit diagnostics mode needs them.
- Diagnostic probe terms and parity-harness knobs.
- Identity spoof/advertising toggles.

## Execution Plan

1. **Backend inventory**
   - Add a machine-readable settings inventory that maps each daemon config knob
     to one of: live preference, startup setting, settings section resource,
     advanced setting, or config-only.
   - Add a policy/test guard so beta-facing config fields cannot be forgotten
     when `DaemonConfig`, `Ed2kConfig`, `KadListenerConfig`, `VpnGuardSettings`,
     or `IpFilterSettings` changes.

2. **Startup settings contract**
   - Add a Rust-native REST resource for restart-required settings, for example
     `/api/v1/app/startup-settings` or `/api/v1/settings/startup`.
   - Include schema metadata with `restartRequired: true`, validation, and clear
     persistence behavior.
   - Do not pretend restart-required settings are live-applied.

3. **Settings section routing**
   - Treat existing routes as settings sections:
     `/shared-directories`, `/categories`, `/servers`, `/kad`, and diagnostics
     or status endpoints where relevant.
   - Avoid duplicating those resources inside `Preferences`.

4. **UI schema consumption**
   - Fetch `/api/v1/app/preferences/schema` and current values.
   - Render grouped controls from schema metadata.
   - Add dirty state, inline validation, reset field/defaults, save/revert, and
     restart-required indicators.
   - Add an advanced toggle and keep advanced controls out of the normal flow.

5. **Beta settings coverage**
   - Add Settings UI sections for downloads/storage, sharing, categories,
     servers, Kad, network/binding, VPN Guard, IP filter, REST/security, and
     advanced tuning.
   - Every visible control must call a real API or clearly show that restart is
     required. No inert fields.

6. **Validation**
   - Shared preference schema tests cover defaults, keys, groups, and bounds.
   - Startup settings schema tests cover restart-required fields.
   - REST route tests prove invalid fields and invalid values fail from shared
     validators.
   - UI compile/tests prove every schema kind and section renders.
   - OpenAPI conformance includes preferences, startup settings, and section
     resources.

## Acceptance Criteria

- [ ] All beta-facing settings above are represented in live preferences,
      startup settings, or an existing section resource.
- [ ] No beta-facing setting is hidden only in TOML unless this item explicitly
      classifies it as config-only.
- [ ] UI uses schema metadata for live preferences instead of hardcoded labels,
      groups, ranges, and restart flags.
- [ ] Startup settings are explicit, validated, persisted, and marked
      restart-required.
- [ ] Existing settings-adjacent resources are reachable from the Settings UI.
- [ ] No inert compatibility fields or legacy preference names are introduced.
- [ ] REST OpenAPI matches implementation and test coverage.

## Next Implementation Slice

Start with the backend inventory and startup settings contract:

1. classify every current daemon config field;
2. add the restart-required settings schema/resource;
3. test it against `DaemonConfig` and OpenAPI;
4. only then wire the UI.
