# Release Branching And Packaging

Status: current organization-wide release boundary. Updated 2026-10-30.

This page applies the lifecycle decisions in
[Product Direction](../active/PRODUCT-DIRECTION.md) to branches, tags, packages,
and public release claims. Product repositories own their exact build commands,
artifact matrices, and release checklists.

## eMuleBB Rust

eMuleBB Rust is the primary product and the only active product-development
lane. CI-gated nightly prereleases from `main` are the first public download
path and should be recommended ahead of the stale Beta 2 release.

- Keep `main` releasable enough to produce dated nightly packages.
- Use short-lived reviewed branches for changes; do not maintain a parallel
  long-running release branch without an explicit release need.
- Publish nightly artifacts through the Rust repository's release workflow and
  preserve its platform, manifest, checksum, and provenance gates.
- Treat the product as an active beta tested for months on live eD2K/Kad
  networks, not as experimental software.
- Beta 3 follows the remaining implementation and stabilization work. The
  current expectation is a few weeks, but release readiness and evidence—not a
  calendar promise—control promotion.
- Keep the Rust application, WebUI, product docs, and release notes
  English-only. Organization-site homepage and FAQ translations are separate
  from the product.

The Rust product repository and its release scope own exact tag names, package
names, supported platforms, and promotion criteria. This repository must not
duplicate those details as a competing release specification.

## eMuleBB MFC

The MFC application is a maintenance product on the published `0.7.x` line.
There is no active `0.8.x` modernization program.

- Start maintenance work only from a current owning issue and explicit roadmap
  placement.
- Keep fixes bounded to accepted maintenance categories in Product Direction.
- Create a maintenance branch only when a concrete `0.7.x` release needs one;
  otherwise use reviewed short-lived branches against the maintained base.
- Preserve existing package names and compatibility unless a maintenance issue
  explicitly requires a change.
- Require focused build, package, smoke, and regression proof appropriate to
  the changed surface before publishing another `0.7.x` package.

The retained [0.7.3 proof summary](../history/releases/0.7.3/RELEASE-0.7.3-PROOF-SUMMARY.md)
describes the already-published line. It is historical evidence, not an active
RC dashboard or a future-product roadmap.

## Infrastructure And Reference Repositories

Build, test, tooling, and reference repositories publish only what their
support role requires. A tag or package in those repositories does not create a
new eMuleBB product or change product lifecycle status.

`ed2k-server` remains a harness/reference component. TrackMuleBB and former
product-family experiments remain archived. aMuTorrent artifacts may be
retained as historical MFC bundle evidence but are not a current product lane.

## Release Evidence

Every public package claim must be traceable to the owning source revision and
the repository's required CI or operator evidence. At minimum, retain:

- source tag or immutable source revision;
- package identity and supported platform;
- checksums, manifests, and SBOM/provenance where the product workflow produces
  them;
- the release notes or proof summary that states the tested boundary; and
- known limitations that materially affect users.

Use [Test Strategy](../active/TEST-STRATEGY.md) for lifecycle-based validation,
[Quality Gates](../active/QUALITY-GATES.md) for repository expectations, and
[Evidence Retention](EVIDENCE-RETENTION.md) for durable proof handling.
