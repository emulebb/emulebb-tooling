---
id: RUST-BUG-133
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/157
title: Bound REST request bodies before metadata validation
status: DONE
priority: Major
category: bug
labels: [rust, rest, security, safety, resource-bounds, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-23
source: 2026-10-23 Rust best-practices and safety audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/157. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-133 - Bound REST request bodies before metadata validation

## Summary

Apply one explicit REST request-body limit before route metadata validation or
any other middleware materializes the body. Reject oversized fixed-length and
streamed bodies with `413 Payload Too Large` without allocating in proportion
to attacker-controlled input.

## Current State

`crates/emulebb-rest/src/route_metadata.rs` calls
`to_bytes(body, usize::MAX)` so it can validate JSON field metadata and then
reconstruct the request. This middleware executes before downstream extractors,
so extractor-level JSON limits do not protect the pre-read. The default daemon
profile binds REST to loopback and requires an API key, but operators may bind
it to another interface and every authenticated request still reaches an
unbounded allocation path.

## Why This Matters

Authentication is not a resource bound. A faulty or compromised client can
stream an arbitrary request and exhaust daemon memory before normal route
validation runs. The failure mode affects the whole P2P process rather than one
request.

## Representative Sites

- `crates/emulebb-rest/src/route_metadata.rs` `validate_route_metadata`.
- `crates/emulebb-rest/src/routes.rs` API middleware ordering.
- REST route-validation and body-validation tests.

## Intended Shape

- Define one typed maximum request-body policy at the outer API boundary.
- Authenticate before consuming request bodies, then enforce the size limit
  before metadata validation and handler extraction.
- Pass the same finite limit to `to_bytes`; do not rely only on
  `Content-Length` or an extractor that runs later.
- Allow a route-specific exception only when its bounded requirement is
  explicit and independently tested.
- Return `413 Payload Too Large` for size violations and keep malformed bounded
  JSON on the existing validation path.

## Scope Constraints

- Preserve the API-key boundary and response security headers.
- Do not introduce a second buffering pass or silently truncate a body.
- This is an internal REST safety policy and must not change stock eMule wire
  behavior.
- API and configuration compatibility are not constraints during beta; choose
  the clearest long-term contract.

## Acceptance Criteria

- [x] Every `/api/v1` request body is capped before route metadata validation
      or full-body materialization.
- [x] Chunked/streamed bodies and incorrect or absent `Content-Length` values
      cannot bypass the cap.
- [x] Oversized bodies return `413 Payload Too Large` without invoking the
      handler or allocating beyond the configured policy plus bounded overhead.
- [x] Unauthorized requests are rejected before their bodies are consumed.
- [x] Normal body-field validation and bounded JSON extraction continue to
      produce the documented API errors.
- [x] The limit and any route-specific exceptions have one documented owner.

## Validation

- Router tests with fixed, chunked, missing-length, and misleading-length
  bodies immediately below and above the limit.
- A streaming-body regression proving early termination and no handler call.
- Existing REST contract, route metadata, OpenAPI, and WebUI tests.

## Resolution

- Enforced the authenticated 1 MiB REST body cap before route metadata parsing or handler extraction.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-rest`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`
