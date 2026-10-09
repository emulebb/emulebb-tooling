# Roadmap Summary

## Current Direction

The eMuleBB organization has one active product-development lane:
**emulebb-rust**, an experimental eD2K/Kad client in beta. CI-gated nightly
prereleases from `main` are the current public testing channel. Beta status is
an invitation to test, not a production-readiness claim; the project receives
best-effort, spare-time development, and
[contributors are welcome](https://github.com/emulebb/emulebb-rust/blob/main/CONTRIBUTING.md).

The published **eMuleBB Windows client** remains available on its stable `0.7.x`
maintenance line. It accepts bugs and bounded low-risk UX, performance,
compatibility, build, packaging, documentation, diagnostics, and release work.
Its feature expansion and major modernization backlog is parked as `DEFERRED`.

Current GitHub-primary work is tracked on org Project #3, **eMuleBB Roadmap**.

## Retained But Not Active

- **qBittorrentBB** and **emulebb-libtorrent** are paused experiments. They are
  preserved for reference and explicit on-demand builds, not roadmap work.
- **aMuTorrent** is the frozen controller shipped with the `0.7.3` bundle.
- **TrackMuleBB** is an archived private experiment.
- **goed2k-server** is fixed harness infrastructure, not an evolving service.
- **ed2k-server** is a reference fork for analysis and potentially upstreamable
  contributions, not a production-hardening or future-harness program.
- **aMule** checkouts are analysis/reference inputs. Existing automation may
  continue, but aMule is not an eMuleBB product lane.

The former cross-network **eMuleBB Suite** roadmap is retired. The name remains
valid for the shipped `0.7.3` MFC/aMuTorrent bundle, its installer and artifacts,
and historical documentation.

## Network Priority

Native Windows VPN integration is no longer a forward development priority.
Existing direct/VPN behavior must remain accurately documented and
evidence-bound. No unspecified Docker/Gluetun stack is currently an eMuleBB
product.

See [Product Portfolio](../active/PRODUCT-PORTFOLIO.md) for the complete
lifecycle map and [Workspace Policy](../WORKSPACE-POLICY.md) for binding rules.
