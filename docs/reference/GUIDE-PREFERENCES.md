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
- BB-owned sections are used only where they make behavior clearer without
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
- `MiniMule`, `AICHTrustEveryHash`
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

Total `preferences.ini` schema entries: **335**.

Dynamic rows are generated families tracked by source expression rather
than a finite static key list. Empty defaults or normalizers mean the
schema did not declare a single explicit value; check the behavior sections
above for user-facing defaults and ranges.

### `<default>`

#### disabled-tombstone

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `VideoPreviewThumbnails` | bool | write | m_bVideoPreviewThumbnails | Not explicitly declared in schema | PPgFiles.cpp | None | Written as false for compatibility while runtime loading forces thumbnails disabled. |
| `AllowPeerPreview` | bool | read, write | m_bAllowPeerPreview | Not explicitly declared in schema | PPgFiles.cpp | None | Explicit opt-in for advertising and serving peer preview frames from shared video files. Requires visible shares and a valid FFmpeg executable. |

#### dynamic-family

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `<dynamic:si>` | string | read | None | Not explicitly declared in schema | None | None | Dynamic family generated at runtime; source expression is guarded instead of enumerating every concrete key. |

#### editable-rest

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `DAPPref` | bool | read, write | None | Not explicitly declared in schema | None | newAutoDown | None |
| `UAPPref` | bool | read, write | None | Not explicitly declared in schema | None | newAutoUp | None |

