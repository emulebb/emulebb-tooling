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
- `workspaces\workspace\app\emulebb-main` is the preferred observable runtime
  oracle for eD2K/Kad parity because it carries the maintained MFC diagnostics
  surface. It is not a second product-development target. Changes are limited
  to diagnostics, deterministic test control, and buildability required for
  oracle use; do not evolve product or protocol behavior there.
- Stock eMule source and accepted protocol goldens remain the authority for wire
  and state-machine intent. `baseline/community-0.72a` is the frozen,
  seam-enabled executable stock lane. Its maintenance is limited to inert
  probes/adapters, narrow tracing, and required buildability fixes; normal
  runtime behavior, persistence, network behavior, and default control flow
  must not change.
- `tracing-harness/community-0.72a` is retired from active parity work. Do not
  add new runners, aliases, tests, or topology dependencies for it. Preserve
  historical work in Git and migrate or remove remaining consumers before the
  worktree is archived.
- aMule has two explicit roles. The parity lane uses one frozen stable release
  and records its exact revision plus any diagnostics-only patch revision. The
  moving upstream HEAD lane is source-analysis and future-interoperability
  evidence only; it is never silently substituted for the frozen parity lane
  and never gates a current parity claim.
- `ed2k-server` is an upstream-clean deterministic test dependency. Its code
  must follow upstream without emulebb-specific protocol behavior. CI,
  packaging, and test wiring may be carried locally when necessary, but packet,
  state-machine, and client-compatibility adaptation belongs in the harness or
  a scripted fixture. A result that depends on fork-only server behavior is not
  stock protocol-parity evidence.
- Rust metadata schema helpers are internal, bounded, backup-first
  infrastructure for known persisted test/soak profiles. They are never an
  end-user migration or recovery path.

## Protocol-Parity Evidence

The active goal is one evidence-driven Rust protocol-parity harness, not a
collection of independent test scripts. The harness must maintain one
machine-readable catalog of the supported eD2K and Kad variants and state
transitions. Each catalog entry identifies its starting state, stimulus,
expected wire/state result, authority, required evidence, deterministic runner,
optional live runner, exact build provenance, and current evidence status.
Named campaigns are selections from that catalog; they do not define competing
coverage or verdict models.

Use these evidence layers in order:

1. codec and transcript tests for packet, tag, boundary, malformed-input, and
   compatibility variants;
2. deterministic local state-machine tests with controlled time, faults, and
   exact ordered transitions;
3. deterministic local cross-client campaigns, with Rust versus MFC as the
   primary observable comparison and frozen stock/aMule lanes as independent
   references where applicable; and
4. public-network persisted-profile soaks for discovery and rare-state
   collection only.

A public finding must be reduced to a deterministic regression whenever the
state can be reproduced locally. Public-network success cannot replace missing
deterministic coverage.

Verdicts have strict meanings:

- `parity`: the required transition occurred on both selected clients and all
  required, causally attributed evidence was recorded and compared;
- `divergence`: comparable causal evidence exists on both sides and establishes
  an actual mismatch;
- `evidence-incomplete`: an action or transition may have occurred, but required
  evidence is absent, ambiguous, dropped, malformed, or cannot be attributed;
- `not-observed`: the required action or transition did not occur; and
- `intentional-difference`: an approved supported-scope difference with its
  authority and rationale recorded in the catalog.

`evidence-incomplete` and `not-observed` never count as parity, divergence, or
green coverage. A campaign reports the exact covered/required count and each
non-covered catalog entry. Zero recorded divergences without covered entries is
not progress or protocol evidence.

Before adding a runner or suite, map it to catalog entries and search the
existing harness. Every existing protocol test must ultimately be classified
as canonical coverage, a shared fixture/helper, a duplicate to remove, a
non-protocol product test, or historical material isolated from active Rust
parity campaigns. Do not preserve obsolete client aliases, report adapters, or
schema compatibility shims during this beta consolidation.

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
  record mapping/reachability evidence. The persisted native-Windows hide.me
  lane treats provider state as inherited operator state and remains read-only;
  it does not configure, repair, or bypass the provider.
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
evidence. WSL and Windows REST control stay on loopback unless a selected
scenario explicitly tests LAN control.

An explicitly selected native-Windows Rust-versus-MFC protocol-parity campaign
may use a narrower operator-approved exception to that direct-test baseline. It
may share only roots listed in ignored operator-local inputs and may admit a
download by exact eD2K hash and size when a prior SHA-256 is unavailable. Both
clients must use fresh isolated profiles and output-root incoming directories,
must never open or execute the downloaded payloads, and must compute SHA-256
after completion and require cross-client equality. That equality proves parity
between the two completed payloads; it does not establish content provenance or
trust. The campaign must remain bounded, tear down automatically, retain exact
local-only evidence, and leave the ordinary direct Rust beta requirements above
unchanged for every other workflow.

An explicitly selected persisted-profile diagnostic soak is a separate
discovery lane, not a parity-certification or release-proof campaign. It may run
until explicitly stopped and may use operator-owned MFC and Rust profile roots
outside the workspace output root under the core policy exception, provided
all of the following remain true:

- profile paths come only from ignored local input or explicit runtime
  arguments and never enter tracked files;
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
or tests. Retained local-only diagnostic evidence is intentionally unredacted
and may contain exact titles, terms, hashes, addresses, paths, identifiers, and
packet payloads. Never publish, upload, commit, or attach those artifacts to a
  public issue or pull request.

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
