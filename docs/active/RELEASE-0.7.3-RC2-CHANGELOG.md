# eMuleBB 0.7.3-rc.2 Changelog

Status: draft for RC2 preparation; finalize at RC2 go after final artifact names, hashes, proof status, and accepted deviations are recorded.

Format: one line per item, grouped by area; this is a power-user changelog, not a Git log.

RC2 is a delta over the published RC1 artifact set: installer/bootstrapper
correctness, controller refresh, and licensing. The core eMuleBB desktop
behavior, protocol surface, and package shape are unchanged from RC1 except
where noted. Final package hashes and proof status are recorded in
[RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md) and tracked by
[CI-035](items/CI-035.md).

### Installer and Bootstrapper

- RC2/Installer: Fixed the interactive suite installer dropping the bundle
  choice — selecting **Controller** or **Core** no longer reverts to **Full**
  and installs the Arr apps. This is the primary RC2 fix; re-test the bundle
  prompt on a fresh install root.
- RC2/Installer: Hardened suite-config handling so wizard selections (bundle,
  selected apps, ports, bind, media tools) persist reliably end to end.
- RC2/Bootstrapper: The suite bootstrapper now installs the latest **release
  candidate or stable release by default**; nightly builds are opt-in via
  `-IncludeNightly`. `-IncludePrerelease` is deprecated, so the bare one-liner
  installs RC2 once it is published.
- RC2/Bootstrapper: The eD2K server list (`server.met`) seed is fetched over
  **HTTPS** instead of plain HTTP.
- RC2/Suite: Renamed two suite helper scripts to match behavior —
  `Update-Suite` → `Repair-Suite` (re-applies the saved config) and
  `Test-Suite` → `Get-SuiteInfo` (shows config paths and suite status).

### Controllers

- RC2/aMuTorrent: The aMuTorrent controller fork is rebased on upstream
  `got3nks/amutorrent` v3.8.5 (footer KAD/ED2K port tooltips, qBittorrent-compat
  Bearer API-key + SID auth) with the eMuleBB integration on top; categories are
  imported from eMuleBB on connect and ED2K client labels are clarified.
- RC2/Family: A headless `emulebb-rust` eD2K/Kad core that implements the shared
  `/api/v1` controller contract is added as a build target with aMuTorrent
  Rust-session wiring. This is lab/preview work, not a shipped end-user product
  in this RC.

### Licensing

- RC2/License: eMuleBB and the owned repositories are relicensed to
  **GPL-2.0-or-later** (previously Unlicense); release packages carry the
  GPL-2.0 license text.

### Packages

- RC2/Packages: x64 and ARM64 standard + diagnostics ZIPs, the suite
  bootstrapper, and the optional aMuTorrent x64 controller package are
  regenerated from the selected RC2 head. Refreshed manifests, SPDX SBOMs, and
  SHA-256 hashes are recorded in the release checklist. *(Final hashes pending
  the RC2 candidate build.)*
- RC2/Packages: Release ZIPs remain **unsigned** (accepted posture); package
  verification continues through manifests, SBOMs, SHA-256 evidence, and GitHub
  artifact attestations.

### Proof

- RC2/Proof: Pending — fresh quick release-campaign proof, package/hash
  confirmation, and the clean-worktree audit on the selected RC2 head before the
  operator tag instruction. Tracked by [CI-035](items/CI-035.md).

### Risk and Testing Focus

- RC2/Risk: Re-test the **suite installer bundle selection** (Core / Controller
  / Full) on a fresh install root — this is the primary RC2 fix.
- RC2/Risk: Re-validate suite bootstrap (RC-default selection, HTTPS
  `server.met`) and the renamed `Repair-Suite` / `Get-SuiteInfo` scripts.
- RC2/Risk: Confirm the regenerated package set and the aMuTorrent v3.8.5
  controller package install and run cleanly before publication.

## RC1 vs Stock/Community Baseline

Baseline: stock/community eMule `0.72a` from `baseline/community-0.72a`; RC1 release date: **2026-06-07**; GitHub `published_at`: `2026-06-07T06:40:23Z`.

### Compatibility

