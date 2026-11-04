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
