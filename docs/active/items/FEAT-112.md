---
id: FEAT-112
title: Add Torrent search type convenience filter and refresh file-type extensions
status: OPEN
priority: Minor
category: feature
labels: [search, kad, file-types, rest, ui, compatibility, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-05
source: operator request to add Torrent search without changing ED2K server behavior
---

# FEAT-112 - Add Torrent Search Type Convenience Filter And Refresh File-Type Extensions

## Summary

Add `Torrent` as a convenience search file type while preserving stock eD2K and
Kad wire behavior. The new search type should mean `.torrent` filename
extension filtering, not a new `FT_FILETYPE` protocol value.

The same work should conservatively review the local file-extension table used
for existing `FT_FILETYPE` classification so eMuleBB classifies, publishes, and
filters modern obvious file formats more accurately.

## Intended Shape

- Add a desktop search file-type entry labeled `Torrent`.
- Add REST/API search type token `torrent`.
- Treat Torrent search as `FT_FILEFORMAT = "torrent"`.
- Do not send or publish `FT_FILETYPE = "Torrent"`.
- Keep current protocol-facing file-type mappings:
  - `Audio` -> `FT_FILETYPE=Audio`
  - `Video` -> `FT_FILETYPE=Video`
  - `Image` -> `FT_FILETYPE=Image`
  - `Document` -> `FT_FILETYPE=Doc`
  - `Program` -> `FT_FILETYPE=Pro`
  - `Archive` and `CD-Image` -> `FT_FILETYPE=Pro`
  - `Collection` -> `FT_FILETYPE=EmuleCollection`
- Locally narrow Torrent results by extension-derived classification, matching
  the existing internal result-type filter behavior used by internal types such
  as Archive and CD-Image.

## Extension Review

Review the extension table used by `GetED2KFileTypeID()` conservatively:

- Add `.torrent` as the new Torrent convenience type.
- Add obvious missing modern extensions only where they have low ambiguity.
- Prefer formats already recognized elsewhere in eMuleBB, such as existing
  file-header or fake-file classifier coverage.
- Avoid broad extension sweeps and ambiguous extensions that could change user
  expectations or protocol-adjacent behavior unexpectedly.

Kad should benefit from the reviewed classification because eMuleBB publishes
Kad `TAG_FILETYPE` from local extension classification. Kad extension filters
can also match `FT_FILEFORMAT` against the filename extension without requiring
`TAG_FILEFORMAT` publication.

## Scope Constraints

- Do not change ED2K server behavior or require server support for a new type.
- Do not add a new stock-incompatible eD2K or Kad file-type string/integer.
- Do not add BitTorrent download, magnet, tracker, or `.torrent` import
  support.
- Do not change existing `Audio`, `Video`, `Image`, `Doc`, `Pro`,
  `EmuleCollection`, Archive, or CD-Image wire meanings.
- Do not broaden REST beyond the search type vocabulary needed for this
  convenience filter.

## Acceptance Criteria

- [ ] The desktop search file-type dropdown includes `Torrent`.
- [ ] REST/API search accepts lowercase `torrent` and rejects unsupported or
      wrongly-cased variants consistently with existing type tokens.
- [ ] Torrent search emits an extension/file-format constraint rather than a
      new `FT_FILETYPE`.
- [ ] `.torrent` files classify and display as Torrent locally.
- [ ] Existing protocol mappings for Audio, Video, Image, Document, Program,
      Archive, CD-Image, and Collection remain unchanged.
- [ ] Conservative extension additions are covered by focused classification
      tests or source checks.
- [ ] Kad extension-filter behavior remains compatible with current filename
      extension matching.

## Validation

- focused native tests for REST search type parsing and mapping
- focused classification tests for `.torrent` and reviewed extension additions
- source/UI checks proving the search file-type dropdown includes Torrent
- focused search-packet test or source check proving Torrent uses
  `FT_FILEFORMAT` and does not send `FT_FILETYPE=Torrent`
- x64 Debug and Release app builds before implementation commit
