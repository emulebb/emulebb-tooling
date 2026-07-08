# MVP — Unified Transfers Dashboard

The first runnable TrackMuleBB feature: a single dark-themed web page that shows
the transfers of **emulebb-rust** (eD2K/Kad) and **qBittorrentBB** (BitTorrent)
in one normalized grid, with select-to-pause/resume.

## Scope & altitude (coexistence)

This dashboard is the controller's **observability home** — read-mostly, plus
pause/resume convenience. It does **not** make TrackMuleBB a required hop: both
clients keep working standalone, and the cross-network *actuation brain*
(`coordinator/intents.py`, intent → "download the torrent instead") is unchanged
and sits beside it. Backends stay authoritative; the dashboard projects + resyncs
and owns no persistent transfer state (the SQLite store is only intent dedup).

MVP excludes: search, library/metadata dedup, cancel/delete, priority, queue
policy, backend lifecycle (start/stop), multi-host, UI auth.

## Architecture

```
adapters/        REST adapters → list_transfers() / pause() / resume() / health()
  rust.py          emulebb-rust  /api/v1   (X-API-Key)
  qbittorrent.py   qBittorrentBB /api/v2   (Authorization: Bearer)
model.py         UnifiedTransfer (frozen pydantic) + Backend/TransferState enums
state/projection.py   in-memory, namespaced per backend, async-safe
coordinator/transfers.py   per-backend poll loops → projection; pause/resume routing
ui/pages.py + theme.py + format.py   dense data-grid, dark slate + teal accent
app.py           wires adapters + projection + engine; starts/stops with the server
```

Single host, single user. Control plane binds `X_LOCAL_IP`; client URLs also
resolve via `X_LOCAL_IP` (never loopback on the split-tunnel machine).

## REST grounding (verified against the real code)

| | emulebb-rust | qBittorrentBB (5.2.1 fork) |
|---|---|---|
| Auth | `X-API-Key` header | `Authorization: Bearer <key>` |
| List | `GET /api/v1/transfers` (envelope `data.items`) | `GET /api/v2/torrents/info` |
| Pause/Resume | `POST .../transfers/{hash}/operations/{pause,resume}` | `POST /api/v2/torrents/{stop,start}` (`hashes=`) |
| Health | `GET /api/v1/status` | `GET /api/v2/app/version` |
| Speeds | KiB/s → ×1024 to B/s | bytes/s |
| Progress | 0..1 | 0..1 |
| ETA | seconds (`null` when idle) | `8640000` sentinel = ∞ → `None` |

## State mapping → `TransferState`

`DOWNLOADING · STALLED · SEEDING · PAUSED · QUEUED · CHECKING · COMPLETED · ERROR`

- **emulebb-rust** `downloading|queued|paused|completed|completing|hashing`
  (`stopped` already folded into `paused`). Derived **STALLED** when
  `downloading` with 0 transferring sources and 0 B/s. eD2K transfers never SEED
  (uploads live in a separate queue) and have no ERROR token.
- **qBittorrent** full vocabulary mapped (`*DL/*UP`, `stalled*`, `checking*`,
  `allocating/moving`, `error/missingFiles`); unknown → ERROR (logged).

## Sync engine

One async loop per backend (rust ~2 s, qBit ~1.5 s). Each poll returns a full
namespace snapshot that replaces that backend's slice of the projection; a failed
poll marks only that client unhealthy. Pause/resume route by the transfer-id
namespace (`ed2k:` / `bt:`) and apply optimistically pending the next refresh. The
UI re-renders from the projection on a ~1 s timer.

### Tracked deviation: full-poll vs delta-sync

For the first version the qBittorrent lane uses `GET /api/v2/torrents/info`
(full list, cleanly typed) instead of the delta `GET /api/v2/sync/maindata?rid=N`.
Delta-sync (with a merged raw-field cache) is the intended optimization and is
left as a follow-up; the adapter boundary already isolates the change.

## Quality baseline (day-1)

uv · Python ≥3.12 · **Ruff** lint+format (ANN = mandatory annotations) ·
**mypy `--strict`** + `pydantic.mypy` · pydantic v2 at every I/O boundary ·
`py.typed` · pre-commit (ruff + ruff-format + mypy) · GitHub Actions `quality.yml`
gating lint/format/types/tests.
