---
id: RUST-CI-006
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/31
title: Refresh current-head stock parity evidence and reconcile docs
status: OPEN
priority: Major
category: ci
labels: [rust, ed2k, kad, parity, evidence, documentation]
milestone: rust-v0.1.0-beta.3
created: 2026-10-03
source: Stock compatibility review and retained parity evidence audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/31. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-006 - Refresh current-head stock parity evidence and reconcile docs

## Distribution Intake Acceptance

- [ ] Reconcile README, downloads, release scope and machine-readable platform
      claims with exact-source evidence. Distinguish compile, native smoke,
      public-network, appliance and minimum-OS proof; archive format is no proof.
- [ ] Use current stable aMule for explicitly scoped comparative evidence while
      preserving the separately frozen parity authorities and stock wire rules.
      Do not claim overall security/performance superiority without measurement.
- [ ] Keep mandatory core parity closure distinct from the optional expansion
      boundary in [Release Scope](../../RELEASE-SCOPE.md#client-gate).

## Summary

After the compatibility findings in this review are dispositioned, run one
authoritative stock eMule/current-aMule/Rust campaign from a clean immutable
Rust head and reconcile the durable documentation to that evidence. The
existing broad parity campaign is tied to an older Rust revision, while later
targeted witnesses do not collectively replace a same-head full campaign.

This is a hard Client-gate item. Release-scope difference tables remain a
declared set, not a proven complete set, until this campaign passes.

## Current State

- Archived `RUST-CI-002` records the authoritative parity campaign against Rust
  revision `3a162136` and later targeted reconciliation evidence.
- The current Rust branch has advanced materially beyond that revision.
- Large-library, live, and targeted peer witnesses exist for later changes, but
  no single retained campaign reruns the complete stock/MFC/current-aMule matrix
  at the current immutable head.
- The bounded Beta 3 implementation checkpoint merged as Rust
  `431d45a8283fe5edbc8357be412e933771af3232` with harness support at
  `00467b7600288989797703785f10b4a2eab2fdc7`, stock eMule at
  `ac3d52e`, and current aMule at
  `c2603a75da93ee248b17cb1d4187237601152d27`. This is a reproducible input
  set, not completed same-head parity evidence.
- The obsolete upload/download gap analysis and beta.1 soak runbook were retired
  on 2026-10-13. Archived `RUST-CI-002` and `RUST-FEAT-033` now own those results;
  the remaining gap is a same-head full campaign.

## Why This Matters

Parity claims are only auditable when code revision, fixtures, clients, policy
omissions, results, and documentation agree. Stale green evidence can conceal a
regression; stale red prose can equally misrepresent completed behavior.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust\history\items\RUST-CI-002.md`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust\history\items\RUST-FEAT-033.md`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust\RELEASE-SCOPE.md`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\policy\rust-client-omissions.toml`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-build-tests`

## Intended Shape

- Select a clean immutable Rust commit only after the blocking compatibility
  items are fixed, explicitly accepted, or scoped with a policy disposition.
- Use the policy quickstart and persisted Python launchers in
  `emulebb-build-tests`; record Windows-to-WSL path/target translation when a
  WSL lane is used.
- Run the full deterministic server, peer-transfer, Kad, REST, VPN, and required
  live/soak matrix against the same revision and recorded reference-client
  builds.
- Publish one manifest mapping every claim to a result artifact, disposition,
  omission, or explicitly non-blocking observation.
- Reconcile active, release-scope, and archived summary prose so no superseded
  claim remains presented as current.

## Scope Constraints

- Do not mix results from unrecorded Rust commits into one claimed campaign.
- Excluded protocol capabilities remain exclusions; this item does not silently
  expand or shrink the frozen omissions registry.
- Public-network checks stay bounded, gentle, and secondary to deterministic
  fixtures.
- Store reports only below `EMULEBB_WORKSPACE_OUTPUT_ROOT`; commit summaries and
  stable references, not bulky/private run artifacts.

## Acceptance Criteria

- [ ] One clean immutable Rust revision is recorded with stock eMule and current
      aMule build identities, configuration, fixture versions, and environment.
- [ ] The full required ED2K server, peer transfer, Kad, REST, VPN, and soak/live
      matrix is rerun or has a documented, approved non-applicability reason.
- [ ] Every RUST-BUG-102..105 and RUST-CI-005 disposition is exercised by a
      deterministic or interop witness appropriate to its risk.
- [ ] The omissions registry and frozen parity matrix match the evidence with no
      hidden proprietary/default divergence.
- [x] Obsolete soak guidance is removed and current release documentation no
      longer contradicts the retained upload-admission evidence.
- [ ] The evidence manifest is reproducible through maintained Python entry
      points and passes cleanup/secret/privacy checks.

## Validation

- Execute the maintained `emulebb-build-tests` parity/soak entry points described
  by the workspace policy; do not substitute ad-hoc launch logic.
- Run repository tests and documentation/link/taxonomy/roadmap checks at the
  recorded commits.
- Manually audit the final manifest against every current parity-matrix row,
  omission, open compatibility item, and summary claim.

## Notes

This is a final evidence/reconciliation gate, not a substitute for fixing the
individual findings. Existing packed-stream bounds, malformed hashset handling,
compressed-part caps, and AICH trust coverage should remain explicit regression
checks in the refreshed campaign.

## Beta 3 Evidence Placement

Retain this item's required Windows/Linux candidate outcome. Other-platform
qualification proceeds in parallel. A static audit, elapsed process time,
or an old passing revision does not establish current-candidate readiness.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_protocol_01.md` section 4.1 / 3 (existing): Browse refusal and truthful no-view advertisement remain. This is a documentation/scope gap, not an interoperability defect or approval to implement peer browsing.
- `emulebb-rust-prompt_audit_findings_protocol_01.md` section 4.2 (design): The sole connect-options producer supports and optionally requests crypto; no supported require-crypto setting exists. Do not implement a hypothetical feature to eliminate a dead future path.
- `emulebb-rust-prompt_audit_findings_protocol_01.md` section 9.1 / 10.3 (existing): Static audit is not candidate runtime proof. Reuse existing candidate certification and current-head evidence owners; other platforms are parallel and non-gating for the user's Beta 3 scope.
- `emulebb-rust-prompt_audit_findings_kad-routing-maint.md` section 4.2 (existing): The built-in fallback still exists. The existing SQLite routing/bootstrap item explicitly preserves built-in seeds and owns bootstrap provenance; scope reconciliation should record this headless operational choice.
- `emulebb-rust-prompt_audit_findings_rest-api.md` section evidence-gaps (existing): Route/auth/body/order and OpenAPI comparisons belong to existing certification/current-head evidence; audit inspection is not a pass.
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section evidence-gap (existing): Owning harness/current-head evidence must distinguish raw local captures from scrubbed shared artifacts; coordinate with testing-harness report.
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section kad-catalog-domains (existing): The catalog still lacks independently named bootstrap/three-way-HELLO/maintenance domains. Extend the existing parity-consolidation owner rather than open a second harness program.
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section crypt-capability-regression (existing): requires_crypt_layer is still hardcoded to zero. Resolve the behavior claim with the protocol audit and stock authority before changing the bit; add the exact capability regression in the canonical parity slice.
- `emulebb-rust-prompt_audit_findings_product_direction.md` section delivery-focus (existing): Existing Client/Indexer/Arr sequencing already owns product focus. Beta increments may ship while the broader Client gate stays open; the user now selects Windows/Linux readiness, with other platform work parallel.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A7-udp-verification (existing): Some firewall responder verification already has a 180-second TTL. Determine which aMule UDP verification state is meant before asserting a missing equivalent; prove the exact corresponding expiry transition.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A8-direct-callback-publish (existing): The report requests verification of a specific capability combination, not a demonstrated defect. Add it to the existing source-publish parity slice against stock authority.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A19-obfuscation (existing): RC4 speed changes require measurement under the existing hot-path owner. Obfuscated-server timeout/fallback is a protocol transition to verify through the parity catalog, not an automatic downgrade feature.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section security-parser-freeze (existing): The applicable Kad freeze and decoder/downloader allocation assertions need concrete regressions under existing bounds/parity owners. The report incorrectly cites RUST-CI-032 as Kad flood work; current #258 owns dependency-aware early checks.

### Scoped Follow-up Acceptance

- [ ] Reconcile refusal with omission registry and release scope under current-head evidence.
- [ ] Retain truthful capability advertisement and stock-shaped refusal.
- [ ] Document conservative supported posture during registry reconciliation.
- [ ] Revisit hello/login require bits only with an approved require-crypto setting.
- [ ] Retain exact revisions and artifacts for required Windows/Linux candidate workflows.
- [ ] Do not equate public-soak duration with deterministic parity.
- [ ] Document fallback ordering and seed review/refresh responsibility.
- [ ] Do not fabricate verified identities or retain import met bytes as durable state.
- [ ] Retain exact source revisions and bounded REST/OpenAPI witnesses before certification.
- [ ] Shared evidence omits operator-private values; raw captures never become public issue attachments by default.
- [ ] Add bounded catalog IDs and canonical deterministic owners for the three domains.
- [ ] Register the required causal evidence layers and immutable receipts.
- [ ] Unproven transitions remain explicitly incomplete.
- [ ] Verify supported/requested/required combinations against the accepted contract.
- [ ] A deterministic hello fixture pins the outcome.
- [ ] Candidate review uses the explicitly selected Beta 3 scope and immutable evidence.
- [ ] Later-phase implementation remains behind its gate.
- [ ] Do not treat all optional/design intake as mandatory Beta 3 implementation.
- [ ] Map the upstream state to the Rust owner.
- [ ] Test stale and mismatched verification without accepting unrelated packets.
- [ ] A controlled fixture proves whether and how the source is published.
- [ ] Record the exact source type and buddy/callback tags.
- [ ] Benchmark before adopting crypto-loop changes.
- [ ] Prove accepted retry/fallback semantics and avoid weakening required obfuscation.
- [ ] Map each reachable freeze/allocation path to its earliest bound.
- [ ] Test counted vectors, compressed data and block/part limits with finite resources.
- [ ] Do not use Rust memory safety or a closed body-limit issue as proof against OOM.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

Priority: Major
Milestone: post-beta-compatibility

After the compatibility findings are dispositioned, rerun the full deterministic/server/peer/Kad/REST/VPN/soak matrix at one clean immutable Rust head against recorded stock eMule and current aMule builds. Reconcile the omissions registry, parity matrix, active docs, and stale upload-admission claim to the resulting manifest.
