# emulebb-rust TODO

Last reviewed: 2026-07-15

This note tracks the remaining Rust profile/settings work after the
2026-07-15 harness/profile and wording cleanup commits.

## Standing Development Rules

- No compatibility shims, aliases, legacy names, remapping, dual reads, dual
  writes, or schema migrations during active Rust development.
- Assume a clean Rust profile by default: no existing DB, no existing settings,
  no legacy TOML, no legacy API contract.
- If an operator needs to keep a local persisted profile while a schema/name is
  changing, handle that profile with an explicit ad-hoc local SQL or Python
  update against the operator-owned DB. Do not encode that repair as product
  migration logic.
- The Rust TOML settings file is only bootstrap/control-plane configuration:
  REST bind and REST authentication. Product settings live in the profile DB.
- Canonical profile layout:
  - `--profile <profile-dir>`
  - `<profile-dir>/emulebb-rust-settings.toml`
  - `<profile-dir>/emulebb-rust-metadata.db`
- Canonical Rust REST settings endpoint:
  `/api/v1/app/settings`.
- Use `settings` for product/runtime settings. Use `config` only when referring
  to external TOML/bootstrap configuration or build configuration.
- Use regular UI controls for settings. Do not introduce a schema-rendered
  settings UI unless there is a separate explicit design decision.
- Protocol parity is mandatory. Upload, download, eD2K, and Kad behavior must
  stay stock/community-compatible unless an intentional compatibility exception
  is documented and accepted.

## Completed 2026-07-15

### Rust build-test harness profile alignment

Owner repo: `repos/emulebb-build-tests`

- Done: replaced `write_rust_config(...)` with a profile-oriented helper,
  `write_rust_profile(...)`.
- Done: the helper creates the profile directory, writes
  `emulebb-rust-settings.toml` with only REST bind/authentication bootstrap
  fields, and seeds `emulebb-rust-metadata.db`.
- Done: settings are seeded into the DB using the Rust metadata schema and
  canonical section names such as `core`, `daemon`, `ed2k`, `kad`, `nat`,
  `vpn.guard`, and `ip.filter`.
- Done: server rows are seeded into the Rust DB `servers` table instead of
  writing server lists to TOML.
- Done: Rust daemon paths launch with `--profile <profile-dir>`, not `--config`.
- Done: local harness variables were renamed from `runtime_dir` to `profile_dir` where the
  value is the Rust profile root.

Known files to review:

- `emule_test_harness/rust_client.py`
- `emule_test_harness/rust_metadata.py`
- `tests/python/test_emulebb_rust_local_client.py`

### Rust REST test and smoke route alignment

Owner repo: `repos/emulebb-build-tests`

- Done: replaced Rust `/api/v1/app/preferences` calls with
  `/api/v1/app/settings`.
- Done: updated PATCH payloads to the canonical settings shape, including nested
  `core` settings where applicable.
- Done: removed old `downloadAutoBroadbandIo` usage from Rust-native tests.
- Done: kept `/api/v2/app/preferences` only where it belongs to non-Rust compatibility
  surfaces.

Known files to review:

- `tests/python/test_emulebb_rust_local_client.py`
- `scripts/rest-api-smoke.py`
- `manifests/release-live-wire-golden.v1.json`

### Soak and live harness naming alignment

Owner repo: `repos/emulebb-build-tests`

- Done: replaced Rust profile contract names:
  - `runtimeDir` -> `profileDir`
  - `metadata.sqlite` -> `emulebb-rust-metadata.db`
  - `emulebb-rust.toml` -> `emulebb-rust-settings.toml`
- Done: updated Rust soak launch/control paths to pass `--profile`.
- Done: did not rename unrelated MFC, qBittorrentBB, or build-system `--config`
  concepts.

Known files to review:

- `emule_test_harness/soak_launch.py`
- `scripts/rust-soak-control.py`
- `scripts/converged-soak-live.py`

### Rust repo wording cleanup

Owner repo: `repos/emulebb-rust`

- Done: changed user-facing `core_settings` error text to `settings.core` or another
  explicit canonical settings path.
- Done: replaced metadata tests that use `"core.core_settings"` with `"core"` or a
  neutral non-legacy section name.
- Done: replaced comments that describe Rust live settings as "preferences" with
  "settings".
- Done: did not change stock eMule references such as `CPreferences`, `thePrefs`, or
  `preferences.dat`.

### UI settings surface review

Owner repo: `repos/emulebb-rust`

- Done: confirmed the Rust UI exposes the current DB-backed settings surface for
  core limits, daemon incoming/bind settings, eD2K, Kad, NAT, VPN Guard, and IP
  filter controls.
- Done: confirmed VPN binding and guard controls are visible and explicit.
- Done: kept server enable/disable available through the selected server form.
- Done: added a visible server-table `Enabled` column so disabled servers are
  visible in the list, not only in the selected-server detail.
- Done: changed the server summary to show the one-active-eD2K-server constraint
  as `N known | X/1 active | Y disabled`.

### Upload, speed, and I/O review

Owner repo: `repos/emulebb-rust`

- Done: reviewed upload scheduling and bandwidth cap usage against the current
  parity-oriented implementation.
- Done: reviewed read/write buffering and DB/file I/O hotspots.
- Done: made no code change from this review because the current code already
  has the important low-risk protections: bounded upload request ranges,
  per-fragment upload throttling, sliding-window upload rate meters, global
  download throttling, cached verified upload readers, cached download payload
  handles, targeted progress checkpoints, and batched credit/file-upload counter
  flushes.
- Future speed/I/O work must start from live CPU/I/O evidence and must not alter
  wire semantics, queue behavior, slot behavior, packet shape, or peer/server
  visible behavior for optimization alone.

## To Be Reviewed / Implemented

- No open profile/settings/UI/upload review item remains in this tracker as of
  2026-07-15. New Rust work should be added here as concrete, evidence-backed
  follow-up items.

## Suggested Execution Order

1. Collect live CPU/I/O evidence before opening any new speed or I/O optimization
   task.
2. Add each new Rust work item here as a concrete behavior, evidence, and
   validation target.

## Validation Expectations

- For `repos/emulebb-build-tests`, run the focused Python tests covering the
  changed Rust harness and smoke paths.
- For `repos/emulebb-rust`, set `CARGO_TARGET_DIR` to
  `EMULEBB_WORKSPACE_OUTPUT_ROOT/builds/rust/target` and run the smallest
  relevant `cargo test` set plus `python tools/rust_quality_gate.py quick` when
  Rust code is touched.
- Rust UI local process smoke should launch a REST-only daemon plus the native
  UI against `/api/v1`. On the operator split-tunnel workstation, bind the REST
  control plane to `X_LOCAL_IP` instead of loopback. The 2026-07-15 LAN-bound
  smoke passed against `http://X_LOCAL_IP:48731/api/v1`: the daemon served
  `/app`, `/app/settings`, and `/snapshot`, and the native UI process stayed live
  against that API.
- Keep commits granular by repo and concern.
