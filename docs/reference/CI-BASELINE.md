# CI Baseline

`emulebb-tooling` owns the shared baseline CI used by the active eMule repos.

## Reusable Workflow

- workflow: `.github/workflows/reusable-baseline.yml`
- stable ref: `ci/v8`

Consumer repos should reference:

- `emulebb/emulebb-tooling/.github/workflows/reusable-baseline.yml@ci/v8`

Do not point long-lived branches at `@main`.

Consumers must pass the same immutable tag as `tooling_ref` so the reusable
workflow executes scripts from the reviewed baseline version.

## Required Checks

Use these status names in branch protection:

- `baseline / baseline (windows-2022)`
- `baseline / baseline (windows-2025-vs2026)`

## Forward Toolset Probe

The app repo also carries `VS2026 v145 Probe` as an explicit
`workflow_dispatch` compatibility check. It runs on `windows-2025-vs2026`,
sets `EMULEBB_VS_PLATFORM_TOOLSET=v145`, sets the CMake generator to
`Visual Studio 18 2026`, and builds Release x64 dependencies plus the Release
x64 main app.

This workflow is intentionally a probe, not a required release gate. The active
workspace toolset baseline remains `v143`; `v145` is used to find compiler,
STL, linker, Visual Studio generator, and dependency-wrapper drift before the
project is ready to move the official release baseline.

The probe result must be read from the uploaded `v145-probe/result.json`, not
only from the GitHub workflow conclusion. The wrapper may complete successfully
while preserving a failed native build result for inspection.

Do not add local Hyper-V test paths to GitHub. Hyper-V remains local-only unless
the workspace policy is updated by a separate operator decision.

Microsoft documents the practical compatibility boundary for `v143` and `v145`
under the Visual Studio 2015-2026 MSVC binary-compatibility rules: mixed
objects and libraries are allowed only when the final linker is at least as new
as the newest input, the installed Visual C++ Redistributable is at least as
new as the newest toolset used, and `/GL` or `/LTCG` inputs must be compiled
and linked with exactly the same toolset version. See
<https://learn.microsoft.com/en-us/cpp/porting/binary-compat-2015-2017> and
<https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist>.

## Shared Scripts

- `ci/guard-tracked-files.py`
- `ci/check-basic-hygiene.py`

Shared implementation lives in `ci/policy_guards.py`. Consumers call the
hyphenated scripts through the reusable workflow and should not import or copy
the implementation module.

Each consumer repo keeps its own:

- `.github/workflows/baseline.yml`
- `manifests/privacy-guard/policy.v1.json`
