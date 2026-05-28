---
id: FEAT-096
title: Improve client and network statistics observability
status: OPEN
priority: Minor
category: feature
labels: [statistics, observability, clients, network, rest, ui, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-28
source: user request after reviewing peer client and mod identity visibility
---

# FEAT-096 - Improve Client And Network Statistics Observability

## Summary

Make the Statistics view and local controller surfaces better at explaining the
peer population eMuleBB is actually seeing. The goal is a general observability
improvement, not a client-specific detector.

## Current Evidence

- `CUpDownClient` already stores base client software and an optional advertised
  mod/version string from standard hello and mule-info tags.
- Existing UI paths that use `DbgGetFullClientSoftVer()` can show the combined
  software plus mod display string for individual peers.
- The Statistics tree currently aggregates known clients by broad client family
  such as eMule, aMule, MLdonkey, Shareaza, eM Compat, and unknown.
- REST/client JSON exposure is inconsistent: upload rows include `clientMod`,
  while some source/detail rows only expose base `clientSoftware`.

## Intended Shape

1. Add passive peer-population statistics that separate base client family from
   advertised client/mod identity where the remote peer provides it.
2. Show both current known-client counts and useful session-observed counts when
   the existing lifetime model can support that without retaining unnecessary
   peer objects.
3. Expose consistent `clientSoftware`, `clientMod`, and full display fields on
   local controller surfaces that already serialize peer rows.
4. Keep the Statistics tree readable by showing top mod/client identities plus
   an "other" bucket instead of unbounded dynamic rows.
5. Use the same normalized counting helper for UI and REST so totals do not
   drift between local surfaces.

## Scope Constraints

- Do not add eMuleAI-specific detection or branding to this item.
- Do not fingerprint peers heuristically. Count only protocol-visible metadata
  that the peer already advertises through compatible tags or existing state.
- Do not change eD2K or Kad protocol semantics, packet shapes, tag shapes, or
  advertised capabilities.
- Do not persist raw peer identities unless a separate privacy/storage decision
  explicitly approves that.
- Keep counting work cheap enough for large live client lists; avoid per-refresh
  allocations or expensive locale transforms on hot paths.

## Acceptance Criteria

- [ ] Statistics distinguishes broad client family from advertised client/mod
      identity when mod identity is available.
- [ ] Unknown or hidden mod identity is reported explicitly instead of inferred.
- [ ] REST peer rows expose base software, mod identity, and full display name
      consistently across upload, queue, and download-source surfaces.
- [ ] Top client/mod identity rows are bounded and deterministic, with an
      aggregate "other" row.
- [ ] UI and REST totals are produced by shared logic or covered by parity tests
      that prevent drift.
- [ ] Tests cover empty mod strings, integer `ModID` strings, mixed-case names,
      duplicate identity labels, and peers with no eMule-compatible mod tag.

## Validation

- `python -m emule_workspace validate`
- targeted native tests for the statistics aggregation helper
- REST JSON contract tests for peer software/mod fields
- x64 Debug and Release app builds before implementation commit
