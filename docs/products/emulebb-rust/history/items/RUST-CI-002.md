---
id: RUST-CI-002
workflow: local
title: Rationalize and close the core stock-eMule parity evidence gate
status: DONE
priority: Major
category: ci
labels: [parity, tests, evidence, release]
milestone: phase-0
created: 2026-06-19
source: core parity closure review (2026-06-19)
---

# RUST-CI-002 - Rationalize and close the core stock-eMule parity evidence gate

## Summary

Close the emulebb-rust **core client parity** lane against stock eMule wire and
core behavior with one authoritative, reproducible evidence gate. emulebb-mfc
can remain a frozen comparison witness, but it is no longer the product parity
target. The close target is core eD2K/Kad client behavior, deterministic local
cross-client interoperation, and a manual public-network smoke witness. It is
not the full Phase 0 product gate: REST API evolution, indexer, Arr/Torznab,
Docker, and SSE remain separately tracked. The automated tunnel-down leak test
is a separate release-safety gate and is complete under `RUST-FEAT-005`.

This item exists to prevent the parity closure decision from being spread across
ad hoc reports. It owns the close checklist, evidence freshness rule, and test
rationalization.

## Current State

**Closed 2026-09-27.** The authoritative `emulebb-rust-overnight` campaign
passed all seven commands and all eight required blocking evidence rows. The
retained result binds Rust `3a162136`, build-tests `9865967`, build `7eccd29`,
tooling `fc9fb53`, MFC `9466ece`, and goed2k-server `ea5d4b2`. The only Rust
status line was the operator-owned, deliberately untracked `TOMORRAWZ.MD`; the
tracked Rust tree was clean. The archive-only documentation commit follows the
captured tooling head and does not change the tested implementation or harness.

The separate targeted Rust/eMuleBB UDP-reask proof also passed: both configured
MFC slots were occupied, a third Rust peer was observed waiting, its queued TCP
session detached, and its UDP reask received an acknowledgement. This closes
`RUST-FEAT-001` without weakening MFC production anti-abuse behavior or Rust's
stock production reask cadence.

The 2026-09-28 server-only reconciliation below also closes every finding in
the pre-fix `TOMORRAWZ.MD` audit. Its result is 17 fixed, four stock-aligned
omissions, and zero deferred server findings. No new defect or source change was
required.

The 2026-09-28 peer TCP and transfer reconciliation below disposes every peer
finding in the same pre-fix audit. Its result is ten fixed findings, four
truthfully omitted features, and one accepted non-wire pacing defer. The audit
found and fixed one additional capability-contract defect: legacy
`OP_EMULEINFO` still advertised SX1 v3 even though the runtime is deliberately
SX2-only. Rust commit `d9f6ae91` clears that legacy claim and adds direct
capability-bit coverage. A refreshed overnight campaign passed all seven
commands and all eight blocking evidence rows at that Rust head, and a fresh
Rust/eMuleBB UDP-reask witness also passed.

The 2026-09-30 Kad and client-UDP reconciliation below disposes every scoped
Kad finding in the pre-fix audit. Its result is six fixed findings, one
stock-aligned omission, one accepted display-only platform boundary, and the
explicit IPv4-only product boundary. The current-head stock protocol oracle
passed all five Rust proof packages that own this surface.

`RUST-BUG-001` remains distinct Phase 0 CI-isolation debt. Forward work in
`RUST-FEAT-002`, `RUST-FEAT-004`, `RUST-FEAT-006`, and `RUST-FEAT-007` is not a
core stock-eMule parity blocker. The regular/manual campaign remains
informational; the overnight campaign is the sole authoritative automated
close gate. Public-network smoke remains optional and nonblocking, and aMule
remains a retired offline reference unless the operator explicitly reopens it.

## Intended Shape

Use `emulebb-rust-overnight` as the authoritative core parity close campaign.
The regular/manual campaign can stay informational unless its manual evidence
rows are converted to JSON-backed evidence and evaluated consistently.

The close gate is:

1. `python -m emule_workspace workspace-status`
2. `python -m emule_workspace validate`
3. `python tools\check_rust_client_policy.py` from `repos\emulebb-rust`
4. Build the MFC release and tracing-harness executables through
   `repos\emulebb-build` orchestration.
5. `python -m emule_workspace test release-campaign --campaign emulebb-rust-overnight --execute --continue-on-failure`
6. Targeted UDP reask proof:
   `python scripts\emulebb-rust-reask-cross-client.py --lan-bind-addr %X_LOCAL_IP%`
7. Optional long-form byte-level confirmation with
   `emulebb-rust-reask-capture-emulebb.py`.
8. Optional public hide.me live-wire smoke using operator-local inputs. Accept it
   only when both obfuscation modes pass with VPN-bound P2P, eD2K/Kad
   connectivity, packet diagnostics, source-exchange evidence, and a completed
   download.

## Scope Constraints

- Core parity closure does not claim full Phase 0 completion.
- Public live-wire remains manual and nonblocking. The completed
  `RUST-FEAT-005` tunnel-down gate is deterministic local safety proof and does
  not turn public-network smoke into a core-parity blocker.
- The July 2026 CI-047 retirement removed aMule launch/control adapters and
  campaign entry points. Current workspace policy treats aMule as an offline
  source/fixture reference, not a release gate; reopening it requires a separate
  operator decision.
- emulebb-mfc source-seam, community/reference parity, VM proof, and
  public-network live proof stay out of the forward suite gate unless explicitly
  requested.
- All public-network proof must follow the workspace live-test network policy
  and must not commit operator-owned live search terms, media names, private
  addresses, or machine paths.

## Acceptance Criteria

- [x] Overnight campaign evidence is regenerated after the current Rust HEAD and
      current MFC/tracing-harness build inputs.
- [x] The retained campaign result records the Rust overnight local client
      pytest proof, source-anchored stock oracle with executable Rust proof
      packages, local ED2K protocol-combination matrix, private parity modules,
      Rust/eMuleBB bidirectional transfer, Rust/Rust bidirectional transfer,
      total parity audit, and REST contract conformance as passed.
