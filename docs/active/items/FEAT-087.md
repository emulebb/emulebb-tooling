---
id: FEAT-087
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/77
title: Add inline transfer speed sparklines
status: OPEN
priority: Minor
category: feature
labels: [ui, transfers, speed, visualization, performance]
milestone: post-0.7.3
created: 2026-05-25
source: operator request for a mini speed chart similar to the parts progress bar
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/77. This local document is retained as an engineering spec/evidence record.

## Summary

Add a compact inline speed chart for transfers, visually similar in density and
placement to the existing parts/progress bar UI.

The intended control is a small sparkline-style rendering inside the transfer
lists, not a full chart panel. It should help users see whether a transfer is
steady, bursting, stalled, or recovering without opening a separate details
view.

## Intended Shape

Start with a lightweight custom-drawn sparkline:

- store a small fixed-size speed history ring per active transfer row
- sample at the existing transfer refresh cadence
- draw only visible rows during normal list paint
- use per-row normalization for v1 so slow transfers still show movement
- keep axes, legends, and interaction out of the first version

Candidate placement:

- download list current-speed/status area, or a narrow optional speed-graph
  column
- upload list equivalent if the download-list version proves cheap enough

## Scope Constraints

- Do not add a separate chart window for this item.
- Do not repaint every transfer row continuously; rendering must stay tied to
  existing visible-row invalidation.
- Do not store long histories. The visual should use roughly 30-60 recent
  samples per row unless profiling supports a different bound.
- Do not block or slow transfer processing to maintain the visual history.

## Acceptance Criteria

- [ ] Visible download rows can show a compact recent-speed sparkline.
- [ ] The sparkline updates at the existing list refresh cadence without
      introducing measurable UI stutter on large transfer lists.
- [ ] The implementation keeps bounded per-row memory usage.
- [ ] Users who do not need the visual can hide it if implemented as a separate
      column.
- [ ] A seam or focused rendering-policy test covers history retention and
      scaling decisions without relying on a live MFC window.
