# eD2K Inventory Methodology

[← Back to the eD2K inventory dashboard](../ED2K-PROJECT-INVENTORY.md)

The inventory is a research index, not an endorsement list. Activity, public adoption, maturity, protocol role, licensing, and strategic relevance are separate signals. A high-adoption project can still be protocol-incomplete or harmful to network contribution.

## Status Labels

| Status | Meaning |
|---|---|
| Active | Recent or ongoing development is visible, or the project is owned by this workspace. |
| Maintained | Usable and periodically maintained, but not necessarily fast-moving. |
| Stale | Source exists, but no current development was apparent during review. |
| Historical | Important for provenance or protocol behavior, but no longer a current project. |
| Archive-only | Local or public archive evidence exists; upstream may be gone or binary-only. |
| Needs verification | Name or lead is useful, but source, license, or project identity still needs confirmation. |

## Colored Markers

| Marker | Meaning |
|---|---|
| 🟢 | Active, maintained, established, or visibly current. |
| 🟡 | Visible but requiring verification, or a medium-strength signal. |
| ⚪ | Niche public adoption. |
| 🟣 | Archive/reference material. |
| ⚫ | Historical or stale lead. |
| 🔴 | Capability or network-contribution warning. |
| ❔ | Public evidence is unavailable or insufficient. |

## Activity And Adoption Ranking

1. **Active with visible adoption:** current projects with established or visible public adoption.
2. **Active or maintained, niche adoption:** current projects with small or unknown public adoption.
3. **Experimental or verification required:** incomplete, early, ambiguous, or independently unverified projects.
4. **Stale or historical:** projects without current maintenance evidence.
5. **Capability warning:** verified download-only clients that do not contribute uploads.

Within a live-project tier, entries sort by latest verified release or default-branch activity, then public adoption, then project name. GitHub stars and forks are discovery and visibility proxies only; they are not active-user counts.

| Adoption badge | Default evidence |
|---|---|
| 🟢 Established | At least 500 GitHub stars, or independently visible broad ecosystem use. |
| 🟡 Visible | 50–499 GitHub stars, or multiple verifiable integrations/distribution channels. |
| ⚪ Niche | Fewer than 50 GitHub stars with a verifiable public repository. |
| ❔ Unknown | No reliable public adoption measure was available. |

## Historical Ranking

1. **Preservation A:** maintained or accessible public source/archive evidence.
2. **Preservation B:** named source or archive evidence with weaker reproducibility.
3. **Preservation C:** partial mirrors, local-only evidence, or unverified public leads.

## Capability Classification

Download-only and non-contributing clients remain visible because they affect ecosystem behavior and competitive visibility. They receive a red warning and are excluded from healthy-peer rankings. Classification is based on documented behavior, source review, or verified runtime evidence—not project origin or developer nationality.

## Refresh Workflow

A future inventory refresh must:

1. Read the scoped AGENTS.md in this directory before editing inventory files.
2. Search public sources and local research archives for new servers, clients, controllers, libraries, and preservation leads.
3. Recheck canonical URLs, redirects, archive state, default branches, release dates, license signals, and available CI checks.
4. Treat project-authored claims as claims until confirmed by source review, retained traces, or independent live evidence.
5. Update the dated snapshot for every changed statistic and leave unknown values explicit.
6. Reapply activity, adoption, maturity, relevance, and participation classifications using this page.
7. Recount category totals, status mixes, and adoption mixes, then update the dashboard total from the current 130-entry baseline.
8. Preserve the dashboard path and category anchors; update MkDocs navigation and cross-links when adding pages.
9. Run documentation validation and a MkDocs build before delivery.
10. Do not commit, push, merge, or change PR state unless the current user request explicitly authorizes it.

## Original Maintenance Procedure

Refresh this inventory when a new eD2K/eMule-related repo is discovered or before
using any project as implementation evidence.

1. Search both public sources and local research archives.
2. Classify server implementations separately from server lists, bootstrap
   services, protocol libraries, clients, controllers, and mods.
3. Prefer canonical upstream URLs. If only a local checkout exists, keep the
   entry as needs verification until an upstream, archive, or provenance link
   is found.
4. Record closed-source historical servers as protocol/history evidence only.
5. Validate whether source, binary archive, license, and protocol coverage are
   actually present before changing status from needs verification.
6. Keep rows concise and factual. Do not add marketing claims or endorsement
   language.
7. Distinguish native eD2K/Kad implementations from wrappers around eMule,
   aMule, `goed2k`, or link handlers.
8. Give every detailed entry one status marker, then recount the linked project
   index before committing.

Recommended recurring searches:

```text
ed2k server github
eDonkey server source code
Lugdunum eserver archive
satan-edonkey-server source
node ed2k server github
go ed2k server github
java ed2k server github
emule mod source archive
MorphXT Xtreme ScarAngel StulleMule Mephisto source
VeryCD easyMule source
eMule EastShare Sivka iONiX Phoenix TK4 source
Torznab ed2k eMule
aMule Sonarr Radarr ed2k
aMuTorrent TransMule Mularr aMulerr amarr aMule Nuxt TauriMule goed2kd
Gopeed FluxDown Kelpie AmuleD Mulee nodemule ed2k
aMule Android Preview aMule Remote aMule Modern aMularr aMulio
eMule Kad extraction eNodeMeta eMule HTTP cache aMule EC profiler
JEmuleServer goed2k-server ED2K server
ed2k hash library Rust Ruby Go
site:github.com ed2k pushed after current year
site:github.com eMule Kad pushed after current year
site:github.com "Kad2" "eMule" "Rust"
site:gitlab.com ed2k eMule Kademlia
site:codeberg.org ed2k eMule Kademlia
OP_LOGINREQUEST OP_OFFERFILES GitHub pushed after current year
eMule Security ed2k-rust main server andrey23127
andrey23127 ed2k-server Rust
rucio eMule Kad2 Rust
eMule 0.72a community stable
emule-qt GitHub
ModderMule eNode-go eMule Qt
Ember-P2P eMule Next padMule
Python-eD2k ged2k jed2k jaMule
KadGlobe eMule Kademlia
aMule WebUI template ed2k
HydraP2P Sharing-Devils eD2K I2P
shortypower eD2K ServerList
```

After editing, run:

```powershell
git diff --check
rg -n "ED2K-PROJECT-INVENTORY" EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs
```

Run `python -m emule_workspace validate` when the workspace lock is free.
