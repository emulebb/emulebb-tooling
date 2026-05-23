# Beta Readiness Review: Build, Test, Packaging, and Release

> Historical snapshot: this audit preserves the 2026-05-11 findings. Current
> beta 0.7.3 release source and pending execution status are controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

## Executive Summary

Release blocker. The build/release path has the right public beta identity (`0.7.3`, `emule-bb-v0.7.3`, and `eMule-broadband-0.7.3-ARCH.zip`), but the current publishable assets are not proven against current `main`, final release proof rows are still open, `emulebb-build-tests` is currently dirty, and `package-release` can create provenance-mismatched packages from dirty source/doc trees. These need to be closed before the first beta can be tagged or published.

## Review Checklist

- [x] Read workspace root `AGENTS.md`.
- [x] Read `repos\emulebb-tooling\docs\WORKSPACE-POLICY.md`.
- [x] Checked `git status --short --branch` before drawing conclusions in `repos\emulebb-tooling`, `repos\emulebb-build`, `repos\emulebb-build-tests`, `repos\emulebb`, `workspaces\v0.72a\app\eMule-main`, `workspaces\v0.72a\app\eMule-v0.72a-community`, and `workspaces\v0.72a\app\eMule-v0.72a-broadband`.
- [x] Reviewed `python -m emule_workspace` CLI surfaces for validate/build/test/package entrypoints.
- [x] Reviewed release package implementation, generated package manifests, active release control docs, release naming policy, and app release version constants.
- [x] Reviewed x64/ARM64 package surface and active build policy evidence statically.
- [ ] Re-run final proof after current repo dirt is resolved and current commits are selected.
- [ ] Regenerate x64 and ARM64 `0.7.3` packages from current release-ready commits.
- [ ] Record final command evidence in the active checklist before tagging.

## Findings

### Release blocker: Existing 0.7.3 packages are stale relative to current main

Severity: Release blocker

Affected area: Release package evidence, beta asset publication, final release checklist

Evidence:

- Generated manifests under `workspaces\v0.72a\state\release\emule-bb-v0.7.3` record x64 and ARM64 packages generated on `2026-05-10T20:11:29Z` and `2026-05-10T20:11:41Z`.
- Those manifests record `appCommit: 74e5c76`, `buildCommit: 0ead21a`, and `toolingCommit: 2d904c3`.
- Current checked heads are app `df1191e`, build `7d81b07`, tooling `d3b0cba`, and build-tests `76af0ef`.
- `repos\emulebb-tooling\docs\active\RELEASE-0.7.3.md:92` records package rehearsal at the older app/build/tooling commits and `docs\active\RELEASE-0.7.3.md:93` says not to create or push the tag until remaining minimum beta proof is complete.
- `docs\active\RELEASE-0.7.3-CHECKLIST.md:6` says the beta checklist must be refreshed on current `main`; `docs\active\RELEASE-0.7.3-CHECKLIST.md:44`, `:59`, and `:65` still have unchecked final clean-worktree/package-verification/tagging rows.
- App commits after the package manifest include REST and adapter changes, for example `df1191e CI-014 harden peer friend REST response`, `784ea9b CI-014 stabilize REST operation envelopes`, and many other `CI-014` / `FEAT-014` commits.

Impact:

Publishing the current ZIPs would publish binaries and docs for older commits, not the current release candidate. The active beta docs explicitly require refreshed proof on current `main`; this is not a paperwork issue because post-package app and tooling commits touch release-facing REST/API behavior and documentation.

Recommended fix:

Treat the existing `0.7.3` ZIPs as stale local rehearsal assets. Select the release commit set, resolve current working-tree dirt, rerun the minimum beta proof, regenerate packages, and update the checklist with current commit hashes and package hashes before tagging.

Suggested validation:

- `python -m emule_workspace validate`
- `python -m emule_workspace build app --config Debug --platform x64`
- `python -m emule_workspace build app --config Release --platform x64`
- `python -m emule_workspace build app --config Release --platform ARM64`
- `python -m emule_workspace build tests --config Debug --platform x64`
- `python -m emule_workspace build tests --config Release --platform x64`
- `python -m emule_workspace test all --config Debug --platform x64`
- `python -m emule_workspace test all --config Release --platform x64`
- `python -m emule_workspace test live-e2e --config Release --platform x64`
- `python -m emule_workspace package-release --config Release --platform x64`
- `python -m emule_workspace package-release --config Release --platform ARM64`

