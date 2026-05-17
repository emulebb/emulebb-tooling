# eMule BB Product Guide

eMule BB is the broadband edition of classic eMule. It keeps the native Windows
desktop workflow and stock-compatible eD2K/Kad behavior while adding modern
defaults, stronger profile handling, large-library support, diagnostics, and a
trusted local REST/controller surface.

This is the product manual entry point. It links to focused guide chapters and
summarizes the behavior that matters when operating the app.

## Audience

eMule BB is for users and operators who want a long-running native eMule client:

- power users with sustained broadband upload capacity
- archivists and seeders with large shared libraries
- users who need explicit firewall, bind, UPnP, and IP-filter behavior
- operators using trusted local controllers through REST
- contributors who need reproducible diagnostics and documented runtime rules

It is not a rewrite and not a headless daemon. The desktop app owns the live
state; REST and companion tools adapt to that state.

## Install And Profile Model

Keep these locations conceptually separate:

| Location | Purpose |
|---|---|
| Application directory | Executable, bundled assets, WebServer templates, skins, toolbar assets |
| Config/profile directory | Identity, `preferences.ini`, server/Kad state, lists, logs, sidecars |
| Temp directory | Incomplete download `.part` and `.part.met` files |
| Incoming directory | Completed downloads |
| Shared directories | User-selected publish roots |

Common profile files include `preferences.ini`, `preferences.dat`,
`server.met`, `nodes.dat`, `known.met`, `known2.met`, `cancelled.met`,
`Category.ini`, `ipfilter.dat`, `addresses.dat`, `shareignore.dat`,
`shareddir.dat`, monitored-share files, and active `.part.met` files.

Before reusing a stock profile, close all eMule-family clients and copy the
whole config directory as a rollback backup. Do not run multiple clients against
the same live profile.

## First Run

For a new profile:

1. Start eMule BB and complete first-run setup.
2. Choose incoming and temporary directories.
3. Configure TCP and UDP ports in `Preferences > Connection`.
4. Leave bind settings empty unless a specific interface or address is required.
5. Enable UPnP only if the router and network policy allow it.
6. Connect to trusted eD2K and/or Kad bootstrap sources.
7. Add shared directories gradually and verify the Shared Files page.
8. Add a small download/search before scaling to a large workload.

For an existing profile:

1. Back up the full config directory while the app is closed.
2. Keep temp and incoming paths stable when possible.
3. Start once without controllers or automation.
4. Verify connection state, downloads, shared files, categories, and logs.
5. Let eMule BB create its branch-specific sidecars and caches.

## Main Guide Chapters

| Need | Guide |
|---|---|
| Install model, first-run profile behavior, and release-aware setup | [Setup Guide](GUIDE-SETUP.md) |
| Complete `preferences.ini` reference and preference behavior | [Preferences Guide](GUIDE-PREFERENCES.md) |
| eD2K, Kad, ports, binding, UPnP, firewall, WebServer network behavior | [Network Guide](GUIDE-NETWORK.md) |
| Downloads, search, categories, broadband upload policy, transfer behavior | [Downloads and Search Guide](GUIDE-DOWNLOADS-SEARCH.md) |
| Shared directories, monitored shares, large libraries, share-ignore rules | [Sharing Guide](GUIDE-SHARING.md) |
| REST, aMuTorrent, Arr, qBit, Torznab, controller behavior | [Controllers and REST Guide](GUIDE-CONTROLLERS-REST.md) |
| IP filter storage, updates, formats, and reload behavior | [IP Filter Guide](GUIDE-IP-FILTERS.md) |
| Deep Windows long-path behavior | [Long Path Guide](GUIDE-LONGPATHS.md) |
| Keyboard and menu workflow | [Keyboard Shortcuts](KEYBOARD-SHORTCUTS.md) |
| Symptom-led diagnostics and support evidence | [Troubleshooting Guide](GUIDE-TROUBLESHOOTING.md) |

## Quality And Test Evidence

eMule BB release claims are tied to the workspace evidence model rather than to
one manual smoke test. The public hosted CI lane gives fast feedback for the
shared Python harness, while the release campaign covers the slower and more
environment-dependent proof that belongs on operator machines.

The current release model is organized around these confidence layers:

- workspace validation and fast non-live test coverage
- native and Python harness coverage for app-facing behavior
- REST contract, OpenAPI drift, malformed-request, and controller checks
- UI, resource, and full stock language smoke coverage
- eD2K/Kad protocol parity, community comparison, and live-diff evidence
- live-wire network, search, transfer, and weak-path scenarios
- x64 and ARM64 build/package provenance, manifests, and SHA-256 hashes

Use [Release Test Strategy](../active/RELEASE-TEST-STRATEGY.md) for the generic
testing model and [Release Test Campaigns](../active/RELEASE-TEST-CAMPAIGNS.md)
for the current campaign view. The beta dashboard remains the release authority
for what has passed, what is still open, and whether public packages may be
tagged.

## Performance Improvements

Performance messaging should be read as operational behavior, not as a synthetic
benchmark promise. eMule BB focuses on places where old desktop assumptions are
visible during long broadband sessions:

