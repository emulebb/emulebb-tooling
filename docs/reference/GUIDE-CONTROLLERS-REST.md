# Controllers And REST Guide

This guide explains how eMule BB should be used with trusted local controllers,
automation, and compatibility adapters.

## REST Is The Preferred Controller Path

eMule BB exposes JSON REST under `/api/v1` through the embedded WebServer
listener. REST is the preferred automation surface. The legacy template web UI
is separate compatibility behavior and should be enabled only when needed.

Contract references:

- [REST API contract](../rest/REST-API-CONTRACT.md)
- [OpenAPI contract](../rest/REST-API-OPENAPI.yaml)
- [Adapter contracts](../rest/REST-API-ADAPTERS.md)

## Trust Model

REST is for trusted local or controlled-network automation.

Use:

- API key authentication with `X-API-Key`
- deliberate bind address and port
- firewall rules matching the exposure policy
- a controlled network path
- redacted diagnostics when sharing support data

Do not expose REST broadly on untrusted networks.

## WebServer HTTPS And Certificates

REST uses the embedded WebServer listener. HTTPS therefore follows WebServer
certificate settings:

- `UseHTTPS` enables HTTPS behavior.
- `HTTPSCertificate` points to the certificate file.
- `HTTPSKey` points to the private-key file.
- `BindAddr`, `Port`, `AllowedIPs`, and firewall policy still control exposure.

The app can generate a WebServer certificate from the command line:

```powershell
emule.exe --generate-webserver-cert --cert webserver.crt --key webserver.key --host localhost --host 127.0.0.1
```

Generate certificates deliberately, store private keys with the profile or
operator-owned secret material, and keep controller API keys out of shared
logs. HTTPS does not make broad untrusted-network exposure safe by itself.

## Native Behavior Remains Authoritative

Controllers must preserve eMule semantics:

- search network choice matters
- categories matter
- paused vs started adds matter
- delete and cancel operations are meaningful and potentially destructive
- completed files and incomplete parts are different resources
- source, fake, trust, comment, and category data should not be discarded
- local path ownership belongs to the native profile

When a controller presents eMule BB as a generic download client, the adapter
must still map back to native behavior correctly.

## Preference Mutation

REST exposes a curated mutable subset of preferences. It is intentionally not a
general `preferences.ini` editor.

Rules:

- use `GET /api/v1/app/preferences` to read the REST preference subset
- use `PATCH /api/v1/app/preferences` only for documented mutable fields
- unsupported names are rejected
- out-of-range values are rejected
- exact mutable field names are documented in OpenAPI and summarized in
  [Preferences Guide](GUIDE-PREFERENCES.md)

Direct config-file edits are a separate maintenance path, not REST behavior.

## aMuTorrent

aMuTorrent integration uses native REST and adapter behavior. Prove the basics
before running long workflows:

- app status reads correctly
- preferences read correctly
- search dispatch works
- add/download flow reaches eMule BB
- upload and queue data remain meaningful when consumed
- typed error envelopes are handled

If browser/UI tests fail, compare aMuTorrent assumptions with the current
OpenAPI contract and live REST smoke evidence.

aMuTorrent should treat the desktop app as the authority. It may present a
modern controller workflow, but category, search, transfer, shared-file,
upload-queue, and lifecycle semantics still come from native eMule BB state.

## Arr, qBit, And Torznab Adapters

Adapter surfaces let Arr-family tools, qBittorrent-compatible workflows, and
Torznab consumers talk to eMule BB. These are compatibility layers, not the
native contract.

Expectations:

- native `/api/v1` remains authoritative
- qBit-compatible actions preserve eMule delete/category semantics
- Torznab search family mapping resolves to supported native search types
- adapter errors remain typed and predictable
- adapter routes should not invent behavior the native app cannot represent

## Lifecycle

REST has lifecycle restrictions. During startup and shutdown, unsafe operations
can be rejected to protect native app state.

Controllers should:

- handle lifecycle errors as retry/stop conditions
- avoid hammering during startup
- stop mutating after shutdown begins
- tolerate temporary unavailability during profile or listener changes

## Legacy WebServer

The legacy WebServer template UI can still be useful for compatibility. It is
not the default automation surface.

REST should remain useful even when legacy templates are absent. Enable legacy
HTML UI explicitly only when you need it.

## Diagnostics

For controller failures, collect:

- route, method, status code, and response body
- whether the route exists in OpenAPI
- app lifecycle state
- WebServer enabled/bind/port settings
- API key configuration
- recent REST and app logs
- redacted diagnostic snapshot

## Troubleshooting

REST unavailable:

1. Confirm WebServer/REST is enabled.
2. Check bind address and port.
3. Check firewall and allowed IP policy.
4. Confirm the app is not starting or shutting down.

Auth failure:

1. Confirm the current API key.
2. Confirm the `X-API-Key` header is sent.
3. Check whether the profile regenerated an empty/missing key.

Route or schema failure:

1. Compare the route with OpenAPI.
2. Check field casing exactly.
3. Remove unsupported aliases.
4. Confirm adapter mapping is not using stale qBit/Torznab assumptions.
