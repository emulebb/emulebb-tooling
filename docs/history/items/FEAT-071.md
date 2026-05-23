---
id: FEAT-071
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/23
title: Filename mojibake repair for search results and download intake
status: Done
priority: Minor
category: feature
labels: [beta-0.7.3, filenames, encoding, search, downloads, mojibake, polish]
milestone: Beta 0.7.3
created: 2026-05-21
closed: 2026-05-22
source: user request after filename encoding analysis
---

# FEAT-071 - Filename Mojibake Repair For Search Results And Download Intake

## Summary

The beta release now includes conservative filename-only repair for common
remote-intake mojibake and bounded HTML/XML entities. The repair applies before
normal filename cleanup for search result names, eD2K link add-download names,
and inherited download filename normalization paths.

## Outcome

- Added `FilenameTextRepairSeams` for bounded entity decoding and conservative
  Windows-1252/Latin-1 mojibake repair.
- Kept the repair filename-only; usernames, server names, comments,
  descriptions, arbitrary metadata, and protocol packet/tag shapes are not
  rewritten.
- Wired search result filename intake and eD2K link filename intake through the
  repair helper before existing download filename normalization.
- Kept valid accented filenames, ASCII names, unknown entities, unsafe numeric
  entities, and low-confidence broken mojibake unchanged.

## Acceptance

- [x] Common Italian and Spanish mojibake examples are repaired in unit tests.
- [x] Common Windows-1252 punctuation mojibake is repaired in unit tests.
- [x] Core and numeric HTML/XML entities are repaired in unit tests.
- [x] Plain valid accented filenames are not changed.
- [x] ASCII-only names are not changed.
- [x] Non-filename strings are not routed through the helper.
- [x] Search result and eD2K-link add-download flows keep existing behavior when
      no mojibake marker is present.
- [x] Existing invalid-character and control-character filename cleanup still
      applies after any accepted repair.

## Validation

- `python -m emule_workspace test native --suite-name parity --config Release --platform x64`
  passed on 2026-05-22 with `700` passed doctest cases, `0` failed, and
  `231` skipped.

## Implementation Commits

- App: `ec77794` (`FEAT-071 repair remote filename mojibake`)
- Build tests: `aea6f8e` (`FEAT-071 cover filename text repair`)
- Tooling: `9ca9dbf` (`FEAT-071 document filename text repair`) plus the
  release-status update that archives this item.
