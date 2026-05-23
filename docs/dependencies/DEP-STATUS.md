# Dependency Status

Reviewed on 2026-05-23 against current `main`, current
`repos\emulebb-build` dependency topology, and the active beta release policy.

This document records the current dependency decisions for the eMuleBB beta workspace.
It supersedes older dependency-removal notes that were written against other
branch lines or earlier release experiments.

## Release Policy

No third-party dependency upgrades or removals are planned for beta `0.7.3`.
The dependency forks below stay as-is unless a new release-critical issue is
explicitly promoted.

| Dependency | Current workspace fork/pin | Release decision |
|---|---|---|
| Crypto++ | `emulebb-cryptopp`, `CRYPTOPP_8_4_0` baseline plus local VS/ARM64 build deltas | Stay on 8.4 for now |
| id3lib | `emulebb-id3lib`, `id3lib-v3.9.1-emule` | Stay as-is for the future; do not track removal/replacement |
| miniupnp / miniupnpc | `emulebb-miniupnp`, `miniupnpc-master-emule` | Stay as-is for now |
| libpcpnatpmp | `emulebb-libpcpnatpmp`, `libpcpnatpmp-master-emule` | Stay as-is for now |
| nlohmann-json | `emulebb-nlohmann-json`, `v3.11.3` | Stay as-is for now |
| MbedTLS | `emulebb-mbedtls`, `mbedtls-v4.1.0-emule` | Current; no upgrade item |
| TF-PSA-Crypto | vendored by the MbedTLS fork, `v1.1.0` baseline | Current; no separate action |
| ResizableLib | `emulebb-resizablelib`, `ResizableLib-bebab50-emule` | Stay as-is |
| zlib | `emulebb-zlib`, `v1.3.2` | Current; stay as-is |

## Notes

### Crypto++

The upstream Crypto++ release tracker reports a newer `CRYPTOPP_8_9_0` tag, but
the release decision is to keep the current 8.4-based fork for now. The local fork
delta is build-system focused, including Visual Studio and ARM64 compatibility.
`REF-034` remains deferred informational dependency hardening, not beta scope.

### id3lib

id3lib remains a supported workspace dependency and remains linked into the app.
The previous removal/replacement direction is explicitly withdrawn: do not track
id3lib removal, taglib replacement, or feature removal as planned work. Existing
metadata behavior and the current static-library integration stay as-is.

### miniupnp and libpcpnatpmp

The NAT mapping dependency forks stay on the current workspace branches. Branch
head movement upstream is not, by itself, a release task. Future changes require
a concrete bug, compatibility issue, or explicit product decision.

Post-`0.7.3` p2p-overlord product-family integration should converge MiniUPnP
source ownership on `repos/third_party/emulebb-miniupnp`. p2p-overlord may keep
its Rust crates and build wrappers, but duplicate C MiniUPnP source trees should
resolve to the shared eMuleBB fork when that future slice is implemented.

### nlohmann-json

The header-only JSON dependency stays at the current workspace pin. The available
upstream release delta is not release scope.

### MbedTLS and TF-PSA-Crypto

The workspace is already on the MbedTLS 4.1-era fork with TF-PSA-Crypto present.
Older notes saying MbedTLS was removed, or still needed a 3.x-to-4.x upgrade, are
stale for current `main`.

### zlib and ResizableLib

Both stay in the current static-library model. No DLL conversion, inlining, or
replacement work is planned for the beta.
