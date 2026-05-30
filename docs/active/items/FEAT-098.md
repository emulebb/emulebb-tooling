---
id: FEAT-098
title: Add strict bound public-IP guard for VPN profiles
status: OPEN
priority: Major
category: feature
labels: [vpn, networking, bind-policy, diagnostics, privacy, live-e2e, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-30
source: operator review of split-tunnel VPN public-IP mismatch risk
---

# FEAT-098 - Add Strict Bound Public-IP Guard For VPN Profiles

## Summary

Harden explicit VPN/interface-bound profiles by proving that the public IP
observed by eMuleBB belongs to an operator-approved VPN public-IP range.

Current bind policy verifies the local P2P socket path: eMuleBB can resolve a
configured interface such as `hide.me`, bind listeners to its local address,
and apply `IP_UNICAST_IF` where Windows supports it. That is necessary, but it
does not prove that a split-tunnel VPN provider is actually routing
`emulebb.exe` through the VPN public egress path.

This feature adds a strict guard for explicit VPN binding. When enabled, eMuleBB
must compare observed public IPv4 addresses against a user-configured CIDR
allow-list and block public P2P networking if the observed address does not
match.

## Intended Shape

1. Add a preference-controlled public-IP guard for explicit interface-bound
   profiles.
2. Let users configure one or more allowed VPN public-IP CIDR ranges.
3. Run a bound HTTP public-IP probe before public P2P connect.
4. Compare eD2K/Kad-reported public IPs against the same CIDR allow-list after
   protocol login or discovery.
5. Fail closed in strict mode when the guard has a definite mismatch, no usable
   CIDR allow-list, or cannot complete the required public-IP check.
6. Surface the guard state in Network Information, logs, and local controller
   diagnostics.

## Preferences

Suggested preference surface:

- `BoundPublicIPGuardMode=Block|Warn|Off`
- `BoundPublicIPAllowedCIDRs=<comma-or-space-separated IPv4 CIDRs>`
- `BoundPublicIPCheckUrls=<ordered public IPv4 echo URLs>`

Default behavior should be strict for explicit VPN binding. A profile with a
configured `BindInterface` and guard mode `Block` should not connect to the
public P2P network unless at least one observed public IP matches
`BoundPublicIPAllowedCIDRs`.

Users must be able to turn the guard off or set it to warning-only for unusual
network setups, but public live-test profiles should keep it strict.

## HTTP Public-IP Probe

The HTTP probe must not reuse the current general `HttpTransfer` path if that
path remains intentionally unbound. It needs a narrow bound probe path that uses
the same resolved P2P bind decision as the P2P sockets:

- bind to the resolved local P2P address where applicable
- apply the resolved interface index with `IP_UNICAST_IF` where supported
- call configured public IPv4 echo URLs in order
- accept only a plain valid public IPv4 result
- compare the result to the CIDR allow-list

Built-in default check URLs are acceptable for first-run usability, but the
list must remain configurable. The app should log which endpoint family was
used without treating any specific provider as authoritative.

## eD2K And Kad Public-IP Verification

Existing public-IP sources should feed the same guard:

- eD2K server-reported public IP during login and LowID handling
- peer `OP_PUBLICIP_ANSWER` responses
- Kad public IPv4 state when available

If a protocol-observed public IP is outside the allowed CIDR list in `Block`
mode, eMuleBB should disconnect or block public P2P for the session and report
the mismatch. In `Warn` mode, it should log and surface the mismatch without
disconnecting.

## Scope Constraints

- Do not hardcode hide.me behavior in the app. Provider-specific split-tunnel
  registration and restart remain Python harness or operator responsibilities.
- Do not write `hide.me` into `BindAddr`; explicit interface binding remains
  `BindInterface=hide.me` with an empty P2P `BindAddr` for hide.me profiles.
- Do not claim this is a full VPN kill switch. It is an app-level public-IP
  guard for public P2P networking.
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
`BoundPublicIPAllowedCIDRs` into test profiles from local operator config. This
lets public live E2E runs prove:

- installer-backed profiles still use `BindInterface=hide.me`
- P2P `BindAddr` remains empty unless the operator explicitly chooses an
  address bind
- the executable is present in developer-local hide.me split-tunnel config when
  that opt-in harness feature is enabled
- HTTP public-IP probe matches the allowed CIDR list before connect
- eD2K/Kad observed public IP matches the allowed CIDR list after connect
- mismatch failures collect logs, REST status, Network Information evidence,
  and live-wire config redacted evidence

## Acceptance Criteria

- [ ] Preferences persist guard mode, allowed CIDRs, and public-IP check URLs.
- [ ] CIDR parsing accepts valid IPv4 CIDRs and rejects malformed or private-only
      enforcement lists with clear diagnostics.
- [ ] Bound HTTP public-IP probe uses the explicit P2P bind decision instead of
      the unbound general HTTP helper.
- [ ] `Block` mode prevents public P2P connect when no allowed CIDR is
      configured for an explicit VPN-bound profile.
- [ ] `Block` mode prevents or tears down public P2P when HTTP, eD2K, peer, or
      Kad public-IP evidence is outside the allow-list.
- [ ] `Warn` mode records the same evidence without blocking.
- [ ] Network Information, logs, and REST status expose the guard decision and
      last observed public-IP evidence.
- [ ] Live-wire tests can seed allowed CIDRs and fail closed on mismatch without
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
