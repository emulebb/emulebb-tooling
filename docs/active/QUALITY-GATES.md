# Quality Gates

Status: governance. Updated 2026-10-02.

Quality gates follow repository lifecycle. A retained experiment does not
inherit the release burden of an active product, and a reference fork must not
be presented as a production candidate merely because CI can build it.

## Active beta: emulebb-rust

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
scope defined by the [Product Direction](PRODUCT-DIRECTION.md).

## Supporting repositories

- `emulebb-build`, `emulebb-build-tests`, and `emulebb-tooling` keep their
  existing CI, privacy, documentation, and topology checks.
- `ed2k-server` is the sole local deterministic server and an upstream-aligned
  reference fork. Validate its required harness behavior and any proposed
  upstream patch, while keeping server changes minimal, generic, and
  upstreamable. The retired production-hardening gates remain available from
  the archival commit recorded in the [history overview](../history/INDEX.md).
- The aMule fork remains an analysis/build reference with its existing
  automation.

## Archived work

Retired product-family and controller repositories have no current workspace
gate or maintenance expectation. Completed release evidence remains historical
provenance and must not revive scheduled product automation implicitly.

## Principles

- Test the owning lane and the surfaces a change can affect.
- Treat non-blocking checks as named, visible debt only in active work.
- Keep privacy and tracked-content guards on every repository that accepts
  changes.
- Require release evidence before using stable, beta, VPN-safe, or
  production-ready labels.