- [x] The close decision explicitly states that `RUST-FEAT-002`,
      `RUST-FEAT-004`, `RUST-FEAT-006`, and `RUST-FEAT-007` are forward Phase 0
      or later work, not core stock-eMule parity blockers.
- [x] `RUST-FEAT-005` is closed with a blocking dynamic tunnel-down leak-test;
      that release-safety gate remains distinct from core parity closure.
- [x] The regular release campaign is either documented as informational or its
      manual rows are converted to JSON evidence so it cannot contradict the
      authoritative overnight gate.

## ED2K Server Audit Reconciliation (2026-09-28)

### Comparison Basis

This is the narrow server-protocol reconciliation requested after the original
audit. It does not re-open peer TCP, file transfer, Kad, REST, WebUI, packaging,
or beta-release readiness.

- Old audit snapshot: emulebb-rust
  `34b2bc0673ac28931144a70b5d670d6d04511500`.
- Reconciled implementation: emulebb-rust `main` at
  `3a162136e23b4c41f490d0a93fb29853aaaa5d23`.
- Stock comparison: `emulebb-community-baseline` branch
  `baseline/community-0.72a`, especially `srchybrid/Opcodes.h`,
  `ServerSocket.cpp`, `UDPSocket.cpp`, `DownloadQueue.cpp`, and
  `SharedFileList.cpp`.
- The old snapshot is an ancestor of the reconciled head. Every implementation
  commit named below is also an ancestor of that head.
- The active `policy/rust-client-omissions.toml` has no server-specific entry.
  `rust-client-omissions-history.toml` records
  `server-obfuscation-metadata-non-config`,
  `legacy-server-udp-global-callback`, and
  `legacy-server-udp-list-exchange` as fixed history.
