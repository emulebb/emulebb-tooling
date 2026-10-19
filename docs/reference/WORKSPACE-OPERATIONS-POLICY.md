# Workspace Operations Policy

Read the [Workspace Policy](../WORKSPACE-POLICY.md) first. This annex is
mandatory for materialization, topology, shared orchestration, packaging,
managed forks, workspace documentation/policy, normalization, and automation
runtime work.

## Layout And Ownership

- `repos\emulebb-tooling` owns shared policy, helper docs, hooks, and static
  audits. `repos\emulebb-build` owns topology, materialization, worktrees,
  dependency pins, build/validation/package/release orchestration, and the
  workspace lock. `repos\emulebb-build-tests` owns shared harness code.
- `workspaces\workspace\deps.json` and `repo-roles.json` are generated
  contracts. Consumers use `workspace.repos`; the deterministic server resolves
  through `workspace.repos.ed2k_server`. Selected repository profiles are
  recorded in both contracts, and non-core repositories are exposed separately
  rather than implied by paths. Consumers do not reconstruct old names or
  establish an independent topology authority.
- The canonical MFC worktrees are `emulebb-main`,
  `emulebb-community-baseline`, and `emulebb-community-tracing-harness` on
  topology-defined branches. `repos\emulebb` is their branch-store anchor.
