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
- [ ] `python -m emule_workspace test live-e2e --profile release-expanded-quick --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`
- [ ] `python -m emule_workspace test live-e2e --profile cpu-heavy-quick --fail-fast`
- [ ] `python -m emule_workspace test live-e2e --profile stabilization-stress-quick --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`
- [ ] `python -m emule_workspace test amutorrent-clean-startup --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [ ] `python -m emule_workspace test amutorrent-emulebb-ui --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [ ] `python -m emule_workspace test amutorrent-resilience --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [x] `python -m emule_workspace test live-e2e --profile ui-resource-depth --fail-fast`
- [ ] `python -m emule_workspace package-release --config Release --platform x64`
- [ ] `python -m emule_workspace package-release --config Release --platform ARM64`
- [ ] `python -m emule_workspace package-amutorrent --config Release --platform x64`
- [ ] `python repos\emulebb-tooling\ci\check-clean-worktree.py`

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

Current state: non-live build/test rows have partial historical evidence in
[CI-035](items/CI-035.md), [CI-037](../history/items/CI-037.md) records a
passed expanded weak-path live run, [CI-038](../history/items/CI-038.md)
records a passed 2026-05-23 current-head `ui-resource-depth` run for all 43
release languages, and [CI-035](items/CI-035.md) records 2026-06-04 fresh
package, manifest, ZIP SHA-256, and SBOM SHA-256 evidence for x64, ARM64, and
optional aMuTorrent x64 assets. [CI-035](items/CI-035.md) also records the
2026-06-04 installer-controller VM proof passing on clean Win10 and Win11
guests, plus the controlled GitHub smoke workflow extension that adds an ARM64
`windows-11-arm` package/offline command-line smoke lane. GitHub controlled
smoke run `26959062075` passed both the x64 `windows-2022` lane and the ARM64
`windows-11-arm` lane. The canonical quick release-campaign gate still remains
open until
`python -m emule_workspace test release-campaign --campaign emulebb-0.7.3
--execute` passes or the operator explicitly accepts narrower evidence. A
2026-06-04 plan-only audit of
`python -m emule_workspace test release-campaign --campaign emulebb-0.7.3`
completed and reported the expected open gate surface: missing or failed
required evidence remains in controller-surface, live-wire-release,
ui-resource-depth, and stabilization-stress phases, while packaging-provenance
rows are present/passed except the clean-worktree row, which remains manual.
The 2026-05-23 fast certification attempt first stopped on the external `hide.me`
adapter precondition; [CI-035](items/CI-035.md) records that failed report and
the follow-up harness classification commit. After the `hide.me` interface was
restored, `python -m emule_workspace test certification --profile fast` passed
on the selected heads and is recorded in [CI-035](items/CI-035.md). Quick
expanded live-wire proof, quick heavy/stress rows, and aMuTorrent add-on rows
remain incomplete. Full overnight certification and real-profile monitoring
are formal `overnight-full` evidence for confidence and failure diagnosis,
while `emulebb-0.7.3` remains the repeatable RC package gate.

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

Run the remaining queue in this order:

1. Revalidate the active release docs and item dispositions.
2. Run the required campaign command rows above on the selected current app
   `main` head,
   including the quick expanded weak-path live gate, quick disposable heavy and
   stabilization profiles, aMuTorrent add-ons, and `ui-resource-depth`.
3. Rebuild package assets again only if the campaign proof changes the selected
   commit set or the operator requests a final publication refresh.
4. Confirm the 2026-06-04 package paths, manifests, SBOMs, SHA-256 hashes, and
   repo commits recorded in [CI-035](items/CI-035.md) are the intended
   publication inputs.
5. Leave the annotated tag step blocked until the operator gives a separate tag
   instruction.

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
- [ ] Annotated RC tag is `emulebb-v0.7.3-rc.1`.
- [ ] Annotated RC tag points at the selected reviewed `main` commit.
- [ ] x64 RC asset is `emulebb-0.7.3-rc.1-x64.zip`.
- [ ] x64 RC manifest is `emulebb-0.7.3-rc.1-x64.manifest.json`.
- [ ] ARM64 RC asset is `emulebb-0.7.3-rc.1-arm64.zip`.
- [ ] ARM64 RC manifest is `emulebb-0.7.3-rc.1-arm64.manifest.json`.
- [ ] Suite bootstrapper asset is `Bootstrap-eMuleBBSuite.ps1`.
- [ ] Suite bootstrapper hash asset is `Bootstrap-eMuleBBSuite.ps1.sha256`.
- [ ] Optional aMuTorrent x64 controller asset is
      `emulebb-0.7.3-rc.1-amutorrent-x64.zip`.
- [ ] Optional aMuTorrent x64 controller manifest is
      `emulebb-0.7.3-rc.1-amutorrent-x64.manifest.json`.
- [ ] Each ZIP contains exactly the full stock language DLL set under
      `eMule\lang`.
- [ ] Each ZIP contains package-facing README, release notes, GPL text,
      third-party notices, SPDX SBOM, and REST docs. Legacy web templates are
      frozen baggage and must not be shipped in RC assets.
- [ ] Package manifests record the ZIP hash, selected executable hash, expected
      language DLL list/count, SBOM hash, per-file package hashes,
      bootstrapper asset name, bootstrapper SHA-256, and bootstrapper SHA-256
      path.
- [ ] Package notes state that ZIPs are not code-signed, contain no debug
      symbols, and do not bundle optional `MediaInfo.dll`.

## Final Operator Steps

- [ ] Confirm no active workspace repo has unrelated uncommitted changes.
- [ ] Confirm fresh x64 and ARM64 package hashes are recorded in
      [CI-035](items/CI-035.md).
- [ ] Confirm fresh x64 and ARM64 package SBOM hashes are recorded in
      [CI-035](items/CI-035.md).
- [ ] Confirm the suite bootstrapper SHA-256 is recorded in
      [CI-035](items/CI-035.md).
- [ ] Confirm the optional aMuTorrent x64 package hash is recorded in
      [CI-035](items/CI-035.md) if that asset is published.
- [ ] Confirm the optional aMuTorrent x64 package SBOM hash is recorded in
      [CI-035](items/CI-035.md) if that asset is published.
- [ ] Create the annotated RC tag only after package verification and a
      separate operator instruction.
