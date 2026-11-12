---
id: RUST-BUG-154
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/221
title: Admit Kad datagrams before learning sender state
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, kad, protocol, security, state-machine, beta]
product: emulebb-rust
phase: Phase 0
milestone: rust-v0.1.0-beta.3
created: 2026-11-04
source: stock eMule Kad UDP listener audit against Rust receive ordering
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/221. This local document owns the durable engineering contract.

# RUST-BUG-154 - Admit Kad datagrams before learning sender state

## Summary

Make Kad UDP admission the mutation boundary. A datagram may be decoded and
non-mutatingly correlated before admission, but banned, flooded, spoofed, or
stock-port-53-rejected traffic must not teach routing identity, version, or
verify-key metadata and must not consume a pending request.

## Implemented Source And Remaining Proof

The source fix already landed in
[PR #225](https://github.com/emulebb/emulebb-rust/pull/225), including commit
`1bd026784ca52e90246c12f939d5477846abbf9d`, and is present in reviewed main
`080a5dea70186da31dab958757b5b8c0fd883f82`. Do not allocate another receive-loop
implementation solely because this tracking item remains open.

Current `emulebb-kad-net/src/rpc/receive_loop.rs` checks correlation without
consuming it, performs ban/flood admission before learning identity/version/key
metadata, and rejects source port 53 for absent or effective-zero verify keys,
including `Some(0)`. Existing `rpc/tests/admission.rs` covers flood-rejected
metadata, banned responses retaining pending state, spoofed replies followed by
a legitimate reply, and a nonzero encrypted source-port-53 positive control.
The receive-loop helper also has a zero-key boundary regression.

This is source reconciliation, not a newly executed campaign. The accepted
specific mixed Rust/MFC Kad campaign receipt for `kad.ingress.admission` and
`kad.ingress.port53-verify-key` has not been confirmed. General CI, packaged
local transfers and PR #225's eD2K server-search/OFFERFILES evidence do not
substitute for that Kad slice. Keep the issue In Progress and its acceptance
open until the parent locates and accepts existing evidence or allocates the
remaining bounded proof through the existing protocol harness owner.

## Slice Binding

- Catalog IDs: `kad.ingress.admission` and
  `kad.ingress.port53-verify-key`.
- Authority: stock/community eMule Kad UDP receive state machine.
- Start/stimulus: one pending request and known sender state; inject spoofed,
  banned, flood-rejected, source-port-53 zero-key, and valid correlated frames.
- Expected result: correlation validation is non-mutating; failed admission
  changes neither metadata nor pending state and does not charge the valid
  sender's flood budget; valid admission learns metadata, consumes once, and
  dispatches.
- Clients/runner: focused Rust paused-time tests, then the canonical mixed Kad
  runner with Rust and MFC.
- Green gates: focused Kad-net tests, full Rust gates, catalog validation, and
  the selected deterministic Kad campaign.

## Scope Constraints

- Preserve the existing spoof defense: an invalid reply cannot consume the
  legitimate sender's pending correlation or flood allowance.
- Treat an absent key and effective zero key identically for stock's UDP
  source-port-53 rejection, including encrypted metadata represented as
  `Some(0)`.
- Do not weaken cryptographic decoding or move untrusted metadata into routing
  state before admission.

## Acceptance Criteria

- [ ] Pending correlation can be checked without consuming or mutating it.
- [ ] Ban and flood admission precede every sender-metadata mutation.
- [ ] Rejected traffic leaves identity, version, key, routing, and pending
      state unchanged.
- [ ] Invalid senders do not consume a legitimate sender's flood budget.
- [ ] Source port 53 is rejected when the effective verify key is absent or
      zero, whether clear or encrypted.
- [ ] Valid admitted replies learn metadata, consume once, and dispatch.

## Validation

- Focused receive-loop ordering, zero-key, spoof, ban, flood, and pending-state
  regressions with deterministic time.
- Canonical Rust gates and selected local mixed-client Kad campaign.
