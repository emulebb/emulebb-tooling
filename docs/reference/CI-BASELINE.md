# CI Baseline

`eMule-tooling` owns the shared baseline CI used by the active eMule repos.

## Reusable Workflow

- workflow: `.github/workflows/reusable-baseline.yml`
- stable ref: `ci/v7`

Consumer repos should reference:

- `eMulebb/eMule-tooling/.github/workflows/reusable-baseline.yml@ci/v7`

Do not point long-lived branches at `@main`.

Consumers must pass the same immutable tag as `tooling_ref` so the reusable
workflow executes scripts from the reviewed baseline version.

## Required Checks

Use these status names in branch protection:

- `baseline / baseline (windows-2022)`
- `baseline / baseline (windows-2025-vs2026)`

## Shared Scripts

- `ci/guard-tracked-files.py`
- `ci/check-basic-hygiene.py`

Shared implementation lives in `ci/policy_guards.py`. Consumers call the
hyphenated scripts through the reusable workflow and should not import or copy
the implementation module.

Each consumer repo keeps its own:

- `.github/workflows/baseline.yml`
- `manifests/privacy-guard/policy.v1.json`