- Retired pre-rename `eMule*` paths are historical references only.
- Output-root children are `builds`, `logs`, `reports`, `artifacts`,
  `packages`, `release`, `tmp`, `tools`, `cache`, and `profiles`.
  Canonical build roots are
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\app`,
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\tests`,
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\amule`,
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\third_party`, and the Rust targets.
  Package-only generated inputs use
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\packages\build`. Runtime tool payloads use
  `tools`, including `tools\amule`. Third-party orchestration prefers
  `builds\third_party`.
- `repos\ed2k-server` is the sole local deterministic ED2K server and an
  upstream-contribution reference. Follow upstream closely, prefer harness-side
  adaptation, and keep server changes minimal, generic, and upstreamable. Its
  candidate stages under `tools\ed2k-server\bin`; retired Go-server providers
  are not selectable workspace infrastructure.

Python topology in `repos\emulebb-build\emule_workspace` is the source of truth.
`python -m emule_workspace validate` fails generated-contract drift. Setup and
sync configure the shared hook and must not overwrite dirty managed work.

## Environment And Tooling

- Never override an already-present `EMULEBB_*` variable. Required
  `EMULEBB_WORKSPACE_ROOT` and `EMULEBB_WORKSPACE_OUTPUT_ROOT` are read exactly;
  the latter remains outside the workspace.
- `EMULEBB_RELEASE_VERSION` selects release orchestration; its default is pinned
  by `emulebb-build`.
- Windows is authoritative for WSL launches from this workspace. Persisted
  Python launchers may translate valid roots and derive a separate
  `builds\rust\target-wsl`, recording the mapping without changing the parent.
- `X_LOCAL_IP` crosses into WSL only for LAN-bound control/probe traffic.
  Loopback-only control planes may omit it.
- Diagnostic, package, VM-lab, and documentation environment knobs remain owned
  by their orchestration modules. Diagnostics use
  `EMULEBB_ENABLE_STARTUP_DIAGNOSTICS`,
  `EMULEBB_ENABLE_PACKET_DIAGNOSTICS`,
  `EMULEBB_ENABLE_UPLOAD_SLOT_DIAGNOSTICS`,
  `EMULEBB_ENABLE_DOWNLOAD_SLOT_DIAGNOSTICS`,
  `EMULEBB_ENABLE_BAD_PEER_DIAGNOSTICS`, and
  `EMULEBB_ENABLE_KAD_DIAGNOSTICS`. Package staging uses
  `EMULEBB_PACKAGE_ROOT_NAME`, `EMULEBB_RELEASE_ASSET_ROOT_NAME`, and
  `EMULEBB_RUNTIME_SCRIPT_PATHS`. The VM lab uses
  `EMULEBB_VM_TEST_PASSWORD`, `EMULEBB_VM_HIDE_ME_SETTINGS_PATH`,
  `EMULEBB_OFFLINE_SOFTWARE`, `EMULEBB_OFFLINE_SYSTEM`, and
  `EMULEBB_OFFLINE_DEFAULT_USER`.
- Toolchain overrides
  (`EMULEBB_VS_PLATFORM_TOOLSET`, `EMULEBB_MSYS2_ROOT`,
  `EMULEBB_CMAKE_GENERATOR`, `EMULEBB_CMAKE_PLATFORM`) are shell/CI diagnostic
  inputs only and require recorded justification for release or CI use.
- `NO_MKDOCS_2_WARNING` may silence the MkDocs upgrade notice.

## Build And Validation

- Interactive build, validation, test, live-test, and packaging commands go
  through `python -m emule_workspace`. Never run competing operations or direct
  MSBuild from app/test worktrees.
- Changes receive scoped validation and the smallest relevant build/test set.
  Toolchain, dependency-pin, build-system, and broad integration changes receive
  the relevant full matrix.
- Routine validate runs build, branch, dependency, documentation-path,
  PowerShell-boundary, entrypoint, warning, localization, English-language, and
  normalization audits. `check-clean-worktree.py` is reserved for CI,
  release-prep, or explicit hygiene work.
- Prefer build-level fixes over third-party source edits when the issue is
  orchestration, toolchain, or warning policy.

## Managed Repositories

- The default `core` profile contains the active Rust product, the MFC seed and
  all three diagnostic/release worktrees, their required third-party forks,
  workspace support repos, the single aMule reference, the stock eMule 0.72
  reference, and the sole local Rust ED2K server. MFC remains buildable and
  shippable for diagnostics and critical fixes; it is not a historical-only
  lane.
- Public-presence repositories and historical analysis repositories are explicit
  optional profiles. Normal materialization and synchronization must not pull
  archived, stale, paused, frozen, or unrelated product-family repositories.
  Unrelated product families stay outside the core profile.
- Supporting repos use setup-pinned branches. `stale/*` and
  `analysis\stale-v0.72a-experimental-clean` are historical-only unless a task
  explicitly selects the historical-analysis profile for comparison.
- Build output stays outside source trees. CMake uses out-of-source output below
  the output root, Go tools stage below `tools\<fork>`, and Rust follows the
  [Rust Product Policy](../products/emulebb-rust/reference/AGENT-POLICY.md).
- Official `amule-org/amule` under `repos\amule` is the single managed moving
  interoperability and offline-fixture reference. Sync may fast-forward only a
  clean `master`; parity evidence records the tested commit. The archival
  `emulebb/amule` fork may remain a secondary remote, not a second checkout,
  product worktree, or release gate.
- Stock eMule 0.72 under `repos\emule-stock` is the single clean moving stock
  compatibility reference. Instrumented eMuleBB MFC branches remain in the
  canonical app seed and worktrees; they do not replace the clean stock oracle.
- Shared tests are extended in `emulebb-build-tests` rather than forked into
  parallel per-client suites.

## Documentation And Backlog

- Active Markdown belongs under `repos\emulebb-tooling\docs`.
  `DOCS-POLICY.md` owns taxonomy, uppercase-slug naming, navigation, and browser
  readability.
- Workspace-wide rules live in the core or routed annexes. Repo READMEs and
  AGENTS point to them rather than copying them.
- GitHub Project #3 and the owning product repo issue own workflow state for
  externally actionable items; local items own durable specifications,
  acceptance criteria, implementation notes, and evidence. Explicitly local,
  historical, exploratory, and provenance-only items are exceptions.
- GitHub Project #3 is `https://github.com/orgs/emulebb/projects/3`. MFC
  `https://github.com/orgs/emulebb/projects/2` and
  `https://github.com/emulebb/emulebb/issues` are archive/provenance by default.
- Historical handoffs stay under `docs\history`. Root state/progress notes are
  disposable after durable conclusions move into docs, history, or issues.

## Files And Automation

- Honor `.editorconfig` and `.gitattributes`, normalize edited tracked files,
  keep active text LF, and do not leave mixed EOL. Use
  `helpers\source-normalizer.py` for uncertain, generated, or bulk edits.
- `hooks\pre-commit` is the shared hook; workspace sync configures
  `core.hooksPath`.
- Repeatable workspace automation is persisted Python in the owning repo.
  Search existing modules first and extend the closest owner before adding a
  file.
- PowerShell is limited to basic interactive inspection/invocation. Persisted
  soak, live, profiling, monitoring, build, package, and support workflows are
  Python. Do not add batch launchers.
- New tracked PowerShell is forbidden except package-owned runtime setup assets
  below
  `repos\emulebb-build\emule_workspace\release_assets\emulebb\scripts\*.ps1`
  and automation examples below
  `repos\emulebb-build\emule_workspace\release_assets\emulebb_automation_examples\automation\*.ps1`.
  Those assets stage under `eMuleBB\scripts` or examples automation, use names
  such as `Start-eMuleBB.ps1` and `Register-Prowlarr.ps1` in `Verb-Noun.ps1`
  form, declare `#Requires -Version 5.1`, and remain Windows PowerShell 5.1
  compatible. New `.cmd` or `.bat` launchers are forbidden.
