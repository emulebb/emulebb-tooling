# Backlog Source Salvage

This records where major historical source documents fed the active backlog.
It is intentionally compact; detailed provenance lives in item docs and dated
review records.

## Historical Docs

| Source | Salvaged into |
|--------|---------------|
| `history/audits/AUDIT-BUGS.md` | early `BUG-*` triage and fixed/wont-fix decisions |
| `history/audits/AUDIT-DEFECTS.md` | [BUG-001](items/BUG-001.md), [REF-004](items/REF-004.md) |
| `history/audits/AUDIT-SECURITY.md` | [BUG-006](items/BUG-006.md), [REF-021](../active/items/REF-021.md), [REF-028](../active/items/REF-028.md) |
| `history/audits/AUDIT-DEADCODE.md` | [REF-002](items/REF-002.md) through [REF-007](items/REF-007.md), [REF-017](items/REF-017.md) through [REF-019](items/REF-019.md) |
| `history/audits/AUDIT-KAD.md` | [FEAT-001](../active/items/FEAT-001.md) through [FEAT-006](../active/items/FEAT-006.md), [CI-007](../active/items/CI-007.md) |
| `history/audits/AUDIT-CODEQUALITY.md` | [CI-001](items/CI-001.md), [CI-002](../active/items/CI-002.md) through [CI-006](../active/items/CI-006.md) |
| `history/ideas/IDEA-BOOST.md` | [REF-008](items/REF-008.md) through [REF-014](items/REF-014.md) |
| `GUIDE-LONGPATHS.md` | [FEAT-010](items/FEAT-010.md) |
| `history/rest/HIST-PLAN-API-SERVER.md` | [FEAT-013](items/FEAT-013.md), [FEAT-014](../active/items/FEAT-014.md) |
| `FEATURE-BROADBAND.md` | [FEAT-015](items/FEAT-015.md), [FEAT-023](items/FEAT-023.md) |
| `FEATURE-MODERN-LIMITS.md` | [FEAT-016](items/FEAT-016.md) |
| `history/audits/AUDIT-WWMOD.md` | Windows modernization refactors and UI/build policy items |
| `history/audits/AUDIT-CODEREVIEW.md` | [BUG-007](items/BUG-007.md), [BUG-008](items/BUG-008.md), [REF-028](../active/items/REF-028.md) |

## Analysis Inputs

- eMuleAI v1.3 seeded early persistence, shared-directory, destructor, and
  startup/config references.
- `stale-v0.72a-experimental-clean` remains a retired reference source for
  implementation ideas only.
- Current-main reviews from April and May 2026 own the live landed/open status.

## Confirmed Done Provenance

Do not use this file as a complete done ledger. For complete status, use
[docs/active/INDEX](../active/INDEX.md). Representative early confirmed
items include `BUG-009` through `BUG-012`, `BUG-015`, `BUG-016`, `FEAT-015`,
`FEAT-016`, `FEAT-023`, `FEAT-024`, `FEAT-025`, `FEAT-038`, and `FEAT-013`.
