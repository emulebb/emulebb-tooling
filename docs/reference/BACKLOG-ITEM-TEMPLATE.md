# Backlog Item Template

This is the canonical shape for an active backlog item under
`docs/active/items/<ID>.md`. It exists so every item reads the same way. Use
[Backlog Process](BACKLOG-PROCESS.md) for the surrounding create/update/close
workflow; this page only fixes the **document structure and section
vocabulary**.

Front-matter rules, ID taxonomy, and status values are owned by
[Documentation Policy](../DOCS-POLICY.md). The taxonomy tool validates front
matter and IDs; section structure below is a convention, not yet a hard gate.

## Skeleton

```markdown
---
id: FEAT-000
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/<number>
title: Short sentence-case item title
status: OPEN
priority: Minor
category: feature
labels: [area, risk, evidence]
milestone: post-0.7.3
created: YYYY-MM-DD
source: short provenance note
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/<number>. This local document is retained as an engineering spec/evidence record.

[body H1 goes here as "# <ID> - <title>" -- see Title And Heading Rules below]

## Summary

One or two short paragraphs: what the item is and why it exists.

## Acceptance Criteria

- [ ] Concrete, checkable outcome
- [ ] Concrete, checkable outcome
```

The `> Workflow status` blockquote appears only on `workflow: github` items;
local-only items omit it.

## Title And Heading Rules

- Every item body starts with a single H1 of the form `# <ID> - <title>`, where
  `<title>` is the front-matter `title` value **verbatim**. The H1, the
  front-matter `title`, and the `docs/active/INDEX.md` row title must match.
- On `workflow: github` items the H1 follows the workflow blockquote.
- Use `##` for the sections below and `###` for sub-points. Do not introduce a
  second H1.

## Section Vocabulary

Use these canonical section names, in this order. Only `Summary` and
`Acceptance Criteria` are required; include the rest when they carry real
content. Do not invent near-synonyms — fold content into the closest canonical
section instead.

| Order | Section | Required | Use it for |
|-------|---------|----------|------------|
| 1 | `## Summary` | yes | What the item is and why it matters, briefly. |
| 2 | `## Current State` | no | Evidence of current `main` behavior or the present defect. |
| 3 | `## Why This Matters` | no | Impact, motivation, or release value. |
| 4 | `## Representative Sites` | no | Concrete code locations (`file.cpp` functions). |
| 5 | `## Intended Shape` | no | Target design or candidate fix direction. |
| 6 | `## Scope Constraints` | no | In-scope, out-of-scope, and non-goals. |
| 7 | `## Acceptance Criteria` | yes | Checklist of concrete, verifiable outcomes. |
| 8 | `## Validation` | recommended | How the change will be proven (tests, builds, smoke). |
| 9 | `## Notes` | no | Dependencies, related items, and open questions. |

### Deprecated section names

Fold these older spellings into the canonical section above rather than adding
a new heading:

- Current State ← `Current Evidence`, `Current Mainline Evidence`,
  `Current Main Evidence`, `Current Behavior`.
- Why This Matters ← `Why Add It`, `Why Now`, `Motivation`, `Release Value`.
- Representative Sites ← `Files`, `Files To Modify`, `Exposure Points`,
  `Representative Live Sites`.
- Intended Shape ← `Intended Mainline Shape`, `Proposed Shape`,
  `Candidate Fix Direction`, `Intended Fix Direction`, `Proposed Direction`,
  `Intended Architecture`.
- Scope Constraints ← `Scope`, `Constraints`, `Non-Goals`, `Out Of Scope`,
  `Intended Scope`.
- Notes ← `Dependencies`, `Related Items`, `Open Questions`.

## Evidence And Journals

Item docs are current specs, not running logs.

- Keep the body focused on the durable spec: summary, scope, acceptance
  criteria, and current validation status.
- Do not accumulate dated journal sections (for example
  `## 2026-05-14 ... Reset`) inside an active item. A long proof or revalidation
  trail belongs in a linked evidence file under `docs/history/` per
  [Documentation Policy](../DOCS-POLICY.md); link to it from `## Validation` or
  `## Notes`.
- Keep tables browser-readable: two to four columns, with long evidence text in
  bullets below the table.
