# p2p-overlord eMule Agent

`p2p-overlord` is a separate Rust/Node product in the eMuleBB organization for
headless, server-oriented P2P metadata and network-agent work. Its current eMule
runtime surface is `overlord-agent-emule`, a Rust agent for Kad and ED2K work in
the `p2p-overlord-agents` repository.

This page is the eMuleBB documentation entrypoint for that agent. The detailed
protocol notes remain in the p2p-overlord source repositories.

## Product Boundary

p2p-overlord is a peer product, not an eMuleBB desktop-app subsystem.
Integration with the eMuleBB workspace means shared contracts, shared campaign
patterns, shared deterministic services where appropriate, and explicit
repository topology. It does not mean merging the Rust agent into the native
Windows desktop app.

The active p2p-overlord repositories are:

| Repository | Role |
|---|---|
| [`p2p-overlord-agents`](https://github.com/emulebb/p2p-overlord-agents) | Rust protocol agents and protocol crates. The current runtime agent is `overlord-agent-emule`. |
| [`p2p-overlord-be`](https://github.com/emulebb/p2p-overlord-be) | Coordinator, public/backend API, SvelteKit UI, Prisma schema, PostgreSQL helper, and product docs. |
| [`p2p-overlord-tooling`](https://github.com/emulebb/p2p-overlord-tooling) | Scenario manifests, parity runners, harness orchestration, reports, and quality guards. |

The eMuleBB desktop app remains the release product for Windows eMule users.
p2p-overlord remains the headless agent and coordinator product for protocol
parity, metadata indexing, scenario evidence, and future multi-network work.

## Current eMule Agent Surface

`overlord-agent-emule` is the current p2p-overlord runtime package for Kad and
ED2K. The agent-side Rust workspace also contains shared runtime, NAT, Kad, ED2K,
MiniUPnP wrapper, and developer-helper crates.

The active protocol target is stock-compatible eMule `v0.72a` Kad and ED2K
behavior where interoperability or observable traffic shape depends on it. The
standing protocol exception is defunct ED2K PeerCache support.

Current source docs:

- [Agents docs](https://github.com/emulebb/p2p-overlord-agents/tree/develop/docs)
- [Kad and ED2K protocol notes](https://github.com/emulebb/p2p-overlord-agents/tree/develop/docs/kad)
- [Backend docs](https://github.com/emulebb/p2p-overlord-be/tree/develop/docs)
- [Tooling docs](https://github.com/emulebb/p2p-overlord-tooling/tree/develop/docs)

## Shared eMuleBB Contracts

`docs/rest/REST-API-OPENAPI.yaml` remains the canonical eMuleBB-compatible REST
contract. If a p2p-overlord implementation advertises an eMuleBB-compatible
`/api/v1` surface, it must prove the claimed subset against that OpenAPI source
instead of defining a parallel contract.

Deterministic ED2K server scenarios should use the active eMuleBB
[`goed2k-server`](https://github.com/emulebb/goed2k-server) fork. Historical
p2p-overlord ED2K server lineage is reference material only.

For the full product-family boundary and implementation order, use the
[p2p-overlord Product-Family Integration Plan](../active/plans/P2P-OVERLORD-PRODUCT-FAMILY-INTEGRATION.md).

## Operating Notes

Use the repo-local `AGENTS.md` files before making code changes in the
p2p-overlord repositories. In the canonical eMuleBB workspace, the shared policy
still starts at `repos/emulebb-tooling/docs/WORKSPACE-POLICY.md`.

Common source-level quality gates are:

| Repo | Gate |
|---|---|
| `p2p-overlord-agents` | `cargo fmt --all --check` and the repo's strict `cargo clippy` command |
| `p2p-overlord-be` | `npm run quality` from the coordinator package |
| `p2p-overlord-tooling` | `python -m overlord_tooling quality-baseline` |

Live-network p2p-overlord runs are opt-in and must follow the workspace live-test
policy. Deterministic local scenarios should be preferred for repeatable
evidence.
