# eMule Workspace Policy

This document is the single source of truth for the canonical eMule workspace.
Repo-local docs should point here instead of restating workspace-wide policy.
AI contributors should use the [Agent Checklist](reference/AGENT-CHECKLIST.md)
as the repeatable operating path after reading this policy.

## Session Startup Contract

Every workspace session starts from this contract:

- Read this policy before making workspace decisions.
- Check `git status --short --branch` in each repo that will be read for
  current-state decisions or edited.
- Use repo-local `AGENTS.md` files only for local deltas after this policy has
  been read.
- Treat historical session handoff notes under `docs\history` as provenance
  only. They are not policy, backlog authority, or a substitute for this
  document.
- Revalidate backlog and release docs against current `main`, current
  dependency pins, and this policy before implementation.
- For future-roadmap items that carry `workflow: github`, treat the linked
  GitHub issue and the `eMuleBB Roadmap` project as the authoritative workflow
  state. The local item doc is retained as engineering spec and evidence.

Directive precedence is:

1. system and developer instructions from the active session
2. workspace-root `AGENTS.md`
3. this workspace policy
4. repo-local `AGENTS.md` local deltas
5. README, backlog, release, and handoff docs

## Workspace Layout

- Canonical workspace paths are expressed through `EMULE_WORKSPACE_ROOT`.
- Repos live under `EMULE_WORKSPACE_ROOT\repos\...`.
- App worktrees live under `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\...`.
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
  `workspaces\workspace\app\eMule-main`, not in `repos\emulebb`.
- Retired pre-rename repository paths such as `repos\eMule`,
  `repos\eMule-build`, `repos\eMule-build-tests`, and `repos\eMule-tooling`
  are historical references only. Active policy, docs, tests, and helper code
  must use `repos\emulebb`, `repos\emulebb-build`,
  `repos\emulebb-build-tests`, and `repos\emulebb-tooling`.
- `workspaces\workspace\deps.json` is the generated dependency contract for
  the active workspace layout. Tests and helpers that need repo paths should
  prefer its `workspace.repos` map instead of reconstructing old repo names.

The canonical workspace currently materializes these app worktrees:

| Worktree | Branch |
|---|---|
| `eMule-main` | `main` |
| `eMule-community-baseline` | `baseline/community-0.72a` |
| `eMule-community-tracing-harness` | `tracing-harness/community-0.72a` |

## Branch And History Policy

- `main` is the only integration branch for the app repo.
- Routine active work happens directly on `main` unless the user explicitly
  requests a separate branch.
- Short-lived working branches are exceptional. If explicitly requested, use
  `feature/<topic>`, `fix/<topic>`, or `chore/<topic>`.
- Future release bugfix branches use `release/MAJOR.MINOR` and are created only
  after an operator-approved release needs maintenance between major versions.
- Do not start normal feature work directly on release branches.
- Supporting repos use `main` unless a repo has an explicitly maintained branch
  documented by setup pins.
- `stale/*` branches are retired historical references only. Never use them as
  active development targets or validation baselines unless a task explicitly
  calls for historical comparison.
- `analysis\stale-v0.72a-experimental-clean` may exist as a historical
  reference checkout only. It is not a managed app worktree or active branch.
- `repos\emulebb` exists to hold history, remotes, and worktrees. Its intended
  neutral state is detached `HEAD` at `origin/main`.
- One `main` commit should represent one coherent outcome.
- Do not push `WIP`, checkpoint, or debug commits to `main`.
- Commit and push each completed coherent slice before starting the next
  unrelated slice unless the user explicitly asks to hold local commits.
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
- Every development change should pass scoped validation. After `validate`, run
  the smallest relevant build and test set for the changed area.
