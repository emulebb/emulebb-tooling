# Product Portfolio & Lifecycle

Status: governance. Captured 2026-06-14. One-page map of every repo in the family:
its tier, lifecycle stage, quality bar, and where its backlog lives. Reduces the
cognitive load of a 14-repo workspace and makes ownership of each decision obvious.

## Tiers

| Tier | Meaning | Quality bar (merge gate) |
|---|---|---|
| **Core** | The strategic forward client | build + test (3-OS) + clippy `-D warnings` + cargo-deny + policy guard + leak-test |
| **Companion** | Future client/controller staged beside Core | build + test + lint + fork hygiene + leak-test (networked) |
| **Service / Lab** | Useful but experimental; not a shipped client | green build (when promoted); narrative tracking while lab |
| **Frozen / Maintenance** | Shipping but closed to features | release proof + security/crash/packaging gates only |
| **Infra** | Build, test, docs, policy tooling | its own checks (privacy guard, docs/policy audits) |
| **Vendored-fork (build track)** | Upstream tool we package, not a product | build/validation track + nightly upstream rebase |
| **Separate family** | Adjacent product line, not the suite | out of scope here |

## The portfolio

| Repo | Tier | Stage | Backlog home | Board Product |
|---|---|---|---|---|
| `emulebb-rust` | Core | forward, Phase 0 | `docs/active` (`RUST-*`) | emulebb-rust |
| `qbittorrentbb` | Companion | future, Phase 1 | `docs/active` (`QBBB-*`) | qBittorrentBB |
| `trackmulebb` | Companion (controller + installer) | parked, Phase 2 (Python; new) | `docs/active` (`TMBB-*`) | TrackMuleBB |
| `itlezy/bountarr` | Companion (household media-grab UI) | parked, Phase 2 (TS/Node) | own repo | TrackMuleBB-suite |
| `amutorrent` | Companion (legacy) | frozen with 0.7.3 | `docs/active` (`AMUT-*` ref) | aMuTorrent |
| `emulebb` (MFC) | Client (MFC) | frozen 0.7.x maintenance | `emulebb-tooling/docs/active` (legacy IDs) | eMuleBB-MFC |
| `goed2k-server` | Service / Lab | lab (no CI gate) | `docs/active` lab index (`GOED2K-*` reserved) | — (not on board while lab) |
| `emulebb-build` | Infra | active | — | tooling |
| `emulebb-build-tests` | Infra | active | — | tooling |
| `emulebb-tooling` | Infra | active | this repo | tooling |
| `emulebb-setup` | Infra | active | — | tooling |
| `amule` | Vendored-fork | build track | — | — |
| `emulebb-miniupnp` | Vendored-fork | build track | — | — |
| `emulebb-pages` / `emulebb-org-profile` | Infra (public) | active | — | — |
| `p2p-overlord-*` | Separate family | out of scope | own repos | — |

Stage notes (decision 2026-07-12):

- `emulebb-rust` is the active forward lane: headless client stabilization plus
  Rust-native UI.
- `emulebb` (MFC) closes the 0.7.x line at 0.7.3 and stays frozen except for
  critical maintenance plus non-behavior-expanding diagnostics/instrumentation.
- `amutorrent` freezes with the 0.7.3 Windows suite.
- `qbittorrentbb` is future companion work; `trackmulebb` is parked until that
  companion work progresses.

## Strategic note

The forward investment is **Core first**. The historically heaviest-resourced
product (`emulebb` MFC) closes its `0.7.x` line at `0.7.3` and is now frozen.
Current development concentrates on `emulebb-rust` headless client stability and
Rust-native UI. qBittorrentBB is the later BitTorrent companion; TrackMuleBB is a
parked future controller/integration layer, not a Rust beta dependency and not an
MFC integration path. The ready-to-use **suite bundle** remains a future design
reference (see [SUITE-INSTALLER](SUITE-INSTALLER.md)). Quality investment (CI
gates, leak-tests, backlog depth) should track the tier and active lifecycle:
Core gets the strongest gates; the Frozen app gets only maintenance gates; Lab
gets the lightest touch until promoted.

## Lifecycle transitions

- **Lab → Service/Companion:** add the tier's full quality bar (CI build+test,
  leak-test if networked), itemize the backlog with the product prefix, and put it
  on the Suite board. (goed2k's promotion trigger lives in its lab index.)
- **Active → Frozen:** declare the final release, move to maintenance gates only,
  slim the roadmap to maintenance + family lanes (see emulebb-mfc precedent).

Related: [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md),
[QUALITY-GATES](QUALITY-GATES.md), [WORKSPACE-POLICY](../WORKSPACE-POLICY.md).
