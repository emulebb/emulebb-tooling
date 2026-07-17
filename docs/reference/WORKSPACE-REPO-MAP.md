# Workspace Repository Map

This map documents the active repository roles in the canonical eMuleBB
workspace. Paths are written relative to `EMULEBB_WORKSPACE_ROOT`; do not replace
them with machine-local absolute paths in docs, scripts, or CI output.

`workspaces/workspace/repo-roles.json` is the generated machine-readable role
manifest for this map. It is written by `python -m emule_workspace sync` from
the Python topology in `repos/emulebb-build`.

## Primary Product Repositories

| Path | Branch | Role | Validation |
|---|---|---|---|
| `repos/emulebb` | `main` seed | Canonical app branch-store clone. | `validate` |
| `workspaces/workspace/app/emulebb-main` | `main` | Active app development worktree. | `build app --variant main` |
| `repos/emulebb-rust` | `main` | Forward Rust eD2K/Kad client and embedded SPA WebUI. | Cargo checks via workspace policy |
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
- `qbittorrentbb`, `qbit`, or `qbbb`:
  primary scope is `repos/qbittorrentbb`. Support scope is shared build,
  harness, and tooling docs only when the task needs workspace integration,
  live-wire, or policy context.

## Workspace Orchestration

| Path | Branch | Role | Validation |
|---|---|---|---|
| `repos/emulebb-build` | `main` | Workspace CLI, topology, packaging. | `pytest`; `validate` |
| `repos/emulebb-build-tests` | `main` | Native, live, controller, campaign tests. | `test python`; selected suites |
| `repos/emulebb-tooling` | `main` | Policies, hooks, docs, CI guards. | policy checks; MkDocs |

## Public Web And Org Repositories

| Path | Branch | Role | Validation |
|---|---|---|---|
| `repos/emulebb-pages` | `main` | Public GitHub Pages site. | static-site/link review |
| `repos/emulebb-org-profile` | `main` | GitHub organization profile README. | Markdown/rendering review |

## Product-Family Repositories

These repos are managed by the workspace but remain peer products or tools, not
subdirectories of the eMuleBB app.

| Path | Branch | Role | Validation |
|---|---|---|---|
| `repos/amutorrent` | `main` | aMuTorrent controller UI fork. | Node checks; live UI harness |
| `repos/qbittorrentbb` | `master` | qBittorrentBB companion fork. | product-family quality checks |
| `repos/goed2k-server` | `master` | Active Go eD2K server fork. | `go test ./...` |
| `repos/amule` | `master` | aMule fork for eMuleBB-published builds. | package/rebase checks |
| `repos/p2p-overlord-agents` | `develop` | Rust p2p-overlord agent code. | `cargo fmt --all --check` |
| `repos/p2p-overlord-be` | `develop` | p2p-overlord backend/coordinator. | `npm run quality` |
| `repos/p2p-overlord-tooling` | `develop` | p2p-overlord scenario catalog and pytest tooling. | future shared campaign adapter |

`p2p-overlord-tooling` is managed from the `emulebb` organization. Its test
suite remains separate until the shared campaign-core decision is implemented.

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

## Analysis Repositories

Analysis repos are source-provenance and comparison inputs. They are managed by
setup, but they are not edited as part of normal product work.

| Path | Role |
|---|---|
| `analysis/community-0.60` | Community eMule 0.60 reference |
| `analysis/community-0.72` | Community eMule 0.72 reference |
| `analysis/mods-archive` | Archived mod source corpus |
| `analysis/stale-v0.72a-experimental-clean` | Historical eMuleBB branch snapshot for comparison |
| `analysis/emuleai` | eMuleAI comparison source |

## GitHub Repository Governance

The GitHub organization uses these repo classes for settings consistency:

| Class | Repositories |
|---|---|
| Product | `emulebb`, `emulebb-rust`, `qbittorrentbb`, `amutorrent` |
| Build, test, tooling, docs | `emulebb-build`, `emulebb-build-tests`, `emulebb-tooling`, `.github`, `emulebb.github.io` |
| Dependency forks | `emulebb-*` dependency forks under `repos/third_party` |
| Research, archive, and mirrors | `emulebb-mods-archive`, `emulebb-ai`, `amule`, `goed2k-server`, `JEmuleServer`, p2p-overlord repos |

GitHub surfaces:

- Product issues/discussions belong on `emulebb`; aMuTorrent remains a
  product-family peer unless promoted to first-class roadmap tracking.
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
  or after dependency lockfile changes in p2p-overlord or `goed2k-server`.
- Run `python -m emule_workspace refresh-product-family-rebases` after the
  scheduled aMule or aMuTorrent upstream-rebase workflows publish rewritten
  fork history. The command fetches `origin` for `repos/amule` and
  `repos/amutorrent`, then refreshes the local branch only when the worktree is
  clean and local `HEAD` exactly matched the pre-fetch remote-tracking ref. If
  local commits or file changes exist, it stops and reports the repo for manual
  review instead of resetting work.
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
  `goed2k-server`, p2p-overlord, or shared contracts. Use
  `--product-family-tier quick` for fast smoke checks and `full` before broad
  product-family release proof. Plain `validate` remains the default eMuleBB
  workspace gate.
