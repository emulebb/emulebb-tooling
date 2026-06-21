# eMule Broadband Edition 0.7.3 Release Checklist

This is the operator checklist for the 0.7.3 release train. RC1/RC2 rows are
historical where marked; active rows now target `emulebb-v0.7.3-rc.3` and then
stable `emulebb-v0.7.3`.
Do not record stale proof here; every row must be refreshed on the selected
reviewed `main` commit.

## Proof Status

Final proof resumed by operator direction on 2026-05-17. Run live E2E,
certification, package refresh, clean-worktree confirmation, and evidence
recording on the selected reviewed `main` heads. Do not create Git tags until
the operator gives a separate tagging instruction after this checklist is
complete.

The previous operator publication target has passed. Treat publication as
blocked until `CI-035` proof, package/SBOM/hash recording, clean-worktree
confirmation, successful push of pending build evidence work, and the separate
tag instruction complete.

Release freeze is active. No new feature, refactor, UI polish, warning-debt, or
roadmap work enters RC3/final; only direct release-gate blockers, package/proof
fixes, and release-documentation corrections may land before tag readiness. The
2026-06-19 operator scope decision keeps RC3/final on the existing PowerShell
MFC+aMuTorrent bundle and excludes qBittorrentBB, emulebb-rust, TrackMuleBB,
`uv`, and the Python installer. Continue one gate at a time, record fresh
evidence, and do not create Git tags until the operator gives a separate tagging
instruction.

## Gate Revalidation

- [ ] [RELEASE-0.7.3](RELEASE-0.7.3.md) has no open RC-blocking task without
      item-level acceptance.
- [ ] [RELEASE-0.7.3-EXECUTION-PLAN](plans/RELEASE-0.7.3-EXECUTION-PLAN.md)
      has no unaccepted blocking item remaining.
- [ ] Every RC-blocking item doc records the implementation commit,
      validation evidence, and final disposition.
- [ ] Any accepted inconclusive live-network result records the external
      condition that blocked proof.
- [ ] Pages `install.ps1` is proven to resolve and invoke the GitHub Release
      `Bootstrap-eMuleBBSuite.ps1` asset, with hash-sidecar verification when the
      sidecar exists.
- [ ] qBittorrentBB is absent from RC3/final suite defaults, package proof,
      lifecycle scripts, Pages install claims, and generated release copy.

## Required Campaign Gate

The canonical RC-blocking proof is the quick campaign execution. The rows under
"Campaign Expanded Rows" are the leaf evidence commands that this gate tracks
or executes; keep them visible so failures can be assigned to the correct
phase.

Relaxed gate (operator decision 2026-06-12): for RC candidates the binding
proof is a passing `test certification --profile fast` for the shipped scope.
The live quick-campaign `--execute` row and the live-network expanded rows are
operator-accepted/non-blocking, and `emulebb-rust` preview tests are out of
ship scope. See [CI-035](items/CI-035.md) for the recorded proof. The campaign
report itself is `warn-only`; after the rc.3 reconciliation the campaign's five
binding rows are the Fast certification, the x64/ARM64/aMuTorrent package
gates, and the clean-worktree provenance check.

Final release gate (stable `0.7.3`): the relaxed RC gate does **not** carry
over to the stable tag. For final, raise the bar beyond Fast cert + packaging:

- Run the quick-campaign live rows for real and require them to pass:
  `installer-controller-surface`, `release-expanded-quick`,
  `stabilization-stress-quick` (for the unique `local-dumps-crash-smoke`), and
  the aMuTorrent live trio (`amutorrent-clean-startup` / `-emulebb-ui` /
  `-resilience`), with `--live-wire-inputs-file`.
- Run the `emulebb-0.7.3-overnight` campaign once as soak sign-off (overnight
  certification + `cpu-heavy` + `live-process-monitor`).
- Run at least one Windows-VM matrix smoke on win10+win11 (`package-smoke` and
  `package-helper-install`) to prove the installer on clean OS images.
- `emulebb-rust` stays out of `0.7.x` ship scope (forward `0.8.*` only).

Run `python -m emule_workspace ...` commands from
`$env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build`. Use absolute
`$env:EMULEBB_WORKSPACE_ROOT\...` paths when passing local input files.

- [x] `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3`
- [ ] `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --execute`

`emulebb-0.7.3` is the stable quick campaign ID in `emulebb-build-tests`; RC1
release tags and assets still use `0.7.3-rc.1`.

## Campaign Expanded Rows

- [x] `python -m emule_workspace test certification --profile fast` (2026-06-12, `--test-network offline`; passed shipped scope: `validate` + all build steps; `emulebb-rust` preview failures accepted out of scope)
- [ ] `python -m emule_workspace test live-e2e --profile release-expanded-quick --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`
- [ ] `python -m emule_workspace test live-e2e --profile cpu-heavy-quick --fail-fast`
- [ ] `python -m emule_workspace test live-e2e --profile stabilization-stress-quick --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`
- [ ] `python -m emule_workspace test amutorrent-clean-startup --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [ ] `python -m emule_workspace test amutorrent-emulebb-ui --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [ ] `python -m emule_workspace test amutorrent-resilience --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json --rest-webserver-scheme https --keep-artifacts`
- [x] `python -m emule_workspace test live-e2e --profile ui-resource-depth --fail-fast`
- [x] `python -m emule_workspace package-release --config Release --platform x64`
- [x] `python -m emule_workspace package-release --config Release --platform ARM64`
- [x] `python -m emule_workspace package-amutorrent --config Release --platform x64`
- [ ] `powershell -NoProfile -ExecutionPolicy Bypass -File $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-pages\install.ps1 -DryRun -Bundle Full`
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

