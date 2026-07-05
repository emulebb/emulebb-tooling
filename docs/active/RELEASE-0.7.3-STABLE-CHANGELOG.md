# eMuleBB 0.7.3 Stable Changelog

Status: PREPARED for stable publication on 2026-07-05. The selected app head is
`9402251c`; the selected aMuTorrent companion head is `2da7c19`.

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

Final stable hashes are recorded after GitHub release publication in
[CI-035](items/CI-035.md). Expected stable assets are:

- `emulebb-0.7.3-x64.zip`
- `emulebb-0.7.3-arm64.zip`
- `emulebb-0.7.3-diagnostics-x64.zip`
- `emulebb-0.7.3-diagnostics-arm64.zip`
- `Bootstrap-eMuleBBSuite.ps1`
- `emulebb-0.7.3-amutorrent-x64.zip`
