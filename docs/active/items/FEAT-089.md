---
id: FEAT-089
title: Add in-app guided Prowlarr indexer setup for eMuleBB
status: OPEN
priority: Minor
category: feature
labels: [ui, rest, torznab, prowlarr, controllers, setup]
milestone: post-0.7.3
created: 2026-05-25
source: operator request for easier Prowlarr indexer setup
---

## Summary

Make it easy for users to add eMuleBB as a Prowlarr indexer from the product UI
without manually assembling the Torznab URL, API path, API key, and category
choices.

The current adapter surface already supports Prowlarr through Generic Torznab at
`/indexer/emulebb/api`. This item is about discoverability, validation, and
operator ergonomics, not a new wire protocol.

## Current Implemented State

Current docs and packages already provide a script-based setup path:

- [Stack Integration Guide](../../reference/GUIDE-STACK-INTEGRATIONS.md)
  documents the manual Generic Torznab fields and the package helper scripts.
- `register-prowlarr.ps1` creates or updates a Prowlarr Generic Torznab indexer
  named `eMuleBB`.
- `register-arr-stack.ps1` can add Radarr/Sonarr qBittorrent-compatible
  download clients and optionally register Prowlarr application sync.
- The helper scripts request controller credentials at runtime and do not store
  Prowlarr, Radarr, or Sonarr credentials in eMuleBB preferences.

The remaining backlog value is an in-app guided surface, copy actions, and a
local health/test affordance.

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

Avoid writing real Prowlarr credentials into eMuleBB preferences. The existing
package helper scripts require explicit controller URLs and API keys at runtime
and avoid storing those controller credentials in eMuleBB preferences.

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

- [x] A user can view the exact eMuleBB Prowlarr Generic Torznab fields from
      product documentation.
- [ ] A user can copy or view the exact eMuleBB Prowlarr Generic Torznab fields
      from product UI.
- [x] The setup guidance explains base URL, API path, API key, and category
      choices.
- [ ] A local health check proves the Torznab caps endpoint responds before the
      user configures Prowlarr.
- [ ] Secrets are redacted in logs, reports, and any generated setup payload.
- [ ] Existing Prowlarr live tests continue to pass with the documented setup.