Owner suggestion: Release owner with build orchestration owner and test harness owner.

Execution checklist:

- [ ] Decide the exact app/build/tooling/build-tests commits that are the beta candidate.
- [ ] Bring all active repos to the intended clean release state.
- [ ] Run the minimum beta proof commands sequentially through `python -m emule_workspace`.
- [ ] Regenerate both package assets from the selected release state.
- [ ] Compare regenerated sidecar manifests against selected commits and expected asset names.
- [ ] Update `RELEASE-0.7.3-CHECKLIST.md` only after the evidence exists.

### Release blocker: Active workspace is not clean enough for tagging or final proof

Severity: Release blocker

Affected area: Release preflight, clean-worktree gate, final release decision

Evidence:

- `git status --short --branch` in `repos\emulebb-build-tests` reports modified files: `emule_test_harness/live_e2e_suite.py`, `emule_test_harness/live_profiles.py`, `manifests/release-live-wire-golden.v1.json`, live scripts, and multiple test files.
- The same status reports untracked `scripts/radarr-emulebb-live.py` and `scripts/sonarr-emulebb-live.py`.
- `docs\active\RELEASE-0.7.3-RUNBOOK.md:24` says not to continue to tagging if any active repo has unrelated uncommitted changes.
- `docs\active\RELEASE-0.7.3-CHECKLIST.md:59` still requires confirming no active workspace repo has unrelated uncommitted changes.

Impact:

The release evidence cannot be trusted as final while the active test harness has uncommitted changes. These files directly affect live E2E, release golden vectors, Prowlarr/Radarr/Sonarr proof, and package-readiness tests, so the dirt is inside the release proof system, not an unrelated scratch area.

Recommended fix:

Resolve the `emulebb-build-tests` work in a normal reviewed commit, or explicitly exclude it from the release candidate after confirming it is unrelated. Do not tag or publish while the release proof harness has uncommitted state.

Suggested validation:

- `git -C repos\emulebb-build-tests status --short --branch`
- `python repos\emulebb-tooling\ci\check-clean-worktree.py`
- `python -m emule_workspace test python --path tests/python/test_release_golden.py --path tests/python/test_live_e2e_suite.py`
- Final full proof commands from the release runbook after cleanliness is restored.

Owner suggestion: Test harness owner and release owner.

Execution checklist:

- [ ] Review every modified/untracked `repos\emulebb-build-tests` path and classify it as release-intended or unrelated.
- [ ] Commit intended release proof harness changes on `main`, or move unrelated local work out of the release workspace.
- [ ] Re-run `git status --short --branch` in every active repo listed by the runbook.
- [ ] Run the clean-worktree guard only after active work is intentionally committed or removed by its owner.
- [ ] Repeat final proof from the clean state.

### High risk: `package-release` does not guard against dirty package inputs

Severity: High risk

Affected area: Package provenance, release manifests, reproducibility, operator safety

Evidence:

- `repos\emulebb-build\emule_workspace\release.py:35` hard-wires package input to `layout.get_app_variant("main").path`.
- `release.py:100-114` records package provenance as `appCommit`, `buildCommit`, and `toolingCommit`.
- The only cleanliness/reanchor check in packaging is `ensure_canonical_app_anchor()` at `release.py:132-149`, and it checks `layout.seed_repo_path`, not the active app worktree, build repo, or tooling docs copied into the package.
- `release.py:74-89` copies `README.md` from the app worktree and REST docs from tooling into the ZIP, but the manifest records only repository HEADs. If either tree is dirty, the package can contain content not represented by the recorded commits.

Impact:

The package manifest can lie without any explicit failure: a local dirty app/doc change can be compiled or copied into a release ZIP while the sidecar manifest still points to the clean HEAD commit. That breaks auditability and can make a published beta impossible to reconstruct.

Recommended fix:

Make `package-release` fail fast unless all package input repos are clean, or add an explicit `--allow-dirty` diagnostic-only option that marks the manifest as non-publishable. At minimum, check active app variant, `repos\emulebb-build`, and `repos\emulebb-tooling`; for final release proof also require clean `repos\emulebb-build-tests`.

