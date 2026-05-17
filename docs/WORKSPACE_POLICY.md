# eMule Workspace Policy

This document is the single source of truth for the canonical eMule workspace.

All workspace-wide directives should point here instead of restating policy in
repo-local docs.

## Session Startup Contract

Every workspace session starts from this contract:

- Read this policy before making workspace decisions.
- Treat this policy as the source of truth for workspace roles, active branches,
  worktrees, setup ownership, dependency pins, build/test entrypoints, release
  naming, and documentation discipline.
- Check `git status --short --branch` in each repo that will be read for
  current-state decisions or edited.
- Use repo-local `AGENTS.md` files only for local deltas after this policy has
  been read.
- Treat historical session handoff notes under `docs\history` as provenance
  only. They are not policy, not backlog authority, and not a substitute for
  this document.
- Revalidate backlog and release docs against current `main`, current
  dependency pins, and this policy before implementation.

Directive precedence is:

1. system and developer instructions from the active session
2. workspace-root `AGENTS.md`
3. this workspace policy
4. repo-local `AGENTS.md` local deltas
5. README, backlog, release, and handoff docs

## Mandatory Preflight

- Read this policy at the start of every workspace task before running build,
  validation, test, commit, or cleanup commands.
- Check `git status --short --branch` in each repo that will be read for
  current-state decisions or edited.
- All active work must be broken into granular, coherent commits. Before
  starting any new chunk of work, finish, verify, commit, and push the current
  chunk unless the user explicitly asks to hold local commits.
- Routine active work happens through those granular commits on each repo's
  `main` branch unless the user explicitly requests a separate branch.
- App edits belong in `workspaces\workspace\app\eMule-main`; do not edit the
  canonical `repos\eMule` branch-store checkout for normal app work.
- Interactive build, validation, and test commands must go through the
  supported `repos\eMule-build` orchestration entrypoints.
- Use `python -m emule_workspace` for workspace build, validation, test,
  live-test, and packaging orchestration.
- `repos\eMule-build` orchestration owns a single workspace lock. Never start
  multiple build, validation, test, or live-test invocations in parallel; run
  them strictly sequentially.
- Do not run ad hoc direct `MSBuild` commands from an app worktree,
  `srchybrid`, or `repos\eMule-build-tests`.

## Workspace Roots

- Canonical workspace paths are expressed through `EMULE_WORKSPACE_ROOT`.
- Repos live under `EMULE_WORKSPACE_ROOT\repos\...`.
- App worktrees live under `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\...`.
- Do not hardcode machine-specific absolute paths in workspace docs or scripts.

## Repo Roles

- `repos\eMule-tooling` owns shared workspace policy, helper docs, and
  engineering notes.
- `repos\eMule-build` owns workspace materialization, repo/worktree
  orchestration, build orchestration, validation, and packaging.
- `repos\eMule-build-tests` owns shared test harness code and test execution
  helpers.
- `repos\eMule` is the canonical app repo checkout used as the branch store and
  worktree anchor.
- Normal app editing belongs in the active app worktrees, not in the canonical
  `repos\eMule` checkout.

## Active Branch Model

### App Repo

- `main` is the only integration branch.
- Routine active app work is done directly in `eMule-main` on `main`.
- Short-lived working branches are exceptional and should be used only when the
  user explicitly requests one or an already-documented workflow requires one.
- If a short-lived branch is explicitly requested, recommended names are:
  - `feature/<topic>`
  - `fix/<topic>`
  - `chore/<topic>`
- Active app branch roles are:

  | Branch | Role | Release status |
  |---|---|---|
  | `main` | active eMule BB integration line | beta 0.7.3 release source after reviewed release proof passes |
  | `baseline/community-0.72a` | seam-enabled parity and regression baseline | test-only baseline; not a release branch |
  | `tracing-harness/community-0.72a` | variant-client parity harness | not a release branch and not the default regression baseline |