- Authoritative current-head campaign:
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\release-campaign-runs\20260927T171451Z-emulebb-rust-overnight\release-campaign-run-result.json`.
  It passed all seven commands and all eight blocking evidence rows, including
  the stock protocol oracle, local eD2K protocol-combination matrix, private
  eD2K client/server modules, cross-client exchange, and total eD2K parity
  audit.

### Surface Verdict

| Required surface | Verdict | Primary proof |
|---|---|---|
| Login and HighID/LowID | PASS | `login_request_reuses_client_id_and_configured_nickname`; `server_state_reports_low_id_as_firewalled`; `old_server_offer_files_use_assigned_high_id_behind_nat`; `old_server_offer_files_hide_endpoint_for_low_id_client` |
| TCP and UDP search | PASS | `background_search_channel_round_trips_results`; `udp_keyword_search_request_uses_legacy_opcode_without_extensions`; `udp_keyword_search_accepts_replies_from_any_queried_server_ip` |
| TCP and UDP source requests | PASS | `background_source_batch_sends_one_complete_frame_per_target`; `udp_source_request_without_legacy_extension_encodes_exactly_one_hash`; `background_udp_source_search_preserves_responding_server` |
| Obfuscation fallback and persisted metadata | PASS | `server_transport_attempts_fall_back_once_then_succeed`; `server_udp_status_persists_and_stale_keys_are_not_reused` |
| Legacy UDP variants | PASS with stock-aligned omissions | `global_callback_matches_stock_layout`; `server_list_request_variants_match_stock_layouts`; definitions-only `OP_INVALID_LOWID` remains omitted |
| Priorities and automatic connection | PASS | `configured_servers_use_stable_stock_priority_order`; `automatic_static_only_filters_without_reordering`; `explicit_target_bypasses_automatic_static_only_filter` |

### Finding Dispositions

The outcome vocabulary is intentionally exact:

- **Fixed** means the old difference is implemented on the reconciled head and
  has a named regression test.
- **Omitted (stock-aligned)** means stock 0.72a itself only defines the opcode
  or labels it deprecated, with no client send/receive implementation. Rust
  does not advertise the behavior. This is not an active protocol divergence.
- **Deferred** would mean a valid difference remains accepted for later work.
  There are no deferred findings in this server-only audit.

| ID | Old finding | Disposition |
|---|---|---|
| A1-01 | TCP `SEARCH_USER` | Omitted (stock-aligned) |
| A1-02 | TCP `DISCONNECT` | Omitted (stock-aligned) |
| A1-03 | Deprecated server chat/query/join/user-list behavior | Omitted (stock-aligned) |
| A1-04 | UDP invalid-LowID | Omitted (stock-aligned) |
| A1-05 | UDP global callback | Fixed |
| A1-06 | UDP server-list exchange | Fixed |
| A1-07 | Malformed multi-file TCP source batching | Fixed |
| A1-08 | No plaintext fallback after failed obfuscated connection | Fixed |
| A1-09 | Legacy UDP source batching ignores capability | Fixed |
| A1-10 | Search-result source identity and metadata discarded | Fixed |
| A1-11 | No 64-bit search capability downgrade | Fixed |
| A1-12 | Incomplete UDP status, obfuscation, and persisted metadata | Fixed |
| A1-13 | Wrong old-server offer endpoint behind NAT | Fixed |
| A1-14 | Incomplete files offered with complete-file sentinel | Fixed |
| A1-15 | Offers omit rating and media tags | Fixed |
| A1-16 | Search criteria omit stock media filters | Fixed |
| A1-17 | Search-result framing rejects stock trailing data | Fixed |
| A1-18 | `OP_SERVERMESSAGE` omits dynamic-IP/version/error semantics | Fixed |
| A1-19 | Server descriptions omit dynamic host/version/auxiliary ports | Fixed |
| A1-20 | Login always sends client ID zero and fixed nickname | Fixed |
| A1-21 | Static-server priority and automatic-connect behavior absent | Fixed |

### Fixed Finding Evidence

1. **A1-05 — global callback.** Commit
   `2d53785b9c1595d97c6831e17218a9414b87c658` completes the old cross-server
   callback route. Tests: `server_callback_requires_self_high_id_and_a_source_server`,
   `callback_route_uses_connected_tcp_or_cross_server_udp`,
   `global_callback_matches_stock_layout`,
   `global_callback_sends_exact_plaintext_datagram_to_server_udp_port`, and
   `global_callback_rejects_a_high_id_target_before_network_io`.
2. **A1-06 — server-list exchange.** Commit
   `2d53785b9c1595d97c6831e17218a9414b87c658` implements both stock request
   layouts and opt-in discovery. Tests: `server_list_request_variants_match_stock_layouts`
   and `udp_server_list_request_is_opt_in_and_emits_discovery`.
3. **A1-07 — TCP source framing.** Commit
   `f60e8994cab1ad69f02625a3c41aed4be3af0750` sends one complete ED2K frame per
   target. Tests: `background_source_batch_sends_one_complete_frame_per_target`
   and `source_request_decoder_recovers_fragmented_coalesced_frames`.
4. **A1-08 — bounded plaintext fallback.** Commit
   `0332b7427a22a5b685a3a7fe39032edf8e235305` adds one session-scoped fallback
   without weakening required-crypt policy. Tests:
   `server_transport_plan_falls_back_to_the_ordinary_endpoint_once`,
   `server_transport_plan_never_downgrades_required_crypt`,
   `server_transport_attempts_stop_after_obfuscated_success`,
   `server_transport_attempts_fall_back_once_then_succeed`, and
   `server_transport_attempt_state_is_bounded_and_session_scoped`.
5. **A1-09 — legacy UDP source capability.** Commit
   `5b1abd0147d6dbd0d4648cf3dd866e350b53b32c` limits non-extended legacy
   requests to one hash while retaining negotiated extended batching. Tests:
   `udp_source_request_without_legacy_extension_encodes_exactly_one_hash`,
   `udp_source_request_batch_encodes_legacy_hashes`, and
   `udp_source_request_batch_encodes_getsources2_sizes`.
6. **A1-10 — complete search-result identity and metadata.** Commits
   `77ad613879413baba7635f6488a4cac2c0a9a818` and
   `76e65c86a234182e47f5080d38d9902faf85ec2d` retain source ID/port, complete
   sources, rating, AICH, and folder metadata through core and persistence.
   Tests: `search_results_decoder_preserves_source_identity_and_metadata`,
   `ed2k_result_maps_source_identity_and_complete_sources`,
   `high_id_search_source_becomes_immediate_transfer_hint`,
   `low_id_or_incomplete_search_source_is_not_dialed_directly`, and
   `legacy_source_metadata_remains_readable`.
7. **A1-11 — 64-bit search downgrade.** Commit
   `0064791549b74ceb460ce7d495aba0ed5fb5c230` gates wide numeric terms on the
   destination server capability. Tests:
   `large_size_uses_64bit_numeric_form_only_for_capable_server` and
   `uint32_boundary_remains_32bit_for_every_server`.
8. **A1-12 — UDP status, obfuscation, and persistence.** Commits
   `8c501f86a700c836aa4dcb72231cad7290276e39` and
   `c046c313b68815c3fab4ea1eb922972c62784ece` retain UDP flags, limits, LowID
   count, obfuscation ports, public-IP-bound UDP key, status/description
   metadata, and crypt-ping lifecycle. Tests:
   `server_udp_status_persists_and_stale_keys_are_not_reused`,
   `crypt_ping_timeout_falls_back_and_persists_status_before_description`,
   `udp_key_is_usable_only_for_its_bound_public_ip`,
   `decode_harvests_obfuscation_ports_key_and_default_ports`,
   `server_status_refreshes_key_binding_ports_and_persistence_event`, and
   `server_udp_crypt_ping_uses_temporary_challenge_key`.
9. **A1-13 — NAT-safe old-server offers.** Commit
   `abe00faf34d9f2826f55c4f48d981415ccb367cf` publishes the server-assigned
   HighID instead of the local bind address and hides the endpoint for LowID.
   Tests: `old_server_offer_files_use_assigned_high_id_behind_nat` and
   `old_server_offer_files_hide_endpoint_for_low_id_client`.
10. **A1-14 — incomplete-file sentinel.** Commit
    `7bf5fbe721c2a0117626c7e1a06865c5e96d2e74` publishes part files with the
    stock incomplete sentinel. Test: `offer_files_uses_incomplete_sentinel_for_part_files`.
11. **A1-15 — offer rating and media tags.** Commits
    `7bf5fbe721c2a0117626c7e1a06865c5e96d2e74` and
    `e859ef43be80d988eb33808102f6ff24f3829c71` publish non-zero ratings and the
    stock media subset. Tests: `offer_files_publishes_nonzero_rating`,
    `old_server_offer_files_use_long_media_names_and_string_length`,
    `offer_files_publish_stock_media_subset`, and
    `shared_catalog_media_survives_runtime_restart_from_source_path`.
12. **A1-16 — media search constraints.** Commit
    `3f4e6aa76b789f1764097338b9b082740fe79478` maps title, album, artist,
    bitrate, length, and codec filters into stock search leaves. Tests:
    `media_search_fields_map_to_server_criteria` and
    `media_constraints_match_stock_leaf_order_and_tag_ids`.
13. **A1-17 — stock trailing search data.** Commit
    `93b839fef9a63ddd85a35614cf0c45d7bdca2155` tolerates diagnostic trailing
    data without weakening bounded decoding. Test:
    `search_results_decoder_tolerates_stock_diagnostic_trailing_data`.
14. **A1-18 — server-message semantics.** Commit
    `c046c313b68815c3fab4ea1eb922972c62784ece` applies error/warning logging,
    version extraction, and validated dynamic-host updates. Tests:
    `decodes_stock_server_message_semantics` and
    `version_prefix_is_case_insensitive_and_ipv4_dynip_is_rejected`.
15. **A1-19 — complete server descriptions.** Commit
    `c046c313b68815c3fab4ea1eb922972c62784ece` decodes and persists dynamic
    host, string/integer version, and auxiliary ports. Tests:
    `decodes_challenge_tag_response_and_rejects_mismatch`,
    `dynamic_host_rejects_ipv4_empty_and_overlong_values`, and
    `udp_server_description_metadata_updates_the_persisted_server`.
16. **A1-20 — reusable login identity and nickname.** Commit
    `62a2e16707c7e91b003b8302b1443f23f831c5b0` reuses the assigned client ID and
    sends the bounded configured nickname. Tests:
    `login_request_reuses_client_id_and_configured_nickname`,
    `configured_ed2k_nickname_reaches_runtime_config`, and
    `server_nickname_trims_defaults_and_bounds_operator_input`.
17. **A1-21 — priority and automatic connect.** Commit
    `1ebca8210f1d2e19f64196710753f36ce385409b` adds stable stock priority order,
    static-only automatic filtering, and explicit-target bypass. Tests:
    `automatic_static_only_filters_without_reordering`,
    `explicit_target_bypasses_automatic_static_only_filter`,
    `configured_endpoints_are_ordered_before_same_priority_persisted_metadata`,
    `configured_servers_use_stable_stock_priority_order`, and
    `disabling_server_priorities_preserves_configured_order`.

### Stock-Aligned Omission Evidence

The four omitted entries are not unimplemented stock behavior:

- Stock `Opcodes.h` defines `OP_DISCONNECT` as "not verified", marks the
  server chat/query/join family deprecated and unsupported by servers, and only
  defines `OP_SEARCH_USER`, `OP_USERS_LIST`, and `OP_INVALID_LOWID`.
- A source scan of stock `ServerSocket.cpp`, `ServerConnect.cpp`, and
  `UDPSocket.cpp` finds no send or receive case for those definitions.
  `UDPSocket.cpp` sends unknown server-UDP opcodes to its default diagnostic
  path, so stock itself does not process `OP_INVALID_LOWID`.
- Rust at audit commit `3a162136e23b4c41f490d0a93fb29853aaaa5d23`
  likewise does not advertise or emit these definitions; unsupported server
  TCP packets reach the bounded diagnostic ignore path in
  `ed2k_server/packet_handler.rs`.
- Test reference: not applicable because there is no stock behavior to port or
  advertise. The source absence was checked on both sides; the implemented
  legacy UDP behaviors have the explicit tests listed for A1-05 and A1-06.

### Close Decision

The old server audit has no remaining deferred item and exposed no new
reproducible defect on current `main`. This closes the narrow server-parity
reconciliation only. It does not imply that unrelated CI, WebUI, soak,
packaging, or final beta gates are complete.

## Peer TCP and Transfer Audit Reconciliation (2026-09-28)

### Comparison Basis

This is the narrow peer-protocol and transfer reconciliation requested after
the server audit. It covers hello/capability tags, SX2, queue and UDP reask,
32/64-bit transfer, hashset/AICH/ICH, secure identification, A4AF, upload
scheduling, and duplicate handling. It does not close Kad, REST, WebUI,
packaging, or the final beta release gate.

- Old audit snapshot: emulebb-rust
  `34b2bc0673ac28931144a70b5d670d6d04511500`.
- Reconciled implementation: emulebb-rust `main` at
  `d9f6ae918bf2e8786d39b61a6d3eef8d62da20af`.
- Stock comparison: `emulebb-community-baseline` branch
  `baseline/community-0.72a`, especially `Opcodes.h`, `BaseClient.cpp`,
  `DownloadClient.cpp`, `UploadClient.cpp`, `ListenSocket.cpp`, and
  `KnownFile.cpp`.
- The old snapshot is an ancestor of the reconciled head. Every implementation
  commit named below is also an ancestor of that head.
- The active omission registry records SX1, peer chat/captcha, and preview as
  approved drops, plus the conservative five-second connection window as a
  nonblocking post-beta defer.
- Authoritative current-head campaign:
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\release-campaign-runs\20260928T202338Z-emulebb-rust-overnight\release-campaign-run-result.json`.
  It passed all seven commands and all eight blocking evidence rows, including
  the stock protocol oracle, local protocol-combination matrix, private eD2K
  modules, eMuleBB/Rust and Rust/Rust bidirectional exchange, and total parity
  audit.
