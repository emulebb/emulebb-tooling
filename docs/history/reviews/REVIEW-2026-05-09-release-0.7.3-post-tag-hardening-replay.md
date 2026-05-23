# Beta 0.7.3 Post-1.0 Hardening Replay

- Date: 2026-05-09
- Baseline internal evidence tag: `emule-bb-v1.0.0`
- Candidate: `EMULE_WORKSPACE_ROOT\workspaces\v0.72a\app\eMule-main` on
  `main`
- Scope: app commits `BUG-102` through `BUG-110`

## Executive Finding

The post-1.0 app hardening queue is small and coherent: nine app commits touch
DirectDownload, packet guards, client UDP receive handling, WebSocket accept
draining, shared startup-cache worker failures, autocomplete allocation, and
meter-icon GDI ownership. The supported Release x64 native replay passed. The
audit initially found several fixes covered only indirectly; those focused
coverage gaps were promoted to [CI-032](../items/CI-032.md) and are now closed
with targeted probes.

## Replay Evidence

- `git log --oneline emule-bb-v1.0.0..main`
- `python -m emule_workspace build tests --config Release --platform x64`
  - passed with 0 warnings
  - build log directory:
    `EMULE_WORKSPACE_ROOT\workspaces\v0.72a\state\build-logs\20260509-140241`
- `python -m emule_workspace test all --config Release --platform x64`
  - `494` parity test cases passed
  - `71` web API test cases passed
  - native coverage directory:
    `EMULE_WORKSPACE_ROOT\repos\emulebb-build-tests\reports\native-coverage\20260509-140248-eMulebb-workspace-v0.72a-eMule-main-x64-Release`
  - live-diff summary:
    `EMULE_WORKSPACE_ROOT\repos\emulebb-build-tests\reports\live-diff-summary.txt`

## Commit Map

| Bug | Commit | File | Release area | Replay status | Follow-up |
|-----|--------|------|--------------|---------------|-----------|
| BUG-102 | `05b94fe` | `srchybrid/DirectDownload.cpp` | Downloads/persistence | App commit `dc412b4` routes WinInet handle ownership through the cancellation registry policy seam; test commit `f377146` proves cancelled owners reject new handle registration. | [CI-032](../items/CI-032.md) |
| BUG-103 | `e3183fd` | `srchybrid/DownloadClient.cpp` | Downloads/protocol parsing | Native parity replay passed protocol guard block-header cases and overflow/truncation cases. | none |
| BUG-104 | `0af5c22` | `srchybrid/ClientUDPSocket.cpp` | UDP/networking | Native parity replay passed client UDP packet failure logging and opcode extraction seams. | none |
| BUG-105 | `06b0d56` | `srchybrid/WebSocket.cpp` | WebServer/WebSocket | App commit `220c0cb` exposes the rejected-IP accept-drain policy and test commit `46eab04` proves the listener continues draining pending accepts after a disallowed remote-access IP is rejected. | [CI-032](../items/CI-032.md) |
| BUG-106 | `ed28dda` | `srchybrid/SharedFileList.cpp` | Shared startup cache | Native parity replay passed startup-cache scheduling, post-failure, completion-action, and shutdown wait seams. | none |
| BUG-107 | `18b22c8` | `srchybrid/Packets.cpp` | Packet decompression | Native parity replay passed bounded size arithmetic and truncated packet span cases. | none |
| BUG-108 | `2653a97` | `srchybrid/CustomAutoComplete.cpp` | UI/preferences | App commits `e336f26` and `083478a` expose the enum-string copy path through `CustomAutoCompleteSeams`; test commit `6273fdb` proves allocation failure returns `E_OUTOFMEMORY` before copying through a null allocation. | [CI-032](../items/CI-032.md) |
| BUG-109 | `a27323a` | `srchybrid/MeterIcon.cpp` | UI/GDI | Test commit `237e6d2` adds focused GDI ownership seam coverage for scoped bitmap, brush, and scratch-DC release paths used by `MeterIcon.cpp`. | [CI-032](../items/CI-032.md) |
| BUG-110 | `9bdf3f7` | `srchybrid/MeterIcon.cpp` | UI/GDI | Test commit `237e6d2` adds focused `ScopedSelectObject` coverage proving selected bitmaps are restored before callers consume them. | [CI-032](../items/CI-032.md) |

## Release Decision

[CI-023](../items/CI-023.md) can remain closed as the post-tag mapping and
replay gate: the commits are mapped, the supported Release x64 replay passed,
and CI-032 now closes the previously insufficient focused coverage for BUG-102,
BUG-105, BUG-108, BUG-109, and BUG-110. Beta 0.7.3 must still wait for the
downstream area gates.
