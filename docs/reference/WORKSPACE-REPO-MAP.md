# Workspace Repository Map

This map documents the active repository roles in the canonical eMuleBB
workspace. Paths are written relative to `EMULE_WORKSPACE_ROOT`; do not replace
them with machine-local absolute paths in docs, scripts, or CI output.

`workspaces/workspace/repo-roles.json` is the generated machine-readable role
manifest for this map. It is written by `python -m emule_workspace sync` from
the Python topology in `repos/emulebb-build`.

## Primary Product Repositories

| Path | Branch | Role | Validation |
|---|---|---|---|
| `repos/emulebb` | `main` seed | Canonical app branch-store clone. | `validate` |
| `workspaces/workspace/app/emulebb-main` | `main` | Active app development worktree. | `build app --variant main` |
| `workspaces/workspace/app/emulebb-community-baseline` | `baseline/community-0.72a` | Community baseline worktree. | compare/live-diff |
| `workspaces/workspace/app/emulebb-community-tracing-harness` | `tracing-harness/community-0.72a` | Tracing baseline worktree. | harness tests |

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
| `repos/goed2k-server` | `master` | Active Go eD2K server fork. | `go test ./...` |
| `repos/amule` | `master` | aMule fork for eMuleBB-published builds. | package/rebase checks |
| `repos/p2p-overlord-agents` | `develop` | Rust p2p-overlord agent code. | `cargo fmt --all --check` |
| `repos/p2p-overlord-be` | `develop` | p2p-overlord backend/coordinator. | `npm run quality` |

`p2p-overlord-tooling` is not part of the active managed topology. Its future
role is intentionally deferred until the shared campaign-core decision is made.

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

## Operational Rules

- Run `python -m emule_workspace sync` after topology changes so generated
  manifests, including `repo-roles.json`, and shared hook configuration
  converge.
- Run `python -m emule_workspace prepare-product-family` after materialization
  or after dependency lockfile changes in p2p-overlord or `goed2k-server`.
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
