---
id: RUST-BUG-110
workflow: local
title: Bind ED2K peer service to the HELLO state machine
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, uploads, identity, protocol-parity]
milestone: rust-v0.1.0-beta.2
created: 2026-10-11
source: 2026-10-11 peer-session audit against community eMule, aMule, maintained MFC, ed2k-server, and Lugdunum 17.15
---

# RUST-BUG-110 - Bind ED2K peer service to the HELLO state machine

## Summary

Require an identity-bearing peer HELLO exchange before ordinary ED2K TCP
service and before an outbound promoted upload receives
`OP_ACCEPTUPLOADREQ`. Preserve community eMule interoperability for legacy
`OP_EMULEINFO` preludes, simultaneous HELLO, and the unaffiliated
`OP_PORTTEST` exception. Adopt the maintained MFC improvement that disconnects
a hash-banned identity immediately after HELLO binding.

## Current State

- An inbound peer reaches the shared opcode dispatcher before `OP_HELLO`, so
  metadata, source, queue, and upload handlers can run with socket-only identity.
- A promoted HighID upload is attached and accepted immediately after Rust sends
  `OP_HELLO`; `OP_HELLOANSWER` identity validation happens later.
- HELLO binding records a hash ban only in upload-scoring state and continues
  into HELLO replies, buddy/callback claims, secure-ident, and other services.
- An outbound route expectation is currently conflated with a bound live
  identity for promoted peers, so an initial stale-endpoint mismatch is treated
  as ban-worthy mid-session identity mutation.

## Authority Review

- Community eMule and aMule require inbound `OP_HELLO` before ordinary peer
  dispatch. Community eMule retains unaffiliated `OP_PORTTEST` as the exception.
- Community eMule and aMule withhold promoted upload acceptance until HELLO
  completion. Legacy community eMule can send `OP_EMULEINFO` before
  `OP_HELLOANSWER`, and simultaneous `OP_HELLO` is valid.
- Maintained eMuleBB MFC disconnects hash-banned identities after either HELLO
  form; this is deliberate operational hardening beyond stock behavior.
- ED2K server callbacks create a new peer TCP connection and do not bypass peer
  HELLO. Lugdunum validates the identity answer before final HighID admission.

## Intended Shape

- Track `AwaitingInboundHello`, `AwaitingOutboundHello`, and `Established`
  explicitly in the peer-session owner.
- Permit only identity/handshake packets appropriate to the current direction;
  `OP_EMULEINFO` and `OP_EMULEINFOANSWER` may precede an outbound identity
  answer but must not establish the session.
- Keep route/grant `expected_user_hash` separate from `bound_user_hash`.
  Initial mismatch closes and releases without banning; a later changed HELLO
  after binding remains impersonation and is banned.
- Hold a promoted grant pending until a matching `OP_HELLOANSWER` or simultaneous
  `OP_HELLO` binds the peer, then attach once and send `OP_ACCEPTUPLOADREQ`.
- Release pending grants on EOF, timeout, ban, mismatch, or unexpected packet.

## Acceptance Criteria

- [ ] Hash-banned HELLO identities disconnect before replies or peer-service
      side effects.
- [ ] Inbound ordinary packets before `OP_HELLO` close the connection without
      queue or file-service effects; decoded `OP_PORTTEST` remains supported.
- [ ] Promoted uploads emit no `OP_ACCEPTUPLOADREQ` before a valid identity
      exchange and attach exactly once after matching HELLO completion.
- [ ] Legacy `OP_EMULEINFO` preludes and simultaneous HELLO remain interoperable.
- [ ] Initial expected-hash mismatch closes and releases without adding a ban;
      post-binding hash mutation still bans.
- [ ] Targeted listener tests, `cargo fmt --check`, and focused clippy pass.

## Validation

- Listener integration tests for hash-ban disconnect and pre-HELLO rejection.
- Promotion tests for delayed accept, legacy info prelude, simultaneous HELLO,
  mismatch, EOF, and timeout cleanup.
- Focused `emulebb-ed2k` listener test suite and workspace formatting checks.
