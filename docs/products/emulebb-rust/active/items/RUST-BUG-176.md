---
id: RUST-BUG-176
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/278
title: Bound URL-import responses and define destination policy
status: OPEN
priority: Major
category: bug
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/278. This local document owns the durable engineering specification and evidence.

# RUST-BUG-176 - Bound URL-import responses and define destination policy

## Summary

Bound discovery downloads before collecting complete bodies or changing imported
state. The confirmed defect is resource handling: the core URL-import fetcher
uses `response.bytes()` without a byte ceiling. This outcome covers memory,
elapsed time, decoding behavior, redirect count, and validation of each URL's
scheme before contact.

Use one small shared discovery-fetch owner for authenticated `server.met` and
`nodes.dat` imports and first-run trusted bootstrap. Reuse the existing format
ceilings: 4 MiB for `server.met` and 2 MiB for `nodes.dat`.

## Release Placement

Major; assigned to the Windows/Linux Beta 3 readiness backlog. All Beta 3
release actions are on operator hold. Workspace, multiarchitecture, and
multiplatform improvements take priority; bug implementation follows that work.
This specification correction does not authorize bug implementation, candidate
execution, workflow dispatch, tagging, version changes, or publication.

Delivery lane: control-plane.

## Current Findings

Confirmed by static inspection of Rust source
`edc59a003fff873e26d2c720bf9ca06f4b640871`; no exploit, runtime, or new
validation result is claimed.

- Core imports share an unbounded body fetch with a 30-second request timeout.
- REST already rejects non-HTTP(S) input schemes. Core text validation does not
  establish the same parsed-URL contract for every caller and redirect.
- Trusted bootstrap already uses the format byte caps, a 10-second timeout,
  three redirects, and streamed reads. Its HTTPS check inspects the final URL
  after automatic redirects; intermediate requests must instead be checked
  before contact.
- Current workspace reqwest consumers do not request automatic compression
  features. Do not introduce decoding merely for this fix.

Source references:

- `repos/emulebb-rust/crates/emulebb-core/src/ed2k_net_drivers.rs:67`
- `repos/emulebb-rust/crates/emulebb-core/src/network_api.rs:124`
- `repos/emulebb-rust/crates/emulebb-core/src/network_api.rs:164`
- `repos/emulebb-rust/crates/emulebb-core/src/views.rs:588`
- `repos/emulebb-rust/crates/emulebb-rest/src/route_body_metadata/validators.rs:1410`
- `repos/emulebb-rust/crates/emulebb-daemon/src/discovery_bootstrap.rs:23`
- `repos/emulebb-rust/crates/emulebb-daemon/src/discovery_bootstrap.rs:177`

## Destination And Scope Contract

Authenticated URL import is an explicitly authorized operator network
capability. Preserve HTTP and HTTPS imports, direct LAN/loopback use,
cross-host redirects within the intended scheme contract, and existing proxy
settings. Do not introduce address-class filtering, DNS pinning, proxy
suppression, destination allowlists, or a new permission model in this outcome.

Validate every initial and redirected URL with the pinned URL/HTTP library
before sending that request. Operator imports retain HTTP/HTTPS support;
trusted automatic bootstrap must remain HTTPS before every hop. Bound the
redirect chain to three hops. Preserve normal certificate verification and
existing supported network behavior.

This work does not promise an SSRF or DNS-rebinding shield. No untrusted-caller
boundary requiring such a shield was established by this review. A stricter
destination model belongs in a separate threat-model/design outcome, with its
operator-compatibility costs made explicit.

## Acceptance Criteria

- [ ] Both operator import paths and trusted bootstrap reuse a bounded
      discovery-fetch implementation with format-specific 4 MiB / 2 MiB caps.
- [ ] Actual received bytes are counted before extending the accumulated body,
      independently of missing or misleading Content-Length. Do not allocate a
      full response or reserve from an untrusted declared length.
- [ ] One finite elapsed-time budget covers the whole fetch, including redirects
      and body reads; retain 30 seconds for operator import and 10 seconds for
      trusted bootstrap unless evidence justifies a documented adjustment.
- [ ] Every redirect target passes the applicable scheme check before contact;
      chains and loops cannot exceed three hops. Trusted bootstrap never sends
      a request to an HTTP intermediate hop.
- [ ] Decoding cannot bypass the byte ceiling. Preserve the currently supported
      identity/raw-body path without adding decompression. If supported
      decoding is retained, bound decoded output independently and prove it.
- [ ] Explicit authenticated LAN/loopback imports, allowed cross-host redirects,
      and existing proxy behavior remain supported without environment changes.
- [ ] Oversized, timed-out, malformed, unsupported-scheme, and excess-redirect
      inputs fail visibly before their rejected document changes existing
      imported state. Keep errors bounded and do not retain secret URL parts.
- [ ] Deterministic local regressions prove the resource, scheme, compatibility,
      and state-preservation behavior on Windows/Linux.
- [ ] Required scoped checks pass at the selected source revisions. No claim of
      full SSRF/rebinding protection is made.

## Implementation Boundary

Prefer a narrow helper in `emulebb-core` consumed by the daemon, which already
depends on core. Reuse reqwest's chunk reader and URL/redirect facilities and
existing dependencies; do not create a general HTTP framework or a new crate.

Expected source scope is the shared helper/tests, core module wiring, the old
fetch helper in `ed2k_net_drivers.rs`, the two `network_api.rs` callers, and
`discovery_bootstrap.rs`. Adjust `views.rs` only where needed for consistent
core URL validation. Extend existing REST/import tests and document the actual
limits at the existing API operations. Do not redesign nodes persistence,
authentication, proxy routing, or unrelated URL consumers.

## Focused Validation

Use synthetic local HTTP fixtures and small injected limits where appropriate:

1. Valid files and exact-limit bodies; limit-plus-one rejection.
2. Oversized declared lengths, absent/misleading lengths, chunked bodies, and
   many small chunks; accumulated memory remains within the chosen cap.
3. Slow headers, drip-fed bodies, and redirect chains share one deadline.
4. Valid relative and cross-host redirects; loops and fourth-hop attempts are
   rejected before contacting that next target.
5. Non-HTTP(S) operator targets and every non-HTTPS bootstrap hop are rejected
   before contact, including an HTTPS-to-HTTP intermediate redirect.
6. Encoded responses cannot cause unbounded decoded output; current
   identity/raw-body compatibility is retained.
7. Explicit LAN/loopback success and unchanged proxy selection, without
   modifying inherited environment variables.
8. Rejected fetches or malformed documents leave prior server rows and nodes
   data intact; unauthenticated REST calls cannot initiate imports.

After a parent-assigned validation window, use the registered source set and
supported `python -m emule_workspace test rust-unit --package <package>`
entrypoint for affected core, daemon, and REST packages, then the required
local push gate. Heavy validation stays serialized. Public-network testing is
not required for this bounded defect.

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_rest-api.md` section 3.1.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md`
  section security-url-import.

## Remaining Evidence And Coordination

The finite byte limits are inherited from trusted bootstrap; representative
operator imports have not been measured here. No runtime exploit or compatibility
test was run. Confirm the actual pinned reqwest decoding and timeout semantics
during implementation. Broader destination restrictions remain a separate
design question rather than an unproven release-security claim.

Parent reserves shared files and the managed workstream before implementation.
