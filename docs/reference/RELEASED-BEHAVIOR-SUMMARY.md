# Released Behavior Summary

This reference records product behavior documented as landed on the current
eMuleBB line. It is a companion to the [Product Guide](GUIDE-EMULEBB.md) and
the focused operator guides; it is not a replacement for the active release
dashboard.

Open, deferred, exploratory, and historical items are not product promises.
Current release state remains in the
[0.7.3 RC1 dashboard](../active/RELEASE-0.7.3.md).

## Landed Feature Matrix

- **Long paths:** Long-path hardening for profile, temp, incoming,
  shared-library, package, and tooling paths.
  Evidence: FEAT-010. Guide: [Long Paths](GUIDE-LONGPATHS.md).
- **Listen socket:** TCP error-flood defense before the broader future shield
  engine. Evidence: FEAT-012. Guide: [Network](GUIDE-NETWORK.md).
- **REST core:** Authenticated in-process JSON REST API under `/api/v1`.
  Evidence: FEAT-013. Guide: [Controllers And REST](GUIDE-CONTROLLERS-REST.md).
- **Broadband upload:** Finite upload slot target, weak-slot recycling,
  low-ratio policy, and queue visibility. Evidence: FEAT-015, FEAT-023. Guide:
  [Downloads And Search](GUIDE-DOWNLOADS-SEARCH.md).
- **Modern limits:** Updated practical defaults for queues, sources, buffers,
  timeouts, and search ceilings. Evidence: FEAT-016, FEAT-029. Guide:
  [Downloads And Search](GUIDE-DOWNLOADS-SEARCH.md).
- **Geolocation:** DB-IP city geolocation update and display support.
  Evidence: FEAT-020. Guide: [Network](GUIDE-NETWORK.md).
- **Profile selection:** `-c <base-dir>` startup diagnostics override for isolated
  profiles. Evidence: FEAT-022. Guide: [Setup](GUIDE-SETUP.md).
- **Sharing policy:** `shareignore.dat`, monitored shares, startup cache,
  duplicate cache, and Shared Files virtualization. Evidence: FEAT-024,
  FEAT-026, FEAT-027, FEAT-028, FEAT-038. Guide:
  [Sharing](GUIDE-SHARING.md).
- **Filename hygiene:** Download filename cleanup, remote-intake
  mojibake/entity repair, and message display cleanup. Evidence: FEAT-025,
  FEAT-054, FEAT-071. Guide:
  [Downloads And Search](GUIDE-DOWNLOADS-SEARCH.md).
- **Network binding:** Completed P2P bind coverage and separate WebServer bind
  behavior. Evidence: FEAT-030. Guide: [Network](GUIDE-NETWORK.md).
- **Disk safety:** Disk-space floor hardening and legacy import-flow
  retirement. Evidence: FEAT-033. Guide:
  [Downloads And Search](GUIDE-DOWNLOADS-SEARCH.md).
- **IP filters:** Automatic IP-filter update scheduling and reload behavior.
  Evidence: FEAT-042. Guide: [IP Filters](GUIDE-IP-FILTERS.md).
- **REST completeness:** Transfer detail, server/Kad bootstrap, search, upload
  queue, and preference expansion. Evidence: FEAT-045, FEAT-046, FEAT-047,
  FEAT-048, FEAT-049. Guide:
  [Controllers And REST](GUIDE-CONTROLLERS-REST.md).
- **Completion automation:** Optional external program launch on completed
  download. Evidence: FEAT-050. Guide:
  [Downloads And Search](GUIDE-DOWNLOADS-SEARCH.md).
- **Power-user UX:** Advanced context menus, keyboard shortcuts, tray options,
  category polish, Web Interface preference layout, and MiniMule polish.
  Evidence: FEAT-051, FEAT-052, FEAT-053, FEAT-059, FEAT-062, FEAT-063,
  FEAT-065, FEAT-066. Guides: [Keyboard Shortcuts](KEYBOARD-SHORTCUTS.md),
  [Preferences](GUIDE-PREFERENCES.md).
- **Preference quality:** Preference inventory, mapping, clamps, persistence
  audit, and strong schema validation. Evidence: FEAT-060, FEAT-061. Guide:
  [Preferences](GUIDE-PREFERENCES.md).
- **qBit-style workflows:** Download shortcuts and batch menu actions that
  preserve eMule semantics. Evidence: FEAT-057. Guide:
  [Downloads And Search](GUIDE-DOWNLOADS-SEARCH.md).
- **Closeout UX:** Release-facing UX polish and audit closeout. Evidence:
  FEAT-058. Guide: [Troubleshooting](GUIDE-TROUBLESHOOTING.md).

## Behavior Summary

Broadband operation:

- upload defaults are finite and modernized for broadband operation
- upload slot allocation uses a fixed broadband target instead of stock-style
  unbounded slot growth on fast links
- slow or zero-rate upload slots can be recycled after warm-up, grace, and
  cooldown windows
- low-ratio scoring and ratio/cooldown UI data are retained as broadband policy
  extras
- file, queue, source, socket, and disk-buffer defaults are raised from old
  stock assumptions where release work landed

Network and bootstrap:

