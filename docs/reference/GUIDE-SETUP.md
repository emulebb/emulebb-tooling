# eMuleBB Setup Guide

This guide covers practical setup for eMuleBB. It complements the
[Product Guide](GUIDE-EMULEBB.md), which remains the user-manual entry point.

## Quick Install: ZIP, Extract, Run

This is the recommended first path for most users and release testers:
download the eMuleBB ZIP, extract it into a new folder, and run
`emulebb.exe`.

1. Open <https://github.com/emulebb/emulebb/releases>.
2. Download the intended package ZIP. For RC1, use
   `emulebb-0.7.3-rc.1-x64.zip` once that asset is published, or use the
   approved nightly or release asset that is actually present on GitHub
   Releases.
3. Extract the ZIP into a new application directory, for example
   `C:\Apps\eMuleBB\0.7.3-rc.1`.
4. Run `emulebb.exe`.
5. On first run, choose directories and ports before serious use.
6. For controlled testing, launch with an explicit disposable profile:

```powershell
emulebb.exe -c "$env:TEMP\eMuleBB-TestProfile"
```

Use the x64 ZIP for normal Windows desktop installs. Use ARM64 only when you
are intentionally testing on ARM64 Windows. Do not overwrite an older
application directory in place; keep each package in its own directory so
rollback is simple.

For RC and nightly testing, prefer a backed-up or disposable profile before
using a daily profile. Do not treat `0.7.3-rc.1` as published until the release
page has the asset; use the latest approved release or nightly package actually
listed on GitHub Releases.

## Install Model

Keep the application, profile, temp, incoming, and shared directories separate.
This makes upgrades, rollback, troubleshooting, and disk-space protection
predictable.

| Location | Purpose |
|---|---|
| Application directory | Executable, bundled runtime assets, skins, toolbar assets |
| Config/profile directory | Identity, preferences, server/Kad state, lists, logs, and sidecars |
| Temp directory | Incomplete `.part` and `.part.met` files |
| Incoming directory | Completed downloads |
| Shared directories | User-selected publish roots |

```mermaid
flowchart TD
    Launch["emulebb.exe -c <profile-base>"]
    AppDir["Application directory<br/>exe, DLLs, packaged assets"]
    Profile["Profile base<br/>operator-owned state root"]
    Config["config<br/>preferences.ini, identity, lists"]
    Logs["logs<br/>runtime diagnostics"]
    Temp["Temp directory<br/>.part and .part.met files"]
    Incoming["Incoming directory<br/>completed downloads"]
    Shared["Shared roots<br/>intentional published files"]

    AppDir --> Launch
    Launch --> Profile
    Profile --> Config
    Profile --> Logs
    Config --> Temp
    Config --> Incoming
    Config --> Shared
```

Do not run multiple eMule-family clients against the same live profile. Before
reusing an existing profile, close all clients and copy the full config
directory as a rollback backup.

## Full Suite Install: PowerShell Bootstrap

Use this second path when you want the full suite/bootstrapper flow instead of
only unpacking and running the desktop app. The bootstrapper installs the
versioned eMuleBB suite from GitHub Releases and can hand off to the bundled
suite installer.

Download `Bootstrap-eMuleBBSuite.ps1` from the release page, open PowerShell in
that download folder, and run the bootstrapper.

For the latest nightly or prerelease:

```powershell
.\Bootstrap-eMuleBBSuite.ps1 -IncludePrerelease
```

For RC1 after it is published:

```powershell
.\Bootstrap-eMuleBBSuite.ps1 -Version 0.7.3-rc.1 -IncludePrerelease
```

The bootstrapper is published as a release asset, so setup does not depend on
the current `main` branch. It resolves the requested release, latest stable
release, or latest prerelease when `-IncludePrerelease` is used. It verifies
the release ZIP against its manifest SHA-256, extracts the versioned suite
installer, and hands off to that installer. The versioned installer is also
included in the main app ZIP under `eMuleBB\scripts`.

To verify the bootstrapper itself before running it, compare the local hash
with the adjacent `Bootstrap-eMuleBBSuite.ps1.sha256` release asset:

```powershell
Get-FileHash -Algorithm SHA256 .\Bootstrap-eMuleBBSuite.ps1
```

### Advanced Split-Tunnel Or Remote Bind

Use this only when a split-tunnel VPN or remote-control setup makes loopback
unsuitable. Set `X_LOCAL_IP` to the machine's LAN IPv4 address before running
the bootstrapper:

```powershell
$env:X_LOCAL_IP = '192.0.2.10'
.\Bootstrap-eMuleBBSuite.ps1 -IncludePrerelease
```

The suite installer uses that address as the default control-service bind and
still warns when services are exposed beyond loopback. Keep ordinary local
installs on the default loopback-oriented path.

## Choose Directories

Use stable paths that will still exist after reboot:

- Put the application under a normal install or unpack directory.
- Put the config/profile directory somewhere writable by the user account that
  runs eMuleBB.
- Put temp files on a fast, reliable local disk with enough free space.
- Put incoming files on the final storage volume when possible.
- Add shared directories deliberately, especially for large libraries.

Avoid using removable drives for temp files unless they are always present
before the app starts. Avoid network paths for temp files. Network paths may be
reasonable for selected shared directories, but they are slower and less
predictable than local NTFS volumes.

For long paths, use modern Windows long-path support and avoid deeply nested
library layouts until the profile is known to work. See
[Long Path Guide](GUIDE-LONGPATHS.md).

## New Profile Recipe

Use this path for a clean first profile:

1. Start eMuleBB with a new config/profile directory.
2. Open `Preferences > Directories`.
3. Choose incoming and temporary directories.
4. Open `Preferences > Connection`.
5. Set TCP and UDP ports.
6. Leave bind settings empty unless you need a specific interface or address.
7. Enable UPnP only when the router and local policy allow it.
8. Connect to trusted eD2K and/or Kad bootstrap sources.
9. Add one small shared directory and verify it on the Shared Files page.
10. Run a small search or add a known safe link before scaling up.

The legacy first-run connection wizard is a frozen surface. Treat the
Preferences pages and the product guides as the supported setup path.

