---
id: FEAT-040
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/64
title: Headless core with modern web/mobile controller and multi-user permissions
status: OPEN
priority: Major
category: feature
labels: [daemon, web, mobile, remote-control, multi-user, permissions, api]
milestone: ~
created: 2026-04-20
source: eMule Qt announcement 2026-03-05; current self-hosted ED2K controller demand
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/64. This local document is retained as an engineering spec/evidence record.

## Summary

Add a product-level remote-control mode where the transfer engine can run headless and be
managed through a modern web/mobile controller with real authentication and permissions.

This is intentionally much broader than `FEAT-013` and `FEAT-014`:

- `FEAT-013` gives the current app a JSON API
- `FEAT-014` tracks API schema/gateway follow-up
- `FEAT-040` is the bigger headless-runtime and modern-controller product line

## Why Add It

Current demand signals increasingly look like self-hosted download-manager expectations:

- run the core on a NAS, server, or always-on box
- manage it remotely from browser or phone
- support multiple users or automation clients safely

That is exactly the direction eMule Qt and current aMule/aMuTorrent-style tooling are
pushing toward.

## Intended Mainline Shape

- headless runtime mode where transfers continue without the classic MFC shell
- modern browser-based control surface with responsive/mobile layout
- strong authentication and per-user or per-role permissions
- durable API keys for automation
- reconnect-safe remote sessions that do not own the transfer engine lifecycle

## Scope Constraints

- build on the existing REST foundation rather than inventing a parallel command channel
- keep local desktop use viable; this is additive, not a forced replacement
- separate core transfer state from the current window lifetime cleanly
- treat auth and multi-user isolation as first-class requirements, not polish

## Acceptance Criteria

- [ ] the transfer core can run without the main MFC shell owning the session
- [ ] a remote web/mobile controller can inspect and manage the core
- [ ] users or roles can be restricted by capability
- [ ] API keys or equivalent automation credentials are supported
- [ ] disconnecting the controller does not stop transfers or destroy session state
