---
id: FEAT-106
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/120
title: Add upload bandwidth ramp-up diagnostics and slot policy
status: OPEN
priority: Major
category: feature
labels: [uploads, bandwidth, slots, diagnostics, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-02
source: operator request to maximize upload bandwidth fill rate
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/120. This local document is retained as an engineering spec/evidence record.

# FEAT-106 - Add Upload Bandwidth Ramp-Up Diagnostics And Slot Policy

## Summary

Add an explicit upload ramp-up policy for periods where configured upload
bandwidth is not being filled even though eligible queued clients exist.

Publishing creates demand, but upload bandwidth utilization is ultimately
controlled by active slot admission, replacement, slow-client handling, and
throttler behavior. This item tracks making that state observable and safely
opening or replacing slots faster during underfilled periods.

## Intended Shape

- Detect a bounded ramp-up mode when upload bandwidth stays below target for a
  short interval while eligible queued clients exist.
- Open upload slots faster during ramp-up, within existing hard safety limits.
- Permit a small number of temporary extra slots only when they improve actual
  throughput and can be reclaimed predictably.
- Replace disconnected, stalled, or persistently slow upload slots faster while
  ramp-up is active.
- Prefer clients requesting files with proven demand without bypassing user
  priority, friend-slot, ban, credit, or abuse controls.
- Exit ramp-up once upload bandwidth and slot utilization are healthy.

## Scope Constraints

- Do not remove existing broadband upload caps or user-configured limits.
- Do not weaken client bans, credit checks, friend-slot semantics, or slow-slot
  cooldown safety.
- Do not create permanent extra slots; ramp-up slots must be explicitly
  temporary and reclaimable.
- Do not change Kad/eD2K protocol behavior.
- Do not make upload-list UI rows drive scheduling decisions.

## Candidate Implementation Notes

- Review `CUploadQueue` slot opening, slow-upload recycling, and throttler
  interaction as one focused slice.
- Add counters for ramp-up state, slot-open attempts, temporary slots, replaced
  slow slots, and reclaimed temporary slots.
- Keep the first implementation conservative and observable before tuning
  thresholds.
- Use live logs to distinguish "no demand" from "demand exists but slots are
  not filling bandwidth".

## Implementation Notes

- 2026-06-04: A focused underfill slice shortened stalled zero-rate upload slot
  replacement for peers with queued local upload data but no network progress.
  The change keeps friend slots and pending disk I/O protected, preserves the
  configured slot cap, and leaves Kad/eD2K wire behavior unchanged.
- 2026-06-04: The upload bandwidth throttler's control-queue removal, merge,
  pop, and shutdown cleanup paths were routed through the existing tested seam
  helpers so the hot-path queue mechanics stay covered by native tests.

## Evidence

- 2026-06-04: `python -m emule_workspace test native --test-run-variant main
  --suite-name parity --config Release --platform x64 --build-output-mode
  ErrorsOnly` passed: 806 test cases, 5055 assertions.
- 2026-06-04: `python -m emule_workspace build app --variant main --config
  Debug --platform x64 --build-output-mode ErrorsOnly` passed.
- 2026-06-04: `python -m emule_workspace build app --variant main --config
  Release --platform x64 --build-output-mode ErrorsOnly` passed.
- 2026-06-04: Fresh Release x64 process launched with
  `-c $env:EMULEBB_LOCAL_TEST_PROFILE_PATH`; startup reached VPN Guard success and shared
  hash progress with no startup-error log output observed.

## Acceptance Criteria

- [ ] Upload underfill with eligible queued clients enters ramp-up mode after a
      bounded delay.
- [ ] Ramp-up opens or replaces slots faster without exceeding hard limits.
- [ ] Temporary slots, if used, are visibly counted and reclaimed.
- [ ] Slow or stalled active slots can be replaced faster while under target.
- [ ] User limits, bans, friend slots, credits, and existing hard caps remain
      respected.
- [ ] Logs or counters explain why ramp-up did or did not open another slot.

## Validation

- focused native tests for ramp-up state transitions
- focused upload queue tests for temporary-slot admission and reclamation
- live upload smoke with mixed fast and slow clients
- x64 Debug and Release app builds before implementation commit
