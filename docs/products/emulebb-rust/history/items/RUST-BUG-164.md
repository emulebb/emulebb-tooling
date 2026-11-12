---
id: RUST-BUG-164
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/248
title: Preserve AICH trust provenance across hashset acquisition
status: DONE
priority: Major
category: bug
labels: [rust, aich, integrity, trust, protocol]
milestone: rust-v0.1.0-beta.3
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/248. This local document owns the durable engineering specification and evidence.

# RUST-BUG-164 - Preserve AICH trust provenance across hashset acquisition

## Closure And Evidence

[PR #315](https://github.com/emulebb/emulebb-rust/pull/315) merged as
`f4e184468d4a5ec1a1669be76cf5be951a699ff1` and closed
[#248](https://github.com/emulebb/emulebb-rust/issues/248). Accepted authority
is persisted separately from a peer's proposal; corroboration or explicit
local/operator authority is required before activation. Authority-generation
fences cover pending answers and background publication, including admitted
decisions whose callers cancel.

The PR records targeted corroboration/conflict, deletion, publication-race and
loopback late-answer regressions. Those are causality tests, not complete
interoperability evidence. The fix is included in the source-qualified and
published [Nightly 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692)
at `080a5dea70186da31dab958757b5b8c0fd883f82`; no older local receipt is
relabeled as execution on that revision. Schema 68 retains the fresh-profile
policy and separate old-profile rollback; no migration was added.

The original contract and audit provenance below remain historical evidence,
not an active implementation queue or a claim that adjacent AICH owners closed.

## Summary and Disposition

Prevent a single peer's internally consistent AICH part hashset from becoming
salvage-authorizing identity before its master root is independently trusted.
Record root provenance explicitly and preserve the distinction between local or
operator-authoritative identity and network consensus. Treat this as a Windows/Linux Beta 3 integrity requirement, not evidence that
ordinary beta downloads are routinely corrupt. MD4 remains the mandatory eD2K completion backstop.

## Revalidated Findings

Rust branch `fix/stock-hash-share-tree` at `58595576` still has this flow:

1. Startup records a peer's AICH root through `record_network_aich_root`.
   The corroboration accumulator normally requires ten distinct masked IPv4
   `/20` signers and at least 92 percent agreement.
2. `session/startup.rs` requests a modern AICH hashset when the peer advertised
   a root, even if the manifest does not yet hold a trusted root.
3. `session.rs` passes an `OP_HASHSETANSWER2` AICH section directly to
   `store_aich_hashset`.
4. That method checks geometry and reconstruction, but sets `manifest.aich_root`
   when it was absent. Reconstructing a peer-chosen master proves internal
   consistency; it does not bind that master to independently trusted content.
5. Recovery subsequently treats the manifest root as trusted and may use it
   for salvage and corruption-blackbox attribution.

There is a second state-model gap: once the manifest has any root,
`record_network_aich_observations` returns without collecting more proposals.
Network consensus therefore becomes fixed like authoritative identity. MFC's
`AICH_TRUSTED` and `AICH_VERIFIED` states are distinct; its untrusted-hash
accumulator can reconsider a consensus root when later observations change the
threshold. Do not infer provenance merely from whether hashes were persisted.

The corresponding paths also exist on locally available main `e3372aba`.
Implementation must revalidate current main and stock behavior before editing.
The reviewed branch's packed-recovery persistence and import conflict fixes do
not close this network acquisition bypass. No exploit campaign was performed.

## Representative Sites and Authority

- `crates/emulebb-ed2k/src/ed2k_tcp/download/session/startup.rs`: AICH request
  options and `peer_advertised_aich_root`.
- `crates/emulebb-ed2k/src/ed2k_tcp/download/session.rs`: modern hashset answers.
- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs`: `store_aich_hashset`,
  authoritative reconciliation, and network observation promotion.
- `crates/emulebb-ed2k/src/ed2k_transfer/aich_trust.rs`: signer/threshold rules.
- `crates/emulebb-core/src/transfer_create_api.rs`: operator link roots and
  actual Kad-responder observations, rather than displayed popularity.
- `crates/emulebb-metadata/src/schema.sql`: any required provenance state.
- Stock/MFC `SHAHashSet.cpp::UntrustedHashReceived`,
  `DownloadClient.cpp::SendHashSetRequest`, and
  `FileIdentifier.cpp::ReadHashSetsFromPacket` provide parity evidence.

## Intended Behavior

Keep candidate roots/hashsets separate from active trusted identity. A valid
hashset may be retained as a bounded candidate, or requested after trust, but it
must not itself promote the root. Only an authoritative root or an independently
corroborated root may authorize part verification, salvage, or attribution.
Validate an acquired part set against that root before activating it. Late
responses for retired candidates must not replace current trusted state.

Distinguish locally computed, explicit operator-link, accepted stock-import, and
network-consensus provenance, with a documented authority ordering. Preserve
the operator's trusted stock-import contract; do not rehash imported payloads
to invent new trust requirements. Preserve actual network-responder provenance,
one vote per masked signer, version gates, and the existing threshold.

For consensus, specify stock-compatible reconsideration and restart semantics.
If consensus loses trust or changes master, invalidate dependent candidate
activation, outstanding requests, and proof eligibility by identity/generation.
Do not demote a local/operator-authoritative root because peers disagree.
Bound observations/candidates and release per-transfer state on retirement.

Persist only the trust decisions/provenance required by the chosen contract;
in-memory vote history need not become a second durable index. A necessary
schema change follows exact-current-schema/fresh-profile policy, with no
runtime migration, repair, or legacy fallback. RUST-FEAT-065 owns presentation.

## Acceptance Criteria

- [ ] One modern peer can supply a consistent root and part set without setting
      salvage-authorizing identity or corruption-blackbox verdicts.
- [ ] Tests cover unsolicited/late hashsets, conflicting candidates, repeated
      signers, same-subnet floods, and pre-version-gate Kad observations.
- [ ] Nine independent signers remain insufficient; ten agreeing signers and
      the 92-percent boundary match stock, including subsequent disagreement.
- [ ] Authoritative link/import/local identities remain stable on conflicting
      network proposals, while consensus has explicit reconsideration rules.
- [ ] Hashset activation, persisted provenance, and restart behavior cannot
      promote a candidate merely because it was stored or acquired.
- [ ] Candidate/observation state is bounded and cleaned up on transfer removal.
- [ ] MD4 identity, single-pass hashing, zero-payload-read import reuse, and
      valid stock-compatible hashset exchanges retain their outcomes.

## Validation and Dependencies

Use a deterministic modern-peer session that returns correct MD4 hashes plus
an unrelated but internally consistent AICH tree. Assert state before any
completion pass can compute the local root. Add trust-transition and restart
tests, including an answer arriving across a consensus generation change.
Retain stock tracing/golden evidence through RUST-CI-031 and RUST-CI-006.

Implement this trust boundary before RUST-BUG-165 enforces AICH disagreements;
otherwise one untrusted peer could turn the stronger check into a denial of
completion. Coordinate request generations with RUST-BUG-166/RUST-BUG-167 and
validated proof ownership with RUST-REF-020. No live or unbounded library run is
authorized by this backlog entry.

## Beta 3 Windows/Linux Placement

Promoted to the Windows/Linux Beta 3 correctness gate on 2026-11-09. An internally consistent peer-supplied tree must not establish trusted content identity by itself.

Qualify the affected behavior on Windows and Linux, using deterministic
faults and synthetic filesystem/protocol inputs. Other-platform qualification,
including macOS/APFS variants, continues in parallel and does not block
Beta 3. This changes release placement; it does not claim a measured exploit
or routine corruption, and it does not authorize publication.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_aich-trust.md` section 2 / 4 network-authoritative assertion (existing): Current store_aich_hashset still assigns the acquired root. Saved complete issue bodies distinguish consistency from trusted provenance and define verification/request defects. Reuse those owners; do not treat persistence as automatic authority. Their current disposition is broader public-release readiness, not a newly demonstrated Beta 3 exploit.
- `emulebb-rust-prompt_audit_findings_aich-trust.md` section 6.1,6.3 / 7.3 (existing): Existing tests cover one vote per subnet; hand-derived mask boundaries and large-file/cross-client proof remain evidence extensions, owned by current AICH and canonical protocol items.
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section aich-regressions (existing): Trailing recovery bytes and equal-weight trust tie behavior should be reconciled with existing AICH admission/provenance/reuse items and the separate AICH audit.

### Scoped Follow-up Acceptance

- [ ] Implement provenance before enforcing AICH disagreement.
- [ ] Coordinate answer admission and bounded request lifecycle with the same generations.
- [ ] Preserve mandatory MD4 completion and imported/operator authority.
- [ ] Use independent /20 byte-order fixtures and 16/32-bit proof boundaries.
- [ ] Avoid duplicate evidence tickets or duplicating payload reads.
- [ ] Reject noncanonical recovery framing under the owning admission contract.
- [ ] Equal input evidence yields a deterministic trust result.
- [ ] Tests preserve request matching and trusted-root authority.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

**Reviewable branch spec:** https://github.com/emulebb/emulebb-tooling/blob/fix/stock-hash-share-tree/docs/products/emulebb-rust/active/items/RUST-BUG-164.md
