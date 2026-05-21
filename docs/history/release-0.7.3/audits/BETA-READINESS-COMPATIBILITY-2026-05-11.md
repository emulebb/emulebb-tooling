# Beta Readiness Review: Regression and Compatibility

> Historical snapshot: this audit preserves the 2026-05-11 findings. Current
> beta 0.7.3 release source and pending execution status are controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

## Executive Summary

Release blocker. The active release-intent branch is not aligned with current `main`, and the release packaging entrypoint packages `main` directly while policy requires official releases to be tagged on a chosen release-branch commit. That creates a concrete risk that the first beta package, release tag, update-check identity, and regression proof will refer to different code.

## Review Checklist

- [x] Read workspace root `AGENTS.md`.
- [x] Read `repos/eMule-tooling/docs/WORKSPACE-POLICY.md`.
- [x] Read repo-local `AGENTS.md` files for the app, build, test, and tooling repos after the workspace policy.
- [x] Ran `git status --short --branch` before drawing conclusions for `workspaces/v0.72a/app/eMule-main`, `workspaces/v0.72a/app/eMule-v0.72a-community`, `workspaces/v0.72a/app/eMule-v0.72a-broadband`, `repos/eMule-build`, `repos/eMule-build-tests`, and `repos/eMule-tooling`.
- [x] Compared `main` against `release/v0.72a-community` for changed-surface scale and compatibility-sensitive files.
- [x] Compared `main` against `release/v0.72a-broadband` for release-branch readiness.
- [x] Reviewed beta 0.7.3 version, tag, package naming, and update-check identity in app and build tooling.
- [x] Reviewed persisted preference/default changes, upload scheduler behavior, and documented broadband exceptions.
- [ ] Align the release-intent branch, package source, tag source, and final evidence commit.
- [ ] Refresh regression and package proof after the release source of truth is aligned.

## Findings

### Release blocker: Release-intent branch is not the current beta candidate

Severity: Release blocker

Affected area: Release branch policy, beta tag source, packaged-code identity, update-check identity.

Evidence: `repos/eMule-tooling/docs/WORKSPACE-POLICY.md:92` states that `main` is not a release branch, and `docs/WORKSPACE-POLICY.md:93` plus `docs/WORKSPACE-POLICY.md:103` identify `release/v0.72a-broadband` as the only release-intent branch. `git rev-list --left-right --count release/v0.72a-broadband...main` in `workspaces/v0.72a/app/eMule-main` returned `3	308`. The release-intent branch has only `57dd9f7`, `e2e991a`, and `d545177` beyond `main`, while `main` has 308 commits beyond it. `git show release/v0.72a-broadband:srchybrid/Version.h` shows no `MOD_RELEASE_*` beta identity, while current `main` has `MOD_RELEASE_PRODUCT_NAME`, `MOD_RELEASE_TAG_PREFIX`, and `MOD_RELEASE_VERSION_*` set to `eMule BB`, `emule-bb-v`, and `0.7.3` in `srchybrid/Version.h:36` through `srchybrid/Version.h:47`. `git diff --name-status release/v0.72a-broadband..main -- srchybrid/Version.h srchybrid/ReleaseUpdateCheckSeams.h srchybrid/ReleaseUpdateCheck.cpp srchybrid/emule.rc` shows the release-update implementation and eMule BB resource branding are absent from the release-intent branch.

Impact: Tagging `release/v0.72a-broadband` now would not tag the current beta product; tagging `main` would conflict with current policy. Either path can produce a public beta whose tag, binary version, GitHub update-check rules, and release notes do not describe the same code. That is a first-beta publication blocker, not only a documentation issue.

Recommended fix: Choose one release source of truth before any public beta tag. Under the current policy, promote reviewed current `main` commits to `release/v0.72a-broadband`, resolve the three release-branch-only commits deliberately, and make the final release candidate a single known release-branch commit. If the intended release model has changed to tag `main`, update the workspace policy and package tooling together before tagging.

