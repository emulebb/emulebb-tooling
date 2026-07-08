# Product Portfolio & Lifecycle

Status: governance. Captured 2026-06-14. One-page map of every repo in the family:
its tier, lifecycle stage, quality bar, and where its backlog lives. Reduces the
cognitive load of a 14-repo workspace and makes ownership of each decision obvious.

## Tiers

| Tier | Meaning | Quality bar (merge gate) |
|---|---|---|
| **Core** | The strategic forward client | build + test (3-OS) + clippy `-D warnings` + cargo-deny + policy guard + leak-test |
| **Companion** | Active client/controller shipped beside Core | build + test + lint + fork hygiene + leak-test (networked) |
| **Service / Lab** | Useful but experimental; not a shipped client | green build (when promoted); narrative tracking while lab |
| **Frozen / Maintenance** | Shipping but closed to features | release proof + security/crash/packaging gates only |
| **Infra** | Build, test, docs, policy tooling | its own checks (privacy guard, docs/policy audits) |
| **Vendored-fork (build track)** | Upstream tool we package, not a product | build/validation track + nightly upstream rebase |
| **Separate family** | Adjacent product line, not the suite | out of scope here |

## The portfolio

| Repo | Tier | Stage | Backlog home | Board Product |
|---|---|---|---|---|
| `emulebb-rust` | Core | forward, Phase 0 | `docs/active` (`RUST-*`) | emulebb-rust |
| `qbittorrentbb` | Companion | active, Phase 1 | `docs/active` (`QBBB-*`) | qBittorrentBB |
| `trackmulebb` | Companion (controller + installer) | forward, Phase 2 (Python; new) | `docs/active` (`TMBB-*`) | TrackMuleBB |
| `itlezy/bountarr` | Companion (household media-grab UI) | forward, Phase 2 (TS/Node) | own repo | TrackMuleBB-suite |
| `amutorrent` | Companion (legacy) | active → freezes at 0.7.3 final | `docs/active` (`AMUT-*` ref) | aMuTorrent |
| `emulebb` (MFC) | Client (MFC) | active, 0.7.x → revived 0.8.x | `emulebb-tooling/docs/active` (legacy IDs) | eMuleBB-MFC |
| `goed2k-server` | Service / Lab | lab (no CI gate) | `docs/active` lab index (`GOED2K-*` reserved) | — (not on board while lab) |
| `emulebb-build` | Infra | active | — | tooling |
| `emulebb-build-tests` | Infra | active | — | tooling |
| `emulebb-tooling` | Infra | active | this repo | tooling |
| `emulebb-setup` | Infra | active | — | tooling |
| `amule` | Vendored-fork | build track | — | — |
| `emulebb-miniupnp` | Vendored-fork | build track | — | — |
| `emulebb-pages` / `emulebb-org-profile` | Infra (public) | active | — | — |
| `p2p-overlord-*` | Separate family | out of scope | own repos | — |

Stage notes (decision 2026-06-20):

- `amutorrent` is actively maintained and upstream-synced through the 0.7.3
  train, then deprecated and superseded by TrackMuleBB.
- `emulebb` (MFC) closes the 0.7.x line at 0.7.3, then resumes as the 0.8.x MFC
  modernization wave.

## Strategic note

The forward investment is **Core + Companion**. The historically heaviest-resourced
product (`emulebb` MFC) closes its `0.7.x` line at `0.7.3` and then **continues in
the revived `0.8.x` modernization line** (decision 2026-06-20). The forward
cross-network controller is **TrackMuleBB** (new, Python). Its first beta targets
emulebb-rust's forward `/api/v1` as a Rust Console UI; later phases add
qBittorrentBB and cross-network automation. **aMuTorrent stays actively
maintained and upstream-synced through the `0.7.3` train and freezes at `0.7.3`
final**, after which it is deprecated as a separate controller (its automation
design is retained as the TrackMuleBB reference). The bundled qBittorrentBB tracks
its latest
REST-API-compatible release rather than a pinned snapshot. The ready-to-use
**suite bundle** also pulls in third-party stacks we do **not** own — the Arr apps
(Prowlarr/Sonarr/Radarr), SABnzbd (Usenet), and Plex (Docker) — installed/wired by
TrackMuleBB but maintained upstream (see [SUITE-INSTALLER](SUITE-INSTALLER.md)). Quality investment (CI gates, leak-tests, backlog depth) should track
the tier, not history: Core/Companion get the strongest gates; the Frozen app gets
only maintenance gates; Lab gets the lightest touch until promoted.

## Lifecycle transitions

- **Lab → Service/Companion:** add the tier's full quality bar (CI build+test,
  leak-test if networked), itemize the backlog with the product prefix, and put it
  on the Suite board. (goed2k's promotion trigger lives in its lab index.)
- **Active → Frozen:** declare the final release, move to maintenance gates only,
  slim the roadmap to maintenance + family lanes (see emulebb-mfc precedent).

Related: [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md),
[QUALITY-GATES](QUALITY-GATES.md), [WORKSPACE-POLICY](../WORKSPACE-POLICY.md).
