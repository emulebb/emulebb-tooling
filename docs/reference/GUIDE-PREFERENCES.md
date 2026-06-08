# Preferences Guide

This is the single English reference for eMuleBB preferences,
`preferences.ini`, preference compatibility policy, and the REST preference
surface. It replaces the older split between a user guide, a preference
architecture note, and a separate preference matrix.

The complete key reference in this guide is aligned with
`repos/emulebb-build-tests/manifests/preference-schema.v1.json`. The guide covers
only schema rows whose storage file is `preferences.ini`; category records,
statistics-only files, and UI-runtime rows are summarized in prose.

## Storage Model

`preferences.ini` is the main text configuration file for eMuleBB. It contains
several different kinds of data:

- user-facing Preferences dialog settings
- hidden and runtime behavior switches
- WebServer and REST listener settings
- branch-owned broadband, IP filter, geolocation, and file-completion settings
- UI layout, presentation, counters, and generated state families
- legacy keys that current code may still read for compatibility or tombstone
  handling

Not every row is a user preference. Some rows are runtime state, compatibility
state, or generated UI layout records. The complete key reference below marks
those classifications explicitly.

## Source Of Truth

Use these sources when changing preference behavior:

- app source load/save behavior
- preference defaults, getters, setters, and normalizers
- Preferences dialog bindings
- REST preference metadata and OpenAPI
- the JSON preference schema in `emulebb-build-tests`
- this guide

For docs-only preference changes, compare the schema to this guide before
committing. If code changes add, remove, rename, re-section, or reclassify a
preference, update the schema and this guide together.

## Compatibility Policy

eMuleBB preserves stock/community drop-in compatibility unless a change is
explicitly chosen as a compatibility break.

Rules:

- established stock keys stay in their established sections
- key lookup is case-insensitive, but writes use canonical casing
- direct INI values are normalized when old code historically tolerated invalid
  values
- new user input should prefer explicit UI/REST validation over silent rewrite
- string reads and writes go through the shared Unicode INI/profile path
- eMuleBB-owned sections are used only where they make behavior clearer without
  breaking stock placement

Known case-only canonical writes include `StatsInterval`, `AutoCat`,
`UpOverheadTotal`, and `UpOverheadTotalPackets`.

## Sections

Important sections:

- default section: most stock and branch settings
- `[FileCompletion]`: file-completion command enable/program/arguments
- `[UploadPolicy]`: broadband upload/session policy
- `[UPnP]`: UPnP enable, close-on-exit, and backend mode
- `[WebServer]`: WebServer, REST listener, credentials, API key, HTTPS, bind,
  upload limit, allowed IPs, and legacy web UI switches
- `[Proxy]`: proxy connection settings
- `[Statistics]`: statistics display/state records
- `[PerfLog]`: performance logging configuration
- `[ListControlSetup]`: generated UI list-control layout state

Branch-added geolocation and IP-filter updater keys remain in the default
section to stay near stock security/advanced behavior.

## Operational Preference Notes

### GitHub Releases Update Check

The current `Check for eMuleBB updates` option checks GitHub Releases at startup
when the configured interval has elapsed and only alerts when a newer eMuleBB
package is available. This is not the old stock eMule update checker that
pointed at defunct update infrastructure.

Disable it for quiet startup. Enable it when the profile should periodically
tell the operator that a newer package is available.

### Auto Broadband I/O

`AutoBroadbandIO` is the REST/UI-facing switch for bounded broadband download
buffering. When enabled, eMuleBB builds a global download-buffer budget from
25% of currently available physical RAM, clamped between 512 MiB and 4 GiB.

Hot files can use more of that budget while quiet active files retain a small
minimum share. The manual file buffer still matters only when Auto Broadband
I/O is disabled; when it is enabled, effective buffering may exceed the manual
value within the adaptive global budget.

### Performance Logging

`[PerfLog]` controls optional performance logging. CSV mode writes one
timestamped file that is easiest to inspect manually. MRTG mode writes graphing
sidecars for tools that expect MRTG-style data and overhead files.

The base path may be blank; blank means the default log path in the eMuleBB
config/log area. Short sampling intervals create finer graphs but more disk
writes. Use performance logs for repeatable diagnosis, then turn them off when
the evidence has been collected.

### Completion Commands

