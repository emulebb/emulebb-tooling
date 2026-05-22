# Agent Checklist

This checklist is the repeatable operating path for AI agents contributing to
the canonical eMuleBB workspace. It does not replace
[Workspace Policy](../WORKSPACE-POLICY.md); when this checklist and policy
appear to conflict, policy wins.

## Startup

- Read [Workspace Policy](../WORKSPACE-POLICY.md) before making workspace
  decisions.
- Read the nearest repo-local `AGENTS.md` only after the central policy.
- Check `git status --short --branch` in every repo that will be read for
  current-state decisions or edited.
- Identify the change family before editing: docs, backlog, app code, build
  orchestration, tests, REST/API, localization/resources, release/package,
  website/org-profile, or handoff.
- Keep work scoped to one coherent outcome and one coherent commit unless the
  user explicitly asks for a different flow.

## Workspace Boundaries

- Use `EMULE_WORKSPACE_ROOT` style paths in maintained docs and scripts.
- Edit app source in `workspaces\workspace\app\eMule-main`.
- Treat `repos\eMule` as the branch-store checkout, not the normal edit
  location.
- Do not hardcode machine-local absolute paths in active docs or helpers.
- Do not use `stale/*` branches as active work targets unless the task is
  explicitly historical analysis.

## Docs Workflow

- Put active Markdown under `repos\eMule-tooling\docs`.
- Follow [Documentation Policy](../DOCS-POLICY.md) for naming, taxonomy, and
  navigation.
- Use [Development Guide](DEVELOPMENT-GUIDE.md) for routine docs-only and
  light-code checklists.
- Update `docs\INDEX.md`, `mkdocs.yml`, and README links when discoverability
  changes.
- For docs-only edits, run:

```powershell
cd $env:EMULE_WORKSPACE_ROOT\repos\eMule-tooling
git diff --check
python scripts\docs-structure-check.py
$env:NO_MKDOCS_2_WARNING='1'
python -m mkdocs build --strict
```

## Backlog And Roadmap

- Use [Backlog Process](BACKLOG-PROCESS.md) for item creation, updates,
  validation, and closure.
- Revalidate backlog work against current `main`, current dependency pins, and
  workspace policy before implementation.
- For files with `workflow: github`, treat the linked GitHub issue and public
  `eMuleBB Roadmap` project as workflow authority.
- Run `python scripts\docs-item-taxonomy-check.py` after active item, index, or
  taxonomy changes.

## Code Workflow

- Prefer compatibility-preserving hardening, bug fixes, and maintainability
  improvements with minimal behavioral drift.
- Before writing custom parsing, encoding, filesystem, crypto, protocol,
  date/time, compression, or structured-data logic, look for an existing
  standard library, platform API, project helper, or pinned dependency.
- Keep app source changes in `workspaces\workspace\app\eMule-main`.
- Use `repos\eMule-build` orchestration for build, validation, test, live-test,
  and packaging.
- Do not run ad hoc direct `MSBuild` from app worktrees, `srchybrid`, or
  `repos\eMule-build-tests`.
- For app code, run workspace validation and both required x64 app builds:

```powershell
cd $env:EMULE_WORKSPACE_ROOT\repos\eMule-build
python -m emule_workspace validate
python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly
python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly
```

## Tests And Evidence

- Choose evidence by changed surface; do not use hosted CI as a substitute for
  local release proof.
- For REST/API work, keep the human contract, OpenAPI contract, adapter notes,
  and implementation aligned.
- For protocol-adjacent work, preserve stock/community eMule wire semantics and
  collect parity evidence through the appropriate baseline, golden, tracing, or
  live-diff path.
- For broad build, dependency, compiler, or toolchain policy changes, use the
  relevant full validation matrix.

## Localization And Resources

- Preserve stock/eMule translations. Do not mass-retranslate legacy labels.
- New release-facing strings must land in `srchybrid\emule.rc` and every stock
  `srchybrid\lang\*.rc` language before release proof.
- Use tooling helpers for release localization coverage, layout/order audits,
  and managed-string updates; do not run concurrent `.rc` writes.
- Preserve community labels exactly unless making an explicit targeted
  correction. New labels need reviewed AI-assisted or curated translations for
  every release language before they are treated as release-ready.
- Treat external or historical translation engines as inspiration only, not
  authoritative release sources.

## Live Tests

- Separate public network live tests from local live-stack tests before
  running them.
- Public network live tests that launch an eMule profile must enable the main
  P2P UPnP preference and bind through `BindInterface=hide.me`.
- Do not write `hide.me` into `BindAddr`.
- Never hardcode real media titles or search terms in tracked harness code,
  docs, or tests.

## Release And Package Work

- Use active release docs for release campaign, packaging, provenance, and tag
  decisions.
- Do not describe open, deferred, exploratory, or future backlog work as
  shipped.
- Do not publish release-package claims before package evidence exists.
- Do not create release tags unless the operator gives a separate tagging
  instruction after release proof.

## Website And Public Docs

- Public website, org-profile, README, and rendered docs claims must follow the
  tooling docs and active release state.
- Keep product claims bounded to shipped and evidenced behavior.
- Update public touchpoints only when discoverability or external-facing claims
  change.

## Commit, Push, And Handoff

- Keep commits granular and behavior-focused.
- Do not bundle unrelated docs, app code, dependency, release, and website
  changes.
- Commit and push each completed coherent slice before starting unrelated work
  unless the user explicitly asks to hold local commits.
- Include tracked item IDs in feature, bug, refactor, and CI backlog commits.
- Record skipped validation with a concrete reason.
- Refresh a handoff note only when terminating a session or when explicitly
  asked; handoff notes are not policy authority.
