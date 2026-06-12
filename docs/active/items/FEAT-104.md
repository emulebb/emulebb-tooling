---
id: FEAT-104
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/118
title: Add optional reverse DNS peer name resolution
status: OPEN
priority: Minor
category: feature
labels: [diagnostics, dns, peer-ui, privacy, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-02
source: operator request to consider resolving peer IP addresses to names
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/118. This local document is retained as an engineering spec/evidence record.

# FEAT-104 - Add optional reverse DNS peer name resolution

## Summary

Add an optional reverse DNS resolver for peer IP addresses so diagnostics and
selected UI surfaces can show a hostname/PTR name next to the raw IP address
when the lookup is cheap, available, and privacy-acceptable.

This must be a diagnostics convenience, not a core identity or policy input.
Peer IP address, user hash, client ID, and protocol state remain authoritative.

## Intended Shape

- Resolve IP addresses through a background worker queue, never synchronously
  from paint, sort, log formatting, connection handling, startup, or shutdown
  hot paths.
- Cache positive and negative lookup results with bounded size and expiry.
- Bound concurrency and lookup rate so high peer churn cannot flood DNS.
- Show raw IP immediately, then append or expose the resolved name only after a
  completed lookup.
- Make the feature opt-in or diagnostics/verbose-only by default because
  reverse DNS queries disclose peer IPs to the configured resolver.

## Scope Constraints

- Do not use resolved names for ban, trust, scoring, routing, source selection,
  upload scheduling, Kad, eD2K server, or protocol decisions.
- Do not block UI interaction, list rendering, sorting, upload/download paths,
  connection establishment, shutdown, or live-test flows on DNS.
- Do not retry failed lookups aggressively.
- Do not treat absent, generic, or changing PTR names as an error.
- Do not replace existing geolocation or raw-IP display; names are supplemental.

## Candidate Implementation Notes

- Prefer a small resolver service with:
  - queue dedupe by IP address
  - positive and negative TTLs
  - a low worker count, for example two to four concurrent lookups
  - cancellation/drain behavior that does not delay shutdown
- Expose a formatting helper such as `FormatPeerAddressWithName(IP)` so list
  controls can opt in without owning resolver details.
- Start with one low-risk surface, such as a details dialog or verbose
  diagnostic view, before adding names to high-volume lists.
- Consider config defaults that keep the resolver disabled unless the operator
  explicitly enables peer-name diagnostics.

## Acceptance Criteria

- [ ] Reverse DNS is optional and disabled or diagnostics-only by default.
- [ ] Lookups run asynchronously and never block UI, networking, startup, or
      shutdown hot paths.
- [ ] Positive and negative results are cached with bounded memory and expiry.
- [ ] Lookup concurrency and rate are bounded.
- [ ] Raw IP display remains available and authoritative on every surface.
- [ ] Resolved names are never used for protocol, routing, trust, scoring, ban,
      upload scheduling, or source-selection behavior.
- [ ] Privacy implications are documented in the setting or diagnostics docs.
- [ ] Focused tests cover cache hits, negative cache behavior, queue dedupe,
      disabled-mode behavior, and stale/expired entries.

## Validation

- focused native tests for resolver cache and queue policy
- manual diagnostics smoke with enabled and disabled resolver modes
- x64 Debug and Release app builds before implementation commit
