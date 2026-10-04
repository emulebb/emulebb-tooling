# emulebb-mfc Agent Policy

Read the [Workspace Policy](../../../WORKSPACE-POLICY.md) first. This annex is
mandatory for `emulebb-main`, MFC maintenance, C++ app builds,
resources/localization, and MFC releases.

## Lifecycle And Source

- eMuleBB MFC is the Windows `eMule broadband edition` fork. Its active source
  is `workspaces\workspace\app\emulebb-main`; `repos\emulebb` is a detached
  branch-store anchor at `origin/main`, not an edit location.
- `main` is the integration and bounded maintenance branch. The `0.7.x` line
  accepts compatibility-preserving, low-risk fixes and bounded UX, performance,
  build, packaging, documentation, diagnostics, and release improvements. It
  must not add new subsystems, broad controller/API capability, protocol
  expansion, or architectural modernization.
- No MFC `0.8.x` lane is active. Frozen unsupported surfaces remain unsupported
  unless shared infrastructure, security, or stability is affected.
- Release stabilization uses `release/MAJOR.MINOR.PATCH`. Do not start routine
  work there. Backport applicable fixes to `main`; one-off stable patches branch
  from the latest stable tag when needed.
- The first post-community commit remains the global source-encoding
  normalization commit. Put changes at the earliest layer where they are true.

## Compatibility And Build

- Preserve stock/community eMule eD2K/Kad semantics and default behavior.
  Protocol-adjacent changes need explicit parity evidence.
- Build, validation, tests, and packaging use `repos\emulebb-build` and
  `python -m emule_workspace`. Do not invoke MSBuild directly from the app or
  tests tree.
- Every app code change rebuilds `Debug|x64`, `Release|x64`, and diagnostics
  `Release|x64` before commit. The active C++ baseline is C++17 with MSVC
  `v143`. `v145` is probe-only, not a release baseline.

```powershell
python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly
python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly
python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly --diagnostics
```

- The active matrix has no Win32. Build support is x64 and ARM64; shared test
  execution remains x64-only. Toolset probes flow through orchestration rather
  than hardcoded project changes.
- Debug uses `RuntimeLibrary=MultiThreadedDebug`,
  `Optimization=Disabled`, `IncrementalLink=true` for executables, and
  `DebugInformationFormat=ProgramDatabase`. Release uses
  `RuntimeLibrary=MultiThreaded`, speed optimization,
  `FunctionLevelLinking=true`, `IntrinsicFunctions=true` where applicable,
  `IncrementalLink=false`, and
  `LinkTimeCodeGeneration=UseLinkTimeCodeGeneration`. Active compiled targets
  use `BufferSecurityCheck=true` and `MultiProcessorCompilation=true` where
  structurally applicable.

## Naming And Release

- Public name: `eMule broadband edition`. Compact app/mod/API name: `eMuleBB`.
  Organization and URL slug: `emulebb`.
- `0.7.3` is the first stable release after the fixed `0.7.3-rc.1` through
  `0.7.3-rc.3` train. Later stable maintenance starts at `emulebb-v0.7.4`;
  prereleases use explicit suffixes such as `0.7.5-rc.1` or `0.7.5-beta.1`.
  Superseded `1.0.0`, `1.0.1`, and `1.1.1` are evidence/rehearsal labels only.
- Stable tags use `emulebb-vMAJOR.MINOR.PATCH`; prerelease tags use
  `emulebb-vMAJOR.MINOR.PATCH-rc.N` or
  `emulebb-vMAJOR.MINOR.PATCH-beta.N`. Tags are annotated and require separate
  operator approval after release proof.
- ZIPs use `emulebb-MAJOR.MINOR.PATCH[-rc.N|-beta.N]-ARCH.zip` and
  `emulebb-MAJOR.MINOR.PATCH[-rc.N|-beta.N]-diagnostics-ARCH.zip`.
  Executables remain `emulebb.exe` and `emulebb-diagnostics.exe` without
  embedded versions.
- Runtime artifact renames are strict unless compatibility aliases are
  explicitly requested. New runs use UTC `YYYYMMDDTHHMMSSZ` ids and the
  canonical `build-result.json`, `certification-result.json`,
  `release-campaign-run-result.json`, and suite result/summary names.
- Each published release from `0.7.3-rc.2` has version-specific release notes
  and a power-user changelog describing operational changes, compatibility,
  packaging/controllers, diagnostics, defaults, risks, and migration/testing
  notes. Finalize it only with release approval. The `0.7.3-rc.2` changelog
  retains a distinct RC1-versus-community-baseline section and RC1 release date.

## Runtime Artifact Names

- Logs remain `emulebb.log`, `emulebb-verbose.log`,
  `emulebb-crt-debug.log`, `emulebb-startup-errors.log`,
  `emulebb-diagnostics-packet.log`,
  `emulebb-diagnostics-upload-slot.log`,
  `emulebb-diagnostics-download-slot.log`,
  `emulebb-diagnostics-bad-peer.log`, `emulebb-diagnostics-kad.log`,
  `emulebb-diagnostics-diag.log`,
  `emulebb-diagnostics-startup.trace.json`, `emulebb-performance.csv`,
  `emulebb-performance.mrtg`, `emulebb-performance-data.mrtg`, and
  `emulebb-performance-overhead.mrtg`.
- Rotated logs insert `-YYYYMMDD-HHMMSS` before the extension. Dumps use
  `emulebb-dump-YYYYMMDD-HHMMSS-pid<PID>-mini|full.dmp` and
  `emulebb-crash-YYYYMMDD-HHMMSS-pid<PID>.dmp`.
- Test suites publish timestamped run directories plus `<suite>\latest` and
  `<suite>-result.json`, `<suite>-result.partial.json`, and
  `<suite>-summary.json` leaves.

## Localization

- Every stock `srchybrid\lang\*.rc` file is a supported release language.
  `helpers\rc-release-languages.json` enumerates exactly that set.
- New release-facing strings land in `srchybrid\emule.rc` and every stock
  language before proof. Preserve existing community translations unless a
  targeted correction is requested; never mass-retranslate them.
- New eMuleBB labels need meaningful reviewed translations. External or
  historical translation engines are not authoritative.
- Use `helpers\rc-string-table.py`,
  `helpers\rc-localization-preflight.py`,
  `helpers\rc-translate-missing.py`,
  `helpers\rc-release-localization-layout.json`, and
  `helpers\rc-release-localization-ignored-ids.txt`. Every new English
  `IDS_*` row is classified as required or ignored. Mechanical edits are keyed
  by resource id and must not modify unrelated labels. Do not run concurrent
  `.rc` writes.

## Live Path Scope

For mixed-client harness rules, read the
[Harness And Live Policy](../../../reference/HARNESS-LIVE-POLICY.md).
Community/baseline/aMule clients remain short-path. Deep-path and folder-mounted
VHD scenarios are eMuleBB-only.