- eD2K and Kad remain the native network model
- bind policy covers peer TCP, client UDP, server UDP, pinger-adjacent paths,
  and UPnP discovery where applicable
- VPN-aware operation is provider-neutral interface/address binding with
  resolved-state diagnostics, startup bind blocking, and optional exit on
  configured-interface loss; VPN kill-switch, firewall, and route enforcement
  remain external operator or provider policy
- WebServer/REST has its own bind address and should be configured separately
- P2P UPnP stores enablement, close-on-exit behavior, and backend mode;
  WebServer UPnP is configured separately from P2P listener mapping
- server.met, nodes.dat, IP filter, and geolocation update sources use practical
  seeded/default behavior
- IPv6 is future connectivity work; current-network dual-stack compatibility and
  the exploratory IPv6 Kad network design are tracked separately

Startup and command line:

- `-c` can select an alternate config directory
- `--help`, `-h`, and `/?` print command-line usage
- `-ignoreinstances`, `-AutoStart`, and Debug-build `-assertfile` keep their
  targeted startup semantics
- `--generate-webserver-cert` creates WebServer TLS certificate/key material and
  exits when `--cert` and `--key` are provided
- `--diagnose-media-metadata` probes maintained metadata extractors and exits
  with `emulebb.mediaMetadataDiagnostic.v1` JSON
- one positional input can be forwarded as an `ed2k` link, magnet link,
  collection file, or command such as `exit`
- the current update check is a GitHub Releases startup check, distinct from
  the removed legacy stock eMule update checker

Sharing and library management:

- share-ignore rules are supported through `shareignore.dat`
- peer preview is an explicit opt-in live-network sharing behavior for shared
  video files when shares are visible and FFmpeg is configured
- shared startup cache and duplicate-path cache accelerate large libraries
- monitored shares can keep selected roots synchronized
- Shared Files UI is hardened and virtualized for large lists
- Shared Files `Last Request` uses the same list date/time formatting preference
  as other native list timestamp columns

Downloads and disk safety:

- search result ceilings are configurable for eD2K and Kad
- remote search and download-intake filenames repair conservative Western
  mojibake and bounded HTML/XML entities before normal filename cleanup
- download filename cleanup can normalize intake and completion names
- categories remain first-class workflow state
- qBittorrent-style shortcuts and batch menu actions preserve native delete,
  category, and paused/started semantics
- completed downloads can optionally run a configured external command
- Auto Broadband I/O bounds download buffer memory by sharing a 512 MiB global
  active-download buffer budget across active buffered files
- protected-volume disk-space floors cover config, temp, incoming, and
  category-specific incoming volumes
- `.part.met` writes have their own free-space guard
- controller add-transfer requests use the same placement guard as native
  download intake

Controllers and diagnostics:

- native REST is the preferred automation surface
- qBit/Torznab/Arr-style adapters are compatibility layers, not the source of
  truth
- WebServer TLS certificate generation is available from the command line
- Tools actions expose save, reload, firewall repair, Windows maintenance,
  diagnostics, dumps, view presets, config-file editors, and folder shortcuts
- redacted diagnostic snapshots are the default support artifact
- performance logging can write CSV or MRTG-style samples for bounded operator
  diagnostics
- normal native UI date/time text follows the Windows user locale by default
- users can customize general, log, and list timestamps with MFC
  `CTime::Format` strings in `preferences.ini`

## Documentation Coverage Rule

For release readiness, a landed feature is fully documented only when the owning
docs cover the relevant surface:

| Feature surface | Required documentation |
|---|---|
| User workflow | Focused guide that owns the workflow |
| Configuration | [Preferences Guide](GUIDE-PREFERENCES.md), including storage key, owner/API, UI binding, REST binding, and normalization notes |
| Network behavior | [Network Guide](GUIDE-NETWORK.md), including bind, firewall, UPnP, WebServer/REST, and diagnosis boundaries |
| Controller behavior | [Controllers And REST Guide](GUIDE-CONTROLLERS-REST.md), REST contract, and OpenAPI |
| Command line | [Development Guide](DEVELOPMENT-GUIDE.md), plus setup/product summary when the option affects operators |
| Testing and release proof | [Development Guide](DEVELOPMENT-GUIDE.md), [Release Test Strategy](../active/RELEASE-TEST-STRATEGY.md), and active release docs |

## Evidence Model

eMuleBB release claims are tied to the workspace evidence model rather than to
one manual smoke test. Current confidence layers include:

- workspace validation and fast non-live test coverage
- native and Python harness coverage for app-facing behavior
- REST contract, OpenAPI drift, malformed-request, and controller checks
- UI, resource, and full stock language smoke coverage
- eD2K/Kad protocol parity, community comparison, and live-diff evidence
- live-wire network, search, transfer, and weak-path scenarios
- x64 and ARM64 build/package provenance, manifests, SHA-256 hashes, SPDX SBOMs,
  and GitHub artifact attestations where published

Use [Release Test Strategy](../active/RELEASE-TEST-STRATEGY.md) for the generic
testing model and [Release Test Campaigns](../active/RELEASE-TEST-CAMPAIGNS.md)
for the current campaign view. The RC dashboard remains the release authority
for what has passed, what is still open, and whether public packages may be
tagged.
