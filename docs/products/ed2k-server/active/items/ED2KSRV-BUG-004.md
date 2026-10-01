---
id: ED2KSRV-BUG-004
workflow: github
github_issue: https://github.com/emulebb/ed2k-server/issues/5
title: Make advertised protocol capabilities truthful
status: OPEN
priority: Critical
category: bug
labels: [protocol, compatibility, capability-negotiation, production-readiness]
milestone: production-readiness
created: 2026-10-01
source: Rust-vs-Go-vs-Lugdunum production-readiness review at ed2k-server 604b257
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# ED2KSRV-BUG-004 - Make advertised protocol capabilities truthful

## Summary

Every advertised server capability must correspond to implemented, tested wire
behavior. Resolve known discrepancies around related search, obfuscated source
lookup replies, and callback behavior.

## Current State

`src/proto/opcodes.rs` documents `RELATEDSEARCH` as advertised but not
implemented. `OP_GETSOURCES_OBFU` and callback paths require end-to-end proof
that the response opcode and advertised flags match actual behavior.

## Scope Constraints

- Prefer removing an advertised bit over claiming incomplete behavior.
- Intentional extensions must not change stock-client semantics silently.
- Compare observable wire behavior only; do not transplant decompiled code.

## Acceptance Criteria

- [ ] `RELATEDSEARCH` is implemented and proven or no longer advertised.
- [ ] Obfuscated source requests receive the correct corresponding response semantics.
- [ ] TCP/UDP callback capabilities are implemented and proven or not advertised.
- [ ] Capability masks have contract tests tied to end-to-end packet fixtures.
- [ ] Stock eMule and aMule smoke evidence shows no negotiation regression.

## Validation

Use the clean-room corpus from `ED2KSRV-CI-001` plus bounded live-client smoke
evidence with synthetic filenames and scrubbed captures.
