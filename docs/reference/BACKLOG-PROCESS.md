# Backlog Process

This runbook is the repeatable workflow for creating, updating, validating, and
closing eMuleBB backlog records.

`docs/active/` is the current local spec and evidence layer. For
GitHub-primary items marked `workflow: github`, GitHub issues in
`emulebb/emulebb` and org Project #2 (`eMuleBB Roadmap`) own workflow state;
the local Markdown file remains the engineering spec and evidence record.

Canonical public backlog workflow endpoints:

- issue tracker: `https://github.com/emulebb/emulebb/issues`
- project board: `https://github.com/orgs/emulebb/projects/2`

When adding or materially updating an externally actionable backlog item,
manage all three records together unless the item is explicitly local-only,
historical, exploratory, or provenance-only: local Markdown spec, GitHub issue,
and Project #2 item.

## Preflight

1. Read `EMULE_WORKSPACE_ROOT\repos\emulebb-tooling\docs\WORKSPACE-POLICY.md`.
2. Check `git status --short --branch` in every repo you will read for
   current-state decisions or edit.
3. Revalidate candidate backlog work against current `main`, current dependency
   pins, and current workspace policy before treating older notes as active.
4. Keep each backlog/doc update as one coherent commit and push it before
   starting an unrelated slice, unless the user explicitly asks to hold commits.

## Create Or Update An Active Item

1. Classify the item:
   - `BUG`: user-visible or runtime correctness defect
   - `FEAT`: product behavior, UX, or capability work
   - `REF`: refactoring, architecture cleanup, or internal modernization
   - `CI`: build, validation, packaging, release proof, or tooling gate
   - `AMUT` / `ARR`: accepted integration-specific work
2. Allocate the next ID by scanning both `docs\active\items` and
   `docs\history\items`. Never reuse an ID, even if the old item is closed or
   `WONT_DO`.
3. Create `docs\active\items\<ID>.md`. The filename stem must match the
   front-matter `id`.
4. Include this active-item front matter:

```yaml
---
id: FEAT-000
title: Short imperative item title
status: OPEN
priority: Minor
category: feature
labels: [area, risk, evidence]
milestone: post-0.7.3
created: YYYY-MM-DD
source: short provenance note
---
```

5. Add a short body that records the problem, current evidence, intended shape,
   scope constraints, and acceptance criteria.
6. Add or update the row in `docs\active\INDEX.md` in the matching section.
   Keep rows sorted by item ID inside each table section.
7. Update the snapshot counts in `docs\active\INDEX.md` when adding, closing, or
   changing active statuses.

## GitHub-Primary Backlog

Use this path for normal externally actionable backlog slices:

1. Create or update the local active item spec first, including the stable item
   ID, scope, constraints, and acceptance criteria.
2. If the item belongs to an approved future lane, add the item ID to
   `docs\active\FUTURE-ROADMAP.md`, then use
   `python scripts\github-roadmap-sync.py` to preview and apply the issue and
   Project #2 import.
3. If the item is GitHub-primary but not part of the future-roadmap import set,
   create or update the issue in `https://github.com/emulebb/emulebb/issues`
   and add it to Project #2 (`https://github.com/orgs/emulebb/projects/2`)
   directly.
4. Set the project fields that mirror the local item: `Roadmap Status`,
   `Work Type`, `Priority`, `Lane`, `Local ID`, and `Release` when applicable.
5. Ensure the local item has `workflow: github`,
   `github_issue: https://github.com/emulebb/emulebb/issues/<number>`, and a
   workflow-status note that points to the issue.
6. After migration, treat GitHub as the workflow authority for status, priority,
   release placement, discussion, ownership, and PR linkage. Keep the Markdown
   item as the durable spec/evidence record.

Run `python scripts\github-roadmap-check.py` after local edits. Run
`python scripts\github-roadmap-check.py --github` when the current GitHub token
has project scope and network access.

## Close Or Reclassify An Item

1. Revalidate the item against current `main` before closing it.
2. For `DONE`, `PASSED`, or `WONT_DO`, move the item record from
   `docs\active\items` to `docs\history\items`.
3. Preserve provenance: include implementation commits, validation commands,
   product decisions, or rejection rationale in the historical item body.
4. Update the `docs\active\INDEX.md` row to point at `../history/items/<ID>.md`
   and use the closed status.
5. Update active snapshot counts.
6. If a GitHub-primary item is closed or materially advanced, update the linked
   GitHub issue/project as the workflow authority.

## Validation And Commit

Run these checks from `EMULE_WORKSPACE_ROOT\repos\emulebb-tooling` after backlog
or active-index changes:

```powershell
git diff --check
python scripts\docs-item-taxonomy-check.py
python scripts\docs-structure-check.py --fail-on-wide-tables
python scripts\github-roadmap-check.py
```

Run this when GitHub credentials are available:

```powershell
python scripts\github-roadmap-check.py --github
```

For docs-only changes, app builds are not required unless the doc change claims
new app validation evidence. Commit messages for backlog work must include the
stable item ID, for example:

```text
CI-039: document backlog process
```