#### editable-ui

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `3DDepth` | integer | read, write | Get3DDepth | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `A4AFSaveCpu` | bool | read, write | GetA4AFSaveCpu, m_bA4AFSaveCpu | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `AddNewFilesPaused` | bool | read, write | addnewfilespaused | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `AddServersFromServer` | bool | read, write | m_bAddServersFromServer | Not explicitly declared in schema | PPgServer.cpp | None | None |
| `AdvancedSpamFilter` | bool | read, write | m_bAdvancedSpamfilter | Not explicitly declared in schema | PPgMessages.cpp | None | None |
| `AlwaysShowTrayIcon` | bool | read, write | IsAlwaysShowTrayIcon, m_bAlwaysShowTrayIcon | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `AutoClearCompleted` | bool | read, write | GetRemoveFinishedDownloads, m_bRemoveFinishedDownloads | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `AutoFilenameCleanup` | bool | read, write | AutoFilenameCleanup, autofilenamecleanup | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `AutoStart` | bool | read, write | m_bAutoStart | Not explicitly declared in schema | PPgGeneral.cpp | None | None |
| `AutoTakeED2KLinks` | bool | read, write | AutoTakeED2KLinks, autotakeed2klinks | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `BeepOnError` | bool | read, write | beepOnError | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `BindAddr` | string | read, write | GetBindAddr, GetConfiguredBindAddr | Not explicitly declared in schema | PPgConnection.cpp | None | None |
| `BindInterface` | string | read, write | GetBindInterface | Not explicitly declared in schema | PPgConnection.cpp | None | None |
| `BlockNetworkWhenBindUnavailableAtStartup` | bool | read, write | m_bBlockNetworkWhenBindUnavailableAtStartup | Not explicitly declared in schema | PPgConnection.cpp | None | None |
| `CheckFileOpen` | bool | read, write | GetCheckFileOpen, m_bCheckFileOpen | Not explicitly declared in schema | PPgSecurity.cpp | None | None |
| `CommentFilter` | string | read, write | commentFilter | Not explicitly declared in schema | PPgMessages.cpp | None | None |
| `CommitFiles` | integer | read, write | m_iCommitFiles | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ConditionalTCPAccept` | bool | read, write | GetConditionalTCPAccept, m_bConditionalTCPAccept | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ConfirmExit` | bool | read, write | confirmExit | Not explicitly declared in schema | PPgGeneral.cpp | None | None |
| `CryptLayerRequested` | bool | read, write | m_bCryptLayerRequested | Not explicitly declared in schema | PPgSecurity.cpp | None | None |
| `CryptLayerRequired` | bool | read, write | IsCryptLayerRequired, m_bCryptLayerRequired | Not explicitly declared in schema | PPgSecurity.cpp | None | None |
| `CryptLayerSupported` | bool | read, write | m_bCryptLayerSupported | Not explicitly declared in schema | PPgSecurity.cpp | None | None |
| `DailyConfigBackup` | bool | read, write | GetDailyConfigBackup, SetDailyConfigBackup | Defaults to enabled | PPgTweaks.cpp | None | Daily configuration backup switch. |
| `DateTimeFormat` | string | read, write | GetDateTimeFormat, m_strDateTimeFormat | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `DateTimeFormat4Lists` | string | read, write | GetDateTimeFormat4Lists, m_strDateTimeFormat4Lists | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `DateTimeFormat4Log` | string | read, write | GetDateTimeFormat4Log, m_strDateTimeFormat4Log | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `DebugSourceExchange` | bool | read, write | m_bDebugSourceExchange | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `DetectTCPErrorFlooder` | bool | read, write | IsDetectTCPErrorFlooder, m_bDetectTCPErrorFlooder | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `DisableKnownClientList` | bool | read, write | m_bDisableKnownClientList | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `DisableQueueList` | bool | read, write | m_bDisableQueueList | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `Ed2kSearchMaxMoreRequests` | integer | read, write | GetEd2kSearchMaxMoreRequests, SetEd2kSearchMaxMoreRequests | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `Ed2kSearchMaxResults` | integer | read, write | GetEd2kSearchMaxResults, SetEd2kSearchMaxResults | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ExitOnBindInterfaceLoss` | bool | read, write | IsExitOnBindInterfaceLossEnabled, SetExitOnBindInterfaceLossEnabled | Not explicitly declared in schema | PPgConnection.cpp | None | None |
| `ExtractMetaData` | integer | read, write | m_iExtractMetaData | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ExtraPreviewWithMenu` | bool | read, write | GetExtraPreviewWithMenu, m_bExtraPreviewWithMenu | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `FileBufferSize` | integer | read, write | GetFileBufferSize, SetFileBufferSize | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `FileBufferTimeLimit` | integer | read, write | GetFileBufferTimeLimit | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `FilenameCleanups` | string | read, write | GetFilenameCleanups, SetFilenameCleanups | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `FilterLevel` | integer | read, write | filterlevel | Not explicitly declared in schema | PPgSecurity.cpp | None | None |
| `FollowMajorityFilenameForNewDownloads` | bool | read, write | GetFollowMajorityFilenameForNewDownloads, SetFollowMajorityFilenameForNewDownloads | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `FollowMajorityFilenameMinimumVotes` | integer | read, write | GetFollowMajorityFilenameMinimumVotes, SetFollowMajorityFilenameMinimumVotes | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `FollowMajorityFilenameRequiredPercent` | integer | read, write | GetFollowMajorityFilenameRequiredPercent, SetFollowMajorityFilenameRequiredPercent | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ForceSpeedsToKB` | bool | read, write | GetForceSpeedsToKB, m_bForceSpeedsToKB | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `FullVerbose` | bool | read, write | m_bFullVerbose | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `HighresTimer` | bool | read, write | GetHighresTimer, m_bHighresTimer | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ICH` | bool | read, write | ICH | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `IconflashOnNewMessage` | bool | read, write | m_bIconflashOnNewMessage | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `IncomingDir` | string | read, write | m_strIncomingDir | Not explicitly declared in schema | PPgDirectories.cpp | None | None |
| `IndicateRatings` | bool | read, write | indicateratings | Not explicitly declared in schema | PPgMessages.cpp | None | None |
| `InspectAllFileTypes` | bool | read, write | GetInspectAllFileTypes, m_bInspectAllFileTypes | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `IPFilterEnabled` | bool | read, write | IsIPFilterEnabled, SetIPFilterEnabled | Not explicitly declared in schema | PPgSecurity.cpp | None | None |
| `IPFilterUpdatePeriodDays` | integer | read, write | GetIPFilterUpdatePeriodDays, SetIPFilterUpdatePeriodDays | Not explicitly declared in schema | PPgSecurity.cpp | None | None |
| `IPFilterUpdateUrl` | string | read, write | GetIPFilterUpdateUrl, SetIPFilterUpdateUrl | Not explicitly declared in schema | PPgSecurity.cpp | None | None |
| `IRCAddTimestamp` | bool | read, write | GetIRCAddTimeStamp, m_bIRCAddTimeStamp | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCAllowEmuleAddFriend` | bool | read, write | GetIRCAllowEmuleAddFriend, m_bIRCAllowEmuleAddFriend | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCEnableSmileys` | bool | read, write | GetIRCEnableSmileys, m_bIRCEnableSmileys | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCEnableUTF8` | bool | read, write | GetIRCEnableUTF8, m_bIRCEnableUTF8 | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCIgnoreEmuleAddFriendMsgs` | bool | read, write | GetIRCIgnoreEmuleAddFriendMsgs, m_bIRCIgnoreEmuleAddFriendMsgs | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCIgnoreEmuleSendLinkMsgs` | bool | read, write | GetIRCIgnoreEmuleSendLinkMsgs, m_bIRCIgnoreEmuleSendLinkMsgs | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCIgnoreJoinMessages` | bool | read, write | GetIRCIgnoreJoinMessages, m_bIRCIgnoreJoinMessages | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCIgnoreMiscMessages` | bool | read, write | GetIRCIgnoreMiscMessages, m_bIRCIgnoreMiscMessages | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCIgnorePartMessages` | bool | read, write | GetIRCIgnorePartMessages, m_bIRCIgnorePartMessages | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCIgnorePingPongMessages` | bool | read, write | GetIRCIgnorePingPongMessages, m_bIRCIgnorePingPongMessages | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCIgnoreQuitMessages` | bool | read, write | GetIRCIgnoreQuitMessages, m_bIRCIgnoreQuitMessages | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCNick` | string | read, write | m_strIRCNick | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCPerformString` | string | read, write | m_strIRCPerformString | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `IRCUsePerform` | bool | read, write | m_bIRCUsePerform | Not explicitly declared in schema | PPgIRC.cpp | None | None |
| `KadFileSearchTotal` | integer | read, write | GetKadFileSearchTotal, SetKadFileSearchTotal | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `KadKeywordSearchTotal` | integer | read, write | GetKadKeywordSearchTotal, SetKadKeywordSearchTotal | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `KeepUnavailableFixedSharedDirs` | bool | read, write | m_bKeepUnavailableFixedSharedDirs | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `Language` | integer | read, write | SetLanguage | Not explicitly declared in schema | PPgGeneral.cpp | None | None |
| `LogA4AF` | bool | read, write | m_bLogA4AF | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `LogBannedClients` | bool | read, write | m_bLogBannedClients | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `LogFileFormat` | integer | read, write | GetLogFileFormat, m_iLogFileFormat | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `LogFileSaving` | bool | read, write | m_bLogFileSaving | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `LogFilteredIPs` | bool | read, write | m_bLogFilteredIPs | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `LogRatingDescReceived` | bool | read, write | m_bLogRatingDescReceived | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `LogSecureIdent` | bool | read, write | m_bLogSecureIdent | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `LogUlDlEvents` | bool | read, write | m_bLogUlDlEvents | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `MaxChatHistoryLines` | integer | read, write | GetMaxChatHistoryLines | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `MaxHalfConnections` | integer | read, write | GetMaxHalfConnections, SetMaxHalfConnections | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `MaxLogBuff` | integer | read, write | GetMaxLogBuff | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `MaxLogFileSize` | integer | read, write | GetMaxLogFileSize | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `MessageEnableSmileys` | bool | read, write | GetMessageEnableSmileys, m_bMessageEnableSmileys | Not explicitly declared in schema | PPgMessages.cpp | None | None |
| `MessageFilter` | string | read, write | messageFilter | Not explicitly declared in schema | PPgMessages.cpp | None | None |
| `MinFreeDiskSpaceConfig` | integer | read, write | GetMinFreeDiskSpaceConfig | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `MinFreeDiskSpaceIncoming` | integer | read, write | GetMinFreeDiskSpaceIncoming | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `MinFreeDiskSpaceTemp` | integer | read, write | GetMinFreeDiskSpaceTemp | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `MinToTray` | bool | read, write | mintotray | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `NotifierDisplayMode` | integer | read, write | notifierDisplayMode | Not explicitly declared in schema | PPgNotify.cpp | None | None |
| `PartiallyPurgeOldKnownFiles` | bool | read, write | DoPartiallyPurgeOldKnownFiles, m_bPartiallyPurgeOldKnownFiles | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `Port` | integer | read, write | port | Not explicitly declared in schema | PPgConnection.cpp | None | None |
| `PreventStandby` | bool | read, write | GetPreventStandby, m_bPreventStandby | Not explicitly declared in schema | PPgGeneral.cpp | None | None |
| `PreviewCopiedArchives` | bool | read, write | GetPreviewCopiedArchives, m_bPreviewCopiedArchives | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `PreviewOnIconDblClk` | bool | read, write | GetPreviewOnIconDblClk, m_bPreviewOnIconDblClk | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `PreviewPrio` | bool | read, write | m_bpreviewprio | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `PreviewSmallBlocks` | integer | read, write | GetPreviewSmallBlocks, m_iPreviewSmallBlocks | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `RearrangeKadSearchKeywords` | bool | read, write | GetRearrangeKadSearchKeywords, m_bRearrangeKadSearchKeywords | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ReBarToolbar` | bool | read, write | GetReBarToolbar, m_bReBarToolbar | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `Reconnect` | bool | read, write | reconnect | Not explicitly declared in schema | PPgConnection.cpp | None | None |
| `RememberCancelledFiles` | bool | read, write | SetRememberCancelledFiles | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `RememberDownloadedFiles` | bool | read, write | SetRememberDownloadedFiles | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `RestoreLastLogPane` | bool | read, write | GetRestoreLastLogPane, m_bRestoreLastLogPane | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `RestoreLastMainWndDlg` | bool | read, write | GetRestoreLastMainWndDlg, m_bRestoreLastMainWndDlg | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `RTLWindowsLayout` | bool | read, write | GetRTLWindowsLayout, m_bRTLWindowsLayout | Not explicitly declared in schema | PPgGeneral.cpp | None | None |
| `ServerKeepAliveTimeout` | integer | read, write | GetServerKeepAliveTimeout | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ShutdownProgressDialog` | integer | read, write | GetShutdownProgressDialogMode, SetShutdownProgressDialogMode | `NormalizeLifecycleProgressDialogMode`; default always shown | PPgTweaks.cpp | None | Shutdown progress dialog visibility mode. |
| `ShowActiveDownloadsBold` | bool | read, write | GetShowActiveDownloadsBold, m_bShowActiveDownloadsBold | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ShowCopyEd2kLinkCmd` | bool | read, write | GetShowCopyEd2kLinkCmd, m_bShowCopyEd2kLinkCmd | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ShowDwlPercentage` | bool | read, write | GetUseDwlPercentage, m_bShowDwlPercentage | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `ShowOverhead` | bool | read, write | m_bshowoverhead | Not explicitly declared in schema | PPgConnection.cpp | None | None |
| `ShowRatesOnTitle` | bool | read, write | ShowRatesOnTitle | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `ShowUpDownIconInTaskbar` | bool | read, write | IsShowUpDownIconInTaskbar, m_bShowUpDownIconInTaskbar | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ShowVerticalHourMarkers` | bool | read, write | m_bShowVerticalHourMarkers | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ShowWin7TaskbarGoodies` | bool | read, write | m_bShowWin7TaskbarGoodies | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `SparsePartFiles` | bool | read, write | GetSparsePartFiles, m_bSparsePartFiles | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `StartNextFile` | integer | read, write | m_istartnextfile | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `StartupProgressDialog` | integer | read, write | GetStartupProgressDialogMode, SetStartupProgressDialogMode | `NormalizeLifecycleProgressDialogMode`; default always shown | PPgTweaks.cpp | None | Startup progress dialog visibility mode. |
| `StatsAverageMinutes` | integer | read, write | GetStatsAverageMinutes, SetStatsAverageMinutes | Not explicitly declared in schema | PPgStats.cpp | None | None |
| `StatsInterval` | integer | read, write | GetStatsInterval, SetStatsInterval | Not explicitly declared in schema | PPgStats.cpp | None | None |
| `StoreSearches` | bool | read, write | m_bStoreSearches | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `TCPErrorFlooderIntervalMinutes` | integer | read, write | GetTCPErrorFlooderIntervalMinutes, m_uTCPErrorFlooderIntervalMinutes | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `TCPErrorFlooderThreshold` | integer | read, write | GetTCPErrorFlooderThreshold, m_uTCPErrorFlooderThreshold | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `TempDir` | string | read, write | GetTempDir, tempdir | Not explicitly declared in schema | PPgDirectories.cpp | None | None |
| `ToolTipDelay` | integer | read, write | GetToolTipDelay, SetToolTipDelay | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `TransferDoubleClick` | bool | read, write | transferDoubleclick | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `TxtEditor` | string | read, write | GetTxtEditor, m_strTxtEditor | Not explicitly declared in schema | PPgSecurity.cpp, PPgServer.cpp, PPgTweaks.cpp | None | None |
| `UDPPort` | integer | read, write | GetUDPPort, udpport | Not explicitly declared in schema | PPgConnection.cpp | None | None |
| `UseAutocompletion` | bool | read, write | GetUseAutocompletion, m_bUseAutocompl | Not explicitly declared in schema | PPgDisplay.cpp, PPgSecurity.cpp | None | None |
| `Verbose` | bool | read, write | m_bVerbose | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `VideoPlayer` | string | read, write | m_strVideoPlayer | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `VideoPlayerArgs` | string | read, write | m_strVideoPlayerArgs | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `VideoThumbnailFfmpegPath` | string | read, write | m_strVideoThumbnailFfmpegPath | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `VideoThumbnailIntervalSeconds` | integer | read, write | m_uVideoThumbnailIntervalSeconds | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `WinaTransToolbar` | bool | read, write | m_bWinaTransToolbar | Not explicitly declared in schema | PPgDisplay.cpp | None | None |
| `YourHostname` | string | read, write | GetYourHostname, SetYourHostname | Not explicitly declared in schema | PPgTweaks.cpp | None | None |

