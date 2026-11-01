# Test Strategy

Status: active lifecycle policy. Updated 2026-11-01.

There is no forward cross-product “Suite” release gate. Test depth follows each
repository's current lifecycle and the risk of the proposed change.

## Product gates

| Lane | Required direction |
|---|---|
| **emulebb-rust** | Active beta. Repo-native quality, test, and cross-platform build gates are primary; add targeted workspace evidence as needed. |
| **emulebb-mfc `0.7.x`** | Preferred observable protocol oracle. Diagnostics, deterministic controls, and oracle buildability only; no product or protocol evolution. |
| **ed2k-server** | Upstream-clean local deterministic dependency. Keep emulebb-specific protocol behavior out of the fork and adapt tests in the harness. |
| **aMule stable** | Frozen independent protocol-parity reference at one exact release and diagnostics-only patch revision. |
| **aMule HEAD** | Moving upstream source-analysis and future-interoperability lane; never a current parity gate. |

## Shared rules

- Keep fast deterministic unit and contract checks close to the owning repo.
- Use `emulebb-build-tests` only for cross-process, protocol, package, soak, or
  live evidence that cannot be proved cleanly in one repository.
- MFC product-release checks do not gate Rust beta work. A selected protocol
  campaign may require causally attributed MFC oracle evidence for the exact
  supported states it claims to cover.
- Public-network, VM, long soak, and destructive scenarios remain explicit,
  evidence-bound lanes rather than default fast checks.
- The persisted native-Windows hide.me lane is discovery-only, treats provider
  state as inherited and read-only, requires full-tunnel mode plus VPN Guard
  Block, and must never silently fall back to a direct route.

Protocol-parity evidence semantics, oracle roles, and consolidation rules are
defined by the [Harness And Live Policy](../reference/HARNESS-LIVE-POLICY.md).

The superseded cross-product planning document is recoverable from the archival
commit recorded in the [history overview](../history/INDEX.md).