Suggested validation: After alignment, verify that `release/v0.72a-broadband` contains the current eMule BB 0.7.3 identity, that `main..release/v0.72a-broadband` contains no unreviewed product delta, and that the package manifest app commit equals the chosen tag commit.

Owner suggestion: Release engineering owner with app maintainer review.

Execution checklist:
- [ ] From the app worktree, run `git status --short --branch` for both `eMule-main` and `eMule-v0.72a-broadband` and confirm no unrelated local work is present.
- [ ] Decide whether beta `0.7.3` tags must be cut from `release/v0.72a-broadband` as policy currently says, or whether policy will be changed to allow tagging `main`.
- [ ] If keeping the release branch model, backport or merge reviewed `main` release-candidate commits into `release/v0.72a-broadband` without adding new feature work there.
- [ ] Recheck `srchybrid/Version.h`, `srchybrid/ReleaseUpdateCheckSeams.h`, `srchybrid/ReleaseUpdateCheck.cpp`, and `srchybrid/emule.rc` on the release branch for `eMule BB`, `0.7.3`, `emule-bb-v`, and `eMule-broadband-` identity.
- [ ] Record the final chosen release-branch commit before package rehearsal and tag creation.

### High: Release package tooling packages `main`, not a release branch

Severity: High

Affected area: Packaging orchestration, release asset provenance, tag/package consistency.

Evidence: `repos/eMule-build/emule_workspace/release.py:34` calls `ensure_canonical_app_anchor(layout)`, then `release.py:35` hardcodes `app_root = layout.get_app_variant("main").path`; `release.py:36` checks the package version against that app root. The `package-release` command in `repos/eMule-build/emule_workspace/cli.py:518` through `cli.py:535` exposes `--release-version` but no release-variant or tag-commit input. Current policy says official releases should be annotated tags on a chosen release-branch commit in `docs/WORKSPACE-POLICY.md:536` through `docs/WORKSPACE-POLICY.md:537`.

Impact: Even if the release branch is fixed, the supported package command still proves and packages `main`. That can produce ZIPs and manifests from one commit while the public annotated tag points at another commit. The update checker is strict about `emule-bb-vMAJOR.MINOR.PATCH` and `eMule-broadband-` assets in `srchybrid/ReleaseUpdateCheckSeams.h:63` through `srchybrid/ReleaseUpdateCheckSeams.h:64`, so provenance drift directly affects users who rely on update notifications.

Recommended fix: Make packaging accept and record the chosen release app variant or release commit, then assert that the package source equals the intended tag source. The conservative fix is to add an explicit release-variant option defaulting to `broadband` for release packaging, with a guard that rejects packaging from `main` unless policy is deliberately changed.

Suggested validation: Package x64 and ARM64 from the chosen release branch, inspect both sidecar manifests for the same app commit, version `0.7.3`, tag `emule-bb-v0.7.3`, and asset names `eMule-broadband-0.7.3-x64.zip` and `eMule-broadband-0.7.3-arm64.zip`.

Owner suggestion: Build orchestration owner with release owner sign-off.

Execution checklist:
- [ ] In `repos/eMule-build`, run `git status --short --branch` before editing package orchestration.
- [ ] Add a packaging source selection that is policy-aligned with the chosen release branch.
- [ ] Make `package-release` fail if the selected app source does not contain the requested `MOD_RELEASE_VERSION_TEXT`.
- [ ] Make the package manifest record the selected app variant and exact app commit.
- [ ] Run `python -m emule_workspace validate` from `repos/eMule-build`.
- [ ] Run `python -m emule_workspace package-release --config Release --platform x64 --release-version 0.7.3`.
- [ ] Run `python -m emule_workspace package-release --config Release --platform ARM64 --release-version 0.7.3`.

### High: Current beta proof is stale relative to current app, build, and tooling heads

Severity: High

Affected area: Regression evidence, package evidence, REST/controller compatibility claims.

