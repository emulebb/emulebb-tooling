# Test Strategy

Status: active lifecycle policy. Updated 2026-10-02.

There is no forward cross-product “Suite” release gate. Test depth follows each
repository's current lifecycle and the risk of the proposed change.

## Product gates

| Lane | Required direction |
|---|---|
| **emulebb-rust** | Active experimental beta. Repo-native quality, test, and cross-platform build gates are primary; add targeted workspace evidence as needed. |
| **emulebb-mfc `0.7.x`** | Long-term maintenance. Baseline plus focused native, package, smoke, or soak proof proportional to the touched maintenance surface. |
| **qBittorrentBB / emulebb-libtorrent** | Paused experiments. No scheduled release gate; retained checks run on repository changes or explicit operator request. |
| **aMuTorrent** | Frozen `0.7.3` controller package. No scheduled sync or forward feature gate; package and bounded maintenance proof run only when needed. |
| **TrackMuleBB** | Archived private experiment. No active gate. |
| **goed2k-server** | Harness-only support service. Validate the harness behavior required by the consuming test lane; do not treat it as a product release. |
| **ed2k-server** | Reference fork for analysis and possible upstream contribution. Use upstreamable, change-focused checks; there is no production-service gate. |
| **aMule fork** | Analysis/reference fork with active mirror and quality automation. It is not an eMuleBB product release lane. |

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

The superseded cross-product planning document is retained as
[historical context](../history/HIST-TEST-STRATEGY-2026-06-15.md).
