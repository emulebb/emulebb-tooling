# Product Direction

Status: current organization-wide product direction. Updated 2026-11-12.

This document is the single current lifecycle and direction authority for the
eMuleBB organization. Product-specific scope and engineering detail remain in
the owning product sections.

## Current Focus

`emulebb-rust` is the only active product-development lane: one universal,
headless eD2K/Kad daemon with an integrated REST API and browser operations
console. Native packages and containers distribute the same product and
state-ownership contract. Qualification remains specific to the source,
platform, architecture and deployment that actually passed.

It is an active beta led by CI-gated nightly prereleases from `main`; users
should choose the newest dated nightly from GitHub Releases. Beta 3 promotion
remains on hold. No implementation or release date is implied by this direction.

eMuleBB Rust, its WebUI, product documentation, and release notes are
English-only. The organization website may localize its homepage and FAQ, but
those pages are not product translations.

The current production phase is the eD2K/Kad client, `/api/v1` control plane,
and embedded operations console. The autonomous Indexer and Arr adapter remain
future phases behind the mandatory core Client gate defined in
[Rust Release Scope](../products/emulebb-rust/RELEASE-SCOPE.md). Optional
distribution channels and additional environments retain explicit owners but
do not keep that gate open solely because they are unfinished. This scope
classification does not remove any required CI or selected release check.

## Product Lifecycle

| Repository or product | Lifecycle | Current role |
|---|---|---|
| `emulebb-rust` | Active beta | Universal headless eD2K/Kad daemon; nightly builds are the public testing path |
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
- Balanced reliability leads the next delivery wave. Existing persistence,
  configuration, schema and client-correctness owners keep their work; there
  is no new umbrella optimization program.
- [Scoop delivery (#324)](https://github.com/emulebb/emulebb-rust/issues/324)
  is the first accepted new distribution lane. Linux services are deferred to
  the bounded [design review (#325)](https://github.com/emulebb/emulebb-rust/issues/325);
  that review authorizes no service installation or enablement.
- Ubuntu 24.04 and Debian 13 on x64/ARM64 are initial Linux qualification
  targets, not a claim that every distribution/CPU combination is proven.
  Package bytes and retained native evidence determine actual support.
- APT, RPM and Homebrew remain expansion candidates pending activation.
  AUR and Nix are unactivated ideas. NAS, BSD, Android/Fire OS and ChromeOS
  qualification remain with their existing optional environment owners.
- MFC maintenance becomes active only through a current owning issue and
  explicit roadmap placement; the archived MFC Project #2 is provenance only.
- Parked, ownerless, completed, and superseded work is archive material, not an
  active backlog.

Related: [eMuleBB Rust](../products/emulebb-rust/README.md),
[Rust Release Scope](../products/emulebb-rust/RELEASE-SCOPE.md),
[MFC Product Section](../products/emulebb-mfc/README.md), and
[Workspace Policy](../WORKSPACE-POLICY.md).