- Future release bugfix branches use `release/MAJOR.MINOR` and are created
  only after an operator-approved release needs maintenance between major
  versions.
- `release/v0.72a-broadband`, `release/v0.72a-build`, `release/v0.72a-bugfix`,
  `oracle/v0.72a-build`, `tracing/v0.72a`, and
  `tracing-harness/v0.72a` are retired historical references.
- Beta 0.7.3 release work is cut from a reviewed commit already present on
  `main`; the annotated beta tag belongs on that selected `main` commit after
  release proof and operator approval.
- Future release-branch promotion, if needed after beta 0.7.3, flows from
  reviewed commits already present on `main` and must be documented before the
  release branch becomes authoritative again.
- Do not start normal feature work directly on release branches.

### Supporting Repos

- The active branch for supporting repos is `main` unless a repo has an
  explicitly maintained branch documented by setup pins.
- No long-lived release branches are part of the active model for:
  - `eMule-build`
  - `eMule-build-tests`
  - `eMule-tooling`
  - `amutorrent`

### `stale/*`

- `stale/*` branches are retired historical references only.
- Never use them as active development targets.
- Never treat them as current validation baselines unless a task explicitly
  calls for historical comparison.
- The only setup-materialization exception is
  `stale/v0.72a-experimental-clean`, which may be cloned under
  `analysis\stale-v0.72a-experimental-clean` as a historical reference checkout
  only.
- `analysis\stale-v0.72a-experimental-clean` is not a managed app worktree, not
  an active branch target, and not a default validation baseline.
- This branch contains a large body of unmerged fixes, features, and
  improvements, so it is a preferred code-reference source when re-implementing
  ideas on current `main`.

## Worktree Mapping

The canonical workspace currently materializes these app worktrees:

- `eMule-main` -> `main`
- `eMule-community-baseline` -> `baseline/community-0.72a`
- `eMule-community-tracing-harness` -> `tracing-harness/community-0.72a`

## Workspace Manifest Contract

- `workspaces\workspace\deps.json` is a required generated contract file.
- `repos\eMule-build` owns that contract and must regenerate it on topology
  changes.
- `python -m emule_workspace validate` must fail if the generated contract
  drifts from the current Python topology.
- `repos\eMule-tooling` and test helpers may consume the generated contract, but
  must not become an independent second source of truth for workspace topology.

## Canonical App Checkout

- `repos\eMule` exists to hold history, remotes, and worktrees.
- It should be treated as the branch store and maintenance checkout.
- It is not the normal editing location for app work.
- Its intended neutral state is detached `HEAD` at `origin/main`.
- The setup helper may leave it detached on that app-anchor commit; that is the
  correct state, not a problem to "fix" by checking out a local branch.

## Merge and History Hygiene

- The default active workflow is direct, granular commits on `main`.
- If an explicit working branch is requested, the default merge strategy back
  to `main` is squash merge.
- `main` history should stay curated and readable.
- Do not push `WIP`, checkpoint, or debug commits to `main`.
- One `main` commit should represent one coherent outcome.
- Commits must stay granular and behavior-focused; do not bundle unrelated work
  into one commit.
- Always commit and push each completed chunk before starting a new independent
  chunk of work. A later chunk must not be layered onto uncommitted changes from
  an earlier chunk unless the work is inseparable and will be committed as one
  coherent outcome.
- When a change spans multiple repos, create and verify those commits sequentially; do not launch parallel commits.
- Commit messages for feature, bug, refactor, and CI backlog work must include the tracked item id such as `BUG-017`, `FEAT-015`, `REF-021`, or `CI-003`.
- Push each completed `main` commit to its `origin/main` before starting the
  next unrelated slice unless the user explicitly asks to hold local commits.

## Development Workflow

- Normal development starts from a clean understanding of current `main` and
  proceeds directly on `main` in the relevant repo.
- Recommended branch families, when a branch is explicitly requested, are:
  - `feature/<topic>` for new behavior
  - `fix/<topic>` for bug fixes
  - `chore/<topic>` for tooling, docs, or repo hygiene
