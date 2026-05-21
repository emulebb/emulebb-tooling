# eMule Tooling

This repo contains the supporting documentation, helper scripts, audit
material, and central workspace policy for the current eMule workspace.

It is not the app repo and it is not the build orchestrator. The current split
is:

- app source: `repos\eMule`
- build/test orchestration: `repos\eMule-build` and `repos\eMule-build-tests`
- companion web UI: `repos\amutorrent`
- local live-test ED2K server: `repos\emulebb-ed2k-server`
- tooling docs and helpers: this repo

## Start Here

- active local backlog/spec and release status:
  [`docs/active/INDEX.md`](docs/active/INDEX.md)
- long-form reference docs and topic map: [`docs/INDEX.md`](docs/INDEX.md)
- historical-reference rules for the stale experimental branch:
  [`docs/HISTORICAL-REFERENCES.md`](docs/HISTORICAL-REFERENCES.md)
- workspace-wide operating contract:
  [`docs/WORKSPACE-POLICY.md`](docs/WORKSPACE-POLICY.md)

## What This Repo Owns

- central workspace policy: [`docs/WORKSPACE-POLICY.md`](docs/WORKSPACE-POLICY.md)
- documentation ownership policy: [`docs/DOCS-POLICY.md`](docs/DOCS-POLICY.md)
- repeatable backlog process:
  [`docs/reference/BACKLOG-PROCESS.md`](docs/reference/BACKLOG-PROCESS.md)
