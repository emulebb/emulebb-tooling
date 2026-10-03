---
id: RUST-BUG-105
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/26
title: Disposition stock source-acquisition default drift
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, sources, scheduling, parity]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against eMule 0.72a and current aMule 3.1
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/26. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-105 - Disposition stock source-acquisition default drift

## Summary

Reconcile Rust's source limits with the actual stock eMule and current aMule
defaults, or explicitly approve and prove a named broadband policy. The current
coordinator defaults to 600 sources per file with a 1,000 soft cap and a 100
source UDP cap, while comments describe those values as oracle-compatible.
They do not match either reference client.

## Current State

- `crates/emulebb-core/src/download_coordinator.rs` uses default/soft/UDP values
  of 600/1,000/100 and describes them as inherited from the oracle.
- Stock eMule defines a 750 source soft limit and a 50 source UDP request cap;
  its preference default is 400 sources per file.
- Current aMule defines a 500 source soft limit and a 50 source UDP request cap;
  its preference default is 300 sources per file.
- The difference is not a packet-codec incompatibility, but it changes network
  load, server/Kad query pressure, connection churn, and high-source behavior.

## Why This Matters

Unacknowledged policy drift makes parity claims inaccurate and can amplify load
on shared ED2K infrastructure. A deliberate modern default may be reasonable,
but it needs a name, rationale, safety bounds, and evidence rather than a stale
compatibility comment.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-core\src\download_coordinator.rs`
- `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main\srchybrid\Opcodes.h`
- `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main\srchybrid\Preferences.cpp`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\include\protocol\ed2k\Constants.h`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\Preferences.cpp`

## Intended Shape

- Record a deliberate choice: align the default/caps to a named reference, or
  retain different values under an explicitly approved Rust broadband profile.
- Make comments and operator-facing settings state the selected policy and the
  difference between configured target, per-file soft limit, UDP packet cap,
  and global pacing.
- Keep all source acquisition subject to bounded server/Kad query pacing,
  connection limits, deduplication, and backoff.
- If a modern profile is retained, support a stock-conservative profile without
  hidden constants or incompatible persistence.

## Scope Constraints

- Do not infer that a higher per-file cap authorizes more aggressive global
  query or connection rates.
- Preserve wire-compatible UDP request sizing and packet bounds.
- Avoid changing defaults without a settings migration/release note where an
  existing user-visible value is affected.

## Acceptance Criteria

- [ ] Every source-limit constant and default has an accurate reference or an
      explicit product-policy rationale.
- [ ] The selected default profile is documented and exposed consistently in
      settings, runtime diagnostics, and configuration schema.
- [ ] UDP source requests respect the selected stock-compatible per-request cap.
- [ ] Per-file and global pacing remain bounded with 1, 100, and 1,000 active
      downloads and high-source-count fixtures.
- [ ] A migration or compatibility path covers persisted settings if defaults or
      meanings change.
- [ ] The disposition is reflected in the parity matrix/evidence rather than
      continuing to claim both incompatible references.

## Validation

- Unit tests for limit precedence, UDP batching, deduplication, and configured
  overrides at each boundary.
- Deterministic source-simulation tests for high file/source counts and global
  pacing.
- A bounded stock eMule/current-aMule server fixture comparing request batch
  sizes and reconnect/query rates under the selected profile.

## Notes

This item asks for an explicit compatibility/product decision. It does not
presuppose that the numerically lowest limit is always best.
