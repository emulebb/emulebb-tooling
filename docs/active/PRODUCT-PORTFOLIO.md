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
| `amutorrent` | Companion (controller) | active, Phase 2 | `docs/active` (`AMUT-*`) | aMuTorrent |
| `emulebb` (MFC) | Frozen / Maintenance | closes 0.7.3 → 0.7.x | `emulebb-tooling/docs/active` (legacy IDs) | eMuleBB-MFC |
| `goed2k-server` | Service / Lab | lab (no CI gate) | `docs/active` lab index (`GOED2K-*` reserved) | — (not on board while lab) |
| `emulebb-build` | Infra | active | — | tooling |
| `emulebb-build-tests` | Infra | active | — | tooling |
| `emulebb-tooling` | Infra | active | this repo | tooling |
| `emulebb-setup` | Infra | active | — | tooling |
| `amule` | Vendored-fork | build track | — | — |
| `emulebb-miniupnp` | Vendored-fork | build track | — | — |
| `emulebb-pages` / `emulebb-org-profile` | Infra (public) | active | — | — |
| `p2p-overlord-*` | Separate family | out of scope | own repos | — |

## Strategic note

The forward investment is **Core + Companion**. The historically heaviest-resourced
product (`emulebb` MFC) is **Frozen** — its CI and 127-item backlog are maintenance,
not growth. Quality investment (CI gates, leak-tests, backlog depth) should track
the tier, not history: Core/Companion get the strongest gates; the Frozen app gets
only maintenance gates; Lab gets the lightest touch until promoted.

## Lifecycle transitions

- **Lab → Service/Companion:** add the tier's full quality bar (CI build+test,
  leak-test if networked), itemize the backlog with the product prefix, and put it
  on the Suite board. (goed2k's promotion trigger lives in its lab index.)
- **Active → Frozen:** declare the final release, move to maintenance gates only,
  slim the roadmap to maintenance + family lanes (see eMuleBB MFC precedent).

Related: [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md),
[QUALITY-GATES](QUALITY-GATES.md), [WORKSPACE-POLICY](../WORKSPACE-POLICY.md).
