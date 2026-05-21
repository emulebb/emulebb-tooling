---
id: FEAT-067
workflow: github
github_issue: https://github.com/eMulebb/eMule/issues/23
title: Filename mojibake repair for search results and download intake
status: OPEN
priority: Minor
category: feature
labels: [filenames, encoding, search, downloads, mojibake, polish]
milestone: post-beta-0.7.3
created: 2026-05-21
source: user request after filename encoding analysis
---

> Workflow status is tracked in GitHub: https://github.com/eMulebb/eMule/issues/23. This local document is retained as an engineering spec/evidence record.

## Summary

Add conservative filename-only repair for common mojibake seen in search
results, eD2K links, and download intake. The motivating cases are Western
European filenames where UTF-8 bytes were decoded as a local ANSI code page,
leaving visible sequences such as `Ã`, `Â`, and `â€` in Italian or Spanish names.

Examples:

- `cittÃ ` should display as `città`
- `EspaÃ±a` should display as `España`
- `canciÃ³n` should display as `canción`
- `Â¿QuÃ©?` should display as `¿Qué?`

## Intended Shape

Implement a small filename-specific helper, for example
`RepairMojibakeFilenameIfLikely(...)`, near the existing filename or string
conversion helpers. The helper should:

- detect strong mojibake markers before attempting repair;
- use the existing strict UTF-8 double-decode primitive as the candidate repair;
- accept the repaired name only when the marker score improves;
- reject repaired output that is empty, contains control characters, or fails
  existing filename normalization rules;
- leave names unchanged when the heuristic is not clearly beneficial.

## Candidate Hook Points

- `CAbstractFile::SetAFileName(...)` as the central display-name setter.
- Search-result `FT_FILENAME` intake before `CSearchFile` stores the visible
  name.
- eD2K file-link intake after URL/UTF-8 decoding and before creating the local
  download filename.
- Download filename normalization paths that already clean invalid filesystem
  characters.

## Scope Constraints

- Filename-only for the first implementation.
- No eD2K or Kad packet/tag shape changes.
- No global `ReadString(...)` behavior change.
- Do not rewrite usernames, server names, comments, descriptions, or arbitrary
  metadata in this slice.
- Do not rename already-shared local files silently. Local disk filenames should
  remain operator-owned unless an explicit rename flow applies the repair.
- Prefer display/intake repair over protocol reinterpretation so stock/community
  wire semantics remain unchanged.

## Acceptance Criteria

- [ ] Common Italian and Spanish mojibake examples are repaired in unit tests.
- [ ] Plain valid accented filenames are not changed.
- [ ] ASCII-only names are not changed.
- [ ] Non-filename strings are not routed through the helper.
- [ ] Search result and eD2K-link add-download flows keep existing behavior when
      no mojibake marker is present.
- [ ] Existing invalid-character and control-character filename cleanup still
      applies after any accepted repair.

## Validation

- Add focused helper tests for positive and negative examples.
- Add or update an intake-level test covering a search result or eD2K-link name.
- App implementation should rebuild `Debug|x64` and `Release|x64` through
  `python -m emule_workspace build app --variant main`.
