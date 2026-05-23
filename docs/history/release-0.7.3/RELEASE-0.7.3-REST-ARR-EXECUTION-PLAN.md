# Beta 0.7.3 REST and Arr Execution Plan

> Historical release plan only. Current beta `0.7.3` execution is controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

This is the active execution plan for beta 0.7.3 REST, aMuTorrent, and Arr work. It
does not own gate status; use [RELEASE-0.7.3](RELEASE-0.7.3-GATE-HISTORY.md) for current release
decisions and item docs for completion evidence.

Current status: the broadband branch remains pre-release stabilization. This
plan describes the REST/Arr shape that supports beta 0.7.3; it is not a tag or
package authorization document.

## Decisions

- Native `/api/v1` cleanliness wins over current client compatibility.
- Breaking pre-release REST contracts is allowed when it makes eMule BB
  cleaner.
- aMuTorrent is the primary UI target, but it adapts to the clean native
  `/api/v1` design; it does not define route names, envelopes, field aliases,
  validation rules, or compatibility drift.
- Sonarr, Radarr, and Prowlarr clients integrate with eMule BB directly. Arr
  compatibility is an eMule BB adapter layer over shared native logic, not an
  aMuTorrent proxy path.
- Prowlarr/Radarr/Sonarr/qBittorrent-compatible behavior is release-critical
  evidence, but it must not force native `/api/v1` to mimic Arr or qBit quirks.
- Legacy WebServer cleanup is limited to REST/WebServer boundary safety and
  shared request/path/concurrency code.
- Do not rewrite or retire the legacy HTML UI for beta 0.7.3.

## Gate Map

| Area | Release gate items | Deep-plan responsibility |
|------|--------------------|--------------------------|
| Native REST errors | [BUG-075](../items/BUG-075.md) | stable JSON error envelope and status mapping |
| WebServer boundary | [BUG-076](../items/BUG-076.md), [BUG-077](../items/BUG-077.md) | malformed REST isolation and mixed REST/legacy stress |
| Contract completeness | [CI-014](../items/CI-014.md), [CI-015](../items/CI-015.md), [FEAT-047](../items/FEAT-047.md) | OpenAPI-backed smoke, route drift checks, stress budgets |
| aMuTorrent | [AMUT-001](../items/AMUT-001.md), [AMUT-002](../items/AMUT-002.md) | UI consumer proof and transfer-detail hydration |
| Arr adapters | [ARR-001](../items/ARR-001.md) | Torznab/qBittorrent adapter proof without native API drift |
| REST controller candidates | [FEAT-045](../items/FEAT-045.md), [FEAT-046](../items/FEAT-046.md), [FEAT-048](../items/FEAT-048.md), [FEAT-049](../items/FEAT-049.md) | documented deferral or promotion path for controller parity work |

## Current Revalidation Focus

The earlier gates have passing evidence, but the next beta 0.7.3 hardening pass
should revalidate the API surfaces below before treating that evidence as fresh.

### Native `/api/v1`

- [x] Re-run the OpenAPI route-drift check against every implemented native
      route, including methods, required bodies, path parameters, and response
      envelopes.
- [x] Re-run live REST completeness with representative read routes, safe
      mutations, destructive confirmation bodies, and unsupported-method checks.
- [x] Re-run malformed-input coverage for bad JSON, non-object JSON, unknown
      fields, malformed query parameters, bad hashes, missing auth, wrong auth,
      unsupported content types, missing resources, and invalid state.
- [x] Re-run mixed REST/legacy WebServer stress with native `/api/v1` errors
      checked for JSON-only responses and no HTML fallback.
- [x] Audit every destructive native operation for explicit confirmation or
      explicit intent fields, especially transfer delete, shared-file delete,
      delete-all searches, clear-completed transfers, directory replacement, and
      app shutdown exclusion from broad mutation loops.
- [x] Record the native REST execution model in the route seam and smoke
      harness so direct routes and UI-thread-dispatched routes cannot drift
      silently.

### Arr And qBit-Compatible Adapters

- [x] Revalidate Prowlarr Torznab indexer add/test/search against live eMule BB
      and confirm adapter errors are bounded, redacted, and diagnosable.
