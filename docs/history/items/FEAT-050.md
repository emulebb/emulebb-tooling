---
id: FEAT-050
title: Launch external program on completed download
status: Passed
priority: Minor
category: feature
labels: [downloads, completion, automation, preferences]
milestone: broadband-release
created: 2026-05-02
source: qBittorrent-style completion command planning
---

## Summary

Add an opt-in qBittorrent-style completion hook that launches one configured
external executable after a download is fully completed and retained as the
live known/shared file.

## Beta 0.7.3 Classification

**Release Gate.** This is the one optional workflow feature promoted into 1.0
in addition to the REST/controller gate. It must stay disabled by default,
executable-only, asynchronous, and covered by targeted native tests so it adds
automation value without creating a shell-execution surface.

## Execution Plan

Covered by the
[Beta 0.7.3 Download Completion Hook execution plan](../../history/release-0.7.3/RELEASE-0.7.3-DOWNLOAD-COMPLETION-HOOK-EXECUTION-PLAN.md).

## Acceptance Criteria

- [x] command does not run for failed completion or duplicate-discard paths
- [x] command runs after final UI-thread completion success and notifier/log
      work
- [x] missing executable is rejected when enabling the feature
- [x] disabled preference allows empty command fields
- [x] token expansion is covered by native tests
- [x] launch helper closes process and thread handles immediately
- [x] app validation and targeted tests pass

## Completion Evidence

- app: `b6ce2ef`, `1db8f7c`
- tests: `ea9f163`
- command: `python -m emule_workspace build tests --config Debug --platform x64`
- command: `python -m emule_workspace test all --config Debug --platform x64`
- build logs: `workspaces\v0.72a\state\build-logs\20260506-201517`
- native coverage: `repos\emulebb-build-tests\reports\native-coverage\20260506-201526-eMulebb-workspace-v0.72a-eMule-main-x64-Debug`
- result: native tests passed `483/483` cases and `2686/2686` assertions
