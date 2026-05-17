# eMule BB Setup Guide

This guide covers the practical setup model for eMule BB. It complements the
[Product Guide](GUIDE-EMULEBB.md), which remains the main product entry point.

## Install Model

Keep the application, profile, temp, incoming, and shared directories separate:

| Location | Purpose |
|---|---|
| Application directory | Executable, bundled assets, WebServer templates, skins, toolbar assets |
| Config/profile directory | Identity, preferences, server/Kad state, lists, logs, and sidecars |
| Temp directory | Incomplete `.part` and `.part.met` files |
| Incoming directory | Completed downloads |
| Shared directories | User-selected publish roots |

Do not run multiple eMule-family clients against the same live profile. Before
reusing an existing profile, close all clients and copy the full config
directory as a rollback backup.

## First Run

For a new profile:

1. Start eMule BB and complete the first-run setup.
2. Choose incoming and temporary directories.
3. Configure TCP and UDP ports in `Preferences > Connection`.
4. Leave bind settings empty unless a specific interface or address is needed.
5. Enable UPnP only when the router and local policy allow it.
6. Bootstrap trusted eD2K servers and/or Kad sources.
7. Add shared directories gradually and verify the Shared Files page.
8. Start with a small search or download before scaling the workload.

For an existing profile:

1. Back up the full config directory while the app is closed.
2. Keep temp and incoming paths stable when possible.
3. Start once without controllers or automation.
4. Verify connection state, downloads, shared files, categories, and logs.
5. Let eMule BB create branch-specific sidecars and caches before heavy use.

## Command-Line Startup

The normal startup path is the desktop executable with the default profile.
Command-line options are for controlled profile isolation, automation, support,
and WebServer certificate maintenance.

```text
emule.exe [options] [ed2k-link|magnet-link|collection-file|command]
```

Supported options:

| Option | Use |
|---|---|
| `--help`, `-h`, `/?` | Print usage and exit |
| `-c <base-dir>` | Use an isolated eMule base directory with config and log folders under that base |
| `-ignoreinstances` | Start without the running-instance guard unless a link, magnet, collection, or command must be forwarded |
| `-AutoStart` | Mark the session as automatic startup |
| `-assertfile` | Debug-build assertion logging helper |
| `--generate-webserver-cert` | Generate a WebServer TLS certificate and exit |
| `--cert <path>` | Certificate output path for certificate generation |
| `--key <path>` | Private-key output path for certificate generation |
| `--host <dns-or-ip>` | Certificate subject alternative name; repeatable |

Only one positional argument is supported. Use it for an `ed2k` link, magnet
link, collection file, or supported command such as `exit`.

`-c <base-dir>` is the release-safe way to keep test, live, and operator
profiles isolated. Use an absolute canonical Windows path and do not point two
running clients at the same live profile.

## Release-Aware Setup

The first public beta line is planned as `0.7.3` and is not released until the
active release dashboard says the gates have passed. Treat current builds as
pre-release unless they are attached to an approved release tag and package.

Setup confidence comes from the same release evidence model used elsewhere in
the workspace:

- hosted fast CI for shared harness checks
- local native and Python test coverage
- REST/controller validation
- UI and stock-language resource smoke coverage
- live eD2K/Kad and live-wire scenarios
- x64 and ARM64 package provenance with recorded hashes

See [Release Test Strategy](../active/RELEASE-TEST-STRATEGY.md),
[Release Test Campaigns](../active/RELEASE-TEST-CAMPAIGNS.md), and the
[Beta 0.7.3 dashboard](../active/RELEASE-0.7.3.md) for the current release
proof model.
