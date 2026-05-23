# eMule Broadband Edition 0.7.3 RC Release Runbook

This runbook is procedure only. Use
[RELEASE-0.7.3](RELEASE-0.7.3.md) for current release status and
[RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) for final evidence.

## Preflight

Start from `EMULE_WORKSPACE_ROOT` and keep build/test/package work behind the
supported workspace entrypoint.

```powershell
python -m emule_workspace validate
git -C repos\emulebb-tooling status --short --branch
git -C repos\emulebb-build status --short --branch
git -C repos\emulebb-build-tests status --short --branch
git -C workspaces\workspace\app\emulebb-main status --short --branch
git -C workspaces\workspace\app\emulebb-main rev-parse --short HEAD
```

Do not continue to tagging if validation fails or if any active repo has
unrelated uncommitted changes.

Show the release campaign matrix before running proof so missing evidence and
local input requirements are visible:

```powershell
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3
```

## Repeatable Build Matrix

Use these rows when refreshing build evidence. Do not substitute direct
MSBuild commands for the workspace entrypoint.

| Purpose | Command | Output contract |
|---|---|---|
| Developer Debug x64 | `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly` | `workspaces\workspace\app\emulebb-main\srchybrid\x64\Debug`; startup profiling is compiled by `_DEBUG`. |
| Developer Release x64 | `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly` | `workspaces\workspace\app\emulebb-main\srchybrid\x64\Release`; startup profiling is compiled in and runtime-gated by `EMULE_STARTUP_PROFILE`. |
| Package Release x64 | `python -m emule_workspace package-release --config Release --platform x64 --clean` | app binary/intermediates under `workspaces\workspace\state\package-build\emulebb-v0.7.3-rc.1\x64`; packaged binary must not contain startup profiling support. |
| Package Release ARM64 | `python -m emule_workspace package-release --config Release --platform ARM64 --clean` | app binary/intermediates under `workspaces\workspace\state\package-build\emulebb-v0.7.3-rc.1\arm64`; packaged binary must not contain startup profiling support. |

`package-release` stages ZIP contents under
`workspaces\workspace\state\release\emulebb-v0.7.3-rc.1\staging\<arch>` and writes
the final ZIP, manifest, and SBOM next to that staging directory. Package app
outputs are intentionally separate from developer app outputs so profiling
builds cannot be reused for release ZIPs.

## Certification Proof

```powershell
python -m emule_workspace test certification --profile fast
```

Then run the full overnight certification gate with the operator-owned live
inputs and Arr-visible roots required by the local environment:

```powershell
python -m emule_workspace test certification --profile overnight `
  --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json `
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
  --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json
```

This profile covers Preferences directory-tree stress, Shared Files,
shared-hash shutdown/recovery, Search UI, shared-directories REST, REST
adversity, cold-start telemetry, local dump/crash smoke, and aMuTorrent browser
smoke. It requires 50 server searches, 50 Kad searches, and 100 successful
paused download triggers. Success means each triggered download is accepted and
materializes in the transfer queue; completion is not required.

## Focused Stabilization Stress

When release proof resumes, refresh the generated heavy-profile gate before the
real-profile gate:

```powershell
python -m emule_workspace test live-e2e --profile cpu-heavy --fail-fast
```

This uses throw-away generated Shared Files stress data and ETW/xperf sampling.
It must not depend on operator media paths.

Then run the real live-wire profile monitor:

```powershell
python -m emule_workspace test live-e2e --suite live-process-monitor --fail-fast
```

This reads ignored local settings from
`repos\emulebb-build-tests\live-process-monitor.local.json`. The local file must
point at the operator-owned real profile and corrected HTTPS REST bind, and the
run must remain at or above the 1800-second minimum.

For extra crash, leak, CPU, REST concurrency, and dump evidence without
rerunning the full overnight gate, run:

```powershell
python -m emule_workspace test live-e2e --profile stabilization-stress --fail-fast
```

This profile runs `rest-api`, `rest-cold-start-dump-stress`, and
`local-dumps-crash-smoke` with REST soak stress, socket/TLS adversity, leak
churn, cold-start resource telemetry, download churn, and crash-dump evidence
checks. It is not a substitute for the overnight certification row or for the
separate generated-heavy and real-profile monitor rows above.

## Packaging

```powershell
python -m emule_workspace package-release --config Release --platform x64 --clean
python -m emule_workspace package-release --config Release --platform ARM64 --clean
```

Package manifests are written next to the ZIP assets under:

```text
workspaces\workspace\state\release\emulebb-v0.7.3-rc.1
```

The release ZIP assets must be named:

```text
emulebb-0.7.3-rc.1-x64.zip
emulebb-0.7.3-rc.1-arm64.zip
```

The packaging command is intentionally strict. It builds the selected
architecture into the package-only app output root, builds the stock language
resource DLLs, stages the portable ZIP, then verifies the package before
writing the manifest. Verification covers:

- `emulebb.exe`, full stock `lang\*.dll` set, package README, release notes,
  GPL text, third-party notices, SBOM, and REST docs;
- absence of the legacy template-based `webserver` payload in RC assets;
- x64 packages containing only x64 PE files and ARM64 packages containing only
  ARM64 PE files for `emulebb.exe` and language DLLs;
- release package `emulebb.exe` not containing startup profiling support;
- no source files, project files, debug symbols, intermediates, or build logs in
  the ZIP; and
- manifest fields for ZIP hash, executable hash, expected language DLL
  list/count, and per-file package hashes.

`MediaInfo.dll` remains optional and external. The release ZIPs are not
code-signed and do not include debug symbols.

## Optional aMuTorrent Controller Package

aMuTorrent is packaged separately from the core eMuleBB portable ZIPs. The
CI packaging proof is x64-only and verifies that the optional controller ZIP can
be produced without publishing workflow artifacts:

```powershell
python -m emule_workspace package-amutorrent --config Release --platform x64
```

The optional controller assets are written next to the core package assets:

```text
workspaces\workspace\state\release\emulebb-v0.7.3-rc.1\emulebb-0.7.3-rc.1-amutorrent-x64.zip
workspaces\workspace\state\release\emulebb-v0.7.3-rc.1\emulebb-0.7.3-rc.1-amutorrent-x64.manifest.json
```

The aMuTorrent package command requires clean provenance inputs for
`repos\amutorrent`, `repos\emulebb-build`, `repos\emulebb-build-tests`, and
`repos\emulebb-tooling`. It rebuilds frontend assets, installs production server
dependencies, rejects generated runtime state and source maps, and records
package-local runtime policy in the manifest. ARM64 aMuTorrent packaging must
run from a native ARM64 Node environment until a deliberate cross-architecture
native-module build path exists.

## Ship Decision

After the final proof:

- update [CI-035](items/CI-035.md) and
  [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md);
- confirm [RELEASE-0.7.3](RELEASE-0.7.3.md) has no open RC-blocking task
  without item-level acceptance;
- confirm release notes use `eMule broadband edition` and `eMuleBB`; and
- create `emulebb-v0.7.3-rc.1` only after package verification and a separate
  operator instruction.