- Current UDP-reask witness:
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\artifacts\emulebb-rust-reask-cross-client\20260928T204605Z-x64-release-10252\emulebb-rust-reask-cross-client-result.json`.
  It passed with two active slots, one observed waiting peer, one queued TCP
  detach, and one acknowledged UDP reask.

### Required Surface Verdict

| Required surface | Verdict | Primary proof |
|---|---|---|
| Hello and capability tags | PASS | `hello_binary_corpus_skips_every_stock_tag_representation`; `hello_misc_options1_advertises_stock_comments_but_not_preview`; `hello_misc_options2_is_truthful_about_implemented_capabilities`; `emule_info_advertises_stock_comments_but_not_preview` |
| SX2 source metadata | PASS | `source_exchange2_v1_through_v4_preserve_their_wire_capabilities`; `remembered_source_hint_preserves_every_crypt_bit_combination`; `listener_source_exchange_preserves_live_source_connect_options`; `listener_source_exchange_returns_only_parts_useful_to_requester` |
| Queue and UDP reask | PASS | `tick_emits_due_ping_then_routes_the_ack`; `upload_queue_reask_reattaches_disconnected_waiter_without_wait_reset`; refreshed cross-client witness above |
| 32/64-bit transfer | PASS | `upload_part_packets_select_sending_opcode_per_fragment`; `upload_part_packets_select_compressed_opcode_per_block`; `large_file_download_starts_hashset_flow_before_peer_secure_ident_key_arrives` |
| Hashset, AICH, and ICH | PASS | `hashset_answer2_roundtrip_preserves_modern_md4_and_aich_sections`; `master_hash_matches_stock_emule_tracing_harness_fixture`; `corrupt_part_triggers_aich_recovery_request`; `ich_rehash_salvages_part_after_prefix_redownload` |
| Secure identification | PASS | `v1_valid_signature_verifies`; `v2_localclient_signature_binds_peer_ip`; `outbound_signature_v2_selected_for_v2_only_peer`; `credit_accrual_gate_matches_oracle_ident_states` |
| A4AF | PASS | `a4af_switch_requests_two_files_on_one_peer_connection`; `a4af_multi_file_peer_is_reused_and_not_double_engaged`; `a4af_nnp_source_is_swapped_to_another_wanted_file`; `direct_download_scheduler_attributes_a4af_results_to_the_switched_file` |
| Upload scheduling and duplicate handling | PASS; diagnostics evidence follow-up remains | `upload_payload_send_granularity_matches_mfc_threshold`; `upload_queue_classifies_queued_and_completed_duplicates_across_packets`; `listener_skips_duplicate_range_within_single_upload_request`; `rejection_ledger_counts_per_peer_block_and_starts_each_key_at_one` |

### Capability Contract

The peer capability words now describe implemented behavior rather than a stock
fingerprint. Regression tests assert the complete claimed subset, including
negative bits:

| Packet field | Advertised support | Explicitly not advertised |
|---|---|---|
| `CT_EMULE_MISCOPTIONS1` | AICH v1, Unicode, UDP v4, compression v1, secure-ident v3, extended requests v2, comments, multipacket | SX1, PeerCache, preview; no-view-shared-files is set |
| `CT_EMULE_MISCOPTIONS2` | file identifiers, SX2, extended multipacket, large files, Kad v10 | captcha; crypt support/request follow the actual local setting and required-crypt is not fabricated |
| `OP_EMULEINFO` tags | compression v1, UDP v4, comments, extended requests v2, secure-ident v3 | `ET_SOURCEEXCHANGE=0` and preview off |

SX2 remains advertised only through `CT_EMULE_MISCOPTIONS2`; clearing the
legacy `ET_SOURCEEXCHANGE` value does not disable or downgrade SX2.

### Finding Dispositions

The outcome vocabulary is intentionally exact:

- **Fixed** means the old difference is implemented, or a false capability
  claim is removed, and named regression evidence exists.
- **Omitted (truthful)** means the optional feature is deliberately unavailable
  and the peer is told that it is unavailable.
- **Deferred** means a valid behavioral difference remains accepted for later
  work and is recorded in the active machine-readable omission registry.

| ID | Old finding | Disposition |
|---|---|---|
| A2-01 | SX2 connection options were lost or fabricated | Fixed |
| A2-02 | Valid stock hello tag representations could abort the handshake | Fixed |
| A2-03 | Requester part state was skipped and SX2 answers were not usefulness-filtered | Fixed |
| A2-04 | Captcha was advertised without interactive response behavior | Omitted (truthful) |
| A2-05 | Received file comments and ratings were discarded | Fixed |
| A2-06 | Obsolete PeerCache packets closed the listener session | Fixed |
| A2-07 | Shared browsing was not feature-complete | Omitted (truthful) |
| A2-08 | SX1 live source exchange was absent | Omitted (truthful) |
| A2-09 | Peer media preview was absent | Omitted (truthful) |
| A2-10 | Connection pacing used a conservative rolling five-second window | Deferred |
| A2-11 | Upload send granularity differed from stock | Fixed |
| A2-12 | Cross-packet duplicate upload requests lacked conformant classification | Fixed; live diagnostics evidence follow-up remains |
| A2-13 | A4AF lacked full source-set switching and live-session reuse | Fixed |
| A2-14 | Out-of-part and unsolicited queue-rank anti-abuse escalation was shallow | Fixed |
| A2-15 | Legacy `OP_EMULEINFO` falsely advertised SX1 v3 | Fixed |

### Fixed Finding Evidence

1. **A2-01 — preserve source connect options.** Commit
   `1617ded40a4dbe0030a030eb3a00e90ad9642af3` retains the real SX2
   support/request/require bits through ingestion, persistence, rediscovery,
   and connection selection. Tests:
   `remembered_source_hint_does_not_fabricate_crypt_options_from_user_hash`,
   `remembered_source_hint_preserves_every_crypt_bit_combination`, and
   `listener_source_exchange_preserves_live_source_connect_options`.
2. **A2-02 — tolerate the full stock hello tag vocabulary.** Commit
   `1d60dc5678adbee8b6b5a3740bd80fce8d582ac9` adds bounded skipping for valid
   unknown stock representations without weakening truncation checks. Tests:
   `hello_binary_corpus_skips_every_stock_tag_representation`,
   `hello_ignores_unknown_long_tag_names_for_stock_valid_values`, and
   `hello_rejects_truncated_variable_width_stock_tags`.
3. **A2-03 — retain requester part state.** Commit
   `47be5a217c959d4ccb3a5df118f77ba38cf34a42` retains per-file part state and
   complete counts, including relayed state, and filters SX2 answers for
   requester usefulness. Tests:
   `source_exchange_filters_known_sources_by_requester_needed_parts`,
   `requester_state_is_scoped_to_its_file_and_keeps_complete_count`, and
   `listener_source_exchange_returns_only_parts_useful_to_requester`.
4. **A2-05 — persist inbound descriptions.** Commit
   `c5adf99ed78dd3a96d27b28353212e08abf316fb` retains received file comments
   and ratings through source rediscovery and reload. Tests:
   `file_description_decodes_stock_rating_and_long_string` and
   `source_file_description_matches_identity_and_survives_rediscovery_and_reload`.
5. **A2-06 — tolerate obsolete PeerCache packets.** Commit
   `959ef6e57418a2197c97c79cadd76032956ff6d5` makes the three obsolete packets
   bounded no-ops instead of disconnect reasons. Test:
   `listener_upload_startup_tolerates_source_exchange_and_aich_probe`.
6. **A2-11 — stock upload granularity.** Commit
   `45b7c1eaf8225db126a3c12a4fe4a4622859359c` matches the stock payload
   threshold. Test: `upload_payload_send_granularity_matches_mfc_threshold`.
7. **A2-12 — duplicate classification.** Commits
   `b1c732cbe0cb1292f643776a2dd89c912f2238b5` and
   `1ea5c157a32160dd6d9935313be8df293cbb3e54` add the conformant bounded ledger
   and classify queued/completed duplicates across packets. Tests:
   `upload_queue_classifies_queued_and_completed_duplicates_across_packets`,
   `behavior_peer_key_prefers_user_hash_then_ip`, and
   `rejection_ledger_counts_per_peer_block_and_starts_each_key_at_one`.
   `RUST-FEAT-025` remains active only for the captured listener-event body
   assertion and live converged-soak `repeatCount` comparison; it does not
   represent a missing rejection or classification path.
8. **A2-13 — complete A4AF switching and reuse.** Commits
   `e7f95b8b4f01454839e1f3f9a9d98653e4dc89c2` and
   `f96747db7c9420b805c2953ca31dc61157047a18` add NNP/FNF selection across the
   peer's source set and reuse one live peer session across files. Tests:
   `a4af_nnp_source_is_swapped_to_another_wanted_file`,
   `a4af_nnp_swap_skips_terminal_best_candidate_for_live_fallback`, and
   `a4af_multi_file_peer_is_reused_and_not_double_engaged`.
9. **A2-14 — transfer anti-abuse escalation.** Commits
   `07ca28993d9ead18f9ecd7d177bc3b8234d79b6f` and
   `3a162136e23b4c41f490d0a93fb29853aaaa5d23` add bounded out-of-part and
   queue-rank escalation while keeping accelerated reask diagnostics bounded.
   Tests: `repeated_out_of_part_requests_suppress_later_accept_with_cancel`,
   `unsolicited_queue_rank_bursts_disconnect_then_ban`, and
   `diagnostics_initial_reask_delay_override_is_bounded`.
10. **A2-15 — truthful legacy source-exchange tag.** Commit
    `d9f6ae918bf2e8786d39b61a6d3eef8d62da20af` sets legacy
    `ET_SOURCEEXCHANGE=0`, retains SX2 in `CT_EMULE_MISCOPTIONS2`, and asserts
    all supported/unsupported hello capability fields. Tests:
    `emule_info_advertises_stock_comments_but_not_preview`,
    `emule_info_decode_preserves_stock_capability_tags`,
    `hello_misc_options1_advertises_stock_comments_but_not_preview`, and
    `hello_misc_options2_is_truthful_about_implemented_capabilities`.

### Truthful Omission Evidence

- **A2-04 — peer chat/captcha.** Commit
  `3a1abdb172d6faceb6117015ba7d8482e8a1b09d` clears the captcha capability.
  `peer-chat-messaging` records the approved headless-product omission;
  unsolicited packets remain bounded and ignored without disrupting transfer.
- **A2-07 — shared browsing.** Rust returns empty/denied browse responses and
  sets no-view-shared-files, matching a stock client configured not to expose
  its inventory. No browse capability is claimed.
- **A2-08 — SX1.** `sx1-live-source-exchange` records the approved drop. Both
  the hello SX1 nibble and legacy `ET_SOURCEEXCHANGE` tag are zero; SX1 packets
  are not acted on, while SX2 v1-v4 stays active.
- **A2-09 — preview.** `ed2k-preview` records the approved drop. The preview bit
  is zero and request/answer packets remain bounded diagnostic input only.

### Deferred Evidence

Only **A2-10** remains a behavioral defer. The
`conn-rate-rolling-five-second-window` registry entry records the conservative
rolling-window implementation and its post-beta target. It has no wire-format
or capability-bit effect and is strictly no more aggressive than stock.

### Peer Close Decision

Every old peer finding now has a fixed, truthful-omission, or deferred
disposition. All advertised peer capabilities are backed by implemented paths,
and deliberately absent SX1, captcha/chat, preview, PeerCache, and shared
browsing behavior is either unadvertised or explicitly disabled. The one
remaining behavioral defer is non-wire connection pacing. The active
`RUST-FEAT-025` work is a diagnostics-evidence closure task, not an unimplemented
duplicate-rejection path.

This closes only the requested A2 peer-transfer reconciliation. It does not
mark the final beta, WebUI, packaging, soak, or unrelated active backlog items
complete.

## Kad and Client UDP Audit Reconciliation (2026-09-30)

### Comparison Basis

This is the narrow Kad and client-UDP reconciliation requested after the peer
audit. It covers Kad versions 2-10, routing persistence, search and publish,
firewall and buddy behavior, UDP obfuscation and receiver keys, publish ACK,
client-UDP port test, and Kad packet tag types. It does not re-open server,
peer-transfer, REST, WebUI, packaging, or the final beta release gate.

- Old audit snapshot: emulebb-rust
  `34b2bc0673ac28931144a70b5d670d6d04511500`.
- Reconciled implementation: emulebb-rust `main` at
  `d9f6ae918bf2e8786d39b61a6d3eef8d62da20af`.
- Stock comparison: `emulebb-community-baseline` branch
  `baseline/community-0.72a`, especially `kademlia/kademlia/Search.cpp`,
  `kademlia/net/KademliaUDPListener.cpp`,
  `kademlia/routing/RoutingZone.cpp`, `kademlia/io/DataIO.cpp`, and
  `ClientUDPSocket.cpp`.
- The old snapshot is an ancestor of the reconciled head. Every implementation
  commit named below is also an ancestor of that head.
- The active omission registry records the IPv4-only product boundary. It
  contains no unresolved Kad version, persistence, search/publish,
  firewall/buddy, obfuscation, publish-ACK, port-test, or tag-type gap.
- Authoritative current-head campaign:
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\release-campaign-runs\20260928T202338Z-emulebb-rust-overnight\release-campaign-run-result.json`.
  It passed all seven commands and all eight blocking evidence rows at the
  reconciled Rust head. The stock-protocol-oracle proof executed and passed
  `emulebb-ed2k`, `emulebb-kad-dht`, `emulebb-kad-net`,
  `emulebb-kad-proto`, and `emulebb-core`.

