# Review — 2026-04-13 Windows / MFC / Toolchain Deep Dive

## Scope

Revalidated the current Windows-facing technical debt against:

- `workspaces\v0.72a\app\eMule-main`
- `repos\emulebb-tooling\docs/active`
- `repos\emulebb-tooling\docs`

Also checked the locally installed Visual Studio / MSVC / MFC toolchain and
current Microsoft documentation.

## Toolchain Baseline

Current `main` project state (`srchybrid/emule.vcxproj`):

- `ToolsVersion="14.0"`
- `PlatformToolset=v143`
- `UseOfMfc=Static`
- `LanguageStandard=stdcpp17`
- `Import Project="$(VCTargetsPath)Microsoft.CPP.UpgradeFromVC71.props"`
- `EnableDpiAwareness=false` in both Debug and Release manifests

Local machine state:

- Visual Studio Professional 2022 `17.14.29 (March 2026)` is the only installed VS instance
- default MSVC tools version is `14.44.35207`
- local MFC headers still report the MFC 14.x family (`_MFC_VER 0x0E00`, filename version `140`)

Official Microsoft status:

- the MFC library is still supported, but Microsoft states it is no longer adding
  features or updating the MFC documentation
- Visual Studio 2026 release notes show newer MSVC/MFC components are available
  there, including MFC support for the newer `14.51` preview toolset

Practical answer to "are we using the latest MFC we can?":

- **On this machine:** yes, the project is already on the newest locally installed
  MFC/toolset line (`v143`, VS 2022, MSVC/MFC 14.44)
- **Across Microsoft's current product line:** no, this machine does not have the
  newer VS 2026 / MSVC 14.51 components installed
- **Inside the codebase itself:** also no, because the app uses almost none of the
  newer MFC UI classes that already exist in the installed toolset

Official references:

- https://learn.microsoft.com/en-us/cpp/mfc/mfc-desktop-applications?view=msvc-170
- https://learn.microsoft.com/en-us/visualstudio/releases/2026/release-notes

## Findings

### 1. `docs/active` still overclaimed several removals

The live app tree still contains code that `docs/active/INDEX.md` had listed as
"already in main":

- `WebServer.cpp`, `WebSocket.cpp`, and `PPgWebServer.cpp` are still compiled by
  `srchybrid/emule.vcxproj`
- `Emule.cpp:701` still constructs `CWebServer`
- `WebSocket.cpp` still actively uses `mbedtls_*`
- `emule.vcxproj:81,117` still links `mbedtls.lib`, `mbedx509.lib`, `tfpsacrypto.lib`,
  and `id3lib.lib`
- `FileInfoDialog.cpp` and `KnownFile.cpp` still use `ID3_Tag` / `ID3_Frame`

That means the prior "MbedTLS + web server removed" and
"id3lib removal -> MediaInfo" rows were false for current `main`.

### 2. The project file still carries a lot of historical build baggage

Revalidated current baggage in `srchybrid/emule.vcxproj`:

- `ToolsVersion="14.0"` at the root
- `Microsoft.CPP.UpgradeFromVC71.props` still imported
- static MFC linking remains enabled
- `DelayLoadDLLs` still lists `gdiplus.dll`, `msimg32.dll`, `oleacc.dll`, and `ws2_32.dll`
- `EnableDpiAwareness=false` remains set in both Debug and Release
- `_CRT_SECURE_NO_DEPRECATE` is still injected via project-wide preprocessor settings

None of this blocks the build, but it is clear evidence that the project is still
carrying compatibility-era and upgrade-era scaffolding.

### 3. The codebase is on modern MFC binaries, but not using modern MFC UI classes

Current `srchybrid` counts from the live tree:

- `243` hits for `CPropertySheet` / `CPropertyPage` / `CTreePropSheet`
- `34` files still touch `ResizableLib`
- `70` hits for `CCriticalSection` / `CSingleLock` / `CEvent` / `CMutex`
- `334` hits for classic MFC container classes
- `20` `AfxBeginThread` call sites
- `0` hits for `CMFCPropertySheet`, `CMFCTabCtrl`, or `CMFCDynamicLayout`

