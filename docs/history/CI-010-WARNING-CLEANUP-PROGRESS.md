# CI-010 Warning Cleanup Progress Log

Commit-by-commit landed-on-`main` progress and scoped-validation trail for
[CI-010](../active/items/CI-010.md). Moved out of the active item to keep
it a current triage spec; the item keeps a short progress summary.

## Current Mainline Progress

Commit `4afa47b` (`CI-010: reduce EmuleDlg callback warnings`) landed on
`main`:

- `BindLossIpInterfaceChangeCallback()` and
  `BindLossUnicastAddressChangeCallback()` are now declared `noexcept`, making
  the Win32 notification callback boundary explicit and removing the two local
  C5039 callback warnings surfaced by recompiling `EmuleDlg.cpp`.
- `CemuleApp::IsIdleMessage()` now stores `GetTickCount64()` state in an
  `ULONGLONG` static instead of truncating through `DWORD`, removing the two
  local C4244 warnings in that idle-processing path.

Commit `edda7c6` (`CI-010: tighten PCP NAT-PMP warning types`) landed on
`main`:

- PCP/NAT-PMP warning logs now store `GetPcpStateText()` results in local
  `CString` variables and pass explicit `LPCTSTR` pointers through the logging
  varargs boundary, removing the local C4840 warnings.
- `pcp_new_flow()` now receives an explicit `uint8_t` protocol value, removing
  the local protocol-narrowing warning while preserving the existing TCP/UDP
  selection behavior.

Commit `b97bcb7` (`CI-010: keep UDP queue timing wide`) landed on `main`:

- `CClientUDPSocket::SendControlData()` now keeps its queue-age comparison
  timestamp as `ULONGLONG`, matching `UDPPack::dwTime` and avoiding truncation
  of `GetTickCount64()` before UDP control-packet expiry checks.

Commit `dafa207` (`CI-010: mark font enumeration callback noexcept`) landed on
`main`:

- `CTreeOptionsFontNameCombo::_EnumFontProc()` and its local bridge method are
  now `noexcept`, making the GDI `EnumFonts()` callback boundary explicit and
  removing the local C5039 warning.

Commit `206622c` (`CI-010: avoid download menu handle truncation`) landed on
`main`:

- `DownloadListCtrl.cpp` now enables and removes popup submenu items by finding
  the matching `hSubMenu` by position instead of casting `HMENU` through
  `UINT`.
- This removes the local C4311/C4302 handle-truncation warnings for the download
  context menu while preserving the existing menu layout and command IDs.

Commit `abeaa01` (`CI-010: keep download list ticks wide`) landed on `main`:

- `CtrlItem_Struct::dwUpdated` and
  `CDownloadListCtrl::m_dwLastAvailableCommandsCheck` now store
  `GetTickCount64()` values as `ULONGLONG`, removing the local C4244
  truncation warnings in progress-bar cache expiry and available-command
  throttling.

Commit `cfc5c1a` (`CI-010: annotate download list fallthroughs`) landed on
`main`:

- `DownloadListCtrl.cpp` now marks its two intentional switch fallthroughs with
  `[[fallthrough]]`: progress-column drawing falls into normal cell drawing,
  and active part-file cancel/delete handling falls into paused-file deletion
  after optional next-file scheduling.

Commit `8c07361` (`CI-010: make download progress size cast explicit`) landed
on `main`:

- `CDownloadListCtrl::GetFinishedSize()` now makes the completed-byte total to
  taskbar-progress `float` conversion explicit. This removes the local C5219
  display/progress warning while preserving the existing taskbar progress math.

Commit `da3de63` (`CI-010: avoid shared menu handle truncation`) landed on
`main`:

- `SharedDirsTreeCtrl.cpp` and `SharedFilesCtrl.cpp` now enable priority popup
  submenus by finding the matching `hSubMenu` by position instead of casting
  `HMENU` through `UINT`.
- This removes the local C4311/C4302 handle-truncation warnings for the shared
  files priority menus while preserving existing menu layout and command IDs.

Commit `9c4d686` (`CI-010: clarify shared files fallthroughs`) landed on
`main`:

- `SharedDirsTreeCtrl.cpp` now uses explicit `break` statements for the
  priority command switch and the outer file-operation switch, removing two
  accidental-looking fallthrough warnings without changing command handling.
- `SharedFilesCtrl.cpp` now marks the intentional icon-then-text drawing
  fallthrough with `[[fallthrough]]`.

Commit `2590f1f` (`CI-010: remove dead shared tree helper`) landed on `main`:

- Removed the unreferenced internal `FindNearestSharedTreeParentItem()` helper
  from `SharedDirsTreeCtrl.cpp`, eliminating the local C5245 dead-code warning
  while leaving the active shared-tree parent path helper intact.

Commit `97d65b3` (`CI-010: keep server upload ticks wide`) landed on `main`:

