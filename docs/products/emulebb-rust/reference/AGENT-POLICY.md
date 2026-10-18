# emulebb-rust Agent Policy

Read the [Workspace Policy](../../../WORKSPACE-POLICY.md) first. This compact
base is mandatory for `emulebb-rust` product work. Load only the task annexes
selected below.

## Task Routing

- eD2K or Kad wire behavior, packets, tags, capabilities, network identity, or
  interoperability: [Protocol Policy](PROTOCOL-POLICY.md).
- `/api/v1`, REST routes, DTOs, OpenAPI, controllers, or the embedded SPA:
  [API And UI Policy](API-UI-POLICY.md).
- Persisted settings, metadata, database schemas, or profile compatibility:
  [Persistence Policy](PERSISTENCE-POLICY.md).
- Rust source structure, test placement, refactoring, maintainability, or lint
  suppressions: [Rust Code Quality Policy](CODE-QUALITY.md).
- Rust product docs, backlog records, release scope, design docs, or retained
  evidence: [Product Documentation Policy](PRODUCT-DOCS-POLICY.md).
- Live, soak, or profile work: the workspace
  [Harness And Live Policy](../../../reference/HARNESS-LIVE-POLICY.md).

Do not load unrelated Rust annexes merely because the repository is active.

## Product Direction

- `rust-v0.1.0-beta.2` is the current published beta baseline. Development
  continues on the beta lane; do not rewrite published beta tags or artifacts.
- The product is an automation-first integrated suite delivered through hard-
  gated Client, Indexer, and Arr phases. Production work stays in the Client
  phase until every active client item, including newly accepted items, closes.
- The Rust headless daemon and embedded SPA operations console are the active
  client and UI. A native desktop UI or recreation of the MFC GUI is outside
  scope.
- Stock/community eMule owns wire behavior and externally visible protocol
  state. Maintained eMuleBB MFC owns only explicitly identified non-wire
  defaults, ceilings, and disk/network I/O outcomes. Current aMule is evidence
  and optimization inspiration, not a behavior authority. Rust-native async
  design owns internal implementation when required outcomes remain intact.
- The bounded-monolith target is one daemon and one SQLite database with
  explicit client, indexer, and compatibility domain boundaries. The future
  autonomous indexer and Arr adapters must not introduce parallel client state.
- API, configuration, and schema compatibility remain explicitly unstable
  through all three phases and freeze together only after the Arr gate. An
  incompatible schema requires an entirely fresh profile.
- `policy\rust-client.toml`, its omission registry, and its extension registry
  are the machine-readable authority for platform, behavior authority,
  protocol, long-path, reviewed-omission, and intentional-extension policy.
- Retired REST, settings, and metadata fields are hard errors. Do not ignore,
  alias, remap, or bridge them.

## Source And Output Boundaries

- Every Windows Cargo build, test, or run uses inherited
  `CARGO_TARGET_DIR=%EMULEBB_WORKSPACE_OUTPUT_ROOT%\builds\rust\target`.
  WSL compilation uses its separately derived `target-wsl` directory. Never
  create repo-local build or scratch output.
- The only runnable Windows workspace binary is
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\tools\emulebb-rust\bin\emulebb-rust.exe`.
  Cargo targets are intermediate cache and are not manual, soak, profiling,
  live-wire, or allow-list executables.
- Windows long-path support applies only to shared-directory trees, incoming
  delivery, and category output paths. Config, logs, metadata DB, hash-named
  piece stores, and other internal paths remain short-path. Exact classes and
  mechanisms live in `policy\rust-client.toml` and
  `emulebb_ed2k::long_path` module documentation.

Use `repos\emulebb-build` orchestration for supported build and validation
entrypoints.
