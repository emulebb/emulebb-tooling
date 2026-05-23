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

## Acceptance Criteria

- [ ] LowID-to-LowID setup succeeds on at least one new traversal path beyond stock behavior
- [ ] relay-assisted signaling remains bounded and control-only
- [ ] traversal diagnostics clearly explain which path succeeded or failed
- [ ] source exchange can carry the extra metadata needed for the feature
- [ ] opt-out and fallback to classic behavior remain available
