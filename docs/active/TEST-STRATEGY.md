# Test Strategy

Status: active lifecycle policy. Updated 2026-10-02.

There is no forward cross-product “Suite” release gate. Test depth follows each
repository's current lifecycle and the risk of the proposed change.

## Product gates

| Lane | Required direction |
|---|---|
| **emulebb-rust** | Active beta. Repo-native quality, test, and cross-platform build gates are primary; add targeted workspace evidence as needed. |
| **emulebb-mfc `0.7.x`** | Diagnostics and critical-fix maintenance. Keep it buildable and shippable; require proof proportional to the touched surface. |
| **ed2k-server** | Sole local deterministic server and upstream-aligned Rust fork. Use minimal upstreamable changes and focused harness proof; no production-service gate. |
| **aMule upstream** | Managed official upstream used for interoperability and protocol parity. It is not an eMuleBB product release lane. |

## Shared rules

- Keep fast deterministic unit and contract checks close to the owning repo.
- Use `emulebb-build-tests` only for cross-process, protocol, package, soak, or
  live evidence that cannot be proved cleanly in one repository.
- MFC source/parity checks do not gate Rust beta work, and paused/frozen fork
  coverage does not gate an unrelated Rust change.
- Public-network, VM, long soak, and destructive scenarios remain explicit,
  evidence-bound lanes rather than default fast checks.
- Native Windows VPN integration is not a forward product priority. If a test
  explicitly selects a VPN mode, it must fail closed and must never silently
  fall back to a direct route.

The superseded cross-product planning document is recoverable from the archival
commit recorded in the [history overview](../history/INDEX.md).