### Required Surface Verdict

| Required surface | Verdict | Primary proof |
|---|---|---|
| Kad versions 2-10 | PASS | `search_phase_selects_stock_packet_family_for_versions_two_through_ten`; `source_publish_selects_stock_packet_family_for_versions_two_through_ten`; `legacy_v2_search_requests_match_stock_wire_shapes`; `legacy_v2_v3_source_publish_matches_stock_counted_layout` |
| Routing persistence | PASS | `unversioned_counts_zero_one_two_three_and_more_are_unambiguous`; `modern_version_two_preserves_key_binding_and_verified_state`; `exact_record_sizes_reject_truncation_and_trailing_bytes`; `learned_contact_is_atomically_persisted_and_reloaded_on_restart` |
| Search and publish | PASS | `test_run_search_phase_replays_restrictive_keyword_payload`; `build_keyword_publish_packets_splits_fifty_one_entries_into_two_packets`; `publish_response_preserves_optional_stock_ack_request_byte`; stock-protocol-oracle package proof above |
| Firewall and buddy behavior | PASS | `tcp_firewall_recheck_tracks_up_to_four_helper_responses`; `udp_round_times_out_as_firewalled_after_completed_failed_tests`; `test_find_buddy_action_walk_stops_at_the_oracle_answer_target`; `kad_callback_req_relays_op_callback_down_held_buddy_socket` |
| UDP obfuscation and receiver keys | PASS | `test_encrypt_decrypt_roundtrip_with_node_id_mode`; `test_encrypt_decrypt_roundtrip_with_receiver_key_mode`; `test_response_opcodes_keep_node_id_when_identity_is_known`; `test_receiver_verify_key_is_reused_across_ports_on_same_ip` |
| Publish ACK and client-UDP port test | PASS | `publish_response_ack_bit_is_detected_without_treating_other_options_as_requests`; `test_publish_res_ack_prefers_receiver_key_when_available`; `parses_only_the_exact_stock_port_test_probe`; `udp_probe_wakes_only_the_current_tcp_registration_once` |
| Kad packet tag types | PASS | `test_stock_storage_class_allowlist_roundtrips`; `test_reader_rejects_generic_ed2k_short_name_marker`; `test_reader_rejects_non_stock_storage_classes`; `test_truncated_name_and_bsob_lengths_are_rejected` |
| IPv4-only boundary | EXPLICIT | `policy/rust-client.toml` sets `protocol.address_family = "ipv4-only"`; `ipv6-ed2k-kad` records the approved permanent drop and confirms that no IPv6 capability is advertised |

