# Suite Docker Delivery

Status: design / direction. Captured 2026-06-16. The Docker form of the eMuleBB
Suite bundle. Companion to [SUITE-INSTALLER](SUITE-INSTALLER.md) (the
Windows-local form); same TrackMuleBB brain, two targets.

## Model

A committed **`docker-compose.yml` driven by compose profiles** + a `.env`, with a
minimal `setup.sh`; TrackMuleBB's setup CLI can generate/update the compose
(`setup --target docker`) so there is **one source of truth, no wiring drift**.
TrackMuleBB runs as a **plain service** (no Docker socket). Docker is **rust-only**
for the eD2K core (MFC is Windows-only).

## Decisions (2026-06-16)

| # | Decision |
|---|---|
| 1 | **Our GHCR images:** rust + qBittorrentBB-nox are **linuxserver-style** (s6, `PUID`/`PGID`, `TZ`, `/config`+`/data`); TrackMuleBB + Bountarr are minimal. |
| 2 | **Single `/data` volume** (`torrents/ usenet/ ed2k/ media/`) shared by all → hardlink + atomic-move. **Model 1: eD2K through Arr** (rust = qBit-emulated client). |
| 3 | **Gluetun** (optional): only the P2P containers route through it; ports published on gluetun; control plane reached at `gluetun:<port>`. |
| 4 | **Compose lives in `trackmulebb/docker/`; TrackMuleBB is a plain service** (no `docker.sock`). "Install a component" = enable a profile + `docker compose up`. |
| 5 | **Bind-mounts under the project dir** (`./config/<app>`, `./data`) for self-containment; **Plex** in bridge + ports (claim token manual). |

## Images (GHCR) — the enabling prerequisite

Four custom images we publish to `ghcr.io/emulebb/*` (latest + versioned), built/
pushed by per-repo CI. **Without these the Docker bundle cannot start.**

| Image | Repo | Convention |
|---|---|---|
| `emulebb-rust` | emulebb-rust | linuxserver-style (s6, PUID/PGID, /config, writes downloads to `/data`) |
| `qbittorrentbb-nox` | qbittorrentbb | **headless nox Linux build** of the fork + linuxserver-style |
| `trackmulebb` | trackmulebb | minimal Python (uv); control plane on `X_LOCAL_IP` equivalent |
| `bountarr` | itlezy/bountarr | minimal Node (v22) |

Third-party images are upstream: Prowlarr/Sonarr/Radarr/SABnzbd (linuxserver.io),
Plex (official), Gluetun (`qmcgaw/gluetun`).

## Storage & permissions

- **One `/data` mount** for every download client + Arr + Plex →
  `torrents/ usenet/ ed2k/ media/`. Same path everywhere enables **hardlinks +
  atomic move**; Arr promotes all three networks to `media/`.
- `PUID`/`PGID`/`TZ` uniform across containers (set in `.env`).
- **Config/data are bind-mounts under the project dir** (`./config/<app>`,
  `./data`) — self-contained, inspectable, backup = copy the folder.

## Networking & Gluetun

- **Gluetun is optional** (not everyone runs a VPN). When **on**, only **rust +
  qBittorrentBB** use `network_mode: "service:gluetun"` (fail-closed killswitch —
  the Docker analog of the Windows hide.me split-tunnel). Control plane,
  Arr/Prowlarr, SAB, Bountarr, Plex stay on the normal network.
- **Port wiring (gluetun gotcha):** P2P containers have no own ports — publish
  **all** their ports (qbbb WebUI + BT listen; rust `/api/v1` + eD2K TCP + Kad UDP)
  **on the gluetun service**, and wire Arr/TrackMuleBB to **`gluetun:<port>`**.
- **Inbound (HighID):** use the **VPN provider's port-forwarding** (gluetun
  supports it for built-in providers) and auto-set the client's listen port;
  otherwise **LowID with a warning**. **UPnP does not work behind a VPN** (the
  gateway is the tunnel) — do not rely on it.
- **Provider:** any. **hide.me is not a built-in gluetun provider** → use gluetun's
  **custom** OpenVPN mode (supply hide.me's `.ovpn`); this means **no auto
  port-forwarding** for hide.me, and the custom config must be **validated**. For
  best inbound on Docker prefer a PF-capable built-in provider.
- **Gluetun down = the P2P clients are fully isolated** (incl. their API/WebUI) —
  safe by design; TrackMuleBB shows them offline.
- **Gluetun = no** is allowed freely (P2P on the normal network); the operator is
  then responsible for VPN/network safety elsewhere.

## Compose & profiles

- **Profiles per component** (`COMPOSE_PROFILES=rust,qbbb,trackmulebb,prowlarr,
  sonarr,radarr,sabnzbd,bountarr,plex,gluetun`) realise the selectable bundle
  without generating files. TrackMuleBB is always present; **>=1 P2P client**;
  dependency enforcement (Bountarr → Radarr/Sonarr).
- `setup.sh` (minimal): prompts → `.env` (components, Gluetun yes/no + provider,
  `PUID/PGID/TZ`, paths) → `docker compose up`.

```yaml
  # (illustrative skeleton, not the final file)
services:
  gluetun:                       # profile: gluetun
    image: qmcgaw/gluetun
    cap_add: [NET_ADMIN]
    ports:                       # P2P ports are published HERE
      - 8080:8080                # qbbb WebUI
      - 4711:4711                # rust /api/v1
      # + BT/eD2K/Kad listen ports
  qbittorrentbb:                 # profile: qbbb
    image: ghcr.io/emulebb/qbittorrentbb-nox
    network_mode: "service:gluetun"
    volumes: [./config/qbbb:/config, ./data:/data]
    environment: [PUID, PGID, TZ]
  emulebb-rust:                  # profile: rust
    image: ghcr.io/emulebb/emulebb-rust
    network_mode: "service:gluetun"
    volumes: [./config/rust:/config, ./data:/data]
  trackmulebb:                   # profile: trackmulebb (plain service, no socket)
    image: ghcr.io/emulebb/trackmulebb
    # reaches rust/qbbb at gluetun:<port>
```

## Relation to the Windows-local form

Same TrackMuleBB brain and the same selectable bundle; the difference is the
**network-safety mechanism** (Windows = hide.me split-tunnel in-app; Docker =
Gluetun namespace) and the **runtime substrate** (native processes vs containers).

## Tracked work

- GHCR images: `emulebb-rust`, `qbittorrentbb-nox`, `trackmulebb`, `bountarr`
  (per-repo CI). The enabling prerequisite.
- TrackMuleBB Docker delivery: compose + profiles + Gluetun wiring +
  compose-generation (`TMBB-FEAT-013`).
- The setup CLI's `--target docker` mode (`TMBB-FEAT-010`).
