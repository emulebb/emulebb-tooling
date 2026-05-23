---
id: FEAT-032
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/13
title: NAT mapping modernization — lease controls, status visibility, and PCP/NAT-PMP
status: DEFERRED
priority: Minor
category: feature
labels: [networking, upnp, nat-pmp, pcp, miniupnp, preferences]
milestone: ~
created: 2026-04-20
source: 2026-04-20 UPnP robustness review plus PCP/NAT-PMP dependency follow-through
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/13. This local document is retained as an engineering spec/evidence record.

## Summary

Current `main` historically carried two UPnP codepaths:

- `miniupnpc` for `UPnP IGD`
- legacy Windows-service/COM discovery and mapping in `UPnPImplWinServ`

That mixed stack is noisy and hard to reason about in practice. Typical logs
show MiniUPnP finding a valid IGD, then an unrelated Windows-service fallback
failure that does not help the operator understand what actually happened.

`FEAT-032` modernizes the NAT-mapping stack by:

- keeping `miniupnpc` as the `UPnP IGD` backend
- removing the legacy Windows-service/COM backend
- adding `libpcpnatpmp` as a second protocol-family backend for `PCP` /
  `NAT-PMP`
- exposing a new Tweaks backend-mode selector

This item also owns the next UPnP/NAT-mapping usability slice:

- allow an operator-configurable mapping lease time instead of relying only on
  backend defaults or hard-coded request lifetimes
- expose the current NAT-mapping status in a human-readable form, including
  backend/protocol selected, local endpoint, requested external endpoint,
  actual mapped external endpoint, lease duration, expiry/renewal deadline,
  last renewal result, delete-on-exit state, and last error
- keep P2P TCP, P2P UDP/Kad, and WebServer mappings separately visible because
  they can succeed, fail, expire, or be disabled independently
- record mapping conflicts and router substitutions, especially when the
  router accepts a mapping but chooses a different external port
- surface status consistently through logs, diagnostics, and the native UI; add
  REST exposure only as a diagnostic/status surface, not as a new controller
  feature family
- make renewal and teardown behavior explicit, including what happens when a
  lease expires, a network interface changes, the bind target changes, or
  `CloseUPnPOnExit` is enabled

## Beta 0.7.3 Classification

**Release Candidate.** The code/build slice is already complete, so beta
`0.7.3` should take the live NAT validation if the available network can prove
it cleanly. Do not block `emulebb-v0.7.3` solely because the local network
cannot provide a PCP/NAT-PMP-capable path.

## Execution Plan

Historical release context: [Beta 0.7.3 NAT Mapping execution plan](../../history/release-0.7.3/RELEASE-0.7.3-NAT-MAPPING-EXECUTION-PLAN.md).

## Acceptance Criteria

- [x] `UPnPImplWinServ` removed from the app build
- [x] `miniupnpc` remains the `UPnP IGD` backend
- [x] `libpcpnatpmp` is linked into the supported app build
- [x] Tweaks exposes `Automatic` / `UPnP IGD only` / `PCP/NAT-PMP only`
- [x] native tests cover `Automatic` as UPnP IGD first, then PCP/NAT-PMP
- [x] WinServ-only active prefs are removed from runtime behavior
- [x] supported `emulebb-build` app builds pass for active architectures
- [ ] live-network NAT-mapping validation completed on current `main`
- [ ] preference-backed lease time exists with bounded validation and a clear
      default that preserves current behavior
- [ ] UI and diagnostic output can list active and failed NAT mappings with
      backend, protocol, internal/external endpoints, lease, expiry/renewal,
      and last-error state
- [ ] P2P TCP, P2P UDP/Kad, and WebServer mapping states are reported
      independently
- [ ] router-selected external-port substitutions and mapping conflicts are
      visible to the operator
- [ ] renewal, interface-change, bind-change, disable, and exit-teardown paths
      are covered by focused tests or lab/live evidence
- [ ] native tests cover lease bounds, status formatting, renewal scheduling,
      and backend-specific result normalization
- [ ] product docs explain lease-time tradeoffs and how to interpret UPnP,
      PCP, and NAT-PMP status

## Beta 0.7.3 Decision

Deferred for beta `0.7.3` live proof. The code/build slice is accepted by the
release plan, but available release validation must not block the beta tag
solely on the absence of a PCP/NAT-PMP-capable network. Complete the remaining
live proof when a suitable router or lab network can exercise MiniUPnP success,
PCP/NAT-PMP fallback, explicit PCP/NAT-PMP-only mode, and WebServer TCP mapping.
