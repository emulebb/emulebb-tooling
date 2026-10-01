---
id: ED2KSRV-CI-003
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/11
title: Resolve dependency advisories and enforce an advisory gate
status: OPEN
priority: Critical
category: ci
labels: [security, dependencies, supply-chain, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: GitHub dependency-alert review after portfolio onboarding at ed2k-server 03eaa4b
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-CI-003 - Resolve dependency advisories and enforce an advisory gate

## Summary

Close the open runtime dependency advisories and add a blocking advisory check
so known high/critical vulnerabilities cannot silently remain on the production
candidate branch.

## Current State

GitHub reports seven open Rust runtime alerts in `Cargo.lock`: one high, three
moderate, and three low. The high-severity `rustls-webpki` denial-of-service
advisory (`GHSA-82j2-j2ch-gfr8`) is present through `ureq -> rustls`. Direct
pins for `bytes` and `tracing-subscriber` are also below their first patched
versions.

## Scope Constraints

- Preserve the declared Rust 1.75 MSRV or make any MSRV change an explicit,
  separately reviewed compatibility decision.
- Use patched upstream releases; do not carry local cryptography/TLS patches.
- An advisory may be waived only with documented reachability, compensating
  controls, expiry, and operator acceptance.

## Acceptance Criteria

- [ ] The locked dependency graph contains patched versions for every applicable open alert.
- [ ] GitHub Dependabot shows no unaccepted open high or critical alert.
- [ ] Remaining lower-severity alerts are fixed or carry a time-bounded accepted-risk record.
- [ ] CI runs a blocking Rust advisory check on pushes and pull requests.
- [ ] The Rust 1.75 locked build/test lane and the current quality/release lane remain green.
- [ ] Dependency, license, formatting, Clippy, unit, integration, and artifact gates pass with the new lockfile.

## Validation

Record the dependency-chain changes, advisory results, MSRV proof, and full
hosted CI URLs in the closing evidence.
