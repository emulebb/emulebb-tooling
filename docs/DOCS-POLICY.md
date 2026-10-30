# Documentation Policy

This repo keeps maintained Markdown under `docs/`. Document authority is
determined by path and lifecycle, not by age or filename alone.

## Current Authority

- `docs/active/` owns current organization-wide direction, compatibility,
  quality, test, and release-operation guidance.
- `docs/products/<product>/` owns current product scope, design, policy, and
  backlog records.
- `docs/reference/`, `docs/rest/`, and `docs/dependencies/` own durable current
  specialist references and contracts.
- `docs/history/` is a curated archive overview and essential evidence set. It
  is never workflow or product-direction authority.

The canonical organization-wide lifecycle and focus document is
`docs/active/PRODUCT-DIRECTION.md`. Other current documents link to it instead
of restating portfolio or roadmap direction.

For GitHub-primary work, Project #3 owns `Status`, `Product`, `Phase`, and
`Priority`; the owning product issue owns discussion, ownership, and pull
request linkage; the local item owns the durable engineering specification and
retained evidence. Project #2 and closed MFC issues are archive provenance.

## Active Work Rules

- Active item records live only below the owning product's `active/items/`
  directory and appear in that product's active index.
- Every active product item has an open owning issue and current Project #3
  placement unless policy explicitly marks it local-only infrastructure.
- Active directories may contain only `OPEN`, `IN_PROGRESS`, or `BLOCKED`
  work. Completed, rejected, parked, ownerless, and indefinitely deferred work
  must not remain active.
- Future direction without an implementation commitment belongs in concise
  product design. It does not require a backlog item or standalone idea file.
- Rust active docs are limited to `active/INDEX.md` and `active/items/`.
  Current scope stays in `RELEASE-SCOPE.md`; implemented structure stays in
  `design/architecture.md`; genuinely forward design stays in `design/`.

## Archive And Retention

- Preserve stable IDs, final dispositions, essential release evidence, binding
  compatibility/security decisions, and unique source-lineage records.
- Reconcile completed temporary plans, checklists, dated reviews, and audits
  into their owning item, current policy, or one concise evidence summary, then
  delete the redundant detail.
- Retain detailed closed records for the active Rust product under
  `docs/products/emulebb-rust/history/items/`; publish their index, not every
  individual record.
- Legacy MFC and retired integration IDs live in
  `docs/history/LEGACY-ITEM-CATALOG.md`. Their full specifications remain
  recoverable from the archival Git commit recorded there.
- Do not create new session-resume archives, duplicate backlog ledgers,
  standalone audit dumps, or historical guide snapshots.
- Historical source paths and branch names are provenance only and never
  override current `main`, product policy, or active issue state.

## Writing Rules

- Keep one authority for each decision and link to it elsewhere.
- Current non-item filenames use uppercase words separated by hyphens.
- Stable item filenames match their item IDs exactly; IDs are never reused.
- Do not create new top-level Markdown files unless they are policy or
  navigation entry points.
- Keep tables browser-readable; move long evidence into prose or bullets.
- Product documentation and release notes for eMuleBB Rust are English-only.
  Organization-site translations are limited to the homepage and FAQ and are
  not product translations.

## Item IDs And Statuses

Core legacy IDs use `PREFIX-###`; Rust IDs use `RUST-<CLASS>-<NNN>`. The
migrated Rust-owned `CI-054` record keeps its stable legacy ID as a documented
exception. Supported classes are bug, feature, refactor, and CI/evidence work.

Canonical active statuses are `OPEN`, `IN_PROGRESS`, and `BLOCKED`. Canonical
closed statuses are `DONE`, `PASSED`, and `WONT_DO`. `DEFERRED` remains valid
only as an archival recorded status; it is not an active-work state.

## Validation And Publishing

Run these checks after documentation changes:

```powershell
python scripts\docs-publish-check.py
python scripts\docs-item-taxonomy-check.py
python scripts\docs-structure-check.py
python scripts\github-roadmap-check.py
python scripts\github-roadmap-check.py --product emulebb-rust
python -m mkdocs build --strict
```

Generated HTML belongs below the configured output root or another ignored
local build directory and must not be committed. GitHub Pages publishing is
owned by `.github/workflows/docs-site.yml`.
