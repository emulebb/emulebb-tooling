# Local suite bring-up (emulebb-rust + TrackMuleBB)

A repeatable, one-command local install of the forward core: it builds the
**emulebb-rust** daemon, runs it bound to the VPN tunnel with the REST control
plane on `X_LOCAL_IP`, seeds Kad + eD2K servers live from **emule-security**, and
starts **TrackMuleBB** against it (eD2K-only; qBittorrentBB disabled).

This is an **interim seed** of the planned TrackMuleBB setup CLI
([`emulebb-tooling/docs/active/SUITE-INSTALLER.md`](../../active/SUITE-INSTALLER.md),
`TMBB-FEAT-006..012`). It is a
dev/local-run helper, not the shipped installer.

Tool: `tools/local-suite/` — `suite.py` + `suite.toml`
(tunables) + `emulebb-rust.toml.tmpl` (rendered config template).

## Design rules

- **No hardcoded IPs.** The control plane uses `$X_LOCAL_IP`; the P2P data plane
  binds by interface **name** (`vpn_interface` in `suite.toml`, live-resolved to
  the tunnel IPv4 + `IP_UNICAST_IF` ifIndex); Kad nodes (`nodes.dat`) and eD2K
  servers (`server.met`) are fetched live from emule-security — even the eD2K seed
  server is read from `server.met` at start, never authored.
- **No hardcoded paths.** Repos resolve from `$EMULEBB_WORKSPACE_ROOT`; all
  generated output (rendered config, runtime SQLite/identity, logs, PIDs, API key)
  goes under `$EMULEBB_WORKSPACE_OUTPUT_ROOT/local-suite/`.
- **Fail-closed VPN.** `start` aborts if the VPN interface is down; the daemon runs
  with `vpnGuard` enabled (`mode = Block`).

## Prerequisites

- `cargo` + Rust toolchain (to build emulebb-rust), `uv`, Python ≥ 3.12.
- Machine env: `EMULEBB_WORKSPACE_ROOT`, `EMULEBB_WORKSPACE_OUTPUT_ROOT`,
  `X_LOCAL_IP` (read-only — never set these here).
- The VPN tunnel up; its adapter name in `suite.toml` `vpn_interface` (default
  `hide.me`).

## Steps

Run from the trackmulebb repo root. `--with psutil` supplies the one extra dep the
orchestrator needs beyond trackmulebb's own.

```bash
# 1. Build the daemon (output under $EMULEBB_WORKSPACE_OUTPUT_ROOT)
uv run --with psutil python tools/local-suite/suite.py build

# 2. Bring the suite up (preflight -> render -> daemon -> seed -> trackmulebb)
uv run --with psutil python tools/local-suite/suite.py start

# 3. Check health any time
uv run --with psutil python tools/local-suite/suite.py status

# 4. Tear everything down (graceful daemon shutdown + full process-tree kill)
uv run --with psutil python tools/local-suite/suite.py stop
```

After `start`:

- REST control plane: `http://$X_LOCAL_IP:4111/api/v1`
- TrackMuleBB UI: `http://$X_LOCAL_IP:8770`

## What `start` does

1. **Preflight** (fail-closed): VPN interface up + `X_LOCAL_IP` present.
2. **Seed server**: fetch `server.met`, take the first endpoint to enable the
   eD2K/Kad subsystem (it is disabled with an empty server list at config time).
3. **Render** `emulebb-rust.toml` from the template into the output root.
4. **Launch** the daemon; wait for REST `200`.
5. **Seed the network over REST** (order matters — the live Kad DHT only exists
   after `connect_ed2k` builds the eD2K runtime): import `server.met` → connect →
   `kad start` → import `nodes.dat` (retried until the DHT is up).
6. **Launch** TrackMuleBB pointed at the daemon (qBittorrentBB disabled).

## Verify the VPN binding

The data plane must sit on the tunnel and the control plane on `X_LOCAL_IP`:

```bash
# eD2K TCP + Kad UDP on the tunnel IPv4; REST on X_LOCAL_IP
netstat -ano | grep -E ":(4662|4672|4111) "
```

Expected: `4662`/`4672` on the tunnel address, `4111` on `$X_LOCAL_IP`.

## Notes

- **LowID / `kadConnected:false` is expected** behind a commercial VPN with no
  inbound port-forward. Downloads still work (LowID + buddy). HighID needs a VPN
  plan that supports inbound port mapping.
- `vpn_interface` is the only machine-specific knob; override it in `suite.toml`
  if your tunnel adapter name differs.
- The orchestrator depends on `httpx` (already a trackmulebb dependency) and
  `psutil` (supplied via `--with psutil`).
