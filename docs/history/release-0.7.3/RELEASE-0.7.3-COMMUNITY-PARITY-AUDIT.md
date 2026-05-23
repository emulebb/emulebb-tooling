# Beta 0.7.3 Community Parity Audit Plan

> Historical release plan only. Current beta `0.7.3` execution is controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

This plan turns the broad `release/v0.72a-community...main` app delta into an
actionable Beta 0.7.3 hardening backlog. It is documentation-first: each code or
test change discovered by this audit must be implemented later as its own
granular item commit.

## Audit Inputs

- Stock/community baseline: `release/v0.72a-community`
- Candidate app line: `EMULE_WORKSPACE_ROOT\workspaces\v0.72a\app\eMule-main`
  on `main`
- Previous internal evidence tag: `emule-bb-v1.0.0`
- Active release control: [RELEASE-0.7.3](../../active/RELEASE-0.7.3.md)
- Detailed current review:
  [REVIEW-2026-05-09-release-0.7.3-community-parity](../reviews/REVIEW-2026-05-09-release-0.7.3-community-parity.md)
- Changed-surface ledger:
  [REVIEW-2026-05-09-release-0.7.3-changed-surface-ledger](../reviews/REVIEW-2026-05-09-release-0.7.3-changed-surface-ledger.md)

## Execution Workflow

1. Refresh repository state.
   - Check `git status --short --branch` in `repos\emulebb-tooling`,
     `repos\emulebb-build`, `repos\emulebb-build-tests`, and the active app
     worktree.
   - Confirm the app candidate is on `main` and the baseline branch exists.

2. Rebuild the changed-surface ledger.
   - Run `git diff --name-status release/v0.72a-community...main`.
   - Exclude generated Visual Studio user/filter churn unless it carries a
     release-relevant build change.
   - Assign each changed file to exactly one release audit area in
     [CI-022](../items/CI-022.md).

3. Reconcile post-1.0 hardening.
   - Run `git log --oneline emule-bb-v1.0.0..main`.
   - Map BUG-102 through BUG-110 commits to test evidence, release area, and
     follow-up risk in [CI-023](../items/CI-023.md).
   - Create missing bug items only when a fix lacks acceptance or replay
     evidence.

4. Run gate-by-gate proof.
   - Controller and adapter proof: [CI-024](../items/CI-024.md) and
     [CI-025](../items/CI-025.md).
   - Shared-file, download, persistence, search, networking, UI, and packaging
     proof: [CI-026](../items/CI-026.md) through
     [CI-031](../items/CI-031.md).
   - Legacy disposition: [REF-037](../items/REF-037.md).

5. Promote findings.
   - A release-blocking product defect becomes the next `BUG-111+` item.
   - Missing or weak automation stays in `CI-022+`.
   - Intentional cleanup or compatibility-preserving refactor work becomes
     `REF-038+`.
   - Non-blocking improvements go to [FEAT-055](../items/FEAT-055.md) or later
     feature items.

6. Close release.
   - Update [RELEASE-0.7.3](../../active/RELEASE-0.7.3.md) gate statuses only when each
     item contains passing evidence.
   - Update [INDEX](../../active/INDEX.md) counts and status tables after every item
     status change.
   - Tag only after all Beta 0.7.3 release gates are Done or explicitly Wont-Fix
     by product decision.

## Area Matrix

| Area | Primary item | Required proof |
|------|--------------|----------------|
| Changed-surface inventory | [CI-022](../items/CI-022.md) | Every app diff path has owner, risk, evidence lane, and item disposition. |
| Post-tag hardening | [CI-023](../items/CI-023.md) | BUG-102..BUG-110 focused tests and validation are replayed. |
| Arr and aMuTorrent | [CI-024](../items/CI-024.md) | Prowlarr, Radarr, Sonarr, and aMuTorrent live artifacts pass or are valid inconclusive. |
| REST/qBit/Torznab | [CI-025](../items/CI-025.md) | Contract manifests, adapter quirks, auth, errors, and destructive routes are replayed. |
| Shared files/startup/cache/long paths | [CI-026](../items/CI-026.md) | 50k tree, watcher churn, cache restart, long-path, and shared-file REST probes pass. |
| Downloads/persistence | [CI-027](../items/CI-027.md) | Part-file, known/server/Kad metadata, direct-download, completion hook, and restart probes pass. |
| Search/server/Kad | [CI-028](../items/CI-028.md) | Search lifecycle, server import, Kad bootstrap, source exchange, and close/cleanup flows pass. |
| Network adversity | [CI-029](../items/CI-029.md) | Bind, UPnP, TCP/UDP, WebSocket, HTTPS, and resource-churn checks pass. |
| UI/preferences/languages | [CI-030](../items/CI-030.md) | Main-window smoke, list controls, preferences, tray, keyboard, resources, and representative language DLLs pass. |
| Packaging/release assets | [CI-031](../items/CI-031.md) | x64/ARM64 packages contain expected binaries, manifests, docs, templates, and data files. |
| Legacy/frozen features | [REF-037](../items/REF-037.md) | Each removed/frozen stock feature is explicitly dispositioned. |
| Improvements | [FEAT-055](../items/FEAT-055.md) | Improvement ideas are ranked without expanding the Beta 0.7.3 blocking scope. |

## Evidence Rules

- Prefer existing supported harnesses before adding new automation.
- If behavior changed, compare against `release/v0.72a-community` when a
  meaningful parity lane exists.
- If a community feature was intentionally removed or frozen, record the
  product decision in [REF-037](../items/REF-037.md).
- Do not mark a gate Done from a passing build alone; each gate needs behavior
  evidence for its changed area.
- Do not mix app fixes, test hardening, and docs-status updates in one commit
  unless the change is inseparable.
