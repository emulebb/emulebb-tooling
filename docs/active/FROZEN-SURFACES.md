# eMuleBB Frozen Surfaces

This document records product areas that are intentionally frozen in current
`main`. If this document conflicts with older active item wording, this document
wins for current support and test-scope decisions.

## Policy

Frozen surfaces receive no product support, no feature work, no bug-fix
commitment, and no new test coverage. They are not release-gated behavior
surfaces. Existing code may remain only as compile-preserved legacy baggage
until a removal pass deletes it. Existing incidental tests may be removed when
they stop serving supported behavior.

Preserved does not mean supported. For 0.7.3, some frozen legacy code, resource
entries, profile keys, or old menu paths may remain so the release can preserve
compatibility while keeping risk low. That retention is a transition state, not
a promise that the surface will receive fixes, documentation, automation, or
release proof. Future releases may remove or replace frozen surfaces through
explicit roadmap or refactor items.

Do not add compatibility layers, shims, diagnostics, harnesses, UI automation,
or parser/golden coverage for these surfaces unless the explicit task is to
remove the surface or prove that its removal did not damage supported behavior.

## Frozen Areas

| Area | Current decision |
|---|---|
| Archive preview and archive recovery | Frozen. No support and no tests. Candidate for deletion. |
| IRC and IRC-adjacent chat UI | Frozen. No support and no tests. Candidate for deletion through `REF-025`. |
| Legacy Scheduler and scheduler preferences | Frozen. No support and no tests. Candidate for deletion through `REF-025`. |
| SMTP/email notifications | Frozen. No support and no tests. Candidate for deletion through `REF-025`. |
| SAPI text-to-speech notifications | Frozen. No feature work and no tests. Keep only best-effort compile/runtime compatibility with installed Windows SAPI. |
| First-run connection wizard | Frozen. No support and no tests. Candidate for deletion through `REF-025`. |
| Splash screen | Frozen. No support and no tests. Candidate for deletion through `REF-025`. |
| Legacy WebServer HTML templates and page UI | Frozen. No support and no tests. The supported surface is JSON REST and controller adapters only. |
| Proxy support | Frozen. No support and no tests. Candidate for later deletion or replacement. |

Proxy support remains frozen. SOCKS parser/handshake hardening findings are
intentionally deferred while this surface remains unsupported.

## Supported Boundaries

- REST `/api/v1`, qBittorrent-compatible `/api/v2`, Torznab, aMuTorrent, and
  Arr integrations remain supported where documented by the REST contract and
  release campaigns.
- WebServer listener safety, HTTPS/TLS, allowed-IP checks, and REST routing
  remain supported because they carry the controller API. This does not revive
  the legacy HTML template UI.
- Category behavior remains supported. Scheduler behavior does not.
- Friend/source dialog behavior remains supported where covered separately.
  IRC/chat UI behavior does not.
- Native MiniMule behavior is owned by eMuleBB and is not part of the frozen
  legacy MiniMule/IE-host removal bucket.

## Release Test Rule

Release campaigns must not require evidence for frozen surfaces. Test manifests
may mention them only as explicitly deferred or frozen exclusions. New release
coverage should target supported protocol, persistence, controller, live-wire,
packaging, and resource/localization behavior instead.
