# emulebb-rust Active Backlog

This index lists only open emulebb-rust work. GitHub Project fields and issue
milestones own workflow state and roadmap placement; each linked Markdown item
owns the durable engineering spec, constraints, acceptance criteria, and
retained evidence.

## Current Operator Hold And Work Priority (2026-11-09)

**Beta3 release is on hold.** Current work prioritizes backlog clarity and
workspace improvements for parallel multiarchitecture/multiplatform delivery,
then bugs/issues. Broader platform development is an active focus independent
of release promotion. Coordinate through
[managed workspace work (Build #28)](https://github.com/emulebb/emulebb-build/issues/28),
[platform workflow separation (#293)](https://github.com/emulebb/emulebb-rust/issues/293),
and the existing platform owners, including
[Linux x64/ARM64 (#227)](https://github.com/emulebb/emulebb-rust/issues/227) and
[Android/Fire OS (#226)](https://github.com/emulebb/emulebb-rust/issues/226).
GitHub issues and Project #3 retain workflow authority.
The `focus:workspace-platforms` label identifies the current coordination set;
it does not alter platform support or release-gate decisions. Dependency-aware
early validation [#258](https://github.com/emulebb/emulebb-rust/issues/258)
is now Major to address the feedback bottleneck without reducing complete
required validation; its milestone is unchanged.

Continue current qualification and permitted development. Do not freeze or
select a Beta3 candidate, execute candidate certification, dispatch a release
workflow, publish, tag, or bump a version while this hold applies.
[Candidate certification (#142)](https://github.com/emulebb/emulebb-rust/issues/142)
remains a future gated action until the operator explicitly lifts the hold;
[audit coordination (#268)](https://github.com/emulebb/emulebb-rust/issues/268)
owns this prioritization reconciliation. The prior Windows/Linux plus required
Linux OCI Beta3 scope remains provisional and documented; this priority change
does not silently change required checks, platform gates, support promises,
or the separate Client-to-Indexer-to-Arr phase gates.

## Current Authority

- Product scope and compatibility boundaries: [`RELEASE-SCOPE`](../RELEASE-SCOPE.md)
- Current architecture: [`architecture`](../design/architecture.md)
- Forward suite architecture: [`integrated-suite`](../design/integrated-suite.md)
- Forward REST contract: [`api/README`](../api/README.md)
- Code quality and test placement: [`CODE-QUALITY`](../reference/CODE-QUALITY.md)
- Backlog lifecycle: [`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md)
- Closed item records: [`history/items`](../history/items/INDEX.md)
- GitHub source and issues: <https://github.com/emulebb/emulebb-rust>

The current production phase is Client. Every active client item below,
including any newly accepted client item, is part of the hard gate that blocks
Indexer implementation. Indexer then blocks Arr. Priority still orders work
inside a phase; it does not allow a gated item to remain open when the next
phase begins.

Stock/community eMule owns wire behavior. Maintained eMuleBB MFC owns only
explicitly identified non-wire operational limits and disk/network I/O
outcomes. Current aMule is evidence and optimization inspiration. Rust owns the
internal async design. The machine-readable omission and extension registries
in `repos/emulebb-rust/policy` remain authoritative for approved differences.

## ID Policy

Rust item IDs use `RUST-<CLASS>-<NNN>` with `BUG`, `FEAT`, `REF`, or `CI`.
Allocate against both active and historical item directories; IDs are never
reused. Parked ideas are not backlog items until explicitly activated. The
pre-product migration item `CI-054` retains its stable ID as the only legacy
exception; new Rust items always use the `RUST-*` form.

## Beta 3 Release Placement

The following grouping distinguishes the Windows/Linux beta increment from
parallel work. Every Client item in either grouping still belongs to the
separate whole-phase Client gate described above. GitHub owns current status,
priority, and milestone placement; the index is the navigation surface.

RUST-CI-035 must implement the platform workflow split before optional jobs
stop gating the actual candidate. Existing required checks remain enforced.

## Windows/Linux Beta 3 Gate

| ID | Class | Title |
|---|---|---|
| [CI-054](items/CI-054.md) | Evidence | Add native Windows Rust/MFC protocol-parity diagnostics campaign |
| [RUST-BUG-117](items/RUST-BUG-117.md) | Bug | Expire silent Kad buddy links from received activity |
| [RUST-BUG-128](items/RUST-BUG-128.md) | Bug | Preserve incremental ED2K offer publication |
| [RUST-BUG-154](items/RUST-BUG-154.md) | Bug | Admit Kad datagrams before learning sender state |
| [RUST-BUG-155](items/RUST-BUG-155.md) | Bug | Share established peer identity and control state |
| [RUST-BUG-156](items/RUST-BUG-156.md) | Bug | Give ED2K server settings one authority |
| [RUST-BUG-159](items/RUST-BUG-159.md) | Bug | Respect destination filename limits during download delivery |
| [RUST-BUG-161](items/RUST-BUG-161.md) | Bug | Respect filesystem case semantics when consolidating shared roots |
| [RUST-BUG-164](items/RUST-BUG-164.md) | Bug | Preserve AICH trust provenance across hashset acquisition |
| [RUST-BUG-165](items/RUST-BUG-165.md) | Bug | Require trusted AICH and MD4 agreement during download verification |
| [RUST-BUG-166](items/RUST-BUG-166.md) | Bug | Admit AICH recovery answers only for matching outstanding requests |
| [RUST-BUG-176](items/RUST-BUG-176.md) | Bug | Bound URL-import responses and define destination policy |
| [RUST-BUG-178](items/RUST-BUG-178.md) | Bug | Warn before creating private diagnostic bundles |
| [RUST-BUG-181](items/RUST-BUG-181.md) | Bug | Bound RIFF media parsing and retain malformed-input regressions |
| [RUST-CI-006](items/RUST-CI-006.md) | Evidence | Refresh current-head stock parity evidence and reconcile docs |
| [RUST-CI-009](items/RUST-CI-009.md) | Evidence | Certify a Beta 3 candidate without publishing |
| [RUST-CI-034](items/RUST-CI-034.md) | Evidence | Reconcile audit findings into the Windows and Linux Beta 3 delivery scope |
| [RUST-CI-035](items/RUST-CI-035.md) | Evidence | Separate mandatory Windows/Linux gates from optional platform outcomes |

## Parallel Client Work — Non-gating for Beta 3

Dependency-aware early validation is now Major and appears first as a
workspace/platform feedback priority. Its milestone remains post-beta-polish;
current work priority does not make it a new Beta3 gate. Other platform owners
retain their Major/Minor ranking and GitHub placement.

| ID | Class | Title |
|---|---|---|
| [RUST-CI-032](items/RUST-CI-032.md) | Evidence | Add dependency-aware early Rust checks without weakening pre-push coverage |
| [RUST-BUG-136](items/RUST-BUG-136.md) | Bug | Bound transfer deletion marker validation reads |
| [RUST-BUG-160](items/RUST-BUG-160.md) | Bug | Reuse stock hashes across unambiguous Unicode filename normalization |
| [RUST-BUG-162](items/RUST-BUG-162.md) | Bug | Bound profile archive fields before allocating import buffers |
| [RUST-BUG-163](items/RUST-BUG-163.md) | Bug | Enforce exclusive process ownership of writable profiles |
| [RUST-BUG-167](items/RUST-BUG-167.md) | Bug | Release and retry failed AICH recovery requests across eligible peers |
| [RUST-BUG-168](items/RUST-BUG-168.md) | Bug | Enforce the stock incoming secure-ident public-key size limit |
| [RUST-BUG-169](items/RUST-BUG-169.md) | Bug | Honor negotiated secure-ident V2 support and LowID challenge addressing |
| [RUST-BUG-170](items/RUST-BUG-170.md) | Bug | Restore the compatible-client branch of old-client upload scoring |
| [RUST-BUG-171](items/RUST-BUG-171.md) | Bug | Reject degenerate server Diffie-Hellman public values |
| [RUST-BUG-172](items/RUST-BUG-172.md) | Bug | Omit unavailable MD4 sections from modern hashset answers |
| [RUST-BUG-173](items/RUST-BUG-173.md) | Bug | Reject file sizes outside representable ED2K hashset geometry |
| [RUST-BUG-174](items/RUST-BUG-174.md) | Bug | Require authenticated or corroborated public-IP evidence for VPN Guard |
| [RUST-BUG-175](items/RUST-BUG-175.md) | Bug | Correlate STUN mapping replies with the expected endpoint |
| [RUST-BUG-177](items/RUST-BUG-177.md) | Bug | Bound remote control-plane admission and authentication abuse |
| [RUST-BUG-179](items/RUST-BUG-179.md) | Bug | Handle malformed transfer-event frames predictably |
| [RUST-BUG-180](items/RUST-BUG-180.md) | Bug | Bound Kad tracker population under source churn |
| [RUST-BUG-182](items/RUST-BUG-182.md) | Bug | Honor ID3 flags before publishing derived text |
| [RUST-BUG-183](items/RUST-BUG-183.md) | Bug | Verify and upstream the PCP socket-initialization allocation leak |
| [RUST-CI-008](items/RUST-CI-008.md) | Evidence | Prove Unicode and long-path large-library behavior across platforms |
| [RUST-CI-028](items/RUST-CI-028.md) | Evidence | Make Windows manifest embedding target-aware |
| [RUST-CI-030](items/RUST-CI-030.md) | Evidence | Verify Rust FFI layouts against vendored C headers |
| [RUST-CI-031](items/RUST-CI-031.md) | Evidence | Consolidate deterministic eD2K and Kad protocol-parity testing |
| [RUST-CI-036](items/RUST-CI-036.md) | Evidence | Add issue and PR evidence templates |
| [RUST-CI-037](items/RUST-CI-037.md) | Evidence | Produce a read-only issue and release-readiness digest |
| [RUST-CI-038](items/RUST-CI-038.md) | Evidence | Report bundled SQLite version in build evidence |
| [RUST-CI-039](items/RUST-CI-039.md) | Evidence | Measure initial source discovery including hostname-added servers |
| [RUST-CI-040](items/RUST-CI-040.md) | Evidence | Verify download limits charge payload rather than control overhead |
| [RUST-CI-041](items/RUST-CI-041.md) | Evidence | Verify per-address limits when upload slots are immediately available |
| [RUST-FEAT-025](items/RUST-FEAT-025.md) | Feature | Validate conformant duplicate-block rejection diagnostics |
| [RUST-FEAT-038](items/RUST-FEAT-038.md) | Feature | Add current-aMule-style endgame source takeover |
| [RUST-FEAT-039](items/RUST-FEAT-039.md) | Feature | Size ED2K request depth from measured RTT and bandwidth |
| [RUST-FEAT-040](items/RUST-FEAT-040.md) | Feature | Carry ED2K and Kad search metadata end to end |
| [RUST-FEAT-048](items/RUST-FEAT-048.md) | Feature | Use sparse part files without weakening capacity reservations |
| [RUST-FEAT-056](items/RUST-FEAT-056.md) | Feature | Deliver supported Android and Fire OS APKs with device harnesses |
| [RUST-FEAT-057](items/RUST-FEAT-057.md) | Feature | Publish portable Linux musl builds for x64 and ARM64 |
| [RUST-FEAT-058](items/RUST-FEAT-058.md) | Feature | Certify NAS deployments across supported appliance systems |
| [RUST-FEAT-059](items/RUST-FEAT-059.md) | Feature | Support FreeBSD on x64 and ARM64 |
| [RUST-FEAT-060](items/RUST-FEAT-060.md) | Feature | Support ChromeOS through Android and Crostini lanes |
| [RUST-FEAT-061](items/RUST-FEAT-061.md) | Feature | Support illumos, NetBSD, and OpenBSD as portable Unix targets |
| [RUST-FEAT-062](items/RUST-FEAT-062.md) | Feature | Persist Kad routing state in SQLite and keep met files import-only |
| [RUST-FEAT-063](items/RUST-FEAT-063.md) | Feature | Carry semantic profile state into a fresh current-schema profile |
| [RUST-FEAT-064](items/RUST-FEAT-064.md) | Feature | Address unusual native paths through lossless API locators |
| [RUST-FEAT-065](items/RUST-FEAT-065.md) | Feature | Expose AICH trust integrity and recovery health to operators |
| [RUST-FEAT-066](items/RUST-FEAT-066.md) | Feature | Weight Kad user estimates by observed firewall and version ratios |
| [RUST-FEAT-067](items/RUST-FEAT-067.md) | Feature | Define supported search text syntax and rating criteria |
| [RUST-FEAT-068](items/RUST-FEAT-068.md) | Feature | Make non-Windows legacy encoding policy explicit |
| [RUST-REF-005](items/RUST-REF-005.md) | Refactor | Decompose oversized Rust modules by responsibility |
| [RUST-REF-006](items/RUST-REF-006.md) | Refactor | Consolidate Rust NAT and runtime safety internals |
| [RUST-REF-007](items/RUST-REF-007.md) | Refactor | Review Rust upload hot-path performance candidates |
| [RUST-REF-008](items/RUST-REF-008.md) | Refactor | Reduce large-library metadata and scan I/O amplification |
| [RUST-REF-009](items/RUST-REF-009.md) | Refactor | Use native storage domains for cross-platform library scheduling |
| [RUST-REF-010](items/RUST-REF-010.md) | Refactor | Bound watcher reconciliation I/O for large shared libraries |
| [RUST-REF-011](items/RUST-REF-011.md) | Refactor | Consolidate duplicated ED2K opcode and capability constants |
| [RUST-REF-016](items/RUST-REF-016.md) | Refactor | Move blocking SQLite work behind bounded async persistence |
| [RUST-REF-018](items/RUST-REF-018.md) | Refactor | Keep shared-root filesystem work outside async state locks |
| [RUST-REF-019](items/RUST-REF-019.md) | Refactor | Offload remaining transfer and large-library CPU bursts |
| [RUST-REF-020](items/RUST-REF-020.md) | Refactor | Reuse validated incoming AICH recovery proofs within bounded ownership |
| [RUST-REF-021](items/RUST-REF-021.md) | Refactor | Reduce delivery verification reads without weakening publication authority |
| [RUST-REF-022](items/RUST-REF-022.md) | Refactor | Restrict incomplete download rechecks to verified payload ranges |
| [RUST-REF-023](items/RUST-REF-023.md) | Refactor | Move fork-only PCP ownership and route integration into consumers |
| [RUST-REF-024](items/RUST-REF-024.md) | Refactor | Replace unchecked AICH geometry narrowing with bounded conversions |

## Indexer Gate

Production implementation remains blocked by every open Client item.

| ID | Class | Title |
|---|---|---|
| [RUST-FEAT-002](items/RUST-FEAT-002.md) | Feature | Indexer — autonomous Kad/eD2K observation index |

## Arr Gate

Production implementation remains blocked by the complete Indexer gate.

| ID | Class | Title |
|---|---|---|
| [RUST-FEAT-004](items/RUST-FEAT-004.md) | Feature | Arr integration — Torznab and qBittorrent compatibility adapters |
