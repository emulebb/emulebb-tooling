# eMule Broadband Edition 0.7.3 Beta Release Runbook

This runbook is procedure only. Use
[RELEASE-0.7.3](RELEASE-0.7.3.md) for current release status and
[RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) for final evidence.

## Preflight

Start from `EMULE_WORKSPACE_ROOT` and keep build/test/package work behind the
supported workspace entrypoint.

```powershell
python -m emule_workspace validate
git -C repos\eMule-tooling status --short --branch
git -C repos\eMule-build status --short --branch
git -C repos\eMule-build-tests status --short --branch
git -C workspaces\workspace\app\eMule-main status --short --branch
git -C workspaces\workspace\app\eMule-main rev-parse --short HEAD
```

Do not continue to tagging if validation fails or if any active repo has
unrelated uncommitted changes.

## Certification Proof

```powershell
python -m emule_workspace test certification --profile fast
```

Then run the full overnight certification gate with the operator-owned live
inputs and Arr-visible roots required by the local environment:

```powershell
python -m emule_workspace test certification --profile overnight `
  --live-wire-inputs-file repos\eMule-build-tests\live-wire-inputs.local.json `
  --radarr-movie-root <radarr-visible-root> `
  --sonarr-series-root <sonarr-visible-root>
```

The certification command records a single aggregate report under
`workspaces\workspace\state\certification\<timestamp>-<profile>\result.json`.
Record that report path and the child report paths it references in
[CI-035](items/CI-035.md).

No release-blocking certification step may fail. A live-network step may be
accepted as inconclusive only when the aggregate and child reports prove the app
and harness behaved correctly and the checklist records the external condition.

## Expanded Weak-Path Gate

Before packaging, run the bounded weak-path live gate with the operator-owned
live-wire inputs:

```powershell
python -m emule_workspace test live-e2e --profile release-expanded --fail-fast `
  --live-wire-inputs-file repos\eMule-build-tests\live-wire-inputs.local.json
```

This profile covers Preferences directory-tree stress, Shared Files,
shared-hash shutdown/recovery, Search UI, shared-directories REST, REST
adversity, cold-start telemetry, local dump/crash smoke, and aMuTorrent browser
smoke. It requires 50 server searches, 50 Kad searches, and 100 successful
paused download triggers. Success means each triggered download is accepted and
materializes in the transfer queue; completion is not required.

## Focused Stabilization Stress

When release proof resumes and the operator wants extra crash, leak, CPU, REST
concurrency, and dump evidence without rerunning the full overnight gate, run:

```powershell
python -m emule_workspace test live-e2e --profile stabilization-stress --fail-fast
```

This profile runs `rest-api`, `rest-cold-start-dump-stress`, and
`local-dumps-crash-smoke` with REST soak stress, socket/TLS adversity, leak
churn, cold-start resource telemetry, download churn, and crash-dump evidence
checks. It is not a substitute for the overnight certification row.

## Packaging

```powershell
python -m emule_workspace package-release --config Release --platform x64
python -m emule_workspace package-release --config Release --platform ARM64
```

Package manifests are written next to the ZIP assets under:

```text
workspaces\workspace\state\release\emule-bb-v0.7.3
```

The release ZIP assets must be named:

```text
eMule-broadband-0.7.3-x64.zip
eMule-broadband-0.7.3-arm64.zip
```

The packaging command is intentionally strict. It builds the selected
architecture, builds the stock language resource DLLs, stages the portable ZIP,
then verifies the package before writing the manifest. Verification covers:

- `emule.exe`, full stock `lang\*.dll` set, `webserver\eMule.tmpl`, package
  README, release notes, GPL text, third-party notices, and REST docs;
- x64 packages containing only x64 PE files and ARM64 packages containing only
  ARM64 PE files for `emule.exe` and language DLLs;
- no source files, project files, debug symbols, intermediates, or build logs in
  the ZIP; and
- manifest fields for ZIP hash, executable hash, expected language DLL
  list/count, and per-file package hashes.

`MediaInfo.dll` remains optional and external. The release ZIPs are not
code-signed and do not include debug symbols.

## Optional aMuTorrent Controller Package

aMuTorrent is packaged separately from the core eMule BB portable ZIPs. The
CI packaging proof is x64-only and verifies that the optional controller ZIP can
be produced without publishing workflow artifacts:

```powershell
python -m emule_workspace package-amutorrent --config Release --platform x64
```

The optional controller assets are written next to the core package assets:

```text
workspaces\workspace\state\release\emule-bb-v0.7.3\eMule-broadband-0.7.3-amutorrent-x64.zip
workspaces\workspace\state\release\emule-bb-v0.7.3\eMule-broadband-0.7.3-amutorrent-x64.manifest.json
```

The aMuTorrent package command requires clean provenance inputs for
`repos\amutorrent`, `repos\eMule-build`, `repos\eMule-build-tests`, and
`repos\eMule-tooling`. It rebuilds frontend assets, installs production server
dependencies, rejects generated runtime state and source maps, and records
package-local runtime policy in the manifest. ARM64 aMuTorrent packaging must
run from a native ARM64 Node environment until a deliberate cross-architecture
native-module build path exists.

## Ship Decision

After the final proof:

- update [CI-035](items/CI-035.md) and
  [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md);
- confirm [RELEASE-0.7.3](RELEASE-0.7.3.md) has no open beta-blocking task
  without item-level acceptance;
- confirm release notes use `eMule broadband edition` and `eMule BB`; and
- create `emule-bb-v0.7.3` only after package verification and a separate
  operator instruction.
