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
