---
id: FEAT-037
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/63
title: Release-oriented sharing controls — PowerShare, Release Bonus, and Share Only The Need
status: DEFERRED
priority: Minor
category: feature
labels: [sharing, release, powershare, upload, queue, rarity, mods]
milestone: ~
created: 2026-04-20
source: MorphXT FAQ; Mephisto FAQ; historical eMule feature catalogs; eMuleAI v1.4 notes
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/63. This local document is retained as an engineering spec/evidence record.

# FEAT-037 - Release-oriented sharing controls — PowerShare, Release Bonus, and Share Only The Need

## Summary

Add an explicit release/distribution policy layer for rare or newly published files.

## 0.7.3 RC1 Classification

**Deferred Beyond 1.0.** Product decision: PowerShare and adjacent
release-oriented sharing controls are not valuable enough to delay the first
release. eMuleBB already has broadband upload-slot control and queue/scoring
work for the 1.0 sharing story; this item stays as a later opt-in feature track.

This feature groups several historically popular mod behaviors under one controlled design:

- `PowerShare`
- release bonus / release-priority queue behavior
- `Share Only The Need` or similar rarity-aware distribution controls
- eMuleAI v1.4 style `Hide Overshares` and default share-permission controls

## Why Add It

This is one of the clearest examples of "beyond stock" eMule behavior that users of older
mods actively valued. Historical MorphXT/Mephisto/Pawcio feature catalogs consistently put
release-focused sharing policy near the center of their differentiation.

For an archival/community-sharing branch, this can be more valuable than another general UI
tweak.

## Intended Mainline Shape

- per-file and/or category-level release sharing mode
- optional PowerShare policy that prioritizes serving a chosen file regardless of normal
  queue dynamics
- optional release bonus or focused upload treatment for selected files
- rarity-aware controls that prefer scarce parts/files over overserved ones
- optional overshare hiding and default share-permission policy
- guardrails so these policies cannot silently starve the rest of the upload ecosystem

## Scope Constraints

- integrate with the current broadband upload controller instead of replacing it
- keep the feature opt-in and explicit
- favor a smaller modernized control surface over porting every legacy mod knob
- coordinate with anti-abuse logic so aggressive release settings do not become a leecher
  fingerprint

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- v1.4 Share Tweaks release-note entry:
  [`Release_Notes.txt`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/Release_Notes.txt#L6)
- per-file share-policy fields:
  [`KnownFile.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/KnownFile.h#L145)
- known-file share-policy behavior:
  [`KnownFile.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/KnownFile.cpp#L1986)
- Share Tweaks options surface:
  [`PPgMod.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/PPgMod.cpp#L695)

## eMuleBB Direction

Keep this deferred. If reopened, implement a narrow per-file release mode with
visible queue effects instead of importing a broad mod-style matrix of
PowerShare, Share Only The Need, Hide Overshares, and default share-permission
rules. The core risk is fairness drift: a release helper should not silently
starve ordinary shared files or make eMuleBB look abusive to stock peers.

## Acceptance Criteria

- [ ] a file can be marked for release-oriented sharing policy
- [ ] upload queue behavior measurably favors the selected release file(s)
- [ ] scarcity-aware distribution can prefer under-served parts or files
- [ ] normal uploads remain bounded and not permanently starved
- [ ] operators can disable the entire feature globally
- [ ] queue-impact diagnostics show exactly how release policy affected upload
      selection