- [x] Revalidate Radarr and Sonarr indexer sync through Prowlarr plus
      qBittorrent-compatible download-client add/test flows.
- [x] Revalidate qBittorrent-compatible login, app preferences, transfer add,
      transfer info/properties/files, category mutation, pause/resume, and
      delete flows against live eMule BB.
- [x] Confirm adapter compatibility parsing reuses shared native validation,
      normalization, path-safety, and serialization helpers where applicable
      instead of carrying divergent behavior.
- [x] Confirm Arr/qBit compatibility errors stay adapter-shaped for those
      clients while native `/api/v1` remains the clean OpenAPI-shaped contract.

### aMuTorrent Consumer Proof

- [x] Re-run the aMuTorrent browser smoke after native `/api/v1` and adapter
      revalidation so UI regressions are caught without making aMuTorrent the
      native API authority.
- [x] Confirm the eMule BB adapter keeps translating aMuTorrent expectations to
      final native fields/routes and does not require native aliases for old UI
      state.
- [x] Confirm status, ED2K/Kad search selection, progress formatting, and
      download-row delete remain covered by the aMuTorrent integration branch.

## Native REST Contract

- Native REST failures return JSON, not legacy HTML.
- Destructive native operations require explicit confirmation bodies.
- Shared-directory root replacement requires `confirmReplaceRoots: true`; this
  route is treated as destructive because it replaces the configured share set.
- Native `/api/v1` hashes stay strict lowercase eD2K identifiers.
- Search result paging is intentionally not exposed in beta 0.7.3; controllers
  poll the current visible native result snapshot.
- `/app/shutdown` stays excluded from broad live mutation loops.
- `GET /api/v1/app` is the only current direct route. Runtime reads, mutations,
  and destructive routes remain UI-thread dispatched until ownership is proven
  safe in the app layer.

## Adapter Boundaries

- qBit-compatible hash inputs may normalize for compatibility, but native
  `/api/v1` remains strict.
- Torznab XML/feed shape and qBit text/session-cookie behavior stay
  adapter-specific.
- `/api/v2` is reserved for direct Arr/qBittorrent-compatible clients talking
  to eMule BB. aMuTorrent release proof must stay on the native `/api/v1`
  surface.
- Operator-owned live-wire search terms, transfer hashes, magnets, and direct
  ED2K bootstrap rows must stay in
  `repos\emulebb-build-tests\live-wire-inputs.local.json`, which is ignored and
  untracked. Tracked release docs, manifests, and fixtures may contain only
  placeholders, stable contract vectors, or redacted summaries for this data.
- Transfer progress ratio math is shared by native `/api/v1` and qBit-compatible
  transfer rows so UI adapters see bounded precision without defining the
  native contract.
- Shared behavior should reuse native parser, validation, normalization,
  serialization, and path-safety helpers.
- aMuTorrent and Arr gates must not force native route names or envelope shape.

## Controller Compatibility Matrix

| Consumer | Surface | Boundary | Proof lane |
|---|---|---|---|
| Native REST | `/api/v1` | OpenAPI/native route seam is authoritative. | REST smoke, route drift, live completeness |
| aMuTorrent | `/api/v1` through adapter code | UI expectations adapt to native fields/envelopes. | aMuTorrent browser smoke |
| Prowlarr | Torznab adapter | XML/feed/errors stay adapter-local. | Prowlarr live |
| Radarr/Sonarr | Torznab plus qBit-compatible client | Arr behavior must not broaden `/api/v1`. | Radarr/Sonarr live |
| qBit-compatible clients | `/api/v2` | Arr-needed subset only; text/session errors stay qBit-shaped. | qBit route completeness and Arr live |

## Execution Lanes

### REST and WebServer Robustness

- Keep [BUG-075](../items/BUG-075.md) as the typed error contract owner.
- Keep [BUG-076](../items/BUG-076.md) as the malformed request boundary owner.
- Keep [BUG-077](../items/BUG-077.md) as the mixed REST and legacy HTML stress owner.
- Any future route, parser, auth, or WebServer concurrency change must rerun the
  REST smoke and malformed/concurrent matrix before beta 0.7.3 evidence is
  reused.

### Contract Completeness