Evidence: `docs/active/RELEASE-0.7.3.md:87` through `docs/active/RELEASE-0.7.3.md:94` records current 0.7.3 package rehearsal evidence for app commit `74e5c76`, build commit `0ead21a`, and tooling commit `2d904c3`. Current app `main` is `df1191e`; `git rev-list --count 74e5c76..main` returned `22`, including CI-014 REST and adapter hardening commits. Current `repos/eMule-build` is `7d81b07`, two commits past `0ead21a`; current `repos/eMule-tooling` is `d3b0cba`, 29 commits past `2d904c3`. `repos/eMule-build-tests` is also currently dirty, with modified live E2E harness files and untracked `scripts/radarr-emulebb-live.py` and `scripts/sonarr-emulebb-live.py`.

Impact: The documented proof no longer proves the current code or current release tooling. This is especially risky because the post-evidence app commits touch REST route shape, response envelopes, search type tokens, Torznab media search, qBit Arr import, and peer-friend REST response behavior. Controller compatibility and update readiness must be based on the code that will actually ship.

Recommended fix: Treat existing proof as historical evidence only. After the release branch/package source issue is resolved and the test-harness worktree is settled, rerun the minimum current-candidate proof from `repos/eMule-build` with the supported `python -m emule_workspace` entrypoints.

Suggested validation: Re-run validation, native/community comparison, focused live/controller checks, and package rehearsal on the exact release candidate. Record current app/build/test/tooling commits in the release control document only after the runs pass.

Owner suggestion: Release QA owner with support from test-harness owner.

Execution checklist:
- [ ] Wait for the concurrent `repos/eMule-build-tests` live-harness changes to be either committed or explicitly excluded from release evidence.
- [ ] Run `git status --short --branch` in every repo and app worktree used for the proof.
- [ ] From `repos/eMule-build`, run `python -m emule_workspace validate`.
- [ ] From `repos/eMule-build`, run `python -m emule_workspace test community-core-coverage --config Release --platform x64 --test-run-variant main --baseline-variant community`.
- [ ] From `repos/eMule-build`, run the scoped live/controller gates required by `docs/active/RELEASE-0.7.3.md` for the final candidate.
- [ ] Re-run x64 and ARM64 `package-release` for version `0.7.3` after the package source is policy-aligned.
- [ ] Record the exact app, build, build-tests, and tooling commits used by the refreshed proof.

### Medium: Upload-scheduler compatibility has intentional drift but incomplete beta validation

Severity: Medium

Affected area: Upload scheduling, eD2K peer fairness, collection request behavior, migrated user preferences.

Evidence: `srchybrid/Preferences.cpp:341` through `srchybrid/Preferences.cpp:343` normalize missing or unlimited upload limits to `6100` KiB/s; `Preferences.cpp:2752` and `Preferences.cpp:2753` set new first-run defaults for upload and download limits. `Preferences.cpp:2897` through `Preferences.cpp:2908` enable broadband upload policy defaults such as `MaxUploadClientsAllowed=8`, low-ratio boost enabled by default, and session transfer mode defaulting to percent-of-file. `srchybrid/UploadQueue.cpp:374` through `srchybrid/UploadQueue.cpp:392` replace stock dynamic slot growth with a fixed broadband cap and target. `UploadQueue.cpp:650` clears the collection upload slot marker before normal admission, and `UploadQueue.cpp:678` through `UploadQueue.cpp:694` routes direct admission through slow-upload cooldown and fixed-cap checks. The intentional collection exception is documented in `docs/history/features/FEATURE-BROADBAND.md:330` through `docs/history/features/FEATURE-BROADBAND.md:338`, but FEAT-015 acceptance criteria remain unchecked in `docs/active/items/FEAT-015.md:163` through `docs/active/items/FEAT-015.md:169`. Existing tests cover seams such as upload scoring and preference normalization, but the observed fixed-cap, slow-slot, collection, and migrated-profile behavior is not proven by a current end-to-end regression gate.

