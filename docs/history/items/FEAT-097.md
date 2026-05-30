---
id: FEAT-097
title: Add connection pressure details to Network Information
status: DONE
priority: Minor
category: feature
labels: [rc1, ui, network, diagnostics]
milestone: 0.7.3-rc.1
created: 2026-05-30
source: operator request for connection count and max in Network Information
---

# FEAT-097 - Add Connection Pressure Details To Network Information

## Summary

The full Network Information dialog now includes a snapshot of connection
pressure so live profiles can expose current socket load against configured
limits without switching to the Statistics tree.

## Implementation

- Increased the full Network Information dialog minimum/opening size from
  800x600 to 900x700.
- Added a full-info-only Connections block with current sockets, max
  connections, half-open sockets, half-open max, completed handshakes, other
  sockets, new-connection burst limit, average, peak, and limit-reached count.
- Kept the dialog snapshot-only; no timer or manual refresh button was added.
- Reused existing localized labels and avoided new release strings.

## Evidence

- `e513d423` `FEAT-097 add connection pressure to network info`

## Validation

- `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
  passed at `20260530T190352Z-build-app`.
- `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`
  passed at `20260530T190451Z-build-app`.
- `python -m emule_workspace validate`
- `python -m emule_workspace test native --config Debug --platform x64 --suite-name parity --build-output-mode ErrorsOnly`
  passed 749 tests.
