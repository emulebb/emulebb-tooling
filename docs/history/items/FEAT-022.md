---
id: FEAT-022
title: Startup config directory override — `-c` flag for alternate preferences path
status: Done
priority: Minor
category: feature
labels: [startup, config, testing, portability, sysadmin]
milestone: ~
created: 2026-04-10
source: `main` commit `fc70cf9` (`FEAT-028 virtualize and harden shared files list`)
---

## Summary

This feature is merged to `main`.

`eMule-main` now accepts `-c <base-dir>` early in startup and redirects the effective
config, log, and related profile paths below that selected base directory before normal
preference initialization runs.

Although the original backlog reference came from the experimental branch, the mainline
implementation landed as part of the broader shared-files performance and startup-hardening
line in commit `fc70cf9`.

## Landed Mainline Shape

Primary files:

- `srchybrid/StartupConfigOverride.h`
- `srchybrid/Emule.cpp`
- supporting startup/config consumers touched on the same line

Key behavior:

- `-c <path>` is parsed before config initialization
- the effective config directory becomes `<base-dir>\config\`
- the effective log directory becomes `<base-dir>\logs\`
- `preferences.ini`, `known.met`, `sharedcache.dat`, and sibling runtime files follow the
  override
- long-path-safe path handling is preserved on the override path

## Why This Matters

This was a real testing and stability enabler, not just a convenience switch:

- deterministic isolated live profiles for build-tests
- multi-instance or staging configs without touching the user's normal profile
- portable-style runs from explicit base directories
- deep long-path config-root stress coverage without polluting the default profile

## Validation Already In Place

The live test harness now exercises this path directly under long config roots:

- `repos\emulebb-build-tests\scripts\config-stability-ui-e2e.py`
- `repos\emulebb-build-tests\scripts\config-stability-ui-e2e.py`

That suite launches real `emule.exe` instances with explicit `-c`, edits/saves settings,
verifies `preferences.ini` persistence across relaunch, and stresses repeated close/save
cycles under overlong config paths.

## Relationship To Other Items

- complements **FEAT-010** / **BUG-029** long-path work because test and portable profiles
  can now live under deep paths
- complements **CI-008**, which now carries the long-config live UI stability regression