### Finding Dispositions

The outcome vocabulary is intentionally exact:

- **Fixed** means the old difference is implemented and named regression
  evidence exists.
- **Omitted (stock-aligned)** means current stock also ignores the obsolete
  family and Rust does not advertise it.
- **Accepted platform boundary** means packet framing and network behavior are
  stock-compatible, while display-only decoding follows the host platform.
- **Permanent boundary** means the product difference is explicit in the
  active machine-readable policy and is not advertised as supported.

| ID | Old finding | Disposition |
|---|---|---|
| A3-01 | Kad v2 search and Kad v2/v3 source-publish fallbacks were missing | Fixed |
| A3-02 | Non-stock Bool, BoolArray, Blob, and unknown storage classes could be indexed and relayed | Fixed |
| A3-03 | `nodes.dat` versions, record sizes, security metadata, and runtime persistence were incomplete | Fixed |
| A3-04 | Kad publish-response ACK requests were ignored | Fixed |
| A3-05 | Client-UDP `OP_PORTTEST` was absent | Fixed |
| A3-06 | NodeID-mode UDP obfuscation did not validate the embedded receiver key | Fixed |
| A3-07 | Kad1 outbound behavior is absent | Omitted (stock-aligned) |
| A3-08 | Invalid-UTF8 search-result fallback differs off Windows | Accepted platform boundary |
| A3-09 | IPv6 eD2K/Kad is absent | Permanent boundary |

