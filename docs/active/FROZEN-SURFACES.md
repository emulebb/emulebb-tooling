# eMuleBB Frozen Surfaces

This document records product areas that are intentionally frozen in current
`main`. If this document conflicts with older active item wording, this document
wins for current support and test-scope decisions.

## Policy

Frozen surfaces receive no product support, no feature work, no bug-fix
commitment, and no new test coverage. They are not release-gated behavior
surfaces. Existing code may remain only as compile-preserved legacy baggage
through the `0.7.x` legacy support line. Existing incidental tests may be
removed when they stop serving supported behavior.

Preserved does not mean supported. For `0.7.3` and later `0.7.x` **LTSC**
(long-term servicing) maintenance, some frozen legacy code, resource entries,
profile keys, or old menu paths may remain so the release can preserve
compatibility while keeping risk low. That retention is a transition state, not a
promise that the surface will receive fixes, documentation, automation, or release
proof. The `0.7.x` LTSC line keeps this compile-preserved legacy; the removals
below happen only on `0.8.0`/`main`.

`0.8.0` is the explicit frozen-surface removal release. The frozen areas below are
**scheduled** for removal in the `0.8.0` **Lean line** (operator decision
2026-06-24) through their tracked `REF-*` items — see
[MFC-0.8.0-LEAN-REMOVAL-PLAN](plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md) — with proof
focused on supported behavior that shares infrastructure.

Do not add compatibility layers, shims, diagnostics, harnesses, UI automation,
or parser/golden coverage for these surfaces unless the explicit task is to
remove the surface or prove that its removal did not damage supported behavior.
In `0.7.x`, do not fix frozen-surface bugs unless the issue affects supported
shared infrastructure, security, or app stability.

## Frozen Areas

| Area | Current decision |
|---|---|
| Archive preview and archive recovery | Frozen. **Scheduled for removal in `0.8.0`** via `REF-052`. |
| IRC and IRC-adjacent chat UI | Frozen. **Scheduled for removal in `0.8.0`** via `REF-025`. |
| Legacy Scheduler and scheduler preferences | Frozen. **Scheduled for removal in `0.8.0`** via `REF-025`. |
| SMTP/email notifications | Frozen. **Scheduled for removal in `0.8.0`** via `REF-025` (shares the mbedTLS decouple with the TLS removal). |
| SAPI text-to-speech notifications | Frozen. **Scheduled for removal in `0.8.0`** via `REF-025` (operator decision 2026-06-24 supersedes the prior "keep best-effort SAPI" stance). |
| First-run connection wizard | Frozen. **Scheduled for removal in `0.8.0`** via `REF-025`. |
| Legacy splash screen | Frozen. **Scheduled for removal in `0.8.0`** via `REF-025`. Targets the *legacy* splash path only — **not** `LifecycleProgressDlg`, which the `0.8.0` startup slice (`REF-058`) keeps as the startup-progress loader. |
| Legacy WebServer HTML templates and page UI | Frozen. **Scheduled for removal in `0.8.0`** via `REF-043`. The REST listener/routing is kept (see Supported Boundaries). |
| WebServer HTTPS / TLS (mbedTLS) | **Scheduled for removal in `0.8.0`** via `REF-060` (operator decision 2026-06-24): mbedTLS/TF-PSA-crypto is dropped and REST serves **plaintext HTTP, bound to the local control-plane address only**. Supersedes the prior "keep HTTPS/TLS" boundary below. |
| Proxy support | Frozen. **Scheduled for removal in `0.8.0`** via `REF-051` (interleaves with the WSAPoll network-thread port). |
| 3D preview control / id3lib MP3 metadata | **Scheduled for removal in `0.8.0`** (operator decision 2026-06-24), folded into `REF-055`. id3lib goes because **MediaInfo.dll becomes the sole MP3-metadata path**. |
| Sound / WAV event notifications | **Scheduled for removal in `0.8.0`** (operator decision 2026-06-24) via `REF-025`. The `PlaySound` event-alert system + its prefs go; **peer chat is kept** (only the audio alerts are removed). |

SOCKS parser/handshake hardening findings remain intentionally deferred — proxy is
removed, not hardened.

## Supported Boundaries

- REST `/api/v1`, qBittorrent-compatible `/api/v2`, Torznab, aMuTorrent, and
  Arr integrations remain supported where documented by the REST contract and
  release campaigns.
- WebServer listener safety, allowed-IP checks, and REST routing remain supported
  because they carry the controller API. This does not revive the legacy HTML
  template UI. **HTTPS/TLS is no longer supported as of the `0.8.0` Lean line**
  (operator decision 2026-06-24, `REF-060`): REST serves plaintext HTTP and **must
  bind to the local control-plane address only** (`X_LOCAL_IP` / loopback-
  equivalent), never a public or VPN-tunnel interface. On the `0.7.x` LTSC line
  HTTPS/TLS stays as compile-preserved behavior.
- Category behavior remains supported. Scheduler behavior does not.
- Friend/source dialog behavior remains supported where covered separately.
  IRC/chat UI behavior does not. The **IRC** chat is removed in `0.8.0` (`REF-025`);
  the **eD2K peer chat** (`ChatWnd`/`ChatSelector`/`SmileySelector` + `CaptchaGenerator`)
  is **retained-but-unsupported** (operator decision 2026-06-24 keeps it) — kept, not
  removed, but no support/test commitment.
- Native MiniMule behavior is owned by eMuleBB and is not part of the frozen
  legacy MiniMule/IE-host removal bucket.
- PeerCache is already removed; the `0.8.0` Lean line only purges its leftover dead
  `IDS_PEERCACHE_*` resource strings.

## Release Test Rule

Release campaigns must not require evidence for frozen surfaces. Test manifests
may mention them only as explicitly deferred or frozen exclusions. New release
coverage should target supported protocol, persistence, controller, live-wire,
packaging, and resource/localization behavior instead.
