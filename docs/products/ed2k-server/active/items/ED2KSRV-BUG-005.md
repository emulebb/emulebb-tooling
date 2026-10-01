---
id: ED2KSRV-BUG-005
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/12
title: Bound protocol parser strings and collections
status: OPEN
priority: Critical
category: bug
labels: [resource-safety, protocol, denial-of-service, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Scope split from ED2KSRV-BUG-001 during decompression-ceiling implementation
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-BUG-005 - Bound protocol parser strings and collections

## Summary

Protocol parsers accept peer-controlled string lengths, tag counts, and
collection counts without one consistent allocation budget. Enforce configured
bounds before allocation or iteration so malformed input cannot amplify memory
or CPU work after frame decoding.

## Current State

`limits.max_string_size` is advertised in configuration but is not consistently
applied by tag and request parsers. Several collection parsers use local
hard-coded reasonableness checks rather than shared configured limits and
remaining-frame validation.

## Scope Constraints

- Preserve valid stock eMule/aMule encodings and boundary values.
- Reject invalid input at the parser boundary without partial state mutation.
- Keep packed-frame decompression limits in `ED2KSRV-BUG-001` and
  admission/rate limiting in `ED2KSRV-BUG-003`.

## Acceptance Criteria

- [ ] Peer-controlled strings are length-checked before allocation and honor the configured ceiling.
- [ ] Tag and collection counts are bounded before allocation and iteration.
- [ ] Declared counts are feasible for the bytes remaining in the decoded frame.
- [ ] Shared parsing helpers apply the same limits across login, offer-files,
      search, and related protocol paths.
- [ ] Exact-boundary, limit-plus-one, truncated, and excessive-count regression tests pass.
- [ ] Parser rejection leaves client, file, source, and search state unchanged.

## Validation

Run focused parser tests, locked unit/integration tests, formatting, Clippy, and
the managed Linux release build.