- Keep [CI-014](../items/CI-014.md) as the OpenAPI and route drift gate.
- Keep [CI-015](../items/CI-015.md) as the malformed and concurrent request matrix gate.
- Keep [FEAT-047](../items/FEAT-047.md) closed by documenting the beta 0.7.3 search
  snapshot behavior instead of adding paging or bounds changes.
- New `/api/v1` routes require OpenAPI, native route seam, live smoke, and
  REST contract documentation updates in the same closure slice.

### Controller Integrations

- Keep [AMUT-001](../items/AMUT-001.md) as the live aMuTorrent browser proof.
- Keep [ARR-001](../items/ARR-001.md) as the live Prowlarr, Radarr, Sonarr, Torznab,
  and qBittorrent-compatible proof.
- Treat [AMUT-002](../items/AMUT-002.md) as promoted for beta 0.7.3. The
  aMuTorrent adapter consumes [FEAT-045](../items/FEAT-045.md) only when eMule
  BB advertises `transferDetails`, and browser smoke coverage verifies the
  hydrated detail fields.

### Candidate Promotion Rules

- [FEAT-045](../items/FEAT-045.md) is closed for beta 0.7.3: the dedicated
  transfer detail endpoint is implemented, advertised through capability
  metadata, and consumed by aMuTorrent through `AMUT-002`.
- [FEAT-046](../items/FEAT-046.md) is closed for beta 0.7.3: server.met import,
  Kad bootstrap, nodes.dat URL import, malformed preservation, and live seed
  import evidence are covered.
- [FEAT-048](../items/FEAT-048.md) is closed for beta 0.7.3 by audit: existing
  upload controls are covered, unsupported operations return typed errors, and
  no additional queue mutation was promoted.
- [FEAT-049](../items/FEAT-049.md) is closed for beta 0.7.3 by audit: aMuTorrent
  needs no additional runtime preference keys, risky internals remain private,
  and the curated surface has live round-trip plus bad-value coverage.

## Release Test Matrix

- native route and OpenAPI drift tests
- REST smoke with representative read and safe mutation routes
- REST malformed-request coverage
- REST mixed stress and soak budgets
- aMuTorrent browser smoke with console/page/request diagnostics
- Prowlarr Torznab live proof
- Radarr/Sonarr integration through Prowlarr plus qBit-compatible download
  control
- long-path and Unicode REST paths for shared directories, transfers, and logs

Latest beta 0.7.3 REST closure proof:

- `python -m emule_workspace validate`
- `python -m emule_workspace build app --config Debug --platform x64`
- `python -m emule_workspace build app --config Release --platform x64`
- `python -m emule_workspace test python --path tests\python\test_rest_api_smoke.py --path tests\python\test_release_golden.py --quiet`
- `python -m emule_workspace test live-e2e --config Release --platform x64 --suite rest-api --rest-coverage-budget contract-stress --rest-stress-budget smoke --rest-stress-duration-seconds 10 --rest-stress-concurrency 4 --rest-download-trigger-count 3 --skip-live-seed-refresh`
- Result: passed on 2026-05-10.
- Live artifact:
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260510-235256-eMule-main-release`
- REST contract summary: 85 OpenAPI routes in the registry, 82 safe routes
  exercised, 3 unsafe routes skipped, 0 failed routes, 37 success outcomes,
  and 45 expected-error outcomes. Strict OpenAPI response-schema validation was
  active for successful native REST envelopes and typed JSON error envelopes.
- Route execution summary: 1 direct route and 84 UI-thread-dispatched routes;
  `GET /api/v1/app` is the only direct native route.
- REST stress summary: 4181 requests, 0 native REST non-JSON responses,
  0 timeouts, p95 latency 68.172 ms, and no failure sample.
- Local dump configuration was enabled for `emule.exe`, `umdh.exe`,
  `procdump.exe`, and `procdump64.exe`.
- Dedicated adapter follow-up on 2026-05-10:
  - Prowlarr/Torznab live passed:
    `repos\emulebb-build-tests\reports\prowlarr-emulebb-live\20260510-224143-eMule-main-release`
  - Radarr/Sonarr plus qBit-compatible live passed:
    `repos\emulebb-build-tests\reports\radarr-sonarr-emulebb-live\20260510-224447-eMule-main-release`
  - aMuTorrent browser smoke stopped before browser execution because
    aMuTorrent served `127.0.0.1:57415` from its persistent server config while
    the harness waited on generated port `127.0.0.1:55939`:
    `repos\emulebb-build-tests\reports\amutorrent-browser-smoke\20260510-225224-eMule-main-release`.
    This is tracked in [BUG-102](../items/BUG-102.md) as aMuTorrent/harness
    configuration drift, not native REST contract drift.

Latest native route/OpenAPI drift proof:

- `python -m pytest
  tests\python\test_rest_api_smoke.py::test_rest_contract_registry_matches_openapi
  tests\python\test_rest_api_smoke.py::test_native_route_specs_match_openapi_methods_paths_and_fields
  tests\python\test_rest_api_smoke.py::test_openapi_contract_routes_are_the_live_completeness_source
  tests\python\test_release_golden.py`
- Result: 6 tests passed on 2026-05-09.

Latest live REST completeness proof:

- `python -m emule_workspace test live-e2e --config Release
  --platform x64 --suite rest-api`
- Artifact:
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260509-080825-eMule-main-release`
- Result: passed with `BindInterface=hide.me`, UPnP enabled, and contract
  coverage enabled.
