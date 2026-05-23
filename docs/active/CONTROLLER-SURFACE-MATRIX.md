# RC 0.7.3 Controller Surface Matrix

This matrix defines the controller API surface that must stay green before the
`emulebb-v0.7.3-rc.1` RC can be tagged. It covers the release-facing API and
controller integrations only; Source Exchange protocol validation is tracked by
the search/server/Kad parity gates.

## Proof Command

Run the focused controller-surface gate from `EMULE_WORKSPACE_ROOT`:

```powershell
python -m emule_workspace test live-e2e --profile controller-surface --fail-fast
```

This profile is separate from `beta-green` so the short backend green run stays
fast, while aMuTorrent and full controller compatibility still have a named
release proof.

## Surface Matrix

| Surface | Public role | Required proof |
|---|---|---|
| Native REST `/api/v1` | Trusted local controller API for eMuleBB and aMuTorrent. | `rest-api` passes OpenAPI/registry parity, safe route coverage, typed JSON success/error envelopes, destructive intent checks, and smoke stress. |
| qBittorrent-compatible `/api/v2` | Arr download-client adapter. This is the Arr-needed qBit subset only, not a full qBittorrent Web API clone. | `rest-api`, Radarr, and Sonarr prove qBit login, add, info, properties, files, category mutation, pause/resume, and delete behavior with adapter-local text/session errors. |
| Torznab-compatible API | Prowlarr indexer adapter consumed directly and synced into Radarr/Sonarr. | Prowlarr, Radarr, and Sonarr prove category-aware search, API-key handling, feed behavior, synced indexers, and redacted live-wire diagnostics. |
| aMuTorrent | Browser UI consumer of native `/api/v1`; it must not drive native route aliases or adapter quirks. | `amutorrent-browser-smoke` proves connection state, categories, searches, transfers, shared files/directories, uploads, transfer detail hydration, and add/delete paths. |

## Closeout Evidence

After each closeout run, record the current artifact paths in:

- [AMUT-001](../history/items/AMUT-001.md) and [AMUT-002](../history/items/AMUT-002.md) for aMuTorrent
- [ARR-001](../history/items/ARR-001.md) for Prowlarr/Radarr/Sonarr and qBit-compatible flows
- [CI-024](../history/items/CI-024.md) for controller replay status
- [CI-025](../history/items/CI-025.md) for native REST and adapter contract drift
- [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) before tagging

All live reports must show the workspace live-network policy:
`BindInterface=hide.me`, empty P2P `BindAddr`, and P2P UPnP enabled.
