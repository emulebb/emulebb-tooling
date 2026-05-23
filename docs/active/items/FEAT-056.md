---
id: FEAT-056
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/19
title: Post-beta-0.7.3 release proof automation and operator evidence UX
status: DEFERRED
priority: Minor
category: feature
labels: [post-beta-0.7.3, release-proof, automation, operator-evidence]
milestone: post-beta-0.7.3
created: 2026-05-09
source: FEAT-055 Beta 0.7.3 improvement triage
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/19. This local document is retained as an engineering spec/evidence record.

## Summary

Build the follow-up tooling and documentation improvements discovered while
hardening the beta `0.7.3` release proof. These are intentionally post-release improvements:
they improve future release velocity and operator evidence quality, but they do
not fix a confirmed Beta 0.7.3 regression or missing advertised behavior.

## Approved Workstream

| Improvement | Classification | Target |
|-------------|----------------|--------|
| one-command Beta 0.7.3 proof orchestration through `python -m emule_workspace` | next-patch | add a single command that runs validate, required builds, native tests, live smoke suites when configured, package rehearsals, and final summary collection |
| compact operator summary for live E2E artifacts | next-patch | emit a short JSON/Markdown summary with suite name, outcome, profile path, ports, app exit status, and inconclusive diagnostics |
| packaging manifest diff report against the previous release asset | next-patch | compare file list, hashes, docs, language DLLs, unsupported artifacts, and app/build commits against the previous tagged package |
| controller compatibility matrix for native REST, qBit, Torznab, Arr, and aMuTorrent consumers | beta-closeout slice | publish a maintained matrix tying controller workflows to API families and evidence artifacts |
| clearer release-note separation between stock parity, Broadband features, and intentionally frozen legacy areas | next-patch | split future release notes into parity, advertised Broadband/API behavior, packaging, and frozen/removal sections |
| automated changed-surface grouping for future release audits | future | convert the manual CI-022 grouping into a repeatable report generator |
| lightweight UI smoke coverage for representative language/resource loads | future | add selected language-load UI smoke beyond language DLL build/package proof |

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
      the runtime cost after Beta 0.7.3.

## Validation

- Future implementation must run through
  `python -m emule_workspace`.
- Any implemented slice should update this item with command output, artifact
  paths, and commit IDs.