Suggested validation:

- Add unit coverage in `repos\emulebb-build\tests` that simulates dirty app/tooling/build repo status and asserts `package-release` rejects it.
- Run `python -m emule_workspace test python --path tests` from the supported workspace entrypoint.
- Run both final package commands after the guard is in place.

Owner suggestion: `emulebb-build` owner.

Execution checklist:

- [ ] Add a helper in `release.py` that checks `repo_status_lines()` for package input repos and reports the dirty paths.
- [ ] Call the helper before any build or copy work starts.
- [ ] Include app main, build repo, tooling repo, and optionally build-tests for final release mode.
- [ ] Add CLI/test coverage for clean and dirty package inputs.
- [ ] Re-run x64 and ARM64 packaging after the guard lands.

### High risk: Release archives and manifests are not reproducible by construction

Severity: High risk

Affected area: Reproducible beta packaging, package hashing, release verification

Evidence:

- `repos\emulebb-build\emule_workspace\release.py:114` writes `generatedAt` with `datetime.now(timezone.utc)`, so the sidecar manifest changes on every run.
- `release.py:245-249` uses `zipfile.ZipFile(..., "w", compression=zipfile.ZIP_DEFLATED)` plus `archive.write(...)`, which inherits filesystem timestamps and default ZIP metadata rather than a normalized timestamp/mode/order policy.
- There is no package determinism test in `repos\emulebb-build\tests`; current tests only assert CLI help exposes `--release-version` at `tests\test_cli.py:91-98`.
- `docs\active\items\FEAT-056.md:26` defers package manifest diff reporting to next-patch rather than making it a current release guard.

Impact:

Operators cannot prove that the same selected commit set yields the same package hash. That weakens first-beta artifact review and makes hash differences hard to triage after publication. The current sidecar manifest is useful as provenance, but it is not a reproducible-build proof.

Recommended fix:

Add deterministic packaging mode for release artifacts: stable ZIP entry ordering, normalized timestamps and permissions, explicit compression level, and a manifest schema that separates deterministic package inputs from non-deterministic generation metadata.

Suggested validation:

- Run two sequential `package-release` rehearsals from the same clean commit set for x64 and compare SHA-256 values.
- Add a unit-level package writer test that fixes source file mtimes and asserts byte-identical ZIP output.
- Keep any wall-clock `generatedAt` outside the ZIP and mark it as sidecar metadata only.

Owner suggestion: `emulebb-build` owner with release owner.

Execution checklist:

- [ ] Introduce a deterministic ZIP writer using `ZipInfo` with normalized timestamps, permissions, and sorted relative paths.
- [ ] Decide whether `generatedAt` is allowed in sidecar manifests or should be replaced by deterministic input metadata plus operator evidence.
- [ ] Add tests that package the same staging tree twice and compare hashes.
- [ ] Rehearse x64 and ARM64 packages twice from the clean candidate and confirm identical hashes.
- [ ] Record the reproducibility result in the release checklist.

### Medium risk: Language resource projects carry stale `v145` toolset declarations

Severity: Medium risk

Affected area: Active build policy, language DLL build, package portability

Evidence:

- Workspace policy requires active MSVC toolset baseline `v143` in `docs\WORKSPACE-POLICY.md:463-486`.
- Main app project declares `v143` at `workspaces\v0.72a\app\eMule-main\srchybrid\emule.vcxproj:32`.
- Language DLL projects declare `v145`; examples include `srchybrid\lang\ar_AE.vcxproj:21`, `srchybrid\lang\de_DE.vcxproj:21`, and every other active language project returned by static scan.
- Package orchestration compensates by passing `/p:PlatformToolset=v143` unless overridden at `repos\emulebb-build\emule_workspace\release.py:188-190`.

Impact:

The supported package command likely builds because it overrides the toolset, but the checked-in project files still violate the policy baseline and can fail or drift when opened or built outside the package path. The static policy audit also does not appear to enforce language project toolset declarations, leaving this drift easy to reintroduce.

Recommended fix:

Normalize language project toolset declarations to `v143`, or document and enforce an explicit exception if the release owner wants orchestration-only override to remain authoritative.

Suggested validation:

