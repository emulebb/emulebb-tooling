# eMule BB Future Roadmap

This is the active post-`0.7.3` product roadmap for eMule BB. It is not a beta
`0.7.3` release gate, and it does not promote every historical feature idea in
the backlog. The purpose is to keep future work focused on the Windows MFC app
with REST support, while explicitly excluding ideas that belong elsewhere or no
longer match the product direction.

## GitHub Workflow Authority

Future-roadmap workflow is GitHub-primary after migration. Promoted roadmap
slices are tracked as issues in `eMulebb/eMule` and as items in the public
`eMule BB Roadmap` org project. Local item docs remain engineering specs and
evidence records; for files marked `workflow: github`, current status, priority,
release placement, discussion, ownership, and PR linkage live in GitHub.

Use `python scripts\github-roadmap-sync.py` from `repos\eMule-tooling` to preview
or apply the initial GitHub import, and use
`python scripts\github-roadmap-check.py` to validate migrated metadata.

## Product Boundary

eMule BB remains a Windows MFC desktop client with a first-class UI, tray
workflow, and in-process REST surface for controllers. Headless-only, daemon,
cross-platform, server-only, and mobile-controller product tracks belong outside
eMule BB, including future Rust `p2p-overlord` work.

## Approved Lanes

| Lane | Scope | Existing anchors |
|------|-------|------------------|
| Connectivity modernization | IPv6 dual-stack compatibility for the current eD2K/Kad network, NAT/LowID relief, safer bind/interface behavior, and low-risk connection diagnostics, while preserving stock eD2K/Kad protocol semantics. A distinct IPv6 Kad network remains exploratory until separately promoted. | `FEAT-032`, `FEAT-035`, `FEAT-036`, `ideas/IDEA-IPV6-KAD-NETWORK.md` |
| Search and trust clarity | Clearer fake-file confidence wording, Kad/search popularity and consistency explanations, source-name divergence handling, filename encoding repair, and media plausibility checks when evidence is local and cheap. | `FEAT-002`, `FEAT-003`, `FEAT-006`, `FEAT-039`, `FEAT-041`, `FEAT-071` |
| UI power-user polish | Dark mode, Per-Monitor DPI, category-management polish, table/menu consistency, keyboard-friendly workflows, and preference clarity. | `FEAT-017`, `FEAT-019`, `FEAT-062` |
| Security and operations | IP-filter input policy, PeerGuardian-style imports, whitelist/private-network policy, dependency/DLL loading hardening, diagnostics, and release-proof automation. | `FEAT-044`, `FEAT-056`, `REF-028`, `REF-038`, `REF-039`, `REF-040`, `REF-041`, `REF-042` |
| Narrow anti-leecher review | CShield-style anti-leecher ideas only where the reasons are observable, explainable, and low false-positive risk. | `FEAT-011` |

## Explicit Non-Goals

These ideas should not be added to the eMule BB future backlog unless the user
explicitly reopens them:

- Headless core, server-only mode, cross-platform client work, or mobile-first
  controller scope.
- New REST capability expansion beyond contract maintenance, drift checks, bug
  fixes, and compatibility repairs.
- Historical releaser controls such as PowerShare, Share Only The Need, release
  bonus, or default share-permission rewrites.
- Large-library or background-worker performance roadmap expansion beyond
  already-active hardening work.
- Metadata/file-intelligence expansion. MediaInfo remains an external DLL in
  this release line.
- Bundled MediaInfo, Windows Property Store expansion, or webservice metadata
  growth.
- Protocol forks, proprietary Kad/eD2K extensions, opcode or packet/tag shape
  changes, Kad state-machine drift, or broad transport rewrites that cannot be
  validated against current community semantics.
- Distinct IPv6 Kad network behavior in the current roadmap lane. The approved
  lane is dual-stack compatibility on the current network; the separate IPv6
  Kad network design stays in `docs/ideas/IDEA-IPV6-KAD-NETWORK.md` until
  explicitly promoted.

## Evidence Used

Local references:

- `analysis\emuleai\Release_Notes.txt`
- `analysis\emuleai\srchybrid`
- `docs\ideas\IDEA-MODERNIZATION-2026.md`
- `docs\history\reviews\REVIEW-2026-04-20-feature-expansion-beyond-stock.md`
- `docs\history\reviews\REVIEW-2026-04-26-emuleai-mods-broadband-scan.md`

External references used as directional signals, not implementation authority:

- [eMule Qt](https://emule-qt.org/)
- [eMule Qt 2026 announcement](https://emule-qt.org/2026/03/05/hello-emule-2026/)
- [MorphXT feature FAQ](https://wiki.emule-web.de/Morphxt_faq)
- [ScarAngel feature FAQ](https://scarangel.sourceforge.net/eng_faq.html)
- [eMule feature category wiki](https://wiki.emule-web.de/Category%3AFeatures)
- [irwir eMule releases](https://github.com/irwir/eMule/releases/)
- [aMule FAQ](https://wiki.amule.org/wiki/FAQ_aMule)
- [BEP 32: IPv6 extension for DHT](https://www.bittorrent.org/beps/bep_0032.html)
- [libtorrent DHT reference](https://libtorrent.org/reference-DHT.html)
- [libtorrent settings reference](https://libtorrent.org/reference-Settings.html)

## Promotion Rules

- This roadmap is grouped intentionally. Do not create a new detailed `FEAT-*`
  file from a lane until the user approves that specific slice.
- After GitHub migration, a promoted future-roadmap slice must have a
  `eMulebb/eMule` issue and `eMule BB Roadmap` project item before
  implementation starts.
- Before implementation, revalidate the slice against current `main`, current
  dependency pins, and `WORKSPACE-POLICY.md`.
- Prefer narrow, observable improvements over broad behavioral rewrites.
- Keep stock/community behavior intact unless the feature explicitly documents
  the product reason for drift.
- Any promoted slice must define targeted validation before implementation
  starts.
- qBittorrent/libtorrent can inform dual-stack architecture, but BitTorrent DHT
  mechanics are not eMule Kad protocol authority.
