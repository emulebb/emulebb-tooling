# emulebb-rust

This section is the canonical home for active emulebb-rust product docs,
backlog, design notes, history, release scope, embedded SPA WebUI scope, and
forward REST contract. The product is an automation-first integrated suite with
hard-gated Client, Indexer, and Arr phases; production work remains in the
Client phase until its complete gate closes.

Current published beta baseline:

- [`0.1.0-beta.2` GitHub release](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.2)
- [`0.1.0-beta.2` release scope](RELEASE-SCOPE.md)
- [Current-head parity evidence and documentation reconciliation](active/items/RUST-CI-006.md)

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
- Agent policy: [`reference/AGENT-POLICY.md`](reference/AGENT-POLICY.md)
- Task-routed policies:
  [`API and UI`](reference/API-UI-POLICY.md),
  [`persistence`](reference/PERSISTENCE-POLICY.md),
  [`protocol`](reference/PROTOCOL-POLICY.md),
  [`product documentation`](reference/PRODUCT-DOCS-POLICY.md), and
  [`code quality and test placement`](reference/CODE-QUALITY.md)

Repo-local docs under `repos/emulebb-rust/docs` are pointers only.
