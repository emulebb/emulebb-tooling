# Roadmap Summary

## Current Direction

The eMuleBB organization has one active product-development lane:
**emulebb-rust**, an eD2K/Kad client in beta. CI-gated nightly prereleases from
`main` are the current public testing channel. The project receives best-effort,
spare-time development, and
[contributors are welcome](https://github.com/emulebb/emulebb-rust/blob/main/CONTRIBUTING.md).

The published **eMuleBB Windows client** remains available, buildable, and
shippable on its stable `0.7.x` maintenance line. It accepts critical fixes and
bounded low-risk UX, performance, compatibility, build, packaging,
documentation, diagnostics, and release work.
Its feature expansion and major modernization backlog is parked as `DEFERRED`.

Current GitHub-primary work is tracked on org Project #3, **eMuleBB Roadmap**.

## Supporting And Historical Context

- **TrackMuleBB** is an archived private experiment.
- **ed2k-server** is the sole local deterministic server and an upstream-aligned
  Rust reference fork, not a production-hardening program or public service.
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
