---
id: RUST-FEAT-035
workflow: local
title: Kad - FINDSOURCE callback fallback for an unknown buddy endpoint
status: DONE
priority: Major
category: feature
labels: [kad, callback, traversal, parity]
milestone: release-0.1.0-beta.1
created: 2026-07-10
source: Rust versus MFC protocol and state-machine parity audit
---

# RUST-FEAT-035 - Kad FINDSOURCE callback fallback

## Outcome

Rust now mirrors MFC's fallback for a firewalled LowID source whose buddy ID is
known but whose buddy IP and UDP port are not. A value-count Kad traversal near
the buddy ID sends the existing 34-byte `KADEMLIA_CALLBACK_REQ` to at most 20
eligible contacts. The active traversal runs for 25 seconds, leaving MFC's final
20 seconds of the 45-second lifecycle for late callback delivery.

The download flow registers the callback intent before launching the traversal,
deduplicates concurrent source/file attempts, and retains the existing 45-second
callback cooldown. Direct callback remains preferred when the buddy endpoint is
already known.

## Evidence

- emulebb-rust commit `41b139a`.
- Focused DHT tests cover the value request count, callback packet selection,
  and 25-second active budget.
- Core callback tests cover unknown-endpoint candidacy, cooldown, and exact wire
  serialization.
- Scoped `cargo check` and warning-free clippy passed on 2026-07-10.