#### editable-ui-rest

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `AutoBroadbandIO` | bool | read, write | IsAutoBroadbandIOEnabled, SetAutoBroadbandIOEnabled | Not explicitly declared in schema | PPgTweaks.cpp | autoBroadbandIo | None |
| `Autoconnect` | bool | read, write | autoconnect | Not explicitly declared in schema | PPgConnection.cpp | autoConnect | None |
| `MaxConnections` | integer | read, write | GetMaxConnections, SetMaxConnections, maxconnections | Not explicitly declared in schema | PPgConnection.cpp, PPgStats.cpp | maxConnections | None |
| `MaxConnectionsPerFiveSeconds` | integer | read, write | GetMaxConperFive, SetMaxConsPerFive | Not explicitly declared in schema | PPgTweaks.cpp | maxConnectionsPerFiveSeconds | None |
| `MaxDownload` | integer | read, write | GetConfiguredMaxDownload, SetMaxDownload | Not explicitly declared in schema | PPgConnection.cpp | downloadLimitKiBps | None |
| `MaxSourcesPerFile` | integer | read, write | SetMaxSourcesPerFile | Not explicitly declared in schema | PPgConnection.cpp | maxSourcesPerFile | None |
| `MaxUpload` | integer | read, write | GetConfiguredMaxUpload, SetMaxUpload | Not explicitly declared in schema | PPgConnection.cpp | uploadLimitKiBps | None |
| `NetworkED2K` | bool | read, write | SetNetworkED2K, networked2k | Not explicitly declared in schema | PPgConnection.cpp | networkEd2k | None |
| `NetworkKademlia` | bool | read, write | GetNetworkKademlia, SetNetworkKademlia, networkkademlia | Not explicitly declared in schema | PPgConnection.cpp | networkKademlia | None |
| `QueueSize` | integer | read, write | GetQueueSize, SetQueueSize | Not explicitly declared in schema | PPgTweaks.cpp | queueSize | None |
| `SafeServerConnect` | bool | read, write | m_bSafeServerConnect | Not explicitly declared in schema | PPgServer.cpp | safeServerConnect | None |
| `UseCreditSystem` | bool | read, write | m_bCreditSystem | Not explicitly declared in schema | PPgTweaks.cpp | creditSystem | None |

