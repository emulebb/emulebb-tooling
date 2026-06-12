---
id: FEAT-011
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/10
title: CShield — integrate ED2K anti-leecher engine (44 bad-client categories)
status: OPEN
priority: Minor
category: feature
labels: [cshield, anti-leecher, ed2k, banning, security]
milestone: ~
created: 2026-04-08
source: FEATURE-PEERS-BANS.md (FEAT_011)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/10. This local document is retained as an engineering spec/evidence record.

# FEAT-011 - CShield — integrate ED2K anti-leecher engine (44 bad-client categories)

## Summary

Port `CShield` from eMuleAI — an ED2K anti-leecher engine with 44 named bad-client categories, graduated punishment levels, and per-category configurable responses. Not started. Complements the existing binary ban system with score-based queue demotion.

## Source Files (eMuleAI reference)

| File | Lines | Purpose |
|------|-------|---------|
| `Shield.h` | — | Class declarations, `EBadClientCategory` enum, `EPunishment` enum |
| `Shield.cpp` | 1079 | Full detection and enforcement logic |
| `PPgProtectionPanel.h/.cpp` | — | MFC options page — per-category punishment assignment |
| `PPgBlacklistPanel.h/.cpp` | — | Blacklist editor (`blacklist.conf`) — hashes/IPs/usernames |

## Detection Categories (`EBadClientCategory` — 44 values)

| Category | Threat |
|----------|--------|
| `PR_WRONGTAGINFOSIZE` / `PR_WRONGTAGHELLOSIZE` | Extra bytes in hello/info packets — DarkMule fingerprint → hard ban |
| `PR_HASHTHIEF` | Steals another peer's user hash to farm upload credits |
| `PR_UPLOADFAKER` | Lies about uploaded bytes to accumulate credits |
| `PR_FILEFAKER` | Reports availability on files it doesn't have; wastes source-exchange slots |
| `PR_AGGRESSIVE` | Over-requests upload slots and sources beyond protocol limits |
| `PR_XSEXPLOITER` | Extended Sources protocol abuse |
| `PR_ANTIP2PBOT` | Anti-P2P crawlers that consume source exchange without uploading |
| `PR_SPAMMER` | Chat and message spam |
| `PR_FAKEMULEVERSION` / `PR_FAKEMULEVERSIONVAGAA` | Lies about eMule version to exploit version-gated features |
| `PR_NONSUIMLDONKEY` / `PR_NONSUIEMULE` | Clients skipping Secure User Identification |
| `PR_WRONGTAGFORMAT` / `PR_WRONGTAGINFOFORMAT` | Malformed protocol tags |
| `PR_BADMODSOFT` / `PR_BADMODUSERHASHHARD` | Known leecher mod names |
| `PR_GHOSTMOD` | Webcache tag without modstring |
| `PR_MODCHANGER` / `PR_USERNAMECHANGER` | Identity cycling to evade per-peer tracking |
| `PR_OFFICIALBAN` | eMule's official ban list entries |
| `PR_MANUAL` | User-triggered ban from client context menu |
| `PR_TCPERRORFLOODER` | (tracked separately — see FEAT-012) |

## Punishment Levels (`EPunishment`)

```
P_IPUSERHASHBAN   — hard ban by IP + user hash
P_USERHASHBAN     — ban by user hash only
P_UPLOADBAN       — blocked from receiving uploads, allowed otherwise
P_SCOREX01-X09    — score multiplier reductions (queue demotion)
P_NOPUNISHMENT    — log only
```

Score reduction is the key addition over eMule's binary ban: borderline clients stay at the bottom of the upload queue rather than being hard-banned, which is more appropriate for protocol quirks vs. confirmed abuse.

## Integration Hooks

```cpp
void CheckClient(CUpDownClient* client);        // on client connect
void CheckLeecher(CUpDownClient* client);       // during active session
bool CheckSpamMessage(CUpDownClient* client, const CString& strMessage);
void CheckHelloTag(CUpDownClient* client, CTag& tag);  // at handshake — earliest possible check
void CheckInfoTag(CUpDownClient* client, CTag& tag);   // at handshake
```

Call sites in eMule:
- `CheckHelloTag` / `CheckInfoTag` → `CUpDownClient::ProcessHelloAnswer()` and `CUpDownClient::ProcessMuleInfoPacket()`
- `CheckClient` → `CClientList::AddClient()`
- `CheckLeecher` → `CUploadQueue::Process()`
- `CheckSpamMessage` → message receive handler

## Configuration Backend

- **`CPPgProtectionPanel`** — MFC tree-options page, per-category punishment, timed bans, friend exemption, "recheck now" button. Declared as `friend` of `CPreferences` (consistent with existing prefs architecture).
- **`CPPgBlacklistPanel`** — Manages `blacklist.conf`; banned hashes/IPs/usernames with 0–100 spam rating.

Both panels register as `CPropertyPage` children under the existing preferences sheet.

## Scope Note

`PR_TCPERRORFLOODER` is tracked in **FEAT-012** because it has a distinct detection path (`CheckTCPErrorFlooder()` at the listen-socket level, before a full client object exists).

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- Core category/punishment engine:
  [`Shield.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Shield.h#L29),
  [`Shield.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Shield.cpp#L420).
- Spam, hello-tag, info-tag, name/mod churn, and TCP error detectors:
  [`Shield.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Shield.cpp#L779),
  [`Shield.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Shield.cpp#L808),
  [`Shield.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Shield.cpp#L839),
  [`Shield.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/Shield.cpp#L898).
- Protection and blacklist UI:
  [`PPgProtectionPanel.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/PPgProtectionPanel.cpp#L744),
  [`PPgBlacklistPanel.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/PPgBlacklistPanel.cpp).
- Client-list display integration for bad-client state:
  [`ClientListCtrl.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientListCtrl.cpp#L995).

## eMuleBB Direction

This should not start as an automatic punishment import. The first useful
eMuleBB slice is detector visibility: log why a peer would have matched a
category, expose that reason in the UI, and measure false positives. Only after
that evidence should per-category punishments be enabled, and hard bans should
remain limited to high-confidence cases.

## Acceptance Criteria

- [ ] `Shield.h` / `Shield.cpp` ported to workspace `srchybrid/`
- [ ] `CheckHelloTag` / `CheckInfoTag` wired into `ProcessHelloAnswer` and `ProcessMuleInfoPacket`
- [ ] `CheckClient` wired into `CClientList::AddClient`
- [ ] `CheckLeecher` wired into upload queue processing
- [ ] `CPPgProtectionPanel` and `CPPgBlacklistPanel` registered in preferences
- [ ] Per-category punishment configurable via UI
- [ ] `blacklist.conf` loaded at startup, hot-reload on prefs save
- [ ] Hard-banned IPs/hashes also added to the existing IPFilter / clientban lists
- [ ] first implementation can run in log-only mode with no score or ban effect
- [ ] false-positive review data exists before any detector is allowed to hard-ban
