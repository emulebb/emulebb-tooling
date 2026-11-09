---
id: RUST-CI-034
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/268
title: Reconcile audit findings into the Windows and Linux Beta 3 delivery scope
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/268. This local document owns the durable engineering specification and evidence.

# RUST-CI-034 - Reconcile audit findings into the Windows and Linux Beta 3 delivery scope

## Summary

Revalidate the temporary audit collection, deduplicate against current work, preserve every finding disposition in durable owning specs, and prioritize a finite Windows/Linux Beta 3 scope. GitHub issues and Project #3 remain workflow authority. Other platforms continue in parallel without blocking Beta 3; Client-to-Indexer and Indexer-to-Arr product gates remain separate.

## Release Placement

Beta 3 blocker for Windows/Linux.

Priority: Major. Delivery lane: parent-coordination.

## Current Findings

Three independent review assignments inspected every report and used targeted current-source checks. Static inspection is not runtime proof. The source collection has 31 files; its local path and private operator material are not dependencies of the resulting backlog.


## Audit Provenance

- 2026-11-08/09 temporary audit collection, all 31 files; per-finding dispositions retained below.

## Acceptance Criteria

- [ ] Every source report and actionable finding has a recorded owning issue or explicit fixed, unsupported, or design disposition.
- [ ] New accepted outcomes have stable unused IDs, durable engineering specs, open owning issues and Project #3 status/product/phase/priority.
- [ ] Existing owners receive the relevant audit evidence without duplicate tickets.
- [ ] Beta 3 Windows/Linux blockers are distinguished from parallel follow-ups and scope decisions; optional-platform work does not silently expand the release gate.
- [ ] The candidate certification spec and milestone describe the operator-approved Windows/Linux scope; any required workflow split is tracked explicitly.
- [ ] Privacy-safe findings and acceptance criteria remain usable after the temporary source folder is removed.

## Dependencies And Coordination

- emulebb-build issue #28 owns managed parallel-checkout implementation.
- RUST-CI-006 and RUST-CI-009 retain exact-candidate certification ownership.
- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Run documentation taxonomy, structure, publication, strict site and live GitHub roadmap reconciliation checks. Verify all 31 source filenames are covered exactly once and each newly allocated ID is unique against active/history specs and GitHub.

## Private Diagnostic Bundle Revalidation (2026-11-09)

The seven raw-export privacy findings below were revalidated against the
intentional authenticated private-bundle contract. The response deliberately
contains exact credentials and operator evidence; the tests require this.
There was no existing safe/shareable-export promise to repair. Their final
disposition is design/nondefect, while stable [RUST-BUG-178](RUST-BUG-178.md)
owns the actual Beta3 UI defect: a visible private-content warning and explicit
acknowledgement before capture/download. A full allowlisted shareable summary
remains a design proposal outside Beta3, with no endpoint implementation
accepted. All 29 stable new-item IDs and all 212 original finding dispositions
remain accounted for; this narrows an existing outcome without reallocating it.

## Audit Disposition Evidence

Reviewed source baseline: Rust `edc59a003fff873e26d2c720bf9ca06f4b640871`. Findings are source-inspected unless an owning item explicitly records runtime evidence. No private operator configuration or raw soak data is reproduced.

### aich-trust.md

Source fingerprint (SHA-256): `216412dd745818d46750eecdb64686120741f7a7e733691800b5c62cbd027a77`.

- **3.1 — Keep the unsafe stock debug trust bypass absent**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Omitting trust-every-hash is a conservative production decision. Do not add a bypass merely to copy a stock debug preference.
- **3.2 — Keep asymmetric-child AICH tree rejection**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Current malformed-tree strictness is intentional and safer; no corrective ticket.
- **2 / 4 network-authoritative assertion — Existing AICH integrity issues override the report's reassuring trust verdict**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/248, https://github.com/emulebb/emulebb-rust/issues/249, https://github.com/emulebb/emulebb-rust/issues/250, https://github.com/emulebb/emulebb-rust/issues/251
  Current store_aich_hashset still assigns the acquired root. Saved complete issue bodies distinguish consistency from trusted provenance and define verification/request defects. Reuse those owners; do not treat persistence as automatic authority. Their current disposition is broader public-release readiness, not a newly demonstrated Beta 3 exploit.
- **6.2 / 7.2 — Separate stock background thread structure is unnecessary**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  Rust computes MD4 and AICH together in its existing bounded ingest worker. The audit did not establish a missing outcome that requires copying stock's AICHSyncThread architecture.
- **6.1,6.3 / 7.3 — Pin AICH subnet, proof geometry and large-file evidence**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/248, https://github.com/emulebb/emulebb-rust/issues/250
  Existing tests cover one vote per subnet; hand-derived mask boundaries and large-file/cross-client proof remain evidence extensions, owned by current AICH and canonical protocol items.

### async-lifecycle.md

Source fingerprint (SHA-256): `75cdf6656734b7f009998741ebba412a272132c47d3ba9b6dfbb2a4fc144fc25`.

- **2.1 — Own upload promotion tasks through cancellation and shutdown**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Existing REF006 explicitly owns task lifecycle. Prefer owned cancellation/RAII guards and observable completion; do not blindly add catch_unwind to every task.
- **2.2 — Make helper single-join contract explicit**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Latent API contract improvement under existing lifecycle owner, not a demonstrated user-triggered crash.
- **2.3 — Keep abort-on-drop as a documented backstop**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Drop cannot await; scheduling abort is expected. No synchronous-drop-join fix.
- **2.4 — Preserve honest unknown-delivery cancellation semantics**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Attach caller retry/cancellation proof to existing lifecycle work; unknown means potentially delivered, not automatic retry.
- **evidence-gaps — Prove bounded task shutdown and blocking-work ownership**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Use existing safety item for Kad task ownership and blocking-job cancellation evidence, without a new broad soak project.

### code-quality-unsafe.md

Source fingerprint (SHA-256): `b0d31a1d4e890d8e3cea6e8bd68d6675f9729e45383e6b0962ed446b85861037`.

- **2.2 — Keep documented Win32 IOCTL value without trivial constant-pinning tests**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  A test asserting the same literal would mirror implementation. Add platform-behavior evidence only if meaningful.
- **2.3 — Verify native aggregate layouts and zero-initialization assumptions**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/163
  Use exact native-header ABI proof; zero is valid for current C aggregates. A bool field by itself does not make zero invalid.
- **2.4 — Retain justified FFI unsafe boundaries**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/9, https://github.com/emulebb/emulebb-rust/issues/163
  Unsafe count and SAFETY comments are not soundness proof; keep proof in existing owners.
- **3.1 — Decompose responsibility-mixed modules under existing owner**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/7
  No line-count-only blocking refactor.
- **3.3 — Make settings inventory mapping total or fail explicitly**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Follow-up safety/contract slice under existing owner. Preserve one settings inventory and avoid a second manual mapping.
- **evidence-gaps — Prove ABI rather than relying on unsafe comments**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/163
  Closed lint/suppression work does not establish C ABI layout compatibility.

### credits-queue.md

Source fingerprint (SHA-256): `46cba0cf8408991338ba026962db10c30bd5d63ae5a8ab497022a71795a9ba2b`.

- **3.1 — Restore the compatible-client branch of old-client upload scoring**
  Disposition: `new`. Owner: RUST-BUG-170
  Current old_client only checks is_emule_client and old version. The compatible-client soft-id leg is not represented, so legacy non-eMule queue ordering can differ.
- **3.2 — Credit-ratio floating precision is a bounded design difference**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  f64-to-permille rounding can differ from float at boundaries; no material failure was demonstrated. Keep the precision choice explicit and do not turn numeric type matching alone into a blocker.
- **3.3 / 3.4 — Neutral unverified credit and friend-slot sentinel are non-defects**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  Crypto is always available, and the friend-slot constant is an ordering sentinel; the recorded differences do not establish changed supported behavior.
- **6.1-3 / 7.3 — Prove disconnected LowID queue and rate-meter behavior**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Callback entitlement and disconnected promotion are implemented; the missing end-to-end oracle derivation is a canonical evidence gap, not a proven missing zero-score check.

### dependencies.md

Source fingerprint (SHA-256): `7baf7ff264729a6df7173e4c945baae503182b2b230516c748bd5e787d682d1f`.

