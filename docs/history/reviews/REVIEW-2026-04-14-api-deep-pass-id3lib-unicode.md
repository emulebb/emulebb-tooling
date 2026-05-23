# Review — 2026-04-14 API Deep Pass / id3lib Unicode

> Historical reference only: `stale-v0.72a-experimental-clean` and
> `analysis\stale-v0.72a-experimental-clean` are retired reference sources, not
> active branch targets or current baselines. Use them only as provenance or
> idea-extraction sources; landed status is determined against `main`. See
> [Historical References](../../HISTORICAL-REFERENCES.md).

## Scope

Focused on two things only:

- live Windows / CRT / Winsock API modernization seams still present in current
  `workspaces\v0.72a\app\eMule-main\srchybrid`
- whether the vendored `repos\third_party\emulebb-id3lib` can realistically be
  made Unicode-safe, rather than just documented as "old"

## Findings

### 1. `id3lib.vcxproj` says Unicode, but the actual library path API is still narrow

The current vendor project is built with `CharacterSet=Unicode` in
`repos\third_party\emulebb-id3lib\libprj\id3lib.vcxproj`, but that does **not**
mean the library can safely consume UTF-16 file paths.

The actual implementation still hinges on narrow path handling:

- `include\id3\tag.h` exposes only `ID3_Tag::Link(const char *fileInfo, ...)`
- `src\tag_impl.h` stores `_file_name` as narrow `dami::String`
- `src\utils.cpp` opens `ifstream` / `fstream` with `name.c_str()`
- `src\tag_file.cpp` still uses `CreateFileA` for truncate and narrow
  `remove(...)` / `rename(...)` for replace paths
- `src\field_binary.cpp` still uses `fopen_s(const char*, ...)`

So the current vendor tree is "Unicode" only in the Visual Studio project
setting sense, not in the filename / filesystem sense that matters to eMule.

### 2. Current `main` still downcasts UTF-16 paths to ANSI before calling `id3lib`

The two live app integrations both still do a lossy path conversion:

- `srchybrid\FileInfoDialog.cpp:883-888`
- `srchybrid\KnownFile.cpp:1421-1426`

Both construct `CStringA` from the UTF-16 file path and then call
`ID3_Tag::Link(...)` on the ANSI buffer.

That makes metadata extraction depend on the active ANSI code page, not on the
actual Unicode filename the rest of the app can open.

### 3. The app is still carrying explicit `id3lib` Unicode workarounds

Current `main` still contains integration-side bug notes and workarounds:

- `FileInfoDialog.cpp:731-764`
  - local `ID3_GetStringW(...)` wrapper only trusts `id3lib`'s Unicode path
    when the source frame is already UTF-16
  - the code explicitly documents `ID3_FieldImpl::Get(unicode_t*, ..., itemNum)`
    / `GetRawUnicodeTextItem` as broken
- `FileInfoDialog.cpp:878-885` and `KnownFile.cpp:1416-1423`
  - the code explicitly avoids mixed ID3v1 + ID3v2 parsing because `id3lib`
    corrupts Unicode strings in that case

That means there are really two problems:

1. filename Unicode is broken
2. field-level Unicode extraction is not trustworthy even after the file opens

### 4. No audited sibling tree contains a Unicode-safe `id3lib` port

- `stale-v0.72a-experimental-clean`
  - removed `id3lib` rather than fixing it
- `emuleai`
  - current workspace snapshot still carries third-party notices, but has no
    active `srchybrid` `ID3_Tag` / `ID3_GetStringW` call sites to port

So there is no direct cherry-pick path for "Unicode-safe id3lib on Windows" in
the currently audited sibling trees.

### 5. Small fix vs full fix are different projects

**Phase A — minimal current-main fix**

Because eMule uses `id3lib` only in two read-only metadata paths, the smallest
viable fix is:

- stop calling `Link(const char*)` from app code
- open the MP3 through a UTF-16 / long-path-safe seam
- feed the bytes into `ID3_Tag::Link(ID3_Reader&)`

That can solve Unicode filenames for the current app use case without first
making the whole vendor library read/write Unicode-safe.

**Phase B — full vendor Unicode support**

If `id3lib` is to remain a strategic dependency, the vendor tree still needs:

- wide or explicit UTF-8-normalized filename APIs in `ID3_Tag` / `ID3_TagImpl`
- wide-aware replacements for `openReadableFile`, `openWritableFile`,
  `createFile`, `truncate`, `remove`, `rename`, and `fopen_s` file paths
- regression tests for:
  - filenames outside ACP
  - mixed ID3v1 + ID3v2
  - multi-item Unicode text frames
  - any binary frame file import/export still in use

**Phase C — replacement / removal**

If that vendor patch burden is not worth it, the sibling-tree precedent is to
remove or replace `id3lib`, not to keep papering over it in app code.

### 6. Additional API seams still live after the earlier Windows pass

The deeper line-by-line pass turned up these still-live hotspots in current
`main`:

- `inet_ntoa`
  - `4` live sites, all concentrated in `AsyncSocketEx.cpp` and
    `AsyncSocketExLayer.cpp`
- `WSAAsyncGetHostByName`
  - `6` live call/reply sites across `AsyncSocketEx.cpp`, `DownloadQueue.cpp`,
    `EmuleDlg.cpp`, and `UDPSocket.cpp`
- `timeGetTime`
  - `13` live sites, concentrated in `EMSocket.cpp` and
    `UploadBandwidthThrottler.cpp`
- `CoInitialize(NULL)`
  - `11` live sites; explicit `CoInitializeEx(...)` would make apartment intent
    visible and auditable
- raw `wcscpy`
  - `3` live sites in `CustomAutoComplete.cpp`, `EmuleDlg.cpp`, and
    `FileInfoDialog.cpp`
- `SHGetFileInfo`
  - `5` live shell display/icon sites in `DirectoryTreeCtrl.cpp`, `Emule.cpp`,
    and `SharedDirsTreeCtrl.cpp`

Not all of these need new backlog rows, but they are still real modernization
surface in `main`, not already-cleaned history.

## Backlog Mapping

- `BUG-028`
  - current `id3lib` ANSI-only / Unicode metadata bug in `main`
- `REF-021`
  - blanket deprecation suppressions plus remaining `inet_ntoa` / related
    Winsock cleanup
- `REF-030`
  - one slice of the remaining window-message DNS resolver debt
- `REF-026` + `FEAT-017`
  - shell / manifest / DPI modernization around the current shell-facing UI
    surfaces

## Practical Recommendation

If the goal is to improve current `main` with minimal drift, do **not** start by
patching all of `id3lib`.

Start with the read-only eMule integration:

1. remove the ANSI path downcast in the two call sites
2. route MP3 reads through `ID3_Tag::Link(ID3_Reader&)` from a Unicode-safe open
3. keep the existing text-getter workaround until the vendor Unicode field code
   is either fixed or the dependency is retired

That gets the user-visible filename bug out first, without immediately taking on
full dependency surgery.
