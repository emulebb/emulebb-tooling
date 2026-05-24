---
id: FEAT-086
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/33
title: Parse eMuleAI extension hints without advertising protocol support
status: OPEN
priority: Minor
category: feature
labels: [emuleai, ipv6, nat-traversal, protocol-compatibility, diagnostics]
milestone: post-0.7.3
created: 2026-05-24
source: operator compatibility review of eMuleAI private IPv6 and NAT traversal protocol surface
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/33. This local document is retained as an engineering spec/evidence record.

# FEAT-086 - Parse eMuleAI Extension Hints Without Advertising Protocol Support

## Summary

Make eMuleBB tolerant of selected eMuleAI-style IPv6, NAT traversal, and
extended-source metadata when those fields are received from remote peers, while
keeping eMuleBB's own public protocol behavior stock-compatible.

This item is receive-only compatibility. It does not implement the full
eMuleAI IPv6 line, does not join an eMuleAI-specific protocol fork, and does
not advertise eMuleAI capabilities to the network.

The practical goal is:

- eMuleBB does not break or misparse when an eMuleAI peer sends private
  extension hints
- those hints can feed diagnostics, counters, and future implementation
  evidence
- no eMuleAI-specific tag, opcode, or capability is emitted by eMuleBB until a
  later feature implements an end-to-end compatible behavior

This item refines [FEAT-035](FEAT-035.md) and [FEAT-036](FEAT-036.md). Those
items own the full IPv6 and NAT traversal product direction. `FEAT-086` owns
the narrower "compatible but not advertising" stance.

## eMuleAI Protocol Surface Reviewed

The eMuleAI implementation is not a separate IPv6 Kad network. It is mostly the
current eD2K/Kad protocol with IPv6 side metadata and private mod extensions.

Important observed pieces:

- `CAddress` stores none, IPv4, and IPv6 addresses in a 16-byte representation,
  with IPv4 mapped into IPv4-mapped IPv6 form.
- Sockets are opened as dual-stack `AF_INET6` sockets with `IPV6_V6ONLY`
  disabled where possible.
- Public IPv6 detection scans local adapters with `GetAdaptersAddresses(AF_INET6)`
  and also consumes peer-reported "your IP" information as a heuristic.
- The hello/client metadata path advertises IPv6 and NAT capability through
  private mod fields.
- Kad publish and source paths can carry IPv6 values as private tags.
- Some paths use IPv4-era sentinel values, including `UINT_MAX`, to represent
  an IPv6 HighID-style state.

Private eMuleAI constants and tag names observed:

| Name | Value / tag | Role |
|---|---:|---|
| `CT_MOD_MISCOPTIONS` | `0xAA` | Private capability bitfield for IPv6, NAT traversal, and extended source hints |
| `OP_CHANGE_CLIENT_IP` | `0xAC` | Private client IP change/update opcode |
| `CT_MOD_YOUR_IP` | `0xAD` | Private "your IP" metadata, including IPv6 forms |
| `CT_MOD_IP_V6` | `0xAE` | Private remote IPv6 address hint |
| `CT_MOD_SVR_IP_V6` | `0xAF` | Private server IPv6 hint |
| `TAG_IPV6` | `ip6` | Private Kad/source IPv6 endpoint tag |
| `TAG_SERVINGBUDDYIPV6` | `bi6` | Private serving-buddy IPv6 tag |

These constants are useful as a parsing map. They are not approved as eMuleBB
advertisement or publication behavior.

## Compatibility Stance

eMuleBB may be eMuleAI-tolerant without claiming eMuleAI protocol support.

Allowed:

- parse selected private tags/opcodes only when received
- store parsed values as local, non-authoritative hints
- expose aggregate diagnostics and counters for engineering review
- use the data to design future IPv6 and NAT traversal work
- ignore unknown or malformed private fields without disconnecting a peer
  unless the packet is otherwise invalid or abusive

Not allowed by this item:

- send eMuleAI capability bits
- publish eMuleAI IPv6 or serving-buddy tags into Kad
- send `CT_MOD_IP_V6`
- send IPv6 `CT_MOD_YOUR_IP`
- send or act on `OP_CHANGE_CLIENT_IP`
- forward eMuleAI private metadata to third-party peers
- claim `SupportsIPv6`, `SupportsNatTraversal`, or `SupportsExtendedXS` in
  `CT_MOD_MISCOPTIONS`
- change connection, routing, source, or Kad decisions solely because an
  unauthenticated eMuleAI hint was received

## Receive-Only Parsing Plan

### `CT_MOD_MISCOPTIONS`

Parse the private bitfield when present and record only local capability hints:

- remote peer appears to claim IPv6 support
- remote peer appears to claim NAT traversal support
- remote peer appears to claim extended source exchange support

The data should be treated as an untrusted peer claim. It may increment
diagnostic counters and appear in debug logs, but it must not enable outbound
private protocol behavior.

### `CT_MOD_IP_V6`

Parse and store the remote IPv6 hint in a quarantined peer-extension record.
The hint must not override the proven socket address and must not be published
to other peers.

Future IPv6 implementation work may use this as evidence, but this item should
not dial IPv6 solely because the private hint exists.

### IPv6 `CT_MOD_YOUR_IP`

Parse only for diagnostics. Peer-reported local address data is not
authoritative and can be wrong under VPNs, NAT, multi-homing, privacy
extensions, or malicious peers.

### `TAG_IPV6` / `ip6`

When encountered in Kad or source metadata, parse the value only as a
quarantined source hint. Do not publish the tag, do not relay it, and do not
feed it into ordinary IPv4 source availability without a future end-to-end IPv6
consumer path.

