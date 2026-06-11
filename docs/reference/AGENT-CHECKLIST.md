# Agent Checklist

This checklist is the single **start-here** on-ramp and repeatable operating
path for any agent contributing to the canonical eMuleBB workspace, independent
of which tool or assistant is used. Read it first, identify your change family in
[Startup](#startup), then jump to the matching section below and to the
authoritative section of [Workspace Policy](../WORKSPACE-POLICY.md) for that
area. It does not replace the policy; when this checklist and policy appear to
conflict, policy wins.

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

- Use `EMULEBB_WORKSPACE_ROOT` style paths in maintained docs and scripts.
- Edit app source in `workspaces\workspace\app\emulebb-main`.
- Treat `repos\emulebb` as the branch-store checkout, not the normal edit
  location.
- Use [Workspace Repository Map](WORKSPACE-REPO-MAP.md) for repo roles,
  product-family boundaries, and repeatable validation commands.
- Prefer `workspaces\workspace\repo-roles.json` when tooling needs
  machine-readable repository roles instead of parsing Markdown tables.
- Do not hardcode machine-local absolute paths in active docs or helpers.
- Do not use `stale/*` branches as active work targets unless the task is
  explicitly historical analysis.

## Docs Workflow

- Put active Markdown under `repos\emulebb-tooling\docs`.
- Follow [Documentation Policy](../DOCS-POLICY.md) for naming, taxonomy, and
  navigation.
- Use [Development Guide](DEVELOPMENT-GUIDE.md) for routine docs-only and
  light-code checklists.
- Update `docs\INDEX.md`, `mkdocs.yml`, and README links when discoverability
  changes.
- For docs-only edits, run:

```powershell
cd $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling
git diff --check
python scripts\docs-structure-check.py --fail-on-wide-tables
$env:NO_MKDOCS_2_WARNING='1'
python -m mkdocs build --strict
```

## Backlog And Roadmap

- Use [Backlog Process](BACKLOG-PROCESS.md) for item creation, updates,
  validation, and closure.
- Revalidate backlog work against current `main`, current dependency pins, and
  workspace policy before implementation.
- When the user asks to add or materially update an externally actionable
  backlog item, manage the local item, the `emulebb/emulebb` issue tracker
  (`https://github.com/emulebb/emulebb/issues`), and Project #2
  (`https://github.com/orgs/emulebb/projects/2`) together unless the item is
  explicitly local-only, historical, exploratory, or provenance-only.
- For files with `workflow: github`, treat the linked GitHub issue and public
  `eMuleBB Roadmap` project as workflow authority. The Markdown item remains
  the spec and evidence record.
- Run `python scripts\docs-item-taxonomy-check.py` after active item, index, or
  taxonomy changes.

## Code Workflow

- Prefer compatibility-preserving hardening, bug fixes, and maintainability
  improvements with minimal behavioral drift.
- For bug fixes with non-obvious defensive logic, add a concise `WHY:` comment
  at the fix site explaining the failure mode and invariant being preserved.
- Before writing custom parsing, encoding, filesystem, crypto, protocol,
  date/time, compression, or structured-data logic, look for an existing
  standard library, platform API, project helper, or pinned dependency.
- Keep app source changes in `workspaces\workspace\app\emulebb-main`.
- Use `repos\emulebb-build` orchestration for build, validation, test, live-test,
  and packaging.
- Use `python -m emule_workspace workspace-status` before broad release or
  product-family work to inspect dirty state across all managed repos.
- Do not run ad hoc direct `MSBuild` from app worktrees, `srchybrid`, or
  `repos\emulebb-build-tests`.
- For app code, run workspace validation plus the required x64 app builds and
  the diagnostics Release build from `repos\emulebb-build`
  (`python -m emule_workspace`), exactly as defined in
  [Workspace Policy](../WORKSPACE-POLICY.md#build-validation-and-test-policy).
  That section is the single source of those commands.

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
- Use [Evidence Retention](EVIDENCE-RETENTION.md) before pruning large generated
  test, diagnostic, profiling, or release-campaign artifacts.
- Treat root-level progress Markdown files under `workspaces\workspace\state`
  as disposable scratch notes after durable conclusions move to active docs,
  history, or GitHub issues.

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
- Enable VPN Guard for public VPN live profiles unless the lane explicitly
  tests guard-off behavior. Empty VPN Guard CIDRs are valid interface-only
  coverage; configured CIDRs add public-exit validation.
- Public VPN live campaigns need operator-local VPN Guard live config for
  provider connect/allow-list/check/restore hooks. LAN-only local eD2K/Kad
  lanes do not need VPN Guard.
- On the canonical split-tunnel test machine, pass the required
  `--lan-bind-addr` / `X_LOCAL_IP` to every live harness path that binds or
  probes non-P2P services. Loopback and wildcard binds remain valid product
  compatibility cases, but not valid operator-machine live harness defaults.
- Keep LAN and P2P bind concepts separate: `--lan-bind-addr` is for non-P2P
  services and control/probe traffic; VPN P2P binding is through
  `BindInterface` unless an address-bound P2P profile is explicitly intended.
- Do not reintroduce ambiguous live harness names such as `--bind-addr`,
  `--rest-bind-addr`, or `--web-bind-addr`.
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
