# emulebb-rust 0.1.0-beta.1 Release Evidence Checklist

This is the single operator checklist for the `rust-v0.1.0-beta.1` candidate.
The selected Rust commit is immutable for this evidence cycle. Any product or
release-workflow change selects a new candidate and invalidates the evidence
below.

**F1 board decision (2026-10-02): GO for tag and workflow-owned publication.**
Hosted CI, non-publishing packages, deterministic Windows certification,
package/SBOM verification, and the fail-closed Gluetun proof are green on the
selected candidate. The board explicitly accepts the residual public-peer
availability risk described below: the Windows bounded probe was inconclusive
and the one-hour WSL completion campaign received 50.7% of the approved ISO
before public sources stopped serving it. Those outcomes remain recorded as
observed; this decision does not relabel them as passing completion evidence.

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
- [x] Final release go is granted. On 2026-10-02 the board accepted the retained
  exact-candidate evidence as sufficient for this beta and explicitly accepted
  the residual risk that the bounded Windows and WSL public campaigns did not
  finish the approved ISO.
- [x] Annotated tag `rust-v0.1.0-beta.1` was pushed and independently resolved
  through GitHub's tag object to candidate commit
  `28a0703561f135b03ffcca94527ceb538ef9012e`.
- [x] The tag-triggered release workflow passed on the selected candidate:
  [workflow run 36993503619](https://github.com/emulebb/emulebb-rust/actions/runs/36993503619).
  All six native architecture jobs, the two-architecture image candidate, the
  versioned GHCR push, and native-asset publication succeeded.
- [x] The GitHub
  [prerelease](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.1)
  is live with 25 files: eight packages, eight manifests, six architecture
  SBOMs, release notes, changelog, and `SHA256SUMS`. All 22 entries in the sums
  file independently recomputed successfully; the `SHA256SUMS` SHA-256 is
  `2086c7c300d053a4c3fae881e6509f4c586556b047e140db22b84bcec30bf6cd`.
  Each of the 25 downloaded files also matches its GitHub asset size and
  server-recorded SHA-256 digest, with no missing or unexpected file.
- [x] The workflow pushed `ghcr.io/emulebb/emulebb-rust:0.1.0-beta.1` for
  `linux/amd64` and `linux/arm64` at manifest-list digest
  `sha256:8ddcb65b209e490405e037e78bb4c004574a5c07ee85c2dd829e16bd21f888f2`.
- [x] Anonymous GHCR inspection succeeds. The public tag resolves to the
  recorded digest with `linux/amd64` and `linux/arm64` images. The anonymous
  registry tag list is exactly `["0.1.0-beta.1"]`, and explicit inspection of
  `latest` returns `not found`.

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
| `emulebb-rust-v0.1.0-beta.1-linux-aarch64.AppImage` | `c8959465eb467be4241529190ce8aebdd9c589aee2575fee0c6c42ba587c276b` | `d8b392b7c785b4f20081e0e2bea5b6b858d35760cbcc19aa28a591d9eaf1d7d7` | `e6087fd1f5d748a516da1df6cd8b6d22674b60008bc7e40df57c1e02e1968547` |
| `emulebb-rust-v0.1.0-beta.1-linux-arm64.deb` | `dbbf358de3643af363b2bab190a1691c4d0559418156531fa62a5b8308a00c88` | `81bda53c57f950ec324aecfb53608bcb78d00126ecd508fdf0dafa59185a3a9e` | `e6087fd1f5d748a516da1df6cd8b6d22674b60008bc7e40df57c1e02e1968547` |
| `emulebb-rust-v0.1.0-beta.1-linux-amd64.deb` | `3a053c2df1b8983f385937d1c70afadd45e3583714973b2255b4a491e781fe95` | `c012c781aff1a30f9571559f0ca4cfba8973d7d116474aa0d9931eef1df205d1` | `13e1807ed246e7a77927ecb1ba4e9bfab52cdd58cb38ac480f7b9153965a0a88` |
| `emulebb-rust-v0.1.0-beta.1-linux-x86_64.AppImage` | `3b84d29e966750aaeefd03388ef926e59c9e517cab098c9c148ead923487f511` | `d651f0ac87038ffce26ca03a95346f861473a0925340ba19d0d34a144239b4f4` | `13e1807ed246e7a77927ecb1ba4e9bfab52cdd58cb38ac480f7b9153965a0a88` |
| `emulebb-rust-v0.1.0-beta.1-macos-arm64.dmg` | `977de939a886713083bb3ae3d57fa996eacea01ffcca2f5be1dda522d210cbb3` | `656a76454aef27b92efbb093a358f8476b968c75fbe83ca9a7941cfb7e1e345a` | `31f15b5224fc906b34be4d244fadb342cc7d4be7478f20e26323f776a95cf100` |
| `emulebb-rust-v0.1.0-beta.1-macos-x64.dmg` | `f827eaf120949ec8ec04ec312e979f045ffb023b2f2d7a56b45dab883f8f408a` | `efe8151b41c2ee8259e1a6e8a2e2abeec6c638e44f1a5eff11c422a38bd8e7ac` | `d1cb98d7b3cffb57ad060deb8380ff8b509b3e469ff320b22e7ddddd7abb956d` |
| `emulebb-rust-v0.1.0-beta.1-windows-arm64.zip` | `a4fbfe1c43cdbcdbfb78941093e896324dac5aa36aeb82c895d425951ab15591` | `e2cc8040efb2d25987fa78a6129ed521971aeb90c62b8571f8b76aba65c86f0a` | `abaa12b304622297b180f2d995461e8aed43796dffa6f37ee02283712165bd09` |
| `emulebb-rust-v0.1.0-beta.1-windows-x64.zip` | `df108cb639f49375cd29d3ac3d93bfce63183d667cdf096d3b6730337f388e9e` | `2d05ddeb1df464712f72b933a5fe7123ae015d25b52f54b9cb16a7966597a146` | `e14b373b7860b784226c9e59a3ac65d822f256b741a8e3bd899fb0421ae3607f` |

The Linux architecture pairs intentionally share one SBOM per architecture.
These are the final published bytes from tagged workflow run `36993503619`,
not the earlier non-publishing candidate builds. The workflow generated and
verified the combined `SHA256SUMS` before prerelease publication.

## Repository State

At final review, `main == origin/main` with an empty worktree for the Rust,
build, build-tests, and tooling repositories. The candidate Rust SHA remains
`28a0703561f135b03ffcca94527ceb538ef9012e`; the evidence-only build-tests HEAD
is `d59fc89ac8b4090a262d0fc63ea27e84ad3742ba`. The tooling HEAD that contains
this checklist is evidence bookkeeping and does not alter the frozen release
notes/OpenAPI revision recorded in package manifests.

## Publication Boundary

F1 final evidence review is complete and the board decision was **GO**. The
workflow-owned GitHub prerelease and all native assets are published from the
approved tag, and the versioned two-architecture GHCR manifest was pushed.
The organization package is public. Anonymous inspection confirms manifest
digest `sha256:8ddcb65b209e490405e037e78bb4c004574a5c07ee85c2dd829e16bd21f888f2`,
the intended amd64/arm64 images, and the version-only tag policy. GitHub issues
`RUST-FEAT-006` and `RUST-FEAT-033` are closed, their Suite Project items are
`Done`, and F2 publication is complete.
