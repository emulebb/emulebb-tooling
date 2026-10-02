# emulebb-rust 0.1.0-beta.1 Release Evidence Checklist

This is the single operator checklist for the `rust-v0.1.0-beta.1` candidate.
The selected Rust commit is immutable for this evidence cycle. Any product or
release-workflow change selects a new candidate and invalidates the evidence
below.

**F1 review result (2026-10-02): NO-GO for tag or publication.** Hosted CI,
non-publishing packages, deterministic Windows certification, package/SBOM
verification, and the fail-closed Gluetun proof are green on the selected
candidate. Exact-candidate public delivery is not green: the Windows bounded
probe was inconclusive and the one-hour WSL completion campaign received 50.7%
of the approved ISO before public sources stopped serving it. No tag, GitHub
prerelease, or GHCR publication is authorized by this checklist.

## Candidate Identity

| Component | Selected revision | Purpose |
|---|---|---|
| `emulebb-rust` | [`28a0703561f135b03ffcca94527ceb538ef9012e`](https://github.com/emulebb/emulebb-rust/commit/28a0703561f135b03ffcca94527ceb538ef9012e) | Immutable beta product candidate |
| `emulebb-build` | [`80e2a1cae4cdd1b56ffba75685466c1f4ceabe12`](https://github.com/emulebb/emulebb-build/commit/80e2a1cae4cdd1b56ffba75685466c1f4ceabe12) | Orchestration and packaging |
| `emulebb-build-tests` (hosted workflow) | [`ecd19103d4a3bab615d47b89d195594501d7b0b4`](https://github.com/emulebb/emulebb-build-tests/commit/ecd19103d4a3bab615d47b89d195594501d7b0b4) | Package, image, and hosted smoke harnesses pinned by the candidate workflow |
| `emulebb-build-tests` (final Gluetun proof) | [`d59fc89ac8b4090a262d0fc63ea27e84ad3742ba`](https://github.com/emulebb/emulebb-build-tests/commit/d59fc89ac8b4090a262d0fc63ea27e84ad3742ba) | Evidence-only compatibility update for the candidate's automatic first-run networking |
| `emulebb-tooling` | [`8035fc8ad161917bdaf97306e0c4a41eebe52437`](https://github.com/emulebb/emulebb-tooling/commit/8035fc8ad161917bdaf97306e0c4a41eebe52437) | Frozen release notes, changelog, and OpenAPI contract embedded in package provenance |

The final harness update does not change the Rust product candidate or any
hosted artifact. It makes the Gluetun proof observe the consumer-default
automatic eD2K/Kad startup instead of issuing redundant explicit connect calls.
Its focused test suite passed 5/5 before the proof and commit.

## Final Evidence

- [x] Candidate identity is selected, pushed, and pinned by full commit SHA in
  the CI and release workflows.
- [x] Hosted CI succeeded for the selected candidate:
  [workflow run 36980088250](https://github.com/emulebb/emulebb-rust/actions/runs/36980088250).
  Policy/format/Clippy, cargo-deny, Windows/Linux/macOS build and test, and live
  REST/OpenAPI conformance all passed on `28a0703561f135b03ffcca94527ceb538ef9012e`.
- [x] The manually dispatched, non-publishing release workflow succeeded for
  the selected candidate:
  [workflow run 36980108964](https://github.com/emulebb/emulebb-rust/actions/runs/36980108964).
  All native package jobs and the two-architecture OCI candidate passed; tag-only
  publication jobs were correctly skipped.
- [x] The exact-candidate deterministic Windows campaign succeeded. Campaign
  `20261002T074738Z-emulebb-rust-overnight` passed 7/7 commands. Report:
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\\reports\\release-campaign-runs\\20261002T074738Z-emulebb-rust-overnight\\release-campaign-run-result.json`;
  SHA-256 `dd8567d3910b850ed2dfa586a83900e8c908957eed8f50842e5e9b159ec0cb0e`.
- [ ] The exact-candidate Windows public-delivery gate succeeds. Campaign
  `20261002T082954Z` was **inconclusive** after its ten-minute bound. It reached
  HighID, connected eD2K and Kad, found nine sources, received 174,452,736
  payload bytes including 5,021,696 stock-identified bytes, recorded 7,221
  diagnostics with zero error events, and shut down gracefully, but did not
  complete the approved ISO. Report:
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\\reports\\rust-windows-direct-smoke\\20261002T082954Z\\report.json`;
  SHA-256 `412b5a473a644ebb053460e060cf417f782185ac4c6f51644c192b19ca1acd1e`.
- [ ] The exact-candidate WSL public-delivery gate succeeds. Campaign
  `20261002T085321Z` **failed** its one-hour completion gate after receiving
  1,411,383,296 of 2,785,017,856 bytes (50.7%). It connected eD2K and Kad,
  observed up to 12 sources, attributed every accepted byte to a
  stock-identifying peer, recorded 39,234 diagnostics across all three schemas
  with zero error events, and shut down gracefully. The approved ISO did not
  complete, so no size/SHA-256 delivery pass is claimed. Report:
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\\reports\\rust-linux-direct-smoke\\20261002T085321Z\\report.json`;
  SHA-256 `33ae6bd7a92ae616574f1f21c7d1bfdc2a20e9c0020953525c4fc57f787d7eeb`.
- [x] The fail-closed Gluetun proof succeeded for the hosted OCI archive; see
  the dedicated section below.
- [x] All eight native release packages come from the selected candidate and
  their SHA-256 hashes are recorded below.
- [x] Every package manifest identifies the selected Rust, build, and tooling
  revisions. Recomputed package and SBOM hashes match every manifest field;
  manifest hashes are independently recorded below.
- [x] `emulebb-rust`, `emulebb-build`, `emulebb-build-tests`, and
  `emulebb-tooling` are clean and synchronized with their remotes at final
  review.
- [x] Final operator-facing release text is frozen in
  [release notes](../RELEASE-0.1.0-beta.1-NOTES.md) and the
  [changelog](../RELEASE-0.1.0-beta.1-CHANGELOG.md) at tooling revision
  `8035fc8ad161917bdaf97306e0c4a41eebe52437`.
- [x] No unresolved beta-blocking security finding remains. Hosted cargo-deny
  passed. The open high-severity `pymdown-extensions` Dependabot alert affects
  the MkDocs-only `requirements-docs.txt` toolchain, is not shipped in Rust
  packages or images, and is classified as non-blocking follow-up maintenance.
- [ ] Final release go is granted. This remains blocked on fresh
  exact-candidate Windows and WSL public campaigns that satisfy completed
  approved delivery, size/SHA-256 verification, stock-identifying accepted
  bytes, clean diagnostics, and graceful teardown.

Earlier passing public campaigns from other Rust commits are not reused here.

## Gluetun Fail-Closed Proof

Proof `20261002T084942Z` used the hosted multi-architecture OCI archive from
release run `36980108964`, Gluetun `qmcgaw/gluetun:v3.41.3`, and the retained
read-only operator VPN fixture. The report is
`${EMULEBB_WORKSPACE_OUTPUT_ROOT}\\reports\\rust-gluetun-proof\\20261002T084942Z.json`,
SHA-256 `f5f4b2a0d546f01542ed0c35bc46c8c94b87dcccd2ed0c3b76cfa5128a8d7989`.

- The OCI archive SHA-256 was
  `997ab96c12a13b93a2f99dd1f54a0cf7dace914c582f3e1caa9e327cfb1e2fb4`.
- The in-image executable SHA-256 was
  `dd16801e0e4213bf4ef99917e30af22b5866c8cca2c50de15b1d5e418556e115`,
  exactly matching the executable extracted from the hosted Linux amd64 DEB.
- Gluetun was healthy; Rust was pinned to `tun0`; automatic first-run eD2K and
  Kad connectivity succeeded; and the positive host sensor observed tunneled
  P2P traffic.
- After Gluetun stopped, Rust remained alive with only `lo`; namespace-local
  REST remained responsive while host-published REST became unreachable.
- The retained 24-byte empty PCAP recorded zero off-tunnel packets:
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\\reports\\rust-gluetun-proof\\20261002T084942Z.off-tunnel.pcap`,
  SHA-256 `e3f42e2687636327d7f18c9635173252505b4a838fa6829a755bab06c9c69749`.
- Test containers, networks, volumes, and the isolated Compose project were
  removed; pre-existing Compose projects were preserved.

## Package, Manifest, and SBOM Hashes

| Asset | Asset SHA-256 | Manifest SHA-256 | SBOM SHA-256 |
|---|---|---|---|
| `emulebb-rust-v0.1.0-beta.1-linux-aarch64.AppImage` | `3bb7ef8a59add76bf2339e4d5fd825755e5668e5835047da3a7a5b5ed4bb9628` | `6d90c30b14655e068a2019ad13cab9897e8c4522ae374db8702151695462420e` | `dbebfc147e049b21b80fa6056a44789e25e777ccf88d32f8082f3ffb2a80e678` |
| `emulebb-rust-v0.1.0-beta.1-linux-arm64.deb` | `388ce4bc896c8227a17505d4ccc1147d6925f1381052fae53cd62d9888dfbed1` | `07dcd7d2df6fc272b7cbdc0128e2cc79c045a21814f0b7f7c9148f1047c56aca` | `dbebfc147e049b21b80fa6056a44789e25e777ccf88d32f8082f3ffb2a80e678` |
| `emulebb-rust-v0.1.0-beta.1-linux-amd64.deb` | `a30096457a7f3caf693d4bf4d3f8bb3c4a6126b45a226e6edbf21b5924c91d49` | `54a8b69c2141f1d1962d8d6941b05a0d840a84a6ef099b1cfd3a9f2beceb2a65` | `53a011b3288d8c5537601ee80247bb2b89e8b7cb7c906d2a62b458769d35a6b9` |
| `emulebb-rust-v0.1.0-beta.1-linux-x86_64.AppImage` | `2f3cd1abf86b3deaea329506da62f916bb66a0dcc3830a895148436c156b5724` | `5b63504a0e5588797032dc23fd00638d673067f17c362d3bf9013b3c5088e08a` | `53a011b3288d8c5537601ee80247bb2b89e8b7cb7c906d2a62b458769d35a6b9` |
| `emulebb-rust-v0.1.0-beta.1-macos-arm64.dmg` | `a7848c0e3136d4023204c79b2c38a6c1b041730e0de3e84708b8e54f9b5fd003` | `7c7129091fe6ad395ffe61f3afae9520a3e73702df77f182fa3ba73cfdd58e8d` | `9ff88407026676a74c3974c83b9deb2fd3ccdfe24f4eb9618fb863cda2dca597` |
| `emulebb-rust-v0.1.0-beta.1-macos-x64.dmg` | `f2259d302a43945b930011c307f17ca08e8706e2eca663da1256919f0f1a2af4` | `ae737f2c854b482f1efd4ea23fe22ff069f18b833e9458cf386ba9cf8b4f7552` | `fccb1c56dbb4aebe90717da19966db949e30520198e38aed69f09892fe98144a` |
| `emulebb-rust-v0.1.0-beta.1-windows-arm64.zip` | `0742ee15cc4c3caf794244ce965c1ad084464c4ff89542278b41d500799ae05f` | `8f339bfdd53eb4dc6c3c75bf96a575d0af86ce867c57cfc68e73585633d3b4cd` | `19a0e3b350dc5acbf13ad3ec026c266fb967f9563b74afbcfd6a1e9fe9848b9a` |
| `emulebb-rust-v0.1.0-beta.1-windows-x64.zip` | `8a5d463ac2ca04a2954a17e8bbfeceb742d01e2977913ceb3a9fb6afda90e843` | `89019bd1e429a3493397c935ebd968e20d353be9bca230c3fda0e32d793d553c` | `3429f32fe384ee61d94e7547e6dd35fa76f211d1c53e8aac4959c23ae7b17390` |

The Linux architecture pairs intentionally share one SBOM per architecture.
The tagged workflow must generate and verify the combined `SHA256SUMS` before
publication; a combined sums file is not emitted by this non-publishing manual
run.

## Repository State

At final review, `main == origin/main` with an empty worktree for the Rust,
build, build-tests, and tooling repositories. The candidate Rust SHA remains
`28a0703561f135b03ffcca94527ceb538ef9012e`; the evidence-only build-tests HEAD
is `d59fc89ac8b4090a262d0fc63ea27e84ad3742ba`. The tooling HEAD that contains
this checklist is evidence bookkeeping and does not alter the frozen release
notes/OpenAPI revision recorded in package manifests.

## Publication Boundary

F1 final evidence review is complete and its decision is **NO-GO**. Do not
create `rust-v0.1.0-beta.1`, publish the GitHub prerelease, or push the GHCR
image until the two unchecked public-delivery gates pass on the same selected
Rust candidate and the operator then gives a separate explicit publication
instruction.