- Keep working branches such as `feature/*`, `fix/*`, and `chore/*` after
  merge until there is an explicit later decision to delete or retire them.
- The normal path for routine work is commit and push each coherent slice on
  `main`.
- One working branch should pursue one coherent outcome.
- Avoid mixing unrelated behavior changes, dependency churn, tooling churn, and
  large cleanup in one branch unless they are inseparable.
- Frozen release branches are not normal development targets.
- Frozen release branches may receive only selective backports from already
  reviewed work on `main`.

## Change Intent And Drift Control

- The default direction for active work is:
  - hardening
  - bug fixing
  - compatibility-preserving cleanup
  - maintainability improvements with minimal behavioral drift
- Minimum drift from eMule community behavior is a hard default rule when
  choosing among technically valid implementations.
- Prefer local safety, correctness, and diagnostics improvements that preserve
  established runtime semantics over broad behavioral rewrites.
- Major behavioral changes are not default maintenance work.
- A major behavioral change must be explicitly justified in the change itself
  and tracked as intentional behavior work rather than blended into hardening,
  cleanup, or routine modernization.
- Major behavioral changes include, for example:
  - broad scheduling or policy rewrites
  - feature additions that materially change default runtime behavior
  - protocol-adjacent behavior changes
  - large UI or workflow changes that alter default user-visible semantics
- Allowed default work includes, for example:
  - defensive checks
  - parser and lifetime hardening
  - race fixes
  - compatibility-preserving refactors
  - narrow logging or diagnostics that do not change default behavior

## Protocol Compatibility Policy

- eMule BB stays stock-compatible at the eD2K and Kad protocol layer.
- The product must preserve stock/community eMule wire semantics, packet and tag
  shapes, opcode meanings, peer/server interaction rules, Kad state-machine
  behavior, persistence semantics that affect network identity, and default
  network behavior.
- Future protocol-adjacent evolution is limited to compatibility-preserving
  connectivity work:
  - IPv6 support
  - NAT traversal and LowID relief
  - safer bind and interface selection
  - diagnostics, tracing, and test evidence that do not alter default behavior
- Do not introduce protocol forks, proprietary Kad/eD2K extensions, incompatible
  opcode or packet changes, default scheduling or routing policy drift, or
  peer/server behavior that cannot be validated against stock/community
  semantics.
- Protocol-adjacent changes must carry explicit parity evidence. Use the
  community baseline, protocol goldens, tracing harness, live-diff, or live
  packet captures as appropriate for the changed surface.
- IPv6 and NAT traversal work must be treated as transport/connectivity
  modernization only. They are not permission to alter Kad or eD2K semantics.

## Validation Expectations

- The default merge bar is scoped validation, not full-matrix validation for
  every change.
- Every development change should pass `validate`.
- After `validate`, run the smallest relevant build and test set for the area
  being changed.
