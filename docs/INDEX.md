# eMule Documentation Index

This directory is the single Markdown home for the tooling repo. Use
[DOCS-POLICY](DOCS-POLICY.md) for ownership rules.

## Start Here

| Need | Primary Doc |
|---|---|
| Workspace policy | [WORKSPACE-POLICY](WORKSPACE-POLICY.md) |
| AI contributor repeatability checklist | [reference/AGENT-CHECKLIST](reference/AGENT-CHECKLIST.md) |
| Active backlog and RC release status | [active/INDEX](active/INDEX.md) |
| Repeatable backlog process | [reference/BACKLOG-PROCESS](reference/BACKLOG-PROCESS.md) |
| Documentation ownership rules | [DOCS-POLICY](DOCS-POLICY.md) |
| Browser-formatted documentation | [MkDocs site](INDEX.md#browser-site) |
| Historical-reference rules | [HISTORICAL-REFERENCES](HISTORICAL-REFERENCES.md) |
| Repo-level navigation | [GitHub README](https://github.com/emulebb/emulebb-tooling/blob/main/README.md) |

If a status claim outside `docs/active/` conflicts with `docs/active/`, treat
`docs/active/` as authoritative for current local backlog and release state.
For GitHub-primary backlog items marked `workflow: github`, the linked
`emulebb/emulebb` issue and the public `eMuleBB Roadmap` org Project #2 are
authoritative for workflow state. Canonical workflow endpoints are
`https://github.com/emulebb/emulebb/issues` and
`https://github.com/orgs/emulebb/projects/2`.

## Active Work

| Document | Description |
|---|---|
| [active/INDEX](active/INDEX.md) | Active backlog dashboard and item tables |
| [active/FUTURE-ROADMAP](active/FUTURE-ROADMAP.md) | GitHub-primary post-beta future roadmap |
| [active/plans/P2P-OVERLORD-PRODUCT-FAMILY-INTEGRATION](active/plans/P2P-OVERLORD-PRODUCT-FAMILY-INTEGRATION.md) | Post-beta p2p-overlord product-family integration plan |
| [active/RELEASE-0.7.3](active/RELEASE-0.7.3.md) | RC release control document |
| [active/RELEASE-0.7.3-CHECKLIST](active/RELEASE-0.7.3-CHECKLIST.md) | RC release operator checklist |
| [active/RELEASE-0.7.3-RUNBOOK](active/RELEASE-0.7.3-RUNBOOK.md) | RC release operator runbook |
| [active/plans/RELEASE-0.7.3-EXECUTION-PLAN](active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md) | Current RC release execution plan |
| `active/items/` | Active item records for Open, In Progress, Blocked, and Deferred work |
| `history/items/` | Closed item records |
| `history/reviews/` | Dated revalidation reviews |
| `history/audits/` | Historical broad audit reports |
| `history/release-0.7.3/` | Superseded beta gate evidence, release audit snapshots, and old cluster plans |

GitHub-primary roadmap-backed backlog helper scripts live under `scripts/`:

- `github-roadmap-sync.py` previews or applies the roadmap-backed backlog
  import to `emulebb/emulebb` issues and the `eMuleBB Roadmap` Project #2.
- `github-roadmap-check.py` validates local GitHub metadata, and can query
  GitHub when run with `--github`.

## Reference Families

| Folder | Role |
|---|---|
| `dependencies/` | Current dependency health and decision records |
| `history/` | Closed item records, dated reviews, historical comparisons, source salvage, and old ledgers |
| `ideas/` | Exploratory proposals only, not active implementation plans |
| `reference/` | Current product guides and durable specialist references |
| `rest/` | REST contract and API reference |

## Common References

- **[reference/AGENT-CHECKLIST](reference/AGENT-CHECKLIST.md)**
  - Description: Repeatable operating checklist for AI agents contributing to the
                 workspace

- **[reference/GUIDE-EMULEBB](reference/GUIDE-EMULEBB.md)**
  - Description: eMuleBB product manual entry point, setup, tools, diagnostics, and
                 compatibility

- **[reference/BACKLOG-PROCESS](reference/BACKLOG-PROCESS.md)**
  - Description: Repeatable workflow for creating, updating, validating, and closing
                 backlog records

- **[reference/CI-BASELINE](reference/CI-BASELINE.md)**
  - Description: Reusable CI baseline workflow contract

- **[reference/DEVELOPMENT-GUIDE](reference/DEVELOPMENT-GUIDE.md)**
  - Description: Development, validation, CI, packaging, command-line, and recurring
                 guide refresh workflow

- **[reference/RELEASE-BRANCHING-AND-PACKAGING](reference/RELEASE-BRANCHING-AND-PACKAGING.md)**
  - Description: Official release branch, tag, version, and portable package naming
                 policy

- **[reference/GUIDE-SETUP](reference/GUIDE-SETUP.md)**
  - Description: Install model, first-run profile behavior, release-aware setup, and
                 evidence links

- **[reference/GUIDE-NETWORK](reference/GUIDE-NETWORK.md)**
  - Description: eD2K, Kad, binding, ports, UPnP, firewall, and REST listener basics

- **[reference/GUIDE-SHARING](reference/GUIDE-SHARING.md)**
  - Description: Shared directories, monitored shares, large libraries, and share-ignore
                 policy

- **[reference/GUIDE-DOWNLOADS-SEARCH](reference/GUIDE-DOWNLOADS-SEARCH.md)**
  - Description: Downloads, search, categories, broadband upload policy, modern limits,
                 and copy workflows

- **[reference/GUIDE-PREFERENCES](reference/GUIDE-PREFERENCES.md)**
  - Description: Single preference manual: `preferences.ini`, compatibility,
                 defaults/ranges, schema coverage, and REST mutation

- **[reference/GUIDE-PERSISTENCE-FILES](reference/GUIDE-PERSISTENCE-FILES.md)**
  - Description: Runtime `.met` and `.dat` file roles, structure, editability, backup
                 importance, and recovery notes

- **[reference/GUIDE-CONTROLLERS-REST](reference/GUIDE-CONTROLLERS-REST.md)**
  - Description: REST, aMuTorrent, Arr, qBit, and Torznab controller guidance

- **[reference/ED2K-PROJECT-INVENTORY](reference/ED2K-PROJECT-INVENTORY.md)**
  - Description: eD2K/eMule ecosystem inventory, including ED2K servers, server lists,
                 clients, controllers, libraries, and historical mods

- **[reference/GUIDE-IP-FILTERS](reference/GUIDE-IP-FILTERS.md)**
  - Description: IP filter storage, seeded URLs, formats, and practical use

- **[reference/GUIDE-LONGPATHS](reference/GUIDE-LONGPATHS.md)**
  - Description: Long-path product behavior, setup, limits, and troubleshooting

- **[reference/KEYBOARD-SHORTCUTS](reference/KEYBOARD-SHORTCUTS.md)**
  - Description: Main shell and list keyboard shortcut reference

- **[reference/GUIDE-TROUBLESHOOTING](reference/GUIDE-TROUBLESHOOTING.md)**
  - Description: Symptom-led diagnostics, support evidence, and testing/performance
                 context

- **[dependencies/DEP-STATUS](dependencies/DEP-STATUS.md)**
  - Description: Current third-party dependency decision record

- **[rest/REST-API-ADAPTERS](rest/REST-API-ADAPTERS.md)**
  - Description: Adapter-specific REST, qBit, Torznab, Arr, and aMuTorrent contract
                 notes

- **[rest/REST-API-CONTRACT](rest/REST-API-CONTRACT.md)**
  - Description: Human-readable broadband REST contract

- **[rest/REST-API-OPENAPI](rest/REST-API-OPENAPI.yaml)**
  - Description: Canonical machine-readable `/api/v1` OpenAPI contract

- **[rest/REST-API-PARITY-INVENTORY](rest/REST-API-PARITY-INVENTORY.md)**
  - Description: Completed REST/WebServer action parity ledger

## Browser Site

This Markdown tree can be rendered with MkDocs Material:

```powershell
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

Use `python -m mkdocs build --strict` for CI-equivalent local validation. The
Material theme emits a current MkDocs 2.0 compatibility notice as a warning, so
set `$env:NO_MKDOCS_2_WARNING='1'` before strict local builds. The generated
HTML is written to `.local/mkdocs-site` and deployed to GitHub Pages by
`.github/workflows/docs-site.yml` on `main` at
`https://emulebb.github.io/emulebb-tooling/`.

## Exploratory Ideas

- **[ideas/IDEA-AMULE-WATCHLIST](ideas/IDEA-AMULE-WATCHLIST.md)**
  - Description: Exploratory aMule reference watchlist; not an active plan

- **[ideas/IDEA-MODERNIZATION-2026](ideas/IDEA-MODERNIZATION-2026.md)**
  - Description: Historical modernization roadmap idea; not an active plan

- **[ideas/IDEA-IPV6-KAD-NETWORK](ideas/IDEA-IPV6-KAD-NETWORK.md)**
  - Description: Exploratory IPv6-native Kad network design inspired by
                 qBittorrent/libtorrent dual-stack DHT state separation; not an active
                 plan

- **[ideas/IDEA-RESTRUCTURE](ideas/IDEA-RESTRUCTURE.md)**
  - Description: Exploratory source-structure idea; not an active plan

## Abandoned Ideas

| Document | Description |
|---|---|
| [history/ideas/IDEA-BOOST](history/ideas/IDEA-BOOST.md) | Abandoned Boost/POCO adoption exploration; provenance only |
| [history/ideas/IDEA-CMAKE](history/ideas/IDEA-CMAKE.md) | Abandoned CMake/Ninja/vcpkg adoption exploration; provenance only |

## Notes

- Historical branch names such as `stale-v0.72a-experimental-clean` and old
  branch labels may appear in reference docs as provenance only.
- Preserve commit ids and historical branch names where they add provenance,
  but do not treat them as current-branch guidance unless `docs/active/`
  explicitly says the work is landed on `main`.