### `TAG_SERVINGBUDDYIPV6` / `bi6`

Parse and log as a private eMuleAI serving-buddy hint. Do not use it for
serving-buddy selection, relay decisions, or third-party publication.

### `CT_EMULE_SERVINGBUDDYIPV6`

If this private client metadata appears, parse and log it only. Any relay or
serving-buddy behavior belongs to [FEAT-036](FEAT-036.md), not this receive-only
item.

### `OP_CHANGE_CLIENT_IP`

Ignore and log initially. Acting on this opcode would let a remote peer mutate
address state through a private extension without an eMuleBB authentication,
context, or replay design.

### eServer Buddy Relay Opcodes

Ignore and log initially. eServer Buddy relay behavior changes reachability and
abuse surfaces, so it belongs to the explicit NAT traversal design in
[FEAT-036](FEAT-036.md).

### uTP Packets

Do not treat uTP as part of this item. If eMuleAI-style uTP packets are
observed, record them only as packet-class evidence. Actual uTP support belongs
to [FEAT-018](FEAT-018.md) after UDP demultiplexing, congestion behavior, and
fallback semantics are designed.

## Suggested Internal Shape

Use a private, non-persisted peer-extension record similar to:

```cpp
struct PeerExtensionHints {
    bool sawEmuleAIStyleMiscOptions = false;
    bool remoteClaimsIPv6 = false;
    bool remoteClaimsNatTraversal = false;
    bool remoteClaimsExtendedXS = false;
    CAddress remoteIPv6Hint;
    CAddress observedOwnIPv6Hint;
    CAddress servingBuddyIPv6Hint;
};
```

The exact address type will depend on [FEAT-035](FEAT-035.md). If eMuleBB does
not yet have a first-class dual-stack address abstraction when this item is
implemented, the parser should keep raw validated bytes plus diagnostic
formatting instead of forcing IPv6 data into IPv4-era fields.

## Robustness Rules

- Bound every parsed extension length before reading.
- Reject malformed IPv6 payloads without crashing or corrupting peer state.
- Never reinterpret a 32-bit IPv4 ID as an IPv6 endpoint.
- Do not persist private hints in `.met` or `.dat` profile files.
- Do not expose private hints through stable REST fields until the REST
  contract explicitly models them as diagnostics.
- Keep logging rate-limited so a peer cannot flood debug output with private
  extension noise.
- Keep disabled/default network behavior indistinguishable from current
  community-compatible eMuleBB behavior.

## Diagnostics

Add aggregate counters when implemented:

- eMuleAI-style misc-options blocks seen
- peers claiming IPv6 support
- IPv6 address hints seen
- IPv6 "your IP" hints seen
- peers claiming NAT traversal support
- serving-buddy IPv6 hints seen
- ignored private IP-change opcodes
- ignored eServer Buddy relay opcodes
- malformed private extension payloads

These counters should be low-cardinality and should not retain peer-identifying
data by default.

## Compatibility Risks

The main risk is accidental protocol advertisement. If eMuleBB sets an eMuleAI
support bit or republishes an eMuleAI private tag before the consumer path is
complete, remote peers may assume eMuleBB implements behavior it does not
actually provide.

Secondary risks:

- treating untrusted peer-reported IPv6 as authoritative
- mixing IPv4 source IDs and IPv6 endpoints in legacy structures
- creating silent divergence from stock Kad/source behavior
- logging peer-provided private metadata too aggressively
- adding compatibility code that later conflicts with the real dual-stack
  design

## Implementation Plan

1. Add parse-only constants and comments that identify the fields as eMuleAI
   private compatibility input, not eMuleBB advertisement.
2. Add a peer-local extension-hint record with no persistence and no outbound
   propagation.
3. Parse `CT_MOD_MISCOPTIONS` into boolean diagnostic hints.
4. Parse `CT_MOD_IP_V6` and IPv6 `CT_MOD_YOUR_IP` into quarantined address
   hints.
5. Parse `TAG_IPV6` and `TAG_SERVINGBUDDYIPV6` as quarantined Kad/source hints.
6. Ignore and count `OP_CHANGE_CLIENT_IP` and private relay opcodes.
7. Add malformed-payload tests and packet fixtures for every accepted parser.
8. Add packet-capture or harness evidence showing eMuleBB sends no eMuleAI
   private support bits, tags, or opcodes by default.

## Acceptance Criteria

- [ ] eMuleAI private extension constants are documented in source as
      receive-only compatibility input.
- [ ] Valid eMuleAI-style hints can be parsed without disconnecting or
      corrupting peer state.
- [ ] Malformed private hints are bounded, ignored, and counted.
- [ ] eMuleBB does not send eMuleAI capability bits, IPv6 private tags, private
      IP-change opcodes, or serving-buddy IPv6 tags.
- [ ] Parsed hints are not persisted into `.met` or `.dat` files.
- [ ] Parsed hints are not forwarded to third-party peers.
- [ ] Diagnostics expose only aggregate counts unless a future explicit debug
      mode is approved.
- [ ] Packet-capture or protocol-harness evidence proves default outbound
      behavior remains stock-compatible.

## Validation

- Focused unit tests for every parser with valid, malformed, oversized, and
  truncated payloads.
- Protocol golden tests confirming outbound hello, Kad publish, and source
  exchange packets do not include eMuleAI private fields by default.
- Live interop smoke against an eMuleAI peer if available, limited to observing
  tolerance and diagnostics.
- `python scripts/docs-item-taxonomy-check.py` and
  `python scripts/docs-structure-check.py --fail-on-wide-tables` from
  `repos/emulebb-tooling`.
