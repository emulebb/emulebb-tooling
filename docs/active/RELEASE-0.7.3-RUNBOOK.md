# eMule Broadband Edition 0.7.3 Release Runbook

This runbook is procedure only. Use
[RELEASE-0.7.3](RELEASE-0.7.3.md) for current release status and
[RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) for final evidence.

Version tokens in the paths and asset names below are placeholders for the
release being prepared. Stable `0.7.3` is published; use
[RELEASE-0.7.3](RELEASE-0.7.3.md) for the current shipped state before reusing
this runbook for patch maintenance.

For stable `0.7.3` and the `0.7.x` support line, the release scope is the
existing PowerShell MFC+aMuTorrent suite. Do not add qBittorrentBB,
emulebb-rust, TrackMuleBB, `uv`, or Python setup assets to the package/proof
flow.

## Preflight

Run build, test, and package commands from the build orchestrator checkout so
`python -m emule_workspace` resolves the local module. Use absolute
`EMULEBB_WORKSPACE_ROOT` paths for cross-repo status and local input files.

```powershell
cd $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build
python -m emule_workspace validate
git -C $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling status --short --branch
git -C $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build status --short --branch
git -C $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests status --short --branch
git -C $env:EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main status --short --branch
git -C $env:EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main rev-parse --short HEAD
```

Do not continue to tagging if validation fails or if any active repo has
unrelated uncommitted changes.

Before package proof, verify the public Pages wrapper parses and forwards to the
release bootstrapper path:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-pages\install.ps1 -DryRun -Bundle Full
```

Show the release campaign matrix before running proof so missing evidence and
local input requirements are visible:

```powershell
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3
```

`emulebb-0.7.3` is the stable quick campaign ID in `emulebb-build-tests`; it is
not the RC tag or package name.

## Repeatable Build Matrix

Use these commands when refreshing build evidence. Do not substitute direct
MSBuild commands for the workspace entrypoint.

Developer Debug x64:

```powershell
python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly
```

Output contract:
`workspaces\workspace\app\emulebb-main\srchybrid\x64\Debug`. Startup profiling
is compiled by `_DEBUG`.

Developer Release x64:

```powershell
python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly
```

Output contract:
`workspaces\workspace\app\emulebb-main\srchybrid\x64\Release`. Startup
profiling is compile-time opt-in and is enabled in the diagnostics package, not
by a runtime environment variable.

Package Release x64:

```powershell
python -m emule_workspace package-release --config Release --platform x64 --clean
```

Output contract:
`workspaces\workspace\state\package-build\emulebb-v0.7.3-<rc>\x64`.
The packaged binary must not contain startup diagnostics support.

Package Release ARM64:

```powershell
python -m emule_workspace package-release --config Release --platform ARM64 --clean
```

Output contract:
`workspaces\workspace\state\package-build\emulebb-v0.7.3-<rc>\arm64`.
The packaged binary must not contain startup diagnostics support.

`package-release` stages ZIP contents under
`workspaces\workspace\state\release\emulebb-v0.7.3-<rc>\staging\<arch>` and writes
the final ZIP, manifest, SBOM, standalone suite bootstrapper, and bootstrapper
SHA-256 file next to that staging directory. Package app outputs are
intentionally separate from developer app outputs so profiling builds cannot be
reused for release ZIPs.

## Certification Proof

```powershell
python -m emule_workspace test certification --profile fast
```

The quick RC campaign is the repeatable blocking package gate. It uses bounded
quick profiles plus targeted controller/aMuTorrent proof so RC packaging can be
refreshed without a full soak each time:

```powershell
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --execute
```

The full overnight certification gate remains available and intentionally uses
the full `release-expanded`, `stabilization-stress`, and aMuTorrent lanes. Run
it with the operator-owned live inputs and Arr-visible roots when collecting
long-form soak proof:

```powershell
python -m emule_workspace test certification --profile overnight `
  --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json `
  --radarr-movie-root <radarr-visible-root> `
  --sonarr-series-root <sonarr-visible-root>
```

For the production overnight campaign, run the first-class campaign wrapper so
the full certification, full generated CPU-heavy stress, and real-profile
monitor are tracked as one proof set:

```powershell
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3-overnight --execute `
  --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json `
  --radarr-movie-root <radarr-visible-root> `
  --sonarr-series-root <sonarr-visible-root>
```

The certification command records a single aggregate report under
`workspaces\workspace\state\certification\<timestamp>-<profile>\certification-result.json`.
Record that report path and the child report paths it references in
[CI-035](../history/items/CI-035.md).

No release-blocking campaign step may fail. A live-network step may be accepted
as inconclusive only when the aggregate and child reports prove the app and
harness behaved correctly and the checklist records the external condition.

## Expanded Weak-Path Gate

Before packaging, the RC campaign runs the bounded weak-path live gate with the
operator-owned live-wire inputs:

```powershell
python -m emule_workspace test live-e2e --profile release-expanded-quick --fail-fast `
  --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json
```

This profile covers Preferences directory-tree stress, Shared Files,
shared-hash shutdown/recovery, Search UI, shared-directories REST, REST
adversity, cold-start telemetry, local dump/crash smoke, and representative
volume/profile cases. The full `release-expanded` profile belongs to the
`overnight-full` proof tier.

## Focused Stabilization Stress

When release proof resumes, refresh the quick generated heavy-profile gate:

