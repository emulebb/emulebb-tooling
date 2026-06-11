# eMule Workspace Policy

This document is the single source of truth for the canonical eMule workspace.
Repo-local docs and `AGENTS.md` files should point here instead of restating
workspace-wide policy. AI contributors should use the
[Agent Checklist](reference/AGENT-CHECKLIST.md) as the repeatable operating
path after reading this policy.

## Session Startup Contract

- Read this policy before making workspace decisions.
- Check `git status --short --branch` in each repo that will be read for
  current-state decisions or edited.
- Use repo-local `AGENTS.md` files only for local deltas after this policy has
  been read.
- Treat historical session handoff notes under `docs\history` as provenance
  only.
- Revalidate backlog and release docs against current `main`, dependency pins,
  and this policy before implementation.
- For backlog items with `workflow: github`, the linked `emulebb/emulebb` issue
  and org Project #2 (`eMuleBB Roadmap`) are authoritative for workflow state.

Directive precedence is:

1. system and developer instructions from the active session
2. workspace-root `AGENTS.md`
3. this workspace policy
4. repo-local `AGENTS.md` local deltas
5. README, backlog, release, and handoff docs

## Workspace Layout

- Canonical workspace paths are expressed through `EMULEBB_WORKSPACE_ROOT`.
- Repos live under `EMULEBB_WORKSPACE_ROOT\repos\...`.
- App worktrees live under `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\...`.
- Do not hardcode machine-specific absolute paths in workspace docs or scripts.
- `repos\emulebb-tooling` owns shared workspace policy, helper docs, and
  engineering notes.
- `repos\emulebb-build` owns workspace materialization, repo/worktree
  orchestration, build orchestration, validation, and packaging.
- `repos\emulebb-build-tests` owns shared test harness code and test execution
  helpers.
- `repos\goed2k-server` owns the local ED2K server used by deterministic
  eMuleBB live E2E and protocol-parity scenarios.
- `repos\emulebb` is the canonical app repo checkout used as the branch store and
  worktree anchor.
- Normal app editing belongs in
  `workspaces\workspace\app\emulebb-main`, not in `repos\emulebb`.
- Retired pre-rename repository paths such as `repos\eMule`,
  `repos\eMule-build`, `repos\eMule-build-tests`, and `repos\eMule-tooling`
  are historical references only. Active policy, docs, tests, and helper code
  must use `repos\emulebb`, `repos\emulebb-build`,
  `repos\emulebb-build-tests`, and `repos\emulebb-tooling`.
- `workspaces\workspace\deps.json` is the generated dependency contract for
  the active workspace layout. Tests and helpers that need repo paths should
  prefer its `workspace.repos` map instead of reconstructing old repo names.
- The canonical app worktrees are `emulebb-main`,
  `emulebb-community-baseline`, and `emulebb-community-tracing-harness` with
  branches defined by the generated dependency contract.
- Generated build, test, release, and runtime output belongs under
  `EMULEBB_WORKSPACE_OUTPUT_ROOT`, not under `repos\...` or
  `workspaces\workspace\state`.
- The canonical output-root children are `builds`, `logs`, `reports`,
  `artifacts`, `packages`, `release`, `tmp`, `tools`, `cache`, and `profiles`.
- Canonical build-output subtrees include
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\app`,
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\tests`,
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\amule`,
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\third_party`, and
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\rust\target`.
- Package-only generated inputs belong under
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\packages\build`; this includes aMuTorrent
  frontend bundles staged under `packages\build\amutorrent`.
- Runtime tool payloads staged for tests and VM workflows belong under
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\tools`, such as `tools\amule`.
- Orchestrated third-party dependency output should prefer
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\third_party`; repo-local third-party
  build directories are tolerated only for upstream/manual tooling and must be
  ignored plus covered by cleanup/audit.
