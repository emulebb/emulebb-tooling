# Beta Readiness Review: Stability

> Historical snapshot: this audit preserves the 2026-05-11 findings. Current
> beta 0.7.3 release source and pending execution status are controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

## Executive Summary

Release blocker. The active candidate is no longer the candidate proven by the recorded 0.7.3 package rehearsal: current `eMule-main` is `df1191e`, while the recorded 0.7.3 package manifests were produced from app commit `74e5c76`. The intervening commits touch runtime REST and adapter paths, so the beta tag should remain held until the minimum proof and package rehearsal are rerun on current heads. I also found a high-risk UPnP/NAT traversal lifetime path where PCP/NAT-PMP discovery can outlive its owner after a timeout and where thread-launch failure can crash instead of failing closed.

## Review Checklist

- [x] Read `AGENTS.md`.
- [x] Read `repos/eMule-tooling/docs/WORKSPACE-POLICY.md`.
- [x] Checked `git status --short --branch` before drawing conclusions for `workspaces/v0.72a/app/eMule-main`: clean `main...origin/main`.
- [x] Checked `git status --short --branch` for `workspaces/v0.72a/app/eMule-v0.72a-community`: clean `release/v0.72a-community`.
- [x] Checked `git status --short --branch` for `repos/eMule-build`: clean `main...origin/main`.
- [x] Checked `git status --short --branch` for `repos/eMule-tooling`: clean `main...origin/main`.
- [x] Checked `git status --short --branch` for `repos/eMule-build-tests`: `main...origin/main` with pre-existing modified and untracked live-test files; treated as prior work.
- [x] Reviewed current release/version naming against beta target `0.7.3`.
- [x] Compared current heads with recorded 0.7.3 proof commits.
- [x] Reviewed startup/shutdown and NAT traversal code paths for concrete runtime stability risk.
- [ ] Rerun minimum beta proof on current heads before tagging.
- [ ] Add targeted UPnP/PCP/NAT-PMP launch-failure and shutdown-timeout validation.

## Findings

### Release blocker: Current main is ahead of recorded 0.7.3 release proof

Severity: Release blocker

Affected area: Release gating, runtime REST/adapter surface, package provenance.

Evidence:

- Current app candidate is `workspaces/v0.72a/app/eMule-main` commit `df1191e` (`CI-014 harden peer friend REST response`).
- Current build orchestration is `repos/eMule-build` commit `7d81b07`; current tooling is `repos/eMule-tooling` commit `d3b0cba`.
- `docs/active/RELEASE-0.7.3.md` records the current 0.7.3 package rehearsal at app commit `74e5c76`, build commit `0ead21a`, and tooling commit `2d904c3`.
- `docs/active/RELEASE-0.7.3.md` also states that tagging is held until the remaining minimum beta proof is complete.
- `docs/active/items/CI-033.md` records the final proof against superseded internal `1.0.1` artifacts at app commit `11e5966`, not current `df1191e`.
- `git diff --stat 74e5c76..HEAD -- srchybrid` in `eMule-main` shows 11 runtime files changed after the recorded 0.7.3 package proof, including `srchybrid/WebServerJson.cpp`, `srchybrid/WebServerArrCompat.cpp`, `srchybrid/WebServerQBitCompat.cpp`, `srchybrid/WebApiSurfaceSeams.h`, and REST seam headers.
- The 0.7.3 identity itself is aligned in source and build defaults: `srchybrid/Version.h` sets `MOD_RELEASE_VERSION_MAJOR/MINOR/PATCH` to `0.7.3`, `srchybrid/ReleaseUpdateCheckSeams.h` uses tag prefix `emule-bb-v` and asset prefix `eMule-broadband-`, and `repos/eMule-build/emule_workspace/config.py` plus `cli.py` default package release version to `0.7.3`.

Impact:

The package and final proof evidence do not cover the current runtime candidate. Because the delta after `74e5c76` includes REST and compatibility adapter code, shipping or tagging `emule-bb-v0.7.3` from current `main` would publish code that has not gone through the documented minimum beta proof or package provenance checks.

Recommended fix:

Hold the beta tag and public release until a fresh current-head proof is completed. Treat the existing 0.7.3 package rehearsal as stale evidence for the current candidate.

Suggested validation:

Run the policy-compliant proof through `repos/eMule-build` only, sequentially:

- `python -m emule_workspace validate`
- `python -m emule_workspace build app --config Debug --platform x64`
- `python -m emule_workspace build app --config Release --platform x64`
- `python -m emule_workspace build app --config Release --platform ARM64`
- `python -m emule_workspace test all --config Release --platform x64`
- `python -m emule_workspace package-release --config Release --platform x64`
- `python -m emule_workspace package-release --config Release --platform ARM64`
- Rerun controller live E2E gates for aMuTorrent, Prowlarr, Radarr, and Sonarr using the supported `python -m emule_workspace` live-test entrypoints.

Owner suggestion: Release owner with app/runtime and build-test owners.

Execution checklist:

- [ ] Freeze the chosen beta candidate commit set and record current app, build, tests, and tooling heads.
- [ ] Rerun minimum beta proof through `python -m emule_workspace` commands from `repos/eMule-build`, without direct app-project builds.
- [ ] Regenerate x64 and ARM64 0.7.3 package rehearsals and confirm sidecar manifests record current app/build/tooling commits.
- [ ] Verify REST/qBit/Torznab/aMuTorrent/Arr smoke results on the post-`74e5c76` REST adapter delta.
- [ ] Update release evidence docs only after the proof passes, then request separate operator approval before creating `emule-bb-v0.7.3`.

### High: PCP/NAT-PMP discovery can outlive its owner and thread launch failure can crash

