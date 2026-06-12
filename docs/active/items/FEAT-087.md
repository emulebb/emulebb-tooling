---
id: FEAT-087
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/77
title: Add transfer minicharts and aggregate progress metrics
status: OPEN
priority: Minor
category: feature
labels: [ui, transfers, speed, progress, ratio, visualization, performance]
milestone: post-0.7.3
created: 2026-05-25
source: operator requests for transfer minicharts and total progress/ratio
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/77. This local document is retained as an engineering spec/evidence record.

# FEAT-087 - Add transfer minicharts and aggregate progress metrics

## Summary

Add compact transfer minicharts plus aggregate transfer-progress metrics,
visually similar in density to the existing parts/progress bar UI.

The intended controls are small, sparkline-style renderings and concise
aggregate totals, not a full chart panel. They should help users see whether
transfers are steady, bursting, stalled, or recovering, and answer the basic
whole-session questions: how far the visible transfer set has progressed and
what its total ratio is.

## Intended Shape

Start with a lightweight custom-drawn sparkline:

- store a small fixed-size speed history ring per active transfer row
- sample at the existing transfer refresh cadence
- draw only visible rows during normal list paint
- use per-row normalization for v1 so slow transfers still show movement
- keep axes, legends, and interaction out of the first version

Candidate minichart placement is deliberately TBD until implementation
prototyping:

- toolbar/status area summary chart for the current transfer view
- per-row download list current-speed/status area, or a narrow optional
  speed-graph column
- upload list equivalent if the download-list version proves cheap enough

Add aggregate metrics in the same UX pass:

- total progress for the current transfer view, based on completed bytes over
  total bytes for the included transfers
- total ratio for the current transfer view, based on aggregate uploaded bytes
  over aggregate downloaded bytes where the underlying counters are available
- clear labeling for whether totals cover all transfers, the active category,
  the current filtered view, or only selected rows

## Scope Constraints

- Do not add a separate chart window for this item.
- Do not repaint every transfer row continuously; rendering must stay tied to
  existing visible-row invalidation.
- Do not store long histories. The visual should use roughly 30-60 recent
  samples per row unless profiling supports a different bound.
- Do not block or slow transfer processing to maintain the visual history.
- Do not make aggregate progress or ratio calculations mutate transfer,
  category, upload, download, credit, or statistics state.
- Do not invent new ratio semantics that conflict with existing upload/download
  counters; if the current counters are ambiguous, document the chosen numerator
  and denominator before exposing the metric.
- Do not force both toolbar and per-row chart placement in the first slice; pick
  the cheapest placement that gives useful feedback and leaves room for the
  other placement later.

## Acceptance Criteria

- [ ] The Transfers/Downloads surface exposes compact minichart feedback either
      in the toolbar/status area or in visible transfer rows.
- [ ] The sparkline updates at the existing list refresh cadence without
      introducing measurable UI stutter on large transfer lists.
- [ ] The implementation keeps bounded per-row memory usage.
- [ ] Users who do not need the visual can hide it if implemented as a separate
      column.
- [ ] The same surface shows total progress for the scoped transfer set.
- [ ] The same surface shows total ratio for the scoped transfer set when
      aggregate upload/download counters are available.
- [ ] Aggregate metric labels make the scope clear: all transfers, active
      category, current filtered view, or selection.
- [ ] Total progress and ratio calculations are display-only and do not affect
      queue, upload, download, credit, or category behavior.
- [ ] A seam or focused rendering-policy test covers history retention and
      scaling decisions without relying on a live MFC window.
