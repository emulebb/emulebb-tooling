# emulebb-rust TODO

Last reviewed: 2026-07-14

This note captures the remaining Rust profile/settings naming cleanup found
after the `--profile`, `emulebb-rust-settings.toml`,
`emulebb-rust-metadata.db`, and `/api/v1/app/settings` alignment work.

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

## To Be Reviewed / Implemented

### Rust build-test harness profile alignment

Owner repo: `repos/emulebb-build-tests`

- Replace `write_rust_config(...)` with a profile-oriented helper such as
  `write_rust_profile(...)`.
- The helper should create the profile directory, write
  `emulebb-rust-settings.toml` with only REST bind/authentication bootstrap
  fields, and seed `emulebb-rust-metadata.db`.
- Seed settings into the DB using the Rust metadata schema and canonical section
  names such as `core`, `daemon`, `ed2k`, `kad`, `nat`, `vpn.guard`, and
  `ip.filter`.
- Seed server rows into the Rust DB `servers` table instead of writing server
  lists to TOML.
- Launch Rust daemon paths with `--profile <profile-dir>`, not `--config`.
- Rename local harness variables from `runtime_dir` to `profile_dir` where the
  value is the Rust profile root.

Known files to review:

- `emule_test_harness/rust_client.py`
- `emule_test_harness/rust_metadata.py`
- `tests/python/test_emulebb_rust_local_client.py`

### Rust REST test and smoke route alignment

Owner repo: `repos/emulebb-build-tests`

- Replace Rust `/api/v1/app/preferences` calls with
  `/api/v1/app/settings`.
- Update PATCH payloads to the canonical settings shape, including nested
  `core` settings where applicable.
- Remove old `downloadAutoBroadbandIo` usage from Rust-native tests.
- Keep `/api/v2/app/preferences` only where it belongs to non-Rust compatibility
  surfaces.

Known files to review:

- `tests/python/test_emulebb_rust_local_client.py`
- `scripts/rest-api-smoke.py`
- `manifests/release-live-wire-golden.v1.json`

### Soak and live harness naming alignment

Owner repo: `repos/emulebb-build-tests`

- Replace Rust profile contract names:
  - `runtimeDir` -> `profileDir`
  - `metadata.sqlite` -> `emulebb-rust-metadata.db`
  - `emulebb-rust.toml` -> `emulebb-rust-settings.toml`
- Update Rust soak launch/control paths to pass `--profile`.
- Do not rename unrelated MFC, qBittorrentBB, or build-system `--config`
  concepts.

Known files to review:

- `emule_test_harness/soak_launch.py`
- `scripts/rust-soak-control.py`
- `scripts/converged-soak-live.py`

### Rust repo wording cleanup

Owner repo: `repos/emulebb-rust`

- Change user-facing `core_settings` error text to `settings.core` or another
  explicit canonical settings path.
- Replace metadata tests that use `"core.core_settings"` with `"core"` or a
  neutral non-legacy section name.
- Replace comments that describe Rust live settings as "preferences" with
  "settings".
- Do not change stock eMule references such as `CPreferences`, `thePrefs`, or
  `preferences.dat`.

Known files to review:

- `crates/emulebb-core/src/network_api.rs`
- `crates/emulebb-core/src/kad_control.rs`
- `crates/emulebb-metadata/src/profile_store.rs`
- `crates/emulebb-core/src/ed2k_transfer.rs`
- `crates/emulebb-core/src/download_coordinator.rs`
- `crates/emulebb-core/src/inbound_admission.rs`

### UI settings surface review

Owner repo: `repos/emulebb-rust`

- Confirm all important DB-backed Rust settings are reachable from the UI.
- VPN binding and guard controls must be visible and explicit.
- Server list UI must include disabled servers.
- Server enable/disable must be available from the list.
- The UI should make it clear that the client can connect to only one eD2K
  server at a time.

### Upload, speed, and I/O review

Owner repo: `repos/emulebb-rust`

- Review upload scheduling and bandwidth cap usage against stock/community
  behavior before changing performance-sensitive paths.
- Review read/write buffering and DB/file I/O hotspots for possible speed
  improvements.
- Treat every speed or I/O improvement as "to be reviewed" until protocol parity
  evidence exists.
- Do not alter wire semantics, queue behavior, slot behavior, packet shape, or
  peer/server visible behavior for optimization alone.

## Suggested Execution Order

1. Update build-test harness profile creation and Rust launch arguments.
2. Update Rust REST tests, smoke checks, and manifests to `/app/settings`.
3. Update soak/live harness naming and Rust profile DB filename usage.
4. Apply Rust repo wording cleanup.
5. Review and extend UI settings controls only after the backend/test naming is
   consistent.
6. Review upload, speed, and I/O improvements separately with protocol-parity
   evidence.

## Validation Expectations

- For `repos/emulebb-build-tests`, run the focused Python tests covering the
  changed Rust harness and smoke paths.
- For `repos/emulebb-rust`, set `CARGO_TARGET_DIR` to
  `EMULEBB_WORKSPACE_OUTPUT_ROOT/builds/rust/target` and run the smallest
  relevant `cargo test` set plus `python tools/rust_quality_gate.py quick` when
  Rust code is touched.
- Keep commits granular by repo and concern.
