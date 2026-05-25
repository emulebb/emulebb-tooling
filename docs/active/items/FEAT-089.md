---
id: FEAT-089
title: Add guided Prowlarr indexer setup for eMuleBB
status: OPEN
priority: Minor
category: feature
labels: [ui, rest, torznab, prowlarr, controllers, setup]
milestone: post-0.7.3
created: 2026-05-25
source: operator request for easier Prowlarr indexer setup
---

## Summary

Make it easy for users to add eMuleBB as a Prowlarr indexer without manually
assembling the Torznab URL, API path, API key, and category choices.

The current adapter surface already supports Prowlarr through Generic Torznab at
`/indexer/emulebb/api`. This item is about discoverability, validation, and
operator ergonomics, not a new wire protocol.

## Current Manual Setup

Prowlarr can be configured today with a Generic Torznab indexer:

- base URL: `http://HOST:PORT/indexer/emulebb`
- API path: `/api`
- API key: the configured eMuleBB REST/Web API key
- categories:
  - `2000` for movies/video
  - `5000` for TV/video
  - `7000` for documents/general live validation

HTTPS works when Prowlarr trusts the certificate or the operator explicitly uses
Prowlarr's local disposable certificate policy for a private test setup.

## Proposed Shape

Add one or more operator-facing conveniences:

- a Copy Prowlarr Torznab URL action in the REST/Web settings page
- a compact setup text block that shows base URL, API path, and key source
- a health/test action that probes `/indexer/emulebb/api?t=caps`
- an optional API endpoint that returns a Prowlarr-ready setup payload with
  redacted secrets by default
- documentation in the Controllers and REST guide with screenshots or exact
  fields

Avoid writing real Prowlarr credentials into eMuleBB preferences. If an
automation helper is added later, it should require an explicit Prowlarr URL and
API key at runtime and should avoid storing them by default.

## Scope Constraints

- Do not replace the existing Torznab adapter contract.
- Do not make Prowlarr mandatory for native REST, qBit-compatible, or Torznab
  operation.
- Do not add a permanent dependency on Prowlarr APIs inside the core eMule
  runtime.
- Do not log API keys or exact live-wire search terms.
- Keep Radarr/Sonarr sync behavior owned by Prowlarr and the Arr apps; eMuleBB
  should provide a correct indexer endpoint and setup guidance.

## Acceptance Criteria

- [ ] A user can copy or view the exact eMuleBB Prowlarr Generic Torznab fields
      from product documentation or UI.
- [ ] The setup guidance explains base URL, API path, API key, and category
      choices.
- [ ] A local health check proves the Torznab caps endpoint responds before the
      user configures Prowlarr.
- [ ] Secrets are redacted in logs, reports, and any generated setup payload.
- [ ] Existing Prowlarr live tests continue to pass with the documented setup.
