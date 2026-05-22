# eMuleBB Release Test Campaigns

Release campaigns are the operator view of the generic
[Release Test Strategy](RELEASE-TEST-STRATEGY.md). They group feature-flow
scenarios into strict phases and show which current commands provide evidence.

## Reporter

Use the supported workspace entrypoint:

```powershell
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3
```

Useful variants:

```powershell
python -m emule_workspace test release-campaign --template
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --phase live-wire-release
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --json
```

The command is report-only. It reads latest known JSON artifacts when they
exist, shows manual evidence rows where command output/checklist evidence is
authoritative, and warns for missing required evidence.

## Current Instance

`emulebb-0.7.3` is the first populated campaign instance. It maps the current
release gates into feature-flow scenarios across:

- workspace validation and fast certification;
- Kad/eD2K protocol parity, native coverage, community comparison, and
  live-diff;
- REST, aMuTorrent, Prowlarr, Radarr, and Sonarr controller flows;
- release-expanded live-wire UI/REST/download weak-path coverage;
- disposable heavy-profile CPU/memory stress plus real-profile long-run
  live-wire monitoring;
- release language/resource UI depth;
- optional stabilization stress and aMuTorrent resilience add-ons;
- x64 package, ARM64 package, optional aMuTorrent package, clean worktree, and
  hash recording.

Frozen surfaces are excluded from campaign ownership: archive preview/recovery,
IRC and IRC-adjacent chat UI, legacy Scheduler, legacy WebServer HTML templates,
and proxy support receive no support and no release-gated tests. See
[FROZEN-SURFACES](FROZEN-SURFACES.md).

The active release checklist remains the ship authority. The campaign report is
the release-matrix and evidence-status view.

## Local Inputs

Live-wire terms, media titles, direct bootstrap rows, and Arr root paths remain
operator-owned runtime inputs. Do not commit them. Use local files such as
`repos\eMule-build-tests\live-wire-inputs.local.json` and explicit command-line
root arguments.

The real-profile long-run monitor is intentionally separate from generated
heavy fixtures. It uses the ignored
`repos\eMule-build-tests\live-process-monitor.local.json` file for the
operator-owned profile path, HTTPS REST bind, API key, and ProcDump path. Keep
that file local.

## Heavy And Real-Profile Pre-Release Gates

Before final package proof, refresh both stabilization-stress profile rows:

```powershell
python -m emule_workspace test live-e2e --profile cpu-heavy --fail-fast
python -m emule_workspace test live-e2e --suite live-process-monitor --fail-fast
```

The first command proves the throw-away generated heavy Shared Files scenario
with ETW/xperf CPU evidence. The second command launches the real live-wire
profile for at least 30 minutes and records CPU, memory, handle, REST counter,
and delayed spike-dump evidence without committing local paths or titles.
