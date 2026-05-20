---
id: FEAT-044
workflow: github
github_issue: https://github.com/eMulebb/eMule/issues/18
title: IP filter input policy - PeerGuardian lists, whitelist, and private-IP exemption
status: OPEN
priority: Minor
category: feature
labels: [ipfilter, security, peerguardian, whitelist, private-ip, emuleai]
milestone: ~
created: 2026-04-26
source: eMuleAI IPFilter comparison and historical mod scan
---


> Workflow status is tracked in GitHub: https://github.com/eMulebb/eMule/issues/18. This local document is retained as an engineering spec/evidence record.

## Summary

Extend the now-safe IP-filter update foundation with optional input-policy
improvements from eMuleAI and historical mods:

- load and merge PeerGuardian `*.p2p` lists from the config directory
- support a static/admin-managed filter overlay
- support a whitelist that overrides blacklist matches
- optionally avoid filtering private/local addresses for lab and LAN use

## Current Main Evidence

Current `eMule-main` has:

- safe manual IP-filter promotion
- `FEAT-042` automatic IP-filter update scheduling
- reload of the running `CIPFilter` instance after successful promotion

It does not yet have `*.p2p` config-directory merge, whitelist override, static
overlay, or a private-IP filtering preference.

## eMuleAI Reference

`analysis\emuleai\srchybrid\IPFilter.cpp/h` includes:

- `LoadP2PFiles()`
- `.p2p` and `guarding.p2p` parsing
- `AddFromFileStatic(...)`
- `AddFromFileWhite(...)`
- `DontFilterPrivateIPs` handling in `IsFiltered(...)`

The eMuleAI code is useful as behavior reference, but should not be copied
wholesale without reconciling `BUG-004` overlap semantics and current safe
promotion helpers.

## Stock/Community Comparison

Stock/community 0.72 remains closer to the single `ipfilter.dat` model. This is
an optional security/operations feature for users who already maintain richer
filter sources.

## Scope Constraints

- build on the safe download/promotion/reload path from `BUG-027` and
  `FEAT-042`
- decide explicit precedence among whitelist, static filter, downloaded filter,
  and manual imports
- preserve the existing disabled-by-default auto-update posture
- do not silently trust bundled external lists; keep sources user-configured
- coordinate with `BUG-004` before claiming full IP-filter correctness

## Acceptance Criteria

- [ ] `*.p2p` parsing is covered by unit tests with PeerGuardian-style samples
- [ ] whitelist precedence is deterministic and documented
- [ ] private/LAN exemption is explicit, persisted, and default-safe
- [ ] malformed or empty inputs cannot clear the live filter
- [ ] live reload semantics match manual and scheduled update paths