- **rsa-ignore — Retain and periodically reassess the documented RSA advisory exception**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  The Marvin exception is deliberate and scoped to non-decryption secure-ident use. Track a reviewed recheck trigger and upstream fix disposition; do not remove the exception or claim a vulnerability merely from the advisory ID.
- **protocol-hashes — Preserve protocol-mandated hash primitives**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  MD4/MD5/SHA-1 are protocol requirements. Replacing them on the wire is not an accepted remediation; trust hardening belongs in the existing identity/AICH work.
- **native-source-docs — Document native sys source and toolchain coupling**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-build/issues/28
  The sys crates depend on pinned external C trees and a matching toolchain. No sys README was found. Document the supported dependency roots and provenance checks without copying machine-local paths. Parent reconciliation: source-root documentation is part of the managed-checkout foundation acceptance, tracked by Build issue #28.
- **native-pins — Keep existing native provenance verification**
  Disposition: `already-fixed`. Owner: https://github.com/emulebb/emulebb-rust/issues/8
  Native revision pins and drift verification already exist. Their presence is not a new supply-chain defect; extend them only for a concrete adapter/upstream revision change.
- **duplicate-crates — Review nonintentional duplicate dependencies without blanket upgrades**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Duplicate versions are warnings, not demonstrated failures. Trace the Windows/tower-http/transitive origins when scheduling updates; retain the intentionally aliased legacy SHA-1 stack.
- **sqlite-provenance — Report bundled SQLite version in build evidence**
  Disposition: `new`. Owner: RUST-CI-038
  Cargo.lock identifies rusqlite/libsqlite3-sys but not a user-facing SQLite runtime version report. Include the exact bundled SQLite version in safe CI/SBOM evidence and define an update review trigger.
- **advisory-gate — Reuse the existing authoritative cargo-deny CI gate**
  Disposition: `already-fixed`. Owner: https://github.com/emulebb/emulebb-rust/issues/8
  The recommendation to start advisory CI is already satisfied by mandatory cargo-deny advisories/licenses/sources. A second cargo-audit runner is not required solely because the historical audit did not execute checks.
- **dependabot-fuzz — Finish the existing Dependabot resolver fix PR**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/267
  The separate CI worker already owns RUST-CI-033 / issue #267. Explicit build declarations and offline resolver regressions are committed in its isolated workstream, awaiting the parent foundation and push-validation window; they are not yet canonical main.

### diagnostics-privacy.md

Source fingerprint (SHA-256): `8c9dccdef79b2528edb1c27805ec94ac268a1e85eafece253c8b6c88b19a6162`.

- **3.1 — Sanitize shareable diagnostic exports**
  Disposition: `design`. Owner: Design only; related private-warning owner RUST-BUG-178 / https://github.com/emulebb/emulebb-rust/issues/280
  Deeper revalidation: this authenticated endpoint deliberately exports exact private operator evidence, including its API key; raw contents are not a defect in that contract. A genuinely shareable allowlisted summary is a design proposal outside Beta3, with no new endpoint accepted. Related RUST-BUG-178 / #280 owns only the missing visible private-content warning and explicit acknowledgement.
- **3.2 — Exclude operator public-address identity from safe exports**
  Disposition: `design`. Owner: Design only; related private-warning owner RUST-BUG-178 / https://github.com/emulebb/emulebb-rust/issues/280
  Deeper revalidation: this authenticated endpoint deliberately exports exact private operator evidence, including its API key; raw contents are not a defect in that contract. A genuinely shareable allowlisted summary is a design proposal outside Beta3, with no new endpoint accepted. Related RUST-BUG-178 / #280 owns only the missing visible private-content warning and explicit acknowledgement.
- **3.3 — Exclude private absolute paths and content names from safe exports**
  Disposition: `design`. Owner: Design only; related private-warning owner RUST-BUG-178 / https://github.com/emulebb/emulebb-rust/issues/280
  Deeper revalidation: this authenticated endpoint deliberately exports exact private operator evidence, including its API key; raw contents are not a defect in that contract. A genuinely shareable allowlisted summary is a design proposal outside Beta3, with no new endpoint accepted. Related RUST-BUG-178 / #280 owns only the missing visible private-content warning and explicit acknowledgement.
- **3.4 — Exclude content fingerprints from safe exports**
  Disposition: `design`. Owner: Design only; related private-warning owner RUST-BUG-178 / https://github.com/emulebb/emulebb-rust/issues/280
  Deeper revalidation: this authenticated endpoint deliberately exports exact private operator evidence, including its API key; raw contents are not a defect in that contract. A genuinely shareable allowlisted summary is a design proposal outside Beta3, with no new endpoint accepted. Related RUST-BUG-178 / #280 owns only the missing visible private-content warning and explicit acknowledgement.
- **3.5 — Exclude peer endpoints and client identifiers from safe exports**
  Disposition: `design`. Owner: Design only; related private-warning owner RUST-BUG-178 / https://github.com/emulebb/emulebb-rust/issues/280
  Deeper revalidation: this authenticated endpoint deliberately exports exact private operator evidence, including its API key; raw contents are not a defect in that contract. A genuinely shareable allowlisted summary is a design proposal outside Beta3, with no new endpoint accepted. Related RUST-BUG-178 / #280 owns only the missing visible private-content warning and explicit acknowledgement.
- **3.6 — Exclude raw packet payloads from safe exports**
  Disposition: `design`. Owner: Design only; related private-warning owner RUST-BUG-178 / https://github.com/emulebb/emulebb-rust/issues/280
  Deeper revalidation: this authenticated endpoint deliberately exports exact private operator evidence, including its API key; raw contents are not a defect in that contract. A genuinely shareable allowlisted summary is a design proposal outside Beta3, with no new endpoint accepted. Related RUST-BUG-178 / #280 owns only the missing visible private-content warning and explicit acknowledgement.
- **3.7 — Preserve diagnostic retention and loss visibility**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Rotation, ring bounds and dropped-line visibility are invariants, not additional backlog.
- **evidence-gap — Check harness evidence promotion against export hygiene**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/31, https://github.com/emulebb/emulebb-rust/issues/84, https://github.com/emulebb/emulebb-rust/issues/96
  Owning harness/current-head evidence must distinguish raw local captures from scrubbed shared artifacts; coordinate with testing-harness report.

### dos-resilience.md

Source fingerprint (SHA-256): `f944937eefe090bd6181221f9939c4adbf90a397e752b68ebcb86f2c04bd0c7f`.

- **2.1 — Ban-store expiry pruning already runs in production**
  Disposition: `already-fixed`. Owner: https://github.com/emulebb/emulebb-rust/issues/83
  Report searched only ed2k crate and missed core owner; do not reopen closed pruning issue.
- **2.2 — Bound Kad tracker population under source churn**
  Disposition: `new`. Owner: RUST-BUG-180
  Per-source request accounting and minute pruning do not themselves establish aggregate memory bounds. Verify churn exposure, then enforce fail-visible bounded admission while preserving stock ordinary traffic.
- **2.3 — Tracked identity expiry pruning already runs in production**
  Disposition: `already-fixed`. Owner: https://github.com/emulebb/emulebb-rust/issues/83
  Same missed downstream owner as2.1; no duplicate fix.
- **2.4 — Bound remote control-plane admission and authentication abuse**
  Disposition: `new`. Owner: RUST-BUG-177
  Authenticated application middleware cannot limit idle pre-auth TCP sessions. Consolidate with rest-api3.3; do not imply API auth fixes socket exhaustion.
- **2.5 — Prove client-UDP source state remains coordinator-bounded**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Do not add a second contradictory source cap without tracing admission. Attach bounded-source ownership proof to canonical client-UDP evidence.

### fuzz-malformed.md

Source fingerprint (SHA-256): `6547b83fab34c3c3f2d1a060bd9fe7e7e14e19d421eb9bbcf28d6734cc500d54`.

- **3.1 — Exercise bounded media parsers with fuzz inputs**
  Disposition: `new`. Owner: RUST-BUG-181
  Consolidate with media-metadata3.1 as one parser-bounds outcome, rather than a second mandatory beta blocker issue.