- REST contract summary: 82 OpenAPI routes in the registry, 81 safe routes
  exercised, 0 failed routes, 36 success outcomes, 45 expected-error outcomes,
  and 1 intentionally skipped unsafe route (`/api/v1/app/shutdown`).
- The run covered native read routes, safe mutations, expected destructive
  confirmation failures, and unsupported-method coverage through the live
  completeness and error-path matrix checks.

Latest malformed REST input proof:

- `python -m pytest tests\python\test_rest_api_smoke.py -k "malformed or
  error_path or wrong_key or bad_json or unknown or duplicate or uppercase or
  method_not_allowed or unsupported"`
- Result: 2 selected tests passed on 2026-05-09.
- Live artifact:
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260509-080825-eMule-main-release`
- The live error-path matrix recorded 72 error responses with no missing release
  statuses. It covered live 400/401/404 responses plus seam-backed
  405/409/500/503 responses.
- The live surface included malformed JSON content type, non-object JSON,
  unknown JSON fields, duplicate and malformed query parameters, bad hashes,
  missing and wrong API keys, missing resources, and destructive confirmation
  errors.

Latest mixed REST/legacy stress proof:

- `python -m pytest tests\python\test_rest_api_smoke.py -k "stress or legacy
  or non_json or html or shutdown_exclusion"`
- Result: 10 selected tests passed on 2026-05-09.
- Live artifact:
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260509-080825-eMule-main-release`
- The live mixed stress ran for 30 seconds with 4-way concurrency and completed
  13,311 requests with 0 failures, 0 timeouts, 0 retry recoveries, and 0 native
  REST non-JSON responses.
- The stress mix included native REST reads and safe mutations, malformed
  native error edges, Torznab and qBittorrent-compatible adapter traffic, and
  legacy HTML root traffic while keeping `/api/v1/app/shutdown` excluded from
  broad mutation loops.

Latest destructive native operation audit:

- Test commit: `c4db9e7`.
- `python -m pytest
  tests\python\test_rest_api_smoke.py::test_destructive_native_routes_require_explicit_confirmation_or_intent
  tests\python\test_rest_api_smoke.py::test_native_route_specs_match_openapi_methods_paths_and_fields
  tests\python\test_rest_api_smoke.py::test_openapi_contract_routes_are_the_live_completeness_source`
- Result: 3 selected tests passed on 2026-05-09.
- The audit checks native route specs against OpenAPI and requires explicit
  confirmation fields for app shutdown, clear-completed transfers, transfer
  delete, shared-file delete, shared-directory replacement, and delete-all
  searches. It also inventories every native DELETE route so new destructive
  routes must be classified.
- Live artifact:
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260509-080825-eMule-main-release`
  confirmed `/api/v1/app/shutdown` remains excluded from broad mutation loops.

Latest Radarr/Sonarr video-category proof:

- `python -m emule_workspace test live-e2e --config Release
  --platform x64 --suite radarr-sonarr-emulebb`