#### persisted-runtime

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `AddServersFromClient` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `AllocateFullFile` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `AllowLocalHostIP` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `AppVersion` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `AutoArchivePreviewStart` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `AutoConnectStaticOnly` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `AutoShowLookups` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `BBPreferenceSchema` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `BringToFront` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `Check4NewVersionDelay` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `CreateCrashDump` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `CryptTCPPaddingLength` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DeadServerRetry` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DesktopUiRefreshIntervalMs` | integer | read, write | None | `NormalizeDesktopUiRefreshIntervalMs`; default `2000`; valid values `0`, `500`, `1000`, `2000`, `5000`, `10000`; `0` pauses transfer/client list refreshes | Tools menu | None | Native desktop transfer/client list refresh interval. Title, tray, and status transfer-rate text stays on the lightweight presentation timer. |
| `DebugClientKadUDP` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugClientTCP` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugClientUDP` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugHeap` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugLogLevel` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugSearchResultDetailLevel` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugServerSearches` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugServerSources` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugServerTCP` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DebugServerUDP` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `DefaultIRCServerNew` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `DisableFirstTimeWizard` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `DontRecreateStatGraphsOnResize` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `EnableScheduler` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `EnableSearchResultSpamFilter` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `FilterBadIPs` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `FilterServersByIP` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `FullChunkTransfers` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `GeoLocationLastUpdateTime` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `GeoLocationLookupEnabled` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `GeoLocationUpdatePeriodDays` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `GeoLocationUpdateUrl` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `HyperTextFont` | binary | read, write | None | Not explicitly declared in schema | None | None | None |
| `IPFilterLastUpdateTime` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `IPFilterUpdateEnabled` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `IRCAcceptLink` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `IRCAcceptLinkFriends` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `IRCFilterName` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `IRCFilterUser` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `IRCHelpChannel` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `IRCListOnConnect` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `IRCSoundEvents` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `IRCUseFilter` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `KadFileSearchLifetime` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `KadKeywordSearchLifetime` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `KadUDPKey` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `LastLogPaneID` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `LastMainWndDlgID` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `LogTextFont` | binary | read, write | None | Not explicitly declared in schema | None | None | None |
| `LostFromCorruption` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `ManualHighPrio` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `MaxMessageSessions` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `MessageFromValidSourcesOnly` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `MessagesFromFriendsOnly` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `MessageUseCaptchas` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `MinToTray_Aero` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `Nick` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierConfiguration` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierMailAuth` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierMailLogin` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierMailPassword` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierMailPort` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierMailRecipient` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierMailSender` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierMailServer` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierMailTLS` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierPopEveryChatMessage` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierPopNewVersion` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierSendMail` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierSoundPath` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifierUseSound` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifyOnChat` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifyOnDownload` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifyOnImportantError` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifyOnLog` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `NotifyOnNewDownload` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `OnlineSignature` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `PartsSavedByICH` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `RandomizePortsOnStartup` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `RemoveFilesToBin` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `SaveDebugToDisk` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `SavedFromCompression` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SaveLogToDisk` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `Scoresystem` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `SearchMethod` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SecureIdent` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `SeeShare` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `Serverlist` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `ServerUDPPort` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `ShowDownloadToolbar` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `ShowInfoOnCatTabs` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `ShowSharedFilesDetails` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `SkinProfile` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `SkinProfileDir` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `SmartIdCheck` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `SplitterbarPosition` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SplitterbarPositionFriend` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SplitterbarPositionIRC` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SplitterbarPositionServer` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SplitterbarPositionShared` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SplitterbarPositionStat` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SplitterbarPositionStat_HL` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `SplitterbarPositionStat_HR` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `StartupMinimized` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `StatGraphsInterval` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `StatsFillGraphs` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `StraightWindowStyles` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `TempDirs` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `ToolbarBitmap` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `ToolbarBitmapFolder` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `ToolbarIconSize` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `ToolbarLabels` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `ToolbarSetting` | string | read, write | None | Not explicitly declared in schema | None | None | None |
| `TransferWnd1` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `TransferWnd2` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `TransflstRemainOrder` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `UserSortedServerList` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `UseSimpleTimeRemainingComputation` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `UseSystemFontForMainControls` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `VariousStatisticsMaxValue` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `VerboseOptions` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `VersionCheckLastAutomatic` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `WatchClipboard4ED2kFilelinks` | bool | read, write | None | Not explicitly declared in schema | None | None | None |
| `WebMirrorAlertLevel` | integer | read, write | None | Not explicitly declared in schema | None | None | None |
| `WebTemplateFile` | string | read, write | None | Not explicitly declared in schema | None | None | None |

#### read-only-legacy

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `LogErrorColor` | color | read | None | Not explicitly declared in schema | None | None | Legacy/customization key is accepted on load; current Preferences.cpp has no matching writer. |
| `LogSuccessColor` | color | read | None | Not explicitly declared in schema | None | None | Legacy/customization key is accepted on load; current Preferences.cpp has no matching writer. |
| `LogWarningColor` | color | read | None | Not explicitly declared in schema | None | None | Legacy/customization key is accepted on load; current Preferences.cpp has no matching writer. |

### `eMule`

#### editable-ui

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `ShowVerticalHourMarkers` | bool | read, write | m_bShowVerticalHourMarkers | Not explicitly declared in schema | PPgTweaks.cpp | None | None |

### `FileCompletion`

#### editable-ui

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `FileCompletionArguments` | string | read, write | GetFileCompletionArguments, m_strFileCompletionArguments | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `FileCompletionProgram` | string | read, write | GetFileCompletionProgram, m_strFileCompletionProgram | Not explicitly declared in schema | PPgFiles.cpp | None | None |
| `RunCommandOnFileCompletion` | bool | read, write | GetRunCommandOnFileCompletion, m_bRunCommandOnFileCompletion | Not explicitly declared in schema | PPgFiles.cpp | None | None |

### `ListControlSetup`

#### dynamic-family

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `<dynamic:di>` | string | write | None | Not explicitly declared in schema | None | None | Dynamic family generated at runtime; source expression is guarded instead of enumerating every concrete key. |

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

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `LowRatioBoostEnabled` | bool | read, write | IsLowRatioBoostEnabled, SetLowRatioBoostEnabled | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `LowRatioThreshold` | number | read, write | GetLowRatioThreshold, SetLowRatioThreshold | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `SessionTimeLimitSeconds` | integer | read, write | GetSessionTimeLimitSeconds, SetSessionTimeLimitSeconds | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `SessionTransferLimitMode` | integer | read, write | GetSessionTransferLimitMode, SetSessionTransferLimitMode | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `SessionTransferLimitValue` | integer | read, write | GetSessionTransferLimitValue, SetSessionTransferLimitValue | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `SlowUploadCooldownSeconds` | integer | read, write | GetSlowUploadCooldownSeconds, SetSlowUploadCooldownSeconds | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `SlowUploadGraceSeconds` | integer | read, write | GetSlowUploadGraceSeconds, SetSlowUploadGraceSeconds | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `SlowUploadThresholdFactor` | number | read, write | GetSlowUploadThresholdFactor, SetSlowUploadThresholdFactor | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `SlowUploadWarmupSeconds` | integer | read, write | GetSlowUploadWarmupSeconds, SetSlowUploadWarmupSeconds | Not explicitly declared in schema | PPgTweaks.cpp | None | None |
| `ZeroUploadRateGraceSeconds` | integer | read, write | GetZeroUploadRateGraceSeconds, SetZeroUploadRateGraceSeconds | Not explicitly declared in schema | PPgTweaks.cpp | None | None |

#### editable-ui-rest

| Key | Type | Access | Owner/API | Default and normalization | UI | REST | Notes |
|---|---|---|---|---|---|---|---|
| `MaxUploadClientsAllowed` | integer | read, write | GetMaxUploadClientsAllowed, SetMaxUploadClientsAllowed | Not explicitly declared in schema | PPgTweaks.cpp | maxUploadSlots, uploadClientDataRate | None |

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
