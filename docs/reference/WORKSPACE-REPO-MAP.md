# Workspace Repository Map

This map documents the active repository roles in the canonical eMuleBB
workspace. Paths are written relative to `EMULEBB_WORKSPACE_ROOT`; do not replace
them with machine-local absolute paths in docs, scripts, or CI output.

`workspaces/workspace/repo-roles.json` is the generated machine-readable role
manifest for this map. It is written by `python -m emule_workspace sync` from
the Python topology in `repos/emulebb-build`. The default `core` profile is the
supported product, compatibility, diagnostics, and release surface. Public
presence repositories require an explicit optional profile. Historical analysis
sources are not materialized as workspace repositories.

## Primary Product Repositories

| Path | Branch | Role | Validation |
|---|---|---|---|
| `repos/emulebb` | `main` seed | Canonical app branch-store clone. | `validate` |
| `workspaces/workspace/app/emulebb-main` | `main` | Maintained MFC app worktree for diagnostics and critical fixes. | `build app --variant main` |
| `repos/emulebb-rust` | `main` | eMuleBB Rust active beta eD2K/Kad client and embedded SPA WebUI. | Cargo checks via workspace policy |
| `workspaces/workspace/app/emulebb-community-baseline` | `baseline/community-0.72a` | Community baseline worktree. | compare/live-diff |
| `workspaces/workspace/app/emulebb-community-tracing-harness` | `tracing-harness/community-0.72a` | Tracing baseline worktree. | harness tests |

## Project Focus Map

Use this map after the operator names an active project. Start in the primary
scope and pull in support repos only when the task needs them.

- `emulebb rust`, `rust`, or `emulebb-rust`:
  primary scope is `repos/emulebb-rust`, including the embedded SPA WebUI.
  Support scope is `repos/emulebb-build-tests` for harnesses and live profile
  scripts, `repos/emulebb-tooling/docs/products/emulebb-rust` for docs, and
  `repos/emulebb-build` for orchestration.
- `emulebb mfc`, `mfc`, or `emulebb`:
  primary scope is `workspaces/workspace/app/emulebb-main`. Support scope is
  `repos/emulebb` as branch-store only, `repos/emulebb-build` for orchestration,
  `repos/emulebb-build-tests` for harnesses, and
  `repos/emulebb-tooling/docs/products/emulebb-mfc` for docs.
## eD2K Reference Terminology

Use these operator terms exactly in protocol audits and source comparisons.
Every path is relative to `EMULEBB_WORKSPACE_ROOT`; the Lugdunum evidence is a
read-only sibling outside the canonical workspace source boundary.

- `aMule` means `repos/amule`, the managed `amule-org/amule` upstream
  reference.
- `stock eMule` means `repos/emule-stock`, the community eMule 0.72 stock
  reference.
- `eD2K Rust server` means `repos/ed2k-server`, the managed upstream-aligned
  fork and sole local deterministic server.
- `Lugdunum decompiled` means
  `../eMule-server/lugdunum/lugdunum_eserver_17.15_linux/decompiled`, external
  decompiled Lugdunum 17.15 protocol evidence with no Git synchronization
  contract.

For any current-state comparison, refresh the relevant Git remote refs first.
Only fast-forward a clean tracking branch; stop and report rewritten or
divergent history instead of resetting, rebasing, or merging it implicitly.
Keep `repos/amule` current with `origin/master`; keep `repos/ed2k-server`
current with `origin/master` and review `upstream/master` before merging it.

## Workspace Orchestration

| Path | Branch | Role | Validation |
|---|---|---|---|
| `repos/emulebb-build` | `main` | Workspace CLI, topology, packaging. | `pytest`; `validate` |
| `repos/emulebb-build-tests` | `main` | Native, live, controller, campaign tests. | `test python`; selected suites |
| `repos/emulebb-tooling` | `main` | Policies, hooks, docs, CI guards. | policy checks; MkDocs |

## Product-Family Repositories

Core entries are managed by normal synchronization. Paused or historical peer
products require explicit work and are not materialized by the core profile.

| Path | Branch | Role | Validation |
|---|---|---|---|
| `repos/ed2k-server` | `master` | Sole local deterministic ED2K server and upstream-aligned Rust reference fork. | workspace build, harness, and quality checks |
| `repos/amule` | `master` | Managed official aMule upstream and moving parity reference. | clean fast-forward sync; record tested SHA in parity evidence |
| `repos/emule-stock` | `v0.72a` | Clean stock eMule compatibility oracle. | clean fast-forward sync; source/parity comparison |

Historical documentation does not make retired product-family checkouts part
of normal materialization or validation.

## Third-Party Forks

