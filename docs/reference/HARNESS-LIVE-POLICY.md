# Harness And Live Policy

Read the [Workspace Policy](../WORKSPACE-POLICY.md) first. This annex is
mandatory for harness code, baseline/tracing work, local live stacks,
public-network tests, soak/profile operation, VPN/bind behavior, and retained
live evidence.

## Ownership And Baselines

- `repos\emulebb-build-tests` owns shared test harness code and execution
  helpers. Repeatable live, UI, soak, profiling, monitoring, and evidence
  workflows are persisted Python scripts/modules; do not recreate them in
  PowerShell, batch, inline Python, or session scratchpads.
- Search existing `scripts` and `emule_test_harness` capabilities before adding
  a helper. Prefer an existing module, then extending the closest script, then a
  reusable module with a thin operator wrapper.
- `baseline/community-0.72a` is the seam-enabled parity/regression baseline.
  Its maintenance is limited to inert seams, deterministic probes/adapters,
  narrow tracing, and required buildability fixes; normal runtime behavior,
  persistence, network behavior, and default control flow must not change.
- `tracing-harness/community-0.72a` is the only sanctioned location for parity
  behavior that intentionally changes runtime decisions. It is neither a
  release branch nor the default regression baseline.
- `goed2k-server` is the deterministic harness server. `ed2k-server` has build
  and source-quality gates as an upstream-contribution reference; no live,
  parity, release, or production campaign selects it.
- Rust metadata schema helpers are internal, bounded, backup-first
  infrastructure for known persisted test/soak profiles. They are never an
  end-user migration or recovery path.

## Selected-Route Safety

Public-network P2P routing is always explicit. Direct mode intentionally uses
the host route and makes no anonymity claim. Selecting VPN mode creates a P0
fail-closed invariant: if the tunnel is unavailable, the product must emit zero
public P2P data-plane traffic over the direct route while local control remains
separate. Never fall back silently from VPN to direct.

- Public tests contact real eD2K/Kad servers, peers, searches, bootstrap nodes,
  or discovered peers. Local live-stack tests use only deterministic
  workspace-owned services. Contact with public infrastructure reclassifies a
  local run as public.
- VPN profiles use `BindInterface` and `VpnGuardMode=Block`. Do not put an
  interface name in `BindAddr`. Address-bound direct profiles use `BindAddr`,
  leave `BindInterface` empty, and keep VPN Guard off.
- Empty `VpnGuardAllowedPublicIpCidrs` is valid for interface-only protection;
  configured CIDRs additionally validate public exit addresses.
- Public VPN campaigns take provider connect, allow-list, check, and restore
  hooks from operator-local configuration. VPN mode must prove tunnel-down
  blocks off-tunnel data before a VPN-safe claim can be made.
- Public profiles enable main P2P UPnP when the selected route supports it and
  record mapping/reachability evidence. Native Windows VPN integration is not a
  forward development priority, but existing safety claims still require proof.
- On the operator split-tunnel machine, non-P2P services and control/probe
  traffic use inherited `X_LOCAL_IP` / `--lan-bind-addr`, never loopback or
  wildcard. Product runtime and other machines retain deliberate loopback and
  wildcard compatibility.
- `--lan-bind-addr` is the only harness name for that LAN concept. Do not
  reintroduce `--bind-addr`, `--rest-bind-addr`, or `--web-bind-addr`.
- Use `192.0.2.x` for documented LAN examples and `127.0.0.1` for canonical
  loopback examples. Use `localhost` only for explicit DNS, URL parsing, UNC,
  or compatibility cases.

A direct Rust beta public test must be explicitly selected, use a fresh isolated
profile with empty shared roots, accept only operator-approved hashes with exact
size and SHA-256, bound traffic and runtime, tear down automatically, and retain
evidence. WSL REST stays on loopback; Windows control follows the split-tunnel
LAN rule.

Never put real media titles or live search terms in tracked harness code, docs,
tests, or retained evidence.

## Persisted Rust Soak Workflow

Do not inspect or recreate launch logic first. From
`repos\emulebb-build-tests`, use:

```powershell
python scripts\start-rust-soak-profile.py --describe
python scripts\start-rust-soak-profile.py --seconds 86400
python scripts\rust-soak-control.py profile-status --include-vpn-status
python scripts\rust-soak-control.py stop-profile-launch
```

`--describe` is authoritative for the profile, staged executable, REST binding,
VPN configuration, bootstrap counts, launch command, and stop command. Required
environment variables must already be valid; never repair them inline.

## Evidence And Path Capability

- Choose evidence by changed surface. Protocol-adjacent work needs the
  appropriate baseline, golden, tracing, live-diff, or capture proof. Hosted CI
  does not replace local release proof.
- Use the workspace evidence-retention policy before pruning generated test,
  diagnostic, profile, or campaign artifacts.
- Only the active eMuleBB product under test may be treated as Windows
  long-path capable. Community clients, tracing/baseline trees, and aMule remain
  short-path unless their own implementations gain and prove support.
- Mixed-client suites keep profiles, incoming/temp directories, and libraries
  on short paths, preferably a throwaway VHD drive-letter root. Deep or
  folder-mounted VHD scenarios are eMuleBB-only and must not launch aMule or the
  community harness against those paths.

Static enforcement includes the shared `test_live_bind_policy_static.py` gate;
workspace output and environment assignment remain covered by the
`output-root` and `emulebb-env-override` audits.
