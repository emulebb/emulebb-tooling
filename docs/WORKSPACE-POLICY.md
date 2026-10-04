# eMule Workspace Policy

This document is the mandatory, product-neutral policy entrypoint for the
canonical eMuleBB workspace. Read it once before making workspace decisions,
then load only the repo-local `AGENTS.md` and policy annexes selected by
[Task routing](#task-routing). The
[Agent Checklist](reference/AGENT-CHECKLIST.md) is an optional execution and
handoff checklist, not a second mandatory policy read.

## Authority And Startup

Directive precedence is:

1. system and developer instructions from the active session
2. workspace-root `AGENTS.md`
3. this core policy
4. every applicable policy annex
5. repo-local `AGENTS.md` local deltas
6. README, backlog, release, and handoff documents

If two applicable annexes appear to conflict, stop and correct the central
policy rather than choosing one silently.

- Infer the active project from the operator's wording and named paths before
  exploring. Explicit product names always win. When product intent remains
  genuinely ambiguous, default to `emulebb-rust` and add harness support only
  when the task needs it.
- Check `git status --short --branch` only in the active repo and support repos
  that will be read for current-state decisions or edited.
- Read the nearest repo-local `AGENTS.md` after this core. Do not sweep
  `repos`, `workspaces`, or dormant products after the focus is known.
- Treat historical notes under `docs\history` as provenance, not current
  authority. Revalidate backlog and release documents against current `main`,
  dependency pins, and policy before implementation.

## Project Focus

- `emulebb rust`, `rust`, or `emulebb-rust` selects
  `repos\emulebb-rust`, including its embedded SPA WebUI. Add
  `repos\emulebb-build-tests` for harness/live/profile work,
  `repos\emulebb-tooling\docs\products\emulebb-rust` for product docs, or
  `repos\emulebb-build` for orchestration only when required.
- `emulebb mfc`, `mfc`, or an MFC source path selects
  `workspaces\workspace\app\emulebb-main`. `repos\emulebb` is its branch store,
  not its normal edit location. Add build, harness, or tooling support only when
  required.
- `qbittorrentbb`, `qbit`, or `qbbb` selects an explicitly materialized
  `repos\qbittorrentbb` checkout. It is a paused experiment and is never the
  ambiguous default.
- Broad workspace scans are allowed only for an explicitly workspace-wide
  request, unclear dependency topology, required orchestration, or genuinely
  cross-product behavior.

## Workspace And Environment Boundaries

- Canonical sources live only below `EMULEBB_WORKSPACE_ROOT\repos` and
  `EMULEBB_WORKSPACE_ROOT\workspaces`. Maintained docs and scripts express
  paths through `EMULEBB_WORKSPACE_ROOT`, never machine-specific absolute paths.
- Generated build, test, package, profile, release, and runtime output belongs
  below `EMULEBB_WORKSPACE_OUTPUT_ROOT`, which must be outside the source
  workspace. Do not create build output or scratch/lab trees below a repo or
  elsewhere under `EMULEBB_WORKSPACE_ROOT`.
- Environment variables are inherited operator state. Agents must not assign,
  repair, shadow, or guess `EMULEBB_WORKSPACE_ROOT`,
  `EMULEBB_WORKSPACE_OUTPUT_ROOT`, `CARGO_TARGET_DIR`, or `X_LOCAL_IP` inline.
  Stop and report a missing or invalid variable when the selected operation
  requires it.
- A persisted Python Windows-to-WSL launcher may translate already-valid
  operator paths for its child and derive a WSL-specific Cargo target below the
  translated output root. It must not mutate the parent environment, persist
  duplicate WSL configuration, or invent missing source values, and it must
  record the translation. Loopback-contained WSL control traffic does not
  require `X_LOCAL_IP`.
- `repos\emulebb-build` owns materialization and supported build, validation,
  test, live-test, packaging, and release orchestration. Interactive operations
  use `python -m emule_workspace` and its single workspace lock; do not start
  competing orchestration runs.

Detailed layout, environment-knob, setup, and automation rules are in the
[Workspace Operations Policy](reference/WORKSPACE-OPERATIONS-POLICY.md).

## Common Engineering Rules

- Prefer compatibility-preserving hardening, fixes, and maintainability work.
  Protocol or other major behavioral changes require explicit justification and
  tracking. Put changes at the earliest layer where they are true.
- Before writing custom parsing, encoding, path, filesystem, crypto, protocol,
  date/time, compression, or structured-data logic, look for a standard
  library, platform API, project helper, or pinned dependency.
- Non-obvious defensive fixes need a concise `WHY:` comment naming the failure
  mode, preserved invariant, and why the repair belongs on that path.
- Reusable code needs succinct API documentation where behavior is not obvious;
  trivial private glue may remain undocumented.
- Every managed-repo commit represents one coherent outcome. Stage explicit
  paths; never use `git add -A` or `git add .` in a mixed tree, bundle unrelated
  existing edits, or push WIP/debug commits.
- Routine work stays on the setup-selected integration branch. Short-lived
  branches are exceptional and, when explicitly requested, use
  `feature/<topic>`, `fix/<topic>`, or `chore/<topic>`. Never use `stale/*` as
  an active target without an explicit historical-comparison request.
- Commit each completed coherent slice before unrelated work. Before final
  handoff, rerun status in every touched repo and commit completed work unless
  the operator asked to hold it, it is genuinely incomplete, or unrelated
  pre-existing changes cannot be staged. Name any exception and dirty path.
- Feature, bug, refactor, and CI backlog commits include their stable item id.
  Do not create release tags without separate operator approval after proof.

## Privacy And Artifact Hygiene

These rules bind source, tests, fixtures, docs, comments, commits, issues, and
retained evidence:

- Never commit credentials, cookies, private host/IP values, account data,
  personal information, or machine-specific absolute paths. Use documented
  variables and obvious synthetic placeholders.
- Never commit real movie, series, episode, album, artist, game, or release
  titles. Use neutral names such as `Sample Title` or `Alpha Beta`. Generic
  encoding tags such as `WEBRip`, `x264`, or `1080p` are allowed where
  technically required.
- Scrub operator screenshots, live logs, searches, and captures before they
  enter tracked files or messages.
- Tracked prose, identifiers carrying prose, comments, diagnostics, logs,
  fixtures, commits, and issue/PR text are English-only. Deliberate localization
  resources and unchanged upstream text are the only exceptions.
- Honor repo `.editorconfig` and `.gitattributes`. Active workspace-owned text
  uses LF; do not leave mixed-EOL edits.

## Task Routing

After this core and the nearest `AGENTS.md`, read only the matching annexes:

- Rust product, daemon, embedded WebUI, REST, metadata, Cargo, or protocol work:
  [Rust Product Policy](products/emulebb-rust/reference/AGENT-POLICY.md).
- Harness code, baseline/tracing work, local or public live tests, soak/profile
  operation, VPN/bind behavior, or retained live evidence:
  [Harness And Live Policy](reference/HARNESS-LIVE-POLICY.md).
- `emulebb-main`, MFC maintenance, C++ app builds, resources/localization, or
  MFC releases:
  [MFC Product Policy](products/emulebb-mfc/reference/AGENT-POLICY.md).
- Materialization, topology, shared orchestration, packaging, managed forks,
  workspace docs/policy, normalization, or automation runtime:
  [Workspace Operations Policy](reference/WORKSPACE-OPERATIONS-POLICY.md).

A Rust live/soak task requires both the Rust and harness/live annexes. A tooling
change that alters generated workspace behavior requires the operations annex.
Reading an annex does not authorize unrelated repo exploration or edits.

## Validation And Documentation

- Every development change gets scoped validation plus the smallest relevant
  build/test set. Broad build-system, dependency, compiler, and integration
  changes require the relevant full matrix.
- Product code changes follow their product annex. Policy/docs-only changes may
  use the documented lighter validation path when they do not alter a build
  contract.
- Active Markdown belongs under `repos\emulebb-tooling\docs`.
  `DOCS-POLICY.md` owns taxonomy, naming, navigation, and readability.
  Workspace-wide rules belong in this core or its routed annexes; repo-local
  `AGENTS.md` files remain thin local deltas.
- The owning product repository issue and org Project #3 (`eMuleBB Roadmap`)
  are the default workflow authority for externally actionable work. Local
  Markdown owns durable specifications and evidence. MFC Project #2 and the
  linked MFC issue set are archive/provenance unless bounded maintenance is
  explicitly approved.
- Refresh handoff notes only when ending a session or when explicitly asked.
