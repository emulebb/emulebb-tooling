# eMuleBB Product Guide

<section class="docs-hero">
  <div>
    <p class="docs-eyebrow">Product manual</p>
    <h2>Run eMule like a serious broadband client.</h2>
    <p>
      eMuleBB keeps the native Windows desktop workflow and stock-compatible
      eD2K/Kad behavior while adding modern defaults, stronger profile
      handling, large-library support, diagnostics, and a trusted local
      REST/controller surface.
    </p>
  </div>
  <img alt="eMuleBB broadband edition logo" src="../../assets/brand/emulebb-broadband-edition-logo.png" />
</section>

This is the product manual entry point. It links to focused guide chapters and
summarizes the behavior that matters when operating the app.

## Who This Is For

eMuleBB is for users and operators who want a long-running native eMule client
with explicit control:

- power users with sustained broadband upload capacity
- archivists and seeders with large shared libraries
- users who need explicit firewall, bind, UPnP, and IP-filter behavior
- operators using trusted local controllers through REST
- contributors who need reproducible diagnostics and documented runtime rules

It is not a rewrite and not a headless daemon. The desktop app owns the live
state; REST and companion tools adapt to that state.

## Why It Exists

Classic eMule still has the right shape for eD2K/Kad: a native client with
visible queues, explicit sharing, server/Kad state, and user-owned profiles.
Modern usage needs tighter defaults around broadband links, path handling,
large libraries, diagnostics, packaging, and automation.

eMuleBB focuses on those gaps:

| Power-user need | eMuleBB answer |
|---|---|
| Keep an existing profile under control | Explicit profile model, `-c` profiles, documented state files |
| Run large shares without guessing | Large-library guidance, share-ignore rules, monitored-share behavior |
| Diagnose real problems | Logs, dumps, performance evidence, symptom-led troubleshooting |
| Use modern controllers | Native REST, aMuTorrent, qBit-compatible, and Torznab adapter docs |
| Preserve eMule behavior | Stock-compatible eD2K/Kad defaults and native desktop authority |

## Compatibility Baseline And Future Evolution

0.7.3 is the compatibility baseline for eMuleBB. It preserves the familiar
native desktop workflow, stock-compatible eD2K/Kad behavior, and practical
profile continuity while introducing the maintained broadband, diagnostics,
packaging, and controller work described in these guides.

That does not mean every old eMule-era surface is a supported feature. Some
legacy code, resources, settings, or menu paths may still be present in 0.7.3
because preserving them is lower risk than deleting them during the release
candidate. Those areas are frozen: they are not release proof targets and should
not be used as the basis for new workflows.

Future releases start from the 0.7.3 baseline and evolve deliberately. The
approved direction is focused modernization: connectivity, UI polish, startup
and large-library performance, controller reliability, security/operations, and
careful local-state planning. Profile safety and current network compatibility
remain hard constraints.

## First Hour Workflow

1. Unpack or install eMuleBB into its own application directory.
2. Launch with a deliberate profile directory, especially for test packages:

   ```powershell
   emulebb.exe -c "$env:TEMP\eMuleBB-Profile"
   ```

3. Set incoming and temp directories before starting serious downloads.
4. Configure TCP/UDP ports, firewall, and UPnP or manual forwarding.
5. Connect eD2K and/or Kad and confirm the state is understandable.
6. Add one small shared directory and verify it on the Shared Files page.
7. Run one small search or add one known safe link.
8. Only then enable REST, aMuTorrent, Prowlarr, Radarr, or Sonarr.

The fastest way to lose clarity is to start a copied profile, a controller, an
Arr app, and a large share scan all at the same time. Prove one layer, then add
the next.

## Daily Operating Model

eMuleBB should feel familiar if you know classic eMule, but the operating model
is stricter:

- profiles are explicit and backed up before risky testing
- incoming, temp, and shared directories are separate concepts
- categories carry real path and controller meaning
- REST is trusted local automation, not a public internet service
- controllers preserve native eMule semantics instead of replacing them
- diagnostics should be collected before changing too many variables

Release documentation follows the same rule as the product: every shipped
feature needs an operator-facing description, a preference/API reference when
it has configuration surface, and development-guide evidence for how it is
validated. Open, deferred, exploratory, and historical items stay out of the
released behavior summary.

## Install And Profile Model

