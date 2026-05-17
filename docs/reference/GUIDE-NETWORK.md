# Network Guide

This guide covers eD2K, Kad, listen ports, binding, UPnP, firewall rules,
WebServer/REST listener behavior, geolocation, and network diagnosis.

## Network Surfaces

eMule BB uses the classic eMule network model:

- eD2K server connections for server-indexed search and source discovery
- Kad for decentralized search, source discovery, and firewall state
- TCP for incoming peer/client connections
- UDP for Kad, source exchange, server support traffic, and firewall tests
- optional WebServer/REST listener for trusted local controllers

Low ID, firewalled Kad, or missing listen sockets means the app is running but
is not reachable as intended.

## Bootstrap Sources

New or blank profiles seed practical HTTPS defaults where available:

- `addresses.dat` seeds server.met update URLs when missing or blank
- server.met manual update defaults to a direct machine-readable HTTPS source
- Kad bootstrap defaults to an HTTPS `nodes.dat` source
- IP filter URL history can be seeded separately

Use direct `server.met` and `nodes.dat` files as bootstrap defaults. Avoid HTML
download pages or stale mirrors as built-in sources.

## Ports

Main user-facing ports:

| Port | Purpose |
|---|---|
| TCP client port | incoming peer/client connections |
| UDP client port | Kad and UDP protocol traffic |
| Server UDP port | legacy server UDP support |
| WebServer/REST port | controller and optional legacy web listener |

Changing peer ports while connected can be confusing. After changing TCP or UDP
ports, reconnect or restart the session, then re-run reachability checks.

## Binding Policy

Leave binding empty unless a specific interface or address is required.

Use interface binding when:

- the machine has multiple network interfaces
- a VPN interface must be used for P2P traffic
- startup should block networking if the target interface is unavailable

Use address binding only when:

- the selected interface has multiple IPv4 addresses
- a specific local address must be chosen
- you understand the address can disappear after network changes

Released bind behavior covers peer TCP, client UDP, server UDP, pinger-adjacent
network paths, and UPnP discovery where applicable. The WebServer/REST bind
address is separate from the P2P bind address.

If the configured bind target cannot be resolved, eMule BB reports the active
bind state in UI/diagnostics. With startup bind blocking enabled, P2P networking
stays offline for that session instead of silently falling back.

## VPN And Interface Binding

VPN-aware operation is implemented as explicit bind policy. Configure an
interface target when P2P traffic must use a named VPN adapter, or an address
target when a stable local address is the actual requirement.

Operational rules:

- `BindInterface` names the interface target.
- `BindAddr` is a local address override and should stay empty when the
  interface name is the intended control.
- startup bind blocking can keep P2P networking offline for the session when
  the required target is unavailable.
- WebServer/REST bind address is configured separately under WebServer
  settings.
- a VPN provider's own kill-switch, firewall, and route policy remain external
  controls; do not present eMule BB interface binding as shipped kill-switch
  behavior.

When diagnosing a VPN path, collect the configured bind target, resolved bind
state, selected local address, UPnP result, firewall state, and current Low ID
or Kad firewalled status before changing ports.

## Windows Firewall

The Windows Firewall repair action launches an elevated PowerShell script and
creates broad allow rules for the eMule BB executable:

- inbound TCP
- inbound UDP
- outbound TCP
- outbound UDP
- all profiles
- all local/remote ports and addresses

The repair action deletes exact-name eMule BB rules before recreating them. It
does not remove unrelated legacy rules. The repair result appears in the
elevated PowerShell window and in diagnostic snapshots.

## Microsoft Defender

`Tools > Maintenance > Exclude eMule Download Folders from Microsoft Defender`
launches an elevated one-time PowerShell action. It adds exclusions for the
active Incoming folder, all configured Temp folders, and category-specific
incoming folders.

Use it when Defender scanning is causing heavy disk activity during large
downloads, hashing, or completion moves. The action skips folders already
excluded by Defender and reports added/skipped/error counts in the elevated
PowerShell window and app log.

## UPnP

UPnP can map ports automatically when the router supports it and local policy
allows it. It is useful on home networks but is not a substitute for knowing
the firewall, router, and bind state.

Main P2P UPnP and WebServer UPnP are separate decisions. P2P mapping targets
the peer TCP/client UDP listener pair; WebServer mapping exposes the controller
listener and should be enabled only when that exposure is intentional.

The persisted UPnP settings cover enablement, close-on-exit behavior, and
backend mode. The automatic backend may use the supported router-discovery
implementation for the current build, including IGD-style UPnP and supported
PCP/NAT-PMP paths where present.

If UPnP fails:

1. Confirm the router supports UPnP.
2. Confirm Windows Firewall allows eMule BB.
3. Confirm bind settings point to the expected interface.
4. Confirm the router path is the same path used by the selected bind target.
5. Test manual port forwarding.

UPnP enablement, close-on-exit behavior, and backend mode are persisted under
the `UPnP` section in `preferences.ini`.

## eD2K Status

A healthy eD2K session has:

- connected or intentionally disconnected state
- no unexpected Low ID
- a trusted server list
- stable server.met update source
- TCP reachability through firewall/router/VPN path

Low ID usually points to incoming TCP reachability: firewall, router forwarding,
VPN/bind mismatch, wrong port, or wrong public path after a network change.

## Kad Status

A healthy Kad session has:

- Kad running and connected
- useful contact state after bootstrap settles
- nonzero users/files when expected
- no persistent firewalled state when reachable UDP is expected

Use Kad firewall recheck after changing ports, firewall rules, UPnP, router
mapping, or bind settings.

Kad SafeKad and broader trust-scoring plans remain active backlog/future work
unless marked done in the active index. This product guide documents released
runtime behavior only.

## IPv6 And Kad Roadmap

Current eMule BB product behavior remains stock-compatible IPv4 eD2K/Kad. IPv6
work is future connectivity modernization, not a shipped beta 0.7.3 capability.

The docs intentionally split IPv6 Kad into two tracks:

| Track | Status | Meaning |
|---|---|---|
| Current-network dual-stack compatibility | Active future item: [FEAT-035](../active/items/FEAT-035.md) | Add IPv6-capable endpoints, address abstraction, display, logging, bind policy, and safe source/Kad handoff without breaking today's network |
| Distinct IPv6 Kad network | Exploratory idea: [IDEA-IPV6-KAD-NETWORK](../ideas/IDEA-IPV6-KAD-NETWORK.md) | Consider a separate IPv6 Kad routing/bootstrap space inspired by qBittorrent/libtorrent dual-stack DHT state separation |

qBittorrent is useful here through its libtorrent backend. Libtorrent's DHT
model keeps separate IPv4 and IPv6 bootstrap state, commonly described as
`nodes` and `nodes6`, and BEP 32 treats IPv4 and IPv6 DHTs as distinct routing
tables. That is a strong architecture reference for future state separation,
but it is not permission to copy BitTorrent DHT wire semantics into eMule Kad.

Do not cherry-pick partial eMuleAI IPv6 Kad tag handling into the current
IPv4-shaped Kad path. IPv6 Kad metadata is useful only after transport,
endpoint representation, persistence, search-result delivery, buddy/source
logic, diagnostics, and validation all have an end-to-end design.

## Flood And Abuse Guards

The released TCP listen-socket flood-defense slice keeps the app more resilient
against TCP error flooding without requiring the full future CShield engine.
Security and anti-leecher ideas that are still open remain out of the product
guide until they ship.

Protocol obfuscation, secure ident, spam filters, message validation, and share
visibility settings are persisted preferences and documented in
[Preferences Guide](GUIDE-PREFERENCES.md).

## Geolocation

Geolocation is optional network metadata. It can show peer location data and
uses update settings stored in `preferences.ini`.

Use it as informational context only. It does not prove identity, trust, or
legal status of a peer. If the database is missing or stale, peer transfers
still work.

## WebServer And REST

WebServer and REST share the embedded listener infrastructure but serve
different purposes:

- REST `/api/v1` is the preferred trusted-controller API.
- Legacy template WebServer UI is optional compatibility behavior.
- WebServer bind address and port are separate from P2P bind settings.
- HTTPS requires configured certificate/key files.
- API key authentication protects native REST routes.

Do not expose REST broadly on untrusted networks. Use deliberate binding,
firewall rules, and controller-side API-key handling.

## Diagnostics

For network issues, collect:

- redacted diagnostic snapshot
- current TCP/UDP/WebServer ports
- bind interface/address and resolved bind state
- eD2K server status and Low ID state
- Kad status and firewall state
- UPnP result
- Windows Firewall repair result
- recent log lines around connection attempts

## Troubleshooting

Low ID:

1. Check TCP port.
2. Run open-port test.
3. Repair Windows Firewall rules.
4. Check bind status.
5. Check router/VPN forwarding.
6. Check current server connection.

Kad firewalled:

1. Check UDP port.
2. Confirm Kad is bootstrapped.
3. Run Kad firewall recheck.
4. Check UPnP/router mapping.
5. Check bind target and firewall repair result.

REST fails:

1. Confirm WebServer/REST is enabled.
2. Check bind address and port.
3. Check API key.
4. Confirm route shape in [REST API Contract](../rest/REST-API-CONTRACT.md).
5. Check startup/shutdown lifecycle state.
6. Review logs and diagnostics.
