# eMuleBB Rust

eMuleBB Rust is an IPv4 eD2K/Kad client for Windows, Linux and macOS, operated
through a browser console and REST API. Search the networks, manage transfers
and share monitored folder trees from one headless daemon.

**Active beta, led by CI-gated nightly builds.** Beta 3 is the next development
target, without a release date. Its publication hold remains in force.

## Use eMuleBB Rust

- [Downloads and platforms](reference/GUIDE-DOWNLOADS-PLATFORMS.md): choose a
  native package, container or experimental Android developer artifact and
  understand requirements, checksums and evidence.
- [Getting started](reference/GUIDE-GETTING-STARTED.md): first launch, private
  API-key login, network setup, downloads, sharing and safe update/rollback.

## Develop With eMuleBB Rust

- [API consumers](api/GUIDE-API-CONSUMERS.md): make an authenticated request and
  follow the canonical OpenAPI contract.
- [Contributors](reference/GUIDE-CONTRIBUTING.md): find the owning repository,
  set up managed workspace branches and run supported checks.

Use the [GitHub Releases page](https://github.com/emulebb/emulebb-rust/releases)
and choose the newest dated nightly prerelease for current public testing.
Formal beta tags remain immutable release history, not the recommended download
path.

## Product And Engineering References

eMuleBB Rust, its WebUI, product documentation, and release notes are
English-only. The organization website may localize its homepage and FAQ, but
those pages are not product translations.

This section is the canonical home for active `emulebb-rust` product docs,
backlog, design notes, history, release scope, embedded SPA WebUI scope, and
forward REST contract. The product is an automation-first integrated suite with
hard-gated Client, Indexer, and Arr phases; production work remains in the
Client phase until its complete gate closes.

Current beta direction:

- [Client release scope](RELEASE-SCOPE.md)
- [Current-head parity evidence and documentation reconciliation](active/items/RUST-CI-006.md)
- [Beta 3 candidate certification without publication](active/items/RUST-CI-009.md)

The current product is the headless IPv4 eD2K/Kad client, its `/api/v1` control
plane, and embedded operations console. The protocol-required local Kad index
is part of that client. The future autonomous observation index and Arr
compatibility surfaces are separate hard-gated phases, not unfinished client
features.

Sharing is configured only through shared folder roots. Each root is a monitored
folder tree; the Rust daemon does not expose single-file sharing controls or a
non-recursive sharing mode.

- Active backlog: [`active/INDEX.md`](active/INDEX.md)
- Forward OpenAPI contract:
  [`api/REST-API-OPENAPI.yaml`](api/REST-API-OPENAPI.yaml)
- Architecture: [`design/architecture.md`](design/architecture.md)
- Stock/MFC hash import: [operator guide](reference/GUIDE-PROFILE-IMPORT.md)
- Forward integrated-suite design:
  [`design/integrated-suite.md`](design/integrated-suite.md)
- Agent policy: [`reference/AGENT-POLICY.md`](reference/AGENT-POLICY.md)
- Task-routed policies:
  [`API and UI`](reference/API-UI-POLICY.md),
  [`persistence`](reference/PERSISTENCE-POLICY.md),
  [`protocol`](reference/PROTOCOL-POLICY.md),
  [`product documentation`](reference/PRODUCT-DOCS-POLICY.md), and
  [`code quality and test placement`](reference/CODE-QUALITY.md)

Repo-local docs under `repos/emulebb-rust/docs` are pointers only.
