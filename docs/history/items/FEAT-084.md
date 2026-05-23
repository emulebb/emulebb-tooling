---
id: FEAT-084
title: Migration Wizard for legacy profile import
status: WONT_DO
priority: Minor
category: feature
labels: [migration, profile, config, emuleai, wont-do]
milestone: ~
created: 2026-05-24
source: eMuleAI migration wizard review
---

# FEAT-084 - Migration Wizard For Legacy Profile Import

## Decision

Record this eMuleAI feature as **WONT_DO** for eMuleBB.

The first eMuleBB release line should not add a wizard that copies or mutates
legacy profiles automatically. eMuleBB has strict `.met`/`.dat` compatibility
and backup policy, and profile import is a data-loss-sensitive workflow. A
wizard could be useful later, but it should not be part of the accepted future
backlog now.

## eMuleAI References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- wizard dialog:
  [`MigrationWizardDlg.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/MigrationWizardDlg.cpp#L84)
- browse/restore and config-dir import helpers:
  [`MigrationWizardDlg.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/MigrationWizardDlg.cpp#L240),
  [`MigrationWizardDlg.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/MigrationWizardDlg.cpp#L289),
  [`MigrationWizardDlg.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/MigrationWizardDlg.cpp#L489)
- startup integration:
  [`Emule.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/Emule.cpp#L855)

## Rationale

- Profile migration touches high-value data: downloads, known files, credits,
  server lists, Kad state, categories, and preferences.
- A wizard can obscure which files were copied, skipped, rewritten, or backed
  up.
- eMuleBB already documents `.met`/`.dat` file roles and backup behavior. Any
  future import tool should be a separate, heavily-tested operator workflow,
  not a startup wizard.

## Replacement Direction

Keep profile movement manual for now. If reopened, implement it as an external
dry-run-capable migration tool with explicit source/target paths, full backups,
and no automatic startup mutation.