- Artifact:
  `repos\emulebb-build-tests\reports\radarr-sonarr-emulebb-live\20260509-074817-eMule-main-release`
- The suite searched video-family Torznab categories for the Arr proof:
  Radarr/qBit video category `2000` and Sonarr category `5000`.
- Operator-owned terms, hashes, magnets, and direct ED2K rows remained in the
  ignored `repos\emulebb-build-tests\live-wire-inputs.local.json`; persisted
  reports kept only counts and presence flags.
- Prowlarr returned video-category rows for both Radarr and Sonarr searches,
  Radarr/Sonarr exposed synced enabled eMule BB indexers, temporary qBittorrent
  clients tested successfully, and two qBit-compatible live-wire
  add/mutate/delete rounds passed against video-category magnets.

Latest Prowlarr video-category proof:

- `python -m emule_workspace test live-e2e --config Release
  --platform x64 --suite prowlarr-emulebb`
- Artifact:
  `repos\emulebb-build-tests\reports\prowlarr-emulebb-live\20260509-080508-eMule-main-release`
- The suite searched explicit Torznab categories: document category `7000`,
  Radarr/movie video category `2000`, and Sonarr/TV video category `5000`.
- Operator-owned search terms stayed in the ignored
  `repos\emulebb-build-tests\live-wire-inputs.local.json`; persisted reports kept
  only term counts, query-presence flags, and result counts.
- Direct eMule BB Torznab searches and Prowlarr API searches returned rows for
  document, movie, and TV categories, and the Prowlarr Generic Torznab
  add/test flow passed.

Latest adapter shared-validation audit:

- Test commit: `88c743f`.
- `python -m pytest
  tests\python\test_rest_api_smoke.py::test_arr_compat_uses_shared_native_validation_and_search_commands
  tests\python\test_rest_api_smoke.py::test_qbit_compat_uses_shared_native_validation_and_bridge_commands
  tests\python\test_rest_api_smoke.py::test_qbit_compat_torrent_list_uses_native_transfer_command`
- Result: 3 selected tests passed on 2026-05-09.
- The audit locks Torznab compatibility to shared request path escape checks,
  query parsing, search text normalization, unsigned decimal parsing, public
  filename validation, and native `search/start`, `search/results`, and
  `search/stop` commands.
- The audit locks qBittorrent compatibility to shared request path escape
  checks, query and form parsing, category normalization, public filename
  validation, decimal parsing, URL encoding, and native transfer bridge
  commands.

Latest adapter error-shape proof:

- `python -m pytest tests\python\test_rest_api_smoke.py -k "qbit or torznab
  or requires_json or adapter or wrong_cookie or bad_login or wrong_query_key"
  tests\python\test_prowlarr_emulebb_live.py::test_direct_torznab_error_edges_are_expected_400s`
- Result: 5 selected tests passed on 2026-05-09.
- Live artifact:
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260509-080825-eMule-main-release`
- qBittorrent-compatible failures stayed qBit-shaped (`text/plain`, `Fails.`
  or `Forbidden`), Torznab failures stayed XML-shaped, and native `/api/v1`
  stress recorded 0 native REST non-JSON responses.

Latest aMuTorrent browser proof:

- `python -m emule_workspace test live-e2e --config Release
  --platform x64 --suite amutorrent-browser-smoke`
- Artifact:
  `repos\emulebb-build-tests\reports\amutorrent-browser-smoke\20260509-081711-eMule-main-release`
- `python -m pytest tests\python -k "amutorrent or browser_smoke or
  search_modes or transfer_detail or segment_snapshot"`
- Result: 21 selected tests passed on 2026-05-09.
- The live browser run passed with `BindInterface=hide.me`, UPnP enabled,
  eD2K connected, Kad connected, automatic/server/Kad search modes exercised,
  category create/delete, shared-files reload, synthetic eD2K add/delete, and
  post-delete snapshot cleanup.
- The transfer row carried hydrated progress/status/source fields plus
  segment-subscribed `partStatus`, `gapStatus`, and `reqStatus`, keeping
  aMuTorrent translation on its adapter side of the native `/api/v1` contract.

## Deferred REST/Arr Work

No REST/Arr controller candidate remains deferred in this execution plan.
`FEAT-032` remains tracked separately by the NAT mapping execution plan.
