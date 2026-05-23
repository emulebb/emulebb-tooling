---
id: FEAT-083
title: Connection Checker based on public reachability polling
status: WONT_DO
priority: Minor
category: feature
labels: [connectivity, diagnostics, reachability, emuleai, wont-do]
milestone: ~
created: 2026-05-24
source: eMuleAI `ConChecker` review
---

# FEAT-083 - Connection Checker Based On Public Reachability Polling

## Decision

Record this eMuleAI feature as **WONT_DO** for eMuleBB.

The general idea of connection diagnostics is valid, but eMuleAI's
`ConChecker` style is not the right product behavior for eMuleBB: it performs
public reachability polling and can become a hidden dependency on a third-party
endpoint. eMuleBB should prefer passive diagnostics, local socket/bind status,
server/Kad state, MiniUPnP/PCP status, and explicit user-triggered tests.

## eMuleAI References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- checker lifecycle and worker:
  [`ConChecker.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/ConChecker.cpp#L53),
  [`ConChecker.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/ConChecker.cpp#L157)
- preference default:
  [`Preferences.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/Preferences.cpp#L3764)

## Rationale

- Hidden external polling is a privacy and reliability concern.
- A hardcoded endpoint can break diagnostics when the endpoint is blocked,
  down, intercepted, or unavailable on controlled networks.
- Current roadmap diagnostics should stay local and explainable unless the user
  explicitly launches a test.

## Replacement Direction

Use [FEAT-032](../../active/items/FEAT-032.md) and connectivity-modernization
diagnostics for local network evidence: bind/interface state, UPnP/PCP lease
state, server connection state, Kad state, and optional explicit port test.