### Fixed Finding Evidence

1. **A3-01 - Kad v2/v3 wire selection.** Commit
   `05c2bf99c55267c75b01d3a342ef3cf3eb58979d` adds the legacy v2 search and
   notes request families, the counted v2/v3 source-publish family, correct
   response tracking, and per-contact selection through version 10. Tests:
   `search_phase_selects_stock_packet_family_for_versions_two_through_ten`,
   `source_publish_selects_stock_packet_family_for_versions_two_through_ten`,
   `legacy_v2_search_requests_match_stock_wire_shapes`, and
   `legacy_v2_v3_source_publish_matches_stock_counted_layout`.
2. **A3-02 - stock Kad tag classes only.** Commit
   `c80e5ec6a4794da344ba72a152363aad3541e854` removes generic eD2K Bool,
   BoolArray, and Blob values from the Kad tag model, retains the stock hash,
   string, integer-width, float, and BSOB classes, requires canonical Kad name
   encoding, and keeps bounded length checks. Tests:
   `test_stock_storage_class_allowlist_roundtrips`,
   `test_reader_rejects_non_stock_storage_classes`,
   `test_reader_rejects_generic_ed2k_short_name_marker`, and
   `test_truncated_name_and_bsob_lengths_are_rejected`.
3. **A3-03 - secure routing persistence.** Commit
   `55fc0ce9916dbec48049ed22280df587e182ed43` parses unversioned and modern
   versions 1-3 without count ambiguity, enforces exact 25/34-byte records,
   preserves UDP key, binding public IP, and verified state, snapshots learned
   routing contacts, and atomically writes and reloads `nodes.dat`. Imported
   keys become usable only after the current public IPv4 binding matches.
   Tests: `unversioned_counts_zero_one_two_three_and_more_are_unambiguous`,
   `modern_version_one_reads_exact_basic_records`,
   `modern_version_two_preserves_key_binding_and_verified_state`,
   `modern_version_three_normal_reads_extended_records`,
   `modern_version_three_bootstrap_edition_reads_basic_records`,
   `exact_record_sizes_reject_truncation_and_trailing_bytes`,
   `encoding_roundtrips_all_extended_security_metadata`, and
   `learned_contact_is_atomically_persisted_and_reloaded_on_restart`.
4. **A3-04 - publish response ACK.** Commit
   `d1fc7b59a282537de75ae8088b12d8a038805742` preserves the stock options
   byte, detects bit zero, gates ACK transmission on a learned sender key, and
   sends `KADEMLIA2_PUBLISH_RES_ACK` in receiver-key mode. Tests:
   `publish_response_preserves_optional_stock_ack_request_byte`,
   `publish_response_ack_bit_is_detected_without_treating_other_options_as_requests`,
   and `test_publish_res_ack_prefers_receiver_key_when_available`.
5. **A3-05 - cross-transport client port test.** Commit
   `93d16d4cb03e442b8ffc02bedf3221352ced22d9` accepts only the exact client-UDP
   `OP_PORTTEST 0x12` probe, associates it with the currently armed TCP test
   session, and emits the one-shot stock TCP result. Tests:
   `parses_only_the_exact_stock_port_test_probe`,
   `udp_probe_wakes_only_the_current_tcp_registration_once`,
   `dropping_registration_disarms_only_its_generation`, and the complete
   listener startup flow in
   `listener_upload_startup_tolerates_source_exchange_and_aich_probe`.
