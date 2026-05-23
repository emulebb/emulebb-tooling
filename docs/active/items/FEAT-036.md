---
id: FEAT-036
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/15
title: NAT traversal and extended source exchange for LowID-to-LowID connectivity
status: OPEN
priority: Major
category: feature
labels: [networking, nat-traversal, lowid, source-exchange, relay, udp, connectivity]
milestone: ~
created: 2026-04-20
source: eMuleAI release notes; eMule Qt announcement 2026-03-05
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/15. This local document is retained as an engineering spec/evidence record.

## Summary

Add a broader connectivity layer for LowID-to-LowID sessions instead of relying almost
entirely on the classic open-port assumption.

This is a major product-expansion feature. It goes well beyond stock behavior by combining
relay-assisted signaling, hole-punch attempts, and richer source metadata so difficult
network topologies can still connect more often.

## Why Add It

LowID, VPN, UDP, and NAT problems remain one of the most visible current user pain points.
eMuleAI explicitly targets this with buddy/relay and traversal work, while eMule Qt now
lists NAT traversal as an upcoming community-requested feature.

## Intended Mainline Shape

- add relay-assisted signaling for LowID-to-LowID setup
- retain Kad buddy rendezvous where helpful, but do not stop there
- add stronger UDP hole-punch attempts and clearer traversal diagnostics
- extend source exchange metadata so peers can advertise traversal-relevant state more
  effectively
- keep relay traffic control-plane only; file data should remain direct whenever possible
- expose the feature as optional/advanced while the line matures

## Scope Constraints

- coordinate with `FEAT-018` instead of forking a second transport strategy
- coordinate with `FEAT-032` so port-mapping and traversal policy are one coherent stack
- do not assume server-side NAT extensions are available
- keep security review front-and-center because this changes network reachability
- treat the eMuleAI protocol surface as prior art only, not as an approved
  wire-format authority
- do not direct-port private opcodes, private tag meanings, or default-on
  retry/routing behavior without a written eMuleBB protocol note and parity
  evidence against the community baseline

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- Private NAT/eServer Buddy opcode definitions:
  [`Opcodes.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/Opcodes.h#L329)
  and IPv6/NAT extension tag area:
  [`Opcodes.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/Opcodes.h#L643).
- NAT traversal preference defaults and persistence:
  [`Preferences.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/Preferences.cpp#L3766)
  and options-page save/load wiring:
  [`PPgMod.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/PPgMod.cpp#L1516).
- Client capability advertisement and serving-buddy exchange:
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L5382),
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6166),
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6195).
- eServer Buddy request/proof/relay helpers:
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6280),
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6381),
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6451),
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6593),
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6667),
  [`BaseClient.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/BaseClient.cpp#L6804).
- Client-list buddy selection and relay bookkeeping:
  [`ClientList.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientList.h#L233),
  [`ClientList.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientList.cpp#L2581).
- Listen-socket handling of private relay/control packets:
  [`ListenSocket.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ListenSocket.cpp#L2139).
- Magic-file proof/source-answer behavior used by the server-buddy path:
  [`SharedFileList.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/SharedFileList.cpp#L184).

## Protocol Change Notes

eMuleAI does more than a local connectivity improvement. It creates a private
mod protocol surface around NAT traversal:

- New or repurposed ED2K/client opcodes are introduced for serving-buddy,
  eServer Buddy, rendezvous, hole-punch, and client-IP-change flows. These
  opcodes are not stock/community eMule wire semantics and must not be
  copied into eMuleBB without an explicit compatibility design.
- The implementation adds NAT and serving-buddy capability advertisement to
  client capability exchange. eMuleBB must define how legacy peers ignore the
  fields, how upgraded peers negotiate them, and how downgrade behavior stays
  indistinguishable from stock when disabled.
- eServer Buddy uses proof material, relay request state, and "magic file"
  source-answer behavior. This changes peer reachability decisions and creates
  abuse risk if not bounded, rate-limited, and observable.
- eMuleAI defaults NAT traversal on. eMuleBB should not. The first eMuleBB
  implementation should be advanced/opt-in until public-network packet
  captures prove that disabled behavior remains stock-compatible and enabled
  behavior fails closed with legacy peers.
- eMuleAI retry behavior can keep sources alive after failed TCP connection
  attempts before normal dead-source handling. That may improve LowID
  connectivity, but it is also scheduling drift. It belongs in this item only
  if measured against stock baseline behavior.

The approved eMuleBB shape is therefore: local diagnostics, bounded
control-plane signaling, explicit negotiation, clean fallback, packet-capture
goldens, and no silent protocol fork.

## Acceptance Criteria

- [ ] LowID-to-LowID setup succeeds on at least one new traversal path beyond stock behavior
- [ ] relay-assisted signaling remains bounded and control-only
- [ ] traversal diagnostics clearly explain which path succeeded or failed
- [ ] source exchange can carry the extra metadata needed for the feature
- [ ] opt-out and fallback to classic behavior remain available
- [ ] protocol design note documents every new or reused opcode/tag before
      implementation
- [ ] packet-capture evidence shows disabled behavior matches community eMule
      behavior