Severity: High

Affected area: UPnP/NAT traversal startup, refresh, and shutdown reliability.

Evidence:

- `srchybrid/UPnPImplPcpNatPmp.cpp`, `CUPnPImplPcpNatPmp::~CUPnPImplPcpNatPmp`, calls `StopAsyncFind()`, then `DeletePorts()`, then `CleanupContext()`.
- `srchybrid/UPnPImplPcpNatPmp.cpp`, `CUPnPImplPcpNatPmp::StopAsyncFind`, sets `m_bAbortDiscovery = true`, waits only up to 7 seconds on `m_mutBusy`, logs timeout, leaves the worker potentially running, then resets `m_bAbortDiscovery = false`.
- `srchybrid/UPnPImplPcpNatPmp.cpp`, `CUPnPImplPcpNatPmp::CStartDiscoveryThread::Run`, keeps a raw `m_pOwner`, locks the owner's static mutex, and accesses owner fields and libpcpnatpmp context/flows during discovery and mapping.
- `srchybrid/UPnPImplPcpNatPmp.cpp`, `CUPnPImplPcpNatPmp::StartThread`, dereferences `pStartDiscoveryThread` immediately after `AfxBeginThread(...)` without checking for `NULL`.
- `srchybrid/UPnPImplMiniLib.cpp`, `CUPnPImplMiniLib::StartThread`, has the same unchecked `AfxBeginThread` dereference, and `CUPnPImplMiniLib::StopAsyncFind` still uses `TerminateThread` after a 7-second wait.
- Existing tests in `repos/eMule-build-tests` cover UPnP wrapper ordering and MiniUPnP mapping seams, but I did not find coverage for PCP/NAT-PMP launch failure, cooperative cancellation, timeout shutdown, or owner lifetime.

Impact:

If a router/library call hangs past the 7-second wait during shutdown or backend reset, the PCP/NAT-PMP worker can continue through a raw owner pointer while the wrapper deletes the implementation and its PCP context/flows. That is a credible use-after-free or crash path. Under low-memory or thread-creation failure, both NAT backends can dereference a null `CWinThread*` during startup instead of reporting UPnP failure and allowing the client to continue.

Recommended fix:

Convert NAT discovery workers to an explicit cooperative ownership model before beta tagging. The fix should be narrow: no NAT behavior rewrite, only launch failure handling, cancellation, and lifetime hardening.

Suggested validation:

Add focused seam/native tests for `AfxBeginThread` failure classification, suspended-thread resume failure, worker timeout, and owner destruction while discovery is in progress. Then run the NAT-related native tests plus a live UPnP smoke through the supported workspace entrypoints.

Owner suggestion: App networking/runtime owner with build-test support.

Execution checklist:

- [ ] Add or reuse a seam that lets `CUPnPImplPcpNatPmp::StartThread` and `CUPnPImplMiniLib::StartThread` fail gracefully when `AfxBeginThread` returns `NULL`.
- [ ] Keep the abort flag asserted until the worker is known to have exited; do not reset it after a timeout while the worker may still run.
- [ ] Replace the MiniUPnP `TerminateThread` fallback with cooperative wake/cancel/observe semantics or mark the backend failed while preserving owner lifetime until the worker exits.
- [ ] Ensure wrapper reset/destruction cannot delete an implementation while its worker can still access `m_pOwner`, context pointers, flow pointers, or result window state.
- [ ] Add native seam tests for launch failure, timeout, and repeated Start/Stop/Reset cycles for both NAT backends.
- [ ] Run `python -m emule_workspace validate`, a focused native test run covering UPnP seams, and the smallest live UPnP smoke that exercises automatic backend ordering.

## Missing Tests / Validation Gaps

- [ ] Fresh current-head beta proof is missing for app commit `df1191e`, build commit `7d81b07`, tooling commit `d3b0cba`, and the current `repos/eMule-build-tests` state.
- [ ] Current 0.7.3 package rehearsals do not cover the runtime REST delta after app commit `74e5c76`.
- [ ] PCP/NAT-PMP implementation lacks focused native seam coverage for `AfxBeginThread` failure, cancellation timeout, and owner destruction while a worker is in flight.
- [ ] MiniUPnP implementation lacks a regression test proving shutdown no longer uses forced thread termination.
- [ ] Live UPnP coverage validates backend-order logging, but not shutdown/resource cleanup under router/library stalls.
- [ ] No long-running soak evidence was found for the post-`74e5c76` REST/qBit/Torznab/Arr adapter hardening commits.

## Cross-review Notes

- `repos/eMule-build-tests` had pre-existing modified and untracked files when reviewed: live E2E/profile scripts, live-wire manifests, and related Python tests. I did not edit or interpret those changes as mine.
- Product naming and release identity are mostly aligned for beta 0.7.3 in current source/build defaults. The remaining issue is provenance: evidence and package manifests must be regenerated on current heads.
- Some active docs still contain superseded `1.0.1` proof details by design, but they can be easy to misread because `CI-033` is marked done while its package table is explicitly superseded.

## Assumptions

- Current `main` heads are the intended beta candidate unless the release owner freezes a different commit set.
- Existing modified/untracked files in `repos/eMule-build-tests` belong to another agent or prior user work and were not changed by this review.
- I did not run build, test, live-test, package, or cleanup commands because this task was audit output only and other agents were working in parallel.
- The stale experimental checkout was not needed for these conclusions and was not used as an active baseline.

## Beta Readiness Verdict

Release blocker. Do not tag or publish `emule-bb-v0.7.3` from current `main` until the fresh current-head proof/package rehearsal passes and the UPnP/NAT traversal worker lifetime issue is either fixed or explicitly accepted as non-blocking by the release owner.
