# Getting Started

eMuleBB Rust is a headless IPv4 eD2K/Kad client with a browser console and REST
API. Start with a [matching nightly package](GUIDE-DOWNLOADS-PLATFORMS.md), verify
its checksum, and keep the complete extracted layout, including `webui`. No Rust
toolchain is needed to use the native packages.

The typed settings commands in this guide require a build that includes
[Public Foundation Round One](../design/PUBLIC-FOUNDATION.md). For an earlier
nightly, use the README shipped with that package.

![eMuleBB Rust WebUI Search view](../../../assets/emulebb-rust/webui-eac9b37a6e20.png){ width="1280" height="720" }

Controlled Windows x64 candidate-package capture from
[source commit `18f09ef`](https://github.com/emulebb/emulebb-rust/commit/18f09ef201450f722d6a58b252c66498e7fef9aa).

## First Launch

Use the [platform download and run guide](GUIDE-DOWNLOADS-PLATFORMS.md) to select
and launch the matching Windows ZIP, Linux DEB/AppImage/musl archive, macOS app,
Ubuntu/Alpine container, or Android alternative. Installed CLI paths require an
explicit writable profile. The Android 12+ APK candidate requires an explicit Start and
storage access; its shell supplies the generated API key and Open WebUI action.
Experimental Termux users keep the complete native archive under private
`$HOME` and use its `run-developer.sh` launcher.

Native nightly packages provide the ready bootstrap described below. Use the
README shipped with your selected package for its exact qualified behavior.

Without `--profile`, the daemon uses the **directory containing its executable**
on every platform, independently of the shell working directory. A missing
bootstrap is created from the canonical packaged template. There is no home,
XDG or Local AppData fallback; an unwritable executable directory fails visibly.
Open `http://127.0.0.1:20017/` and enter
`change_me_123change_me_123change_me_123`. Choose your own key in the private
`emulebb-rust-settings.toml` bootstrap for your deployment. Existing profiles are never
overwritten by startup. Use `--profile <writable-directory>` to override the
profile; missing directories/configuration are created. Relative arguments
resolve from the shell working directory. `--profile .` equals the default only
when the shell working directory is the executable directory.

| Launch mode | Profile selection |
| --- | --- |
| Direct daemon, every platform | Directory containing the executable |
| Explicit `--profile <directory>` | Selected directory; relative to shell working directory |
| Linux desktop launcher / AppImage | Explicit `$XDG_CONFIG_HOME/emulebb-rust` or `~/.config/emulebb-rust` |
| macOS app launcher | Explicit `~/Library/Application Support/emulebb-rust` |
| Official container | Explicit `/config/emulebb-rust` |
| Android APK | App-owned private profile; controlled by the foreground service |
| Android native archive / Termux | Directory containing the executable, or explicit `--profile` |

Installed CLI binaries may live in read-only directories; pass a writable
`--profile` instead of running them with elevated permissions. A profile
override does not repair an incompatible database.
The one-shot [stock/MFC importer](GUIDE-PROFILE-IMPORT.md) retains its explicit
manifest-validation workflow.

For portable updates, preserve your selected TOML/database and replace program
files deliberately. Raw archive extraction follows the extractor's overwrite
choice; it is not configuration merging or profile management.

**REST binding does not select offline P2P.** Startup may fetch trusted discovery
inputs and start configured networking. Use a deliberately isolated configuration
and the supported harness when testing offline; a first launch is not that harness.

## Profile And Control-Plane Settings

The minimal bootstrap TOML owns REST binding/authentication and optional asset
location. The canonical ready configuration is:

```toml
[rest]
bind_addr = "0.0.0.0:20017"
api_key = "change_me_123change_me_123change_me_123"
```

Startup rejects
blank, documented placeholder, whitespace-padded, non-printable and shorter-than-32
character keys. The ready starter key has 39 ASCII characters. Unix profile and
bootstrap permissions are private (`0700`/`0600`); permissive existing bootstrap
files are rejected with a remediation message. Never commit this file.

Mutable client/network settings live in SQLite and are exposed by Settings and
the [API](../api/GUIDE-API-CONSUMERS.md). Do not add a second set of runtime keys
to bootstrap TOML. The default listener accepts connections on every IPv4
interface. Open `http://127.0.0.1:20017` locally or use the host's address from
another device. The daemon serves authenticated plain HTTP. `webui` normally sits beside the executable;
optional `[rest].web_root_dir` resolves relative to the profile when not absolute.

## Connect And Check Reachability

Review **Network**, **Servers** and **Kad** in the console. Check your intended
P2P interface and incoming/category directories before starting transfers.
First-run listener defaults are eD2K TCP 20019, Kad UDP 20020 and REST TCP 20017.
Router/firewall/container mappings must match your chosen settings; High ID is
not guaranteed behind every NAT, router or VPN.

If route detection is ambiguous, stop the daemon and save the intended interface:

```text
emulebb-rust --profile "PATH_TO_PROFILE" settings set network.p2p.bindInterface "INTERFACE_NAME"
```

Restart the daemon after saving. Resolve an ambiguous P2P bind before starting
transfers. VPN use is optional and does not itself establish native leak-safety proof.

Fresh discovery initialization is tracked in SQLite independently of list
contents. Failed initialization leaves the console available and retries at the
next launch. An explicitly initialized empty list stays empty; Kad does not
silently use hidden fallback seeds, while explicit operator bootstrap endpoints
remain available. Validated `server.met`/`nodes.dat` input records are imported
into SQLite; those source files are not written as profile state. Runtime
persistence qualification remains tracked by
[RUST-FEAT-062](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-FEAT-062.md).

## Search, Download And Share

After connecting, search for a synthetic name such as **Sample File**, inspect
the result and choose its download action. Watch **Transfers** for sources,
progress and errors. An empty search alone does not mean installation failed;
availability, server/Kad state, peers, queues and reachability affect results.
Only download content you are entitled to access.

Add an intentionally chosen folder under **Shared Directories**, review ignore
rules, and watch scan/hash progress in **Shared Files**. Each shared root is a
recursive, monitored tree. There are no single-file sharing-management controls
or non-recursive mode. Use a dedicated sample directory rather than your home
directory; review the files it contains before sharing.

## Shutdown, Updates And Rollback

Stop gracefully using the console/API shutdown operation or the process/service's
normal stop. Preserve the stopped profile, payloads and old binary before an
update. Inspect the selected nightly's schema warning and source revision.

Minimal TOML bootstrap settings have a stability goal separate from the beta's
explicitly unstable API/database. An incompatible schema is visibly rejected
and requires an **entirely fresh profile**. The client does not migrate, reset,
delete, move or partially repair the old profile. Keep it and its payloads intact
for explicit rollback with the matching old binary. Do not edit schema markers,
delete the database, use internal harness migrations or promise automatic
continuation of unfinished transfers in a new incompatible profile.

The stock/MFC importer is a separate read-only source import into the current
Rust schema. It does not provide cross-version Rust database migration or carry
unfinished downloads. See [the import guide](GUIDE-PROFILE-IMPORT.md).

## Logging And Listener Troubleshooting

Regular builds log INFO and above to the console, bounded REST buffer and daily
JSON Lines under `<profile>/logs`. The logger retains the newest eight files;
file-output failure warns and leaves console/API logging available. `RUST_LOG`
controls the tracing filter, for example `warn` or `info,emulebb_core=debug`.
The API buffer retains 2,000 entries and truncates rendered messages at 4 KiB;
clearing that buffer does not delete retained files.

On Windows, REST socket error 10013 means access denied. It can involve reserved
ports, exclusive socket ownership or security software. Inspect the REST address
in the error separately from your P2P interface. For the default port:

```powershell
netsh interface ipv4 show excludedportrange protocol=tcp
Get-NetTCPConnection -LocalPort 20017 -ErrorAction SilentlyContinue
```

Choose an available loopback port if needed. Stop the daemon and set
`bind_addr = "127.0.0.1:14711"` under `[rest]` in the private bootstrap TOML.
Restart the daemon and browse to that address. This does not change eD2K/Kad
ports. For ambiguous P2P routing,
`Get-NetAdapter | Select-Object Name, Status` identifies Windows interface names;
save the intended name with the offline settings command above, then restart.

The browser console is served at the REST origin root, with history routes such
as `/downloads` and static `/assets`. Reverse-proxy subpath mounting is not part
of the current deployment contract. Keep the complete packaged asset directory.

## Common Problems

| Symptom | First check |
| --- | --- |
| Executable will not start | CPU/package match and the selected build's host dependencies |
| Console assets missing | Complete package layout, adjacent `webui`, configured asset root |
| API returns 401 | Exact private `X-API-Key`; do not substitute Basic/Bearer authentication |
| REST bind fails | Occupied/reserved port and configured loopback listener, separately from P2P |
| Default route ambiguous | Explicit intended P2P interface, then persist through Settings |
| Schema rejected | Preserve the old profile; select an entirely fresh profile for the new binary |

Regular logs are available in the console, bounded API log buffer and retained
profile log files. Diagnostic bundles are **private operator evidence** and can
contain the exact API key, paths, identifiers and logs. Do not attach them
unreviewed to a public issue. Report suspected vulnerabilities through the
[private security route](https://github.com/emulebb/emulebb-rust/security/advisories/new).

Next: [API consumers](../api/GUIDE-API-CONSUMERS.md),
[contributors](GUIDE-CONTRIBUTING.md), or [release scope](../RELEASE-SCOPE.md).