- Every app code change must rebuild both active x64 app configurations before
  commit:
  - `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
  - `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`
- For feature and fix work on `main`, targeted regression checks are the
  default expectation.
- When a change affects observable behavior, compare `main` against
  `baseline/community-0.72a` as the seam-enabled parity and regression
  baseline where the existing targeted test or live-diff flow makes that
  comparison meaningful.
- Full matrix validation is expected for:
  - build-system changes
  - dependency pin or dependency project changes
  - compiler or toolchain policy changes
  - broad integration changes that span multiple repos or architectures
- Docs-only or policy-only changes may use a lighter validation path when they
  do not alter the build contract.
- An exception to targeted regression work is acceptable only when the change
  has no meaningful runtime or observable behavior surface.
- Cleanliness checks like `check-clean-worktree.py` are appropriate for CI,
  release prep, or explicit hygiene passes, but are not the default requirement
  for every in-progress feature branch.

## Live Test Network Policy

- Every live test that launches an eMule profile must enable the main P2P UPnP
  preference.
- Every live test that launches an eMule profile must bind the P2P stack through
  the `hide.me` interface by writing `BindInterface=hide.me`.
- Live test harnesses must not write `hide.me` into `BindAddr`; `BindAddr` is an
  address override and should remain empty when the bind target is an interface
  name.
- Standalone live test entrypoints must use the same defaults as aggregate live
  runners. Do not make UPnP or the `hide.me` bind depend on aggregate-only
  wrapper flags.
- Live-wire media titles and search terms are operator-owned runtime inputs.
  Never hardcode real movie, series, or release titles in tracked harness code,
  docs, or tests. Load live terms from `live-wire-inputs.local.json` or an
  explicit `--live-wire-inputs-file`; tracked examples and fixtures may use only
  generic placeholders.

## Backport And Baseline Maintenance Rules

- `baseline/community-0.72a` is the seam-enabled parity and regression
  baseline. It is test-only and not a product release line.
- Retired refs such as `release/v0.72a-broadband`, `release/v0.72a-build`,
  `release/v0.72a-bugfix`, `oracle/v0.72a-build`, `tracing/v0.72a`, and
  `tracing-harness/v0.72a` are historical references only.
- Future release branch backports are narrow and selective:
  - critical buildability fixes
  - important low-risk bug fixes
  - narrowly scoped release maintenance for an already published line
- Acceptable parity/regression baseline maintenance is limited to:
  - inert test seams
  - deterministic probes or adapters
  - narrow logging or tracing needed by regression and parity tests
  - buildability fixes required to keep the baseline usable
- Unacceptable backports include:
  - normal feature work
  - broad refactors
  - speculative cleanup
  - changes that have not already been reviewed on `main`
- Prefer cherry-picks or tightly scoped merge work over branch drift on
  release maintenance branches.

## Community Baseline Rules

- `baseline/community-0.72a` is the seam-enabled comparison baseline for
  parity and regression testing. It is not an actual release, not a product
  release, and not a packaging or public-tag target.
- Allowed parity/regression baseline changes are limited to:
  - test seams
  - deterministic probes or adapters
  - narrow logging or tracing needed by the test harness
  - buildability fixes required to keep the baseline usable
- Community seams must be inert unless explicitly exercised by the test
  harness.
- Community baseline changes must not alter normal runtime behavior,
  persistence semantics, network behavior, or default control flow.
- Community seams may lag `main`; backport only the minimal common seam surface
  required to compile and run the intended comparison tests.

## Tracing Harness Rules

- `tracing-harness/community-0.72a` derives from
  `baseline/community-0.72a`.
- `tracing-harness/community-0.72a` is the only sanctioned place for
  deterministic parity-harness behavior used for explicit variant P2P client
  comparisons, such as:
  - CLI orchestration hooks
  - ready-file / startup automation
  - seeded source-publish or source-search overrides
  - swarm-control or parity-seed behavior that intentionally changes runtime
    decisions
- The tracing harness is not a release branch, not a product baseline, and not
  the default regression baseline.
- `baseline/community-0.72a` remains the default comparison baseline for
  live-diff, regression, and comparable parity work unless a task explicitly
  requires `tracing-harness`.

## Setup and Dependency Authority

- `repos\eMule-build` owns materialization, managed app worktrees, repo pinning,
  and supported app-build orchestration.
- Python topology in `repos\eMule-build\emule_workspace` is the source of truth
  for active dependency branches used by the canonical workspace.
- App worktrees do not by themselves define a complete supported app-build
  environment; dependency materialization and third-party build inputs are part
  of the `eMule-build` contract.
- Interactive build, validation, and test work must use the supported
  `repos\eMule-build` orchestration entrypoints. The Python
  `emule_workspace` CLI is authoritative for build, validation, test,
  live-test, and packaging orchestration.
- Direct ad hoc `MSBuild` commands from an app worktree, `srchybrid`, or
  `repos\eMule-build-tests` are prohibited. Direct `MSBuild` invocation is
  allowed only inside owned orchestration implementation that is itself called
  through the supported `eMule-build` entrypoints.
- If a build fails, report the supported `eMule-build` command and log path.
  Do not diagnose the workspace from an unsupported direct app-project build.
- Repo-local docs must not redefine dependency pin authority or workspace
  topology.

## Shared CI Policy

- Shared workspace policy audits live under `repos\eMule-tooling\ci\`.
- Routine workspace policy audits run through
  `repos\eMule-tooling\ci\check-workspace-policy.py`; do not add new
  routine validation audits as PowerShell scripts.
- Routine `validate` in `repos\eMule-build` must run the active static audits:
  - build policy
  - branch policy
  - dependency pin policy
  - active documentation path policy
  - PowerShell boundary policy
  - project entrypoint policy
  - warning policy
- `check-clean-worktree.py` is an explicit cleanliness guard for CI or
  pre-release verification; it is not part of routine `validate` because local
  feature work may legitimately leave tracked changes in progress.

## Documentation Discipline

- Workspace-wide development rules belong only in this document.
- Workspace-wide hooks and workspace-wide policy must be centralized in
  `repos\eMule-tooling`.
- All Markdown documentation belongs under `repos\eMule-tooling\docs`; do not
  create a parallel active-doc tree outside `docs`.
- `repos\eMule-tooling\docs\DOCS_POLICY.md` owns the documentation taxonomy:
  active docs under `docs\active`, exploratory ideas under `docs\ideas`,
  current reference material under role-specific folders, and stale or
  historical material under `docs\history`.
- Historical handoff notes live under `repos\eMule-tooling\docs\history`.
  Create or refresh a current handoff only when terminating a session or when
  the user explicitly asks for one. Detailed durable analysis belongs in
  tooling docs.
- Repo-local `AGENTS.md` files should stay thin and repo-specific.
- Repo-local docs must point to this policy rather than restating workspace
  branch, worktree, setup, or dependency authority.
- Repo-local hook or policy helpers must point back to the centralized
  `repos\eMule-tooling` implementation instead of redefining workspace rules.
- Use `EMULE_WORKSPACE_ROOT` style references instead of machine-specific
  absolute paths in active docs.
- Backlog and planning docs are not authoritative by themselves.
- Before implementing a backlog item, revalidate it against current `main`,
  current dependency pins, and the current workspace policy.
- The documentation and normalization requirements in this policy are mandatory
  completion criteria, not optional style guidance.
- Lack of a dedicated automated audit for a policy requirement does not waive
  that requirement.
- Newly generated code should include succinct Doxygen-style documentation for
  new functions, classes, structs, enums, namespaces, and other reusable
  surfaces introduced by the change.
- The expectation applies to app code, tooling, and shared test/support code
  when the new code is intended to be read, reused, extended, or audited later.
- Short private glue code may stay undocumented when it is truly trivial, but
  new helper layers and reusable test fixtures should not be left comment-free.
- Routine workspace validation currently enforces normalization policy, but it
  does not yet provide a general Doxygen audit. Doxygen coverage therefore
  remains mandatory through authoring and review discipline.

## File Normalization Policy

- Tracked text-file edits must honor the repo-local `.editorconfig` and
  `.gitattributes` rules of the repo being edited.
- Authors must normalize edited tracked files before commit; do not rely on
  hooks or later cleanup passes to repair `.editorconfig` drift after the fact.
- Line endings, charset or BOM, trailing whitespace, and final-newline policy
  are part of the workspace contract, not optional editor preferences.
- Active workspace-owned repos use LF for tracked text files, including
  Windows command files (`*.bat`, `*.cmd`), Windows resource files (`*.rc`,
  `*.rc2`), Visual Studio solution/project files, and any explicitly allowed
  PowerShell files. Tracked CRLF text is not allowed in active workspace-owned
  repos or managed app worktrees.
- Do not leave edited tracked files in mixed-EOL state.
- `repos\eMule-tooling\helpers\source-normalizer.py` is the canonical
  normalization helper for workspace-owned repos and app worktrees.
- The normalizer is not a mandatory per-edit step for small LF-stable edits.
  Use it when touching files with uncertain encoding or EOL history, after
  generated or bulk edits, or when `diff --check`, hooks, or `validate` show
  normalization drift.
- `repos\eMule-tooling\hooks\pre-commit` is the shared workspace hook entrypoint
  for catching normalization drift before commit.
- `python -m emule_workspace sync` configures repo-local `core.hooksPath` to
  that shared hook directory.
- Routine `validate` must fail when modified tracked files in workspace-owned
  repos or canonical app worktrees drift from their declared normalization
  policy.

## PowerShell Runtime Policy

- Workspace-wide PowerShell policy is centralized in `repos\eMule-tooling`.
- `repos\amutorrent\installer\windows\*.ps1` is also allowed for aMuTorrent-owned
  native Windows installer/setup assets. These scripts are product runtime
  assets, not workspace orchestration, and must stay compatible with Windows
  PowerShell `5.1`.
- Allowed scripts in `repos\amutorrent\installer\windows\` must declare
  `#Requires -Version 5.1`.
