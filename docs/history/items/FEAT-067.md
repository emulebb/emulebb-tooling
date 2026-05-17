---
id: FEAT-067
title: External VPN kill-switch watchdog
status: WONT_DO
priority: Minor
category: feature
labels: [vpn, networking, bind-policy, documentation]
milestone: ~
created: 2026-05-17
source: retired exploratory VPN kill-switch idea
---

# FEAT-067 - External VPN Kill-Switch Watchdog

## Decision

**Abandoned.** eMule BB will not pursue an external VPN kill-switch/watchdog
helper as a product feature, sidecar, or active roadmap item.

## Rationale

eMule BB already has the product boundary needed for release: provider-neutral
interface/address binding, startup bind blocking, resolved bind diagnostics,
and separate WebServer bind policy. A process-killing watchdog would be a
broader machine policy tool, not an eMule feature. VPN provider kill switches,
firewall rules, route policy, and OS-level enforcement remain operator-owned
external controls.

## Preserved Provenance

The retired idea explored a standalone helper that would:

- monitor a configured VPN interface/address/route
- treat unknown VPN health as unsafe
- discover protected P2P processes such as `emule.exe`
- request graceful shutdown and then force termination
- write an audit log for VPN health transitions and process action

This remains historical analysis only. Do not promote it as current product
direction without opening a new active item and explicitly overriding this
`WONT_DO` decision.

## Product Documentation Rule

Product docs may describe eMule BB bind policy and diagnostics. They must not
describe a maintained eMule BB VPN kill-switch helper or watchdog. If users
require kill-switch semantics, point them to external VPN-provider, firewall,
or OS policy outside the eMule BB product claim.