`[FileCompletion]` controls the optional command that runs after a download
completes. Supported argument tokens are documented in
[Downloads And Search](GUIDE-DOWNLOADS-SEARCH.md#completion-command).

Use explicit executable paths and arguments. The app does not expand
environment variables in the argument template.

## Load, Normalize, And Save

Preferences are loaded at startup through the shared INI/profile layer. Missing
keys use defaults from code, not from a template file. Direct edits are accepted
only when the local parser and normalizer accepts the stored value.

Important behavior:

- numeric limits are often clamped or normalized during load or setter calls
- empty strings can mean either default, disabled, or intentionally blank,
  depending on the key
- some settings are startup-only and require restart or reconnect
- Preferences dialog writes validated values; direct INI edits may be corrected
  or ignored on next load
- Tools menu actions such as saving preferences, editing config files, firewall
  repair, diagnostics, and quick speed changes interact with the same persisted
  state where applicable

Use `Tools > Save Preferences Now` before risky maintenance when you need an
explicit save point.

## Registry And Profile Identity

eMuleBB owns branch-specific Windows registry identity under
`HKCU\Software\eMuleBB`. It does not use stock `HKCU\Software\eMule` as a
fallback.

`UsePublicUserDirectories` is the registry-backed default profile directory
mode used when the app is launched without `-c`:

| Value | Mode |
|---|---|
| `0` | Multiuser/per-user application-data profile layout |
| `1` | Public/shared application-data profile layout |
| `2` | Executable-directory profile layout |

Treat this as startup compatibility state, not as a preferred operator control.
For reproducible testing, support, and automation, launch with
`emulebb.exe -c <profile-base>` and keep the profile root visible in the command
line or service configuration.

The Windows Run value for app autostart is `eMuleBBAutoStart`. The collection
file ProgID is `eMuleBB.Collection`. The `ed2k` URL scheme is intentionally
shared by Windows, so eMuleBB only claims it through explicit setting-driven
link-repair behavior.

Default filesystem folder names remain stock-compatible unless the user chooses
another location.

## Behavior Groups

General and profile behavior:

- identity, language, startup, tray, confirmation, update, and link-association
  settings shape how the native desktop session starts and presents itself
- profile files remain mostly stock-compatible, but eMuleBB owns its own
  registry identity and branch-specific sidecars

Connection and network behavior:

- TCP, UDP, server UDP, bind interface/address, startup bind blocking, reconnect,
  ED2K enablement, Kad enablement, and churn limits decide whether the app can
  reach peers and accept incoming traffic
- UPnP settings live under the `UPnP` section
- WebServer and REST listener settings live under `WebServer`

Transfer behavior:

- upload/download caps are finite runtime limits
- source, queue, file-buffer, commit, sparse/preallocation, free-space, and
  timeout settings are operational safety controls, not only UI options
- broadband upload policy controls slot target, slow-slot recycling, low-ratio
  scoring, and session rotation

Sharing and files:

- incoming/temp directories, shared roots, monitored-share behavior, cancelled
  and downloaded file memory, archive preview, media metadata extraction, video
  preview, filename cleanup, and completion commands affect local file handling

Security and messaging:

- IP filter, secure ident, protocol obfuscation, spam filters, share visibility,
  message source validation, captchas, and comment filters affect accepted
  network/user input

Display and state:

- list layouts, colors, toolbar, fonts, statistics, category records, and
  dynamic generated families are persisted for UI continuity
- these rows are documented because they appear in `preferences.ini`, but many
  are state rather than user-tunable contracts

## Important Defaults And Ranges

These values are the user/operator behavior highlights most often needed during
configuration and troubleshooting:

- `MaxUpload` defaults to `6100` KiB/s; invalid unlimited-like direct values
  normalize to the branch default
- `MaxDownload` defaults to `12207` KiB/s; REST rejects unlimited sentinel
  values
- `MaxConnections` uses the recommended runtime default, normally `500` on
  modern high/unlimited TCP-cap profiles
- `MaxHalfConnections` and `MaxConnectionsPerFiveSeconds` default to `50`
- missing or invalid peer TCP/UDP ports become valid randomized ports; UDP `0`
  disables UDP
- bind protection is effective only when a bind interface is configured
- `ConnectionTimeout` has a minimum of `5` seconds; default is `30`
- `DownloadTimeout` has a minimum of `5` seconds; default is `75`
- `KadFileSearchTotal` and `KadKeywordSearchTotal` clamp to `100..5000`
- `KadFileSearchLifetime` and `KadKeywordSearchLifetime` clamp to `30..180`
  seconds
- `QueueSize` clamps to `2000..10000`
- `FileBufferSize` clamps from `16` KiB through `512` MiB
- `FileBufferTimeLimit` clamps to `1..86400` seconds
- free-space floors clamp to operational GiB ranges for config, temp, and
  incoming directories
- `MaxUploadClientsAllowed` clamps to `1..32`
- IP filter update period clamps to `1..365` days
- geolocation update checks are disabled by `0`; nonzero values are `7..365`
  days
- WebServer port must be `1..65535`; invalid or `0` normalizes to default
  `4711`
- WebServer upload size clamps to `0..65535` MiB
- WebServer page refresh clamps to `0..3600` seconds
- WebServer timeout clamps to `0..1440` minutes

Exact keys, owners, UI bindings, and REST bindings are in the complete reference
below.

## Date And Time Formatting

eMuleBB uses the Windows user locale for normal date/time text. At startup the
app initializes the C runtime locale from Windows, then keeps numeric formatting
stable by forcing the numeric category back to `C`. In practice, date and time
names follow the user's Windows language and regional settings, while decimal
and protocol-oriented numeric output stays predictable.

Three persisted format strings control most native UI timestamps:

| Key | Default | Used for |
|---|---|---|
| `DateTimeFormat` | `%A, %c` | General file, friend, and peer detail displays |
| `DateTimeFormat4Log` | `%c` | Log lines and log-like status output |
| `DateTimeFormat4Lists` | `%c` | List-view timestamp columns, including Downloads timestamps and Shared Files `Last Request` |

These values are MFC `CTime::Format` format strings, which follow the C
`strftime` token model. Literal text can be written directly in the value. Use
`%%` when a literal percent sign is needed.

Common tokens:

| Token | Meaning | Example shape |
|---|---|---|
| `%c` | Locale date and time representation | user-locale date plus time |
| `%x` | Locale date representation | user-locale date |
| `%X` | Locale time representation | user-locale time |
| `%A` | Full weekday name | `Friday` |
| `%a` | Abbreviated weekday name | `Fri` |
| `%B` | Full month name | `May` |
| `%b` | Abbreviated month name | `May` |
| `%Y` | Four-digit year | `2026` |
| `%y` | Two-digit year | `26` |
| `%m` | Month number, zero-padded | `05` |
| `%d` | Day of month, zero-padded | `22` |
| `%H` | Hour, 24-hour clock, zero-padded | `14` |
| `%I` | Hour, 12-hour clock, zero-padded | `02` |
| `%M` | Minute, zero-padded | `07` |
| `%S` | Second, zero-padded | `09` |
| `%p` | Locale AM/PM marker | `PM` |
| `%j` | Day of year, zero-padded | `142` |
| `%w` | Weekday number, Sunday as `0` | `5` |
| `%U` | Week number, Sunday first day | `20` |
| `%W` | Week number, Monday first day | `20` |
| `%%` | Literal percent sign | `%` |

Useful examples:

| Format string | Output shape |
|---|---|
| `%c` | Windows locale default date/time |
| `%Y-%m-%d %H:%M:%S` | `2026-05-22 14:07:09` |
| `%d.%m.%Y %H:%M` | `22.05.2026 14:07` |
| `%A, %x %X` | full weekday plus locale date/time |

Keep custom values concise for list columns and logs. `DateTimeFormat` and
`DateTimeFormat4Log` are validated as non-empty by the Preferences UI.
`DateTimeFormat4Lists` is used directly by list controls, so an empty or
invalid direct INI edit can produce blank or confusing list timestamps.

Not every timestamp is user-formatted. Protocol, HTTP, REST, and
machine-readable outputs keep fixed formats or raw Unix timestamps where
interoperability matters. For example, HTTP `Last-Modified` uses an English GMT
wire format, REST JSON timestamp fields use Unix seconds or `null`, and some
diagnostic/performance log files intentionally use fixed machine-readable
formats.

## REST Preferences

REST exposes a curated mutable subset of preferences. It is not a general
`preferences.ini` editor. REST field names, accepted ranges, and validation
rules are defined by the OpenAPI contract and this guide.

If a preference is not listed as REST-bound in the complete reference,
controllers should not try to mutate it through REST.

Mutable REST fields:

| REST field | Backing setting | PATCH validation |
|---|---|---|
| `uploadLimitKiBps` | `MaxUpload` | integer `1..4294967294` |
| `downloadLimitKiBps` | `MaxDownload` | integer `1..4294967294` |
| `maxConnections` | `MaxConnections` | integer `1..2147483647` |
| `maxConnectionsPerFiveSeconds` | `MaxConnectionsPerFiveSeconds` | integer `1..2147483647` |
| `maxSourcesPerFile` | `MaxSourcesPerFile` | integer `1..2147483647` |
| `uploadClientDataRate` | derived upload slot target | integer `1..4294967295` |
| `maxUploadSlots` | `MaxUploadClientsAllowed` | integer `1..32` |
| `queueSize` | `QueueSize` | integer `2000..10000` |
| `autoConnect` | `Autoconnect` | boolean |
| `newAutoUp` | `UAPPref` | boolean |
| `newAutoDown` | `DAPPref` | boolean |
| `creditSystem` | `UseCreditSystem` | boolean |
| `safeServerConnect` | `SafeServerConnect` | boolean |
| `networkKademlia` | `NetworkKademlia` | boolean |
| `networkEd2k` | `NetworkED2K` | boolean |
| `autoBroadbandIo` | `AutoBroadbandIO` | boolean |

## Direct Editing

Direct editing is useful for recovery and batch maintenance, but it is not a
live-management API.

Recommended rules:

- close the app before editing startup, path, bind, WebServer, or layout state
- keep a backup of the config directory before bulk edits
- prefer UI or REST for ordinary runtime preferences
- restart or reconnect after changing network and listener keys
- do not edit binary profile files such as `preferences.dat`

## Retired And External Names

Some old names remain useful when reading historical profiles or support logs,
but current main does not read, write, migrate, or delete them unless a
dedicated migration says otherwise.

Tracked retired names include:

- `DownloadCapacity`, `UploadCapacityNew`, `UploadCapacity`
- `FileBufferSizePref`, `QueueSizePref`
- `AICHTrustEveryHash`
- `ResumeNextFromSameCat`, `AdjustNTFSDaylightFileTime`
- `SkipWANIPSetup`, `SkipWANPPPSetup`, `LastWorkingImplementation`
- `DisableMiniUPNPLibImpl`, `DisableWinServImpl`
- `UDPReceiveBufferSize`, `BigSendBufferSize`
- old same-named `UploadClientDataRate`

REST `uploadClientDataRate` is a derived controller input that updates upload
slots. It is not a same-named persisted INI preference.

## State Outside This Key Reference

This guide's full table intentionally covers only schema rows stored in
`preferences.ini`.

Other persisted surfaces:

- `Category.ini`: category title, incoming path, comments, color, A4AF priority,
  auto-category rules, filters, and category behavior flags
- statistics-only files/sections: transfer totals, overhead counters,
  connection/server/share high-water marks, graph/tree state, and color records
- UI-runtime rows without `preferences.ini` storage: source bindings and runtime
  UI/schema metadata tracked by the JSON schema
- sidecar files such as `addresses.dat`, `AC_IPFilterUpdateURLs.dat`,
  `shareignore.dat`, share directory files, startup caches, and filter files

Server.met URL history and IP filter URL history are seeded only when missing
or blank. If one of these sidecars becomes a first-class `preferences.ini`
preference, add it to the schema and this guide.

## Complete preferences.ini Reference

This section is derived from
`repos/emulebb-build-tests/manifests/preference-schema.v1.json`.

Total `preferences.ini` schema entries: **336**.

Dynamic rows are generated families tracked by source expression rather
than a finite static key list. Empty defaults or normalizers mean the
schema did not declare a single explicit value; check the behavior sections
above for user-facing defaults and ranges.

### `<default>`

#### disabled-tombstone

- **`VideoPreviewThumbnails`**
  - Type: bool
  - Access: write
  - Owner/API: m_bVideoPreviewThumbnails
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: Written as false for compatibility while runtime loading forces thumbnails
           disabled.

- **`AllowPeerPreview`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bAllowPeerPreview
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: Explicit opt-in for advertising and serving peer preview frames from shared
           video files. Requires visible shares and a valid FFmpeg executable.

#### dynamic-family

- **`<dynamic:si>`**
  - Type: string
  - Access: read
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: Dynamic family generated at runtime; source expression is guarded instead of
           enumerating every concrete key.

#### editable-rest

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `DAPPref` | bool | read, write | None | Not explicitly declared in schema | None | newAutoDown | None |
| `UAPPref` | bool | read, write | None | Not explicitly declared in schema | None | newAutoUp | None |

#### editable-ui

- **`3DDepth`**
  - Type: integer
  - Access: read, write
  - Owner/API: Get3DDepth
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`A4AFSaveCpu`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetA4AFSaveCpu, m_bA4AFSaveCpu
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`AddNewFilesPaused`**
  - Type: bool
  - Access: read, write
  - Owner/API: addnewfilespaused
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`AddServersFromServer`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bAddServersFromServer
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgServer.cpp
  - REST: None
  - Notes: None

- **`AdvancedSpamFilter`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bAdvancedSpamfilter
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgMessages.cpp
  - REST: None
  - Notes: None

- **`AlwaysShowTrayIcon`**
  - Type: bool
  - Access: read, write
  - Owner/API: IsAlwaysShowTrayIcon, m_bAlwaysShowTrayIcon
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`AutoClearCompleted`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetRemoveFinishedDownloads, m_bRemoveFinishedDownloads
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`AutoFilenameCleanup`**
  - Type: bool
  - Access: read, write
  - Owner/API: AutoFilenameCleanup, autofilenamecleanup
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`AutoStart`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bAutoStart
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgGeneral.cpp
  - REST: None
  - Notes: None

- **`AutoTakeED2KLinks`**
  - Type: bool
  - Access: read, write
  - Owner/API: AutoTakeED2KLinks, autotakeed2klinks
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`BeepOnError`**
  - Type: bool
  - Access: read, write
  - Owner/API: beepOnError
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`BindAddr`**
  - Type: string
  - Access: read, write
  - Owner/API: GetBindAddr, GetConfiguredBindAddr
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: None
  - Notes: None

- **`BindInterface`**
  - Type: string
  - Access: read, write
  - Owner/API: GetBindInterface
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: None
  - Notes: None

- **`VpnGuardMode`**
  - Type: string
  - Access: read, write
  - Owner/API: GetVpnGuardMode, SetVpnGuardMode
  - Default and normalization: Defaults to `Off`; recognized values are
    `Off` and `Block`
  - UI: PPgConnection.cpp
  - REST: Status/snapshot diagnostics expose the current mode under
    `network.vpnGuard.mode`
  - Notes: `Block` enables the app-level VPN Guard for named-interface P2P
    profiles. The guard blocks public P2P startup unless the selected
    interface is usable and runtime monitoring is armed.

- **`VpnGuardAllowedPublicIpCidrs`**
  - Type: string
  - Access: read, write
  - Owner/API: GetVpnGuardAllowedPublicIpCidrs, SetVpnGuardAllowedPublicIpCidrs
  - Default and normalization: Empty string; comma, semicolon, whitespace, and
    newline separated public IPv4 CIDRs are accepted
  - UI: PPgConnection.cpp
  - REST: Status/snapshot diagnostics expose the configured value under
    `network.vpnGuard.allowedPublicIpCidrs`
  - Notes: Optional additive public-exit check for VPN Guard. When empty,
    VPN Guard enforces only the selected bind interface. When non-empty, a
    bound public IPv4 probe must return an address in the allow-list before
    public P2P startup is allowed.

- **`BlockNetworkWhenBindUnavailableAtStartup`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bBlockNetworkWhenBindUnavailableAtStartup
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: None
  - Notes: Retired compatibility key. Current guarded startup behavior is
    controlled by `VpnGuardMode=Block`.

- **`CaptureFullCrashDump`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetCaptureFullCrashDump, SetCaptureFullCrashDump
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`CheckFileOpen`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetCheckFileOpen, m_bCheckFileOpen
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`CommentFilter`**
  - Type: string
  - Access: read, write
  - Owner/API: commentFilter
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgMessages.cpp
  - REST: None
  - Notes: None

- **`CommitFiles`**
  - Type: integer
  - Access: read, write
  - Owner/API: m_iCommitFiles
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ConditionalTCPAccept`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetConditionalTCPAccept, m_bConditionalTCPAccept
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ConfirmExit`**
  - Type: bool
  - Access: read, write
  - Owner/API: confirmExit
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgGeneral.cpp
  - REST: None
  - Notes: None

- **`CryptLayerRequested`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bCryptLayerRequested
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`CryptLayerRequired`**
  - Type: bool
  - Access: read, write
  - Owner/API: IsCryptLayerRequired, m_bCryptLayerRequired
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`CryptLayerSupported`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bCryptLayerSupported
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`DailyConfigBackup`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetDailyConfigBackup, SetDailyConfigBackup
  - Default and normalization: Defaults to enabled
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: Daily configuration backup switch.

- **`DateTimeFormat`**
  - Type: string
  - Access: read, write
  - Owner/API: GetDateTimeFormat, m_strDateTimeFormat
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`DateTimeFormat4Lists`**
  - Type: string
  - Access: read, write
  - Owner/API: GetDateTimeFormat4Lists, m_strDateTimeFormat4Lists
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`DateTimeFormat4Log`**
  - Type: string
  - Access: read, write
  - Owner/API: GetDateTimeFormat4Log, m_strDateTimeFormat4Log
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`DebugSourceExchange`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bDebugSourceExchange
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`DetectTCPErrorFlooder`**
  - Type: bool
  - Access: read, write
  - Owner/API: IsDetectTCPErrorFlooder, m_bDetectTCPErrorFlooder
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`DisableKnownClientList`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bDisableKnownClientList
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`DisableQueueList`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bDisableQueueList
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`Ed2kSearchMaxMoreRequests`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetEd2kSearchMaxMoreRequests, SetEd2kSearchMaxMoreRequests
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`Ed2kSearchMaxResults`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetEd2kSearchMaxResults, SetEd2kSearchMaxResults
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ExitOnBindInterfaceLoss`**
  - Type: bool
  - Access: read, write
  - Owner/API: IsExitOnBindInterfaceLossEnabled, SetExitOnBindInterfaceLossEnabled
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: None
  - Notes: Retired compatibility key. Current runtime bind-loss exit behavior
    is controlled by `VpnGuardMode=Block`.

- **`ExtractMetaData`**
  - Type: integer
  - Access: read, write
  - Owner/API: m_iExtractMetaData
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ExtraPreviewWithMenu`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetExtraPreviewWithMenu, m_bExtraPreviewWithMenu
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`FileBufferSize`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetFileBufferSize, SetFileBufferSize
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`FileBufferTimeLimit`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetFileBufferTimeLimit
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`FilenameCleanups`**
  - Type: string
  - Access: read, write
  - Owner/API: GetFilenameCleanups, SetFilenameCleanups
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`FilterLevel`**
  - Type: integer
  - Access: read, write
  - Owner/API: filterlevel
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`FollowMajorityFilenameForNewDownloads`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetFollowMajorityFilenameForNewDownloads,
               SetFollowMajorityFilenameForNewDownloads
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`FollowMajorityFilenameMinimumVotes`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetFollowMajorityFilenameMinimumVotes,
               SetFollowMajorityFilenameMinimumVotes
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`FollowMajorityFilenameRequiredPercent`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetFollowMajorityFilenameRequiredPercent,
               SetFollowMajorityFilenameRequiredPercent
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ForceSpeedsToKB`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetForceSpeedsToKB, m_bForceSpeedsToKB
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`FullVerbose`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bFullVerbose
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`HighresTimer`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetHighresTimer, m_bHighresTimer
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ICH`**
  - Type: bool
  - Access: read, write
  - Owner/API: ICH
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`IconflashOnNewMessage`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bIconflashOnNewMessage
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`IncomingDir`**
  - Type: string
  - Access: read, write
  - Owner/API: m_strIncomingDir
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDirectories.cpp
  - REST: None
  - Notes: None

- **`IndicateRatings`**
  - Type: bool
  - Access: read, write
  - Owner/API: indicateratings
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgMessages.cpp
  - REST: None
  - Notes: None

- **`InspectAllFileTypes`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetInspectAllFileTypes, m_bInspectAllFileTypes
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`IPFilterEnabled`**
  - Type: bool
  - Access: read, write
  - Owner/API: IsIPFilterEnabled, SetIPFilterEnabled
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`IPFilterUpdatePeriodDays`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetIPFilterUpdatePeriodDays, SetIPFilterUpdatePeriodDays
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`IPFilterUpdateUrl`**
  - Type: string
  - Access: read, write
  - Owner/API: GetIPFilterUpdateUrl, SetIPFilterUpdateUrl
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`IRCAddTimestamp`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCAddTimeStamp, m_bIRCAddTimeStamp
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCAllowEmuleAddFriend`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCAllowEmuleAddFriend, m_bIRCAllowEmuleAddFriend
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCEnableSmileys`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCEnableSmileys, m_bIRCEnableSmileys
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCEnableUTF8`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCEnableUTF8, m_bIRCEnableUTF8
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCIgnoreEmuleAddFriendMsgs`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCIgnoreEmuleAddFriendMsgs, m_bIRCIgnoreEmuleAddFriendMsgs
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCIgnoreEmuleSendLinkMsgs`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCIgnoreEmuleSendLinkMsgs, m_bIRCIgnoreEmuleSendLinkMsgs
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCIgnoreJoinMessages`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCIgnoreJoinMessages, m_bIRCIgnoreJoinMessages
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCIgnoreMiscMessages`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCIgnoreMiscMessages, m_bIRCIgnoreMiscMessages
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCIgnorePartMessages`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCIgnorePartMessages, m_bIRCIgnorePartMessages
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCIgnorePingPongMessages`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCIgnorePingPongMessages, m_bIRCIgnorePingPongMessages
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCIgnoreQuitMessages`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetIRCIgnoreQuitMessages, m_bIRCIgnoreQuitMessages
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCNick`**
  - Type: string
  - Access: read, write
  - Owner/API: m_strIRCNick
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCPerformString`**
  - Type: string
  - Access: read, write
  - Owner/API: m_strIRCPerformString
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`IRCUsePerform`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bIRCUsePerform
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgIRC.cpp
  - REST: None
  - Notes: None

- **`KadFileSearchTotal`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetKadFileSearchTotal, SetKadFileSearchTotal
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`KadKeywordSearchTotal`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetKadKeywordSearchTotal, SetKadKeywordSearchTotal
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`KeepUnavailableFixedSharedDirs`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bKeepUnavailableFixedSharedDirs
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`Language`**
  - Type: integer
  - Access: read, write
  - Owner/API: SetLanguage
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgGeneral.cpp
  - REST: None
  - Notes: None

- **`LogA4AF`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bLogA4AF
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`LogBannedClients`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bLogBannedClients
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`LogFileFormat`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetLogFileFormat, m_iLogFileFormat
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`LogFileSaving`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bLogFileSaving
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`LogFilteredIPs`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bLogFilteredIPs
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`LogRatingDescReceived`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bLogRatingDescReceived
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`LogSecureIdent`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bLogSecureIdent
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`LogUlDlEvents`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bLogUlDlEvents
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`MaxChatHistoryLines`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMaxChatHistoryLines
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`MaxHalfConnections`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMaxHalfConnections, SetMaxHalfConnections
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`MaxLogBuff`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMaxLogBuff
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`MaxLogFileSize`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMaxLogFileSize
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`MessageEnableSmileys`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetMessageEnableSmileys, m_bMessageEnableSmileys
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgMessages.cpp
  - REST: None
  - Notes: None

- **`MessageFilter`**
  - Type: string
  - Access: read, write
  - Owner/API: messageFilter
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgMessages.cpp
  - REST: None
  - Notes: None

- **`MinFreeDiskSpaceConfig`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMinFreeDiskSpaceConfig
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`MinFreeDiskSpaceIncoming`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMinFreeDiskSpaceIncoming
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`MinFreeDiskSpaceTemp`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMinFreeDiskSpaceTemp
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`MiniMule`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bEnableMiniMule
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgGeneral.cpp
  - REST: None
  - Notes: Native MiniMule enable switch.

- **`MinToTray`**
  - Type: bool
  - Access: read, write
  - Owner/API: mintotray
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`NotifierDisplayMode`**
  - Type: integer
  - Access: read, write
  - Owner/API: notifierDisplayMode
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgNotify.cpp
  - REST: None
  - Notes: None

- **`PartiallyPurgeOldKnownFiles`**
  - Type: bool
  - Access: read, write
  - Owner/API: DoPartiallyPurgeOldKnownFiles, m_bPartiallyPurgeOldKnownFiles
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`Port`**
  - Type: integer
  - Access: read, write
  - Owner/API: port
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: None
  - Notes: None

- **`PreventStandby`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetPreventStandby, m_bPreventStandby
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgGeneral.cpp
  - REST: None
  - Notes: None

- **`PreviewCopiedArchives`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetPreviewCopiedArchives, m_bPreviewCopiedArchives
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`PreviewOnIconDblClk`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetPreviewOnIconDblClk, m_bPreviewOnIconDblClk
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`PreviewPrio`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bpreviewprio
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`PreviewSmallBlocks`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetPreviewSmallBlocks, m_iPreviewSmallBlocks
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`RearrangeKadSearchKeywords`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetRearrangeKadSearchKeywords, m_bRearrangeKadSearchKeywords
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ReBarToolbar`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetReBarToolbar, m_bReBarToolbar
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`Reconnect`**
  - Type: bool
  - Access: read, write
  - Owner/API: reconnect
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: None
  - Notes: None

- **`RememberCancelledFiles`**
  - Type: bool
  - Access: read, write
  - Owner/API: SetRememberCancelledFiles
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`RememberDownloadedFiles`**
  - Type: bool
  - Access: read, write
  - Owner/API: SetRememberDownloadedFiles
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`RestoreLastLogPane`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetRestoreLastLogPane, m_bRestoreLastLogPane
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`RestoreLastMainWndDlg`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetRestoreLastMainWndDlg, m_bRestoreLastMainWndDlg
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`RTLWindowsLayout`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetRTLWindowsLayout, m_bRTLWindowsLayout
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgGeneral.cpp
  - REST: None
  - Notes: None

- **`ServerKeepAliveTimeout`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetServerKeepAliveTimeout
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ShutdownProgressDialog`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetShutdownProgressDialogMode, SetShutdownProgressDialogMode
  - Default and normalization: `NormalizeLifecycleProgressDialogMode`; default always
                               shown
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: Shutdown progress dialog visibility mode.

- **`ShowActiveDownloadsBold`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetShowActiveDownloadsBold, m_bShowActiveDownloadsBold
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ShowCopyEd2kLinkCmd`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetShowCopyEd2kLinkCmd, m_bShowCopyEd2kLinkCmd
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ShowDwlPercentage`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetUseDwlPercentage, m_bShowDwlPercentage
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`ShowOverhead`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bshowoverhead
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: None
  - Notes: None

- **`ShowRatesOnTitle`**
  - Type: bool
  - Access: read, write
  - Owner/API: ShowRatesOnTitle
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`ShowUpDownIconInTaskbar`**
  - Type: bool
  - Access: read, write
  - Owner/API: IsShowUpDownIconInTaskbar, m_bShowUpDownIconInTaskbar
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ShowVerticalHourMarkers`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bShowVerticalHourMarkers
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ShowWin7TaskbarGoodies`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bShowWin7TaskbarGoodies
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`SparsePartFiles`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetSparsePartFiles, m_bSparsePartFiles
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`StartNextFile`**
  - Type: integer
  - Access: read, write
  - Owner/API: m_istartnextfile
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`StartupProgressDialog`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetStartupProgressDialogMode, SetStartupProgressDialogMode
  - Default and normalization: `NormalizeLifecycleProgressDialogMode`; default always
                               shown
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: Startup progress dialog visibility mode.

- **`StatsAverageMinutes`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetStatsAverageMinutes, SetStatsAverageMinutes
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgStats.cpp
  - REST: None
  - Notes: None

- **`StatsInterval`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetStatsInterval, SetStatsInterval
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgStats.cpp
  - REST: None
  - Notes: None

- **`StoreSearches`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bStoreSearches
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`TCPErrorFlooderIntervalMinutes`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetTCPErrorFlooderIntervalMinutes, m_uTCPErrorFlooderIntervalMinutes
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`TCPErrorFlooderThreshold`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetTCPErrorFlooderThreshold, m_uTCPErrorFlooderThreshold
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`TempDir`**
  - Type: string
  - Access: read, write
  - Owner/API: GetTempDir, tempdir
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDirectories.cpp
  - REST: None
  - Notes: None

- **`ToolTipDelay`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetToolTipDelay, SetToolTipDelay
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`TransferDoubleClick`**
  - Type: bool
  - Access: read, write
  - Owner/API: transferDoubleclick
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`TxtEditor`**
  - Type: string
  - Access: read, write
  - Owner/API: GetTxtEditor, m_strTxtEditor
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgSecurity.cpp, PPgServer.cpp, PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`UDPPort`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetUDPPort, udpport
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: None
  - Notes: None

- **`UseAutocompletion`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetUseAutocompletion, m_bUseAutocompl
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp, PPgSecurity.cpp
  - REST: None
  - Notes: None

- **`Verbose`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bVerbose
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`VideoPlayer`**
  - Type: string
  - Access: read, write
  - Owner/API: m_strVideoPlayer
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`VideoPlayerArgs`**
  - Type: string
  - Access: read, write
  - Owner/API: m_strVideoPlayerArgs
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`VideoThumbnailFfmpegPath`**
  - Type: string
  - Access: read, write
  - Owner/API: m_strVideoThumbnailFfmpegPath
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`VideoThumbnailIntervalSeconds`**
  - Type: integer
  - Access: read, write
  - Owner/API: m_uVideoThumbnailIntervalSeconds
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`WinaTransToolbar`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bWinaTransToolbar
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgDisplay.cpp
  - REST: None
  - Notes: None

- **`YourHostname`**
  - Type: string
  - Access: read, write
  - Owner/API: GetYourHostname, SetYourHostname
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

#### editable-ui-rest

- **`AutoBroadbandIO`**
  - Type: bool
  - Access: read, write
  - Owner/API: IsAutoBroadbandIOEnabled, SetAutoBroadbandIOEnabled
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: autoBroadbandIo
  - Notes: Enabled behavior derives a global download-buffer budget from
           currently available physical RAM, clamps it between 512 MiB and
           4 GiB, and distributes it by active download demand.

- **`Autoconnect`**
  - Type: bool
  - Access: read, write
  - Owner/API: autoconnect
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: autoConnect
  - Notes: None

- **`MaxConnections`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMaxConnections, SetMaxConnections, maxconnections
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp, PPgStats.cpp
  - REST: maxConnections
  - Notes: None

- **`MaxConnectionsPerFiveSeconds`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMaxConperFive, SetMaxConsPerFive
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: maxConnectionsPerFiveSeconds
  - Notes: None

- **`MaxDownload`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetConfiguredMaxDownload, SetMaxDownload
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: downloadLimitKiBps
  - Notes: None

- **`MaxSourcesPerFile`**
  - Type: integer
  - Access: read, write
  - Owner/API: SetMaxSourcesPerFile
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: maxSourcesPerFile
  - Notes: None

- **`MaxUpload`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetConfiguredMaxUpload, SetMaxUpload
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: uploadLimitKiBps
  - Notes: None

- **`NetworkED2K`**
  - Type: bool
  - Access: read, write
  - Owner/API: SetNetworkED2K, networked2k
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: networkEd2k
  - Notes: None

- **`NetworkKademlia`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetNetworkKademlia, SetNetworkKademlia, networkkademlia
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgConnection.cpp
  - REST: networkKademlia
  - Notes: None

- **`QueueSize`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetQueueSize, SetQueueSize
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: queueSize
  - Notes: None

- **`SafeServerConnect`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bSafeServerConnect
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgServer.cpp
  - REST: safeServerConnect
  - Notes: None

- **`UseCreditSystem`**
  - Type: bool
  - Access: read, write
  - Owner/API: m_bCreditSystem
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: creditSystem
  - Notes: None

#### persisted-runtime

- **`AddServersFromClient`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`AllocateFullFile`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`AllowLocalHostIP`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`AppVersion`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`AutoArchivePreviewStart`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`AutoConnectStaticOnly`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`AutoShowLookups`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`BBPreferenceSchema`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`BringToFront`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`Check4NewVersionDelay`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: Startup interval for the current GitHub Releases update check, not the
           removed legacy stock eMule update checker.

- **`CreateCrashDump`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`CryptTCPPaddingLength`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DeadServerRetry`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DesktopUiRefreshIntervalMs`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: `NormalizeDesktopUiRefreshIntervalMs`; default `2000`;
                               valid values `0`, `500`, `1000`, `2000`, `5000`, `10000`;
                               `0` pauses transfer/client list refreshes
  - UI: Tools menu
  - REST: None
  - Notes: Native desktop transfer/client list refresh interval. Title, tray,
           status, MiniMule, and visible transfer-list presentation share this
           desktop presentation timer. When set to `0`, routine presentation is
           paused and the title speed remains on a 10-second cadence.

- **`DebugClientKadUDP`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugClientTCP`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugClientUDP`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugHeap`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugLogLevel`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugSearchResultDetailLevel`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugServerSearches`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugServerSources`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugServerTCP`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DebugServerUDP`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DefaultIRCServerNew`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DisableFirstTimeWizard`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`DontRecreateStatGraphsOnResize`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`EnableScheduler`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`EnableSearchResultSpamFilter`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`FilterBadIPs`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`FilterServersByIP`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`FullChunkTransfers`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`GeoLocationLastUpdateTime`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`GeoLocationLookupEnabled`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`GeoLocationUpdatePeriodDays`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`GeoLocationUpdateUrl`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`HyperTextFont`**
  - Type: binary
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IPFilterLastUpdateTime`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IPFilterUpdateEnabled`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IRCAcceptLink`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IRCAcceptLinkFriends`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IRCFilterName`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IRCFilterUser`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IRCHelpChannel`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IRCListOnConnect`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IRCSoundEvents`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`IRCUseFilter`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`KadFileSearchLifetime`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`KadKeywordSearchLifetime`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`KadUDPKey`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`LastLogPaneID`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`LastMainWndDlgID`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`LogTextFont`**
  - Type: binary
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`LostFromCorruption`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ManualHighPrio`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`MaxMessageSessions`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`MediaInfo_MediaInfoDllPath`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: Optional MediaInfo.dll lookup path. The `<noload>` token intentionally
           disables the optional DLL while keeping built-in metadata fallbacks.

- **`MessageFromValidSourcesOnly`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`MessagesFromFriendsOnly`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`MessageUseCaptchas`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`MinToTray_Aero`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`Nick`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierConfiguration`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierMailAuth`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierMailLogin`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierMailPassword`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierMailPort`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierMailRecipient`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierMailSender`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierMailServer`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierMailTLS`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierPopEveryChatMessage`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierPopNewVersion`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierSendMail`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierSoundPath`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifierUseSound`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifyOnChat`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifyOnDownload`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifyOnImportantError`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifyOnLog`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`NotifyOnNewDownload`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`OnlineSignature`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`PartsSavedByICH`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`RandomizePortsOnStartup`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`RemoveFilesToBin`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SaveDebugToDisk`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SavedFromCompression`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SaveLogToDisk`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`Scoresystem`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SearchMethod`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SearchResultsFileSizeFormat`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: SetSearchResultsFileSizeFormat
  - UI: None
  - REST: None
  - Notes: Search results file-size display mode: default, KiB, or MiB.

- **`SecureIdent`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SeeShare`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`Serverlist`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ServerUDPPort`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ShowDownloadToolbar`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ShowInfoOnCatTabs`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ShowSharedFilesDetails`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SkinProfile`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SkinProfileDir`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SmartIdCheck`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SplitterbarPosition`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SplitterbarPositionFriend`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SplitterbarPositionIRC`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SplitterbarPositionServer`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SplitterbarPositionShared`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SplitterbarPositionStat`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SplitterbarPositionStat_HL`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`SplitterbarPositionStat_HR`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`StartupMinimized`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`StatGraphsInterval`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`StatsFillGraphs`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`StraightWindowStyles`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`TempDirs`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ToolbarBitmap`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ToolbarBitmapFolder`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ToolbarIconSize`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ToolbarLabels`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`ToolbarSetting`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`TransferWnd1`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`TransferWnd2`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`TransflstRemainOrder`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`UserSortedServerList`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`UseSimpleTimeRemainingComputation`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`UseSystemFontForMainControls`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`VariousStatisticsMaxValue`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`VerboseOptions`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`VersionCheckLastAutomatic`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: Last automatic GitHub Releases update-check time; separate from legacy
           stock eMule update infrastructure.

- **`WatchClipboard4ED2kFilelinks`**
  - Type: bool
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`WebMirrorAlertLevel`**
  - Type: integer
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

- **`WebTemplateFile`**
  - Type: string
  - Access: read, write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: None

#### read-only-legacy

- **`LogErrorColor`**
  - Type: color
  - Access: read
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: Legacy/customization key is accepted on load; current Preferences.cpp has no
           matching writer.

- **`LogSuccessColor`**
  - Type: color
  - Access: read
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: Legacy/customization key is accepted on load; current Preferences.cpp has no
           matching writer.

- **`LogWarningColor`**
  - Type: color
  - Access: read
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: Legacy/customization key is accepted on load; current Preferences.cpp has no
           matching writer.

### `eMule`

#### editable-ui

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `ShowVerticalHourMarkers` | bool | read, write | m_bShowVerticalHourMarkers | Not explicitly declared in schema | PPgTweaks.cpp | None | None |

### `FileCompletion`

#### editable-ui

- **`FileCompletionArguments`**
  - Type: string
  - Access: read, write
  - Owner/API: GetFileCompletionArguments, m_strFileCompletionArguments
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: Supports `%F`, `%D`, `%N`, `%H`, `%S`, and `%C`; `%F` and `%D` are
           quoted automatically and environment variables are not expanded.

- **`FileCompletionProgram`**
  - Type: string
  - Access: read, write
  - Owner/API: GetFileCompletionProgram, m_strFileCompletionProgram
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

- **`RunCommandOnFileCompletion`**
  - Type: bool
  - Access: read, write
  - Owner/API: GetRunCommandOnFileCompletion, m_bRunCommandOnFileCompletion
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgFiles.cpp
  - REST: None
  - Notes: None

### `ListControlSetup`

#### dynamic-family

- **`<dynamic:di>`**
  - Type: string
  - Access: write
  - Owner/API: None
  - Default and normalization: Not explicitly declared in schema
  - UI: None
  - REST: None
  - Notes: Dynamic family generated at runtime; source expression is guarded instead of
           enumerating every concrete key.

### `Proxy`

#### persisted-runtime

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `ProxyEnablePassword` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `ProxyEnableProxy` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `ProxyName` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `ProxyPassword` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `ProxyPort` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `ProxyType` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `ProxyUser` | string | read, write | None | Not explicitly declared in schema | None | None | None |

### `UploadPolicy`

#### editable-ui

- **`LowRatioBoostEnabled`**
  - Type: bool
  - Access: read, write
  - Owner/API: IsLowRatioBoostEnabled, SetLowRatioBoostEnabled
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`LowRatioThreshold`**
  - Type: number
  - Access: read, write
  - Owner/API: GetLowRatioThreshold, SetLowRatioThreshold
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`SessionTimeLimitSeconds`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetSessionTimeLimitSeconds, SetSessionTimeLimitSeconds
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`SessionTransferLimitMode`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetSessionTransferLimitMode, SetSessionTransferLimitMode
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`SessionTransferLimitValue`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetSessionTransferLimitValue, SetSessionTransferLimitValue
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`SlowUploadCooldownSeconds`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetSlowUploadCooldownSeconds, SetSlowUploadCooldownSeconds
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`SlowUploadGraceSeconds`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetSlowUploadGraceSeconds, SetSlowUploadGraceSeconds
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`SlowUploadThresholdFactor`**
  - Type: number
  - Access: read, write
  - Owner/API: GetSlowUploadThresholdFactor, SetSlowUploadThresholdFactor
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`SlowUploadWarmupSeconds`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetSlowUploadWarmupSeconds, SetSlowUploadWarmupSeconds
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

- **`ZeroUploadRateGraceSeconds`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetZeroUploadRateGraceSeconds, SetZeroUploadRateGraceSeconds
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: None
  - Notes: None

#### editable-ui-rest

- **`MaxUploadClientsAllowed`**
  - Type: integer
  - Access: read, write
  - Owner/API: GetMaxUploadClientsAllowed, SetMaxUploadClientsAllowed
  - Default and normalization: Not explicitly declared in schema
  - UI: PPgTweaks.cpp
  - REST: maxUploadSlots, uploadClientDataRate
  - Notes: None

#### persisted-runtime

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `LowIDScoreDivisor` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `LowRatioScoreBonus` | integer | read, write | None | Not explicitly declared in schema | None | None | None |

### `UPnP`

#### editable-ui

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `CloseUPnPOnExit` | bool | read, write | CloseUPnPOnExit, m_bCloseUPnPOnExit | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `EnableUPnP` | bool | read, write | m_bEnableUPnP | Not explicitly declared in schema | PPgConnection.cpp | None | None |

#### persisted-runtime

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `BackendMode` | integer | read, write | None | Not explicitly declared in schema | None | None | None |

### `WebServer`

#### editable-ui

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `AllowAdminHiLevelFunc` | bool | read, write | GetWebAdminAllowedHiLevFunc | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `ApiKey` | string | read, write | GetWSApiKey, SetWSApiKey | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `BindAddr` | string | read, write | GetWebBindAddr, SetWebBindAddr | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `HTTPSCertificate` | string | read, write | GetWebCertPath, SetWebCertPath | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `HTTPSKey` | string | read, write | GetWebKeyPath, SetWebKeyPath | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `MaxFileUploadSizeMB` | integer | read, write | GetMaxWebUploadFileSizeMB, SetMaxWebUploadFileSizeMB | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `Password` | string | read, write | SetWSPass | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `PasswordLow` | string | read, write | SetWSLowPass | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `Port` | integer | read, write | GetWSPort, SetWSPort | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `UseGzip` | bool | read, write | GetWebUseGzip, SetWebUseGzip | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `UseHTTPS` | bool | read, write | GetWebUseHttps, SetWebUseHttps | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `WebTimeoutMins` | integer | read, write | GetWebTimeoutMins, SetWebTimeoutMins | Not explicitly declared in schema | PPgWebServer.cpp | None | None |
| `WebUseUPnP` | bool | read, write | GetWSUseUPnP, m_bWebUseUPnP | Not explicitly declared in schema | PPgWebServer.cpp | None | None |

#### persisted-runtime

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `AllowedIPs` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `Enabled` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `EnableDiagnosticRestEndpoints` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `EnableLegacyWebUi` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `PageRefreshTime` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `UseLowRightsUser` | bool | read, write | None | Not explicitly declared in schema | None | None | None |

## Troubleshooting

When a setting does not behave as expected:

1. Check the classification in the complete reference.
2. Check whether the value is UI-bound, REST-bound, hidden, dynamic, or state.
3. Check the behavior sections above for the important default/range behavior.
4. Restart or reconnect if the setting controls startup, sockets, binding, or
   listener state.
5. Use diagnostics before deleting profile files or resetting the whole config.