- **3.2 — Expand malformed wire-input proof to Kad inbound obfuscation**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Attach bounded fuzz/property target plus deterministic regressions to canonical protocol evidence; overlaps testing-harness report.
- **3.3 — Expand malformed wire-input proof to stream framing**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Keep stream length/packed/truncation proof in canonical codec owner, not another test ledger.
- **3.4 — Exercise filename normalization and legacy codec boundaries**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/242
  Attach normalization fuzz/property proof to existing decoder and filename owners. Overlaps search6.1 and testing-harness traversal gap.
- **3.5 — Retain selector dispatch as an accepted fuzz organization**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/42
  Separate targets may improve attribution but selector dispatch alone is not a defect.

### hashset-largefile.md

Source fingerprint (SHA-256): `e1af346e0ddf7c11de0c8a756caf5dc85a2645c24200ec09576253a9d5caf20e`.

- **2.1 — Omit unavailable MD4 sections from modern hashset answers**
  Disposition: `new`. Owner: RUST-BUG-172
  The encoder still sets the MD4-present bit for Some(empty) with a multi-part size. Serving callers obtain metadata through the runtime, so production reachability must be demonstrated; the encoder currently cannot enforce the stock expected-count invariant.
- **2.2 — Reject file sizes outside representable ED2K hashset geometry**
  Disposition: `new`. Owner: RUST-BUG-173
  Expected MD4 counts still saturate to u16::MAX while the actual encoder rejects overflowing vector length. Make the accepted transfer geometry explicit instead of letting saturation stand in for a supported-size decision.
- **2.3 — Do not change the correct file-hash-prefixed MD4 layout**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  The upstream opcode comment is stale; Rust's actual encoder correctly emits the file hash before count and hashes.
- **5 — Hashset large-file interoperability remains existing evidence work**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  The report did not run a live exchange. Preserve the existing part-count, AICH geometry and bitmap outcomes through canonical boundaries rather than creating a second parity suite.

### indexer.md

Source fingerprint (SHA-256): `a80cad49fc4e8a0053aca621ebb6a7bbf3f872c32af9e231c5dc756390128451`.

- **queue-restart — Persist Indexer demand/provenance state at the future Indexer gate**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/2
  Snapshot/merge helpers exist without a production persistence/restore call. Track a separately deliverable slice under the existing Indexer owner; do not silently turn default-off Client passive replay into autonomous Indexer production.
- **write-fault-latch — Pause future Indexer discovery on persistent index-write failure**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/2
  Current passive writes log and continue; the future Indexer contract requires persistent fault reporting and discovery isolation. This is an unimplemented future-phase acceptance outcome, not a Beta 3 shipped-Indexer defect.
- **global-replay-budget — Reconcile the Indexer aggregate discovery budget**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/2
  Current general/source budgets can sum to 84 queries per 600 seconds, while the future design says one global budget. Choose an explicit combined ceiling or a reviewed documented interpretation.
- **passive-file-type — Retain available file-type classification in indexed observations**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/2, https://github.com/emulebb/emulebb-rust/issues/29
  Passive indexed rows currently hardcode unknown. Reuse canonical type classification and metadata merge rules, while keeping live search metadata ownership in #29 and autonomous Indexer work behind its phase gate.

### IPv6.md

Source fingerprint (SHA-256): `3beb1001352bfdc5e9dcc43ab10ea0916df3868ebffa484354974e844e7afab5`.

- **ipv6-scope — Decide whether to reopen current-network dual-stack scope**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Track a decision outcome, not an accepted IPv6 implementation. Current policy still permanently omits IPv6. Assess additive peer/server transport with IPv4 Kad routing, effort, evidence and phase placement before changing registries.
- **ipv6-endpoints — Design endpoint representation and opt-in IPv6 listeners**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Assess IpAddr/SocketAddr-based endpoint representation, IPv4-mapped handling and separate IPv6-only listeners while preserving today's IPv4 defaults. No implementation commitment follows from ecosystem reports alone.
- **ipv6-peer-server-sources — Specify peer/server IPv6 negotiation and source interoperability**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Validate CT_MOD_IP_V6, OP_IPV6_UPDATE, server status/flags and inline IPv6 source records against exact reference revisions. Include extended source exchange and s6/bracketed-link handling; the report's external adoption claims are not independently reverified here.
- **ipv6-kad-metadata — Design IPv6 source metadata without widening Kad transport**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Assess the two IPv6 source payload tags only after the full endpoint/source design. Legacy zero-buddy interpretation and LowID behavior require explicit fixtures; do not cherry-pick a partial tag implementation.
- **ipv6-persistence-api — Plan lossless dual-stack persistence, REST and diagnostics**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Endpoint scope affects stored peers/sources, search delivery, API/WebUI models, bind settings and diagnostics. Design the full chain and schema/profile consequences before any advertisement ships.
- **ipv6-reachability — Define fail-closed IPv6 advertisement and abuse accounting**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Assess observed-over-asserted addresses, global usability, dial-back/reflection/corroboration, contradictory evidence vetoes, stable address selection and /64 abuse accounting. Never advertise an address simply because a peer supplied it.
- **ipv6-bind-obfuscation-proof — Design dual-stack confinement and interop qualification**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  VPN/bind confinement, obfuscation, NAT and dual-stack need combined proof. Reference-client trust models vary, so a byte-compatible parser alone cannot establish safe reachability.
- **ipv6-kad-network — Keep a distinct IPv6-routed Kad network outside the proposal**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  A separate IPv6 Kad DHT is exploratory and is not current-network dual-stack interoperability. No automatic product commitment or new network implementation should result from this report.

### kad-routing-maint.md

Source fingerprint (SHA-256): `d2b1d4cfbeee8137a1d81d4e3ce66473b9af1bb6cba8f6bc389e6e0158ae3f94`.

- **4.1 — Weight Kad user estimates by observed firewall and version ratios**
  Disposition: `new`. Owner: RUST-FEAT-066
  The estimator still uses fixed firewall multipliers. Improving this optional operator statistic has no routing, search or publish correctness impact.
- **4.2 — Record built-in Kad seed provenance and refresh policy**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/233, https://github.com/emulebb/emulebb-rust/issues/31
  The built-in fallback still exists. The existing SQLite routing/bootstrap item explicitly preserves built-in seeds and owns bootstrap provenance; scope reconciliation should record this headless operational choice.
- **4.3 — Unverified text bootstrap contacts preserve the trust boundary**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Plain-text endpoint input deliberately does not authenticate a contact. Preserve verified=false rather than treating the extra handshake as a defect.
- **6 / 7.3 — Routing timer and replacement boundaries belong to canonical evidence**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/202
  The report requests optional timer/fill-boundary goldens and acknowledges untraced quality constants. Existing routing maintenance and canonical evidence owners cover this work.

### media-metadata.md

Source fingerprint (SHA-256): `c2afd6612616c82fb9d04cb35848a34aeb59e8914b9a665e99f970cc2c8a959b`.

- **3.1 — Bound RIFF nesting and media-parser work**
  Disposition: `new`. Owner: RUST-BUG-181
  Adversarial locally shared WAVE/AVI bytes can drive recursion. Scope is local library admission, not demonstrated unauthenticated remote input. Consolidate fuzz-malformed3.1.
- **3.2 — Bound optional media enrichment and remove publication delay**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/96
  Existing REF008 explicitly owns bounded optional enrichment and extra reads. Avoid timeout wrappers that merely abandon a still-running blocking task.
- **3.3 — Honor ID3 flags before publishing derived text**
  Disposition: `new`. Owner: RUST-BUG-182
  Display metadata correctness; separate from FEAT040 inbound metadata transport. Skip encrypted/compressed frames; handle supported unsynchronization safely.
- **3.4 — Disposition approximate MPEG metadata estimates**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Stricter frame/CRC checks are optional accuracy improvements; do not label an approximate estimate a memory-safety defect.
- **3.5 — Preserve media text, read and SQL bounds**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Text limits and disabled cover art remain requirements; no separate task.

### multi-platform.md

Source fingerprint (SHA-256): `dcada371776cc74fb529b14bcb960f205668fdb86a412e6d090de466d0670b10`.