- Orchestrated Rust builds must set `CARGO_TARGET_DIR` to
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\rust\target`.

## Branch And History Policy

- `main` is the only integration branch for the app repo.
- Routine active work happens directly on `main`; short-lived branches are
  exceptional and, when explicitly requested, use `feature/<topic>`,
  `fix/<topic>`, or `chore/<topic>`.
- Release stabilization branches use `release/MAJOR.MINOR.PATCH` and are
  created from the selected reviewed `main` commit when a release candidate
  starts. The `0.7.3` train is fixed as `0.7.3-rc.1`, `0.7.3-rc.2`,
  `0.7.3-rc.3`, then stable `0.7.3`.
- After stable `0.7.3`, `main` opens for `0.8.0` work and
  `release/0.7.x` carries the legacy support line.
- The `0.7.x` legacy line accepts only compatibility-preserving, low-risk bug
  fixes on supported surfaces plus security, crash/data-loss, packaging,
  update-check, release-proof, and release-documentation fixes. It must not add
  new product surface, new controller/API capability, or feature expansion.
- Frozen legacy surfaces remain unsupported in `0.7.x`; do not fix them unless
  the issue affects supported shared infrastructure, security, or app
  stability.
- Patch maintenance on `release/0.7.x` publishes stable patch tags such as
  `emulebb-v0.7.4`. If a separate one-off patch branch is needed, branch from
  the latest stable tag when `main` has moved on.
- Do not start normal feature work directly on release branches.
- Fixes made on release branches must be merged or cherry-picked back to `main`
  unless the fix is release-packaging metadata that does not apply to `main`.
- Supporting repos use their setup-pinned branch.
- `stale/*` branches are retired historical references only. Never use them as
  active development targets or validation baselines unless a task explicitly
  calls for historical comparison.
- `analysis\stale-v0.72a-experimental-clean` is a historical reference checkout
  only when present.
- `repos\emulebb` exists to hold history, remotes, and worktrees. Its intended
  neutral state is detached `HEAD` at `origin/main`.
- One `main` commit should represent one coherent outcome.
- Do not push `WIP`, checkpoint, or debug commits to `main`.
- Commit and push each completed coherent slice before starting unrelated work
  unless the user explicitly asks to hold local commits.
- Feature, bug, refactor, and CI backlog commit messages must include the
  tracked item id such as `BUG-017`, `FEAT-015`, `REF-021`, or `CI-003`.
- GitHub-tracked roadmap work should keep the stable local item id and link the
  GitHub issue when the work closes or materially advances it.

## Build, Validation, And Test Policy

- Interactive build, validation, test, live-test, and packaging commands must
  go through `repos\emulebb-build` orchestration.
- Use `python -m emule_workspace` for workspace build, validation, test,
  live-test, and packaging orchestration.
- `repos\emulebb-build` owns a single workspace lock. Never start multiple build,
  validation, test, or live-test invocations in parallel.
- Do not run ad hoc direct `MSBuild` commands from an app worktree,
  `srchybrid`, or `repos\emulebb-build-tests`.
- Direct `MSBuild` invocation is allowed only inside owned orchestration
  implementation called through supported `emulebb-build` entrypoints.
- Every development change should pass scoped validation plus the smallest
  relevant build and test set for the changed area.
- Every app code change must rebuild both active x64 app configurations and the
  diagnostics Release executable before commit:
  - `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
  - `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`
  - `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly --diagnostics`
- Docs-only or policy-only changes may use a lighter validation path when they
  do not alter the build contract.
- Full matrix validation is expected for build-system, dependency pin,
  compiler/toolchain policy, and broad integration changes.
- `check-clean-worktree.py` is a CI, release-prep, or explicit hygiene guard;
  it is not the default requirement for every in-progress feature branch.

Routine `validate` in `repos\emulebb-build` must run the active static audits
for build, branch, dependency pin, active documentation path, PowerShell
boundary, project entrypoint, warning, localization, and normalization policy.

## Development And Compatibility Defaults

- Default active work is hardening, bug fixing, compatibility-preserving
  cleanup, and maintainability work with minimal behavioral drift.
- Minimum drift from eMule community behavior is the default rule when choosing
  among technically valid implementations.
- Major behavioral changes are exception work. They must be explicitly
  justified and tracked as intentional behavior work.
- Major behavioral changes include broad scheduling or policy rewrites,
  material default-runtime feature changes, protocol-adjacent behavior changes,
  and large UI or workflow changes.
- Put changes at the earliest layer where they are true, then let later layers
  inherit them.
- Bug fixes that add state repair, lifetime guards, synchronization guards,
  bounds checks, fallback paths, or other non-obvious defensive logic must carry
  concise `WHY:` comments at the fix site. The comment should name the concrete
  failure mode, the invariant being preserved, and why the repair belongs on
  that path; avoid restating what the code already says.
- Before writing custom parsing, encoding, path, filesystem, crypto, protocol,
  date/time, compression, or structured-data logic, first look for an existing
  standard library, platform API, project helper, or pinned dependency.
- Prefer narrow build-level fixes over source edits in third-party dependency
  forks when the issue is build policy, warning policy, or orchestration.
- New reusable code should include succinct Doxygen-style documentation. Short
  private glue code may stay undocumented when it is truly trivial.

## Protocol Compatibility Policy

- eMuleBB stays stock-compatible at the eD2K and Kad protocol layer.
- Preserve stock/community eMule wire semantics, packet and tag shapes, opcode
  meanings, peer/server interaction rules, Kad state-machine behavior,
  persistence semantics that affect network identity, and default network
  behavior.
- Protocol-adjacent evolution is limited to compatibility-preserving
  connectivity work such as IPv6 support, NAT traversal, safer bind/interface
  selection, and diagnostics or tracing that do not alter default behavior.
- Do not introduce protocol forks, proprietary Kad/eD2K extensions,
  incompatible opcode or packet changes, default scheduling or routing policy
  drift, or peer/server behavior that cannot be validated against
  stock/community semantics.
- Source Exchange v1 is the explicit exception to the stock-compatibility
  default: eMuleBB intentionally removed the deprecated live-network SX1
  advertise, request, response, and version-tracking paths. Source Exchange is
  SX2-only on the live network; do not treat absent `OP_REQUESTSOURCES` /
  `OP_ANSWERSOURCES` live-path support as an accidental protocol regression.
  The durable decision record is [REF-002](history/items/REF-002.md).
- Protocol-adjacent changes must carry explicit parity evidence through the
  community baseline, protocol goldens, tracing harness, live-diff, or live
  packet captures as appropriate.

## Baseline And Harness Policy

- `baseline/community-0.72a` is the seam-enabled parity and regression
  baseline. It is test-only and not a product release line.
- Allowed baseline maintenance is limited to inert test seams, deterministic
  probes or adapters, narrow logging/tracing needed by regression and parity
  tests, and buildability fixes required to keep the baseline usable.
- Community baseline changes must not alter normal runtime behavior,
  persistence semantics, network behavior, or default control flow.
- `tracing-harness/community-0.72a` derives from the community baseline and is
  the only sanctioned place for deterministic parity-harness behavior that
  intentionally changes runtime decisions.
- The tracing harness is not a release branch, not a product baseline, and not
  the default regression baseline.
- Future release branch backports are narrow and selective: critical
  buildability fixes, important low-risk bug fixes, or release maintenance for
  an already published line.

## Setup And Dependency Authority

- `repos\emulebb-build` owns materialization, managed app worktrees, repo pinning,
  and supported app-build orchestration.
- Python topology in `repos\emulebb-build\emule_workspace` is the source of truth
  for active dependency branches used by the canonical workspace.
- `workspaces\workspace\deps.json` is a required generated contract file.
- `python -m emule_workspace validate` must fail if the generated dependency
  contract drifts from the current Python topology.
- Tooling docs and test helpers may consume the generated dependency contract,
  but must not become an independent topology source.
- The ED2K server path is exposed as `workspace.repos.ed2k_server`; live E2E
  helpers must resolve it from the manifest or orchestration layout.
- Repo-local docs must not redefine dependency pin authority or workspace
  topology.

## Environment Variables

Canonical workspace paths and supported orchestration knobs are expressed
through environment variables. Agents and CI must rely on the canonical
variables below and treat override knobs as shell- or CI-boundary diagnosis
tools, not as committed workspace state. `repos\emulebb-build\README.md`
(`Environment Overrides`) is the authoritative reference for toolchain override
knobs, and the owning orchestration module is authoritative for command-scoped
knobs.

Canonical workspace variables:

- `EMULEBB_WORKSPACE_ROOT` (required) is the absolute workspace root;
  orchestration fails if it is unset. Maintained docs, scripts, and helpers
  express paths relative to it and must not hardcode machine-specific absolute
  paths.
- `EMULEBB_WORKSPACE_OUTPUT_ROOT` (required) is the generated-output root and
  must resolve outside `EMULEBB_WORKSPACE_ROOT`; orchestration fails if it is
  unset or nested inside the workspace root. All build, test, release, and
  runtime output belongs under it, never under `repos\...` or
  `workspaces\workspace\state`.
- `EMULEBB_RELEASE_VERSION` selects the release version for build, package, and
  release orchestration; the active default is pinned in `repos\emulebb-build`.
- `CARGO_TARGET_DIR` is set by orchestration to
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\builds\rust\target` for orchestrated Rust
  builds; do not redirect Rust output back inside a repo tree.

Toolchain override knobs (shell or CI boundary only; leave unset for release and
CI unless the run evidence records why an override was needed):

- `EMULEBB_VS_PLATFORM_TOOLSET` forces the Visual Studio toolset (default
  `v143`) for compatibility diagnosis.
- `EMULEBB_MSYS2_ROOT` points the aMule Windows client build at a nonstandard
  MSYS2 install.
- `EMULEBB_CMAKE_GENERATOR` and `EMULEBB_CMAKE_PLATFORM` override the CMake
  generator and platform for dependency builds.

Command-scoped knobs (owned by, and authoritative in, their orchestration
module):

- Diagnostics build flags `EMULEBB_ENABLE_STARTUP_DIAGNOSTICS`,
  `EMULEBB_ENABLE_PACKET_DIAGNOSTICS`,
  `EMULEBB_ENABLE_UPLOAD_SLOT_DIAGNOSTICS`,
  `EMULEBB_ENABLE_DOWNLOAD_SLOT_DIAGNOSTICS`,
  `EMULEBB_ENABLE_BAD_PEER_DIAGNOSTICS`, and `EMULEBB_ENABLE_KAD_DIAGNOSTICS`
  enable diagnostics instrumentation for the `--diagnostics` app build.
- Local package install knobs `EMULEBB_PACKAGE_ROOT_NAME`,
  `EMULEBB_RELEASE_ASSET_ROOT_NAME`, and `EMULEBB_RUNTIME_SCRIPT_PATHS` control
  package staging and runtime script resolution.
- Windows VM lab knobs `EMULEBB_VM_TEST_PASSWORD`,
  `EMULEBB_VM_HIDE_ME_SETTINGS_PATH`, `EMULEBB_OFFLINE_SOFTWARE`,
  `EMULEBB_OFFLINE_SYSTEM`, and `EMULEBB_OFFLINE_DEFAULT_USER` configure the
  windowed VM test lab.
- The live-test harness uses `X_LOCAL_IP` as the LAN bind address (equivalent to
  `--lan-bind-addr`) for non-P2P control and probe traffic on the operator
  split-tunnel machine.
- Documentation builds may set `NO_MKDOCS_2_WARNING` to silence the MkDocs
  upgrade notice.

## Documentation Policy

- Workspace-wide development rules belong only in this document.
- Workspace-wide hooks and policy helpers must be centralized in
  `repos\emulebb-tooling`.
- All active Markdown documentation belongs under `repos\emulebb-tooling\docs`.
- `docs\DOCS-POLICY.md` owns the documentation taxonomy, naming conventions,
  navigation expectations, and browser-readability rules.
- `docs\reference\AGENT-CHECKLIST.md` is the repeatable operating checklist
  for AI agents contributing to the workspace.
- `docs\reference\DEVELOPMENT-GUIDE.md` is the practical guide for routine
  docs-first and light-code contribution work.
- Backlog and planning docs are supporting specs; for GitHub-primary items they
  are not workflow authority by themselves.
- Canonical public backlog workflow endpoints are
  `https://github.com/emulebb/emulebb/issues` and
  `https://github.com/orgs/emulebb/projects/2`.
- New externally actionable backlog items should be managed in the local item,
  linked `emulebb/emulebb` issue, and Project #2 together unless explicitly
  local-only, historical, or provenance-only.
- For GitHub-primary backlog work, GitHub owns workflow state, priority,
  release placement, ownership, discussion, and PR linkage. Local Markdown owns
  durable engineering specs, acceptance criteria, implementation notes, and
  evidence.
- Historical handoff notes live under `docs\history`. Create or refresh a
  current handoff only when terminating a session or when explicitly asked.
- Repo-local `AGENTS.md` files should stay thin and repo-specific.
- Use `EMULEBB_WORKSPACE_ROOT` style references instead of machine-specific
  absolute paths in active docs.
- Documentation and normalization requirements are mandatory completion
  criteria, not optional style guidance.

## File Normalization Policy

- Tracked text-file edits must honor repo-local `.editorconfig` and
  `.gitattributes` rules.
- Authors must normalize edited tracked files before commit.
- Active workspace-owned repos use LF for tracked text files, including Windows
  command files, resource files, Visual Studio solution/project files, and any
  explicitly allowed PowerShell files.
- Do not leave edited tracked files in mixed-EOL state.
- `repos\emulebb-tooling\helpers\source-normalizer.py` is the canonical
  normalization helper for workspace-owned repos and app worktrees.
- The normalizer is not mandatory for small LF-stable edits. Use it when
  touching files with uncertain encoding or EOL history, after generated or
  bulk edits, or when checks show normalization drift.
- `repos\emulebb-tooling\hooks\pre-commit` is the shared workspace hook
  entrypoint.
- `python -m emule_workspace sync` configures repo-local `core.hooksPath` to
  that shared hook directory.

## Script And Automation Runtime Policy

- Repeatable workspace automation should be implemented as persisted Python
  scripts or modules in the owning repo.
- One-off PowerShell commands are acceptable for basic shell operations such as
  file finding, string search, directory listing, environment inspection, and
  invoking existing tools.
- New tracked PowerShell files must not be added in workspace-owned repos or
  managed app worktrees unless this policy explicitly allows them.
- `repos\emulebb-build\emule_workspace\release_assets\emulebb\scripts\*.ps1`
  is allowed for eMuleBB package-owned native Windows setup and integration
  assets staged into `eMuleBB\scripts`. These scripts are product runtime assets
  and must stay compatible with Windows PowerShell `5.1`.
- `repos\emulebb-build\emule_workspace\release_assets\emulebb_automation_examples\automation\*.ps1`
  is allowed for eMuleBB package-owned REST automation examples staged by the
  bootstrapper into `examples\automation`. These scripts are example assets and
  must stay compatible with Windows PowerShell `5.1`.
- eMuleBB package-owned PowerShell runtime script filenames must use
  `Verb-Noun.ps1` form, for example `Start-eMuleBB.ps1` or
  `Register-Prowlarr.ps1`; lowercase kebab-case script names are not allowed.
- Allowed eMuleBB runtime scripts must declare `#Requires -Version 5.1`.
- Workspace hygiene checks must fail when tracked PowerShell appears outside
  the allowed path or when an allowed script omits the required header.

## Active Build Policy

- Active compiler baseline for workspace-owned C++ builds is C++17.
- Active MSVC toolset baseline is `v143`.
- `v145` is a forward-compatibility probe target only. It may be used in
  GitHub automation, local diagnosis, and explicitly labeled experimental
  artifacts, but it is not the default release toolset.
- Official RC/stable packages must use the active baseline toolset unless the
  operator makes a separate release-policy decision after sustained probe,
  smoke, and package evidence.
- The active workspace build matrix has no `Win32` target.
- Supported build architectures are `x64` and `ARM64`.
- Debug builds in the active matrix must use:
  - `RuntimeLibrary=MultiThreadedDebug`
  - `Optimization=Disabled`
  - `IncrementalLink=true` for executable targets
  - `DebugInformationFormat=ProgramDatabase`
- Release builds in the active matrix must use:
  - `RuntimeLibrary=MultiThreaded`
  - explicit speed-oriented optimization
  - `FunctionLevelLinking=true`
  - `IntrinsicFunctions=true` where the project compiles code directly
  - `IncrementalLink=false` for executable targets
  - `LinkTimeCodeGeneration=UseLinkTimeCodeGeneration` for release app links
- Active compile targets should declare `BufferSecurityCheck=true` and
  `MultiProcessorCompilation=true`.
- This policy applies to `emulebb-main`, `emulebb-build-tests`, and maintained
  dependency projects used by the canonical workspace build.
- Shared test builds support `x64` and `ARM64`; test execution remains `x64`
  only.
- Frozen app branches are not normalization targets for routine build-policy
  cleanup.
- Project-specific structural exceptions are allowed for C-only projects,
  utility wrappers that inherit policy through orchestration, and `cryptopp`
  toolset enforcement that lives in workspace build orchestration.
- Toolset overrides must flow through `emulebb-build` orchestration. Do not
  hardcode a newer Visual Studio generator or `PlatformToolset` in project files
  when a build-time override can express the probe.

## Live Test Network Policy

- Public network live tests contact the real public eD2K/Kad network, public
  servers, public peers, public search results, or operator-provided live-wire
  terms.
- Local live-stack tests run only against deterministic workspace-owned
  services and clients.
- Public network live tests that launch an eMule profile must enable the main
  P2P UPnP preference and bind the P2P stack through `hide.me` by writing
  `BindInterface=hide.me`.
- Public network live-test harnesses must not write `hide.me` into `BindAddr`.
- Public network live-test profiles must enable VPN Guard
  (`VpnGuardMode=Block`) unless the scenario explicitly exists to prove
  guard-off behavior. Empty `VpnGuardAllowedPublicIpCidrs` is allowed for
  interface-only guard coverage; configured CIDRs add public-exit validation.
- Public VPN live campaigns must take VPN Guard live configuration from
  operator-local inputs so the harness can connect, allow-list, verify, and
  restore the split-tunnel provider state. LAN-only suites such as local eD2K
  and local Kad do not need VPN Guard.
- In the canonical operator split-tunnel environment, live harness control and
  probe traffic must bind and connect through an explicit LAN address supplied
  as `--lan-bind-addr` / `X_LOCAL_IP`; do not use loopback or wildcard
  addresses for those harness paths on that machine.
- The operator split-tunnel rule is harness- and machine-specific. Product
  runtime behavior, release package scripts, and user installations must still
  support deliberate loopback and wildcard bindings where the product contract
  allows them.
- `--lan-bind-addr` is the canonical harness parameter for the LAN address used
  by all non-P2P services and control/probe surfaces. Do not reintroduce
  ambiguous names such as `--bind-addr`, `--rest-bind-addr`, or
  `--web-bind-addr`.
- Public-network P2P profiles that use an interface policy must write the VPN
  adapter name to `BindInterface` and leave the eMule P2P `BindAddr` empty. Use
  `BindAddr` for P2P only when the profile is intentionally address-bound
  rather than interface-bound.
- In tests and examples, use `192.0.2.x` addresses for LAN bind examples. Use
  `127.0.0.1` as the canonical loopback spelling where loopback compatibility
  must be documented or tested; reserve `localhost` for explicit DNS, URL
  parsing, UNC, or compatibility cases.
- Local live-stack tests may bind to LAN addresses, local-only virtual
  adapters, test-specific adapters, or explicit local IP addresses when needed
  for deterministic behavior.
- A local live-stack test becomes a public network live test as soon as it
  contacts public eD2K/Kad infrastructure, imports public bootstrap nodes,
  performs public searches, or accepts public peer discovery.
- Live-wire media titles and search terms are operator-owned runtime inputs.
  Never hardcode real movie, series, or release titles in tracked harness code,
  docs, or tests.

## Live Test Storage And Path Capability Policy

- eMuleBB is the only active Windows P2P client under test that is treated as
  long-path capable.
- The community tracing harness, community baseline, eMuleAI comparison trees,
  and aMule are compatibility clients. They must not be used as proof targets
  for long-path behavior unless their own code has explicitly gained and proven
  long-path support.
- Mixed-client local live suites that include aMule or the tracing harness must
  keep generated profiles, incoming directories, temp directories, and shared
  libraries on short paths. Prefer throwaway VHD drive-letter roots for those
  suites.
- VHD folder-mount or intentionally deep-path storage scenarios are eMuleBB-only
  tests. They may exercise eMuleBB shared files, startup cache, REST, part-file,
  and completion behavior, but they must not launch aMule or the tracing harness
  against those long paths.

## Product And Release Naming

- The full public product name is `eMule broadband edition`.
- The compact app, UI, API, and protocol-facing mod name is `eMuleBB`.
- The GitHub organization, code name, and URL slug are `emulebb`.
- The fixed `0.7.3` release-candidate train is `0.7.3-rc.1`,
  `0.7.3-rc.2`, and `0.7.3-rc.3`.
- The first stable release is `0.7.3`.
- After stable `0.7.3`, the `0.7.x` series is the legacy support version with
  a frozen public surface.
- The `0.8.x` series is the modernization line; `0.8.0` is the first release
  expected to remove currently frozen legacy surfaces.
- Stable patch releases increment the patch number, starting with `0.7.4` after
  `0.7.3` if a stable hotfix is needed.
- Future prereleases use the next target version with an explicit prerelease
  suffix, for example `0.7.5-rc.1` or `0.7.5-beta.1`.
- Superseded `1.0.0`, `1.0.1`, and `1.1.1` release labels are internal
  evidence/rehearsal labels only.
- Release tags use `emulebb-vMAJOR.MINOR.PATCH` for stable releases and
  `emulebb-vMAJOR.MINOR.PATCH-rc.N` or
  `emulebb-vMAJOR.MINOR.PATCH-beta.N` for prereleases.
- Standard release ZIP assets use
  `emulebb-MAJOR.MINOR.PATCH[-rc.N|-beta.N]-ARCH.zip`; paired diagnostics
  assets use `emulebb-MAJOR.MINOR.PATCH[-rc.N|-beta.N]-diagnostics-ARCH.zip`.
- The standard package executable remains `emulebb.exe`; the diagnostics
  package executable is `emulebb-diagnostics.exe`. Do not put the version
  number in executable filenames.
- Runtime diagnostic artifacts written by the app use lowercase kebab-case
  `emulebb` names. Current log names are `emulebb.log`,
  `emulebb-verbose.log`, `emulebb-crt-debug.log`,
  `emulebb-startup-errors.log`, `emulebb-diagnostics-packet.log`,
  `emulebb-diagnostics-upload-slot.log`,
  `emulebb-diagnostics-download-slot.log`,
  `emulebb-diagnostics-bad-peer.log`,
  `emulebb-diagnostics-kad.log`,
  `emulebb-diagnostics-startup.trace.json`, `emulebb-performance.csv`,
  `emulebb-performance.mrtg`, `emulebb-performance-data.mrtg`, and
  `emulebb-performance-overhead.mrtg`. Rotated logs append
  `-YYYYMMDD-HHMMSS` before the extension. Dump names use
  `emulebb-dump-YYYYMMDD-HHMMSS-pid<PID>-mini|full.dmp` and
  `emulebb-crash-YYYYMMDD-HHMMSS-pid<PID>.dmp`.
- Runtime artifact renames are strict unless the user explicitly requests
  compatibility aliases; do not add dual writes or fallback opens for retired
  filenames by default.
- Build and test artifact names are strict. New build, certification, release
  campaign, and test runs use UTC `YYYYMMDDTHHMMSSZ` run ids. Build recaps use
  `build-result.json`; certification recaps use `certification-result.json`;
  release-campaign recaps use `release-campaign-run-result.json`. Test suites
  publish timestamped run folders plus `<suite>\latest` snapshots, and suite
  leaves use `<suite>-result.json`, `<suite>-result.partial.json`, and
  `<suite>-summary.json`.
- Public release documentation must include a version-specific changelog for
  every actual published release from `0.7.3-rc.2` onward. Release notes explain
  the release for users; changelogs enumerate material changes in the released
  artifact set. Changelogs are power-user release documents, not Git logs or
  commit lists: describe operationally relevant changes, compatibility
  boundaries, packaging/controller changes, diagnostics, defaults, risks, and
  migration/testing notes that users or administrators need to know. Start the
  active-candidate changelog during RC preparation and finalize it only when the
  operator gives the release go. The `0.7.3-rc.2` changelog must include a
  separate RC1-vs-stock/community-baseline section with the RC1 release date.
- Official release tags are annotated tags on selected reviewed commits only
  after release proof passes and the operator gives a separate tagging
  instruction.

## Release Localization Policy

- Every stock eMule resource file under `srchybrid\lang\*.rc` in the active app
  worktree is a supported eMuleBB release language and part of release gating.
- `repos\emulebb-tooling\helpers\rc-release-languages.json` is the
  machine-readable release manifest and must enumerate exactly the current
  stock resource file set.
- New release-facing user-visible strings must land in `srchybrid\emule.rc` and
  every stock language file before release proof.
- Existing stock/eMule community translation strings must be preserved exactly
  as labels unless the user explicitly asks for a targeted correction. Do not
  mass-retranslate legacy labels or rewrite unrelated strings during a
  release-label pass.
- New eMuleBB labels must be meaningfully translated for every release
  language. AI or machine translation is allowed and expected for draft
  coverage, but it must be treated as a reviewed translation source, not a
  blind bulk replacement.
- External or historical translation engines, including the eMuleAI analysis
  tree, are not authoritative translation sources for release `.rc` files.
- `helpers\rc-string-table.py` is the canonical helper for release localization
  coverage, layout, ordering, and quality audits.
- `helpers\rc-localization-preflight.py` is the canonical aggregate release
  localization gate. It must run from workspace validation and from pre-commit
  when staged localization/resource policy files change.
- `helpers\rc-translate-missing.py` is a convenience helper for adding only
  missing managed strings while preserving existing translations.
- `helpers\rc-release-localization-layout.json` owns source-anchored placement
  rules for managed release labels that must keep identical order across all
  release language `.rc` files.
- `helpers\rc-release-localization-ignored-ids.txt` owns the baseline of
  English `IDS_*` rows that are intentionally not release-gated. New English
  string IDs must be classified in either the required-ID manifest or this
  ignored-ID baseline before they are committed.
- Mechanical localization edits must be generated or audited by the helpers and
  keyed on resource ids, not fragile surrounding text. A managed label may be
  inserted or normalized, but unrelated community labels must not change.
- Parallel localization work is allowed only for draft/review artifacts. Do not
  run concurrent `.rc` writes.