- Every app code change must rebuild both active x64 app configurations before
  commit:
  - `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
  - `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`
- Docs-only or policy-only changes may use a lighter validation path when they
  do not alter the build contract.
- Full matrix validation is expected for build-system changes, dependency pin
  changes, compiler/toolchain policy changes, and broad integration changes.
- `check-clean-worktree.py` is a CI, release-prep, or explicit hygiene guard;
  it is not the default requirement for every in-progress feature branch.

Routine `validate` in `repos\emulebb-build` must run the active static audits:

- build policy
- branch policy
- dependency pin policy
- active documentation path policy
- PowerShell boundary policy
- project entrypoint policy
- warning policy
- localization policy
- normalization policy

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
- Backlog and planning docs are supporting specs, not authority by themselves.
- For GitHub-migrated future-roadmap work, the linked GitHub issue and public
  `eMuleBB Roadmap` project win on workflow state.
- Historical handoff notes live under `docs\history`. Create or refresh a
  current handoff only when terminating a session or when explicitly asked.
- Repo-local `AGENTS.md` files should stay thin and repo-specific.
- Use `EMULE_WORKSPACE_ROOT` style references instead of machine-specific
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

## PowerShell Runtime Policy

- Workspace-wide PowerShell policy is centralized in `repos\emulebb-tooling`.
- New tracked PowerShell files must not be added in workspace-owned repos or
  managed app worktrees unless this policy explicitly allows them.
- `repos\amutorrent\installer\windows\*.ps1` is allowed for aMuTorrent-owned
  native Windows installer/setup assets. These scripts are product runtime
  assets and must stay compatible with Windows PowerShell `5.1`.
- Allowed aMuTorrent scripts must declare `#Requires -Version 5.1`.
- Workspace hygiene checks must fail when tracked PowerShell appears outside
  the allowed path or when an allowed script omits the required header.

## Active Build Policy

- Active compiler baseline for workspace-owned C++ builds is C++17.
- Active MSVC toolset baseline is `v143`.
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
- This policy applies to `eMule-main`, `emulebb-build-tests`, and maintained
  dependency projects used by the canonical workspace build.
- Shared test builds support `x64` and `ARM64`; test execution remains `x64`
  only.
- Frozen app branches are not normalization targets for routine build-policy
  cleanup.
- Project-specific structural exceptions are allowed for C-only projects,
  utility wrappers that inherit policy through orchestration, and `cryptopp`
  toolset enforcement that lives in workspace build orchestration.

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
- Local live-stack tests may bind to LAN addresses, local-only virtual
  adapters, test-specific adapters, or explicit local IP addresses when needed
  for deterministic behavior.
- A local live-stack test becomes a public network live test as soon as it
  contacts public eD2K/Kad infrastructure, imports public bootstrap nodes,
  performs public searches, or accepts public peer discovery.
- Live-wire media titles and search terms are operator-owned runtime inputs.
  Never hardcode real movie, series, or release titles in tracked harness code,
  docs, or tests.

## Product And Release Naming

- The full public product name is `eMule broadband edition`.
- The compact app, UI, API, and protocol-facing mod name is `eMuleBB`.
- The GitHub organization, code name, and URL slug are `emulebb`.
- The first beta/public release is `0.7.3`.
- Superseded `1.0.0`, `1.0.1`, and `1.1.1` release labels are internal
  evidence/rehearsal labels only.
- Release tags use `emulebb-vMAJOR.MINOR.PATCH`.
- Release ZIP assets use `emulebb-MAJOR.MINOR.PATCH-ARCH.zip`.
- Official beta `0.7.3` is marked with an annotated tag on a selected reviewed
  `main` commit only after release proof passes and the operator gives a
  separate tagging instruction.

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
- `helpers\rc-translate-missing.py` is a convenience helper for adding only
  missing managed strings while preserving existing translations.
- `helpers\rc-release-localization-layout.json` owns source-anchored placement
  rules for managed release labels that must keep identical order across all
  release language `.rc` files.
- Mechanical localization edits must be generated or audited by the helpers and
  keyed on resource ids, not fragile surrounding text. A managed label may be
  inserted or normalized, but unrelated community labels must not change.
- Parallel localization work is allowed only for draft/review artifacts. Do not
  run concurrent `.rc` writes.
