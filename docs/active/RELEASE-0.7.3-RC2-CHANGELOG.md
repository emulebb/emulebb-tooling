# eMuleBB 0.7.3-rc.2 Changelog

Status: draft for RC2 preparation. This file is started before the RC2 release
go so the power-user changes are reviewed while proof is still active. It is
not final publication text until the operator gives the RC2 go and final
artifact names and hashes are recorded.

This changelog is intentionally not a Git log. It describes user-visible,
operator-visible, package-visible, controller-visible, and compatibility
changes that matter when running or evaluating the release.

## RC2 Changes Since RC1

RC2 delta entries are still pending final proof. Complete this section at RC2
go with only the changes that differ from the published RC1 artifact set, for
example:

- package, bootstrapper, manifest, SBOM, and hash changes;
- blocker fixes or accepted release-gate deviations since RC1;
- changed local/VM proof status and any operator-accepted inconclusive rows;
- controller, aMuTorrent, REST, Torznab, or Arr behavior changes since RC1;
- new shutdown, upload/download, shared-file, WebServer, or packaging risk
  notes that should affect test selection.

Do not copy commit subjects here. Summarize the behavior and the practical
impact for people running eMuleBB.

## RC1 vs Stock/Community Baseline

Baseline: stock/community eMule `0.72a` behavior as carried by the
`baseline/community-0.72a` comparison branch. RC1 release date:
**2026-06-07**. The GitHub release record for `emulebb-v0.7.3-rc.1` reports
`published_at` as `2026-06-07T06:40:23Z`.

### Compatibility Model

RC1 keeps the native eD2K and Kad model compatible with stock eMule peers. It
does not turn eMuleBB into a new network protocol, does not require a private
tracker or server, and does not intentionally break the existing profile
layout.

The compatibility promise is narrower than "every historical eMule surface is
release-proof." The native desktop client, existing profile model, eD2K, Kad,
core uploads/downloads, search, server lists, shared files, and preferences are
the release focus. Older optional surfaces such as legacy WebServer templates,
IRC, archive preview/recovery flows, and other frozen maintenance baggage are
not treated as RC-blocking unless they affect the supported runtime path.

Do not run stock eMule and eMuleBB against the same live profile at the same
time. Use a backup or disposable copy first, especially when testing monitored
shares, part files, controller automation, or startup cache behavior.

### Release Packages and Install Shape

RC1 changes the release shape from a loose developer build to portable,
manifested release assets. The expected package set is x64 and ARM64 core ZIPs,
diagnostics ZIPs when produced by the package gate, a suite bootstrapper
PowerShell script with its SHA-256 file, SPDX SBOMs, package manifests, and an
optional x64 aMuTorrent controller ZIP.

The package manifests record the ZIP hash, selected executable hash, expected
language DLL set, per-file hashes, SBOM hash, and bootstrapper identity. This is
meant to let power users verify exactly which binary and resource set they are
testing. The release ZIPs are not code-signed, do not include debug symbols,
and do not bundle optional `MediaInfo.dll`.

The stock language DLL set is part of release gating. RC1 packaging verifies
that architecture-specific ZIPs contain the matching executable and language
DLLs, reject source/build/debug artifacts, and include the package README,
release notes, GPL text, third-party notices, REST documentation, manifest, and
SBOM.

### Profile Selection and Test Isolation

RC1 adds first-class profile isolation via `-c <base-dir>`. This is important
for release testing because it lets a tester point eMuleBB at a disposable
profile root without moving the main profile by hand.

Startup diagnostics and command-line handling were expanded around the release
flow. The supported command-line surface includes profile selection, help
flags, instance handling, generated WebServer certificate actions, selected
diagnostic export paths, and positional forwarding for add-link/file entry
points. This makes repeatable local and VM tests practical without requiring a
developer checkout.

### Broadband Upload Behavior

RC1 changes the stock-style upload defaults toward broadband operation. The
upload queue uses a finite modern slot target instead of letting slots grow in
an effectively unbounded way under high configured upload limits. Slow or
zero-rate slots can be recycled so they do not pin capacity indefinitely.

Low-ratio behavior is treated explicitly in queue scoring and visibility. This
does not remove eMule-style sharing incentives, but it makes broadband queue
state easier to reason about when many peers are connected and many files are
shared.

Several defaults and ceilings were raised or modernized for large profiles:
queue limits, source limits, buffers, timeouts, and search ceilings are tuned
for current machines and broadband links rather than early-2000s assumptions.
These changes are user-visible mostly under load: more peers, more files, more
sources, and longer sessions can be handled before legacy limits become the
first bottleneck.

### Downloads, Disk Safety, and Filename Hygiene

RC1 keeps normal part-file resume semantics but adds stronger guardrails around
placement and disk pressure. Protected-volume floors and part metadata checks
reduce the chance that automation or controller intake writes into an unsafe
location or continues into a known bad disk state.

Remote filename intake now performs conservative cleanup before the name is
used in the UI or on disk. That includes existing invalid-character cleanup and
additional repair for bounded HTML/XML entities and common Western mojibake.
This is designed to improve messy network-origin names without becoming a broad
automatic transliteration engine.

Category and qBittorrent-style workflow polish is included for power users who
operate many downloads at once. Shortcut and batch actions were added where
they preserve eMule semantics. Completed-download automation can optionally
launch an external command, which should be treated as a local power-user hook
and configured carefully.

