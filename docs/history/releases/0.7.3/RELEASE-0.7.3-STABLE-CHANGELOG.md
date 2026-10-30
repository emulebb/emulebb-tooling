# eMuleBB 0.7.3 Stable Changelog

Status: PUBLISHED on 2026-07-05. The selected app head is `9402251c`; the
selected aMuTorrent companion head is `2da7c19`.

This stable cut carries forward the published RC3 package shape and suite scope:
MFC eMuleBB, diagnostics packages, the PowerShell bootstrapper, aMuTorrent, and
local Arr integration scripts. qBittorrentBB, emulebb-rust, TrackMuleBB, `uv`,
and the Python installer remain outside the `0.7.x` release line.

## Stable Delta After RC3

- Stability: added shutdown/socket lifetime guards for server connection paths
  (`BUG-152`, `BUG-153`).
- Diagnostics: aligned MFC `diag_event_v1` oracle output for ED2K publish,
  upload slot, Kad publish, packet bulk sampling, and download source-count
  traces. These are diagnostics-only and do not change default eD2K/Kad wire
  behavior.
- Documentation: synced README install commands to the published RC3
  bootstrapper path and aligned runtime diagnostics artifact names with the MFC
  implementation.
- Release decision: the operator accepted the remaining stable live/soak/VM
  proof rows as waived on 2026-07-05 based on prior RC3 proof and current release
  confidence.

## Published Heads And Artifacts

App release: <https://github.com/emulebb/emulebb/releases/tag/emulebb-v0.7.3>
(published 2026-07-05T20:14:01Z; workflow run 28752898974; annotated tag peels
to app `9402251c2dc986dfc2346e5c80046e22d5c7e3d6`).

aMuTorrent companion release:
<https://github.com/emulebb/amutorrent/releases/tag/amutorrent-v3.8.8-emulebb-v0.7.3>
(published 2026-07-05T19:57:39Z; workflow run 28752899013; annotated tag peels
to `2da7c19313c44fe2ed29bf8d24eec4cca3eeeb8d`).

Final published SHA-256:

- `emulebb-0.7.3-x64.zip`: `c7a0238e36619e34acebf0687ff3ba9ab8b366be160c6f53ef72ba02d2235db9`
- `emulebb-0.7.3-arm64.zip`: `d61baffe96aa4110c9b7a7550d2d744d5c51d654f6276d545e2a4ecb6bd301cd`
- `emulebb-0.7.3-diagnostics-x64.zip`: `41f383f4e0d9b429211f0a23e7415da68fb06c9b4f70f86ee84db080765d5795`
- `emulebb-0.7.3-diagnostics-arm64.zip`: `f74c4180b06e6c00a8e33373a284ca6261d1a16d573396a05dc804adcc96d2f3`
- `Bootstrap-eMuleBBSuite.ps1`: `05a94d71993efc8df4bdf34b90c6250dd5cf0ebd4652c78b972918d2f674c0ed`
- `Bootstrap-eMuleBBSuite.ps1.sha256`: `56bfa42479c66dca46f2a1805e2b1c232101e0833185f78c2e2f55891e1835bd`
- `emulebb-0.7.3-amutorrent-x64.zip`: `47fa82c254b62bdb786fe848f66d31d5616254a39b0d5b45553492f77a6c732e`

SPDX SBOM SHA-256: x64
`93e73132f2b3ff4208c42b7d24c1dfa68bf5fbb674ca0a0f32fe29751d426269`,
arm64 `77375a2c598f1e7b240de9fefbece9a0ed58a9b9ad4ff6fcf94a4ff64eb828b8`,
diagnostics-x64
`1ffecf0dcda47035d06d5952a8ff3ceaf708b326425201f69237e3a99bacf3a8`,
diagnostics-arm64
`12caa2343fd74d32fb9a23794fa9cf6c60043ee4b61b05c8e94acf7771784b73`, and
aMuTorrent x64
`9618f94190aaa2aefe89b1a42daf74c549d03dd3f2be45fdd96677b4c15be110`.

Manifest SHA-256: x64
`c7aa4fcb319148ba51bda6736fb86a8d6a70e0d46c5e515628aa055c8000abdb`,
arm64 `32ce7d4a5eeb3fe287df5fed88d5e821247923216b2580c90daba3bbd576b315`,
diagnostics-x64
`a0e6e27e2da5cf5d4df4ab06d1d2f0840ce0f32e3f08a289ca1b09fc6a0c98cc`,
diagnostics-arm64
`a23826f38fff5a784704d6498cc9dfdfd98c85277bf432866f1393bd69359e90`, and
aMuTorrent x64
`f2cac268bc68fb92c10b32dbeeadf69935ab9a3c71e39d4e1c58c9e685bd00e7`.
