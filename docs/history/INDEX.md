# History Archive

This is the map of `docs/history/` — the workspace's provenance archive.

!!! note "Provenance only"
    Everything under `docs/history/` is retained for history: closed item
    records, dated reviews and audits, superseded plans, abandoned ideas, and
    old ledgers. It does **not** determine current status. Current truth lives
    in [`docs/active/`](../active/INDEX.md); see the
    [Documentation Policy](../DOCS-POLICY.md) for how document role is decided
    by path. For the retired stale experimental branch specifically, see
    [Historical References](../HISTORICAL-REFERENCES.md).

## Archive Sections

| Section | Contents |
| --- | --- |
| [`items/`](items/INDEX.md) | Closed item records (`DONE`, `PASSED`, `WONT_DO`) — 253 files: 132 BUG, 48 FEAT, 40 CI, 30 REF, 2 AMUT, 1 ARR. Stable item-ID filenames; IDs are never reused. |
| `reviews/` | 19 dated review reports (2026-04 → 2026-05) plus the mods/eMuleAI scan, kept after they stopped driving active execution. |
| `release-0.7.3/` | Superseded 0.7.3 execution plans, gate history, community-parity audit, proof-evidence log, and 8 dated beta-readiness audits in `release-0.7.3/audits/`. |
| `audits/` | 13 standalone audit snapshots covering bugs, code quality, code review, dead code, defects, Kad, security, C++ safety, architecture, and REST custom code. |
| `features/` | 6 historical feature analyses (peer-ban engines, media thumbnails, and related capability studies). |
| `dependencies/` | 2 dependency-removal records (DLL and source-tree disposition). |
| `ideas/` | 4 abandoned exploratory proposals: Boost/POCO, CMake/Ninja/vcpkg, the 2026 modernization roadmap, and the MFC restructure guidance. |
| `guides/` | 4 superseded product-guide snapshots (Diagnostics, Setup, Tools Menu, Troubleshooting). Current copies live in [`reference/`](../reference/GUIDE-DIAGNOSTICS.md). |
| `rest/` | 1 historical REST plan (`HIST-PLAN-API-SERVER`). The current contract lives under [`docs/rest/`](../rest/REST-API-CONTRACT.md). |

## Ledgers And Roll-Ups

These top-level history files are cross-cutting ledgers rather than single
records:

| Document | Purpose |
| --- | --- |
| [Backlog History](BACKLOG-HISTORY.md) | Compact historical reference for the active backlog (not the live status source). |
| [Backlog Dependency Graph](BACKLOG-DEPENDENCY-GRAPH.md) | Implementation-ordering hints across backlog items; not a release plan. |
| [Backlog Source Salvage](BACKLOG-SOURCE-SALVAGE.md) | Where major historical source documents fed the active backlog. |
| [History Changelog](HISTORY-CHANGELOG.md) | Code-review trail across the community lineage (v0.60d → v0.70b → v0.72a). |
| [0.70b vs 0.72a Comparison](HISTORY-070-VS-072.md) | Detailed community-build comparison report (2026-03-29). |
| [Refactor & Task Roadmap](REFACTOR-TASKS.md) | Historical refactor roadmap from the `v0.72a-broadband-dev` line. |
| [Session Resume (2026-05-12)](HIST-SESSION-RESUME-2026-05-12.md) | A dated session-termination handoff snapshot. |

!!! info "One current-work exception"
    [CI-010 Warning Cleanup Progress Log](CI-010-WARNING-CLEANUP-PROGRESS.md)
    lives here for convenience but tracks the **active** item
    [`CI-010`](../active/items/CI-010.md) (`IN_PROGRESS`). It is the only file
    in this archive that follows current work rather than closed history.
