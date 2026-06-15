# Brand & Naming

Status: governance. Captured 2026-06-15. The canonical naming convention for the
family, so pages, docs, and product copy stay consistent as the suite grows beyond
eD2K. Operator decision: **keep the "eMuleBB" name** (historical), and structure
everything around it.

## Two levels + a family token

- **Organization / house brand:** **eMuleBB** (GitHub org slug `emulebb`, unchanged).
- **The suite (umbrella term):** **eMuleBB Suite** — use this when talking about the
  cross-network whole (matches the public board "eMuleBB Suite").
- **Family token:** **`-BB`** — the shared suffix that signals "part of this family"
  (eMu­le**BB**, qBittorrent**BB**). New first-party clients take a `-BB` name where
  it reads naturally. "BB" originated as "broadband"; it is now the family mark.

## Disambiguation rule (the important one)

Always distinguish the **suite/house** from the **eD2K product**:

- **eMuleBB** (alone) = the organization / the suite / the house brand.
- **eMuleBB client** (or "eMuleBB Windows client") = the eD2K/Kad desktop product.

When there is any ambiguity, qualify the client. A BitTorrent client living under
"eMuleBB" is not odd once eMuleBB is understood as the house, not "just eMule".

## Product names

| Product | Refer to it as | Role |
|---|---|---|
| eMuleBB client | "the eMuleBB client" / "eMuleBB Windows client" | eD2K/Kad desktop (Windows; maintenance `0.7.x`) |
| emulebb-rust | "emulebb-rust" | multiplatform eD2K/Kad core (forward core) |
| qBittorrentBB | "qBittorrentBB" | BitTorrent companion |
| aMuTorrent | "aMuTorrent" (the `0.7.3` Suite controller) | cross-network web-UI controller, **frozen** on `0.7.3` (sustainability) |
| TrackMuleBB | "TrackMuleBB" (the eMuleBB Suite controller) | forward cross-network controller; Python, integrated web UI; repo `trackmulebb` |

- aMuTorrent keeps its fork name (a controller, not a `-BB` client); tag it
  "the `0.7.3` Suite controller". The forward controller is **TrackMuleBB**
  (name = tracker + mule + `-BB`; first-party, built in-house, not a fork) — tag
  it "the eMuleBB Suite controller".
- **Upstream courtesy:** qBittorrentBB and aMuTorrent are **unofficial forks** of
  qBittorrent and aMuTorrent-upstream; say so where a newcomer might confuse them
  with the upstream projects.

## Copy do / don't

- **Do:** "the eMuleBB Suite", "the eMuleBB client", "emulebb-rust (the forward
  core)", "qBittorrentBB, the BitTorrent companion".
- **Don't:** call the suite "eMule"; imply the eMuleBB client is the whole suite;
  introduce a second umbrella brand. One umbrella: **eMuleBB Suite**.

## Where this applies

- The org home (`emulebb` profile README), the marketing site (`emulebb-pages`),
  and the docs site (`site_name: eMuleBB Suite Documentation`).
- Docs IA is **centralized with per-product sections** (one MkDocs site, sections
  for eMuleBB Suite / eMuleBB Client / emulebb-rust / qBittorrentBB / aMuTorrent).
- Related: [PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md),
  [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md).
