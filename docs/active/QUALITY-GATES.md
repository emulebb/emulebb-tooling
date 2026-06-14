# Quality Gates (merge-gate matrix)

Status: governance. Captured 2026-06-14. Defines the **Definition of Done / merge
gate** per product tier, so "what blocks a merge" is explicit and uniform instead
of per-repo folklore. Tiers are defined in [PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md).

## Gate matrix

| Gate | Core (rust) | Companion (qBittorrentBB / aMuTorrent) | Frozen (MFC) | Lab (goed2k) | Infra |
|---|---|---|---|---|---|
| Build (matrix) | ✅ 3-OS | ✅ (fork CI) | ✅ x64 Debug+Release+diag | ⛔ while lab | ✅ |
| Unit/integration tests | ✅ blocking | ✅ | ✅ shared harness | ⛔ while lab | ✅ |
| Lint | ✅ clippy `-D warnings` + fmt | ✅ (upstream + fork checks) | warning-debt cleanup | — | — |
| Supply chain | ✅ cargo-deny advisories | dependency-review | dependency-review | — | dependency-review |
| Policy guard | ✅ rust-client policy | fork hygiene (output-root, env, bind) | workspace validate | — | workspace validate |
| Privacy guard | ✅ no private data / titles | ✅ | ✅ | ✅ | ✅ tracked-file-privacy-guard |
| **Leak-test (networked)** | ✅ **release-blocking** | ✅ **release-blocking** | required for live profiles | n/a (local-only) | n/a |
| Docs/normalization | ✅ LF + docs checks | ✅ | ✅ | ✅ | ✅ |

✅ = required to merge/release · ⛔ = intentionally not gated yet · — = not applicable

## Current gaps (tracked)

- **Core (rust):** leak-test gate not yet implemented (`RUST-FEAT-005`); eD2K TCP
  egress pin open (`RUST-FEAT-003`); `kad_swarm` tests non-blocking (`RUST-BUG-001`).
  cargo-deny enforces advisories only; bans/licenses pending a dep audit.
- **Companion (qBittorrentBB):** `vpnReady()` not truly fail-closed (`QBBB-FEAT-004`).
- **Lab (goed2k):** no build/test CI by decision; promotion adds the Service bar.

## Principles

- **Invest by tier, not by history.** Core/Companion carry the strongest gates; the
  Frozen MFC app gets maintenance gates only; Lab stays light until promoted.
- **The leak-test is non-negotiable for any networked product** — it is the
  automated form of the P0 Network Safety invariant
  ([WORKSPACE-POLICY](../WORKSPACE-POLICY.md#network-safety-no-clearnet-leak--p0-invariant)).
- **A non-blocking gate must have an owning item** (e.g. `RUST-BUG-001`) so it is
  visible debt, never silent.
- New networked products inherit the Core/Companion bar at promotion time (see
  [PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md) lifecycle transitions).