Impact: The changes are documented and may be valid beta behavior, but they are user-visible compatibility changes from community eMule: migrated users with unlimited upload are silently moved to a finite broadband budget, collection priority slots no longer bypass the queue, and slot count is capped by a new broadband policy. Without targeted proof, beta users could see reduced sharing throughput, different queue fairness, or collection-transfer latency and treat it as a regression.

Recommended fix: Close the upload-scheduler acceptance criteria with focused regression tests before first beta publication. The goal is not to revert the broadband scheduler; it is to prove the documented intentional drift behaves as designed and does not break protocol compatibility.

Suggested validation: Add or run tests that cover migrated `preferences.ini` values (`MaxUpload=0`, missing `MaxUpload`, existing finite `MaxUpload`), fixed slot cap at 8 and 12 on a high-bandwidth profile, slow/zero upload recycling and cooldown, and `.emulecollection` requests under the new non-priority admission model.

Owner suggestion: App upload-scheduler owner with QA/live-test support.

Execution checklist:
- [ ] Add a migrated-profile preference test for missing `MaxUpload`, `MaxUpload=0`, and finite existing `MaxUpload`.
- [ ] Add a deterministic upload-scheduler seam or live-diff scenario proving default `MaxUploadClientsAllowed=8` does not exceed the cap under high upload budget.
- [ ] Add a second scenario proving manual `MaxUploadClientsAllowed=12` is honored.
- [ ] Add a slow/zero uploader scenario proving warm-up, recycle, and cooldown timings match `docs/history/features/FEATURE-BROADBAND.md`.
- [ ] Add a collection-request scenario proving collection downloads still complete without the removed priority slot bypass.
- [ ] Run the resulting checks through `python -m emule_workspace test community-core-coverage --config Release --platform x64 --test-run-variant main --baseline-variant community` or the narrower supported `eMule-build` entrypoint that owns the new tests.

## Missing Tests / Validation Gaps

- [ ] Current release package proof from the exact tag source commit.
- [ ] Automated guard that package source, sidecar manifest app commit, and annotated tag commit are identical.
- [ ] Current `main` versus `release/v0.72a-community` proof after the 22 post-`74e5c76` app commits.
- [ ] Migrated `preferences.ini` compatibility coverage for stock unlimited upload and missing broadband policy keys.
- [ ] Upload-slot cap, slow-slot recycle, cooldown, and collection-request regression coverage.
- [ ] Final x64 and ARM64 package rehearsal after package tooling and release-branch policy are aligned.
- [ ] Clean or intentionally frozen `repos/eMule-build-tests` state before live/controller evidence is treated as release proof.

## Cross-review Notes

- Naming and release parser constants on current app `main` are aligned with policy: `srchybrid/Version.h:39` through `srchybrid/Version.h:47` use `eMule BB` and `0.7.3`, while `srchybrid/ReleaseUpdateCheckSeams.h:63` through `srchybrid/ReleaseUpdateCheckSeams.h:64` use `emule-bb-v` and `eMule-broadband-`.
- `repos/eMule-build/emule_workspace/config.py:145` and `repos/eMule-build/emule_workspace/cli.py:521` default release packaging to `0.7.3`.
- The current workspace manifest maps `main`, `community`, `broadband`, and `tracing-harness` worktrees consistently with the policy, but the release packaging command does not use the `broadband` release-intent worktree.
- The dirty `repos/eMule-build-tests` state appears to be concurrent/prior live-harness work. I did not modify it.

## Assumptions

- I treated `release/v0.72a-community` as the parity/regression baseline and did not treat stale branches as active.
- I treated existing modified/untracked files in `repos/eMule-build-tests` as prior work from another user or agent.
- I did not run build, validation, live-test, or package commands during this audit because the request was review output only and other agents are working in parallel.
- I treated current local `main` branches as current because `git status --short --branch` reported `main...origin/main` without ahead/behind counts for the app, build, build-tests, and tooling repos.

## Beta Readiness Verdict

Release blocker. Do not publish or tag beta `0.7.3` until the release branch, package source, tag source, and refreshed regression evidence all point to the same current candidate.
