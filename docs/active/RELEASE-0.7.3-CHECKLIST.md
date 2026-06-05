# eMule Broadband Edition 0.7.3 RC1 Release Checklist

This is the final operator checklist for the 0.7.3 RC1 target
`emulebb-v0.7.3-rc.1`.
Do not record stale proof here; every row must be refreshed on the selected
reviewed `main` commit.

## Proof Status

Final proof resumed by operator direction on 2026-05-17. Run live E2E,
certification, package refresh, clean-worktree confirmation, and evidence
recording on the selected reviewed `main` heads. Do not create Git tags until
the operator gives a separate tagging instruction after this checklist is
complete.

The current operator publication target is 2026-06-03. Treat that as a
conditional target, not a release claim: `CI-035` proof, package/SBOM/hash
recording, clean-worktree confirmation, and the separate tag instruction must
complete first.

Release freeze is active. No new feature, refactor, UI polish, warning-debt, or
roadmap work enters 0.7.3 RC1; only direct release-gate blockers may be fixed
before tag readiness. The prior documentation-only hold is lifted for release
proof. Continue one gate at a time, record fresh evidence, and do not create
Git tags until the operator gives a separate tagging instruction.

## Gate Revalidation

- [ ] [RELEASE-0.7.3](RELEASE-0.7.3.md) has no open RC-blocking task without
      item-level acceptance.
- [ ] [RELEASE-0.7.3-EXECUTION-PLAN](plans/RELEASE-0.7.3-EXECUTION-PLAN.md)
      has no unaccepted blocking item remaining.
- [ ] Every RC-blocking item doc records the implementation commit,
      validation evidence, and final disposition.
- [ ] Any accepted inconclusive live-network result records the external
      condition that blocked proof.

## Required Campaign Gate

The canonical RC-blocking proof is the quick campaign execution. The rows under
"Campaign Expanded Rows" are the leaf evidence commands that this gate tracks
or executes; keep them visible so failures can be assigned to the correct
phase.

Run `python -m emule_workspace ...` commands from
`$env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build`. Use absolute
`$env:EMULEBB_WORKSPACE_ROOT\...` paths when passing local input files.

- [x] `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3`
- [ ] `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --execute`

`emulebb-0.7.3` is the stable quick campaign ID in `emulebb-build-tests`; RC1
release tags and assets still use `0.7.3-rc.1`.

## Campaign Expanded Rows