- **portable-delivery — Qualify no-clobber completed-file delivery on extended Unix targets**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/226, https://github.com/emulebb/emulebb-rust/issues/229, https://github.com/emulebb/emulebb-rust/issues/231
  The unsupported-platform arm still rejects completed delivery. Android/FreeBSD/other Unix issues already own platform viability. Do not adopt the audit's check-then-rename suggestion: it can race and clobber data.
- **android-route-inventory — Make Android route selection explicit and evidence based**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/226
  Android still receives an empty default-route interface inventory. Its existing support item must define supported route discovery or an honest explicit-bind-only contract; Android APK/signing remains on hold.
- **aich-width — Replace unchecked AICH geometry narrowing with bounded conversions**
  Disposition: `new`. Owner: RUST-REF-024
  Plain u64-to-usize casts remain. The audit establishes a hardening opportunity, not a reachable Windows/Linux 64-bit failure. Avoid adding a new supported 32-bit product target merely for this cleanup.
- **extended-lanes — Reconcile historical missing-lane claims with current CI**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/226, https://github.com/emulebb/emulebb-rust/issues/227
  The audit's no-musl/no-Android-CI claim is stale: both musl architectures and Android compile/ELF lanes now exist. Keep the owning feature issues open for their remaining runtime/package evidence; cross-compilation is not complete platform certification.
- **beta3-gate-split — Separate mandatory Windows/Linux gates from optional platform outcomes**
  Disposition: `new`. Owner: RUST-CI-035
  Parent-reserved RUST-CI-035 owns the user-authorized split. CI combines Linux ARM/Windows/macOS in build-test and requires Android; release smoke/images depend on the entire native matrix, and the assembler hardcodes macOS assets. Docs alone cannot implement the new gate.
- **platform-evidence — Retain tiered Unicode and packaged runtime proof**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/84, https://github.com/emulebb/emulebb-rust/issues/142, https://github.com/emulebb/emulebb-rust/issues/227, https://github.com/emulebb/emulebb-rust/issues/228, https://github.com/emulebb/emulebb-rust/issues/229, https://github.com/emulebb/emulebb-rust/issues/230, https://github.com/emulebb/emulebb-rust/issues/231
  Windows/Linux are Beta 3 gates. macOS and extended target qualification continue in parallel, with per-target limitations and no stronger support claim than retained runtime evidence.

### obfuscation.md

Source fingerprint (SHA-256): `5f9f93dc77bb32df43bca193900cf26211c0b6b4e605f99944be8930f945aca0`.

- **2.1 — Reject degenerate server Diffie-Hellman public values**
  Disposition: `new`. Owner: RUST-BUG-171
  The server DH path still computes modpow without rejecting degenerate values. Stock has the same weakness; rejecting invalid inputs preserves valid-peer compatibility and should not imply modern authenticated encryption.
- **2.2 — Bounded handshake padding is not an unbounded allocation defect**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Inbound length is one byte and bounded to 255 bytes. Server padding above its preferred cap is already logged. Blindly clamping a read can desynchronize RC4/frame state; no automatic cap change should follow this audit.
- **2.3 — Verify mixed Kad and eD2K obfuscation on the shared socket**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/1
  A named classification helper remains staged, but production Kad decrypt already falls through to a registered foreign raw-datagram handler. This disproves the blanket unwired-transport premise; correctness needs mixed-key/protocol evidence before rewiring.
- **2.4 — Preserve protocol-mandated legacy obfuscation primitives**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  RC4, MD5 and the legacy DH group are compatibility constraints, not an approved stronger-transport feature.
- **5 — Complete server UDP and encrypted-exchange evidence**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  The report inspected constants without proving all server UDP key derivation/state transitions or replaying encrypted exchanges.

### persistence.md

Source fingerprint (SHA-256): `6958700b30dff6e7f267a3d13a2bd3fd43315616c35078f19a685a44c5856235`.

- **2.1 — Reject incorrect FTS phrase-versus-AND claim**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  The report confuses quoted phrase syntax with bare whitespace-separated tokens. Do not implement its proposed correction without a reproducer.
- **2.2 — Reject blanket missing settings bounds claim**
  Disposition: `not-supported`. Owner: https://github.com/emulebb/emulebb-rust/issues/16
  Report inspected serde structs but missed actual validation boundaries. Individual settings bypasses require specific reproduction; no broad validator replacement.
- **2.3 — Keep dynamic SQL identifiers restricted to trusted schema owners**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Typed identifiers or whitelists are optional defensive API design. No defect solely because trusted identifier strings are formatted.
- **2.4 — Keep SQLite scheduling work in the existing bounded persistence owner**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/155
  Do not add speculative pools or independent actors. Existing REF016 owns queue/wait/commit semantics and read-lane justification.
- **2.5 — Settings table is active product storage**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  The vestigial-table claim is incorrect; removing it would destroy persisted settings.

### product_direction.md

Source fingerprint (SHA-256): `d8e2e1de3dc9b4be521e765d1a835d9e033258756140eea053f64b4d1075bae5`.

- **public-contract — State support and parity claims through existing evidence**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Replace vague universal/perfect claims with concrete supported behavior, reviewed omissions and evidence tiers. Ecosystem popularity and marketing claims in the report are dated observations, not validated product facts. Parent disposition: the current release scope and product landing page already state the bounded beta/support contract; retain this as an editorial constraint during reconciliation.
- **succession — Define contributor ownership and succession safeguards**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  The report's single-maintainer risk warrants a governance/contributor plan. It does not justify automatic outreach, role assignment or a new technical release blocker.
- **adoption-onboarding — Assess container demos and contributor/user onboarding**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Review current nightly, container and profile-import instructions for a small reproducible onboarding outcome. Do not create marketing commitments or contact outside parties without an explicit assignment.
- **retention-policy — Review the proposed Indexer quota against its current retention contract**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/2
  The recommendation for a configurable record/disk ceiling directly conflicts with the explicit no-TTL/no-quota product decision. Track a design review, not an automatic implementation or a current runtime defect.
- **stability-freezes — Evaluate early schema stability as an explicit policy decision**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Current API/config/schema freeze is deliberately post-Arr. An earlier schema freeze or migration promise would change product policy and needs an assessed decision, not incidental implementation.
- **ipv6-timebox — Use the focused IPv6 scope review for the reachability recommendation**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Deduplicate the broad product-direction IPv6 recommendation into the focused IPv6 decision. CGNAT and IPv6 are related but IPv6 is not a universal CGNAT fix for all peers.
- **server-relationship — Assess an upstream Rust server interoperability relationship**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  A server partnership is an ecosystem idea. Preserve the upstream-clean server boundary and avoid a parallel server product or fork-only compatibility evidence.
- **indexer-data-policy — Define Indexer data and abuse-handling posture before shipping**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/2
  Track data-retention, provenance, operator controls and abuse/moderation questions as a future Indexer design outcome. The report's jurisdictional risk is a question for review, not a proven compliance defect.
- **delivery-focus — Finish the bounded Beta 3 candidate before later suite production**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/142, https://github.com/emulebb/emulebb-rust/issues/31, https://github.com/emulebb/emulebb-rust/issues/2, https://github.com/emulebb/emulebb-rust/issues/4
  Existing Client/Indexer/Arr sequencing already owns product focus. Beta increments may ship while the broader Client gate stays open; the user now selects Windows/Linux readiness, with other platform work parallel.

### product_direction_amule_future_parity.md

Source fingerprint (SHA-256): `067757068618b2d75ef9e2dd01e0d8257b94688d052435833641afaf77640d53`.

- **present-features — Avoid duplicate implementations for already-supported protocol features**
  Disposition: `not-supported`. Owner: https://github.com/emulebb/emulebb-rust/issues/22, https://github.com/emulebb/emulebb-rust/issues/25, https://github.com/emulebb/emulebb-rust/issues/249
  AICH-over-Kad, AICH/hashsets/ICH, source reask, obfuscation, OfferFiles, firewall/buddy/callback and NAT capabilities already exist. The report's feature inventory does not prove every edge case; retain existing trust and parity owners rather than reimplement the feature.