Before adding a large shared library, review
[Sharing Guide](GUIDE-SHARING.md#large-library-operation). The first run should
prove one curated root, peer-preview policy, cache behavior, and monitored-share
scope before broad roots or automation are enabled.

## Existing Profile Recipe

Use this path when moving from stock eMule or another eMule-family build:

1. Close all eMule-family clients.
2. Back up the full config directory, not just `preferences.ini`.
3. Keep temp and incoming paths stable when possible.
4. Start eMuleBB once without controllers or automation.
5. Verify connection state, downloads, shared files, categories, and logs.
6. Let eMuleBB create branch-specific sidecars and caches before heavy use.
7. Re-enable controllers, automation, and large sharing only after the profile
   looks healthy.

Common profile files include:

- `preferences.ini` and `preferences.dat`
- `server.met` and `nodes.dat`
- `known.met`, `known2_64.met`, and `cancelled.met`
- `Category.ini`
- `ipfilter.dat` and `addresses.dat`
- `shareignore.dat` and `shareddir.dat`
- monitored-share files and shared-cache sidecars
- active `.part.met` files for incomplete downloads

For `.met` and `.dat` roles, structures, and recovery priority, use the
[Persistence Files](GUIDE-PERSISTENCE-FILES.md) reference.

If the old profile has stale paths, fix directories before starting downloads.
If the old profile has broad shared roots, let scanning finish before judging
performance.

## Isolated Profile Recipe

Use `-c <base-dir>` when you need a separate test, live, or operator profile:

```powershell
emulebb.exe -c C:\eMuleBB-Profiles\live
```

The path must be an absolute canonical Windows path. eMuleBB creates the base
directory, `config`, and `logs` when they are missing. The effective
preferences file is `config\preferences.ini` under that base. If that file
already exists and contains `IncomingDir` or `TempDir`, those paths take
precedence over the clean-profile defaults. Do not point two running clients at
the same base directory.

An isolated base is useful for:

- testing a new package without touching a production profile
- running a live proof profile with controlled inputs
- reproducing a support problem with a copy of a profile
- separating controller/API experiments from daily use

Keep profile backups outside the live base directory so they are not mistaken
for active config files.

## Legacy Profile Directory Mode

Prefer `-c <base-dir>` for every test, support, and operator profile. It makes
the profile root explicit in the launch command and avoids ambiguity when
packages are moved between machines.

When `-c` is not used, eMuleBB still honors its branch-specific registry value
`HKCU\Software\eMuleBB\UsePublicUserDirectories` to choose the default profile
directory model:

| Value | Mode | Effect |
|---|---|---|
| `0` | Multiuser | Use the per-user Windows application-data profile layout. |
| `1` | Public user | Use the public/shared Windows application-data profile layout. |
| `2` | Executable directory | Store profile/config state beside the executable. |

This registry-backed mode is mainly compatibility and recovery behavior. If a
profile appears to be "missing" after a package move or account change, check
whether the app was launched without `-c` and whether this registry value points
the app at a different default profile layout. Do not use registry edits as a
routine profile switcher; create an explicit profile directory and launch with
`-c` instead.

## Command-Line Startup

The normal startup path is the desktop executable with the selected profile.
Command-line options are for controlled profile isolation, automation, support,
and WebServer certificate maintenance.

```text
emulebb.exe [options] [ed2k-link|magnet-link|collection-file|command]
```

Supported options:

| Option | Use |
|---|---|
| `--help`, `-h`, `/?` | Print usage and exit |
| `-c <base-dir>` | Use an isolated eMule base directory |
| `-ignoreinstances` | Start without the running-instance guard unless input must be forwarded |
| `-AutoStart` | Mark the session as automatic startup |
| `-assertfile` | Debug-build assertion logging helper |
| `--generate-webserver-cert` | Generate a WebServer TLS certificate and exit |
| `--cert <path>` | Certificate output path for certificate generation |
| `--key <path>` | Private-key output path for certificate generation |
| `--host <dns-or-ip>` | Certificate subject alternative name; repeatable |
| `--diagnose-media-metadata` | Probe maintained media metadata extractors and exit |
| `--input <path>` | Media file path for metadata diagnostics |
| `--output <path>` | Optional JSON output path for metadata diagnostics |

Only one positional argument is supported. Use it for an `ed2k` link, magnet
link, collection file, or supported command such as `exit`.

Metadata diagnostics produce the `emulebb.mediaMetadataDiagnostic.v1` JSON
schema and include the input path. Use them for controlled support or release
proof, not as an anonymous public telemetry artifact.

## Network Setup Recipe

For ordinary home or lab use:

1. Choose fixed TCP and UDP ports.
2. Allow the app through Windows Firewall.
3. Configure router forwarding manually or enable P2P UPnP.
4. Connect to eD2K and Kad.
5. Check for High ID and non-firewalled Kad state.
6. If Low ID or firewalled Kad remains, use
   [Troubleshooting Guide](GUIDE-TROUBLESHOOTING.md).

Leave bind settings empty unless the machine has multiple active network paths,
a VPN/interface requirement, or an operator-controlled routing policy. When
binding is required, prefer explicit interface/address configuration and verify
the resolved bind state in diagnostics.

Binding is not a VPN kill switch. Keep VPN provider kill-switch, route, and
Windows Firewall policy separate from eMuleBB bind settings, and configure the
WebServer/REST bind address independently from P2P bind policy.

## Controller Setup Recipe

For trusted local automation:

1. Finish normal desktop setup first.
2. Open `Preferences > Web Server`.
3. Enable the WebServer/REST listener only when needed.
4. Bind to localhost, `X_LOCAL_IP`, or a controlled interface.
5. Use a strong API key/password.
6. Add firewall rules that match the intended exposure.
7. Generate or configure HTTPS material if the controller path requires it.
8. Test with a simple status/read request before allowing mutations.

REST is the supported controller surface. The legacy HTML template UI is frozen
pending removal and should not be treated as a maintained setup target. See
[Controllers and REST Guide](GUIDE-CONTROLLERS-REST.md). For a full
eMuleBB plus aMuTorrent plus Prowlarr/Radarr/Sonarr setup, use the
[Stack Integration Guide](GUIDE-STACK-INTEGRATIONS.md).

## Release-Aware Setup

The current official public test line is 0.7.3 RC1. Use packages attached to
`emulebb-v0.7.3-rc.1` or a later approved release tag. Treat nightly and older
beta builds as pre-release packages unless the release notes explicitly direct
a test run to them.

Before trusting a package:

- Confirm the tag name matches the documented release family.
- Confirm the package architecture matches the machine.
- For eMuleBB nightly assets, verify the GitHub artifact attestation when you
  can:

  ```powershell
  gh attestation verify PATH_TO_ASSET -R emulebb/emulebb
  ```

- Keep a copy of the previous working package.
- Back up the profile before first launch.
- Check release notes for frozen, removed, or unsupported legacy surfaces.
- Start once without controllers or automation after upgrade.

When testing a nightly:

- Prefer a disposable profile for first launch.
- Use an explicit config path with `emulebb.exe -c <profile-path>`.
- Never run another eMule-family client against the same profile at the same
  time.
- Record the package name, architecture, profile type, and repro steps before
  reporting a failure.

Setup confidence comes from the same release evidence model used elsewhere:

- hosted fast CI for shared harness checks
- local native and Python test coverage
- REST/controller validation
- UI and stock-language resource smoke coverage
- live eD2K/Kad and live-wire scenarios
- x64 and ARM64 package provenance with recorded hashes

See [Release Test Strategy](../active/RELEASE-TEST-STRATEGY.md),
[Release Test Campaigns](../active/RELEASE-TEST-CAMPAIGNS.md), and the
[0.7.3 RC1 dashboard](../active/RELEASE-0.7.3.md) for the current release
proof model.

## Unsupported Setup Targets

These legacy surfaces may still appear in old resources or code, but they are
not maintained setup workflows:

- first-run connection wizard
- legacy Scheduler
- IRC and IRC-adjacent chat UI
- SMTP/email notifications
- proxy support
- legacy WebServer HTML templates and page UI
- archive preview and archive recovery

Use [Frozen Surfaces](../active/FROZEN-SURFACES.md) when deciding whether a
legacy setup path should be documented, tested, or removed.
