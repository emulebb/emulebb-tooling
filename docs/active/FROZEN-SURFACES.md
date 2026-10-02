# eMuleBB MFC Frozen Surfaces

This document records legacy MFC areas that are intentionally outside the
supported `0.7.x` maintenance surface. If older plans or item text conflict
with this document, this document controls current support decisions.

## Policy

Frozen surfaces receive no routine feature work, bug-fix commitment, new test
coverage, or release gate. Existing code may remain to preserve compatibility
and keep maintenance risk low. A change is justified only when a frozen area
affects supported shared infrastructure, security, data integrity, buildability,
or application stability.

The former `0.8.0` removal program is not active. Its deletion proposals remain
available in the
[parked lean-removal design](../ideas/IDEA-MFC-0.8.0-LEAN-REMOVAL-PLAN.md),
but no removal is scheduled without a new explicit decision.

## Frozen Areas

- archive preview and archive recovery;
- IRC and IRC-adjacent chat UI;
- the legacy scheduler and scheduler preferences;
- SMTP/email, SAPI text-to-speech, and sound/WAV event notifications;
- the first-run connection wizard and legacy splash screen;
- legacy WebServer HTML templates and page UI;
- proxy/SOCKS support;
- the 3D preview control and id3lib metadata path;
- unsupported residual PeerCache resources and other dead legacy remnants.

These areas may stay compile-preserved. Do not add shims, diagnostics, harnesses,
UI automation, or parser/golden coverage for them unless an approved
maintenance task needs to protect a supported shared boundary.

## Supported Boundaries

- REST `/api/v1`, the bounded qBittorrent-compatible `/api/v2` adapter,
  Torznab, and the shipped aMuTorrent `0.7.3` integration remain supported where
  the release contract documents them.
- WebServer listener safety, HTTPS/TLS behavior on `0.7.x`, allowed-IP checks,
  and REST routing remain supported because they carry the controller API.
- Category behavior remains supported; scheduler behavior does not.
- Friend/source behavior remains supported where covered separately. eD2K peer
  chat is retained but unsupported; IRC chat is frozen.
- Native MiniMule behavior remains owned by eMuleBB and is not part of the
  frozen legacy WebServer UI.

## Release Test Rule

Release campaigns must not require evidence for frozen surfaces. Test manifests
may mention them only as exclusions or when a maintenance change needs to prove
that supported shared behavior was not damaged.