- New tracked PowerShell files must not be added anywhere else in workspace-owned
  repos or managed app worktrees.
- Workspace hygiene checks must fail when tracked PowerShell appears outside
  the allowed path or when an allowed script omits the required
  `#Requires -Version 5.1` header.

## Active Build Policy

- Active compiler baseline for workspace-owned C++ builds is `C++17`
  (`LanguageStandard=stdcpp17`).
- Active MSVC toolset baseline is `v143`.
- The active workspace build matrix has no `Win32` target.
- Supported build architectures are:
  - `x64`
  - `ARM64`
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
- Active compile targets should also declare:
  - `BufferSecurityCheck=true`
  - `MultiProcessorCompilation=true`
- This policy applies to active workspace targets:
  - `eMule-main`
  - `eMule-build-tests`
  - maintained dependency projects used by the canonical workspace build
- Shared test builds support `x64` and `ARM64`; test execution remains `x64`
  only.
- Frozen app branches are not normalization targets for routine build-policy
  cleanup.
- Project-specific exceptions are allowed when they are structural, not
  accidental:
  - C-only projects are not forced to declare a C++ language standard
  - utility wrappers like `zlib` and `mbedtls` inherit their compiler policy
    through wrapper/CMake orchestration
  - `cryptopp` toolset enforcement remains in workspace build orchestration to
    avoid unnecessary fork delta

