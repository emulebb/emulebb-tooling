---
id: FEAT-056
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/19
title: Post-0.7.3 release proof automation and operator evidence UX
status: DEFERRED
priority: Minor
category: feature
labels: [post-0.7.3, release-proof, automation, operator-evidence]
milestone: post-0.7.3
created: 2026-05-09
source: FEAT-055 0.7.3 RC1 improvement triage
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/19. This local document is retained as an engineering spec/evidence record.

## Summary

Build the follow-up tooling and documentation improvements discovered while
hardening the 0.7.3 RC1 release proof. These are intentionally post-release improvements:
they improve future release velocity and operator evidence quality, but they do
not fix a confirmed 0.7.3 RC1 regression or missing advertised behavior.

## Approved Workstream

### One-Command 0.7.3 RC1 Proof Orchestration

Classification:
`next-patch`.

Target:
add a single `python -m emule_workspace` command that runs validate, required
builds, native tests, configured live smoke suites, package rehearsals, and
final summary collection.

### Compact Operator Summary For Live E2E Artifacts

Classification:
`next-patch`.

Target:
emit a short JSON/Markdown summary with suite name, outcome, profile path,
ports, app exit status, and inconclusive diagnostics.

### Packaging Manifest Diff Report

Classification:
`next-patch`.

Target:
compare file list, hashes, docs, language DLLs, unsupported artifacts, and
app/build commits against the previous tagged release asset.

### Controller Compatibility Matrix

Classification:
`rc1-closeout slice`.

Target:
publish a maintained matrix tying native REST, qBit, Torznab, Arr, and
aMuTorrent workflows to API families and evidence artifacts.

### Release-Note Separation

Classification:
`next-patch`.

Target:
split future release notes into stock parity, advertised Broadband/API
behavior, packaging, and frozen/removal sections.

### Changed-Surface Grouping

Classification:
`future`.

Target:
convert the manual CI-022 grouping into a repeatable report generator.

### Language/Resource UI Smoke

Classification:
`future`.

Target:
add selected language-load UI smoke beyond language DLL build/package proof if
it remains worth the runtime cost after 0.7.3 RC1.

## Acceptance Criteria

- [ ] `python -m emule_workspace` exposes a documented proof-orchestration command.
- [ ] Live E2E artifact summaries are generated in a stable machine-readable
      and operator-readable shape.
- [ ] Release packages can be diffed against a previous release package and
      manifest.
- [x] Controller compatibility matrix is linked from active release docs.
- [ ] Future release notes use separate sections for stock parity, Broadband
      features, packaging, and frozen legacy decisions.
- [ ] Changed-surface grouping is reproducible from a command or script.
- [ ] Representative language/resource UI smoke is added if it remains worth
      the runtime cost after 0.7.3 RC1.

## Validation

- Future implementation must run through
  `python -m emule_workspace`.
- Any implemented slice should update this item with command output, artifact
  paths, and commit IDs.