### Shared Files and Large Libraries

Long-path handling was hardened across profile, temp, incoming, shared-library,
package, and tooling paths. This matters for modern media libraries where deep
folder trees and long release names are common.

Shared-file startup behavior includes cache work for large libraries, duplicate
tracking, monitored shares, and UI virtualization in the Shared Files view.
These changes are aimed at reducing startup and UI cost when many directories
or files are shared.

`shareignore.dat` is a supported release-facing sharing policy input. Use it to
keep generated, private, transient, or controller-owned files out of the shared
library rather than relying only on manual folder hygiene.

Optional peer preview for shared videos remains conditional on the file being
visible and the local media tooling being configured. It should not be treated
as a core sharing or transfer requirement.

### Network Binding, Bootstrap, and UPnP

RC1 adds stronger binding coverage for P2P sockets, including peer TCP, client
UDP, server UDP, pinger, and UPnP paths. The goal is predictable behavior on
multi-interface systems, VPN-bound systems, and hosts with both public and
private adapters.

The WebServer/REST bind is a separate concern from P2P binding. Treat the
controller HTTP/HTTPS endpoint as a local automation surface with its own
address, certificate, and exposure decisions. Do not assume that binding P2P to
one interface automatically makes the WebServer safe to expose.

P2P UPnP and WebServer UPnP are also separate. This matters when testing NAT
behavior: a successful peer-port mapping does not imply that the controller
port should be mapped or reachable externally.

Server list, Kad node, IP-filter, and geolocation seed/update paths were
adjusted for a practical release setup. IPv6 is still future-facing rather than
a release-complete Kad/eD2K parity surface.

### REST, aMuTorrent, Torznab, and Arr Workflows

RC1 introduces an authenticated in-process JSON REST API under `/api/v1`. It is
the preferred automation surface for release testing and for modern controller
workflows. REST coverage includes transfer detail, add-transfer flows, search,
server/Kad bootstrap operations, upload queue visibility, and a wider
preference surface.

The REST API enables qBittorrent-style, Torznab, and Arr-facing workflows
without changing the underlying eD2K/Kad transfer model. Adapters are
compatibility layers for automation, not a promise that every qBittorrent API
semantic maps one-to-one to eMule.

aMuTorrent is packaged as an optional controller asset, separate from the core
eMuleBB ZIPs. The RC package proof is x64-only for this controller. Native ARM64
aMuTorrent packaging requires a deliberate ARM64 Node/native-module path before
it can be treated as release-ready.

Controller and WebServer hardening includes typed errors, authentication
handling, TLS/certificate generation support, static-file boundaries, socket
lifecycle checks, and browser smoke coverage. Treat the controller endpoint as
trusted-local unless a later release explicitly documents an internet-exposed
security posture.

### Preferences and Power-User UI

RC1 includes a preference inventory and stronger schema checks for storage
keys, REST bindings, and Preferences UI source bindings. The practical result
is fewer silent mismatches between what the UI shows, what the REST API exposes,
and what the profile stores.

Power-user desktop polish includes advanced context menus, keyboard shortcuts,
tray preference cleanup, category handling, Web Interface preference layout
work, and MiniMule polish. These are release-facing usability changes, but they
do not change the core network compatibility model.

Display and date/time behavior received release-facing cleanup, including
locale-aware formatting and clearer timestamp customization paths. This matters
for users comparing log files, transfer history, shared-file activity, and
controller output.

### Diagnostics and Support Evidence

RC1 makes diagnostics more explicit. Release testing relies on redacted
diagnostic snapshots, startup traces, performance logs, package manifests,
SBOMs, and structured campaign reports rather than informal screenshots or
manual notes.

Diagnostics builds can include startup, packet, upload-slot, download-slot, and
bad-peer instrumentation. Standard release packages must not accidentally ship
those diagnostics-only binaries in place of the normal executable.

For support or bug reports, the useful evidence is the package identity,
profile isolation method, bind/interface settings, relevant controller endpoint
configuration, logs, and exact repro steps. A bare "it is slower than stock" or
"Arr cannot add a download" report is usually not enough to distinguish network,
profile, controller, and package issues.

### Security and Exposure Notes

RC1 release assets are portable and unsigned. Verify hashes and package
manifests before using them on an important host. Prefer a disposable profile
for first-run testing and keep the stock profile backed up.

REST/WebServer automation should be treated as a local trusted-control surface.
Use explicit binds and generated certificates where appropriate. Do not expose
controller endpoints to the public internet just because the P2P client itself
is reachable from the internet.

Automatic update/check behavior is release-scoped around GitHub release checks
and package evidence. The older broad legacy updater model is not the release
trust model for RC1.

### Known Deferred or Frozen Areas

The following areas are not stock-vs-RC1 promises for release readiness:

- legacy WebServer HTML templates as a shipped UI payload;
- IRC and other old optional community surfaces;
- archive preview/recovery flows;
- IPv6 Kad/eD2K parity;
- internet-exposed REST/WebServer security posture;
- ARM64 aMuTorrent package proof;
- running multiple eMule/eMuleBB clients against one profile concurrently.

These are either intentionally frozen, deferred to later roadmap work, or
outside the release proof boundary for the 0.7.3 RC train.
