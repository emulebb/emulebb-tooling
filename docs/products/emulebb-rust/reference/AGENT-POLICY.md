# emulebb-rust Agent Policy

Read the [Workspace Policy](../../../WORKSPACE-POLICY.md) first. This annex is
mandatory only for `emulebb-rust` product, daemon, embedded WebUI, REST,
metadata, Cargo, or Rust protocol work.

## Product Direction

- `rust-v0.1.0-beta.2` is the active corrective release line. It is the active
  experimental product-development lane; beta is not a production-readiness
  claim. Do not rewrite published beta tags or artifacts.
- The Rust headless daemon and embedded SPA WebUI are the active client and UI.
  Slint/native UI is a frozen experiment unless the operator explicitly asks to
  remove or revive it.
- Preserve stock/community eD2K and Kad wire behavior, packet/tag shapes,
  opcodes, peer/server rules, network-identity persistence, and default network
  behavior. Rust REST, settings, scheduling, diagnostics, and UI are clean
  Rust-native async-daemon concepts, not MFC or legacy GUI mirrors.
- Broadband-oriented async I/O is the baseline, not a compatibility toggle.
  IPv6 remains parked and the protocol cores stay IPv4-only. Source Exchange is
  intentionally SX2-only; absent `OP_REQUESTSOURCES` and `OP_ANSWERSOURCES`
  live paths are not regressions.
- Protocol-adjacent changes require parity evidence through appropriate
  goldens, community baseline, tracing, live-diff, or packet captures.

`policy\rust-client.toml` and its omission registry are the machine-readable
authority for platform, protocol, long-path, and reviewed-omission policy.

## API And UI Contract

- The forward `/api/v1` contract under
  `docs\products\emulebb-rust\api` is authoritative. The frozen MFC REST
  contract is not a forward-compatibility constraint.
- Route or DTO changes evolve the daemon, OpenAPI, validators, embedded SPA
  models, and tests together. Do not add speculative aliases or legacy shapes.
- Do not bump `apiVersion` or REST `contractVersion` without a deliberate API
  freeze or release-boundary decision.
- Retired REST, settings, and metadata fields are hard errors: do not ignore,
  alias, remap, or bridge them.

## Current-Only Persistence

- During the experimental phase, every change touching persisted data must
  review whether the checked-in schema remains the clean current model. Evolve
  it when warranted; do not retain an inferior shape merely to preserve
  development profiles.
- Product code requires the current schema exactly. It must not contain legacy
  branches, fallback reads, migrations, repair, profile-reset logic, or silent
  compatibility behavior.
- A schema-version change makes existing end-user profiles incompatible.
  Startup must fail visibly and instruct the user to create an entirely fresh
  profile. It must not delete, move, replace, migrate, or partially reset the
  incompatible profile.
- Python migrations in `repos\emulebb-build-tests` are internal, intentional,
  backup-first support for known persisted test and soak schemas only. They are
  not an end-user migration or recovery path and must not appear in
  product-facing guidance.

## Source And Output Boundaries

- Follow the
  [Rust Code Quality Policy](CODE-QUALITY.md) for responsibility-based
  structure, test placement, maintainability, and lint suppressions.
- Every Windows Cargo build, test, or run uses inherited
  `CARGO_TARGET_DIR=%EMULEBB_WORKSPACE_OUTPUT_ROOT%\builds\rust\target`.
  WSL compilation uses its separately derived `target-wsl` directory. Never
  create a repo-local `target` or any source-tree build/scratch output.
- The only runnable Windows workspace binary is
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\tools\emulebb-rust\bin\emulebb-rust.exe`.
  Cargo targets are intermediate cache and must not be used by manual, soak,
  profiling, live-wire, or allow-list workflows.
- Windows long-path support applies only to shared-directory trees, incoming
  delivery, and category output paths. Config, logs, metadata DB, hash-named
  piece stores, and every other internal path intentionally remain short-path.
  The exact allowed classes and implementation mechanism live in
  `policy\rust-client.toml` and the `emulebb_ed2k::long_path` module docs.

Use `repos\emulebb-build` orchestration for supported build and validation
entrypoints. Rust live, soak, or profile work additionally requires the
[Harness And Live Policy](../../../reference/HARNESS-LIVE-POLICY.md).