- RC1/Compatibility: eD2K and Kad remain native stock-compatible protocols, not a new private network or tracker-dependent mode.
- RC1/Compatibility: Existing profile layout remains the compatibility target, but first-run testing should use a backup or disposable profile copy.
- RC1/Compatibility: Running stock eMule and eMuleBB against the same live profile at the same time is unsupported and risks profile corruption.
- RC1/Compatibility: Release proof focuses on desktop client, profile, eD2K, Kad, uploads, downloads, search, servers, shared files, and preferences.
- RC1/Frozen: Legacy WebServer templates, IRC, archive preview/recovery flows, and old optional surfaces are frozen baggage unless they affect supported runtime paths.
- RC1/Future: IPv6 Kad/eD2K parity remains future work and is not a release-ready stock-parity surface in RC1.

### Packages

- RC1/Packages: Release moves from loose developer output to portable ZIP assets with manifests, SPDX SBOMs, bootstrapper hash, and package verification.
- RC1/Packages: Core release assets include x64 and ARM64 ZIPs, plus diagnostics ZIPs when produced by the package gate.
- RC1/Packages: The suite bootstrapper is published as `Bootstrap-eMuleBBSuite.ps1` with a companion SHA-256 file.
- RC1/Packages: Package manifests record ZIP hash, executable hash, expected language DLL set, per-file hashes, SBOM hash, and bootstrapper identity.
- RC1/Packages: Release ZIPs are unsigned, contain no debug symbols, and do not bundle optional `MediaInfo.dll`.
- RC1/Packages: Packaging verifies architecture-matched executables and language DLLs for x64 and ARM64 assets.
- RC1/Packages: Packaging rejects source files, project files, debug artifacts, intermediates, and build logs from release ZIPs.
- RC1/Packages: Stock language DLL coverage is release-gated and must remain complete in each architecture package.
- RC1/Packages: Legacy template-based WebServer payloads are not shipped as RC release assets.

### Startup and Profiles

- RC1/Startup: `-c <base-dir>` adds first-class isolated profile selection for disposable-profile testing and package validation.
- RC1/Startup: Command-line handling covers help flags, instance handling, generated WebServer certificates, diagnostic export actions, and add-link/file forwarding.
- RC1/Startup: Startup diagnostics support belongs to diagnostics packages and must not replace the normal standard release executable.
- RC1/Profiles: Monitored shares, part files, controller intake, and startup cache behavior should be tested on copied profiles before production use.

### Broadband Operation

- RC1/Upload: Upload scheduling moves toward a finite broadband slot target instead of stock-style effectively unbounded slot growth at high limits.
- RC1/Upload: Slow or zero-rate upload slots can be recycled so inactive peers do not pin capacity indefinitely.
- RC1/Upload: Low-ratio behavior is reflected in queue scoring and visibility while preserving eMule-style sharing incentives.
- RC1/Limits: Queue limits, source limits, buffers, timeouts, and search ceilings are raised or modernized for current machines and broadband links.
- RC1/Load: Large peer counts, large shared libraries, and longer sessions are better supported before legacy limits become the primary bottleneck.

### Downloads and Disk Safety

- RC1/Downloads: Normal part-file resume remains the compatibility model while placement and disk-pressure guards are stricter.
- RC1/Disk: Protected-volume floors reduce the chance that downloads or controller intake continue into unsafe disk states.
- RC1/Disk: Part metadata guardrails reduce risk around bad placement, damaged metadata, and unsafe controller add-transfer flows.
- RC1/Filenames: Remote filenames are cleaned for invalid characters before UI display or disk use.
- RC1/Filenames: Bounded HTML/XML entities and common Western mojibake are repaired during remote filename intake.
- RC1/Categories: Category workflows and qBittorrent-style shortcut/batch actions are polished for high-volume download management.
- RC1/Completion: Completed-download automation can launch an optional external command and should be treated as a local power-user hook.

### Shared Files

