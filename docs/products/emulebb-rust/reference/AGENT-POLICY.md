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

- CI-gated nightlies from `main` are the current beta testing lane. Published
  beta tags remain immutable release evidence; do not rewrite their tags or
  artifacts, and do not promote stale tags as the current download path.
- One universal headless eD2K/Kad daemon is delivered through hard-gated Client,
  Indexer and Arr phases. Production stays in Client until the mandatory core
  gate in [Release Scope](../RELEASE-SCOPE.md#client-gate) closes. Explicitly
  classified distribution/environment expansion does not block that phase
  transition solely by remaining open; its phase ownership and every actual
  required CI/full-nightly check remain intact.
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
- API and database schema compatibility remain explicitly unstable through all
  three phases and freeze together only after the Arr gate. An incompatible
  schema requires an entirely fresh profile. Minimal TOML bootstrap settings
  have a separate stability goal after adopting the accepted clean Beta3
  snake_case contract. Use the [Persistence Policy](PERSISTENCE-POLICY.md) for
  naming, target defaults and ownership; obsolete shapes are hard errors, never
  aliases, compatibility shims, fallback keys or remapped values.
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
- The Windows operator runtime uses
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\tools\emulebb-rust\bin\emulebb-rust.exe`.
  Registered validation may use the regular or diagnostics daemon below
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\tools\workstreams\<id>\emulebb-rust\<target>\bin`
  after the Builder verifies its registration, source/material identity and
  ready receipt covering native companions and WebUI bytes. These stages use
  the existing heavy-validation lock and disposable harness profiles. Manual,
  persisted-soak and application allow-list paths retain the operator runtime.
  Cargo target directories remain intermediate caches.
- Windows long-path support applies only to shared-directory trees, incoming
  delivery, and category output paths. Config, logs, metadata DB, hash-named
  piece stores, and other internal paths remain short-path. Exact classes and
  mechanisms live in `policy\rust-client.toml` and
  `emulebb_ed2k::long_path` module documentation.

Use `repos\emulebb-build` orchestration for supported build and validation
entrypoints.
