# Beta Readiness Review: Feature Completeness

> Historical snapshot: this audit preserves the 2026-05-11 findings. Current
> beta 0.7.3 release source and pending execution status are controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

## Executive Summary

Release blocker. The advertised eMule BB feature set is largely implemented, but the first beta cannot be treated as release-ready because final proof and package evidence are stale against current `main`, the release-intent branch is not aligned with the current candidate, and public-facing update/API identity surfaces still carry pre-`emulebb` or stock-eMule identity.

## Review Checklist

- [x] Read workspace root `AGENTS.md`.
- [x] Read and applied `repos\emulebb-tooling\docs\WORKSPACE-POLICY.md`.
- [x] Ran `git status --short --branch` before drawing conclusions in `workspaces\v0.72a\app\eMule-main`.
- [x] Ran `git status --short --branch` before drawing conclusions in `workspaces\v0.72a\app\eMule-v0.72a-community`.
- [x] Ran `git status --short --branch` before drawing conclusions in `workspaces\v0.72a\app\eMule-v0.72a-broadband`.
- [x] Ran `git status --short --branch` before drawing conclusions in `repos\emulebb`.
- [x] Ran `git status --short --branch` before drawing conclusions in `repos\emulebb-build`.
- [x] Ran `git status --short --branch` before drawing conclusions in `repos\emulebb-build-tests`.
- [x] Ran `git status --short --branch` before drawing conclusions in `repos\emulebb-tooling`.
- [x] Reviewed active release control, checklist, runbook, package manifests, app version/update code, REST identity code, and package-facing README.
- [ ] Re-run the minimum beta proof on current heads after fixes.
- [ ] Reconcile release-intent branch/tag target before tagging.
- [ ] Add automated checks for public product identity and release URL drift.

## Findings

### Release blocker: Final beta proof and package evidence are stale against current main

Severity: Release blocker

Affected area: Release readiness, package contents, current-main feature proof, release-intent branch alignment.

Evidence:

- `docs\active\RELEASE-0.7.3.md:92-95` records package rehearsal evidence for app `74e5c76`, build `0ead21a`, and tooling `2d904c3`, and says tagging is held until remaining minimum proof is complete.
- Current checked heads are app `df1191e`, build `7d81b07`, and tooling `d3b0cba`.
- App commits after the packaged app commit include REST and adapter behavior changes such as `FEAT-014 clean REST v1 search and upload routes`, `CI-014 harden qBit Arr import adapter`, `CI-014 expose native search type tokens`, and `CI-014 harden peer friend REST response`.
- `docs\active\RELEASE-0.7.3-CHECKLIST.md:6-8` says the beta checklist must be refreshed on current `main` before tagging or publishing assets.
- `docs\active\RELEASE-0.7.3-CHECKLIST.md:24-45` still has all required command rows unchecked, and `docs\active\RELEASE-0.7.3-CHECKLIST.md:57-66` still leaves final evidence recording, clean-worktree confirmation, and tag creation unchecked.
- `git rev-list --left-right --count release/v0.72a-broadband...main` returned `3 308`; the release-intent branch is not current with the `main` candidate.
- `git ls-remote --tags origin 'refs/tags/emule-bb-v*'` returned no remote eMule BB release tags.

Impact:

The current beta packages do not prove the current app/build/tooling state. Several post-package commits affect REST and controller-facing behavior, which is part of the advertised beta feature set. Tagging or publishing from the existing evidence would ship an unproven binary and leave uncertainty about whether the release tag should land on `main` or the release-intent branch.

Recommended fix:

Refresh the final beta proof on current heads, then deliberately promote or tag the selected release commit according to policy.

Suggested validation:

Run only supported orchestration commands from `repos\emulebb-build`: `python -m emule_workspace validate`, required app/test builds, required native tests, full Release x64 `live-e2e`, and x64/ARM64 package rehearsal.

Owner suggestion:

Release owner with app, build, and test-harness owners available for failures.

Execution checklist:

- [ ] Confirm current dirty state is either cleaned or explicitly accepted before final proof; `repos\emulebb-build-tests` currently has unrelated modified and untracked live-test work.
- [ ] Decide whether `release/v0.72a-broadband` is to be fast-forwarded/cherry-picked to the proven `main` commit or whether policy/docs are updated to make `main` the beta tag target.
- [ ] Run `python -m emule_workspace validate` from `repos\emulebb-build`.
- [ ] Run the minimum beta proof from `docs\active\RELEASE-0.7.3.md:112-121`.
- [ ] Regenerate x64 and ARM64 packages from the selected current commit.
- [ ] Update release evidence docs only after proof passes.
- [ ] Create the annotated `emule-bb-v0.7.3` tag only after the operator gives the separate tagging instruction.

### High: Update and help links still target old `itlezy` locations instead of `emulebb`

Severity: High

Affected area: Public update check, Help link, GitHub release discovery, product naming/URL policy.

Evidence:

- Workspace policy says the GitHub organization, code name, and URL slug are `emulebb` in `docs\WORKSPACE-POLICY.md:521-524`.
- Release tags and assets must use `emule-bb-vMAJOR.MINOR.PATCH` and `eMule-broadband-MAJOR.MINOR.PATCH-ARCH.zip` in `docs\WORKSPACE-POLICY.md:528-532`.
- The active build topology uses `https://github.com/emulebb/emulebb.git` for the app repo.
- `srchybrid\Preferences.cpp:3647-3659` returns `https://github.com/itlezy/eMule`, `https://github.com/itlezy/eMule/releases`, and `https://api.github.com/repos/itlezy/eMule/releases/latest`.
- `srchybrid\Emule.cpp:87-88` sets online help to `https://github.com/itlezy/emulebb-tooling/blob/main/docs/HELP.md`.
- `srchybrid\ReleaseUpdateCheckSeams.h` correctly requires `emule-bb-v` tags and `eMule-broadband-...zip` assets, so the wrong repository endpoint can make an otherwise correct parser look like update failure.

Impact:

The public "Check for eMule BB updates" feature can query the wrong repository and fail to find the first beta or later eMule BB releases. The Help command also sends users to the old owner path, undermining first-beta public-facing completeness and supportability.

Recommended fix:

Move all app-facing GitHub URLs to the `eMulebb` organization and add a test seam that fails on old owner URLs.

Suggested validation:

Native update-check seam tests should evaluate a synthetic `emule-bb-v0.7.4` release payload with `eMule-broadband-0.7.4-x64.zip`, and a small source/static check should reject `github.com/itlezy` and `api.github.com/repos/itlezy` in app-facing release/help code.

Owner suggestion:

App owner for URL constants and update-check seam tests; tooling owner for release URL policy audit if centralized.

Execution checklist:

- [ ] Replace `CPreferences::GetHomepageBaseURLForLevel`, `GetVersionCheckBaseURL`, and `GetVersionCheckApiURL` with `eMulebb` URLs.
- [ ] Replace `ONLINEHELPURL` with the current `emulebb/emulebb-tooling` Help path or the final public docs URL.
- [ ] Add native seam coverage for release URL selection and update payload evaluation.
- [ ] Add a lightweight policy check for stale `itlezy` public URLs in active app sources and package-facing docs.
- [ ] Validate with `python -m emule_workspace validate` and the focused native update-check tests through the supported test entrypoint.

### Medium: Native REST app identity still reports stock `eMule`

Severity: Medium

Affected area: Native REST `/api/v1/app` identity, aMuTorrent/controller metadata, product naming.

Evidence:

- Workspace policy defines `eMule BB` as the compact app, UI, API, and protocol-facing mod name in `docs\WORKSPACE-POLICY.md:521-523`.
- `srchybrid\WebServerJson.cpp:819-826` builds the public REST app payload with `{"name", "eMule"}` while the same payload exposes beta capabilities.
- `srchybrid\Emule.cpp:896-904` intentionally keeps release builds at version text such as `0.7.3 x64`, so `name` is the only stable REST field that can identify the product as eMule BB.
- The OpenAPI app schema requires `name`, `version`, `apiVersion`, and `capabilities` in `docs\rest\REST-API-OPENAPI.yaml:1453-1483`, but it does not constrain the expected name value.

Impact:

Controllers and users reading the advertised native REST metadata see stock `eMule`, not `eMule BB`. That is a public API branding mismatch and can break consumer-side feature gating or support diagnostics that depend on product identity rather than only capabilities.

Recommended fix:

Return `eMule BB` from the native REST app identity and lock that value in contract tests/docs.