```powershell
python -m emule_workspace test live-e2e --profile cpu-heavy-quick --fail-fast
```

This uses throw-away generated Shared Files stress data and ETW/xperf sampling.
It must not depend on operator media paths.

The full generated-heavy profile and real live-wire profile monitor are
long-form `overnight-full` proof:

```powershell
python -m emule_workspace test live-e2e --profile cpu-heavy --fail-fast
python -m emule_workspace test live-e2e --suite live-process-monitor --fail-fast
```

This reads ignored local settings from
`repos\emulebb-build-tests\live-process-monitor.local.json`. The local file must
point at the operator-owned real profile and corrected HTTPS REST bind, and the
run must remain at or above the 1800-second minimum.

For blocking crash, leak, REST concurrency, and dump evidence, the RC campaign
uses the quick stress profile:

```powershell
python -m emule_workspace test live-e2e --profile stabilization-stress-quick --fail-fast `
  --live-wire-inputs-file $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests\live-wire-inputs.local.json
```

The full `stabilization-stress` profile keeps the deeper REST soak stress,
socket/TLS adversity, leak churn, cold-start resource telemetry, download
churn, and crash-dump evidence checks for the `overnight-full` proof tier.

## Packaging

```powershell
python -m emule_workspace package-release --config Release --platform x64 --clean
python -m emule_workspace package-release --config Release --platform ARM64 --clean
```

Package manifests are written next to the ZIP assets under:

```text
workspaces\workspace\state\release\emulebb-v0.7.3-<rc>
```

The release publication assets must be named:

```text
Bootstrap-eMuleBBSuite.ps1
Bootstrap-eMuleBBSuite.ps1.sha256
emulebb-0.7.3-<rc>-x64.zip
emulebb-0.7.3-<rc>-x64.manifest.json
emulebb-0.7.3-<rc>-x64.sbom.spdx.json
emulebb-0.7.3-<rc>-arm64.zip
emulebb-0.7.3-<rc>-arm64.manifest.json
emulebb-0.7.3-<rc>-arm64.sbom.spdx.json
```

No qBittorrentBB, emulebb-rust, TrackMuleBB, `uv`, or Python setup asset belongs
in the stable `0.7.3` or `0.7.x` publication set.

The packaging command is intentionally strict. It builds the selected
architecture into the package-only app output root, builds the stock language
resource DLLs, stages the portable ZIP, then verifies the package before
writing the manifest. Verification covers:

- `emulebb.exe` in the standard package, `emulebb-diagnostics.exe` in the
  diagnostics package, full stock `lang\*.dll` set, package README, release
  notes, release changelog link or payload, GPL text, third-party notices,
  SBOM, and REST docs;
- diagnostics package executable contains startup, packet, upload-slot,
  download-slot, and bad-peer diagnostics support;
- absence of the legacy template-based `webserver` payload in RC assets;
- x64 packages containing only x64 PE files and ARM64 packages containing only
  ARM64 PE files for the selected eMuleBB executable and language DLLs;
- standard release package `emulebb.exe` not containing startup diagnostics support;
- no source files, project files, debug symbols, intermediates, or build logs in
  the ZIP; and
- manifest fields for ZIP hash, executable hash, expected language DLL
  list/count, per-file package hashes, bootstrapper asset name, bootstrapper
  SHA-256, and bootstrapper SHA-256 path.

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
workspaces\workspace\state\release\emulebb-v0.7.3-<rc>\emulebb-0.7.3-<rc>-amutorrent-x64.zip
workspaces\workspace\state\release\emulebb-v0.7.3-<rc>\emulebb-0.7.3-<rc>-amutorrent-x64.manifest.json
```

The aMuTorrent package command requires clean provenance inputs for
`repos\amutorrent`, `repos\emulebb-build`, `repos\emulebb-build-tests`, and
`repos\emulebb-tooling`. It rebuilds frontend assets, installs production server
dependencies, rejects generated runtime state and source maps, and records
package-local runtime policy in the manifest. ARM64 aMuTorrent packaging must
run from a native ARM64 Node environment until a deliberate cross-architecture
native-module build path exists.

## Public Pages Wrapper

For stable `0.7.3` and `0.7.x`, `https://emulebb.github.io/install.ps1` is a
wrapper around the GitHub Release `Bootstrap-eMuleBBSuite.ps1` asset. It should
select the requested `-Version` when provided, otherwise the newest non-draft,
non-nightly stable release; verify `Bootstrap-eMuleBBSuite.ps1.sha256` when that
sidecar is present; and pass the existing bootstrapper parameters through
unchanged.

The wrapper must not download `uv`, fetch TrackMuleBB, read a TrackMuleBB suite
manifest, or install qBittorrentBB.

## Ship Decision

After the final proof:

- update [CI-035](../history/items/CI-035.md) and
  [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md);
- confirm [RELEASE-0.7.3](RELEASE-0.7.3.md) has no open RC-blocking task
  without item-level acceptance;
- confirm release notes use `eMule broadband edition` and `eMuleBB`;
- before the operator gives the go for the active RC, maintain that
  candidate's `RELEASE-0.7.3-RC<N>-CHANGELOG.md`; at RC go, finalize its RC
  delta and the separate RC1-vs-stock/community-baseline section, including the
  RC1 release date from the GitHub release record; and
- create the active candidate tag only after package verification and a
  separate operator instruction.
