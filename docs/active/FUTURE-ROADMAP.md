# eMuleBB Future Roadmap

This is the active post-`0.7.3` product roadmap for eMuleBB. It is not a beta
`0.7.3` release gate, and it does not promote every historical feature idea in
the backlog. The purpose is to keep future work focused on the Windows MFC app
with REST support, while making related product-family boundaries explicit and
excluding ideas that no longer match the eMuleBB desktop product direction.

## GitHub Workflow Authority

Future-roadmap workflow is GitHub-primary after migration. Promoted roadmap
slices are tracked as issues in `emulebb/emulebb` and as items in the public
`eMuleBB Roadmap` org project. Local item docs remain engineering specs and
evidence records; for files marked `workflow: github`, current status, priority,
release placement, discussion, ownership, and PR linkage live in GitHub.

Use `python scripts\github-roadmap-sync.py` from `repos\emulebb-tooling` to preview
or apply the initial GitHub import, and use
`python scripts\github-roadmap-check.py` to validate migrated metadata.

## Product Boundary

eMuleBB remains a Windows MFC desktop client with a first-class UI, tray
workflow, and in-process REST surface for controllers. Headless-only, daemon,
cross-platform, server-only, and mobile-controller product tracks belong outside
the eMuleBB desktop app.

Those tracks may still belong to the broader eMuleBB product family when the
operator explicitly promotes them. p2p-overlord is a separate Rust/Node product
in that family: it can share REST contracts, test-campaign infrastructure, and
selected dependency forks, but it does not become part of the desktop app.
See [P2P-OVERLORD-PRODUCT-FAMILY-INTEGRATION](plans/P2P-OVERLORD-PRODUCT-FAMILY-INTEGRATION.md).

## Approved Lanes

### Connectivity Modernization

Scope:
IPv6 dual-stack compatibility for the current eD2K/Kad network, NAT/LowID
relief, UPnP/PCP/NAT-PMP lease controls and status visibility, safer
bind/interface behavior, low-risk connection diagnostics, and narrowly profiled
source-hostname resolver scaling. Stock eD2K/Kad protocol semantics remain the
boundary. A distinct IPv6 Kad network remains exploratory until separately
promoted.

Existing anchors:
`FEAT-018`, `FEAT-032`, `FEAT-035`, `FEAT-036`, `FEAT-081`, `REF-030`,
`ideas/IDEA-IPV6-KAD-NETWORK.md`.

### Search And Trust Clarity

Scope:
Clearer fake-file confidence wording, Kad/search popularity and consistency
explanations, source-name divergence handling, and media plausibility checks
when evidence is local and cheap. The lane also includes opt-in remote
shared-file inventory discovery when a peer already exposes that inventory
through compatible browse/share behavior.

Existing anchors:
`FEAT-002`, `FEAT-003`, `FEAT-006`, `FEAT-031`, `FEAT-039`, `FEAT-041`,
`FEAT-078`.

### UI Power-User Polish

Scope:
Dark mode, Per-Monitor DPI, category-management polish, table/menu consistency,
keyboard-friendly workflows, preference clarity, and visible progress for
long-running startup maintenance.

Existing anchors:
`FEAT-017`, `FEAT-019`, `FEAT-062`, `FEAT-075`, `FEAT-082`.

### Startup And Storage Performance

Scope:
Compatibility-preserving startup and shared-file performance work where the
behavior remains explainable and safe under large real profiles. This includes
responsive startup maintenance, large-library startup cache cleanup, and
storage-aware shared-file hashing across independent physical volumes or SSDs,
background-safe metadata persistence, and protected-volume disk-space snapshot
refresh.

Existing anchors:
`FEAT-034`, `FEAT-072`, `FEAT-075`, `FEAT-076`, `FEAT-079`, `FEAT-080`.

### Controller Surface Performance

Scope:
REST/controller maintenance that bounds memory use and latency for large
profiles without expanding the public capability surface. Snapshot workers may
build immutable response records, but live app objects remain owned by their
normal app/UI/protocol paths.

Existing anchors:
`FEAT-068`.

### Upload Policy Clarity

Scope:
Compatibility-preserving upload/seeding policy improvements that make Broadband
behavior clearer without silently mutating user-managed state. Friend slots
remain user-directed by default; any automatic promotion must be opt-in,
diagnosable, and safe for manual Friends.

Existing anchors:
`FEAT-015`, `FEAT-023`, `FEAT-077`.

### Security And Operations

Scope:
IP-filter input policy, PeerGuardian-style imports, whitelist/private-network
policy, dependency/DLL loading hardening, diagnostics, and release-proof
automation.

Existing anchors:
`FEAT-044`, `FEAT-056`, `REF-028`, `REF-038`, `REF-039`, `REF-040`,
`REF-041`, `REF-042`.

### Product-Family Integration

Scope:
Post-`0.7.3` alignment for p2p-overlord repos, shared REST conformance, shared
campaign variants, and shared MiniUPnP source ownership without merging
products.

Existing anchors:
`FEAT-073`.

### Local State And Configuration Planning

Scope:
Evaluate local persistence changes before implementation. This includes
SQLite-backed local metadata structures, queryable auto-browse inventory
caches, and operator-editable JSON or TOML configuration where a structured
format is more robust than legacy INI text. Existing profile compatibility,
backup behavior, downgrade behavior, and stock-compatible `.met`/`.dat`
semantics remain hard constraints.

Existing anchors:
`FEAT-078`, `REF-045`, `REF-046`.

### Narrow Anti-Leecher Review

Scope:
CShield-style anti-leecher ideas only where the reasons are observable,
explainable, and low false-positive risk.

Existing anchors:
`FEAT-011`.

## Explicit Non-Goals

These ideas should not be added to the eMuleBB future backlog unless the user
explicitly reopens them:

- Headless core, server-only mode, cross-platform client work, or mobile-first
  controller scope inside the eMuleBB desktop app.
- New REST capability expansion beyond contract maintenance, drift checks, bug
  fixes, and compatibility repairs.
- Historical releaser controls such as PowerShare, Share Only The Need, release
  bonus, or default share-permission rewrites.
- Public-reachability polling as a background Connection Checker. Local and
  user-triggered diagnostics remain acceptable; the eMuleAI-style checker is
  recorded as `FEAT-083` WONT_DO.
- Startup profile-copy/import wizards that automatically mutate legacy
  profiles. The eMuleAI migration wizard is recorded as `FEAT-084` WONT_DO.
- Large-library or background-worker performance roadmap expansion outside the
  approved startup and storage performance lane.
- Metadata/file-intelligence expansion. MediaInfo remains an external DLL in
  this release line. Operator-approved local persistence planning in
  `FEAT-078`, `REF-045`, and `REF-046` is allowed only as storage/configuration
  evaluation, not as a broad metadata-intelligence feature.
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
  `emulebb/emulebb` issue and `eMuleBB Roadmap` project item before
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

## GitHub-Primary Backlog Import Set

| Lane | Scope | Items |
|---|---|---|
| Search and trust clarity | Remote shared-file inventory discovery and cached browse inspection | `FEAT-031`, `FEAT-078` |
| Local state and configuration planning | SQLite metadata and structured configuration evaluation | `REF-045`, `REF-046` |
