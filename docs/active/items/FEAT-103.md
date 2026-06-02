---
id: FEAT-103
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/117
title: Publish Windows Hyper-V run guide for eMuleBB
status: OPEN
priority: Minor
category: feature
labels: [docs, hyper-v, windows-vm, onboarding, package-smoke, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-02
source: operator request to make the local Hyper-V eMuleBB run path visible to users
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/117. This local document is retained as an engineering spec/evidence record.

# FEAT-103 - Publish Windows Hyper-V Run Guide For eMuleBB

## Summary

Publish a user-facing guide for running eMuleBB inside a local Windows Hyper-V
guest using the existing workspace VM lab automation. The guide should make the
path approachable for users and contributors who want a clean, repeatable
Windows test environment without paying for cloud nested virtualization.

The guide should describe the automation as mostly headless VM orchestration:
the host prepares, boots, tests, checkpoints, and restores the guest from
commands. It must not describe eMuleBB itself as a headless daemon.

## Intended Shape

- Add a current reference guide under `docs/reference/`.
- Explain host prerequisites:
  - Windows Pro, Enterprise, or Server with Hyper-V support
  - elevated PowerShell for VM preparation and test execution
  - enough local RAM, disk, and CPU for at least one Windows guest
- Tell users to provide their own legal Windows ISO.
- Point users from `vm-lab.example.json` to an ignored `vm-lab.local.json`.
- Show the supported orchestration commands:
  - `python -m emule_workspace vm-lab prepare --matrix win11`
  - `python -m emule_workspace test windows-vm --matrix win11 --profile package-smoke`
- Explain the clean-checkpoint workflow: build once, restore often.
- Keep the guide clear that first image preparation is slow, while repeat runs
  are intended to be cheap and mostly unattended.

## Scope Constraints

- Do not bundle, mirror, or link to unauthorized Windows ISO images.
- Do not add a product promise that eMuleBB is daemon-only or headless.
- Do not require public-network live tests in the introductory path.
- Do not make cloud nested virtualization the default recommendation.
- Do not hardcode machine-specific absolute paths in the guide.

## Candidate Implementation Notes

- Place the canonical guide at `docs/reference/GUIDE-HYPERV-WINDOWS.md`.
- Link the guide from the active docs index or another appropriate current
  navigation point.
- Add a short pointer from the build repo README only if it does not duplicate
  the canonical guide.
- Include troubleshooting for missing Hyper-V commands, non-elevated shells,
  Windows Home hosts, ISO edition mismatches, and failed checkpoint restores.
- Prefer `win11` as the first example matrix and mention `win10` only where the
  local config supports it.

## Acceptance Criteria

- [ ] A current reference guide documents local Hyper-V setup for eMuleBB.
- [ ] The guide clearly states that users must supply their own Windows ISO.
- [ ] The guide uses supported `python -m emule_workspace` commands.
- [ ] The guide distinguishes headless VM automation from a headless eMuleBB
      runtime.
- [ ] The guide explains clean checkpoints and repeatable package smoke runs.
- [ ] The guide includes practical troubleshooting for common host and ISO
      failures.
- [ ] Current documentation checks pass after the guide is added.

## Validation

- `python scripts\docs-item-taxonomy-check.py`
- `python scripts\docs-structure-check.py`
- manual read-through of the guide from a clean-user perspective