The fastest full-suite install is the RC1 PowerShell one-liner in the
[Setup Guide](GUIDE-SETUP.md#full-suite-install-powershell-bootstrap). It
bootstraps eMuleBB plus the local controller/Arr integration flow from GitHub
Releases. If you only want the standalone desktop app, download the eMuleBB ZIP,
extract it into a new application folder, and run `emulebb.exe`.

Keep these locations conceptually separate:

| Location | Purpose |
|---|---|
| Application directory | Executable, bundled runtime assets, skins, toolbar assets |
| Config/profile directory | Identity, `preferences.ini`, server/Kad state, lists, logs, sidecars |
| Temp directory | Incomplete download `.part` and `.part.met` files |
| Incoming directory | Completed downloads |
| Shared directories | User-selected publish roots |

Common profile files include `preferences.ini`, `preferences.dat`,
`server.met`, `nodes.dat`, `known.met`, `known2_64.met`, `cancelled.met`,
`Category.ini`, `ipfilter.dat`, `addresses.dat`, `shareignore.dat`,
`shareddir.dat`, monitored-share files, and active `.part.met` files. See the
[Persistence Files](GUIDE-PERSISTENCE-FILES.md) reference for `.met` and `.dat`
roles, structures, and recovery priority.

With `emulebb.exe -c <profile-dir>`, the effective preferences file is
`<profile-dir>\config\preferences.ini`. Existing `IncomingDir` and `TempDir`
values in that file take precedence over the clean-profile default directories
under `<profile-dir>`.

Before reusing a stock profile, close all eMule-family clients and copy the
whole config directory as a rollback backup. Do not run multiple clients against
the same live profile.

## First Run

For a new profile:

1. Start eMuleBB with a clean profile.
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
5. Let eMuleBB create its branch-specific sidecars and caches.

## Main Guide Chapters

| Need | Guide |
|---|---|
| Learn eMule from zero through full operation: eD2K, Kad, High ID, queues, credits, sources, sharing, automation, safety, and tuning | [Power User Manual](GUIDE-POWER-USERS.md) |
| Install model, profile migration, isolated `-c` profiles, and release-aware setup | [Setup Guide](GUIDE-SETUP.md) |
| Complete `preferences.ini` reference and preference behavior | [Preferences Guide](GUIDE-PREFERENCES.md) |
| eD2K, Kad, ports, binding, UPnP, firewall, WebServer network behavior | [Network Guide](GUIDE-NETWORK.md) |
| Downloads, search, categories, broadband upload policy, transfer behavior | [Downloads and Search Guide](GUIDE-DOWNLOADS-SEARCH.md) |
| Shared directories, monitored shares, large libraries, share-ignore rules | [Sharing Guide](GUIDE-SHARING.md) |
| eMuleBB plus aMuTorrent plus Prowlarr/Radarr/Sonarr workflows | [Stack Integration Guide](GUIDE-STACK-INTEGRATIONS.md) |
| REST behavior, adapter boundaries, lifecycle, and controller safety | [Controllers and REST Guide](GUIDE-CONTROLLERS-REST.md) |
| Landed behavior matrix, release documentation coverage, and evidence model | [Released Behavior Summary](RELEASED-BEHAVIOR-SUMMARY.md) |
| IP filter setup, updates, manual reloads, formats, levels, and troubleshooting | [IP Filter Guide](GUIDE-IP-FILTERS.md) |
| Deep Windows long-path behavior | [Long Path Guide](GUIDE-LONGPATHS.md) |
| Keyboard and menu workflow | [Keyboard Shortcuts](KEYBOARD-SHORTCUTS.md) |
| Symptom-led diagnostics, support evidence, Low ID, Kad, REST, and disk-space triage | [Troubleshooting Guide](GUIDE-TROUBLESHOOTING.md) |
| Translation terminology, localized homepage rules, and glossary | [Translations And Localization](GUIDE-TRANSLATIONS.md) |
| Development, validation, CI, packaging, and guide refresh workflow | [Development Guide](DEVELOPMENT-GUIDE.md) |

## Public Documentation And Evidence

The product guide is maintained as Markdown in `emulebb-tooling` and published as
browser-readable HTML through the MkDocs documentation site at
`https://emulebb.github.io/emulebb-tooling/`. The public homepage links to that
rendered documentation and summarizes it; the Markdown guide remains the source
of truth for product behavior, release evidence, and operator workflows.

The repeatable publishing workflow is:

1. Update the owning Markdown guide under `repos\emulebb-tooling\docs`.
2. Run the local documentation publish gate:

   ```powershell
   cd $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling
   python scripts\docs-publish-check.py
   ```

3. Commit and push the source Markdown. GitHub Actions builds the MkDocs HTML
   site from `main` and deploys it to GitHub Pages.
4. When the public homepage needs a shorter product summary, update
   `repos\emulebb-pages` from the rendered-doc facts and regenerate its static
   HTML pages.

Release-facing product claims are backed by evidence, not by homepage copy.
Current quality signals include extensive automated testing, native and Python
harness coverage, REST/OpenAPI checks, live E2E lanes, package manifests,
SHA-256 hashes, SPDX SBOM files for release packages, and GitHub artifact
attestations for eMuleBB nightly assets. The homepage may advertise those
strengths only after the source guide and release docs describe the same
evidence.

## Public Testing And Downloads

Public testing currently runs through GitHub Releases and nightly prerelease
packages. Treat nightly packages as test builds: keep the previous working
package, use a disposable or backed-up profile, and report repeatable failures
with evidence.

eMuleBB nightly release assets are published with GitHub artifact attestations
so testers can verify that a downloaded ZIP, manifest, or SBOM asset matches a
signed GitHub Actions provenance claim:

```powershell
gh attestation verify PATH_TO_ASSET -R emulebb/emulebb
```

- eMuleBB desktop app:
  `https://github.com/emulebb/emulebb/releases`. Nightly testing is open.
  The current official public test line is 0.7.3 RC1; use
  `emulebb-v0.7.3-rc.1` or a later approved release tag for release-candidate
  testing. Nightly and older beta packages remain pre-release test builds.
- aMule Windows builds:
  `https://github.com/emulebb/amule/releases`. eMuleBB publishes Windows build
  and validation artifacts for aMule users. This is an ecosystem build track,
  not upstream aMule ownership.
- aMuTorrent manager fork:
  `https://github.com/emulebb/amutorrent/releases`. Release automation exists
  for the eMuleBB-oriented fork. If the release page has no published asset,
  there is no public package yet.
- MiniUPnP/miniupnpc for Windows:
  `https://github.com/emulebb/emulebb-miniupnp/releases`. Windows `upnpc`
  packages are published as adjacent tooling for the eMuleBB ecosystem.

### Repeatable Nightly Test Recipe

Use this flow when testing a public nightly:

1. Download the ZIP for the intended architecture, normally x64 unless testing
   ARM64 specifically.
2. Unzip it into a new application directory. Do not overwrite the previous
   known-good package.
3. Choose a config/profile directory. Prefer a disposable profile for first
   tests; if using a real profile, close every eMule-family client and back up
   the full config directory first.
4. Launch with an explicit profile path:

   ```powershell
   emulebb.exe -c "$env:TEMP\eMuleBB-TestProfile"
   ```

5. Start once without REST controllers, aMuTorrent, Arr tools, or other
   automation.
6. Verify the app opens, connection state is visible, server and Kad setup are
   intentional, shared directories load, logs are written, and shutdown
   completes normally.
7. Add one small search or transfer and one small shared directory before
   scaling to a large profile or live-wire workload.
8. Keep the exact package name, architecture, profile type, and repro steps in
   your notes.

Never run two clients against the same live profile at the same time. If a test
build damages a disposable profile, delete the disposable profile and retest
from the same clean starting state before reporting data-loss behavior.

### Repeatable Controller Test Recipe

Only test controllers after the normal desktop app is healthy:

1. Enable WebServer/REST only for the test window.
2. Bind to localhost or a controlled interface.
3. Use a strong API key or password path.
4. Confirm a read-only status request works before running mutations.
5. Compare controller behavior with the desktop UI when transfer, search, file,
   or preference state looks wrong.
6. Capture method, route, status code, request body, response body, controller
   logs, and app logs for any failure.

REST and companion tools are supported controller surfaces. The legacy HTML
WebServer UI is frozen and should not be used as proof that REST behavior is
broken or supported.

### Evidence To Include In Reports

Good public-test reports should include:

- package name or release tag, architecture, and whether the package was a
  nightly, RC, or stable build
- Windows version and whether the run used x64 or ARM64
- profile type: disposable, copied real profile, or live-wire real profile
- exact launch command, including `-c` when used
- exact repro steps and whether the failure survives a clean retry
- relevant logs such as `emulebb.log`, `emulebb-verbose.log`, controller logs,
  package logs, or startup/shutdown progress symptoms
- diagnostic snapshot or redacted settings when preferences, paths, REST, or
  networking are involved
- mini dump for a crash, full dump for a hang or memory-growth case
- REST method, route, status code, request body, and response body for API
  failures

## Recommended Reading Paths

For a first-time user:

1. Read [Setup Guide](GUIDE-SETUP.md).
2. Configure ports and connection behavior with
   [Network Guide](GUIDE-NETWORK.md).
3. Add one small shared directory with [Sharing Guide](GUIDE-SHARING.md).
4. Learn searches and transfers with
   [Downloads and Search Guide](GUIDE-DOWNLOADS-SEARCH.md).
5. Use [Troubleshooting Guide](GUIDE-TROUBLESHOOTING.md) if Low ID, Kad,
   search, disk-space, or startup symptoms appear.

For a long-running seeder:

1. Review directory layout and profile backup in
   [Setup Guide](GUIDE-SETUP.md).
2. Review shared-cache, monitored-share, and share-ignore behavior in
   [Sharing Guide](GUIDE-SHARING.md).
3. Review disk-space floors in
   [Downloads and Search Guide](GUIDE-DOWNLOADS-SEARCH.md).
4. Review long-path behavior in [Long Path Guide](GUIDE-LONGPATHS.md).
5. Keep support evidence paths from
   [Troubleshooting Guide](GUIDE-TROUBLESHOOTING.md) available.

For controller or automation use:

1. Finish normal desktop setup first.
2. Configure the listener with
   [Controllers and REST Guide](GUIDE-CONTROLLERS-REST.md).
3. Use [REST API contract](../rest/REST-API-CONTRACT.md) and
   [OpenAPI](../rest/REST-API-OPENAPI.yaml) for exact routes.
4. Use [Preferences Guide](GUIDE-PREFERENCES.md) for preference fields.
5. Keep legacy HTML WebServer behavior out of supported automation plans.

## Released Behavior And Evidence

The product guide stays at the operating-model level. Detailed release behavior,
feature-to-guide mapping, documentation coverage rules, and release evidence
belong in [Released Behavior Summary](RELEASED-BEHAVIOR-SUMMARY.md).

Use that companion reference when you need to answer:

- which feature IDs back a documented behavior
- which focused guide owns the behavior details
- what evidence layers support release claims
- which docs must change when a landed behavior changes

The product guide should describe what an operator can rely on. It should not
turn test-only seams, future backlog, abandoned ideas, or private evidence
labels into product promises.

## Storage Allocation Defaults

Sparse part files and full preallocation are both off by default. This keeps the
default storage profile neutral across SSDs, mechanical disks, removable
volumes, and space-constrained temp directories.

Operators can tune these settings deliberately:

- enable sparse part files on NTFS when conserving temp space matters more than
  contiguous layout
- keep sparse part files off on mechanical or SMR HDDs when upload/read
  smoothness matters, because out-of-order download writes can fragment sparse
  files
- enable full allocation only for non-sparse part files on mechanical HDDs with
  enough free space, where reserving the target size can reduce fragmentation
  and improve later sequential reads/uploads
- leave both settings off when unsure

## Performance Improvements

Performance messaging should be read as operational behavior, not as a synthetic
benchmark promise. eMuleBB focuses on places where old desktop assumptions are
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

## Tools And Maintenance

The Tools menu is the operational shortcut surface. It groups:

- session actions: connect, disconnect, pane jumps, tray, exit
- transfers, speed, and refresh: transfer navigation, upload/download/both
  limit presets, refresh interval controls
- files and categories: incoming, temp, config, logs, WebServer, skins,
  executable, category manager, category config
- network actions: server.met update, port test, firewall repair, geolocation
- controllers and integrations: Prowlarr indexer setup plus separate Radarr
  and Sonarr download-client helpers
- maintenance: reload filters/rules, rescan shared files, save preferences,
  enable Windows long paths, and add Defender exclusions for active download
  folders
- diagnostics: logs, redacted/raw snapshots, mini dump, full dump
- display and views: toolbar skins, text labels, display reset, toolbar
  customization, stock/extended/full view presets
- config editors: preferences, filters, shares, comments, statistics
- links: eMuleBB web links and configured web-service entries

Main-shell shortcuts are language-independent and reuse the reviewed English
toolbar mnemonics. Transfers owns `Alt+T`; Tools opens with `Alt+W` so keyboard
users can open Tools and continue by letter without colliding with Transfers.
See [Tools Menu Guide](GUIDE-TOOLS-MENU.md) for the current menu map.
The expanded Tools popup and compact tray Tools path intentionally allow only
one submenu level, so grouped commands remain reachable without nested flyout
chains.

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

Runtime diagnostic file names are intentionally uniform and script-friendly.
The normal log is `emulebb.log`, the verbose log is `emulebb-verbose.log`, the
debug CRT log is `emulebb-crt-debug.log`, recoverable early startup directory
errors use `emulebb-startup-errors.log`, diagnostics logs use
`emulebb-diagnostics-packet.log`, `emulebb-diagnostics-upload-slot.log`,
`emulebb-diagnostics-download-slot.log`, and
`emulebb-diagnostics-bad-peer.log`, and performance logs default to
`emulebb-performance.csv` or `emulebb-performance.mrtg` with
`emulebb-performance-data.mrtg` and `emulebb-performance-overhead.mrtg`
sidecars.
Rotated logs append `-YYYYMMDD-HHMMSS` before the extension. Diagnostic dumps
use `emulebb-dump-YYYYMMDD-HHMMSS-pid<PID>-mini|full.dmp` for operator-requested
dumps and `emulebb-crash-YYYYMMDD-HHMMSS-pid<PID>.dmp` for crash dumps.

The rename is strict in current eMuleBB builds: tools and support procedures
should use the new names and should not rely on legacy `eMule.log`,
`eMule_Verbose.log`, `eMule-startup-errors.log`, or `perflog.*` filenames.

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
`preferences.dat`, `clients.met`, `cryptkey.dat`, `known.met`, `known2_64.met`,
`cancelled.met`, `.part.met`, `server.met`, and `nodes.dat`.

eMuleBB also writes branch-specific state such as `shareignore.dat`,
monitored-share files, shared-library caches, REST/WebServer settings,
geolocation/IP-filter updater state, and preference schema markers. Older stock
clients can ignore many unknown text preferences, but they do not understand all
eMuleBB sharing policy, cache files, or controller-side behavior.

Live Source Exchange is SX2-only. eMuleBB intentionally removed deprecated
live-network SX1 advertise, request, response, and version-tracking paths. Do
not treat missing live `OP_REQUESTSOURCES` or `OP_ANSWERSOURCES` SX1 support as
an accidental protocol regression.

IPv6 roadmap language has two separate meanings. Current-network dual-stack
compatibility is tracked by [FEAT-035](../active/items/FEAT-035.md). A separate
IPv6 Kad network is only an exploratory design note in
[IDEA-IPV6-KAD-NETWORK](../ideas/IDEA-IPV6-KAD-NETWORK.md), inspired by the
qBittorrent/libtorrent approach of keeping IPv4 and IPv6 DHT state separate.
Neither track changes planned 0.7.3 RC1 release behavior unless the active release
docs later say otherwise.

## Unsupported Legacy Areas

Some old eMule surfaces may still appear in resources, settings, or historical
notes. In 0.7.3, their presence means compatibility-preserved and frozen, not
supported. They are not maintained user workflows for eMuleBB:

- archive preview and archive recovery
- IRC and IRC-adjacent chat UI
- legacy Scheduler and scheduler preferences
- SMTP/email notifications
- SAPI text-to-speech notifications
- first-run connection wizard
- splash screen
- legacy WebServer HTML templates and page UI
- proxy support

Use the supported replacements where they exist: Preferences pages for setup,
REST and controller adapters for automation, Windows or operator scheduling for
recurring tasks, and normal diagnostic snapshots for support. See
[Frozen Surfaces](../active/FROZEN-SURFACES.md) for the current support rule.

## Release Status

Product usage docs do not duplicate release proof. Current release state remains
in:

- [0.7.3 RC1 dashboard](../active/RELEASE-0.7.3.md)
- [0.7.3 RC1 checklist](../active/RELEASE-0.7.3-CHECKLIST.md)
- [0.7.3 RC1 runbook](../active/RELEASE-0.7.3-RUNBOOK.md)
- [Active backlog index](../active/INDEX.md)

When user-visible behavior changes, update the guide chapter that owns it.
