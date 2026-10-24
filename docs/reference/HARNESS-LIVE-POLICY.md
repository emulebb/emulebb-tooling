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
- `repos/amule` is the managed official upstream aMule checkout and the moving
  interoperability target. Refresh it through workspace sync before current
  parity work and record its exact commit in retained evidence. Never silently
  substitute it for the fixed Community 0.72a regression baseline; campaigns
  report fixed-stock and moving-upstream results as distinct lanes.
- `ed2k-server` is the sole local deterministic harness server and an
  upstream-contribution reference. Keep it close to upstream, prefer
  harness-side adaptation, and keep server changes minimal, generic, and
  upstreamable. Local live and parity campaigns may select it; release and
  public-production campaigns do not.
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
- A full-tunnel host lane must prove split tunneling is disabled and must not
  call helpers that add application allow-list entries, excluded ranges, or
  other provider settings. Its local control planes use loopback while P2P
  remains bound through `BindInterface` with VPN Guard Block.
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

An explicitly selected native-Windows Rust-versus-MFC protocol-parity campaign
may use a narrower operator-approved exception to that direct-test baseline. It
may share only roots listed in ignored operator-local inputs and may admit a
download by exact eD2K hash and size when a prior SHA-256 is unavailable. Both
clients must use fresh isolated profiles and output-root incoming directories,
must never open or execute the downloaded payloads, and must compute SHA-256
after completion and require cross-client equality. That equality proves parity
between the two completed payloads; it does not establish content provenance or
trust. The campaign must remain bounded, tear down automatically, retain
sanitized evidence, and leave the ordinary direct Rust beta requirements above
unchanged for every other workflow.

An explicitly selected persisted-profile diagnostic soak is a separate
discovery lane, not a parity-certification or release-proof campaign. It may run
until explicitly stopped and may use operator-owned MFC and Rust profile roots
outside the workspace output root under the core policy exception, provided
all of the following remain true:

- profile paths come only from ignored local input or explicit runtime
  arguments and never enter tracked files or retained messages;
- hide.me is already active in full-tunnel mode, split tunneling is off, both
  P2P planes use `BindInterface`, both clients use VPN Guard Block, and the
  harness fails before launch rather than changing provider settings;
- local REST control uses loopback and stays separate from the guarded public
  P2P data plane;
- a truly empty Rust profile may be imported once from the selected MFC
  profile, while a nonempty current-schema Rust profile is validated and reused
  without automatic reset or reimport;
- every temporary MFC profile override is backup-first and recoverable after
  normal stop, launch failure, or stale-manifest recovery;
- campaign manifests, summaries, archived diagnostic segments, and selected
  retained evidence stay below `EMULEBB_WORKSPACE_OUTPUT_ROOT`, while generic
  workspace cleanup never owns the external profiles; and
- diagnostic storage, monitoring history, and retained payloads are bounded by
  explicit byte, age, and free-space limits. Missing required families, parse
  failures, sequence gaps, or dropped records make evidence inconclusive or
  failed rather than successful parity.

Discoveries from this lane require a separate bounded, reproducible campaign
before they support a parity, certification, release, or VPN-safety claim.

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
