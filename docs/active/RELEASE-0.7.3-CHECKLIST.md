# eMule Broadband Edition 0.7.3 Beta Release Checklist

This is the final operator checklist for beta target `emule-bb-v0.7.3`.
Do not record stale proof here; every row must be refreshed on the selected
reviewed `main` commit.

## Proof Status

Final proof resumed by operator direction on 2026-05-17. Run live E2E,
certification, package refresh, clean-worktree confirmation, and evidence
recording on the selected reviewed `main` heads. Do not create Git tags until
the operator gives a separate tagging instruction after this checklist is
complete.

Release freeze is active. No new feature, refactor, UI polish, warning-debt, or
roadmap work enters beta `0.7.3`; only direct release-gate blockers may be fixed
before tag readiness. The current closure pass is documentation-only by operator
direction: do not run eMule tests or edit eMule test/harness files until the
operator lifts that hold. All command rows below remain pending unless they are
rerun and recorded after the hold.

## Gate Revalidation

- [ ] [RELEASE-0.7.3](RELEASE-0.7.3.md) has no open beta-blocking task without
      item-level acceptance.
- [ ] [RELEASE-0.7.3-EXECUTION-PLAN](plans/RELEASE-0.7.3-EXECUTION-PLAN.md)
      has no unaccepted blocking item remaining.
- [ ] Every beta-blocking item doc records the implementation commit,
      validation evidence, and final disposition.
- [ ] Any accepted inconclusive live-network result records the external
      condition that blocked proof.

## Required Commands

- [ ] `python -m emule_workspace test release-campaign --campaign emule-bb-0.7.3`
- [ ] `python -m emule_workspace test certification --profile fast`
- [ ] `python -m emule_workspace test certification --profile overnight`
- [ ] `python -m emule_workspace test live-e2e --profile release-expanded --fail-fast --live-wire-inputs-file repos\eMule-build-tests\live-wire-inputs.local.json`
- [ ] `python -m emule_workspace test live-e2e --profile ui-resource-depth --fail-fast`
- [ ] `python -m emule_workspace package-release --config Release --platform x64`
- [ ] `python -m emule_workspace package-release --config Release --platform ARM64`
- [ ] `python -m emule_workspace package-amutorrent --config Release --platform x64`
- [ ] `python repos\eMule-tooling\ci\check-clean-worktree.py`

Run certification with the required local live inputs and Arr roots when those
are needed by the operator environment, for example
`--live-wire-inputs-file`, `--radarr-movie-root`, and `--sonarr-series-root`.
Record certification reports, command summaries, commits, log paths, package
paths, and SHA-256 hashes in [CI-035](items/CI-035.md).

`package-release` is the package verification gate. It must fail instead of
writing accepted manifests when a ZIP is missing a required runtime/doc file,
does not contain the full stock language DLL set, contains a language DLL for
the wrong architecture, contains source/build/debug artifacts, or cannot record
per-file SHA-256 hashes in the package manifest.

Current state: non-live build/test rows have partial historical evidence in
[CI-035](items/CI-035.md), [CI-037](../history/items/CI-037.md) records a passed expanded
weak-path live run, and [CI-035](items/CI-035.md) records 2026-05-17 non-UI
package evidence for x64, ARM64, and optional aMuTorrent x64 assets. `CI-038`
and final certification proof remain incomplete until rerun and recorded on the
selected heads.

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

Run the remaining queue in this order:

1. Revalidate the active release docs and item dispositions.
2. Run the required command rows above on the selected current app `main` head,
   including the expanded weak-path live gate and `ui-resource-depth`.
3. Regenerate x64, ARM64, and optional aMuTorrent x64 packages only after proof
   succeeds.
4. Record fresh package paths, manifests, SHA-256 hashes, and repo commits in
   [CI-035](items/CI-035.md).
5. Leave the annotated tag step blocked until the operator gives a separate tag
   instruction.

## Stabilization Add-On

This focused add-on remains available for diagnosing a certification failure
without rerunning the full overnight gate:

- [ ] `python -m emule_workspace test live-e2e --profile stabilization-stress --fail-fast`

This add-on does not replace the required overnight certification row above.

## Release Identity

- [ ] Release notes use `eMule broadband edition` as the public product name.
- [ ] Release notes use `eMule BB` as the compact app/mod/API name.
- [ ] Package-facing README identifies reviewed `main` as the beta `0.7.3`
      release source and does not depend on a broadband stabilization branch.
- [ ] Annotated beta tag is `emule-bb-v0.7.3`.
- [ ] Annotated beta tag points at the selected reviewed `main` commit.
- [ ] x64 beta asset is `eMule-broadband-0.7.3-x64.zip`.
- [ ] ARM64 beta asset is `eMule-broadband-0.7.3-arm64.zip`.
- [ ] Optional aMuTorrent x64 controller asset is
      `eMule-broadband-0.7.3-amutorrent-x64.zip`.
- [ ] Each ZIP contains exactly the full stock language DLL set under
      `eMule\lang`.
- [ ] Each ZIP contains package-facing README, release notes, GPL text,
      third-party notices, and REST docs. Legacy web templates are frozen
      baggage and are not required release assets.
- [ ] Package manifests record the ZIP hash, `emule.exe` hash, expected
      language DLL list/count, and per-file package hashes.
- [ ] Package notes state that ZIPs are not code-signed, contain no debug
      symbols, and do not bundle optional `MediaInfo.dll`.

## Final Operator Steps

- [ ] Confirm no active workspace repo has unrelated uncommitted changes.
- [ ] Confirm fresh x64 and ARM64 package hashes are recorded in
      [CI-035](items/CI-035.md).
- [ ] Confirm the optional aMuTorrent x64 package hash is recorded in
      [CI-035](items/CI-035.md) if that asset is published.
- [ ] Create the annotated beta tag only after package verification and a
      separate operator instruction.
