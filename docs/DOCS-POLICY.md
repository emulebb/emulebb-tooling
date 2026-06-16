# Documentation Policy

This repo keeps all Markdown under `docs/`. Document role is determined by
path, not by filename alone.

## Active Docs

`docs/active/` owns current local backlog/spec and release truth:

- `docs/active/INDEX.md`: active backlog dashboard and item tables
- `docs/active/RELEASE-0.7.3*.md`: RC release control, checklist, runbook,
  and release operator docs
- `docs/active/items/`: active item records for `OPEN`, `IN_PROGRESS`,
  `BLOCKED`, and `DEFERRED` work
- `docs/active/plans/`: current execution/integration plans (the RC release
  execution plan plus suite/cross-product plans such as the ecosystem bootstrap
  and product-family integration plans)

If another doc conflicts with `docs/active/`, `docs/active/` wins for current
status.

For GitHub-primary backlog items, workflow status is an exception: the linked
`emulebb/emulebb` issue and the public org-level `eMuleBB Roadmap` Project #2
own current state, priority, release placement, discussion, ownership, and PR
linkage. The canonical endpoints are
`https://github.com/emulebb/emulebb/issues` and
`https://github.com/orgs/emulebb/projects/2`. The local active item doc remains
the engineering spec/evidence record. Such files carry `workflow: github` and
`github_issue:` front matter. Their legacy `status:` field is retained only for
the current taxonomy tooling until the active-doc model is migrated more
broadly.

## Reference Docs

- `docs/rest/`: current REST contract and API reference
- `docs/reference/`: durable current product guides and specialist references
- `docs/dependencies/`: current dependency health and decision records
- `docs/history/`: closed item records, dated review findings, historical
  comparisons, source salvage, old ledgers, dated audits, stale dependency
  analysis, and superseded release plans

Reference docs may preserve historical branch names, old paths, and old
decisions as provenance, but they do not override active status.

## Ideas

`docs/ideas/` contains exploratory proposals only. These documents are not
active implementation plans and must not be treated as current release scope or
current branch direction unless a future active item explicitly promotes a
specific slice.

Examples: IPv6 Kad experiments and source-structure proposals.

Abandoned exploratory proposals move to `docs/history/ideas/` and are retained
as provenance only.

## Writing Rules

- Keep current decisions in `docs/active/`, not in historical reference docs.
- Current non-item Markdown filenames use uppercase words separated by hyphens:
  `WORKSPACE-POLICY.md`, `GUIDE-NETWORK.md`, `REST-API-CONTRACT.md`.
- `docs/INDEX.md` is also the MkDocs web entrypoint. Do not add a separate
  lowercase `docs/index.md`; case-only twins are unsafe on Windows checkouts.
- `docs/index.html` is the static MkDocs root redirect to `INDEX/` for GitHub
  Pages hosting.
- Release-control filenames may include version dots inside the existing
  `RELEASE-*` family, such as `RELEASE-0.7.3.md`.
- Active and historical item records keep their stable item-ID filenames, such
  as `BUG-117.md` and `CI-039.md`.
- Historical provenance docs are not renamed only for style.
- Move closed item records (`DONE`, `PASSED`, `WONT_DO`) to
  `docs/history/items/`.
- Move dated review reports to `docs/history/reviews/` after they stop driving
  active execution.
- Move stale audit reports to `docs/history/audits/`; move release-specific
  audit snapshots under that release's `docs/history/release-*` folder.
- Prefix historical analysis files outside the standard closed-item/review
  folders with `HIST-`; prefix speculative proposals with `IDEA-`.
- Keep the current release execution sequence in one active plan. Superseded
  release cluster plans belong under `docs/history/`.
- Every actionable active task must have its own item ID under
  `docs/active/items/`; release dashboards and plans should point to item IDs
  instead of carrying anonymous task rows.
- New externally actionable backlog items should be GitHub-primary by default:
  create or update the local item, the `emulebb/emulebb` issue, and membership
  in the `eMuleBB Roadmap` Project #2 unless the item is explicitly local-only,
  historical, exploratory, or provenance-only.
- Do not create new top-level Markdown files in `docs/` unless they are policy
  or navigation entry points.
- Add new exploratory proposals under `docs/ideas/` with an explicit
  exploratory-only banner.
- Keep Markdown tables browser-readable. Prefer two to four columns, move long
  evidence text into bullets below the table, split large inventories by
  section, and avoid long comma-separated ID lists inside table cells.
- Before RC documentation closeout, current docs under `docs/active/`,
  `docs/reference/`, and `docs/rest/` should pass
  `python scripts\docs-structure-check.py --fail-on-wide-tables`. Historical
  provenance docs may stay warning-only unless they are promoted back into
  current release guidance.

## Item IDs And Statuses

Item IDs use a typed key format: `PREFIX-###`. Prefixes are uppercase, followed
by a hyphen and a zero-padded numeric sequence. IDs are never reused; skipped
ranges stay skipped.

Canonical core prefixes:

- `BUG`: user-visible or runtime correctness defects
- `FEAT`: product behavior, UX, or capability work
- `REF`: refactoring, architecture cleanup, and internal modernization
- `CI`: build, packaging, validation, release proof, and tooling gates

Integration-specific prefixes are allowed only when they name an external
consumer or adapter surface. Current accepted integration prefixes are `AMUT`
and `ARR`.

Canonical active statuses:

- `OPEN`: accepted backlog item that is not currently being worked
- `IN_PROGRESS`: active implementation, validation, or investigation is
  underway
- `BLOCKED`: cannot proceed without an external decision, dependency, or proof
- `DEFERRED`: intentionally postponed but still a valid item

Canonical closed statuses:

- `DONE`: implementation or documentation work landed
- `PASSED`: validation, audit, proof, or gate succeeded without necessarily
  landing an implementation
- `WONT_DO`: explicitly rejected or accepted as not worth doing

Legacy title-case status spellings in historical files are provenance only.
`Wont-Fix` maps to `WONT_DO`.

Use `python scripts\docs-item-taxonomy-check.py` after item or active-index
changes to validate item IDs, statuses, duplicate front matter IDs, and active
index consistency.

Use `python scripts\github-roadmap-sync.py` to preview and apply
GitHub-primary issue and Project #2 synchronization for all active backlog
items under `docs/active/items`. Use
`python scripts\github-roadmap-check.py` after migration to validate local
GitHub metadata; pass `--github` when the local GitHub token has `project`
scope and network access.

Use [reference/BACKLOG-PROCESS](reference/BACKLOG-PROCESS.md) as the repeatable
operator runbook for creating, updating, validating, and closing backlog items.

Use `python scripts\docs-structure-check.py` after current-doc navigation,
naming, or table-heavy edits. Use
`python scripts\docs-structure-check.py --fail-on-wide-tables` before RC docs
closeout and before publishing current docs as HTML.

Use MkDocs for browser-formatted documentation:

- install dependencies with `python -m pip install -r requirements-docs.txt`
- preview locally with `python -m mkdocs serve`
- run the repeatable local publish gate with
  `python scripts\docs-publish-check.py`
- the publish gate runs item taxonomy, docs structure, GitHub roadmap metadata,
  and strict MkDocs HTML generation checks

Generated HTML belongs under `.local/mkdocs-site` and must not be committed.
GitHub Pages publishing is owned by `.github/workflows/docs-site.yml`; the
rendered site URL is `https://emulebb.github.io/emulebb-tooling/`.