- **scale-proof — Finish existing large-library and slow-disk evidence work**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/84, https://github.com/emulebb/emulebb-rust/issues/95, https://github.com/emulebb/emulebb-rust/issues/96, https://github.com/emulebb/emulebb-rust/issues/97, https://github.com/emulebb/emulebb-rust/issues/98, https://github.com/emulebb/emulebb-rust/issues/155, https://github.com/emulebb/emulebb-rust/issues/240, https://github.com/emulebb/emulebb-rust/issues/241
  The aMule scaling wave is inspiration, not evidence of the same defect in Rust. Existing storage-domain, scan-I/O, async SQLite/filesystem/CPU and upload-performance items own the remaining work.
- **A1-combined-search — Design a single search spanning eD2K and Kad**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Current automatic search selects one ready lane, preferring the server; it is not concurrent All search. Assess the additive unified-search behavior, rate budget, cancellation and result-merging contract before implementation.
- **A2-search-metadata — Reuse the search metadata carry owner**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/29
  Standard media tags, type, note/rating and provenance-bearing AICH metadata already belong to RUST-FEAT-040. Verify which decoders/storage/API fields still drop data rather than create a second metadata project.
- **A3-kad-cache-load — Include synchronous Kad cache hydration in async persistence review**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/155
  Kad cache hydration calls SQLite synchronously during core construction. Existing async SQLite persistence work is the nearest owner; the review did not measure startup blocking or establish a new release defect.
- **A4-kad-diagnostics — Assess bounded Kad contact and lookup diagnostics**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  A contact-distribution/lookup trace view is an observability idea. Inventory existing diagnostics first and define bounded, privacy-safe output rather than add an unbounded trace surface.
- **A5-buddy — Extend existing buddy-liveness proof with relay ownership checks**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/103, https://github.com/emulebb/emulebb-rust/issues/164
  Silent-buddy expiry is already #103. Verify that no callback is relayed for an unrelated buddy within the canonical buddy slice; the aMule report alone does not establish that Rust currently cross-relays.
- **A6-firewall-recheck — Retain existing firewall recheck state protection**
  Disposition: `already-fixed`. Owner: Recorded disposition; no new implementation commitment.
  Recheck code snapshots the previous state and tests exercise stale rounds and retained UDP-open behavior. Do not open an unproven recheck defect; expand only for a specific missing variant.
- **A7-udp-verification — Verify stale Kad verification expiry under the existing parity catalog**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/31
  Some firewall responder verification already has a 180-second TTL. Determine which aMule UDP verification state is meant before asserting a missing equivalent; prove the exact corresponding expiry transition.
- **A8-direct-callback-publish — Prove the firewalled-TCP/direct-UDP/no-buddy publish combination**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/31
  The report requests verification of a specific capability combination, not a demonstrated defect. Add it to the existing source-publish parity slice against stock authority.
- **A9-tag-layout — Prove buddy hash layout and UTF-8 Kad tag variants**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  UTF-8 decoding support exists. Verify the buddy-hash byte layout and negotiated tag cases with exact packet fixtures rather than infer a bug from an aMule changelog.
- **A10-source-latency — Measure initial source discovery including hostname-added servers**
  Disposition: `new`. Owner: RUST-CI-039
  The audit did not establish a source-discovery timing defect. Create a bounded verification outcome for initial source requests and hostname server UDP behavior before considering a scheduling change.
- **A11-endgame — Include failed takeover requeue semantics in the existing endgame item**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/27
  Bounded endgame takeover already owns cancellation, lease redistribution and first-verified-wins semantics. Add failed-takeover requeue/free-interval coverage to that acceptance, not a duplicate feature.
- **A12-payload-throttle — Verify download limits charge payload rather than control overhead**
  Disposition: `new`. Owner: RUST-CI-040
  A shared payload throttle and multi-transfer tests already exist. The remaining review is the call-site byte accounting for control/header/compressed data; no missing limiter is established.
- **A13-address-slot-cap — Verify per-address limits when upload slots are immediately available**
  Disposition: `new`. Owner: RUST-CI-041
  A three-client per-IP admission cap and tests already exist. Verify activation/reask/available-slot paths before treating the aMule per-address-slot item as a missing Rust feature.
- **A14-compression — Retain the existing compressed-format exclusion list**
  Disposition: `already-fixed`. Owner: Recorded disposition; no new implementation commitment.
  The Rust upload codec already skips common compressed containers with case-insensitive extension matching and tests. No new compression-skip feature is needed.
- **A15-live-rebind — Decide whether live TCP/UDP port rebind is a supported operation**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  API-mutable settings do not prove a safe live rebind path. Specify restart versus transactional rebind behavior, active-transfer impact and rollback before accepting this feature.
- **A16-share-exclusions — Review folder exclusion and office-file default scope**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/92
  Per-file exclusions/default ignore rules are already shipped; current custom tests deliberately reject paths. Folder-name patterns and blanket office-document exclusion change supported sharing semantics and need a separate decision.
- **A17-integrity-proof — Reuse trusted verification and upload invalidation work**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/249, https://github.com/emulebb/emulebb-rust/issues/151, https://github.com/emulebb/emulebb-rust/issues/254, https://github.com/emulebb/emulebb-rust/issues/255
  Corrupt-part nonadvertisement and nonserving proofs must compose with existing trusted MD4/AICH verification and upload invalidation. Do not assume the aMule Verify-Local-Data feature is entirely absent.
- **A17-periodic-reverify — Assess optional periodic re-verification separately**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Periodic user-scheduled re-verification is an additive behavior beyond current completion/upload invalidation work. Assess disk cost and authority before adding background scans.
- **A18-delete-completed — Retain the existing confirmed completed-file deletion API**
  Disposition: `already-fixed`. Owner: https://github.com/emulebb/emulebb-rust/issues/125
  The report's not-present assertion is stale. The handler already requires confirm=true and invokes the core file-deletion operation, with extensive delivery/deletion tests.
- **A19-obfuscation — Keep RC4 performance review separate from fallback protocol proof**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/95, https://github.com/emulebb/emulebb-rust/issues/31, https://github.com/emulebb/emulebb-rust/issues/164
  RC4 speed changes require measurement under the existing hot-path owner. Obfuscated-server timeout/fallback is a protocol transition to verify through the parity catalog, not an automatic downgrade feature.
- **frozen-ipv6 — Deduplicate the aMule IPv6 proposal into the focused decision**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  The aMule gap analysis does not supersede the IPv4-only product decision. Track the focused end-to-end dual-stack design and evidence plan.
- **frozen-utp-proxy — Review uTP and proxy transports only as explicit scope decisions**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  uTP and proxy transports are current non-goals. Record watch/design outcomes, not an accepted transport implementation or Beta 3 requirement.
- **frozen-chat-preview-sx1 — Retain current chat, preview and SX1 omissions unless deliberately reopened**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  Chat/CAPTCHA, peer preview and SX1 are reviewed permanent omissions. The user authorized tracking audit outcomes, not automatically shipping each aMule feature.
- **collection-magnet — Assess collection and URI convenience scope before adding formats**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Collection import/export is a non-goal; the meaning of aMule magnet handling for the eD2K product is not established. Capture a bounded format/use-case investigation.
- **quic-utp-watch — Track external transport adoption without a dormant implementation**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  QUIC/uTP groundwork in moving aMule is external evidence, not a proven production interoperability contract. Use a post-Client checkpoint and require peer adoption evidence before implementation.
- **nat-rendezvous — Assess server-coordinated NAT rendezvous as a two-side protocol decision**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Lugdunum/server-coordinated rendezvous is a possible LowID reachability direction. It requires an upstream interoperability contract and server support; do not patch the reference server into a private protocol oracle.
- **security-url-import — Bound authenticated server.met and nodes.dat URL imports**
  Disposition: `new`. Owner: RUST-BUG-176
  Core URL imports collect response.bytes without a byte ceiling; REST already restricts input to HTTP(S). RUST-BUG-176 owns bounded shared body/time/decoding handling, three redirects and pre-contact scheme checks, with HTTPS required at every trusted-bootstrap hop. Preserve authenticated operator LAN/loopback, allowed cross-host redirects and existing proxy behavior. Destination access remains an operator-authorized capability; no SSRF or DNS-rebinding shield is promised.
- **security-remote-paths — Decide the non-loopback REST filesystem authority contract**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  An authenticated remote-directory allow-list could narrow filesystem authority, but its absence is not proven unauthorized access. Review shared/category write semantics and local versus remote administration before adopting aMule's model.
- **security-native — Use existing native ownership and ABI work for LAN input safety**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9, https://github.com/emulebb/emulebb-rust/issues/163
  Native miniupnpc/PCP input hardening belongs to existing runtime-safety and mechanical ABI proof owners. Rust memory safety does not establish the C boundary is safe.
