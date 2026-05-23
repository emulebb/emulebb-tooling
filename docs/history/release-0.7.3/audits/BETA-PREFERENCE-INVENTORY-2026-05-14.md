# Beta 0.7.3 Preference Inventory Audit

Date: 2026-05-14

Scope: `Preferences.cpp` `CIni` key references, native REST mutable preference
mapping, route body schema coverage, request validation, and release proof
impact.

## Result

The audit found 420 distinct `CIni` key references after stripping comments.
They are now tracked in
`repos\emulebb-build-tests\manifests\preference-inventory.v1.json` and guarded by
`tests\python\test_preference_inventory.py`.

No preference key was renamed. No migration was introduced. No default value was
changed.

## Notable Classifications

- `DownSessionCompletedFiles`: write-only session statistic in
  `statistics.ini`.
- `VideoPreviewThumbnails`: disabled/tombstone write; runtime loading forces
  thumbnails disabled.
- `LogErrorColor`, `LogWarningColor`, `LogSuccessColor`: read-only
  legacy/customization keys in `Preferences.cpp`.
- `UpdateQueueListPref`: read-only legacy key.
- Dynamic families: statistics color rows and list-control setup keys are
  guarded as generated families rather than expanded into every concrete key.

## REST Preferences

The native REST mutable preference list is centralized in
`WebApiSurfaceSeams::GetMutablePreferenceSpecs()`. The same metadata now feeds:

- `ParseMutablePreferenceName`;
- PATCH `/app/preferences` route body field inventory;
- seam-side PATCH body validation.

The implementation keeps the public `/api/v1/app/preferences` field names and
accepted ranges unchanged.

## Proof Impact

This is release hardening, not a runtime behavior change. It resets the
candidate heads for final proof because app and build-test commits changed
after the previous closeout state.

Fresh final proof and package hashes remain owned by `CI-035`.
