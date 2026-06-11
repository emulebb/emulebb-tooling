---
id: FEAT-118
workflow: local
github_issue:
title: Composite Confidence indicator replacing the Risk + Kad-Confidence columns
status: DONE
priority: Minor
category: feature
labels: [ui, search, downloads, fake-detection, rest, localization, 0.8.x]
milestone: 0.8.0
created: 2026-06-11
source: 2026-06-11 operator review of the search/download "Risk" column + eMuleAI/beba comparison
---

## Problem

The search/download **"Risk"** column (`IDS_SEARCH_TRUST`) shows only the
`FakeFileDetector` verdict (OK/Caution/Warning/High-risk/Spam), and a *separate*
**"Kad Confidence"** column (`IDS_SEARCH_KAD_TRUST`) shows publisher consistency.
The name is negative-only, the two columns fragment one concept, the single tier
hides the reasons, and there is no positive "looks legit" end. Comparison: beba's
`AntiFake` "FakeAlyzer" (Good->Fake) and eMuleAI's 6-level rating both expose a
positive end; eMuleBB's existing detector is otherwise richer (header-magic, AICH
consensus, masquerade) than either mod.

## Decision / scope

- Collapse both columns into one **"Confidence"** column with a symmetric scale
  **Genuine / Looks good / Caution / Suspect / Likely fake / Spam** (+ 0-100 score),
  composing fake heuristics + user ratings + Kad publisher confidence.
- **REST consolidation with no legacy shims:** replace `riskEvidence` +
  `kadPublisherEvidence` with one `confidence` object `{band, score, reasons}`
  (breaking, acceptable pre-1.0). `availabilityEvidence` stays separate.
- Borrow **one** signal from beba: `name_media_tag_mismatch` (filename vs the
  result's own embedded `FT_MEDIA_ARTIST/ALBUM/TITLE`), a Low soft signal. DRM-codec
  signal intentionally not borrowed.
- UI + REST presentation + localization only; **no eD2K/Kad wire change** (no
  protocol parity required). Detection heuristics otherwise unchanged.

## Key files

- `srchybrid\SearchTrustHintSeams.h` (composite), `srchybrid\FakeFileDetectorSeams.h`
  (+`name_media_tag_mismatch`), `srchybrid\FakeFileDetector.cpp` (evidence + format),
  `srchybrid\SearchListCtrl.cpp`, `srchybrid\DownloadListCtrl.cpp`,
  `srchybrid\WebServerJson.cpp`, `srchybrid\emule.rc` + 43 `lang\*.rc`.
- Docs: `docs\rest\REST-API-OPENAPI.yaml`, `REST-API-CONTRACT.md`,
  `REST-API-PARITY-INVENTORY.md`.

## Acceptance criteria

- One "Confidence" column in search + downloads with the 6-level scale, correct
  sort, infotip carrying fake reasons + Kad detail; Kad Confidence column gone;
  saved layouts intact.
- REST search returns consolidated `confidence`; old fields removed; OpenAPI/contract
  drift gate green; aMuTorrent/adapters still parse results.
- `name_media_tag_mismatch` fires only when embedded media tags are absent from the
  filename.
- All 43 stock languages carry the new labels; `rc-localization-preflight.py` green.
- Debug|x64, Release|x64, Release|x64 diagnostics build clean; seam + REST tests pass.

## Outcome (2026-06-11)

- Seam: `SearchTrustHintSeams::ConfidenceLevel`/`ConfidenceHint` +
  `BuildConfidenceHint`/`CompareConfidenceHints`/`ConfidenceToken`; borrowed
  `name_media_tag_mismatch` added to `FakeFileDetectorSeams::Analyze` (fires only
  when a >=4 char embedded `FT_MEDIA_ARTIST/ALBUM/TITLE` tag is absent from every
  observed filename).
- UI: search collapses `Risk`+`Kad Confidence` into one `Confidence` column
  (col 14, AICH renumbered 14->15->15); downloads `Risk`->`Confidence`; view-preset
  order/hidden-column arrays and saved-layout indices migrated.
- REST: `riskEvidence` + `kadPublisherEvidence` removed (no shims); single
  `confidence` object `{band, score, fakeScore, severity, spam, userRating, kadBand,
  reasons}`; OpenAPI `SearchConfidence` schema + contract updated; Rust REST stub
  and the fake-kad-trust soak script/tests updated.
- Localization: 9 new IDS (`IDS_CONFIDENCE*` + `IDS_FAKEFILE_REASON_NAME_MEDIA_TAG_MISMATCH`)
  in `emule.rc` + all 43 stock `lang\*.rc` via `rc-translate-missing.py`; required-id
  and identical-ok (`Spam`/`Suspect` loanwords) manifests updated; preflight green.
- Verification: Debug/Release/Release-diagnostics x64 builds clean; native doctest
  (916 cases) + python harness (1333) pass; `validate` green (REST drift, localization,
  taxonomy, normalization, warning policy).
