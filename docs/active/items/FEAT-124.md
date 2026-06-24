---
id: FEAT-124
workflow: local
github_issue:
title: Leech mode - monitoring-only build that observes the network without sharing
status: OPEN
priority: Minor
category: feature
labels: [research, leech-mode, identity, uploads, kad-publish, local-branch]
milestone: research-local-only
created: 2026-06-24
source: research need - observe live eD2K/Kad network behavior with a client that contributes nothing back
---
# FEAT-124 - Leech mode (monitoring-only build)

## Summary

A dedicated local branch (`feature/leech-mode`) that turns the client into a
passive observer of the eD2K/Kad network: it can search and download, but never
contributes uploads, never advertises its files, and never reveals that it is a
mod. Intended for studying live network behavior without affecting it.

This is **not** slated for `main`; it is a research branch.

## Behavior

Gated on a single compile-time constant `IsLeechModeActive()` (`LeechMode.h`):

1. **Stock identity (no mod string).** The peer hello omits the `CT_MOD_VERSION`
   tag entirely (the hello tag count is decremented to match), so the client
   announces a vanilla eMule identity. The legacy `OP_EMULEINFO` packet already
   carries no mod/compatible-client tag.
2. **Forced stock nickname.** `CPreferences::SetUserNick` always stores the
   genuine vanilla eMule default nick `http://www.emule-project.net` (not the
   eMuleBB homepage URL, which would itself reveal the mod) and ignores any
   configured/imported value. The Preferences nick field is shown locked.
3. **No uploads or shared-file publish.** Every sharing entry point is refused:
   - upload queue admission (`CUploadQueue::AddClientToQueue`) and the disk-IO
     block builder (`CUploadDiskIOThread::StartCreateNextBlockPackage`) bail, so
     no `OP_SENDINGPART` ever leaves;
   - incoming `OP_REQUESTPARTS` / `OP_REQUESTPARTS_I64` are dropped;
   - `CSharedFileList::SendListToServer` skips the `OP_OFFERFILES` publish;
   - `CSharedFileList::Publish` skips all Kad keyword/source/note stores;
   - browse-shared (`OP_ASKSHAREDFILES` / `OP_ASKSHAREDDIRS` /
     `OP_ASKSHAREDFILESDIR`) and `OP_REQUESTPREVIEW` are answered as denied/empty.

Source-exchange of other peers' sources is deliberately left intact: it shares
no local files and helps the client keep leeching.

## Files

`srchybrid/LeechMode.h` (new), `BaseClient.cpp`,
`BaseClientFriendBuddySeams.h`, `Preferences.cpp`, `PPgGeneral.cpp`,
`UploadQueue.cpp`, `UploadDiskIOThread.cpp`, `ListenSocket.cpp`,
`SharedFileList.cpp`.
