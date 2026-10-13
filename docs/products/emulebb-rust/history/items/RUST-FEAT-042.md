---
id: RUST-FEAT-042
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/85
title: Handle OP_INVALID_LOWID server-UDP notification
status: WONT_DO
priority: Minor
category: feature
labels: [rust, ed2k, server, udp, diagnostics]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/85. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-042 - Handle OP_INVALID_LOWID server-UDP notification

## Summary

Disposition record. `OP_INVALID_LOWID` (0x9E) appears in stock eMule and aMule
opcode headers, but the current reference review found no executable sender,
receiver branch, or user-visible behavior in either client and no corresponding
behavior in the maintained Rust server reference. The Rust client's bounded
unsupported-opcode diagnostic is sufficient without an invented payload
contract.

## Current State

- `crates/emulebb-ed2k/src/ed2k_server.rs` does not assign semantic behavior to
  `OP_INVALID_LOWID` (0x9E).
- The server-UDP receive path retains a bounded unsupported-opcode diagnostic.
- `analysis/community-0.72/srchybrid/Opcodes.h` and aMule's protocol header
  declare the numeric opcode, but repository-wide searches found no executable
  handling that establishes the proposed four-byte payload or side effects.
- `repos/ed2k-server` contains no live implementation evidence for this opcode.

## Why This Matters

Implementing a decoder from a declaration alone would manufacture protocol
semantics rather than port reference behavior. Generic bounded diagnostics keep
unexpected traffic observable without claiming an unverified packet contract.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server.rs` - server UDP opcode table
- `crates/emulebb-ed2k/src/ed2k_server/udp.rs` - server-UDP datagram framing
- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs` - server-UDP receive
  dispatch
- `EMULEBB_WORKSPACE_ROOT\analysis\community-0.72\srchybrid\Opcodes.h` - `OP_INVALID_LOWID` (0x9E)

## Intended Shape

No product change. Retain generic unsupported-opcode diagnostics unless an
executable reference, captured packet, or independent product requirement
establishes a real payload and behavior.

## Scope Constraints

- Do not infer payload shape from an opcode name or header comment.
- A future proposal requires captured wire evidence or executable reference
  behavior and must receive a new backlog item.

## Acceptance Criteria

- [x] Reference review distinguishes declarations from executable behavior.
- [x] Existing unknown-opcode handling remains bounded and observable.
- [x] The unsupported proposal is closed without adding speculative wire code.

## Validation

- Documentation taxonomy and structure checks.

## Notes

Closed `WONT_DO` on 2026-10-13 after revalidating stock eMule, aMule, and
`ed2k-server`: declarations exist, but no executable implementation establishes
the proposed behavior.
