---
id: RUST-CI-006
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/31
title: Refresh current-head stock parity evidence and reconcile docs
status: OPEN
priority: Major
category: ci
labels: [rust, ed2k, kad, parity, evidence, documentation]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review and retained parity evidence audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/31. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-006 - Refresh current-head stock parity evidence and reconcile docs

## Summary

After the compatibility findings in this review are dispositioned, run one
authoritative stock eMule/current-aMule/Rust campaign from a clean immutable
Rust head and reconcile the durable documentation to that evidence. The
existing broad parity campaign is tied to an older Rust revision, while later
targeted witnesses do not collectively replace a same-head full campaign and
one active soak document still contradicts later upload evidence.

## Current State

- Archived `RUST-CI-002` records the authoritative parity campaign against Rust
  revision `3a162136` and later targeted reconciliation evidence.
- The current Rust branch has advanced materially beyond that revision.
- Large-library, live, and targeted peer witnesses exist for later changes, but
  no single retained campaign reruns the complete stock/MFC/current-aMule matrix
  at the current immutable head.
- `RUST-SOAK-UPLOAD-DOWNLOAD-GAP-ANALYSIS.md` still describes upload admission as
  open, while later `RUST-CI-002` peer evidence records that path as passing.

## Why This Matters

Parity claims are only auditable when code revision, fixtures, clients, policy
omissions, results, and documentation agree. Stale green evidence can conceal a
regression; stale red prose can equally misrepresent completed behavior.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust\history\items\RUST-CI-002.md`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust\active\RUST-SOAK-UPLOAD-DOWNLOAD-GAP-ANALYSIS.md`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust\RELEASE-SCOPE.md`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\policy\rust-client-omissions.toml`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests`

## Intended Shape

- Select a clean immutable Rust commit only after the blocking compatibility
  items are fixed, explicitly accepted, or scoped with a policy disposition.
- Use the policy quickstart and persisted Python launchers in
  `emulebb-build-tests`; record Windows-to-WSL path/target translation when a
  WSL lane is used.
- Run the full deterministic server, peer-transfer, Kad, REST, VPN, and required
  live/soak matrix against the same revision and recorded reference-client
  builds.
- Publish one manifest mapping every claim to a result artifact, disposition,
  omission, or explicitly non-blocking observation.
- Reconcile active, release-scope, and archived summary prose so no superseded
  claim remains presented as current.

## Scope Constraints

- Do not mix results from unrecorded Rust commits into one claimed campaign.
- Excluded protocol capabilities remain exclusions; this item does not silently
  expand or shrink the frozen omissions registry.
- Public-network checks stay bounded, gentle, and secondary to deterministic
  fixtures.
- Store reports only below `EMULEBB_WORKSPACE_OUTPUT_ROOT`; commit summaries and
  stable references, not bulky/private run artifacts.

## Acceptance Criteria

- [ ] One clean immutable Rust revision is recorded with stock eMule and current
      aMule build identities, configuration, fixture versions, and environment.
- [ ] The full required ED2K server, peer transfer, Kad, REST, VPN, and soak/live
      matrix is rerun or has a documented, approved non-applicability reason.
- [ ] Every RUST-BUG-102..105 and RUST-CI-005 disposition is exercised by a
      deterministic or interop witness appropriate to its risk.
- [ ] The omissions registry and frozen parity matrix match the evidence with no
      hidden proprietary/default divergence.
- [ ] Active and release documentation contains no contradiction such as the
      stale upload-admission statement.
- [ ] The evidence manifest is reproducible through maintained Python entry
      points and passes cleanup/secret/privacy checks.

## Validation

- Execute the maintained `emulebb-build-tests` parity/soak entry points described
  by the workspace policy; do not substitute ad-hoc launch logic.
- Run repository tests and documentation/link/taxonomy/roadmap checks at the
  recorded commits.
- Manually audit the final manifest against every current parity-matrix row,
  omission, open compatibility item, and summary claim.

## Notes

This is a final evidence/reconciliation gate, not a substitute for fixing the
individual findings. Existing packed-stream bounds, malformed hashset handling,
compressed-part caps, and AICH trust coverage should remain explicit regression
checks in the refreshed campaign.
