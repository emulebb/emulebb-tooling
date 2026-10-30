# Product Direction

Status: current organization-wide product direction. Updated 2026-10-30.

This document is the single current lifecycle and direction authority for the
eMuleBB organization. Product-specific scope and engineering detail remain in
the owning product sections.

## Current Focus

`emulebb-rust` is the only active product-development lane. It is an active
beta led by CI-gated nightly prereleases from `main`; users should choose the
newest dated nightly from GitHub Releases. The client has been tested for
months on live eD2K/Kad networks. Beta 3 is expected after a few more weeks of
implementation and stabilization.

eMuleBB Rust, its WebUI, product documentation, and release notes are
English-only. The organization website may localize its homepage and FAQ, but
those pages are not product translations.

The current production phase is the eD2K/Kad client, `/api/v1` control plane,
and embedded operations console. The autonomous Indexer and Arr adapter remain
concise future phases behind the complete Client gate. They are not active
implementation lanes and have no schedule.

## Product Lifecycle

| Repository or product | Lifecycle | Current role |
|---|---|---|
| `emulebb-rust` | Active beta | Primary eD2K/Kad client; nightly builds are the public testing path |
| `emulebb` (MFC) | Maintenance | Published Windows `0.7.x` line for critical and bounded low-risk maintenance |
| `ed2k-server` | Harness / reference | Deterministic local eD2K server kept close to upstream; not a public service |
| `amule-org/amule` | Reference | Interoperability and protocol-parity input; not an eMuleBB product |
| Build, test, and tooling repositories | Infrastructure | Workspace orchestration, validation, policy, and documentation |
| TrackMuleBB and former product-family experiments | Archived | Historical source and provenance only |

## MFC Maintenance Boundary

eMuleBB MFC remains published, buildable, and shippable on `0.7.x`. It may
accept bug, crash, security, data-loss, compatibility, build, packaging,
documentation, diagnostics, and bounded low-risk UX or performance fixes.

It does not have an active `0.8.x` modernization program. New subsystems, broad
APIs, protocol expansion, architectural modernization, controller-platform
development, and native Windows VPN integration are outside the current lane.
Future product development belongs to eMuleBB Rust.

## Retired Directions

The former cross-network **eMuleBB Suite** roadmap is retired. The name remains
valid only for the shipped `0.7.3` MFC/aMuTorrent bundle, its artifacts, and
historical release records. TrackMuleBB is archived. aMuTorrent automation may
remain as historical release infrastructure, but it is not an active eMuleBB
product-development lane.

`ed2k-server` production hardening is also retired. New server work must be
limited to deterministic harness capability, upstream alignment, or generic
upstreamable fixes unless the operator explicitly adopts a new product role.

## Planning Rules

- Project #3, **eMuleBB Roadmap**, contains current GitHub-primary work.
- Rust Beta 3 work and its Client gate take precedence over inactive future
  phases and legacy product proposals.
- MFC maintenance becomes active only through a current owning issue and
  explicit roadmap placement; the archived MFC Project #2 is provenance only.
- Parked, ownerless, completed, and superseded work is archive material, not an
  active backlog.

Related: [eMuleBB Rust](../products/emulebb-rust/README.md),
[Rust Release Scope](../products/emulebb-rust/RELEASE-SCOPE.md),
[MFC Product Section](../products/emulebb-mfc/README.md), and
[Workspace Policy](../WORKSPACE-POLICY.md).