## Implementation Discipline

- Put changes at the earliest layer where they are true, then let later layers
  inherit them.
- Before writing custom parsing, encoding, path, filesystem, crypto, protocol,
  date/time, compression, or structured-data logic, look for an existing
  standard library, platform API, project helper, or already-pinned dependency
  that owns the behavior. Prefer the established API unless there is a clear
  correctness, security, compatibility, or maintenance reason to implement a
  small local helper, and document that reason in the change.
- Prefer narrow, build-level fixes over source edits in third-party dependency
  forks when the issue is build policy, warning policy, or orchestration.
- When several valid implementations exist, prefer the one that improves safety
  or maintainability with the least drift from eMule community behavior.
- Do not revive `stale/*` branches or historical workflows as active solutions.
- Do not reintroduce workspace orchestration, dependency pin policy, or branch
  policy into app-repo docs or ad hoc notes.
- Keep commits and reviewed outcomes behavior-focused and easy to explain.
- If an exception to these defaults is necessary, record it clearly in the
  change itself rather than relying on local habit.

## Product Naming

- The full public product name is `eMule broadband edition`.
- The compact app, UI, API, and protocol-facing mod name is `eMule BB`.
- The GitHub organization, code name, and URL slug are `emulebb`.
- The first beta/public release is `0.7.3`.
- Superseded `1.0.0`, `1.0.1`, and `1.1.1` release labels are internal
  evidence/rehearsal labels only. Do not publish GitHub release packages for
  those labels.
