---
id: RUST-BUG-155
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/222
title: Share established peer identity and control state
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, protocol, peer, callback, state-machine, beta]
product: emulebb-rust
phase: Phase 0
milestone: rust-v0.1.0-beta.3
created: 2026-11-04
source: stock eMule established-peer control audit against Rust inbound and outbound paths
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/222. This local document owns the durable engineering contract.

# RUST-BUG-155 - Share established peer identity and control state

## Summary

Use one established-peer control model after HELLO on inbound and outbound
connections. Client/server identity must remain mutable, callback and firewall
acknowledgement controls must update state on either path, and valid unknown
post-handshake frames must receive the same stock-compatible tolerant handling.

## Slice Binding

- Catalog IDs: `peer.identity.change-client-id`, `peer.control.callback`,
  `peer.control.firewall-ack`, and `peer.control.unknown-opcode`.
- Authority: stock/community eMule peer socket state behavior.
- Start/stimulus: complete HELLO on inbound and outbound transports, then send
  each valid control frame and one well-framed unknown post-HELLO opcode.
- Expected result: identity and callback/firewall state mutate once and are
  visible to their owners; the unknown frame is ignored consistently without
  closing either established connection.
- Clients/runner: focused Rust state-machine tests, then canonical Rust/MFC
  peer-handshake and callback campaigns.
- Green gates: focused ED2K tests, full Rust gates, catalog validation, and the
  selected deterministic peer campaigns.

## Scope Constraints

- Keep framing, payload, and connection-phase validation strict.
- Do not create separate inbound and outbound callback authorities.
- Tolerance applies only to validly framed unknown opcodes after HELLO; it is
  not permission to accept malformed or phase-invalid traffic.

## Acceptance Criteria

- [ ] `OP_CHANGE_CLIENT_ID` updates mutable client and server identity on both
      established paths.
- [ ] Callback and firewall-check acknowledgement controls apply statefully on
      inbound and outbound connections.
- [ ] Shared control handling preserves existing listener behavior and exposes
      the same transition results to download sessions.
- [ ] A valid unknown post-HELLO frame is ignored consistently without closing
      the connection; malformed frames still fail closed.
- [ ] Focused tests cover every control on both connection directions.

## Validation

- Focused established-peer identity/control state-machine regressions.
- Canonical Rust gates and selected peer-handshake/callback campaigns.
