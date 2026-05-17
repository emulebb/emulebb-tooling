# eMule BB Release Test Campaigns

Release campaigns are the operator view of the generic
[Release Test Strategy](RELEASE-TEST-STRATEGY.md). They group feature-flow
scenarios into strict phases and show which current commands provide evidence.

## Reporter

Use the supported workspace entrypoint:

```powershell
python -m emule_workspace test release-campaign --campaign emule-bb-0.7.3
```

Useful variants:

```powershell
python -m emule_workspace test release-campaign --template
python -m emule_workspace test release-campaign --campaign emule-bb-0.7.3 --phase live-wire-release
python -m emule_workspace test release-campaign --campaign emule-bb-0.7.3 --json
```

The command is report-only. It reads latest known JSON artifacts when they
exist, shows manual evidence rows where command output/checklist evidence is
authoritative, and warns for missing required evidence.

## Current Instance

`emule-bb-0.7.3` is the first populated campaign instance. It maps the current
release gates into feature-flow scenarios across:

- workspace validation and fast certification;
- Kad/eD2K protocol parity, native coverage, community comparison, and
  live-diff;
- REST, aMuTorrent, Prowlarr, Radarr, and Sonarr controller flows;
- release-expanded live-wire UI/REST/download weak-path coverage;
- release language/resource UI depth;
- optional stabilization stress and aMuTorrent resilience add-ons;
- x64 package, ARM64 package, optional aMuTorrent package, clean worktree, and
  hash recording.

The active release checklist remains the ship authority. The campaign report is
the release-matrix and evidence-status view.

## Local Inputs

Live-wire terms, media titles, direct bootstrap rows, and Arr root paths remain
operator-owned runtime inputs. Do not commit them. Use local files such as
`repos\eMule-build-tests\live-wire-inputs.local.json` and explicit command-line
root arguments.
