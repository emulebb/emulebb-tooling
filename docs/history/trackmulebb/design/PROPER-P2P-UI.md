# Proper p2p UI — depth pass over the dashboard

Builds on [`MVP-UNIFIED-TRANSFERS.md`](MVP-UNIFIED-TRANSFERS.md). The MVP was a
read-mostly transfers grid; this pass turns the UI into a proper eD2K client
shell. Scope is **eD2K (emulebb-rust) first**; every feature is backed by an
existing `/api/v1` endpoint (no core changes). qBittorrentBB parity and
add-by-link/categories are deliberately deferred.

## App shell (`ui/shell.py`)

A qBittorrent-style chrome reused by every page via the `app_shell(active, …)`
context manager:

- Left-drawer nav (Transfers / Search / Shared / Servers / Status / Settings).
  The Transfers page appends its status-filter list under the nav.
- Shared header with per-backend health pills (from `TransfersSync.health()`).
- A persistent bottom **status bar** (`ui/status_bar.py`): live session
  download/upload speed, session totals, active counts, eD2K HighID/LowID and Kad
  state, plus a 60-sample dl/ul **echart sparkline**. Fed by `GET /api/v1/stats`
  on the shell's refresh timer; dims on a transient REST error.

## Transfer depth (`ui/detail.py`, `ui/pages.py`)

- **Right-click context menu** on each transfer row (Details / Resume / Pause /
  Stop / Priority▸ / Recheck / Delete), emitted from a Quasar `q-menu` in the
  name cell back to Python via the table's `rowaction` event.
- **Priority** column + submenu → `PATCH /transfers/{hash}` (`auto`/`low`/
  `normal`/`high`). **Recheck** → `POST .../operations/recheck`. Both eD2K-only.
- **Detail right-drawer**: the ED2K **part-availability bar** (one flex segment
  per part, colored complete/requested/corrupted/gap) plus the **live sources
  table** (peer software, state, speed, parts, queue rank) with per-peer ops
  (browse / add-friend / ban) → `GET /transfers/{hash}/details` +
  `POST .../sources/{clientId}/operations/{op}`.

## Network control (`ui/servers.py`, `ui/settings.py`)

- **Servers page**: server list (`GET /servers`) with connect (`POST
  /servers/{endpoint}/operations/connect`), disconnect, add (`POST /servers`),
  and import server.met by URL. The server id is the `address:port` endpoint.
  Same page hosts a **Kad panel**: Start / Stop / Recheck-firewall
  (`POST /kad/operations/*`) over the live Kad status.
- **Settings page**: bandwidth / connection / network-toggle form bound to
  `GET /api/v1/app/preferences`; Save PATCHes only the changed fields (snake_case
  keys converted to the daemon's camelCase wire form).

## Invariants kept

Additive and never a required hop: the backends stay authoritative, the UI only
projects + actuates over REST, and the control plane binds `X_LOCAL_IP`. All new
adapter DTOs follow the existing `to_camel` + `extra="ignore"` pattern; pure
mappers (`parts_bar_html`, stats/details/server/preferences parsing) are unit
tested in `tests/test_mapping.py`.
