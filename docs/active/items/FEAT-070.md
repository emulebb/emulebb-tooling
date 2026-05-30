---
id: FEAT-070
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/68
title: Add targeted client UserHash and upload-lifecycle diagnostics
status: OPEN
priority: Minor
category: feature
labels: [diagnostics, logging, upload, clients, userhash]
milestone: post-0.7.3
created: 2026-05-21
source: aMule issue #538 triage against current client/upload logging
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/68. This local document is retained as an engineering spec/evidence record.

## Summary

Add a narrow diagnostic pass for client identity and upload-queue lifecycle
events. The goal is better abuse/debug visibility without changing transfer
policy.

## Current Mainline Evidence

Current debug strings include IP, username, client software, download/upload
state, and Kad state, but `CUpDownClient::DbgGetClientInfo(...)` does not
include UserHash. Upload queue add/remove paths already log some lifecycle
events, but the coverage is uneven across queue admission, slot grant, ban,
drop, and removal transitions.

## Scope

- Add UserHash to targeted debug logs after hello parsing, where it is valid.
- Add or normalize upload-queue lifecycle logs for:
  - waiting queue admission/rejection;
  - slot grant;
  - upload removal with reason;
  - ban-state transitions where already supported by preferences.
- Keep logs behind existing verbose/debug preferences.
- Avoid logging secrets, API keys, or local filesystem paths.

## Non-Goals

- Do not add new punishment, banning, or scoring behavior.
- Do not make verbose logging default-on.
- Do not change the upload slot controller.

## Upstream Signal

aMule issue #538 asks for detailed client connection logging including UserHash,
IP, lifecycle events, bans, and filtered attempts. eMuleBB already has much of
this surface, but a focused UserHash/lifecycle pass would improve diagnostics.

## Acceptance Criteria

- [ ] UserHash appears in selected client diagnostics after the client hello is
      parsed.
- [ ] Upload queue add/grant/remove transitions have consistent debug messages.
- [ ] Ban and filtered-connection messages remain controlled by existing prefs.
- [ ] Tests or log-route smoke coverage verify the new diagnostics do not break
      normal logging.