Current state: CI is green on current `main` (Nightly 2026-06-21; Controlled
Smoke and RC Package Proof 2026-06-20), and build commit `fb6e286` (VPN Guard
config forwarding through certification) is pushed — `emulebb-build` main is now
`a7e1aa4`. The earlier blockers (the failed 2026-06-05 aggregate quick campaign
and the `WinError 10051` outbound-network outage) are resolved. The default quick
campaign plans 18 commands: Hyper-V VM proof is on-demand/nonblocking, and the
long-running `live-process-monitor` is isolated behind
`installer-controller-surface-soak`. The RC3 candidate heads are identified in
the [RC3 changelog](RELEASE-0.7.3-RC3-CHANGELOG.md); they still need a fresh
certification and package refresh before tag.

The next required aggregate command is:

```powershell
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --execute --test-network all --continue-on-failure `
  --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json `
  --vpn-guard-live-config $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\vpn-guard-live.local.json
```

Full overnight certification and real-profile monitoring are formal
`overnight-full` soak/confidence evidence for failure diagnosis and are not
part of the quick RC1 package gate.

Proof rows are head-sensitive: treat every proof row as pending a rerun on the
locked RC3 candidate heads. Older package manifests are rehearsal artifacts and
must not be reused as final release hashes; recent live reports are supporting
signal only where [CI-035](items/CI-035.md) classifies them. (The rc.2-era
proof-invalidation notes for FEAT-058/059/060/061/071 are now historical — those
features shipped in rc.2.)

Current remaining queue:

1. Lock the RC3 candidate heads (operator) — see the
   [RC3 changelog](RELEASE-0.7.3-RC3-CHANGELOG.md).
2. Run `test certification --profile fast` on the locked heads (binding
   relaxed-gate proof) and record the result in [CI-035](items/CI-035.md).
3. Regenerate the x64/ARM64/diagnostics (and optional aMuTorrent x64) packages
   and record SHA-256 + SBOM hashes in [CI-035](items/CI-035.md).
4. Run the Pages `install.ps1` dry-run wrapper proof.
5. Rerun the tracked clean-worktree audit.
6. Finalize the RC3 changelog (heads, package names, hashes, accepted
   deviations).
7. Wait for the separate operator tag instruction.

## Overnight-Full Campaign

These full-duration rows belong to the `emulebb-0.7.3-overnight` campaign.
Run them when diagnosing release-candidate failures or collecting deeper soak
confidence:

- [ ] `python -m emule_workspace test certification --profile overnight`
- [ ] `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3-overnight --execute`
- [ ] `python -m emule_workspace test live-e2e --profile release-expanded --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`
- [ ] `python -m emule_workspace test live-e2e --profile cpu-heavy --fail-fast`
- [ ] `python -m emule_workspace test live-e2e --profile installer-controller-surface-soak --fail-fast`
- [ ] `python -m emule_workspace test live-e2e --profile stabilization-stress --fail-fast --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json`

The blocking release campaign uses the quick variants plus targeted aMuTorrent
proofs. The `overnight-full` campaign is tracked separately so long-duration
soak status cannot be confused with the repeatable RC package gate.

## Release Identity

- [ ] Release notes use `eMule broadband edition` as the public product name.
- [ ] Release notes use `eMuleBB` as the compact app/mod/API name.
- [ ] RC2 release notes are refreshed only after the operator gives the RC2 go.
- [ ] RC2 changelog is maintained during RC2 preparation as
      `RELEASE-0.7.3-RC2-CHANGELOG.md` and finalized at RC2 go.
- [ ] RC2 changelog includes a separate RC1-vs-stock/community-baseline section
      with the RC1 release date from the GitHub release record.
- [ ] Package-facing README identifies reviewed `main` as the 0.7.3 RC1
      release source and does not depend on a broadband stabilization branch.
- [ ] Annotated RC tag is `emulebb-v0.7.3-rc.1`.
- [ ] Annotated RC tag points at the selected reviewed `main` commit.
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
- [x] qBittorrentBB is not an RC3/final asset.
- [x] emulebb-rust, TrackMuleBB, `uv`, and the Python setup CLI are not
      RC3/final assets.
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

- [ ] Confirm no active workspace repo has unrelated uncommitted changes.
- [ ] Confirm fresh x64 and ARM64 package hashes are recorded in
      [CI-035](items/CI-035.md).
- [ ] Confirm fresh x64 and ARM64 package SBOM hashes are recorded in
      [CI-035](items/CI-035.md).
- [x] Confirm the suite bootstrapper SHA-256 is recorded in
      [CI-035](items/CI-035.md).
- [ ] Confirm the optional aMuTorrent x64 package hash is recorded in
      [CI-035](items/CI-035.md) if that asset is published.
- [ ] Confirm the optional aMuTorrent x64 package SBOM hash is recorded in
      [CI-035](items/CI-035.md) if that asset is published.
- [ ] Confirm release artifacts include or link the active candidate release
      notes and changelog before tag approval.
- [ ] Create the annotated RC tag only after package verification and a
      separate operator instruction.

Tag closure: not started. Wait for separate operator confirmation before
creating or pushing any tag.