- [x] `python -m emule_workspace test certification --profile fast`
- [x] `python -m emule_workspace test live-e2e --profile release-expanded-quick --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`
- [x] `python -m emule_workspace test live-e2e --profile cpu-heavy-quick --fail-fast`
- [x] `python -m emule_workspace test live-e2e --profile stabilization-stress-quick --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`
- [x] `python -m emule_workspace test amutorrent-clean-startup --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [x] `python -m emule_workspace test amutorrent-emulebb-ui --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [x] `python -m emule_workspace test amutorrent-resilience --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [x] `python -m emule_workspace test live-e2e --profile ui-resource-depth --fail-fast`
- [x] `python -m emule_workspace package-release --config Release --platform x64`
- [x] `python -m emule_workspace package-release --config Release --platform ARM64`
- [x] `python -m emule_workspace package-amutorrent --config Release --platform x64`
- [x] `python repos\emulebb-tooling\ci\check-clean-worktree.py`

Run certification with the required local live inputs and Arr roots when those
are needed by the operator environment, for example
`--live-wire-inputs-file`, `--radarr-movie-root`, and `--sonarr-series-root`.
Record certification reports, command summaries, commits, log paths, package
paths, SBOM paths, and SHA-256 hashes in [CI-035](items/CI-035.md).

`package-release` is the package verification gate. It must fail instead of
writing accepted manifests when a ZIP is missing a required runtime/doc file,
does not contain the full stock language DLL set, contains a language DLL for
the wrong architecture, contains source/build/debug artifacts, or cannot record
per-file SHA-256 hashes and SPDX SBOM provenance in the package manifest.

Current state: [CI-035](items/CI-035.md) records 2026-06-05 final current-head
quick RC1 proof on app `abe374dd`, build orchestration `bb432ca`, build-tests
`c8336f5`, tooling `e9d3fc5`, and aMuTorrent `d25452a`. The refreshed fast
certification, `ui-resource-depth`, `controller-surface`,
`release-expanded-quick`, `cpu-heavy-quick`, `stabilization-stress-quick`, and
three aMuTorrent live add-on rows all passed using the operator-provided
`hide.me` bind interface and VPN guard allow list. Final x64, ARM64, and
optional aMuTorrent x64 RC packages were regenerated with
`--release-version 0.7.3-rc.1 --clean`, and [CI-035](items/CI-035.md) records
the final ZIP, diagnostics ZIP, bootstrapper, SBOM, manifest, and provenance
hashes. The tracked clean-worktree audit passed on 2026-06-05.

The literal aggregate command
`python -m emule_workspace test release-campaign --campaign emulebb-0.7.3
--execute` was not rerun after the leaf rows passed; leave that row visible if
the operator wants one more aggregate campaign wrapper invocation. Full
overnight certification and real-profile monitoring are formal
`overnight-full` soak/confidence evidence for failure diagnosis and are not
part of the quick RC1 package gate.

2026-05-14 closeout prep did not run live E2E, regenerate packages, or create
tags. Existing package manifests are rehearsal artifacts from older commits and
must not be used as final release hashes. Recent live reports may be cited as
supporting signal only where [CI-035](items/CI-035.md) classifies them; they do
not complete the required current-head proof rows.

The accepted [FEAT-058](../history/items/FEAT-058.md) closeout copy/audit
polish changed release-facing docs after the previous prep audit. Treat all
final proof rows as pending until rerun on the pushed heads that exist after
that polish lands.

The accepted [FEAT-059](../history/items/FEAT-059.md) tray preference UI polish
also changed the app candidate. Treat all final proof rows as pending until
rerun on the pushed heads that exist after that polish lands.

The accepted [FEAT-060](../history/items/FEAT-060.md) preference inventory and
REST preference metadata hardening also changed the app and build-tests
candidates. Treat all final proof rows as pending until rerun on the pushed
heads that exist after this hardening lands.

The accepted [FEAT-061](../history/items/FEAT-061.md) strong preference schema
validation changed the build-tests candidate. Treat all final proof rows as
pending until rerun on the pushed heads that exist after this schema hardening
lands.

The accepted [FEAT-071](../history/items/FEAT-071.md) filename mojibake repair
changed the app and build-tests candidates. Treat all final proof rows as
pending until rerun on the pushed heads that exist after this filename-intake
hardening lands.

Current remaining queue:

1. Commit this evidence update and rerun the tracked clean-worktree audit.
2. Optionally run the literal aggregate `release-campaign --execute` wrapper if
   the operator wants the campaign wrapper itself to restamp the already-passed
   leaf rows.
3. Annotated RC1 tag was created and pushed after the operator gave the
   separate tag instruction on 2026-06-05.

## Overnight-Full Campaign

These full-duration rows belong to the `emulebb-0.7.3-overnight` campaign.
Run them when diagnosing release-candidate failures or collecting deeper soak
confidence:

- [ ] `python -m emule_workspace test certification --profile overnight`
- [ ] `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3-overnight --execute`
- [ ] `python -m emule_workspace test live-e2e --profile release-expanded --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`
- [ ] `python -m emule_workspace test live-e2e --profile cpu-heavy --fail-fast`
- [ ] `python -m emule_workspace test live-e2e --suite live-process-monitor --fail-fast`
- [ ] `python -m emule_workspace test live-e2e --profile stabilization-stress --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`

The blocking release campaign uses the quick variants plus targeted aMuTorrent
proofs. The `overnight-full` campaign is tracked separately so long-duration
soak status cannot be confused with the repeatable RC package gate.

## Release Identity

- [ ] Release notes use `eMule broadband edition` as the public product name.
- [ ] Release notes use `eMuleBB` as the compact app/mod/API name.
- [ ] Package-facing README identifies reviewed `main` as the 0.7.3 RC1
      release source and does not depend on a broadband stabilization branch.
- [x] Annotated RC tag is `emulebb-v0.7.3-rc.1`.
- [x] Annotated RC tag points at the selected reviewed `main` commit.
- [x] x64 RC asset is `emulebb-0.7.3-rc.1-x64.zip`.
- [x] x64 RC manifest is `emulebb-0.7.3-rc.1-x64.manifest.json`.
- [x] ARM64 RC asset is `emulebb-0.7.3-rc.1-arm64.zip`.
- [x] ARM64 RC manifest is `emulebb-0.7.3-rc.1-arm64.manifest.json`.
- [x] Suite bootstrapper asset is `Bootstrap-eMuleBBSuite.ps1`.
- [x] Suite bootstrapper hash asset is `Bootstrap-eMuleBBSuite.ps1.sha256`.
- [x] Optional aMuTorrent x64 controller asset is
      `emulebb-0.7.3-rc.1-amutorrent-x64.zip`.
- [x] Optional aMuTorrent x64 controller manifest is
      `emulebb-0.7.3-rc.1-amutorrent-x64.manifest.json`.
- [x] Each ZIP contains exactly the full stock language DLL set under
      `eMule\lang`.
- [x] Each ZIP contains package-facing README, release notes, GPL text,
      third-party notices, SPDX SBOM, and REST docs. Legacy web templates are
      frozen baggage and must not be shipped in RC assets.
- [x] Package manifests record the ZIP hash, selected executable hash, expected
      language DLL list/count, SBOM hash, per-file package hashes,
      bootstrapper asset name, bootstrapper SHA-256, and bootstrapper SHA-256
      path.
- [x] Package notes state that ZIPs are not code-signed, contain no debug
      symbols, and do not bundle optional `MediaInfo.dll`.

## Final Operator Steps

- [x] Confirm no active workspace repo has unrelated uncommitted changes.
- [x] Confirm fresh x64 and ARM64 package hashes are recorded in
      [CI-035](items/CI-035.md).
- [x] Confirm fresh x64 and ARM64 package SBOM hashes are recorded in
      [CI-035](items/CI-035.md).
- [x] Confirm the suite bootstrapper SHA-256 is recorded in
      [CI-035](items/CI-035.md).
- [x] Confirm the optional aMuTorrent x64 package hash is recorded in
      [CI-035](items/CI-035.md) if that asset is published.
- [x] Confirm the optional aMuTorrent x64 package SBOM hash is recorded in
      [CI-035](items/CI-035.md) if that asset is published.
- [x] Create the annotated RC tag only after package verification and a
      separate operator instruction.

Tag closure:

- tag: `emulebb-v0.7.3-rc.1`
- target: `abe374dd3378e6a1b292a363f9dfe1ae6f2f74dc`
- tag object: `6f251ec88f72deafa1a32c8df79d6ae9dcaf559b`
- remote: `origin`