- **security-parser-freeze — Reduce applicable freeze/OOM advisory classes to deterministic bounds**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/31
  The applicable Kad freeze and decoder/downloader allocation assertions need concrete regressions under existing bounds/parity owners. The report incorrectly cites RUST-CI-032 as Kad flood work; current #258 owns dependency-aware early checks.
- **security-logs — Reconcile raw peer-log claims with existing logging hardening**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/34
  Raw wire logging claims require the diagnostics/privacy audit and existing regular-build logging contract. Preserve bounded safe retained evidence; do not assert the historical vulnerability exists solely from a wire_dump name.
- **security-rest-transport — Review non-loopback TLS and origin/host deployment guarantees**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Loopback defaults and API-key auth already exist. Assess reverse-proxy TLS, browser origin/host behavior and intended remote exposure, then identify concrete negative tests; do not silently add a TLS server or change supported deployment scope.
- **inapplicable-advisories — Record architecture-specific aMule advisories as inapplicable where proven**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  EC-port, guest-role and shell-event-command vulnerabilities do not directly map to this REST/headless architecture. Do not create imitation features or speculative fixes. Stats crashes and packet-memory classes still require concrete Rust evidence if observed.

### protocol_01.md

Source fingerprint (SHA-256): `35a02694c4b42df9b026cbba349eca8d09ad113a13997ca1b9a84905d04d666e`.

- **4.1 / 3 — Document shared-file browse refusal as an intentional product boundary**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/31
  Browse refusal and truthful no-view advertisement remain. This is a documentation/scope gap, not an interoperability defect or approval to implement peer browsing.
- **4.2 — Keep require-crypto advertisement consistent with supported settings**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/31
  The sole connect-options producer supports and optionally requests crypto; no supported require-crypto setting exists. Do not implement a hypothetical feature to eliminate a dead future path.
- **4.3 / 4.4 — Preserve verified stock layouts and registered protocol differences**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Verified constants and intentional SX1/chat/preview/IPv6 omissions are non-defects; moving aMule does not supersede frozen stock authority.
- **9.1 / 10.3 — Refresh exact-candidate Windows and Linux parity evidence**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/31, https://github.com/emulebb/emulebb-rust/issues/142, https://github.com/emulebb/emulebb-rust/issues/71
  Static audit is not candidate runtime proof. Reuse existing candidate certification and current-head evidence owners; other platforms are parallel and non-gating for the user's Beta 3 scope.
- **9.3-5 / 10.4 — Consolidate missing protocol boundary and state-machine goldens**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Hello/tag boundary, Kad framing, and flood exemptions belong to the existing canonical coverage owner. Reference freshness and unused decompiler material do not justify pulling support repos or adding server patches.

### reachability.md

Source fingerprint (SHA-256): `4ff6e5c32b10058543667c3a4c3f14a1ee6c8bafb558ba743a48ffdde33b9993`.

- **2.1 / 4.1 — Require authenticated or corroborated public-IP evidence for VPN Guard**
  Disposition: `new`. Owner: RUST-BUG-174
  Plain HTTP is unauthenticated and current guard logic accepts one allowlisted successful leg when the other fails. This contradicts the report's two-independent-success mitigation. Native VPN remains experimental; keep the fix separate from supported Docker/Gluetun Beta 3 certification unless that experimental mode is promoted.
- **2.2 — Public-IP response parsing is already octet-validated**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  The scanner already uses Ipv4Addr::parse and rejects invalid octets. Tolerance of markup is deliberate. Logging raw provider bodies would create unnecessary privacy risk.
- **2.3 — Correlate STUN mapping replies with the expected endpoint**
  Disposition: `new`. Owner: RUST-BUG-175
  The unconnected mapping probe checks source IP and random transaction ID but not source port. Endpoint matching is reasonable defense in depth; first confirm supported STUN response-source/alternate-port semantics.
- **2.4 / 4.2-3 — Native NAT ABI and musl/Android qualification already have owners**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/163, https://github.com/emulebb/emulebb-rust/issues/226, https://github.com/emulebb/emulebb-rust/issues/227
  ABI verification and native-target compile/runtime proof belong to existing FFI and platform items. Android is parallel and non-gating for Beta 3; do not replace proven C libraries with a narrower pure-Rust fallback to avoid qualification.
- **2.5-8 / 4.4 — Preserve generation-fenced reachability and verify remaining timer evidence**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/121
  Generation fences, mapping startup ordering and long-path boundaries are positive confirmations; unresolved timer/cross-client derivations belong to existing evidence work.

### rest-api.md

Source fingerprint (SHA-256): `14689a6e58d1df6cc6858917957cd14343849d7bfcfa921020068afbf6b9266f`.

- **3.1 — Bound URL-import responses and define destination policy**
  Disposition: `new`. Owner: RUST-BUG-176
  The confirmed defect is unbounded response collection. RUST-BUG-176 reuses format caps with bounded elapsed time, decoding and redirects, and validates each hop's scheme before contact. Authenticated imports retain HTTP/HTTPS, LAN/loopback, allowed cross-host redirects and existing proxies; automatic bootstrap stays HTTPS throughout. No address filtering, DNS pinning, proxy redesign or full SSRF/rebinding protection belongs to this bounded outcome.
- **3.2 — Disposition deliberate crash-test endpoint exposure**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Authenticated and explicitly confirmed crash testing is an intentional diagnostic operation. The assertion that it has no operational purpose is unsupported; do not remove a published endpoint automatically.
- **3.3 — Bound remote control-plane admission and authentication abuse**
  Disposition: `new`. Owner: RUST-BUG-177
  32-byte key validation exists under closed issue36. Failure throttling is optional additional hardening, not an established weak-key exposure. Consolidate with dos-resilience 2.4.
- **3.4 — Sanitize shareable diagnostic exports**
  Disposition: `design`. Owner: Design only; related private-warning owner RUST-BUG-178 / https://github.com/emulebb/emulebb-rust/issues/280
  Deeper revalidation: this authenticated endpoint deliberately exports exact private operator evidence, including its API key; raw contents are not a defect in that contract. A genuinely shareable allowlisted summary is a design proposal outside Beta3, with no new endpoint accepted. Related RUST-BUG-178 / #280 owns only the missing visible private-content warning and explicit acknowledgement.
- **3.5 — Keep health probe intentionally minimal**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Unauthenticated health response is deliberate; no new defect item.
- **evidence-gaps — Retain exact-head API and middleware evidence**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/31
  Route/auth/body/order and OpenAPI comparisons belong to existing certification/current-head evidence; audit inspection is not a pass.

### search.md

Source fingerprint (SHA-256): `e80a1758707e970509c1079be16fc93bfd9f8fc00721ff42436508cce0fe3e54`.

- **3.1 — Define supported search text syntax and rating criteria**
  Disposition: `new`. Owner: RUST-FEAT-067
  Stock input ergonomics are not wire incompatibility. Preserve structured Rust API; explicitly reject unsupported metatag/link text or define it, and assess rating criteria separately from inbound metadata issue29.
- **3.2 — Keep verified stock operator precedence**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Do not change unusual but stock-compatible precedence.
- **3.3 — Retain stock-compatible tolerant Kad string decoding unless parity proves a defect**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Strict UTF-8 rejection would change wire acceptance. Require stock malformed-string evidence before changing it.
- **3.4 — Preserve frozen Kad folding map**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Do not replace frozen network lowercase mapping with evolving Unicode data.
- **3.5 — Define local versus wire search normalization semantics**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/2
  Future live/index/hybrid semantics belong to Indexer owner; identical local and wire normalization is not automatically correct. Closed issue198 explicitly avoids offline-library search.
- **4.1 — Make non-Windows legacy encoding policy explicit**
  Disposition: `new`. Owner: RUST-FEAT-068
  Closed186 establishes negotiated Unicode/legacy behavior, not every locale. Optional explicit operator codepage policy can improve Linux legacy names; silent automatic charset guessing is not a default correctness fix.