The workspace owns these dependency forks because eMuleBB needs repeatable
Windows builds and pinned update policy. They are not application feature repos.

| Path | Role |
|---|---|
| `repos/third_party/emulebb-cryptopp` | Crypto++ fork pinned for eMuleBB native builds |
| `repos/third_party/emulebb-id3lib` | ID3 library fork with eMule-compatible patch state |
| `repos/third_party/emulebb-libpcpnatpmp` | libpcpnatpmp fork used by MiniUPnP-related NAT traversal work |
| `repos/third_party/emulebb-mbedtls` | Mbed TLS fork and submodules for HTTPS/TLS dependencies |
| `repos/third_party/emulebb-miniupnp` | MiniUPnP fork used by eMuleBB and standalone upnpc packages |
| `repos/third_party/emulebb-nlohmann-json` | Header-only JSON dependency fork |
| `repos/third_party/emulebb-resizablelib` | Native UI layout helper fork |
| `repos/third_party/emulebb-zlib` | zlib fork for native compression dependencies |

## Historical Analysis Sources

Historical branches and external peer projects are provenance, not canonical
workspace repositories. Normal materialization never clones them. Use retained
commit references and documentation first; inspect an exact remote revision only
for an explicitly named comparison, without adding it to workspace topology.

- `stale/v0.72a-experimental-clean` remains historical eMuleBB Git provenance.
- `ModderMule/emule-qt` remains an external comparison source.

## GitHub Repository Governance

The GitHub organization uses these repo classes for settings consistency:

| Class | Repositories |
|---|---|
| Active / maintained products | `emulebb-rust`, `emulebb` |
| Reference / harness | `ed2k-server`, `amule` |
| Build, test, tooling, docs | `emulebb-build`, `emulebb-build-tests`, `emulebb-tooling`, `.github`, `emulebb.github.io` |
| Dependency forks | `emulebb-*` dependency forks under `repos/third_party` |
| Research, archive, and mirrors | `emulebb-mods-archive`, `emulebb-ai`, `trackmulebb`, `JEmuleServer`, p2p-overlord repos |

GitHub surfaces:

- Current product issues belong on the owning `emulebb-rust` or `emulebb`
  repository. Paused experiments do not accept normal issue intake.
- Build, test, tooling, and docs repos keep issues enabled for active work
  intake; repo projects and wikis are non-authoritative.
- Dependency fork issues, projects, discussions, and wikis are disabled unless
  a fork needs active upstream-facing maintenance.
- Research, archive, and mirror repo surfaces stay off unless the repo owns
  active product-family work.

All non-archived public repos should have Dependabot alerts, Dependabot security
updates, secret scanning, and push protection enabled where GitHub supports
those features. Official eMuleBB release tag rules target `emulebb-v*` only;
nightly tags such as `emulebb-nightly-*` must remain workflow-managed.

License metadata is provenance, not decoration. Repos with missing or
`NOASSERTION` license metadata must not receive new license files until the
correct upstream or project license is identified. For dependency forks, record
the upstream project, fork purpose, pinned branch, and known license source in
the repo README or this map before making legal metadata changes.

## Operational Rules

- Run `python -m emule_workspace sync` after topology changes so generated
  manifests, including `repo-roles.json`, and shared hook configuration
  converge.
- Run `python -m emule_workspace prepare-product-family` after materialization
  or after dependency lockfile changes in `ed2k-server`.
- Run `python -m emule_workspace build ed2k-server --config Release --platform
  x64` to build the Linux-only Rust server through WSL on Windows (or native
  Cargo on Linux) and stage the candidate binary below
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\tools\ed2k-server\bin`. This command does not
  start the server.
- Run `python -m emule_workspace workspace-status` before release and broad
  testing to inspect dirty state, branches, upstreams, and ahead/behind counts
  across all managed repos.
- Run `python -m emule_workspace cleanup --profile routine` before large test
  campaigns when generated state contains stale reports, payloads, caches, or
  Windows path anomalies.
- Use [Evidence Retention](EVIDENCE-RETENTION.md) before pruning large
  generated diagnostics, profiling runs, release-campaign output, or scratch
  progress notes.
- Use explicit cleanup scopes for broader hygiene:
  `--include-product-family-outputs` prunes generated outputs such as
  `node_modules`, Rust `target`, and product-family dist folders;
  `--include-root-legacy-state` removes old root-level generated state; and
  `--include-legacy-root-logs` removes retired root workspace logs.
- Run `python -m emule_workspace validate --include-product-family
  --product-family-tier quality` when a product-family change touches
  `ed2k-server` or shared contracts. Use
  `--product-family-tier quick` for fast smoke checks and `full` before broad
  product-family release proof. Plain `validate` remains the default eMuleBB
  workspace gate.
