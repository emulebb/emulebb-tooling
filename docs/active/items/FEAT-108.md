---
id: FEAT-108
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/122
title: Add publish effectiveness feedback for shared files
status: OPEN
priority: Minor
category: feature
labels: [shared-files, publishing, uploads, bandwidth, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-02
source: operator request to make shared-file publishing fill upload demand faster
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/122. This local document is retained as an engineering spec/evidence record.

# FEAT-108 - Add publish effectiveness feedback for shared files

## Summary

Track whether recent ED2K/Kad publishing actually produces upload requests and
use that feedback to tune future publish selection.

The current balanced publish ranking uses local demand, request history,
under-served ratio, publish age, and deterministic jitter. This item adds the
next feedback loop: avoid repeatedly spending publish slots on files that do
not attract requests, while preserving fairness and user priority.

## Intended Shape

- Track a lightweight per-file publish effectiveness signal.
- Boost files whose recent publish activity led to upload requests.
- Cool down files that were published repeatedly without attracting requests.
- Keep under-served and newly visible files in rotation so they are not
  permanently hidden by already-popular files.
- Expose enough diagnostics to explain why a file was boosted or cooled down.

## Scope Constraints

- Do not increase Kad keyword store caps or ED2K server publish caps by default.
- Do not make request feedback the only ranking signal.
- Do not starve low-ratio, manually high-priority, or rarely published files.
- Do not persist high-churn telemetry unless a durable format is deliberately
  designed.

## Candidate Implementation Notes

- Start with session-local counters tied to publish timestamps and subsequent
  upload request increments.
- Prefer bounded decay windows over unbounded history.
- Keep the scoring contribution small at first so this remains a tuning input,
  not a policy rewrite.
- Log aggregate effectiveness rather than per-tick per-file chatter.

## Acceptance Criteria

- [ ] Recent publish-to-request effectiveness is tracked per shared file or
      equivalent session-local key.
- [ ] Balanced publish ranking can boost files that produce requests.
- [ ] Files repeatedly published without demand receive a bounded cooldown.
- [ ] User priority and under-served fairness still influence selection.
- [ ] Diagnostics explain publish effectiveness decisions at a useful level.

## Validation

- focused native tests for effectiveness scoring and cooldown decay
- live publish smoke with popular, rare, and no-demand files
- x64 Debug and Release app builds before implementation commit
