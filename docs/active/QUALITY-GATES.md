# Quality Gates

Status: governance. Updated 2026-10-02.

Quality gates follow repository lifecycle. A retained experiment does not
inherit the release burden of an active product, and a reference fork must not
be presented as a production candidate merely because CI can build it.

## Active experimental beta: emulebb-rust

Rust changes require the repository's supported platform build and test
matrix, formatting and lint checks, dependency policy, tracked-content privacy
guards, contract validation, and the proof appropriate to the changed surface.
Release claims require the beta release checklist and product-specific evidence.
VPN-safe language requires product-specific leak proof; no such property should
be inferred from bind support alone.

## Stable maintenance: eMuleBB MFC

MFC changes require the maintained Windows build matrix, native and shared
harness tests appropriate to the change, workspace validation, REST/OpenAPI
checks when the controller surface is touched, and release/package evidence for
published patches. Changes must remain within the bounded `0.7.x` maintenance
scope defined by the [MFC maintenance roadmap](FUTURE-ROADMAP.md).

## Supporting repositories

- `emulebb-build`, `emulebb-build-tests`, and `emulebb-tooling` keep their
  existing CI, privacy, documentation, and topology checks.
- `goed2k-server` is a fixed-purpose harness server. Validate changes only when
  the harness requires them; do not create a product-evolution gate.
- `ed2k-server` is a reference fork for analysis and possible upstream
  contribution. Source checks may support a proposed upstream patch, but the
  retired production-hardening gates are historical:
  [ED2KSRV-CI-002](../history/ed2k-server/items/ED2KSRV-CI-002.md) and
  [ED2KSRV-CI-003](../history/ed2k-server/items/ED2KSRV-CI-003.md).
- The aMule fork remains an analysis/build reference with its existing
  automation.

## Paused, frozen, and archived work

qBittorrentBB and emulebb-libtorrent are paused, aMuTorrent is frozen, and
TrackMuleBB is archived. They have no forward release gate. Any explicitly
approved maintenance should run the smallest repo-native checks needed to avoid
regression and should not revive scheduled product automation implicitly.

## Principles

- Test the owning lane and the surfaces a change can affect.
- Treat non-blocking checks as named, visible debt only in active work.
- Keep privacy and tracked-content guards on every repository that accepts
  changes.
- Require release evidence before using stable, beta, VPN-safe, or
  production-ready labels.