6. **A3-06 - NodeID receiver-key validity.** Commit
   `2b17400bcdad20c9c33c8e703f01af3a167347fc` validates the embedded
   receiver key after successful NodeID-mode decryption instead of tying
   validity to the selected RC4 key mode. Tests:
   `test_encrypt_decrypt_roundtrip_with_node_id_mode`,
   `test_response_opcodes_keep_node_id_when_identity_is_known`, and
   `test_publish_res_ack_prefers_receiver_key_when_available`.

### Boundary and Stock-Aligned Evidence

- **A3-07 - Kad1.** Current stock explicitly ignores deprecated Kad1
  bootstrap, hello, request, search, and publish opcodes. Rust drops Kad1
  contacts (`test_sanitize_res_contacts_drops_kad1_and_dns_port_contacts`) and
  does not advertise Kad1. Versions 2-10 use the tested packet selection above.
- **A3-08 - legacy search strings.** Windows Rust follows stock by trying UTF-8
  and then the active ANSI code page. Non-Windows builds use Windows-1252 only
  for invalid-UTF8 display text (`test_search_res_decodes_legacy_cp1252_strings`).
  The fallback does not alter packet framing, search routing, indexing keys, or
  advertised capability. It is an accepted host-platform display boundary,
  not a network parity defer.
- **A3-09 - IPv4 only.** `policy/rust-client.toml` is explicit that the product
  address family is IPv4-only. The active `ipv6-ed2k-kad` omission records the
  operator-approved permanent boundary for eD2K, Kad, transfer, NAT, and
  bootstrap behavior, and confirms that no IPv6 capability bit is advertised.

### Kad and Client UDP Close Decision

Every Kad/client-UDP finding from the old audit now has fixed,
stock-aligned, accepted-platform, or permanent-boundary evidence. The supported
Kad v2-v10, routing, search/publish, firewall/buddy, UDP obfuscation,
publish-ACK, port-test, and tag-type surfaces are covered by named tests and the
current-head stock-protocol-oracle package proof. The IPv4-only boundary is
explicit in both the machine policy and the active omission registry.

This closes only the requested A3 Kad and client-UDP reconciliation. It does
not mark the final beta, WebUI, packaging, soak, or unrelated active backlog
items complete.

## Validation

Required for closing this item:

- `python -m emule_workspace workspace-status`
- `python -m emule_workspace validate`
- `python tools\check_rust_client_policy.py`
- `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`
- `python -m emule_workspace build app --variant tracing-harness --config Release --platform x64 --build-output-mode ErrorsOnly`
- `python -m emule_workspace test release-campaign --campaign emulebb-rust-overnight --execute --continue-on-failure`

Closure results:

- `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\release-campaign-runs\20260927T171451Z-emulebb-rust-overnight\release-campaign-run-result.json`
  passed seven of seven commands and eight of eight required blocking evidence
  rows.
- `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\artifacts\emulebb-rust-reask-cross-client\20260927T164726Z-x64-release-9936\emulebb-rust-reask-cross-client-result.json`
  passed the targeted UDP-reask witness.
- The final regular Rust release build completed without warnings at
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\logs\builds\20260927T165347Z-build-clients\build-result.json`.
- `workspace-status` completed successfully. `workspace validate` passed the
  active policy, branch, dependency-pin, documentation-path, editorconfig,
  environment, localization, output-redirection, PowerShell-boundary, entrypoint,
  and warning-policy audits, then reported the existing workspace artifact-audit
  debt: ignored local virtual environments plus `emulebb-rust/webui/node_modules`.
  Those operator caches are outside this parity closure and were not deleted.

Peer reconciliation refresh:

- Rust commit `d9f6ae918bf2e8786d39b61a6d3eef8d62da20af` passed the orchestrated
  `emulebb-ed2k` Release package run: 876 passed, zero failed.
- `python tools\check_rust_client_policy.py` and focused `rustfmt --check` for
  all three changed Rust files passed.
- `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\release-campaign-runs\20260928T202338Z-emulebb-rust-overnight\release-campaign-run-result.json`
  passed seven of seven commands and eight of eight required blocking evidence
  rows at Rust `d9f6ae91`, build-tests `9865967`, build `7eccd29`, tooling
  `9b13576`, MFC `9466ece`, and goed2k-server `ea5d4b2`.
- `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\artifacts\emulebb-rust-reask-cross-client\20260928T204605Z-x64-release-10252\emulebb-rust-reask-cross-client-result.json`
  passed with `effectiveSlotCap=2`, `activeSlots=2`,
  `mfcWaitingSessionsMax=1`, `detaches=1`, and `ackedReplies=1`.
- The refreshed `workspace validate` again passed every audit before the
  workspace artifact audit, which reported 68 existing generated files under
  unrelated local virtual environments plus `emulebb-rust/webui/node_modules`.
  Those operator-owned caches were not changed or deleted.

Kad and client-UDP reconciliation refresh:

- All six focused implementation commits are ancestors of Rust
  `d9f6ae918bf2e8786d39b61a6d3eef8d62da20af`; the tracked Rust tree is
  unchanged from the authoritative campaign head.
- The same `20260928T202338Z` overnight result passed all seven commands and
  all eight blocking evidence rows. Its stock-protocol-oracle result passed
  the `emulebb-ed2k`, `emulebb-kad-dht`, `emulebb-kad-net`,
  `emulebb-kad-proto`, and `emulebb-core` proof packages.
- `python tools\check_rust_client_policy.py` and `git diff --check` passed at
  the reconciled Rust head. The policy check includes the explicit IPv4-only
  configuration and active omission-registry validation.

Optional smoke:

- `python scripts\rust-live-wire-hideme.py --inputs live-wire-inputs.local.json`

## Notes

- This item is local because it records the evidence gate and close decision
  rather than a product feature. If the gate needs public workflow visibility,
  promote it to a GitHub-tracked CI item before closure.
- Related owners: completed `RUST-FEAT-001` for UDP reask live validation,
  completed `RUST-FEAT-003` for VPN egress pinning, completed `RUST-FEAT-005`
  for dynamic no-leak automation, and `RUST-BUG-001` for isolated Kad swarm CI
  debt.