- finite broadband upload policy with reviewable slot targets
- weak or stalled slot recycling after warm-up, grace, and cooldown windows
- higher queue, source, socket-buffer, and disk-buffer defaults where landed
- startup and shared-file cache work for large libraries
- duplicate-path and monitored-share handling for deep shared trees
- long-path guidance for modern Windows library layouts
- fixed timeout and buffer assumptions exposed as documented preferences where
  useful
- REST/controller behavior tested as part of the product, not as an external
  scraping layer

These improvements are deliberately compatibility-preserving. They tune local
policy, limits, caching, diagnostics, and controller surfaces while keeping
stock eD2K/Kad wire behavior and the native desktop app model intact.

## Released Behavior Summary

Broadband operation:

- upload defaults are finite and modernized for broadband operation
- upload slot allocation uses a fixed broadband target instead of stock-style
  unbounded slot growth on fast links
- slow or zero-rate upload slots can be recycled after warm-up, grace, and
  cooldown windows
- low-ratio scoring and ratio/cooldown UI data are retained as broadband
  policy extras
- file, queue, source, socket, and disk-buffer defaults are raised from old
  stock assumptions where release work landed

Network and bootstrap:

- eD2K and Kad remain the native network model
- bind policy covers peer TCP, client UDP, server UDP, pinger-adjacent paths,
  and UPnP discovery where applicable
- WebServer/REST has its own bind address and should be configured separately
- server.met, nodes.dat, IP filter, and geolocation update sources use practical
  seeded/default behavior

Sharing and startup:

- `-c` can select an alternate config directory
- share-ignore rules are supported through `shareignore.dat`
- shared startup cache and duplicate-path cache accelerate large libraries
- monitored shares can keep selected roots synchronized
- Shared Files UI is hardened and virtualized for large lists

Downloads and search:

- search result ceilings are configurable for eD2K and Kad
- download filename cleanup can normalize intake and completion names
- categories remain first-class workflow state
- direct delete/cancel operations keep native semantics

Controllers and diagnostics:

- native REST is the preferred automation surface
- qBit/Torznab/Arr-style adapters are compatibility layers, not the source of
  truth
- Tools actions expose save, reload, firewall repair, Windows maintenance,
  diagnostics, dumps, view presets, config-file editors, and folder shortcuts
- redacted diagnostic snapshots are the default support artifact

## Tools And Maintenance

The Tools menu is the operational shortcut surface. It groups:

- session actions: connect, disconnect, pane jumps, tray, exit
- speed actions: upload/download/both limit presets
- folders: incoming, temp, config, logs, WebServer, skins, executable
- config editors: preferences, filters, shares, categories, comments, statistics
- network actions: server.met update, port test, firewall repair, geolocation
- maintenance: reload filters/rules, rescan shared files, save preferences,
  enable Windows long paths, and add Defender exclusions for active download
  folders
- view presets: stock, extended, full, with optional width reset
- diagnostics: logs, redacted/raw snapshots, mini dump, full dump

The top-level Tools groups have native Alt mnemonics so keyboard users can open
Tools with `Alt+T` and continue by letter.

Direct text edits are not always live. Prefer matching reload actions when they
exist, and restart after startup, bind, listener, or layout-state edits.

## Diagnostics And Troubleshooting

Collect evidence before changing many settings. Use:

- normal and verbose logs
- redacted diagnostic snapshot JSON
- firewall repair output
- mini dumps for crashes
- full dumps for hangs or memory growth
- startup/shared-cache evidence for large libraries
- REST/OpenAPI checks for controller failures

Common symptom routing:

| Symptom | First checks |
|---|---|
| Low ID | TCP port, firewall, router/NAT, bind target, port test |
| Kad firewalled | UDP port, Kad bootstrap, firewall, UPnP/router, bind target |
| No search results | selected network, server/Kad state, query shape, search method |
| Slow startup | shared cache state, broad share roots, hash queue, long paths |
| Slow upload | finite upload cap, slot target, slow-slot state, IO/timer diagnostics |
| REST fails | WebServer enabled, bind/port, API key, lifecycle, OpenAPI route |
| IP filter ineffective | enabled flag, rule count, filter level, reload/update logs |

## Compatibility Notes

Core profile files remain stock-compatible where possible, including
`preferences.dat`, `clients.met`, `cryptkey.dat`, `known.met`, `known2.met`,
`cancelled.met`, `.part.met`, `server.met`, and `nodes.dat`.

eMule BB also writes branch-specific state such as `shareignore.dat`,
monitored-share files, shared-library caches, REST/WebServer settings,
geolocation/IP-filter updater state, and preference schema markers. Older stock
clients can ignore many unknown text preferences, but they do not understand all
BB sharing policy, cache files, or controller-side behavior.

## Release Status

Product usage docs do not duplicate release proof. Current release state remains
in:

- [Beta 0.7.3 dashboard](../active/RELEASE-0.7.3.md)
- [Beta 0.7.3 checklist](../active/RELEASE-0.7.3-CHECKLIST.md)
- [Beta 0.7.3 runbook](../active/RELEASE-0.7.3-RUNBOOK.md)
- [Active backlog index](../active/INDEX.md)

When user-visible behavior changes, update the guide chapter that owns it.