- Release tags use the compact tag family `emule-bb-vMAJOR.MINOR.PATCH`.
- Release ZIP assets use the public package family
  `eMule-broadband-MAJOR.MINOR.PATCH-ARCH.zip`.
- Do not use `emule-broadband-v` for release tags unless the release parser,
  update-check tests, and release policy are deliberately migrated together.

## Release Localization Policy

- Every stock eMule resource file under `srchybrid\lang\*.rc` in the active
  app worktree is a supported eMule BB release language and is part of release
  gating. There is no smaller "core" language subset for release-facing labels.
- `repos\eMule-tooling\helpers\rc-release-languages.json` is the
  machine-readable release manifest and must enumerate exactly the current
  stock `srchybrid\lang\*.rc` file set. Historical compatibility file names,
  such as `cz_CZ.rc`, `ua_UA.rc`, `jp_JP.rc`, and `es_ES_T.rc`, must stay as
  file names even when their policy language code is more canonical.
- New release-facing user-visible strings must land in `srchybrid\emule.rc`
  and every stock `srchybrid\lang\*.rc` language file before release proof.
  Missing managed labels in any stock language are release blockers.
- Existing stock/eMule translation strings in supported `.rc` files must be
  preserved. Do not mass-retranslate legacy labels, do not replace established
  community wording just because a machine translation suggests different text,
  and do not rewrite unrelated strings during a release-label pass.
- New eMule BB labels must be translated meaningfully for the target language.
  Machine translation may be used only as a draft source; the committed text
  must be reviewed for product context, false friends, menu/action style,
  placeholders, protected product/protocol names, and target-language idiom.
- External or historical translation engines, including the eMuleAI analysis
  tree, may inspire validation techniques but are not authoritative translation
  sources for release `.rc` files.
- eMule BB managed translation blocks may be updated to add or improve new
  eMule BB strings. Such edits must stay scoped to those new/managed labels
  unless the user explicitly asks for a broader translation refresh.
- `repos\eMule-tooling\helpers\rc-string-table.py` is the canonical helper for
  auditing release localization coverage, duplicate ids, printf/literal-percent
  marker parity, line-break escape parity, mnemonic accelerator parity,
  copied-English mistakes, missing managed ids, and curated semantic quality
  rules. The release gate must use the full stock language set, either through
  `--release-languages helpers\rc-release-languages.json` or
  `--all-stock-targets`.
- `repos\eMule-tooling\helpers\rc-translate-missing.py` is a convenience helper
  for adding only missing managed strings. It must preserve existing target
  translations by default, verify that stock strings did not change after a
  write, support review-packet/draft-only workflows, and support curated
  per-language `--manual-dir` updates for the full stock language set. Prefer
  curated manual translations for new labels before falling back to machine
  translation drafts.
- Parallel localization work is allowed only for draft/review artifacts from
  stock eMule `.rc` files. Do not run concurrent `.rc` writes, and do not add
  release languages that are not present as stock eMule resource files.
- Workspace validation must run the localization policy audit so manifest drift
  and missing required managed labels across stock languages fail before release
  proof.

## Tags

- Official beta 0.7.3 release should be marked with an annotated tag on the
  selected reviewed `main` commit after release proof passes and the operator
  gives a separate tagging instruction.
- Public GitHub releases and uploaded release assets start at
  `emule-bb-v0.7.3`. Superseded higher-version evidence tags, if present, are
  internal markers only and must not have published package assets attached.
- Recommended tag families:
  - `emule-bb-vMAJOR.MINOR.PATCH` for eMule broadband edition releases,
    with the first beta package release at `emule-bb-v0.7.3`
- eMule broadband edition release packages should include a platform-specific
  ZIP asset whose name matches the release version, for example:
  - `eMule-broadband-0.7.3-x64.zip`
  - `eMule-broadband-0.7.3-arm64.zip`
