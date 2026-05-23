# Beta 0.7.3 SDET Stress Execution Plan

> Historical release plan only. Current beta `0.7.3` execution is controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

This plan owns the Beta 0.7.3 test-robustness gaps from the 2026-05-08 SDET stability
review. These are release-gate test items, not product feature work. They block
`emule-bb-v1.0.0` until implemented, run, and reflected in their item docs.

Covered items:

- [CI-018](../items/CI-018.md) - Shared Files 50k-file tree refresh stress gate
- [CI-019](../items/CI-019.md) - HTTPS and REST socket adversity stress gate
- [CI-020](../items/CI-020.md) - REST and legacy WebServer error-path coverage gate
- [CI-021](../items/CI-021.md) - WebSocket and legacy socket leak-churn gate

## Current State

The existing Beta 0.7.3 suite has strong native REST parser/status tests and live HTTP
REST stress evidence. The uncovered Beta 0.7.3 risk is at the hostile live boundary:
large Shared Files UI churn, HTTPS handshake stalls, socket resets, live 500
fault paths, and resource-accounted socket churn.

## Sequencing

1. Implement [CI-018](../items/CI-018.md) first because it expands the Shared
   Files fixture and UI-harness capabilities that later release runs can reuse.
2. Implement [CI-019](../items/CI-019.md) next to put the existing REST contract
   and stress matrix through HTTPS and raw socket adversity.
3. Implement [CI-020](../items/CI-020.md) after the HTTPS harness path exists so
   the error-path matrix can run over both HTTP and HTTPS where useful.
4. Implement [CI-021](../items/CI-021.md) last as the resource-accounting soak
   that combines the socket churn surfaces and proves cleanup.

Each slice must be committed and pushed before the next independent slice
starts.

## Shared Rules

- Use supported workspace entrypoints for build, validation, and live E2E.
- Keep new stress modes selectable so routine Beta 0.7.3 gates can run a bounded smoke
  profile and operators can run longer soak profiles.
- Preserve legacy ED2K/Kad runtime behavior; these items add proof and harness
  coverage, not protocol changes.
- Emit durable artifacts for every gate: command line, profile settings,
  request counts, status counts, timeout counts, resource deltas, and sampled
  failures.
- Treat public-network absence as inconclusive only when the harness records
  enough diagnostics to distinguish environment failure from product failure.

## Detailed Plan

### CI-018 - Shared Files 50k-file tree refresh stress gate

Implementation:

- Add a 50k-file fixture profile to the Shared Files fixture generator.
- Add tree collapse support and a rapid churn driver to the Shared Files UI
  live harness.
- Combine expand/collapse/select/reload/sort/paint operations with monitored
  filesystem mutations under shared roots.
- Cross-check UI-visible state with REST shared-file and shared-directory
  snapshots after each churn phase.
- Capture screenshots, REST snapshots, selected path, row counts, timeout
  reasons, and process resource deltas on failure.

Validation:

- Run the smoke budget through the supported `live-e2e` entrypoint.
- Run the longer soak budget before release-candidate tagging.
- Confirm no crash, hang, stale rows, duplicate rows, invalid row counts, or
  unbounded process resource growth.

Status:

- Done. Test harness commit `92002da` adds the opt-in 10k+ stress
  fixture, `tree-refresh-stress-10k` scenario, tree collapse/expand churn,
  reload/sort/paint churn, aggregate Shared Files UI suite wiring, resource
  snapshots, and targeted Python coverage.
- Test harness commit `aea5e55` enables REST in the tree stress profile and
  checks `/api/v1/shared-files` row-count convergence before and after churn.
- Test harness commit `6ebc3a7` and build orchestration commit `756819d` expose
  tree stress churn-cycle selection through the aggregate live suite and the
  supported workspace `live-e2e` entrypoint.
- Test harness commit `8d63a45` hardens the tree stress fixture to keep 10k+
  observable nodes with `1024` file rows, selects the stress subtree before the
  initial row-count gate, and extends the heavy scenario startup wait.
- Test harness commit `e751fbb` updates the release target to `50000` shared
  files while keeping the 10k observable-node floor, and raises the heavy
  scenario waits to distinguish slow startup from a hard block.
- Live smoke artifact
  `repos\emulebb-build-tests\reports\shared-files-ui-e2e\20260508-125931-eMule-main-release\tree-refresh-stress-10k\result.json`
  failed before churn with `Timed out waiting for eMule main window`; this is
  tracked as [BUG-101](../items/BUG-101.md).
- Passing 50k smoke artifact
  `repos\emulebb-build-tests\reports\shared-files-ui-e2e\20260508-170043-eMule-main-release\result.json`
  and passing 160-cycle operator soak artifact
  `repos\emulebb-build-tests\reports\shared-files-ui-e2e\20260508-204401-eMule-main-release\tree-refresh-stress-10k\result.json`
  close this gate with resource thresholds enforced by test harness commit
  `f79199e`.

