# Quality Gates (merge-gate matrix)

Status: governance. Captured 2026-06-14. Defines the **Definition of Done / merge
gate** per product tier, so "what blocks a merge" is explicit and uniform instead
of per-repo folklore. Tiers are defined in [PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md).

## Gate matrix

| Gate | Core (rust) | Companion (qBittorrentBB / aMuTorrent) | MFC (eMuleBB, 0.7.x → 0.8.x) | Service / Lab servers | Infra |
|---|---|---|---|---|---|
| Build (matrix) | ✅ 3-OS | ✅ (fork CI) | ✅ x64 Debug+Release+diag | ed2k-server ✅ Linux; goed2k ⛔ while lab | ✅ |
| Unit/integration tests | ✅ blocking | ✅ | ✅ shared harness | ed2k-server ✅ source tests; goed2k ⛔ while lab | ✅ |
| Lint | 🔸 clippy advisory (relaxed; → `-D warnings` at Phase 0 close) + fmt ✅ | ✅ (upstream + fork checks) | warning-debt cleanup | ed2k-server fmt ✅ + clippy advisory | — |
| Supply chain | ✅ cargo-deny advisories | dependency-review | dependency-review | ed2k-server dependency-review | dependency-review |
| Policy guard | ✅ rust-client policy | fork hygiene (output-root, env, bind) | workspace validate | ed2k-server fork hygiene | workspace validate |
| Privacy guard | ✅ no private data / titles | ✅ | ✅ | ✅ | ✅ tracked-file-privacy-guard |
| **VPN leak-test** | ✅ before VPN-safe release | ✅ before VPN-safe release | required for VPN live profiles | n/a (local-only) | n/a |
| Docs/normalization | ✅ LF + docs checks | ✅ | ✅ | ✅ | ✅ |

✅ = required to merge/release · ⛔ = intentionally not gated yet · — = not applicable

## Current gaps (tracked)

- **Core (rust):** clippy is **relaxed to advisory** during active development —
  re-enable blocking `-D warnings` before the Phase 0 close. Leak-test gate not yet
  implemented (`RUST-FEAT-005`); eD2K TCP egress pin open (`RUST-FEAT-003`);
  `kad_swarm` tests non-blocking (`RUST-BUG-001`). cargo-deny enforces advisories
  only; bans/licenses pending a dep audit.
- **Companion (qBittorrentBB):** `vpnReady()` not truly fail-closed (`QBBB-FEAT-004`).
- **Service / Lab servers:** `goed2k-server` still has no build/test CI by
  decision. `ed2k-server` has Linux source-quality and candidate-artifact CI,
  but no harness/runtime gate; adding one requires the future test-server
  integration decision.

## Principles

- **Invest by tier, not by history.** Core/Companion carry the strongest gates; the
  MFC app gets maintenance gates only on the shipping `0.7.x` line (heavier gates
  return with the `0.8.x` modernization line); Lab stays light until promoted.
- **VPN-mode leak proof is non-negotiable before a VPN-safe claim or release.**
  Explicitly selected direct-mode betas must be labeled as direct, not anonymous
  ([WORKSPACE-POLICY](../WORKSPACE-POLICY.md#network-safety-selected-route-integrity-p0-invariant)).
- **A non-blocking gate must have an owning item** (e.g. `RUST-BUG-001`) so it is
  visible debt, never silent.
- New networked products inherit the Core/Companion bar at promotion time (see
  [PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md) lifecycle transitions).
- The **test gating set** (which test tiers gate which release: suite vs MFC
  `0.7.x` vs on-demand reference) is defined in
  [TEST-STRATEGY](TEST-STRATEGY.md#gating-matrix-per-release). MFC-source, parity,
  and VM/public tests are reference-only and do not gate a suite release.