- `CServerConnect::connectionattempts` now keys connection attempts by
  `ULONGLONG`, and the timeout/removal iterator keys match that width. This
  keeps `GetTickCount64()` values intact for server connect timeout handling.
- `CUploadQueue::m_dwRemovedClientByScore` now stores the existing
  `GetTickCount64()` initializer in `ULONGLONG` storage, removing another
  queue-timing truncation point.

Commit `e56b38a` (`CI-010: clarify search list fallthroughs`) landed on
`main`:

- `SearchListCtrl.cpp` now marks the owner-draw file-name switch fallthroughs
  explicitly: the file-name cases adjust tree/icon indentation and then fall
  into the shared text drawing path.
- `DrawSourceChild()` now breaks immediately after the default text drawing
  path, removing the empty fallthrough into the file-type/file-hash cases.

Commit `b41fab9` (`CI-010: extract search summary file size`) landed on
`main`:

- `SearchListCtrl.cpp` now extracts the `CEMFileSize` wrapper to `uint64`
  before passing it through `CString::Format()` for copied search summaries,
  removing the local C4840 varargs warning without changing copied output.

Commit `e7505de` (`CI-010: make search display math explicit`) landed on
`main`:

- `SearchListCtrl.cpp` now uses explicit float/double conversions for search
  result color-shade interpolation, debug Kad trust display, and MiB display
  formatting.
- The touched conversions are display-only; the existing truncating RGB shade
  behavior and formatted output precision are preserved.

Commit `e2f4007` (`CI-010: match app initializer order`) landed on `main`:

- `CemuleApp` constructor initializers now match the member declaration order
  for the IP filter/geolocation/app-state cluster and the queued-log
  counter/startup-bind cluster.
- This removes the local C5038 initializer-order warnings without changing
  actual construction order or runtime behavior.

Commit `c8ea5d6` (`CI-010: expose base command-line parser overloads`) landed
on `main`:

- `CEmuleCommandLineInfo` now exposes the base `CCommandLineInfo::ParseParam`
  overload set before overriding the active `TCHAR` overload.
- This removes the local C4266 hidden-virtual warning without changing the
  existing `-c <base-dir>` skip behavior.

Commit `1c42e02` (`CI-010: remove dead app journal lookup`) landed on `main`:

- Removed the unused const `FindMonitoredSharedRootJournalState()` overload
  from `Emule.cpp`.
- The mutable lookup overload remains in use for monitored-share journal state
  loading and refresh paths.

Commit `6bdddcf` (`CI-010: use pointer-width shell icon cache casts`) landed on
`main`:

- `CemuleApp::GetFileTypeSystemImageIdx()` now stores and retrieves shell icon
  indices in the existing `CMapStringToPtr` caches with `LongToPtr()` and
  `PtrToLong()`.
- This removes the local C4311/C4302/C4312 pointer-payload warnings while
  preserving the existing extension-to-icon-index cache structure.

Commit `6b09478` (`CI-010: keep local source request ordering wide`) landed on
`main`:

- `CDownloadQueue::ProcessLocalRequests()` now keeps the local-server source
  request priority comparison in `ULONGLONG` tick space instead of narrowing
  `CPartFile::m_LastSearchTime` through a `DWORD`.
- The existing priority bias and request selection behavior are preserved.

Commit `77f53d8` (`CI-010: make download queue progress math explicit`) landed
on `main`:

- `CDownloadQueue::Process()` now makes the byte-count to float conversion
  explicit when updating `theStats.m_fGlobalDone` and
  `theStats.m_fGlobalSize`.
- The progress totals remain float-based for the existing UI/status consumers;
  only the conversion intent is clarified.

Commit `55c36eb` (`CI-010: make credit ratio math explicit`) landed on
`main`:

- `CClientCredits::GetScoreRatio()` now captures uploaded/downloaded byte
  totals once and uses explicit float conversions at the established ratio,
  exponential cap, and linear cap calculations.
- The existing credit formula and clamp behavior are preserved.

Commit `9cf16a3` (`CI-010: annotate IRC registration fallthrough`) landed on
`main`:

- `IrcMain.cpp` now uses `[[fallthrough]]` for the intentional numeric-reply
  `001` to `002`/`003`/`004` path. Reply `001` still sets logged-in state,
  optionally requests the channel list, runs perform commands, and then shares
  the normal status-display path.

Commit `cdb38f5` (`CI-010: annotate part file fallthroughs`) landed on
`main`:

- `PartFile.cpp` now uses `[[fallthrough]]` for the intentional
  `DS_ONQUEUE` to shared reask/connect handling path and for the `PB_READY` to
  `PB_PENDING` flush-buffer continue path.
- Existing UDP reask behavior, shared TCP/connect reask handling, and
  buffered-write state handling are preserved.

