---
id: ED2KSRV-BUG-001
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/2
title: Bound packed-frame decompression and input sizes
status: OPEN
priority: Critical
category: bug
labels: [resource-safety, protocol, denial-of-service, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-BUG-001 - Bound packed-frame decompression and input sizes

## Summary

Packed `0xD4` frames are decompressed into an unbounded buffer after only the
compressed wire length has been bounded. Establish explicit wire, decompressed,
tag/string, and collection limits so hostile input cannot drive unbounded
allocation or CPU.

## Current State

`src/proto/frame.rs` uses `flate2::read::ZlibDecoder::read_to_end`. The
configuration advertises `max_string_size`, but production enforcement is not
consistent across protocol parsing paths.

## Scope Constraints

- Preserve valid stock eMule/aMule packed-frame behavior.
- Use standard bounded I/O/decompression mechanisms.
- Treat malformed and oversized input as a connection-level protocol error,
  not a process failure.

## Acceptance Criteria

- [ ] Compressed wire length and decompressed output have explicit configurable ceilings.
- [ ] Tag strings and variable-length collections are consistently bounded before allocation.
- [ ] Compression-bomb, truncated-stream, oversized-frame, and boundary-value regression tests pass.
- [ ] Normal packed frames remain compatible with the shared golden corpus.
- [ ] A focused stress test demonstrates bounded memory and termination time for rejected input.

## Validation

Run locked unit/integration tests, the protocol corpus, Clippy, formatting, and
a focused hostile-input memory/CPU check.
