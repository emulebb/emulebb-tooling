# eMuleBB Release Test Campaigns

Release campaigns are the operator view of the generic
[Release Test Strategy](RELEASE-TEST-STRATEGY.md). They group feature-flow
scenarios into strict phases and show which current commands provide evidence.

## Reporter And Executor

Use the supported workspace entrypoint:

```powershell
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3
```

Useful variants:

```powershell
python -m emule_workspace test release-campaign --template
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --phase live-wire-release
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --json
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3 --execute
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3-overnight --execute
```

Without `--execute`, the command reads latest known JSON artifacts when they
exist, shows manual evidence rows where command output/checklist evidence is
authoritative, and warns for missing required evidence. With `--execute`, it
runs the selected campaign's blocking commands in manifest order.

Pass operator-owned runtime inputs at execution time rather than committing
them into manifests:

```powershell
python -m emule_workspace test release-campaign --campaign emulebb-0.7.3-overnight --execute `
  --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json `
  --radarr-movie-root <radarr-visible-root> `
  --sonarr-series-root <sonarr-visible-root>
```

## Current Instance

`emulebb-0.7.3` is the RC-blocking quick campaign. It maps the current release
gates into feature-flow scenarios across:

- workspace validation and fast certification;
- Kad/eD2K protocol parity, native coverage, community comparison, and
  live-diff;
- REST, aMuTorrent, Prowlarr, Radarr, and Sonarr controller flows;
- quick release-expanded live-wire UI/REST/download weak-path coverage;
- quick disposable heavy-profile CPU/memory stress;
- release language/resource UI depth;
- quick stabilization stress and targeted aMuTorrent add-ons;
- x64 package, ARM64 package, optional aMuTorrent package, clean worktree, and
  hash recording.

`emulebb-0.7.3-overnight` is the full overnight campaign. It is deliberately
longer and runs:

- full `certification --profile overnight`;
- full generated `cpu-heavy` live E2E;
- real-profile `live-process-monitor` using the ignored local monitor config.

Frozen surfaces are excluded from campaign ownership: archive preview/recovery,
IRC and IRC-adjacent chat UI, legacy Scheduler, legacy WebServer HTML templates,
and proxy support receive no support and no release-gated tests. See
[FROZEN-SURFACES](FROZEN-SURFACES.md).

The active release checklist remains the ship authority. The campaign report is
the release-matrix and evidence-status view.

Post-`0.7.3` p2p-overlord product-family campaigns should build on the same
campaign base in `repos\emulebb-build-tests` with product-specific variants for
Rust agents, backend coordinator checks, long-run monitoring, and claimed REST
subset conformance.

## Local Inputs

Live-wire terms, media titles, direct bootstrap rows, and Arr root paths remain
operator-owned runtime inputs. Do not commit them. Use local files such as
`repos\emulebb-build-tests\live-wire-inputs.local.json` and explicit command-line
root arguments.

The real-profile long-run monitor is intentionally separate from generated
heavy fixtures. It uses the ignored
`repos\emulebb-build-tests\live-process-monitor.local.json` file for the
operator-owned profile path, HTTPS REST bind, API key, and ProcDump path. Keep
that file local.

## Heavy And Real-Profile Campaigns

The quick RC campaign uses bounded stress gates:

```powershell
python -m emule_workspace test live-e2e --profile cpu-heavy-quick --fail-fast
python -m emule_workspace test live-e2e --profile stabilization-stress-quick --fail-fast `
  --live-wire-inputs-file repos\emulebb-build-tests\live-wire-inputs.local.json
```

The overnight campaign uses full soak gates:

```powershell
python -m emule_workspace test certification --profile overnight
python -m emule_workspace test live-e2e --profile cpu-heavy --fail-fast
python -m emule_workspace test live-e2e --suite live-process-monitor --fail-fast
```

The real monitor launches the operator-owned live-wire profile for at least 30
minutes and records CPU, memory, handle, REST counter, and delayed spike-dump
evidence without committing local paths or titles.