### CI-019 - HTTPS and REST socket adversity stress gate

Implementation:

- Add an HTTPS-enabled live REST profile with deterministic certificate/key
  handling.
- Run the existing contract-stress matrix against HTTPS.
- Add raw socket probes for slow TLS handshake, stalled handshake, reset during
  handshake, reset during headers, reset during declared body, and reset during
  response send.
- Add malformed live payload probes for invalid UTF-8 JSON, empty/non-object
  JSON, oversized body, overlong headers, duplicate `Content-Length`,
  conflicting duplicate sensitive headers, wrong method, and unsupported
  content type.
- Add 32-client and 64-client stress budgets for mixed native REST,
  qBit-compatible, Torznab, and legacy HTML requests.

Validation:

- HTTPS contract-stress completes with expected status and envelope behavior.
- Socket adversity cases close or fail deterministically without hangs.
- Accepted-client threads drain and resource deltas remain bounded.
- Latency percentiles and timeout counts are included in the report.

Status:

- Done. Test harness commit `ad2ac65` adds the `rest_socket_adversity`
  smoke budget with raw socket probes for partial-header reset,
  declared-body reset, conflicting `Content-Length`, overlong headers, and
  invalid UTF-8 JSON. Build orchestration commit `4a531f6` exposes the budget
  through the supported workspace `live-e2e` entrypoint.
- Test harness commit `96f4759` adds the HTTPS WebServer profile path,
  generated local certificate/key material, unverified local HTTPS client
  context, and aggregate suite scheme wiring. Build orchestration commit
  `a229e6c` exposes the scheme selector through the supported workspace
  `live-e2e` entrypoint.
- Test harness commit `e216f44` adds an HTTPS-only TLS handshake adversity
  budget covering stalled connect-close, partial TLS record reset, and partial
  ClientHello reset. Build orchestration commit `17dc429` exposes the same
  budget through the supported workspace `live-e2e` entrypoint.
- Test harness commit `9e130c3` adds a full-request
  `reset_during_response_send` raw socket probe to exercise queued-send cleanup
  when the client resets before consuming the response.
- HTTPS smoke artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-120119-eMule-main-release\result.json`
  passed with `--webserver-scheme https`,
  `--rest-tls-handshake-adversity-budget smoke`, three TLS handshake probes,
  and process resource snapshots after launch and after adversity/stress.
- HTTPS 32-client contract-stress artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-201653-eMule-main-release\result.json`,
  HTTPS 64-client contract-stress artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-202554-eMule-main-release\result.json`,
  and HTTP 64-client socket-adversity artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-203041-eMule-main-release\result.json`
  close this gate. App hardening commit `c5a2794` keeps accepted-client
  concurrency bounded while adding release-gate headroom, and test harness
  commit `d6b4f82` records transient reset retry recovery without masking
  listener death, timeouts, or response-shape regressions.

### CI-020 - REST and legacy WebServer error-path coverage gate

Implementation:

- Create a route/error matrix for native `/api/v1`, qBit-compatible `/api/v2`,
  Torznab, and legacy HTML/static-file surfaces.
- Cover 400, 401/403-style auth failures, 404, 405, 409, 500, and 503 branches
  with explicit expected status and envelope/payload rules.
- Add safe fault-injection seams for 500 paths that cannot be triggered
  reliably from black-box traffic.
- Add reset-during-error-response probes to prove queued-send cleanup.
- Fail the route summary on undeclared 4xx/5xx results.

Validation:

- Every release-relevant error branch has an explicit row and result.
- Native REST errors retain the stable typed JSON envelope.
- Legacy HTML/static-file errors are deterministic and stay bounded.
- Fault-injected 500 paths clean up request state.

Status:

- Done. Test harness commit `36a612a` adds the
  `rest_error_path_matrix` release artifact to live REST reports, including
  observed status counts, covered release statuses, missing release statuses,
  and sampled error responses.
- Test harness commit `f12b49d` adds explicit seam-backed 500 and 503 release
  rows tied to existing `web_api.tests.cpp` coverage for `EMULE_ERROR` and
  `EMULE_UNAVAILABLE`, while preserving `live_missing_release_statuses` for
  live evidence gaps.
- Test harness commit `69b8afa` adds explicit seam-backed 405 and 409 release
  rows tied to existing `web_api.tests.cpp` coverage for `METHOD_NOT_ALLOWED`
  and `INVALID_STATE`.
