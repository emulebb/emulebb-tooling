# eMule Tooling

This repo is the documentation and policy home for the eMuleBB workspace. It
contains shared workspace policy, helper scripts, docs validation, CI baseline
configuration, and engineering reference material.

It is not the app repo and it is not the build orchestrator:

- app source: `workspaces\workspace\app\eMule-main`
- branch-store checkout: `repos\emulebb`
- build/test orchestration: `repos\emulebb-build`
- shared test helpers: `repos\emulebb-build-tests`
- local live-test ED2K server: `repos\goed2k-server`
- workspace docs and helper audits: this repo

## Start Here

- rendered docs site:
  <https://emulebb.github.io/emulebb-tooling/>
- workspace policy:
  [`docs/WORKSPACE-POLICY.md`](docs/WORKSPACE-POLICY.md)
- agent checklist:
  [`docs/reference/AGENT-CHECKLIST.md`](docs/reference/AGENT-CHECKLIST.md)
- development guide:
  [`docs/reference/DEVELOPMENT-GUIDE.md`](docs/reference/DEVELOPMENT-GUIDE.md)
- documentation policy:
  [`docs/DOCS-POLICY.md`](docs/DOCS-POLICY.md)
- active backlog and release status:
  [`docs/active/INDEX.md`](docs/active/INDEX.md)
- backlog process:
  [`docs/reference/BACKLOG-PROCESS.md`](docs/reference/BACKLOG-PROCESS.md)
- reference index:
  [`docs/INDEX.md`](docs/INDEX.md)

## What This Repo Owns

- central workspace policy and documentation taxonomy
- durable product, REST, dependency, and development reference docs
- active local backlog/spec docs and release-control docs
- MkDocs site configuration for GitHub Pages
- shared policy and documentation audits under `ci\` and `scripts\`
- normalization and release-localization helpers under `helpers\`
- shared workspace pre-commit hook under `hooks\`
- reusable baseline GitHub Actions workflow under `.github\workflows\`

Workspace materialization, dependency pinning, app builds, test orchestration,
and release packaging are owned by `repos\emulebb-build`. App source is edited in
the active app worktree, not in this repo.

## Common Commands

Preview the formatted docs locally:

```powershell
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

Run the docs build gate used by CI:

```powershell
python scripts\docs-publish-check.py
```

Run Markdown structure validation:

```powershell
python scripts\docs-structure-check.py
```

Run backlog item taxonomy validation when active item metadata or indexes
change:

```powershell
python scripts\docs-item-taxonomy-check.py
```

Run workspace validation through the build orchestrator:

```powershell
cd $env:EMULE_WORKSPACE_ROOT\repos\emulebb-build
python -m emule_workspace validate
```

## Conventions

Canonical paths are expressed through `EMULE_WORKSPACE_ROOT`:

- repos live under `EMULE_WORKSPACE_ROOT\repos\...`
- app worktrees live under `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\...`

Use [`docs/WORKSPACE-POLICY.md`](docs/WORKSPACE-POLICY.md) for the operating
contract before making workspace decisions. Use
[`docs/reference/AGENT-CHECKLIST.md`](docs/reference/AGENT-CHECKLIST.md) for
the repeatable AI contributor checklist. Use
[`docs/reference/DEVELOPMENT-GUIDE.md`](docs/reference/DEVELOPMENT-GUIDE.md)
for the routine contributor workflow.