- RC1/LongPaths: Long-path handling is hardened across profile, temp, incoming, shared-library, package, and tooling paths.
- RC1/Sharing: Startup cache work reduces repeated large-library scan cost for users with many shared files.
- RC1/Sharing: Duplicate tracking improves behavior for large or overlapping shared libraries.
- RC1/Sharing: Monitored shares are release-facing and should be validated before pointing at production media trees.
- RC1/Sharing: Shared Files UI virtualization improves usability with large shared libraries.
- RC1/Sharing: `shareignore.dat` is supported for excluding generated, private, transient, or controller-owned files from sharing.
- RC1/Preview: Shared-video peer preview remains optional and depends on file visibility plus local media tooling.

### Network and Bootstrap

- RC1/Binding: P2P bind coverage includes peer TCP, client UDP, server UDP, pinger, and UPnP paths.
- RC1/Binding: Multi-interface and VPN-bound hosts get more predictable socket binding and diagnostics than stock behavior.
- RC1/WebServer: WebServer/REST binding is separate from P2P binding and must be configured as its own local control surface.
- RC1/UPnP: P2P UPnP and WebServer UPnP are separate, so a peer-port mapping does not imply a controller-port mapping.
- RC1/Bootstrap: Server list, Kad node, IP-filter, and geolocation seed/update paths are adjusted for practical release setup.
- RC1/GeoIP: DB-IP city geolocation update/display replaces older assumptions about location data freshness.
- RC1/IPFilter: Automatic IP-filter update scheduling and reload behavior are release-facing surfaces.

### REST and Controllers

- RC1/REST: Authenticated in-process JSON REST API under `/api/v1` becomes the preferred automation surface.
- RC1/REST: REST coverage includes transfer detail, add-transfer flows, search, server/Kad bootstrap, upload queue visibility, and expanded preferences.
- RC1/Adapters: qBittorrent-style, Torznab, and Arr workflows are adapter layers over eD2K/Kad semantics, not one-to-one qBittorrent behavior.
- RC1/aMuTorrent: aMuTorrent is packaged as an optional controller ZIP separate from the core eMuleBB release ZIPs.
- RC1/aMuTorrent: aMuTorrent RC package proof is x64-only; native ARM64 packaging needs a deliberate ARM64 Node/native-module path.
- RC1/WebServer: Controller hardening covers typed errors, authentication, TLS/certificate generation, static-file boundaries, and socket lifecycle checks.
- RC1/Security: REST/WebServer should be treated as a trusted-local control surface unless a later release documents internet exposure.

### Preferences and UI

- RC1/Preferences: Preference inventory maps storage keys, REST bindings, and Preferences UI sources to reduce silent mismatches.
- RC1/Preferences: Strong section-qualified schema validation protects preference key uniqueness and mutable REST metadata.
- RC1/UI: Power-user desktop polish adds or refines advanced context menus, keyboard shortcuts, tray options, categories, Web Interface preferences, and MiniMule behavior.
- RC1/UI: Display and date/time handling gets locale-aware formatting and clearer timestamp customization paths.
- RC1/UI: qBittorrent-style download shortcuts and batch menu actions are added where they preserve native eMule semantics.

### Diagnostics and Support

- RC1/Diagnostics: Release support relies on redacted diagnostics, startup traces, performance logs, manifests, SBOMs, and structured campaign reports.
- RC1/Diagnostics: Diagnostics builds can include startup, packet, upload-slot, download-slot, and bad-peer instrumentation.
- RC1/Diagnostics: Standard release packages must not ship diagnostics-only binaries in place of the normal executable.
- RC1/Support: Useful bug reports should include package identity, profile isolation method, bind/interface settings, controller config, logs, and exact repro steps.
- RC1/Performance: Performance logging and timestamped reports improve comparison of startup, transfer, shared-file, and controller behavior.

### Security and Trust

- RC1/Security: Verify downloaded portable assets with hashes, manifests, SBOMs, and GitHub release evidence before using them on important hosts.
- RC1/Security: Generated WebServer certificates support local HTTPS testing but do not make public exposure safe by themselves.
- RC1/Security: GitHub release checks and package evidence replace the older broad legacy updater trust model for this release train.
- RC1/Security: Public internet exposure of REST/WebServer remains outside the release security posture.
