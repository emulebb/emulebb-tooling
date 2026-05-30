---
id: FEAT-007
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/56
title: Windows Property Store integration for non-media file metadata
status: OPEN
priority: Minor
category: feature
labels: [metadata, windows-api, exploratory]
milestone: ~
created: 2026-04-08
source: REFACTOR-TASKS.md (REFAC_010)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/56. This local document is retained as an engineering spec/evidence record.

> Historical reference only: `stale-v0.72a-experimental-clean` and
> `analysis\stale-v0.72a-experimental-clean` are retired reference sources, not
> active branch targets or current baselines. Use them only as provenance or
> idea-extraction sources; landed status is determined against `main`. See
> [Historical References](../../HISTORICAL-REFERENCES.md).

## Summary

The current metadata pipeline already uses `MediaInfo.dll`, but current `main`
still also carries legacy `id3lib` paths for MP3 tag extraction. For non-audio/video
files (images, documents,
PDFs, archives), the Windows Property Store (`IPropertyStore`) can provide
rich metadata (author, title, page count, dimensions, etc.) without an
additional library dependency.

2026-04-18 note: the audio/video path was modernized on `main` to use a shared
`MediaInfo.dll` helper first, with built-ins and `id3lib` retained as fallback.
That change used the stale experimental tree only as a helper-extraction
reference; it did not port the stale dependency policy or reduce the separate
value of Property Store work for non-media files.

**Status: Exploratory — not committed to implementation.**

## Proposed Architecture

1. **First path**: try Windows Property Store (`IPropertyStore`) via
   `SHGetPropertyStoreFromParsingName()`.
2. **Fallback**: `MediaInfo.dll` where it adds coverage beyond the Windows
   property system.
3. **Result merge**: combine results from both sources, preferring the
   most specific value.

## Why Now

- `MediaInfo` is being refactored into per-format files anyway.
- Windows Property Store is available on all supported OS versions (Windows 10+).
- Current `main` still keeps both `MediaInfo` and `id3lib`, so Property Store is a
  Windows-native way to improve non-media metadata coverage without expanding the
  third-party dependency surface further.

## Scope

- File types NOT currently handled well by `MediaInfo` alone:
  - Office documents (`.docx`, `.xlsx`, `.pptx`)
  - PDF files
  - Images (EXIF via Windows Imaging Component / Shell Properties)
  - ZIP archives (`.zip`, `.7z`)

## Risk

Unknown effort — the Windows Property Store API surface is wide and
per-format coverage varies. The "exploratory" status reflects this.

## Files

- `srchybrid/FileInfoDialog.cpp` / `.h` — metadata display
- `srchybrid/MediaInfo*.cpp` / `.h` — existing MediaInfo integration
- New: `srchybrid/PropertyStoreMetadata.cpp` / `.h` (if pursued)
