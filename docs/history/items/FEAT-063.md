---
id: FEAT-063
title: Web Interface preferences layout polish
status: DONE
priority: Minor
category: feature
labels: [preferences, webserver, ui-polish]
milestone: beta-0.7.3
---

# FEAT-063 - Web Interface Preferences Layout Polish

## Status

Done

## Summary

The Preferences > Web Interface page now uses the wider 1024x800 preferences
dialog real estate instead of the old narrow stock column. The layout groups
settings by user flow:

- General REST API settings: enable, port, bind address, API key, allowed IPs,
  and UPnP.
- Administrator settings.
- Guest settings.
- HTTPS certificate settings.
- Legacy Web UI settings: enable, gzip, max file size, session timeout, and
  template controls.

The change is intentionally static `.rc` layout work plus matching control
enable-state cleanup. It does not change WebServer preference persistence,
defaults, API behavior, or template handling.

## Implementation

- App commit: `1776b51 FEAT-063 polish web interface preferences`
- Follow-up app commit: `c652d31 FEAT-063 move legacy web limits`
- Added resource IDs for the HTTPS and legacy group boxes.
- Reordered `IDD_PPG_WEBSRV` tab flow around the new section layout.
- Localized the new group boxes with existing strings only.
- Updated Web Interface enable/disable handling so labels and section controls
  gray consistently when REST, guest, HTTPS, or legacy UI options are off.
- Moved session timeout and max file-size controls into the Legacy Web UI
  section because both are consumed by the legacy WebServer/session/template
  paths, not by native REST API requests.

## Validation

- Debug app build:
  `python -m emule_workspace build app --workspace-root C:\prj\p2p\eMule\eMulebb-workspace --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
- Release app build:
  `python -m emule_workspace build app --workspace-root C:\prj\p2p\eMule\eMulebb-workspace --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`
- Release validation:
  `python -m emule_workspace validate --config Release --platform x64 --build-output-mode ErrorsOnly`
- Preference UI harness:
  `python repos\emulebb-build-tests\scripts\preference-ui-e2e.py --workspace-root workspaces\v0.72a --app-root workspaces\v0.72a\app\eMule-main --configuration Debug --artifacts-dir workspaces\v0.72a\state\ui-proof\web-interface-after --web-interface-screenshot-name web-interface-after.png --keep-artifacts`
- Follow-up Preference UI harness:
  `python repos\emulebb-build-tests\scripts\preference-ui-e2e.py --workspace-root workspaces\v0.72a --app-root workspaces\v0.72a\app\eMule-main --configuration Debug --artifacts-dir workspaces\v0.72a\state\ui-proof\web-interface-legacy-controls --web-interface-screenshot-name web-interface-legacy-controls.png --keep-artifacts`
- UI proof:
  `workspaces\v0.72a\state\ui-proof\web-interface-before\web-interface-before.png`
  and
  `workspaces\v0.72a\state\ui-proof\web-interface-after\web-interface-after.png`
- Follow-up UI proof:
  `workspaces\v0.72a\state\ui-proof\web-interface-legacy-controls\web-interface-legacy-controls.png`
