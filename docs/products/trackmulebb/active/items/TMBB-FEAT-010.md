---
id: TMBB-FEAT-010
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/9
title: Suite setup CLI - self-contained installer (TUI + suite.toml, install/update/repair)
status: OPEN
priority: Major
category: feature
labels: [installer, cli, setup, self-contained, bundle]
milestone: phase-2
created: 2026-06-16
source: suite bundle notes 4,8-15 (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-010 - Suite setup CLI - self-contained installer (TUI + suite.toml, install/update/repair)

## Summary

The suite installer lives in TrackMuleBB as a **Python setup CLI**: TUI (interactive) + flags/**suite.toml** (non-interactive). It installs and auto-wires the selectable bundle, **self-contained** in the install dir, invoked by the minimal install.ps1 bootstrap. Design: emulebb-tooling SUITE-INSTALLER.

## Why This Matters

Moves the real setup out of PowerShell into one Python brain (single pane of install + config). The web UI never installs; the CLI owns the component lifecycle.

## Intended Shape

- **TUI + suite.toml + flags** (Typer). CLI = install/lifecycle; web UI = settings only.
- **Lifecycle:** install / update / repair (no uninstall - delete the dir). Initial phase = install only.
- **Self-contained:** Python via **uv --python-preference only-managed** in the install dir (no system Python, no admin, no PATH); Node only for Bountarr.
- **Selection:** components selectable, TrackMuleBB always (optional start), **>=1 P2P client**, dependency enforcement.
- **Auto-wiring:** every inter-app connection (keys, Prowlarr/Arr/client registration, the indexer-exclusion tag).
- **Targets:** Windows-local (native) + Docker (generate compose + profiles + Gluetun option, P2P-only). Firewall = check + docs (no silent change). Data paths overridable.

## Acceptance Criteria

- [ ] install.ps1 is a minimal bootstrap (uv + fetch TrackMuleBB + run CLI).
- [ ] CLI installs the selected bundle self-contained (uv only-managed; no system Python/admin).
- [ ] Auto-wiring connects every selected component.
- [ ] --target docker emits a compose with profiles + optional Gluetun (P2P-only).
- [ ] update + repair exist (no uninstall command).

## Notes

- Big umbrella; may be split as built. uv is already TrackMuleBB tooling (uv sync).