Commit `173acb6` (`CI-010: make part file progress math explicit`) landed on
`main`:

- `PartFile.cpp` now makes its progress, time-remaining, rating, progress-bar,
  and availability integer-to-floating conversions explicit.
- The touched values are existing display, estimate, and summary calculations;
  the established float/double domains and rounding behavior are preserved.

Commit `e017824` (`CI-010: match tweaks initializer order`) landed on `main`:

- `PPgTweaks.cpp` now initializes `m_bUseSystemFontForMainControls` before
  `m_bVerbose`, matching the declaration order in `PPgTweaks.h`.
- This removes the local C5038 initializer-order warning without changing
  actual construction order.

Commit `984f272` (`CI-010: annotate proxy error fallthrough`) landed on
`main`:

- `EMSocket.cpp` now marks the intentional `PROXYERROR_NOCONN` to
  `PROXYERROR_REQUESTFAILED` fallthrough in proxy-layer callback handling.
- The existing behavior is preserved: no-connection proxy failures still set
  the connect-failed flag and then share the verbose proxy error detail path.

Commit `be22d9f` (`CI-010: clarify media info switch breaks`) landed on
`main`:

- `FileInfoDialog.cpp` now breaks explicitly after the handled MPEG version and
  layer cases that previously fell into `default: break`.
- The parsed media-format text and audio format tag behavior are unchanged.

Commit `913b54f` (`CI-010: annotate IRC smiley fallthrough`) landed on
`main`:

- `IrcWnd.cpp` now marks the intentional `IDC_SMILEY` to `default` fallthrough
  in `CIrcWnd::OnCommand()`.
- Existing behavior is preserved: the smiley command runs and returns
  immediately instead of falling through to the shared input-focus reset.

Commit `e73b24b` (`CI-010: keep delayed edit ticks wide`) landed on `main`:

- `CEditDelayed::m_dwLastModified` now stores `GetTickCount64()` values in
  `ULONGLONG` storage instead of narrowing through `DWORD`.
- This removes the delayed filter edit's local C4244 timestamp truncation
  warnings while preserving the existing 400 ms delayed-evaluation behavior.

Commit `bdbe018` (`CI-010: avoid Kad search metadata pointer truncation`)
landed on `main`:

- Kad search result metadata still uses the existing legacy varargs shape, but
  the `uint32` payloads are now packed and unpacked through `UINT_PTR` instead
  of truncating through `uint32` pointer casts.
- This removes the local C4311/C4302 pointer-truncation warnings in
  `SearchList.cpp` while preserving the existing `TAGTYPE_UINT32` metadata
  values for length, bitrate, and source count.

Commit `e4fd71e` (`CI-010: mark CRT alloc hook pointer noexcept`) landed on
`main`:

- The debug CRT allocation hook's saved previous-hook pointer now uses the same
  `noexcept` callback contract as `eMuleAllocHook()`, and the debug statistics
  translation units share that declaration.
- This removes the local C5039 extern-C callback-boundary warnings around
  `_CrtSetAllocHook()` while preserving the existing debug-only allocation-hook
  behavior.

Scoped validation:

- `python -m emule_workspace validate`
- `python -m emule_workspace build app --config Debug --platform x64`
  - First pass rebuilt `EmuleDlg.cpp` and reduced its reported warnings from 34
    to 26.
  - Immediate incremental pass completed all app targets with `0` warnings.
  - The PCP/NAT-PMP slice completed all app targets with `0` warnings.
  - The UDP timing slice completed all app targets with `0` warnings.
  - The TreeOptions callback slice first rebuilt UI dependents and surfaced
    existing unrelated warning debt; the immediate incremental pass completed
    all app targets with `0` warnings.
  - The download menu handle-truncation slice first rebuilt
    `DownloadListCtrl.cpp` and left only unrelated local warning families; the
    immediate incremental pass completed all app targets with `0` warnings.
  - The download-list tick-width slice first rebuilt UI dependents and left only
    unrelated local warning families; the immediate incremental pass completed
    all app targets with `0` warnings.
  - The download-list fallthrough slice rebuilt `DownloadListCtrl.cpp` and left
    only unrelated local warning families; the immediate incremental pass
    completed all app targets with `0` warnings.
  - The download progress-size slice rebuilt `DownloadListCtrl.cpp`; its only
    remaining local warning is the separately triaged MFC message-map C4191
    bucket. The immediate incremental pass completed all app targets with `0`
    warnings.
  - The shared menu handle-truncation slice rebuilt the shared files UI surfaces
    and left only unrelated local warning families; the immediate incremental
    pass completed all app targets with `0` warnings.
  - The shared-files fallthrough slice rebuilt the same UI surfaces and left
    only unrelated local warning families; the immediate incremental pass
    completed all app targets with `0` warnings.
  - The dead shared-tree helper slice completed all app targets with `0`
    warnings.
  - The server/upload tick-width slice rebuilt broad app surfaces and left only
    unrelated local warning families. The immediate incremental pass completed
    all app targets with `0` warnings.
  - The search-list fallthrough slice rebuilt `SearchListCtrl.cpp`; its
    remaining local warnings are separate C4840/C5219 numeric and varargs
    warnings. The immediate incremental pass completed all app targets with
    `0` warnings.
  - The search-summary file-size slice rebuilt `SearchListCtrl.cpp`; the local
    C4840 warning is gone and the remaining local warnings are C5219 numeric
    display conversions. The immediate incremental pass completed all app
    targets with `0` warnings.
  - The search display-math slice rebuilt `SearchListCtrl.cpp` and completed
    all app targets with `0` warnings on the first pass.
  - The app initializer-order slice rebuilt `Emule.cpp`; the local C5038
    warnings are gone and the remaining local warnings are separate C4266,
    C5039, pointer-payload, and dead-helper items. The immediate incremental
    pass completed all app targets with `0` warnings.
  - The command-line parser overload slice rebuilt `Emule.cpp`; the local
    C4266 warning is gone and the remaining local warnings are separate C5039,
    pointer-payload, and dead-helper items. The immediate incremental pass
    completed all app targets with `0` warnings.
  - The app journal lookup slice rebuilt `Emule.cpp`; the local C5245 warning
    is gone and the remaining local warnings are separate C5039 and
    pointer-payload items. The immediate incremental pass completed all app
    targets with `0` warnings.
  - The shell-icon cache slice rebuilt `Emule.cpp`; the local C4311/C4302/C4312
    pointer-payload warnings are gone and only the separate debug CRT hook
    C5039 warnings remain in that file. The immediate incremental pass
    completed all app targets with `0` warnings.
  - The local source-request ordering slice rebuilt `DownloadQueue.cpp`; the
    local C4244 tick truncation warning is gone and remaining warnings in that
    file are separate C5219 display/ratio math. The immediate incremental pass
    completed all app targets with `0` warnings.
  - The download queue progress-math slice rebuilt `DownloadQueue.cpp` and
    completed all app targets with `0` warnings on the first pass.
  - The credit-ratio math slice rebuilt `ClientCredits.cpp` and completed all
    app targets with `0` warnings on the first pass.
  - The IRC registration fallthrough slice rebuilt `IrcMain.cpp` and completed
    all app targets with `0` warnings on the first pass.
  - The part-file fallthrough slice rebuilt `PartFile.cpp`; the local C5262
    warnings are gone and the remaining local warnings are separate C5219
    numeric conversion items.
  - The part-file progress-math slice rebuilt `PartFile.cpp`; local compiler
    warnings dropped to zero. The first pass reported one Crypto++ weak
    algorithm banner line as a workspace warning, and the immediate incremental
    pass completed all app targets with `0` warnings.
  - The tweaks initializer-order slice rebuilt the current `Release|x64` main
    target and completed with `0` warnings.
  - The proxy error fallthrough slice rebuilt the current `Release|x64` main
    target and completed with `0` warnings.
  - The media-info switch-break slice rebuilt the current `Release|x64` main
    target and completed with `0` warnings.
  - The IRC smiley fallthrough slice rebuilt the current `Release|x64` main
    target and completed with `0` warnings.
  - The delayed-edit tick-width slice rebuilt the current `Debug|x64` and
    `Release|x64` main targets with CFG verification. `EditDelayed.cpp`
    rebuilt in both logs without its previous C4244 timestamp warnings. Build
    logs:
    `workspaces\workspace\state\build-logs\20260510-062418\summary.json` and
    `workspaces\workspace\state\build-logs\20260510-062432\summary.json`.
  - The Kad search metadata pointer-width slice rebuilt the current
    `Debug|x64` and `Release|x64` main targets with CFG verification.
    `SearchList.cpp` and `kademlia\kademlia\Search.cpp` rebuilt without the
    previous C4311/C4302 pointer-truncation warnings. Build logs:
    `workspaces\workspace\state\build-logs\20260510-062718\summary.json` and
    `workspaces\workspace\state\build-logs\20260510-062728\summary.json`.
  - The CRT allocation hook no-throw pointer slice rebuilt the current
    `Debug|x64` and `Release|x64` main targets with CFG verification.
    The rebuilt logs no longer contain the previous C5039 `_CrtSetAllocHook`
    warnings. Build logs:
    `workspaces\workspace\state\build-logs\20260510-063024\summary.json` and
    `workspaces\workspace\state\build-logs\20260510-063038\summary.json`.

The item remains `In Progress`: the remaining `EmuleDlg.cpp` warnings are
separate MFC message-map and UI/stat numeric warnings, and the broader
Release|x64 warning floor still needs dedicated follow-up slices.