Suggested validation:

Add native REST route tests and live REST smoke assertions that `/api/v1/app` reports `name: "eMule BB"` and version `0.7.3...` for the beta candidate.

Owner suggestion:

App REST owner and REST contract/docs owner.

Execution checklist:

- [ ] Change `BuildAppJson` to use the compact policy name `eMule BB`.
- [ ] Update OpenAPI/contract docs to document the expected beta identity value.
- [ ] Add or update native route tests for `/api/v1/app` identity.
- [ ] Update live REST smoke to assert the identity in addition to capabilities.
- [ ] Validate with supported native and live REST lanes.

### Medium: Package-facing README still references superseded Release 1.0 gates

Severity: Medium

Affected area: Package contents, public release documentation, release naming/version rules.

Evidence:

- Package manifests include `eMule/README.md` in both x64 and ARM64 0.7.3 assets.
- `workspaces\v0.72a\app\eMule-main\README.md:13-16` says the broadband release-intent branch is not ready until "Release 1.0 gates and operator steps are complete".
- Workspace policy says the first beta/public release is `0.7.3`, and superseded `1.0.0`, `1.0.1`, and `1.1.1` labels are internal evidence/rehearsal labels only in `docs\WORKSPACE-POLICY.md:521-527`.

Impact:

The beta package can ship a README that tells users or downstream packagers that the release is gated on a superseded 1.0 concept. That is not a runtime defect, but it is a public-facing completeness gap for the first beta.

Recommended fix:

Make package-facing docs use the 0.7.3 beta naming model and keep historical "Release 1" language only in clearly marked internal history docs.

Suggested validation:

Add a package-content text scan that rejects `Release 1.0`, `1.0.1`, `1.1.1`, and old tag families in package-facing files unless they are in an explicitly internal evidence context.

Owner suggestion:

Tooling/docs owner with release owner review.

Execution checklist:

- [ ] Update app `README.md` to say beta `0.7.3` gates/operator steps instead of `Release 1.0` gates.
- [ ] Scan packaged files for superseded release labels and old tag families.
- [ ] Add package-content validation for public docs included in release ZIPs.
- [ ] Regenerate packages after documentation correction.
- [ ] Confirm the package manifests still include the corrected README and REST docs.

## Missing Tests / Validation Gaps

- [ ] No final current-head proof exists for app `df1191e`, build `7d81b07`, and tooling `d3b0cba`.
- [ ] No automated check appears to reject old public GitHub owner URLs in app release/help code.
- [ ] Native REST tests should assert `/api/v1/app.name == "eMule BB"`.
- [ ] Live REST smoke should verify product identity, not only route availability and capabilities.
- [ ] Package validation should scan included public docs for superseded release labels and stale release URL families.
- [ ] Release automation should fail when package manifests reference commits older than the current selected release candidate.

## Cross-review Notes

- `repos\emulebb-build-tests` is dirty on `main` with modified live E2E, live profile, release golden, and controller live scripts/tests plus untracked Radarr/Sonarr scripts. I treated these as parallel work and did not edit them. Final release proof should not proceed until the release owner either incorporates or isolates that work.
- `repos\amutorrent` reports `main...upstream/main [ahead 1]`. I did not use it for release-blocking conclusions beyond noting that controller compatibility should be revalidated after current app REST changes.
- `git ls-remote --tags origin 'refs/tags/emule-bb-v*'` returned no remote eMule BB release tags from `https://github.com/emulebb/emulebb.git`; this matches the 0.7.3 tag hold but conflicts with older wording that described superseded evidence tags as pushed.

## Assumptions

- The active beta candidate is the current `workspaces\v0.72a\app\eMule-main` `main` worktree unless the release owner explicitly promotes a different commit to `release/v0.72a-broadband`.
- `release/v0.72a-community` remains the parity baseline and is not a release target.
- Historical `analysis\stale-v0.72a-experimental-clean` was not needed for these findings.
- I did not run build, test, live, or package commands because this was a review-only audit and other agents have parallel work in progress.

## Beta Readiness Verdict

Not ready for first beta tagging or publication. Feature implementation is close, but current-head proof, release-branch/tag alignment, and public identity/update-link fixes must be completed before `emule-bb-v0.7.3` can be treated as release-ready.