- `python -m emule_workspace validate`
- `python -m emule_workspace package-release --config Release --platform x64`
- `python -m emule_workspace package-release --config Release --platform ARM64`
- Extend the workspace policy audit to include `srchybrid\lang\*.vcxproj` toolset values.

Owner suggestion: App build owner and tooling policy owner.

Execution checklist:

- [ ] Decide whether language projects should be normalized to `v143` or formally exempted.
- [ ] If normalized, update every active `srchybrid\lang\*.vcxproj` `PlatformToolset` value to `v143`.
- [ ] Add a policy audit assertion for language project toolsets.
- [ ] Run validate and both package commands sequentially.
- [ ] Record the package proof in CI-031 or the release checklist.

### Medium risk: Package command cannot select the release-intent broadband worktree

Severity: Medium risk

Affected area: Release branch policy, packaging target selection, operator clarity

Evidence:

- Workspace policy identifies `release/v0.72a-broadband` as the only release-intent branch at `docs\WORKSPACE-POLICY.md:92-104` and says official releases should be annotated tags on the chosen release-branch commit at `docs\WORKSPACE-POLICY.md:536-543`.
- Active release control identifies the candidate app line as `workspaces\v0.72a\app\eMule-main` on `main` at `docs\active\RELEASE-0.7.3.md:22`.
- `repos\emulebb-build\emule_workspace\release.py:35` always packages the `main` variant and `repos\emulebb-build\emule_workspace\cli.py:518-521` exposes no package variant or release-branch selection option.

Impact:

The current docs and implementation can support a `main`-based beta candidate, but the policy also names a release-intent branch and annotated release-branch tags. Without an explicit release-target decision, an operator could tag one commit while packaging another line, or assume `package-release` builds the broadband release worktree when it always builds `main`.

Recommended fix:

Resolve the release-target policy: either explicitly document that beta `0.7.3` packages are cut from `main`, or add `package-release --variant broadband|main` and require the selected variant to match the tag target.

Suggested validation:

- Add CLI tests showing the default package target and any explicit variant option.
- Confirm sidecar manifest records the selected variant name and branch.
- Before tagging, compare `git rev-parse` of the selected package variant and the annotated tag target.

Owner suggestion: Release owner and `emulebb-build` owner.

Execution checklist:

- [ ] Decide whether Beta 0.7.3 ships from `main` or `release/v0.72a-broadband`.
- [ ] Update release docs so the selected line and tag target are unambiguous.
- [ ] If needed, add package variant selection to `package-release`.
- [ ] Record variant, branch, and commit in package manifests.
- [ ] Validate that the annotated tag is created on the same commit that was packaged.

## Missing Tests / Validation Gaps

- [ ] No automated dirty-input guard test for `package-release` provenance.
- [ ] No deterministic package hash test for repeated package generation from identical inputs.
- [ ] No static audit coverage for language project `PlatformToolset` drift under `srchybrid\lang\*.vcxproj`.
- [ ] No package manifest field for selected app variant or branch.
- [ ] No final current-HEAD package proof after app/build/tooling/build-tests moved past the recorded package manifest commits.
- [ ] No final clean-worktree proof while `repos\emulebb-build-tests` has modified and untracked release-harness files.

## Cross-review Notes

- REST/API changes after the current package rehearsal are likely covered by another review area, but they make the current package hashes stale for build/release purposes.
- The current runbook and checklist intentionally hold tagging; this audit agrees with that hold.
- I did not run build/test/package commands during this audit. Static inspection was sufficient, and package/test commands would have been premature while `emulebb-build-tests` is dirty.

## Assumptions

- The checked generated ZIPs and sidecar manifests under `workspaces\v0.72a\state\release\emule-bb-v0.7.3` are local rehearsal artifacts, not already published public assets.
- Current `main` heads are intended to be considered for the first beta unless the release owner selects an earlier commit.
- The uncommitted `repos\emulebb-build-tests` changes are from another user or agent and should not be reverted by this audit.
- The active policy remains authoritative where older release docs mention Release 1.0 terminology.

## Beta Readiness Verdict

Release blocker. Do not tag or publish `emule-bb-v0.7.3` until the workspace is clean, final proof is refreshed on the selected current release commits, x64/ARM64 packages are regenerated, package provenance cannot include dirty inputs, and the release checklist records current evidence.
