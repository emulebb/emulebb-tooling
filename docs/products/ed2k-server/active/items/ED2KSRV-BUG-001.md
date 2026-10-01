---
id: ED2KSRV-BUG-001
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/2
title: Bound packed-frame decompression
status: OPEN
priority: Critical
category: bug
labels: [resource-safety, protocol, denial-of-service, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-BUG-001 - Bound packed-frame decompression

## Summary

Packed `0xD4` frames are decompressed into an unbounded buffer after only the
compressed wire length has been bounded. Add an independent configurable
ceiling for decompressed output so a small zlib payload cannot exhaust process
memory.

## Current State

`src/proto/frame.rs` uses `flate2::read::ZlibDecoder::read_to_end` without an
output ceiling.

## Scope Constraints

- Preserve valid stock eMule/aMule packed-frame behavior.
- Use standard bounded I/O/decompression mechanisms.
- Treat malformed and oversized input as a connection-level protocol error,
  not a process failure.
- Tag, string, and collection parser limits are tracked separately by
  `ED2KSRV-BUG-005`.

## Acceptance Criteria

- [ ] Compressed wire length and decompressed output have independent explicit ceilings.
- [ ] The decompressed ceiling is configurable and defaults safely for existing configurations.
- [ ] Decompression terminates after at most one byte beyond the configured ceiling.
- [ ] Normal, exact-boundary, limit-plus-one, high-expansion, truncated-stream,
      and wire-limit regression tests pass.
- [ ] Plain frames and valid packed frames retain their existing behavior.

## Validation

Run locked unit/integration tests, formatting, Clippy, and the managed Linux
release build.