Representative live code:

- `PreferencesDlg.h:23` still derives `CPreferencesDlg` from `CTreePropSheet`
- `TreePropSheet.h:65` still implements a custom `CPropertySheet` wrapper

So the project is using current-enough MFC runtimes, but not the MFC feature set that
has existed for years in those runtimes.

Result:

- added `REF-032` to track migration toward MFC-native property sheets and dynamic layout

### 4. Compatibility-era dynamic Win32 API loading is still live

Current `srchybrid` still has:

- `10` `LoadLibrary` call sites
- `21` `GetProcAddress` call sites

Not all of those are bad. Dynamic loading remains appropriate for optional modules like
MediaInfo, UnRAR, and language DLLs.

The compatibility debt is the always-present Win10 API subset:

- `Emule.cpp:181-182` — `GetProcessDEPPolicy` / `SetProcessDEPPolicy`
- `Emule.cpp:269` — `HeapSetInformation`
- `EmuleDlg.cpp:382` — `ChangeWindowMessageFilter`
- `EmuleDlg.cpp:3907-3914` — `DwmGetColorizationColor`
- `Preferences.cpp:2976` — `SHGetKnownFolderPath`
- `Preferences.cpp:3181-3186` — `DwmIsCompositionEnabled`
- `Mdump.cpp:65-71` — `MiniDumpWriteDump`

These are still good cleanup candidates for `REF-020`.

### 5. Blanket deprecation suppression is still hiding real cleanup work

Current live state:

- `Stdafx.h:73-74` still defines `_CRT_SECURE_NO_DEPRECATE`
- `Stdafx.h:99-100` still defines `_WINSOCK_DEPRECATED_NO_WARNINGS`
- `emule.vcxproj:310` still injects `_CRT_SECURE_NO_DEPRECATE`

Current call-site counts in `srchybrid`:

- `15` `inet_addr`
- `4` `inet_ntoa`
- `0` `gethostbyname`
- `49` legacy printf-family calls (`_stprintf`, `_sntprintf`, `wsprintf`, `sprintf`)

That keeps `REF-021` and `REF-023` fully justified.

### 6. The manifest and Windows shell surface are still conservative / legacy-heavy

Current manifests:

- `res/emulex64.manifest` still declares Vista, 7, 8, 8.1, and 10
- `res/emuleARM64.manifest` still declares 8, 8.1, and 10
- neither manifest declares a `Microsoft.Windows.Common-Controls 6.0` dependency

Other still-live Windows-specific cleanup targets:

- `Pinger.cpp` still keeps a raw ICMP socket path for UDP ping fallback
- the custom HTTP client stack remains in place instead of using `WinHTTP`
- taskbar progress integration is already present in `EmuleDlg.cpp`, so the older
  "missing taskbar progress" modernization note is stale for current `main`

## Practical Priority

The highest-value Windows/MFC follow-up items remain:

1. `FEAT-017` + `REF-026` — DPI and manifest modernization
2. `REF-020` + `REF-021` + `REF-023` — remove Win10 compatibility shims and warning suppression debt
3. `REF-032` — start using MFC-native UI host/layout classes already available in the installed toolset
4. `REF-028` — keep the live web/TLS dependency stack current if the WebServer path remains strategic

## Docs Updated By This Review

- `docs/active/INDEX.md`
- `docs/active/REF-003.md`
- `docs/active/REF-016.md`
- `docs/active/REF-020.md`
- `docs/active/REF-021.md`
- `docs/active/REF-025.md`
- `docs/active/REF-026.md`
- `docs/active/REF-028.md`
- `docs/active/FEAT-007.md`
- `docs/active/REF-032.md`
- this review file

Historical docs were also marked as stale where they were still claiming branch-only
removals as if they were current `main`.
