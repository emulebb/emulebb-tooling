---
id: FEAT-100
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/107
title: Improve startup progress and UI readiness locking
status: OPEN
priority: Major
category: feature
labels: [startup, ui, responsiveness, lifecycle, locking, progress, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-31
source: operator request after reviewing startup progress dialog and UI locking behavior
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/107. This local document is retained as an engineering spec/evidence record.

# FEAT-100 - Improve Startup Progress And UI Readiness Locking

## Summary

Make startup progress and startup-time UI locking coherent. The current app has
early and main-window startup progress dialogs, but repainting depends on broad
message pumping while the app is only partially initialized. That keeps the
dialog visible, but it can also dispatch normal commands, timers, or UI work
before the shell, services, network, and shared-file state are fully ready.

This item owns the broader lifecycle safety and UX pass. Existing narrower
items remain the owners for specific heavy startup paths:

- [FEAT-072](FEAT-072.md): startup cache and shared-library startup blocking
- [FEAT-075](FEAT-075.md): daily config backup progress responsiveness
- [FEAT-034](FEAT-034.md): shared-files reload and scan responsiveness

## Current Evidence

- `CLifecycleProgressDlg` is shared by startup and shutdown progress.
- `PumpLifecycleProgressMessages` currently peeks and dispatches all queued
  messages, with only dialog-message handling special-cased.
- Early startup progress is shown before preferences and core services finish
  initialization.
- Main-window startup progress is shown while the modal main dialog is created
  and while `UM_STARTUP_NEXT_STAGE` advances startup phases.
- Several startup phases still contain blocking I/O or large in-memory work,
  especially daily config backup and shared startup cache/load/scan paths.

## Intended Shape

1. Add a lifecycle progress controller.
   - Own startup and shutdown progress phase state in one place.
   - Preserve monotonic percent updates.
   - Rate-limit repaint/pump work.
   - Track elapsed time and last visible progress update for diagnostics.
   - Keep early startup and main-window startup transitions explicit.

2. Restrict lifecycle message pumping.
   - Replace broad `PeekMessage` dispatch during lifecycle progress with a
     narrow pump for paint/dialog/lifecycle-safe messages.
   - Do not let arbitrary commands, normal timers, hotkeys, tray actions, or
     mutating REST work run while startup is incomplete.
   - Keep shutdown pumping similarly constrained so teardown cannot reenter
     normal app workflows.

3. Add a startup readiness gate.
   - Define explicit startup readiness states such as shell creating, UI
     created, services starting, network starting, and startup complete.
   - Centralize command availability for toolbar buttons, menus, tray commands,
     hotkeys, and mutating REST commands.
   - Make disabled/blocked commands explainable in logs or diagnostics where
     appropriate.

4. Add progress callbacks for known blocking paths.
   - Start with daily config backup callbacks from FEAT-075.
   - Add rate-limited progress reports for shared startup cache and scan loops
     under FEAT-072.
   - Keep callbacks side-effect-light and testable; they should update
     lifecycle progress only, not advance normal app work.

5. Improve the visible dialog after the safety model is clear.
   - Consider a dedicated startup progress dialog resource instead of reusing
     the shutdown progress resource.
   - Use stable text areas for header, phase, detail, and optional elapsed time.
   - Use marquee mode for unknown-duration I/O and determinate mode for known
     phase progress.
   - Avoid a cancel button unless there is a real safe abort contract.

## Scope Constraints

- Do not change eD2K/Kad protocol behavior or startup network defaults.
- Do not dispatch normal app commands from lifecycle progress pumping.
- Do not mutate MFC UI, shared-file owner state, or network state from worker
  threads.
- Do not make daily config backup asynchronous in the first slice; keep its
  early snapshot ordering until a separate worker-backed plan proves safe.
- Do not treat visual polish as complete while broad lifecycle message pumping
  remains unsafe.

## Acceptance Criteria

- [ ] Startup and shutdown progress use a shared lifecycle progress controller.
- [ ] Lifecycle message pumping is restricted to approved paint/dialog/lifecycle
      messages.
- [ ] Toolbar, menu, tray, hotkey, and mutating REST commands respect centralized
      startup readiness state.
- [ ] Startup progress remains repaintable during daily config backup and large
      shared startup cache/load/scan work.
- [ ] Progress diagnostics expose stale progress updates or long unpumped
      startup phases.
- [ ] Native tests cover lifecycle pump filtering, readiness gate decisions,
      monotonic progress updates, and progress callback cadence.
- [ ] Startup profiling or live evidence shows no broad command/timer reentry
      during startup progress pumping.

## Validation

- `python -m emule_workspace validate`
- focused native tests for lifecycle progress controller and readiness gates
- focused native tests for backup/cache progress callback cadence
- x64 Debug and Release app builds before implementation commit
