# Suite Bundle & Installer

Status: split current/future direction. Updated 2026-07-05 for the stable
`0.7.3` release path.

For stable `0.7.3`, the current installer remains the proven
PowerShell suite bootstrap:

1. Pages `install.ps1` is a small wrapper for the GitHub Release
   `Bootstrap-eMuleBBSuite.ps1` asset.
2. `Bootstrap-eMuleBBSuite.ps1` resolves the matching eMuleBB and aMuTorrent
   package assets, then invokes the packaged `Install-eMuleBBSuite.ps1`.
3. The shipped bundle is eMuleBB MFC + aMuTorrent + the local Arr plumbing. It
   does **not** install qBittorrentBB, emulebb-rust, TrackMuleBB, `uv`, or the
   Python setup CLI.

The TrackMuleBB/`uv`/Python installer design below is future `0.8.*`-program
direction only (it begins after `0.7.3` ships). It must not be described as the
current Pages one-liner until it is built, packaged, and release-proven.

Governance companions: [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md),
[PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md),
[API-V1-COMPATIBILITY](API-V1-COMPATIBILITY.md),
`plans/ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md`.

## Current 0.7.3 Goal

A release-stable Windows bundle that closes the `0.7.x` feature line with the
existing PowerShell installer: eMuleBB MFC as the eD2K/Kad core, aMuTorrent as
the frozen `0.7.3` controller companion, and the local Arr setup scripts. The
`0.7.x` path is stabilization-only and avoids new product surface.

## Future Goal

A **ready-to-use bundle** that combines our P2P/Usenet download stack with the Arr
automation stack in one setup: emulebb-rust (or eMuleBB MFC on Windows),
qBittorrentBB, TrackMuleBB, the Arr stack, SABnzbd, Bountarr, and (Docker) Plex.
**Self-contained** in the install directory, **no interference** with the host,
with all inter-app connections **auto-wired**.

## Future Bundle Composition

Two tiers, by who can install/wire them reliably:

| Tier | Components | Install |
|---|---|---|
| **Ours (auto-scripted)** | emulebb-rust, eMuleBB MFC (Windows only), qBittorrentBB, TrackMuleBB, Bountarr | installed + fully auto-wired by TrackMuleBB's setup |
| Third-party (manual, phase 1) | Arr, SABnzbd, Plex (Docker) | manual install + docs; base settings pre-configured (paths/language/wiring) |

- **Phasing (decision 2026-06-16):** phase 1 fully automates *our* components and
  **pre-configures base settings** (paths/language/wiring) for the rest; deeper
  third-party install automation comes later.
- **eD2K core:** on Windows the bundle offers **MFC or emulebb-rust** (selectable);
  the strategic direction replaces the eMule backend with emulebb-rust. Docker is
  **rust-only** (MFC is Windows-only).
- **Bountarr** is ours but needs the Arr stack (it pulls Radarr/Sonarr as a
  dependency) and is the **only Node** component (Node confined to Bountarr; the
  rest is Python).

## Future Selection Rules

- **TrackMuleBB is always installed; its start is optional** (additive, never a
  required hop — clients work standalone).
- Components are **selectable**; the selector **enforces dependencies** (e.g.
  Bountarr → Radarr/Sonarr; SAB → a Usenet indexer in Prowlarr).
- **At least one P2P download client** must be selected (emulebb-rust / eMuleBB MFC
  / qBittorrentBB). SABnzbd (Usenet) is additive and does not satisfy the rule
  alone.
- Whether optional-start applies to non-controller components too is **TBD**.

## Future Delivery Forms (same TrackMuleBB brain, two targets)

- **Windows-local:** a later `install.ps1` minimal bootstrap → TrackMuleBB Python
  **setup CLI** does the native install.
- **Docker:** a committed `docker-compose.yml` driven by **compose profiles**
  (`COMPOSE_PROFILES=rust,qbbb,arr,sab,gluetun`) + a tiny `setup.sh` (prompts →
  `.env`, picks profiles, `up`). TrackMuleBB's CLI can generate/update this compose
  (`setup --target docker`) so there is **one source of truth, no wiring drift**.
  - **Gluetun yes/no** is the Docker network-safety mechanism: when on, **only the
    P2P containers** (rust, qbbb) route through Gluetun (`network_mode:
    service:gluetun`, fail-closed) — the Docker analog of the hide.me split-tunnel.
    Control plane, Arr, SAB, Bountarr, Plex stay on the normal network. Any
    Gluetun-supported VPN provider.
  - **Plex** is Docker-only (on Windows users run Plex natively); pre-wired
    library paths + Bountarr token, but the **plex.tv claim** stays a manual step.