- **4.2 — Preserve BOM, UTF8 and NFC handling**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/186
  No new action.
- **5.1 — Extend name repair only under explicit encoding policy**
  Disposition: `new`. Owner: RUST-FEAT-068
  Same outcome as4.1. Heuristic repairs must not corrupt already-correct names; also overlaps closed89 intent.
- **5.2 — Preserve bounded entity, percent and NFC repair**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/89
  No new action.
- **6.1 — Prove normalization-to-delivery path safety at one materialization boundary**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/242, https://github.com/emulebb/emulebb-rust/issues/164
  Physical proximity of helpers is not a vulnerability. Preserve original display names separately from filesystem-safe leaves; add end-to-end traversal/percent-decoding proof instead of sanitizing metadata early.
- **6.2 — Respect destination filename component and collision budgets**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/242
  Use existing BUG159; its current spec covers Windows UTF16/Linux byte units, suffixes and collision safety. No arbitrary universal240-character truncation.
- **6.3 — Specify DEL/C1 policy in delivered leaf allocator**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/242
  Extend existing leaf-safety acceptance with explicit terminal-hostile control policy; do not claim platform-invalid characters where OS permits them.
- **6.4 — Preserve no-clobber and reserved-name handling**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/242
  No new action; retained invariants for BUG159.

### secure-ident.md

Source fingerprint (SHA-256): `821dd6b34c8177e0148b32a398f2b1f9e8f862624c8e0a3274baee2f3700338a`.

- **4.1 — Enforce the stock incoming secure-ident public-key size limit**
  Disposition: `new`. Owner: RUST-BUG-168
  The inbound decoder verifies its byte prefix but does not apply the existing 80-byte stock cap before RSA parsing. The outbound key cap does not cover this path.
- **4.2 — Preserve the reviewed per-challenge secure-ident attempt limit**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/196
  Closed BUG-145 deliberately permits one attempt per challenge/IP and preserves the first verdict. No demonstrated unbounded repro justifies changing its contract to a lifetime latch.
- **4.3 — Honor negotiated secure-ident V2 support and LowID challenge addressing**
  Disposition: `new`. Owner: RUST-BUG-169
  The V2-shaped signature is decoded and verified without checking the peer's advertised V2 capability. This is bounded leniency, not proof of authentication bypass.
- **4.4 — Honor negotiated secure-ident V2 support and LowID challenge addressing**
  Disposition: `new`. Owner: RUST-BUG-169
  The REMOTECLIENT reconstruction falls back to unspecified IPv4 and the download handler passes no external address. Verify stock LowID/local-address fallback and implement the actual reachable edge alongside V2 handling.
- **4.5 — Unknown secure-ident level does not justify an unproven wire change**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  The zero-capability V1/V2 difference is theoretical and lacks a reachable conformant-peer failure. Document or revisit with a fixture rather than changing crypto selection incidentally.
- **4.6 — Standalone key-file write is not the daemon's persistence path**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  Production secure-ident secrets are persisted in SQLite under the owner-only profile directory. The report's public helper fs::write observation does not establish a daemon private-key exposure.
- **5 / 7 — Secure-ident weak primitives and remaining cross-client evidence**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/195, https://github.com/emulebb/emulebb-rust/issues/226, https://github.com/emulebb/emulebb-rust/issues/227
  Weak stock RSA/SHA1 is an accepted interoperability boundary. Key pinning has a closed owner; native-target build/runtime and cross-client proof have existing owners.

### server-reply.md

Source fingerprint (SHA-256): `5fd754643ac3b8554c21610282041da93846e1d32c287c256656555ae89a0949`.

- **3.1 — Callback peer hash disagreement is already rejected downstream**
  Disposition: `already-fixed`. Owner: Recorded disposition; no new implementation commitment.
  Server-routed expected hash reaches the callback session; outbound HELLO mismatch closes the session before identity application. The audit did not open that owner and does not establish a missing defense.
- **3.2 — Callback IP filters and bans already run before dialing**
  Disposition: `already-fixed`. Owner: Recorded disposition; no new implementation commitment.
  All callback routes converge on admission before connect; IP and user-hash bans are checked and dedicated no-dial regressions exist.
- **6.2-4 — Prove source admission and legacy server UDP replies under canonical evidence**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Untraced downstream source filtering and partially reviewed UDP bodies are evidence gaps, not confirmed vulnerabilities.
- **4.1-8 — Verified server reply layouts need no corrective tickets**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  Existing IDCHANGE offsets, found-sources user-hash bit, trailing-more byte, and bounded inflate behavior were positive confirmations.

### testing-harness.md

Source fingerprint (SHA-256): `e9feadd86f3ae7495a0677d536c296e0c1250cb191db9324cd4da25ca9136ab2`.

- **kad-catalog-domains — Add named Kad bootstrap, HELLO and maintenance coverage**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/31
  The catalog still lacks independently named bootstrap/three-way-HELLO/maintenance domains. Extend the existing parity-consolidation owner rather than open a second harness program.
- **wire-goldens — Complete exact-byte ownership for remaining digest-only records**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  The blanket claim that all records use FNV-only evidence is stale: newer stock records already carry fixtureBase64 and SHA-256 validation. Reconcile remaining FNV records and explicit full-frame golden ownership within CI-031.
- **riff-regression — Add adversarial RIFF nesting regression with the owning parser fix**
  Disposition: `new`. Owner: RUST-BUG-181
  The recursive LIST parser has no visible depth budget. The regression belongs with the media-audit defect, not a separate competing implementation.
- **crypt-capability-regression — Pin crypt-layer capability bits through the protocol owner**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164, https://github.com/emulebb/emulebb-rust/issues/31
  requires_crypt_layer is still hardcoded to zero. Resolve the behavior claim with the protocol audit and stock authority before changing the bit; add the exact capability regression in the canonical parity slice.
- **decoded-filename-regression — Prove decoded separators cannot escape download delivery**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/242
  Literal-separator sanitization exists. Add the specific normalization-to-delivery regression for percent-encoded separators; absence of that test alone does not establish traversal. Parent reconciliation: add this delivery-boundary regression to RUST-BUG-159 rather than creating a competing test-only owner.
- **callback-latch — Retain the existing per-IP direct-callback limiter tests**
  Disposition: `already-fixed`. Owner: Recorded disposition; no new implementation commitment.
  The claimed missing limiter/regression is contradicted by current source: production enforces a 180-second per-IP window and tests cover repeated requests and expiry.
- **aich-regressions — Attach canonical framing and deterministic trust regressions to AICH work**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/248, https://github.com/emulebb/emulebb-rust/issues/249, https://github.com/emulebb/emulebb-rust/issues/250, https://github.com/emulebb/emulebb-rust/issues/252
  Trailing recovery bytes and equal-weight trust tie behavior should be reconciled with existing AICH admission/provenance/reuse items and the separate AICH audit.
- **settings-test-matrix — Review concrete settings edge cases before adding tests**
  Disposition: `not-supported`. Owner: Recorded disposition; no new implementation commitment.
  Raw files-with-tests counts do not establish coverage quality. Inventory malformed values, unknown keys and retired fields, then add only missing behavior cases. Parent disposition: no specific missing behavior case was established; file/test counts are insufficient grounds for a new implementation commitment.
- **rest-test-density — Do not infer a REST defect from stale test-density counts**
  Disposition: `not-supported`. Owner: https://github.com/emulebb/emulebb-rust/issues/15, https://github.com/emulebb/emulebb-rust/issues/157
  Current REST tests include dedicated body, query, path, category and route suites, plus conformance ownership. Track specific untested behaviors through the REST audit; a low historical file count is not an actionable defect.
- **media-fuzz — Add a bounded media-metadata fuzz target**
  Disposition: `new`. Owner: RUST-BUG-181
  The fuzz workspace still has no media-metadata target. Share ownership with the fuzz/media audit and ensure recursion/size budgets precede continuous fuzzing.

### udp-reask.md

Source fingerprint (SHA-256): `29f034e72a8b354419ece0380bd488c48f2573a25ac9ebb35f303fc80e3bd011`.

- **2.1 — Buddy relay already prepends requester endpoint**
  Disposition: `already-fixed`. Owner: https://github.com/emulebb/emulebb-rust/issues/200, https://github.com/emulebb/emulebb-rust/issues/1
  Current production relay emits requester IP/port plus body[16..], equivalent to stock's overwrite-and-forward from offset 10. The report incorrectly treats transport as deferred and tail storage as the complete relay packet.