- reference-doc index: [`docs/INDEX.md`](docs/INDEX.md)
- browser-formatted docs entrypoint: [`docs/INDEX.md`](docs/INDEX.md#browser-site)
- active backlog/spec index: [`docs/active/INDEX.md`](docs/active/INDEX.md)
- GitHub-primary future roadmap:
  [`docs/active/FUTURE-ROADMAP.md`](docs/active/FUTURE-ROADMAP.md)
- product guide: [`docs/reference/GUIDE-EMULEBB.md`](docs/reference/GUIDE-EMULEBB.md)
- development guide and recurring product-doc refresh workflow:
  [`docs/reference/DEVELOPMENT-GUIDE.md`](docs/reference/DEVELOPMENT-GUIDE.md)
- historical API sidecar plan:
  [`docs/history/rest/HIST-PLAN-API-SERVER.md`](docs/history/rest/HIST-PLAN-API-SERVER.md)
- modernization idea:
  [`docs/ideas/IDEA-MODERNIZATION-2026.md`](docs/ideas/IDEA-MODERNIZATION-2026.md)

This repo does not own workspace materialization, app source, or build/test
execution contracts. It is the authoritative documentation home for
workspace-wide policy and the place for deeper engineering notes and helper
scripts that operate inside the canonical workspace.

Documentation is intentionally organized by document role:

- `docs/active/` = active revalidated local specs, release control, item
  evidence, execution plans, and dated review trail
- `docs/architecture/`, `docs/rest/`, and `docs/reference/` = durable technical
  and product reference
- `docs/dependencies/DEP-STATUS.md` = current dependency decision record
- `docs/history/` = provenance, historical analysis, dated audits, old plans,
  and closed item records
- `docs/ideas/` = exploratory proposals only, not active implementation plans

If a status statement in `docs/` conflicts with `docs/active`, treat
`docs/active` as authoritative for the current local backlog state. For
future-roadmap items marked `workflow: github`, the linked GitHub issue and the
public `eMule BB Roadmap` org project are authoritative for workflow state.

The central policy defaults to low-drift hardening and bug-fix work. Major
behavioral changes are exception work and must be explicitly justified rather
than blended into routine cleanup or modernization.

Shared CI and policy guard code lives under `ci\`:

- `ci\check-workspace-policy.py` is the Python workspace policy audit entrypoint
  used by `python -m emule_workspace validate`
- `ci\policy_guards.py` owns reusable guard implementations such as tracked-file
  privacy, basic hygiene, and explicit clean-worktree checks
- `ci\guard-tracked-files.py`, `ci\check-basic-hygiene.py`, and
  `ci\check-clean-worktree.py` are operator-facing Python wrappers
- `.github\workflows\reusable-baseline.yml` is the reusable baseline workflow;
  consumers should pin the stable ref documented in
  [`docs/reference/CI-BASELINE.md`](docs/reference/CI-BASELINE.md)
- `.github\workflows\docs-site.yml` builds the MkDocs Material documentation
  site and deploys it to GitHub Pages from `main`

Normalization helpers live here too:

- `helpers\source-normalizer.py` checks or rewrites tracked text files to match
  repo `.editorconfig` and `.gitattributes`
- `helpers\rc-string-table.py` audits and edits Windows `.rc` string tables.
  For release localization it is the coverage/quality gate: it checks required
  resource IDs, duplicate IDs, printf/literal-percent marker parity, line-break
  escape parity, mnemonic accelerator parity, copied-English strings, and
  optional semantic quality rules.
- `helpers\rc-translate-missing.py` adds only missing eMule BB managed strings
  to supported language `.rc` files. It preserves existing translations by
  default, refuses stock-string drift after writing, and can produce
  `--review-packet` TSVs. Use curated `--manual-tsv` input for one language or
  `--manual-dir` per-language TSVs for all stock languages before
  relying on machine translation drafts; use `--draft-only
  --no-machine-translate` when preparing review packets without touching `.rc`
  files. Parallel processing is supported only for stock eMule `.rc` review
  packets through `--all-stock-targets`; it intentionally refuses concurrent
  `.rc` writes and machine-translation calls.
- `helpers\rc-release-languages.json` is the canonical machine-readable release
  language manifest. It must enumerate every stock `srchybrid\lang\*.rc` file;
  release validation rejects a smaller language subset.
- `helpers\rc-release-localization-ids.txt` lists the release-facing eMule BB
  resource IDs that every supported language must contain.
- `helpers\rc-translation-identical-ok-ids.txt` allow-lists IDs where identical
  English-looking text is intentional, such as acronyms or common protocol/UI
  terms.
- `helpers\rc-translation-quality-rules.json` records language-specific traps
  for meaningful translations, such as false friends and tray/taskbar wording.
- `helpers\pages-site-tools.py` validates the static `eMulebb-pages` HTML,
  canonical locale links, sitemap, and page asset policy; it can also render
  `sitemap.xml` from the canonical locale table
- `hooks\pre-commit` is the shared workspace pre-commit hook entrypoint
- `python -m emule_workspace sync` configures repo-local `core.hooksPath` to
  use that shared hook
- `scripts\github-roadmap-sync.py` previews or applies the GitHub-primary
  future-roadmap import to `eMulebb/eMule` issues and the `eMule BB Roadmap`
  project.
- `scripts\github-roadmap-check.py` validates local GitHub roadmap metadata,
  and can query GitHub when run with `--github`.
- `scripts\docs-item-taxonomy-check.py` validates backlog item IDs, required
  active-item front matter, filename/front-matter alignment, active index links,
  status counts, and table ordering.
- `scripts\docs-structure-check.py` validates current Markdown naming,
  navigation coverage, top-level headings, and wide table rows that can render
  poorly in browsers.

Documentation can be previewed as formatted HTML with MkDocs:

```powershell
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

Set `$env:NO_MKDOCS_2_WARNING='1'`, then use
`python -m mkdocs build --strict` for the same local site build gate used by
CI. The generated site is written under `.local\mkdocs-site`.
Published documentation is served from
`https://emulebb.github.io/eMule-tooling/`.

Release translation rule: preserve stock/eMule translations as they are; add
or refine only new eMule BB labels, and make those translations meaningful for
the target language. Machine translation is acceptable only as a draft, never
as an unreviewed final result. Historical or external translation engines,
including the eMuleAI analysis tree, may inspire validation checks but are not
translation sources for release `.rc` files.

Deterministic label update flow: add the English string to `emule.rc`, add its
ID to `helpers\rc-release-localization-ids.txt`, generate all-stock review
packets, review/translate each new label using stock terminology in the same
language first, compare external material only as a sanity check, apply curated
per-language TSVs through `--manual-dir`, then run the release localization
audit. Do not hand-edit broad legacy translations during a label update.

Typical release localization audit:

```powershell
python helpers\rc-string-table.py --cross-reference --quality-audit --fail-on-quality-warning --show-extra --allow-identical-ids helpers\rc-translation-identical-ok-ids.txt --quality-rules helpers\rc-translation-quality-rules.json --english-rc ..\..\workspaces\workspace\app\eMule-main\srchybrid\emule.rc --require-ids helpers\rc-release-localization-ids.txt --release-languages helpers\rc-release-languages.json
```

Release language manifest audit:

```powershell
python helpers\rc-string-table.py --audit-release-manifest --english-rc ..\..\workspaces\workspace\app\eMule-main\srchybrid\emule.rc --release-languages helpers\rc-release-languages.json
```

Missing managed-label report:

```powershell
python helpers\rc-string-table.py --missing-report --fail-on-missing --english-rc ..\..\workspaces\workspace\app\eMule-main\srchybrid\emule.rc --require-ids helpers\rc-release-localization-ids.txt --release-languages helpers\rc-release-languages.json
```

Stock-language review packets, safe to run in parallel:

```powershell
python helpers\rc-translate-missing.py --source-rc ..\..\workspaces\workspace\app\eMule-main\srchybrid\emule.rc --require-ids helpers\rc-release-localization-ids.txt --all-stock-targets --draft-only --no-machine-translate --ignore-cache --review-dir $env:TEMP\emule-rc-review --jobs 8
```

Apply curated per-language TSVs after review:

```powershell
python helpers\rc-translate-missing.py --source-rc ..\..\workspaces\workspace\app\eMule-main\srchybrid\emule.rc --require-ids helpers\rc-release-localization-ids.txt --all-stock-targets --no-machine-translate --ignore-cache --manual-dir $env:TEMP\emule-rc-reviewed --jobs 1
```

Tracked PowerShell is not used for workspace orchestration. Keep future
workspace automation in Python unless `docs\WORKSPACE-POLICY.md` explicitly
allows a PowerShell runtime asset.

## Workspace Convention

Canonical paths are expressed through `EMULE_WORKSPACE_ROOT`:

- repos live under `EMULE_WORKSPACE_ROOT\repos\...`
- app worktrees live under `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\...`

Helper scripts in this repo should follow that model and should not encode old
fixed `eMulebb` workspace paths.

For the full workspace operating contract, use
`EMULE_WORKSPACE_ROOT\repos\eMule-tooling\docs\WORKSPACE-POLICY.md`.

## Notes

- many documents here are design notes, audits, and planning artifacts rather
  than step-by-step operator guides
- references to `stale-v0.72a-experimental-clean` are preserved as historical
  provenance only; see [`docs/HISTORICAL-REFERENCES.md`](docs/HISTORICAL-REFERENCES.md)
- concrete tool-install paths may still appear in historical audit documents
  when they are part of a captured environment snapshot
