# Network Guide

This guide covers eD2K, Kad, listen ports, binding, UPnP, firewall rules,
WebServer/REST listener behavior, geolocation, and network diagnosis.

## Network Surfaces

eMuleBB uses the classic eMule network model:

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

## P2P Binding Policy

Leave binding empty unless a specific interface or address is required.

Use interface binding when:

- the machine has multiple network interfaces
- a VPN interface must be used for P2P traffic
- startup should block networking if the target interface is unavailable

Use address binding only when:

- the selected interface has multiple IPv4 addresses
- a specific local address must be chosen
- you understand the address can disappear after network changes

eMuleBB treats P2P binding as an active connectivity policy. When a named
interface is configured, the P2P stack resolves that interface to its current
IPv4 address and adapter index, then uses both pieces of information for P2P
socket setup. That means the listener bind selects the local address, and the
Windows `IP_UNICAST_IF` socket option pins IPv4 egress to the resolved adapter
where Windows supports it.

Released bind behavior covers peer TCP, client UDP, server UDP,
pinger-adjacent network paths, layered/proxy TCP paths, and UPnP discovery where
applicable. The WebServer/REST bind address is intentionally separate from the
P2P bind address.

Binding is not a VPN kill switch. It chooses and verifies the local P2P socket
path that eMuleBB controls; it does not replace the VPN provider, Windows
Firewall, routing table, or external leak-prevention policy. Treat WebServer,
REST, UPnP discovery, and LAN/controller exposure as separate surfaces.

If the configured bind target cannot be resolved, eMuleBB reports the active
bind state in UI/diagnostics. With startup bind blocking enabled, P2P networking
stays offline for that session instead of using an unintended route.

Released bind coverage:

| Surface | Behavior |
|---|---|
| Peer TCP listener | Uses the active P2P bind target when configured |
| Client UDP listener | Uses the active P2P bind target when configured |
| Server UDP support | Uses the active P2P bind target where the server path needs local UDP |
| IPv4 egress interface | Uses `IP_UNICAST_IF` when a named bind interface resolves to an adapter index |
| Layered/proxy TCP paths | Apply the same local bind and adapter-index selection as direct peer TCP paths |
| Pinger-adjacent network paths | Keep the same resolved bind decision where applicable |
| UPnP discovery/mapping | Runs against the selected P2P path where the backend supports it |
| WebServer/REST | Uses its own WebServer bind address, not the P2P bind address |

## VPN And Interface Binding

VPN-aware operation is implemented as explicit bind policy. Configure an
interface target when P2P traffic must use a named VPN adapter, or an address
target when a stable local address is the actual requirement.

Operational rules:

- `BindInterface` names the interface target.
- `BindAddr` is a local address override and should stay empty when the
  interface name is the intended control.
- named interface binding resolves both the IPv4 address and adapter index; if
  `IP_UNICAST_IF` cannot be applied to required P2P sockets, that socket path
  fails closed instead of using an unintended route.
- startup bind blocking can keep P2P networking offline for the session when
  the required target is unavailable.
- `ExitOnBindInterfaceLoss` can close the app if the resolved configured
  interface is lost during runtime; it is an app lifecycle safety option, not
  VPN route enforcement.
- WebServer/REST bind address is configured separately under WebServer
  settings.
- VPN kill-switch, firewall, and route enforcement remain external operator or
  provider controls; eMuleBB interface binding is not a kill switch.

When diagnosing a VPN path, collect the configured bind target, resolved bind
state, selected local address, UPnP result, firewall state, and current Low ID
or Kad firewalled status before changing ports.

Recommended VPN-profile shape:

| Setting | Recommended value |
|---|---|
| `BindInterface` | VPN adapter/interface name when interface binding is the policy |
| `BindAddr` | Empty unless a specific stable local address is required |
| Startup bind blocking | Enabled when P2P traffic must not start without the configured interface |
| Exit on bind loss | Optional, depending on operator preference for closing the desktop app after interface loss |
| WebServer bind | Usually loopback or another deliberate controller interface, configured separately |

Practical verification is straightforward:

1. Confirm diagnostics show the expected `BindInterface` and resolved P2P local
   address.
2. Confirm live TCP/UDP P2P sockets are bound to the resolved interface address.
3. Capture the VPN and physical adapters during active peer traffic.
4. Expect eD2K/Kad peer traffic on the selected adapter and no matching P2P
   listener or peer-port traffic on the physical adapter.
5. Classify WebServer/REST, UPnP discovery, LAN multicast, and the VPN tunnel
   itself separately from public P2P traffic.

## Windows Firewall

The Windows Firewall repair action launches an elevated PowerShell script and
creates broad allow rules for the eMuleBB executable:

- inbound TCP
- inbound UDP
- outbound TCP
- outbound UDP
- all profiles
- all local/remote ports and addresses

The repair action deletes exact-name eMuleBB rules before recreating them. It
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

Release-facing UPnP settings:

| Setting | Scope | Meaning |
|---|---|---|
| `[UPnP] EnableUPnP` | P2P listener mapping | Enables automatic mapping for the peer TCP/client UDP listener pair |
| `[UPnP] CloseUPnPOnExit` | P2P listener mapping | Requests removal of mappings on app exit when the backend supports it |
| `[UPnP] BackendMode` | P2P listener mapping | Selects automatic, IGD-only, or PCP/NAT-PMP-only backend behavior |
| `[WebServer] WebUseUPnP` | WebServer/REST listener mapping | Separately controls WebServer/REST exposure through UPnP |

If UPnP fails:

1. Confirm the router supports UPnP.
2. Confirm Windows Firewall allows eMuleBB.
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

## Source Exchange Compatibility

Live Source Exchange is SX2-only in eMuleBB. The old SX1 live-network advertise,
request, response, and version-tracking paths are intentionally absent.

Do not treat missing live `OP_REQUESTSOURCES` or `OP_ANSWERSOURCES` SX1 support
as a protocol regression. Local eD2K-link source import remains separate from
live SX1 packet support. The durable decision record is
[REF-002](../history/items/REF-002.md).

## IPv6 And Kad Roadmap

Current eMuleBB product behavior remains stock-compatible IPv4 eD2K/Kad. IPv6
work is future connectivity modernization, not a shipped 0.7.3 RC1 capability.

The docs intentionally split IPv6 Kad into two tracks:

- **Current-network dual-stack compatibility**
  - Status: Active future item: [FEAT-035](../active/items/FEAT-035.md)
  - Meaning: Add IPv6-capable endpoints, address abstraction, display, logging, bind
             policy, and safe source/Kad handoff without breaking today's network

- **Distinct IPv6 Kad network**
  - Status: Exploratory idea: [IDEA-IPV6-KAD-NETWORK](../ideas/IDEA-IPV6-KAD-NETWORK.md)
  - Meaning: Consider a separate IPv6 Kad routing/bootstrap space inspired by
             qBittorrent/libtorrent dual-stack DHT state separation

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