## Future Two-stage Installer (Windows-local)

1. **Future `install.ps1` (minimal bootstrap, on pages):** download the **`uv`** binary
   directly into the install dir, fetch the TrackMuleBB setup, and invoke its CLI.
   Nothing else (no per-product download/wiring in the ps1).
2. **TrackMuleBB setup CLI (Python, in the `trackmulebb` repo):** the real
   installer — component selection, install, **auto-wiring of every connection**
   (API keys, Prowlarr/Arr/download-client registration, the TrackMuleBB
   indexer-exclusion tag), profile import, and start.

### CLI shape

- **TUI** (rich, interactive) by default; **non-interactive** via flags + a
  declarative **`suite.toml`** (reproducible, CI-able).
- **CLI owns install/lifecycle; the web UI owns app settings only** (never
  installation). Add a component later = re-run the CLI.
- Lifecycle: **install / update / repair** (no uninstall command — removal = delete
  the self-contained dir, by design). Initial phase = install only.

## Self-contained & host isolation

- **Everything under the install dir:** runtimes, component binaries, config, data,
  state, logs.
- **Python via `uv`, only-managed:** the bootstrap puts the `uv` binary in the
  install dir; `uv python install <pinned> --python-preference only-managed` uses a
  standalone CPython and **never touches or requires a system Python**. `UV_*` dirs
  point inside the install dir. No global PATH, no admin.
- **Node only for Bountarr:** TrackMuleBB downloads a self-contained Node (v22+)
  into the install dir when Bountarr is selected; never global.
- **Data paths:** default under the install dir, **overridable at setup** (large
  media can live on another disk).
- **Firewall:** the setup does a **basic check** and, on Windows with the firewall
  active, **points the user to documentation** (UPnP/NAT-PMP preferred; manual
  inbound rules as a documented, opt-in admin step) — never a silent system change.
- **No Windows services** (user processes); avoid local port clashes.

## Profile import

- Optional **import of existing profiles**: copy only an **allowlist of relevant
  keys** and **rewrite the path parameters** to the install-dir layout. One-time
  **copy + rewrite**, never a link; the original profile is untouched.
- Phase 1 scope: **P2P clients first** (eD2K profile for eMuleBB/rust +
  qBittorrentBB), the rest later. **Cross-core mapping** (MFC profile ↔ rust) is
  **TBD**.

## Networks & bandwidth

The bundle spans **three networks** — eD2K (rust/MFC), BitTorrent (qBittorrentBB),
Usenet (SABnzbd). TrackMuleBB is the **single pane**: unified transfers/search,
**dynamic global bandwidth coordination** (rebalances per-client limits under a
configurable global cap; upload-coordination is eD2K+BT only since Usenet is
download-only), and cross-network **dedup** (see TrackMuleBB backlog). Search
aggregates the clients natively + Prowlarr (excluding the tagged TrackMuleBB
indexers); results merge by the metadata-fabric equivalence map, falling back to
exact-size + name.

## Migration / status

- For stable `0.7.3` and `0.7.x`, Pages `install.ps1` is the release
  bootstrap wrapper for `Bootstrap-eMuleBBSuite.ps1`.
- After `0.7.3`, `install.ps1` may become the TrackMuleBB minimal bootstrap;
  `suite-manifest.json` then moves into TrackMuleBB (a bundled default + an
  optional remote-override copy on pages). The setup logic lives in
  `trackmulebb` (`setup/` CLI + `web/` UI + `coordinator/`).
- **Scaffold:** the TrackMuleBB setup CLI and the bundle wiring are not built yet;
  the org README one-liner stays on the tested stable bootstrap until this is
  validated.
- Tracked work: TrackMuleBB `TMBB-FEAT-*` (search/dedup/bandwidth/SAB/settings/
  setup-CLI/profile-import); the cores' `/api/v1` capability work (FEAT-122,
  RUST/QBBB items).