- HTTP contract artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-120738-eMule-main-release\result.json`
  passed with all release statuses covered by live or seam-backed rows,
  `missing_release_statuses=[]`, and live gaps preserved for 405, 409, 500, and
  503.
- Test harness commit `704a97b` promotes the matrix to a hard release gate and
  adds `reset_during_error_response_send` socket coverage. The Beta 0.7.3 release
  decision keeps 405, 409, 500, and 503 as deterministic seam-backed rows, with
  live gaps visible in `live_missing_release_statuses`. HTTPS artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-202554-eMule-main-release\result.json`
  and HTTP socket-adversity artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-203041-eMule-main-release\result.json`
  both passed with `missing_release_statuses=[]`.

### CI-021 - WebSocket and legacy socket leak-churn gate

Implementation:

- Add resource baselining for process handles, threads, GDI objects, USER
  objects, private bytes, and accepted WebSocket thread counts.
- Run 1k+ HTTP and 1k+ HTTPS connect/reset cycles across idle, partial-header,
  partial-body, slow-response, and queued-response disconnect cases.
- Add legacy listen-socket churn where it can be done without joining the public
  network.
- Run WebSocket stop/start cycles after churn.
- Emit baseline, peak, and post-drain resource counts.

Validation:

- HTTP and HTTPS churn complete without unbounded resource growth.
- Accepted-client threads drain before global WebSocket termination state is
  closed.
- Stop/start succeeds only after a fully drained state.
- The final report identifies any stuck thread, handle, or queued-send state.

Status:

- Done. Test harness commit `1d97dd4` adds live REST process resource
  snapshots after launch and after REST socket adversity/stress, plus deltas for
  handles, GDI objects, USER objects, private bytes, and working set bytes.
- Test harness commit `e88e067` adds selectable HTTP leak-churn smoke and soak
  modes; soak defaults to 1000 connect/reset cycles and reports baseline, peak,
  post-drain, and delta resource counts. Build orchestration commit `94d1044`
  exposes the same controls through supported workspace `live-e2e` parameters.
- Test harness commit `ae3a840` extends leak churn to HTTPS profiles with
  stalled TLS connect-close, partial TLS record reset, and partial ClientHello
  reset cycles.
- Test harness commit `941c439` adds Beta 0.7.3 resource-threshold evaluation for
  leak-churn deltas and fails the run on threshold violations.
- Test harness commit `b8729d3` adds process thread-count snapshots and
  thread-count leak thresholds as accepted-client drain proxy evidence.
- Test harness commit `352a2d2` adds stop/start-after-churn proof for the REST
  smoke harness; build orchestration commit `3ec3674` exposes it through
  `-RestStopStartAfterChurn`.
- HTTPS smoke artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-121849-eMule-main-release\result.json`
  passed 100/100 HTTPS leak-churn cycles with enforced thresholds,
  `resource_thresholds.ok=true`, and zero threshold violations. Observed
  post-drain deltas were handles `+1`, private bytes `+45056`, and working set
  bytes `+57344`.
- HTTP soak artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-122017-eMule-main-release\result.json`
  passed 1000/1000 HTTP leak-churn cycles with enforced thresholds,
  `resource_thresholds.ok=true`, and zero threshold violations. Observed
  post-drain deltas were handles `+1`, private bytes `+442368`, and working set
  bytes `+745472`.
- HTTPS soak artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-122141-eMule-main-release\result.json`
  passed 1000/1000 HTTPS leak-churn cycles with enforced thresholds,
  `resource_thresholds.ok=true`, and zero threshold violations. Observed
  post-drain deltas were GDI objects `+1`, private bytes `+131563520`, and
  working set bytes `+131661824`; handles finished below baseline.
- Thread-count smoke artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-122517-eMule-main-release\result.json`
  passed with process thread count `19 -> 19 -> 19` across baseline, peak, and
  post-drain snapshots, `thread_count` delta `0`, and zero threshold
  violations.
- HTTPS stop/start-after-churn artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-123736-eMule-main-release\result.json`
  passed 100/100 HTTPS leak-churn cycles with enforced thresholds,
  `resource_thresholds.ok=true`, and zero threshold violations. The old process
  `15520` closed in `8590.308` ms, the same profile relaunched as process
  `16760`, and REST readiness returned status `200`.
- Fresh HTTP stop/start soak artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-203500-eMule-main-release\result.json`
  and HTTPS stop/start soak artifact
  `repos\emulebb-build-tests\reports\rest-api-smoke\20260508-203928-eMule-main-release\result.json`
  close this gate with 1000/1000 churn cycles, `resource_thresholds.ok=true`,
  zero threshold violations, and successful post-churn relaunch.

## Release Exit Criteria

All covered items must be `Done` or `Passed` with:

- commit evidence for the harness/test changes
- supported workspace validation command evidence
- smoke artifact evidence
- soak artifact evidence where the item defines an operator soak budget
- documented resource thresholds and observed deltas
