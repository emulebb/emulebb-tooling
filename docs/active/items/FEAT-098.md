---
id: FEAT-098
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/35
title: Add strict bound public-IP guard for VPN profiles
status: OPEN
priority: Major
category: feature
labels: [vpn, networking, bind-policy, diagnostics, privacy, live-e2e, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-30
source: operator review of split-tunnel VPN public-IP mismatch risk
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/35. This local document is retained as an engineering spec/evidence record.

# FEAT-098 - Add strict bound public-IP guard for VPN profiles

## Summary

Harden explicit VPN/interface-bound profiles by proving that the public IP
observed by eMuleBB belongs to an operator-approved VPN public-IP range.

Current bind policy verifies the local P2P socket path: eMuleBB can resolve a
configured interface such as `hide.me`, bind listeners to its local address,
and apply `IP_UNICAST_IF` where Windows supports it. That is necessary, but it
does not prove that a split-tunnel VPN provider is actually routing
`emulebb.exe` through the VPN public egress path.

This feature adds a guard for explicit VPN binding. The RC1 slice is
interface-first: when enabled, eMuleBB blocks public P2P networking unless the
configured VPN interface is usable and runtime monitoring is armed. A
user-configured public IPv4 CIDR allow-list adds public-exit validation; it is
not required merely to enable the guard.

The remaining post-RC strict work is to centralize more protocol-observed
public-IP evidence after eD2K/Kad connect, centralize peer-connect gating at
the core peer connect primitive, and decide whether a future warning-only mode
is worth shipping.

## Current RC1 Slice

Current shipped behavior uses:

- `VpnGuardMode=Off|Block`
- `VpnGuardAllowedPublicIpCidrs=<optional public IPv4 CIDRs>`

`VpnGuardMode=Block` requires a named P2P bind interface. Empty CIDRs are
valid and mean interface-only guarding. Non-empty CIDRs trigger a bound HTTP
public IPv4 probe before public P2P startup; the first successful provider
response wins and must match the allow-list. Runtime checks repeat after
startup approval and on bind-interface change notifications; runtime failure
closes the app.

Public VPN live campaigns now require operator-local VPN Guard live config
unless the scenario explicitly tests guard-off behavior. The config owns
provider-specific split-tunnel connect, allow-list, check, and restore hooks.

## Intended Shape

1. Add a preference-controlled public-IP guard for explicit interface-bound
   profiles.
2. Let users configure one or more allowed VPN public-IP CIDR ranges.
3. Run a bound HTTP public-IP probe before public P2P connect.
4. Compare eD2K/Kad-reported public IPs against the same CIDR allow-list after
   protocol login or discovery.
5. Gate direct peer connection attempts at `CUpDownClient::TryToConnect()` or
   an equivalent core primitive so download reasks, upload admission, direct
   callbacks, shared-file browse, and queued safe-send paths cannot bypass a
   guarded block.
6. Fail closed in `Block` mode when the guard has a definite public-IP
   mismatch or cannot complete a required public-IP check. Empty CIDRs are
   allowed and mean interface-only guard coverage.
7. Surface the guard state in Network Information, logs, and local controller
   diagnostics.

## Preferences

Current preference surface:

- `VpnGuardMode=Block|Off`
- `VpnGuardAllowedPublicIpCidrs=<comma-or-space-separated public IPv4 CIDRs>`

Default behavior for existing profiles remains `Off`. A profile with a
configured `BindInterface` and `VpnGuardMode=Block` should not connect to the
public P2P network unless the configured interface is usable and runtime
monitoring is armed. If `VpnGuardAllowedPublicIpCidrs` is non-empty, at least
one bound HTTP public-IP probe result must match the allow-list before startup
public P2P is allowed.

Users can turn the guard off for unusual network setups, but public live-test
profiles should keep it in `Block` mode. A future warning-only mode remains
open design work.

## HTTP Public-IP Probe

The HTTP probe must not reuse the current general `HttpTransfer` path if that
path remains intentionally unbound. It needs a narrow bound probe path that uses
the same resolved P2P bind decision as the P2P sockets:

- bind to the resolved local P2P address where applicable
- apply the resolved interface index with `IP_UNICAST_IF` where supported
- call configured public IPv4 echo URLs in order
- accept only a plain valid public IPv4 result
- compare the result to the CIDR allow-list

The current RC1 slice uses built-in HTTP IPv4 echo providers and accepts the
first valid public IPv4 result. Future work may make the provider list
configurable if operators need it.

## eD2K And Kad Public-IP Verification

Existing public-IP sources should feed the same guard:

- eD2K server-reported public IP during login and LowID handling
- peer `OP_PUBLICIP_ANSWER` responses
- Kad public IPv4 state when available

This is remaining post-RC strict work. If a protocol-observed public IP is
outside the allowed CIDR list in `Block` mode, eMuleBB should disconnect or
block public P2P for the session and report the mismatch. A future `Warn` mode
would log and surface the mismatch without disconnecting if that mode is
accepted.

## Scope Constraints

- Do not hardcode hide.me behavior in the app. Provider-specific split-tunnel
  registration and restart remain Python harness or operator responsibilities.
- Do not write `hide.me` into `BindAddr`; explicit interface binding remains
  `BindInterface=hide.me` with an empty P2P `BindAddr` for hide.me profiles.
- Do not claim this is a full VPN kill switch. It is an app-level public-IP
  guard for public P2P networking.
- Do not rely only on toolbar, web, REST, or Kad/server start-command gates.
  Any peer-level path that can open a public TCP or callback path must inherit
  the same guard decision from the core connect primitive.
- Do not use adapter name, local VPN address, route table, UPnP success, LowID,
  or interface metrics as proof of VPN public egress by themselves.
- Keep WebServer/REST binding separate from P2P bind policy.
- Keep default eD2K/Kad wire behavior stock-compatible; this item changes
  local connect gating and diagnostics, not protocol semantics.

## Diagnostics

Expose low-cardinality guard evidence:

- configured guard mode
- configured CIDR allow-list status, redacted where needed
- resolved P2P bind interface, address, and interface index
- last HTTP probe result and decision
- last eD2K/Kad observed public IP and decision
- final guard state: unchecked, checking, matched, mismatched, unavailable, or
  disabled
- reason for any block or warning

An optional unbound or router-WAN public-IP can be shown as a canary if it is
clearly labeled as diagnostic-only. It must not replace the CIDR allow-list as
the enforcement source of truth.

## Test And Harness Expectations

The Python live-wire and materialized-install harnesses should be able to seed
`VpnGuardAllowedPublicIpCidrs` into test profiles from local operator config.
This lets public live E2E runs prove:

- installer-backed profiles still use `BindInterface=hide.me`
- P2P `BindAddr` remains empty unless the operator explicitly chooses an
  address bind
- the executable is present in developer-local hide.me split-tunnel config when
  that opt-in harness feature is enabled
- HTTP public-IP probe matches the allowed CIDR list before connect when CIDRs
  are configured
- eD2K/Kad observed public IP matches the allowed CIDR list after connect when
  post-RC protocol-observed verification lands
- mismatch failures collect logs, REST status, Network Information evidence,
  and live-wire config redacted evidence

## Acceptance Criteria

- [x] Preferences persist guard mode and allowed CIDRs.
- [x] CIDR parsing accepts valid IPv4 CIDRs and rejects malformed or private-only
      enforcement lists with clear diagnostics.
- [x] Bound HTTP public-IP probe uses the explicit P2P bind decision instead of
      the unbound general HTTP helper.
- [x] `Block` mode permits interface-only guard when no allowed CIDR is
      configured for an explicit VPN-bound profile.
- [x] `Block` mode blocks startup public P2P when required HTTP public-IP
      evidence is outside the allow-list or unavailable.
- [ ] `Block` mode prevents or tears down public P2P when eD2K, peer, or Kad
      public-IP evidence is outside the allow-list.
- [ ] Peer-level connect attempts are centrally guard-gated so reasks, upload
      admission, callbacks, shared-file browse, and queued safe-send paths
      cannot bypass a VPN Guard block or unarmed runtime monitor.
- [ ] `Warn` mode records the same evidence without blocking if accepted for a
      future release.
- [x] Network Information, logs, and REST status expose the guard decision and
      startup block evidence.
- [x] Live-wire tests can seed allowed CIDRs and fail closed on mismatch without
      adding new PowerShell scripts.

## Validation

- `python -m emule_workspace validate`
- focused native tests for IPv4/CIDR parsing and match decisions
- seam tests for bound HTTP probe success, mismatch, timeout, malformed
  response, and endpoint fallback
- live-wire public-network smoke with `BindInterface=hide.me`, empty P2P
  `BindAddr`, and an allowed CIDR list
- negative harness proof that a mismatching public IP fails closed and reports
  actionable evidence