- **2.1 documentation citation — Correct the stock buddy-relay implementation citation**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Rust's explanatory memcpy expression is an equivalent reconstruction, not the literal source expression. Clarify the citation during canonical protocol-evidence work without changing wire behavior.
- **2.2 — Direct-callback rate limiting already exists in core**
  Disposition: `already-fixed`. Owner: Recorded disposition; no new implementation commitment.
  The receive path calls the shared limiter before callback dispatch; the audit searched the wrong module.
- **4.1-4 / 5.3 — UDP reask timer and obfuscation coverage belongs to existing evidence owner**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/164
  Failure-ratio fallback is already implemented with total>3 and failed/total>0.3; remaining transport/obfuscation validation is evidence work rather than implementing a missing timer.

### webui.md

Source fingerprint (SHA-256): `b7341c5ddc571c8ac0b919c913169845c3719144c1ef1409a194d6a3e2401ccd`.

- **3.1 — Document authenticated browser transport boundary**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/36
  Session storage/header bearer auth is intentional. Preserve loopback/default security and document trusted TLS termination for external access; optional cookie auth is separate design, not a bug.
- **3.2 — Handle malformed transfer-event frames predictably**
  Disposition: `new`. Owner: RUST-BUG-179
  One malformed frame terminates the stream and outer UI reconnects. Add explicit per-frame/stream failure behavior with a regression; no claim of security compromise.
- **3.3 — Retain documented lenient JSON error decoding**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Leading-object/array fallback is not a confirmed defect. Avoid changing error behavior just for stricter content-type parsing.
- **3.4 — Keep API key mandatory in first-party UI**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/36
  No-auth loopback is not a supported mode; no task to add it.
- **3.5 — Keep development toolchain updates under existing dependency controls**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/46
  New major development tools alone do not establish a defect; dependency updates remain evidence-driven.

### LIBPCPNATPMP-CONSUMER-REFACTOR-AUDIT-2026-11-09.md

Source fingerprint (SHA-256): `c664c71e0d3bfdca163bd09d6de516c3559aed1512da4dae12e7481ec5a15f52`.

- **consumer-adapters — Move fork-only PCP ownership and route integration into consumers**
  Disposition: `new`. Owner: RUST-REF-023
  Fork-specific init, server-admission and free APIs remain in use. A consumer C adapter can own matched-CRT frees and explicit route filtering while keeping upstream sources unchanged. Context destruction must be tied to the exact upstream revision.
- **gateway-inventory-decision — Choose the consumer gateway inventory boundary**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Automatic discovery cannot be replaced by requiring an explicit PCP server. Choose an isolated adapter around pinned internal getgateways, or supported platform inventory APIs/dependency; do not copy upstream routing code.
- **upstream-init-leak — Verify and upstream the PCP socket-initialization allocation leak**
  Disposition: `new`. Owner: RUST-BUG-183
  The context allocation precedes socket creation; the failing socket path returns null without returning ownership. The existing fork does not establish a fix. Confirm against the pinned upstream revision and prefer a small upstream correction.
- **route-change-confinement — Define whether mappings need continuous route confinement**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Both existing custom filtering and the proposed consumer replacement validate selection-time routing only. Stronger confinement after a route change is a separate requirement, not an existing guarantee.
- **native-proof — Reuse native ABI and runtime-safety proof owners**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9, https://github.com/emulebb/emulebb-rust/issues/163
  Adapter work must compose with existing native layout and runtime-safety items. Desktop/musl/Android compile evidence does not alone prove allocator lifecycle correctness; MFC changes require a separate bounded consumer assignment.

### PM.md

Source fingerprint (SHA-256): `820734c874ea3328246a73639b3bfb62e2ce7e1a2b183938c83c65e9f98da63d`.

- **templates — Add issue and PR evidence templates**
  Disposition: `new`. Owner: RUST-CI-036
  No issue or PR templates were found. Standardize scope, evidence, attribution and wire-impact prompts without requiring users to invent an unallocated stable ID.
- **release-checklist — Reuse the existing Beta 3 certification checklist**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/142
  The requested release checklist already exists as the candidate certification item. Update its platform scope under the user's Windows/Linux Beta 3 decision; do not create a second release authority.
- **changelog — Keep existing commit-derived release notes**
  Disposition: `already-fixed`. Owner: https://github.com/emulebb/emulebb-tooling/issues/32
  The proposed changelog script is already implemented in the owning Rust release helper and invoked by release preparation. A new tooling implementation would duplicate it.
- **audit-register — Record audit dispositions in the owning backlog**
  Disposition: `new`. Owner: RUST-CI-034
  Use the parent audit-intake outcome rather than a parallel PM tracker. Keep one issue/spec per independently deliverable finding, with evidence, disposition and deduplication.
- **board-triage — Define a concise triage cadence and Project field mapping**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  Review labels, status transitions and a saved triage view against Project #3. A weekly review is a process proposal, not authorization to create a scheduled automation.
- **pm-digest — Produce a read-only issue and release-readiness digest**
  Disposition: `new`. Owner: RUST-CI-037
  A persisted PM command can project GitHub state into a concise digest and readiness view. It must cite owning issues and report uncertainty rather than establish another tracker.
- **pm-skill — Assess a thin coordinator skill around persisted PM tooling**
  Disposition: `design`. Owner: Recorded disposition; no new implementation commitment.
  A skill is a possible operator interface after the persisted digest command proves useful. It should delegate to canonical scripts and existing policy.
- **parallel-policy — Continue the existing parent-coordinated checkout outcome**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-build/issues/28
  The audit's single-PR posture is superseded by the explicitly authorized parallel-workstream project. Build issue #28 and Tooling PR #156 already own the checkout, hook, lock and delivery-policy changes; preserve them.

### unsafe1.md

Source fingerprint (SHA-256): `aa7184b110d9ebcb5257bdc37bf091038af0254b5ef7a6d7d48b56ffbfaec10d`.

- **inventory — Keep justified platform FFI and preserve Linux safe rename**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/9, https://github.com/emulebb/emulebb-rust/issues/163
  Unsafe counts are not backlog units. Windows/macOS primitives and reference NAT providers remain intentional.
- **MoveFileExW — Consolidate Windows move wrappers only where semantics agree**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Duplicate implementation can be reviewed under REF006, but no-replace publication must never inherit replacement flags.
- **route-table — Prove Win32 route-table slice ownership and bounds**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Dedicated zero/multi-row/error/drop tests are meaningful FFI safety evidence; no replacement of windows-sys layouts suggested.
- **CSP — Review inline-style CSP as a separate browser hardening decision**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/36
  Do not remove style allowance without checking actual UI styles. Distinguish style policy from script execution and from Rust unsafe.

### unsafe2.md

Source fingerprint (SHA-256): `9cafe51d81521c82de0472ebd5165d1b7e28116fa61c7709b969862ad081c1ab`.

- **correction-1 — Keep reference NAT libraries; prove their ABI and ownership**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/22, https://github.com/emulebb/emulebb-rust/issues/163, https://github.com/emulebb/emulebb-rust/issues/9
  Pure-Rust alternatives do not establish equal PCP/NAT-PMP/UPnP behavior. Existing providers remain; ABI and leak-free ownership proof belong to existing items.
- **correction-2 — Keep Windows ACP conversion rather than replacing it with widestring**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/186
  This correction does not rule out an explicit non-Windows legacy codepage policy from search4.1. Preserve Windows behavior.
- **recommendation-1 — Consolidate Windows move wrappers only where semantics agree**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Same owner and outcome as unsafe1; do not create duplicate tickets.
- **recommendation-2 — Prove Win32 route-table slice ownership and bounds**
  Disposition: `existing`. Owner: https://github.com/emulebb/emulebb-rust/issues/9
  Same owner and outcome as unsafe1; do not create duplicate tickets.
- **recommendation-3 — Review inline-style CSP as a separate browser hardening decision**
  Disposition: `design`. Owner: https://github.com/emulebb/emulebb-rust/issues/36
  Same nonblocking design decision as unsafe1; preserve UI behavior.
