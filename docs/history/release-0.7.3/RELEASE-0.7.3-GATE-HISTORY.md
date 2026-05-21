# eMule Broadband Edition 0.7.3 Gate History

> Historical release evidence only. Current beta `0.7.3` status is controlled
> by [RELEASE-0.7.3](../../active/RELEASE-0.7.3.md), and current execution is
> controlled by
> [RELEASE-0.7.3-EXECUTION-PLAN](../../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md).

This is the archived internal control document for rehearsal tag
`emule-bb-v1.0.0`. It records Release 1 gate status, candidate decisions, and
readiness evidence from the internal pre-release pass.

Current status: Release 1 gate proof has fresh 2026-05-09 revalidation
evidence, rehearsal packages were created, and the annotated internal app tag
`emule-bb-v1.0.0` was pushed to `eMulebb/eMule` at app commit `953a39f`.
This tag and its assets are superseded internal evidence only; the first beta
release target is `emule-bb-v0.7.3`.

Operator docs:

- [Beta 0.7.3 checklist](../../active/RELEASE-0.7.3-CHECKLIST.md)
- [Beta 0.7.3 runbook](../../active/RELEASE-0.7.3-RUNBOOK.md)
- [REST/Arr execution plan](RELEASE-0.7.3-REST-ARR-EXECUTION-PLAN.md)
- [Live E2E execution plan](RELEASE-0.7.3-LIVE-E2E-EXECUTION-PLAN.md)
- [Download completion hook execution plan](RELEASE-0.7.3-DOWNLOAD-COMPLETION-HOOK-EXECUTION-PLAN.md)
- [NAT mapping execution plan](RELEASE-0.7.3-NAT-MAPPING-EXECUTION-PLAN.md)
- [Beta 0.7.3 stability blockers execution plan](RELEASE-0.7.3-STABILITY-BLOCKERS-EXECUTION-PLAN.md)
- [SDET stress execution plan](RELEASE-0.7.3-SDET-STRESS-EXECUTION-PLAN.md)

## Release Identity

- Product name: `eMule broadband edition`
- Compact app/mod name: `eMule BB`
- Internal rehearsal tag: `emule-bb-v1.0.0`
- Internal rehearsal assets:
  - `eMule-broadband-1.0.0-x64.zip`
  - `eMule-broadband-1.0.0-arm64.zip`

## Release Gates

These gates must remain passed, or be explicitly revalidated if their evidence
ages out or related code changes.

Current REST hardening focus: revalidate both the native `/api/v1` contract and
the Arr/qBittorrent-compatible adapter APIs before tagging. The detailed pending
task queue lives in the
[REST/Arr execution plan](RELEASE-0.7.3-REST-ARR-EXECUTION-PLAN.md#current-revalidation-focus).
aMuTorrent remains the primary UI proof target, but it adapts to the clean
native `/api/v1` design and must not drive native route shape, aliases,
envelopes, or validation policy.

Current stability focus: the original adversarial current-branch findings from
the 2026-05-08 Beta 0.7.3 review are closed on `main`, the first 2026-05-08 follow-up
pass findings [BUG-092](../items/BUG-092.md) through [BUG-096](../items/BUG-096.md)
are closed on `main`, and the latest follow-up blockers
[BUG-097](../items/BUG-097.md), [BUG-099](../items/BUG-099.md), and
[BUG-100](../items/BUG-100.md) are now closed on `main`. Archive preview and
recovery findings [BUG-074](../items/BUG-074.md) and
[BUG-098](../items/BUG-098.md) are Wont-Fix by product decision because those
deprecated features are entirely frozen, including known bugs. Keep their
execution and closure flow in the
[Beta 0.7.3 stability blockers execution plan](RELEASE-0.7.3-STABILITY-BLOCKERS-EXECUTION-PLAN.md).

Current SDET stress focus: the 2026-05-08 test-robustness review promoted four
additional Beta 0.7.3 release gates for large Shared Files UI churn, HTTPS/socket
adversity, explicit error-path coverage, and resource-accounted socket leak
churn. Keep their execution and closure flow in the
[SDET stress execution plan](RELEASE-0.7.3-SDET-STRESS-EXECUTION-PLAN.md).

| ID | Gate | Status | Evidence pointer |
|----|------|--------|------------------|
| [BUG-075](../items/BUG-075.md) | REST typed error consistency | Passed | item completion evidence |
| [BUG-076](../items/BUG-076.md) | Malformed WebServer/REST hardening | Passed | item completion evidence |
| [BUG-077](../items/BUG-077.md) | Concurrent WebServer soak | Passed | item completion evidence |
| [CI-011](../items/CI-011.md) | Release live E2E umbrella | Done | item completion evidence and full `live-e2e` report `20260509-093500-eMule-main-release`; `auto-browse-live` accepted inconclusive for unavailable live browse-capable source |
| [CI-014](../items/CI-014.md) | REST manifest/live completeness gate | Passed | item completion evidence |
| [CI-015](../items/CI-015.md) | REST malformed/concurrent matrix | Passed | item completion evidence |
| [AMUT-001](../items/AMUT-001.md) | aMuTorrent live E2E validation | Passed | item completion evidence; fresh artifact `20260509-081711-eMule-main-release` |
| [AMUT-002](../items/AMUT-002.md) | aMuTorrent transfer detail hydration | Passed | item completion evidence and fresh aMuTorrent browser smoke artifact `20260509-081711-eMule-main-release` |
| [ARR-001](../items/ARR-001.md) | Arr live E2E validation | Passed | item completion evidence; fresh Prowlarr artifact `20260509-102138-eMule-main-release` and Radarr/Sonarr artifact `20260509-102255-eMule-main-release`; media searches used video categories |
| [FEAT-050](../items/FEAT-050.md) | Download completion hook | Passed | item completion evidence |
| [BUG-078](../items/BUG-078.md) | qBit auth fails closed on session RNG failure | Done | app `02fd5bf`, tests `dfc86d6`, Release x64 validation |
| [BUG-079](../items/BUG-079.md) | WebSocket accepted-client shutdown lifetime | Done | app `aa66699`, Release x64 validation |
| [BUG-080](../items/BUG-080.md) | WebSocket shutdown avoids `TerminateThread` | Done | app `aa66699`, Release x64 validation |
| [BUG-081](../items/BUG-081.md) | HTTPS WebSocket WANT_READ/WANT_WRITE loops yield to socket waits | Done | app `aa66699`, Release x64 validation |
| [BUG-082](../items/BUG-082.md) | GeoLocation/IPFilter refresh state cannot wedge | Done | app `e5c8f81`, Release x64 validation |
| [BUG-083](../items/BUG-083.md) | Client UDP malformed-packet logging is bounds-safe | Done | app `1af8bb5`, tests `cfe9b96`, Release x64 validation |
| [BUG-084](../items/BUG-084.md) | Web admin process token handles are closed | Done | app `1513358`, Release x64 validation |
| [BUG-085](../items/BUG-085.md) | Kad/client UDP encryption gating has compatibility proof | Done | app `2ee49ab`, tests `2d5cc1a`, Release x64 validation |
| [BUG-086](../items/BUG-086.md) | HTTPS WebSocket mbedTLS socket context ABI is safe | Done | app `c6c1526`, Release x64 validation |
| [BUG-087](../items/BUG-087.md) | HTTPS WebSocket queued TLS writes cannot stall on WANT_READ | Done | app `dfcf1fe`, Release x64 validation |
| [BUG-088](../items/BUG-088.md) | WebSocket failed shutdown cannot poison restart | Done | app `7a5de38`, Release x64 validation |
| [BUG-089](../items/BUG-089.md) | UDP control sender is exception-safe under `sendLocker` | Done | app `4796d2f`, Release x64 validation |
| [BUG-090](../items/BUG-090.md) | Background refresh completion cannot wedge on failed UI post | Done | app `1a09692`, Release x64 validation |
| [BUG-091](../items/BUG-091.md) | DirectDownload rejects close-time persistence failures | Done | app `c237d48`, Release x64 validation |
| [BUG-092](../items/BUG-092.md) | Background refresh workers cannot write through freed owner memory | Done | app `cfb0625`, Debug and Release x64 validation |
| [BUG-093](../items/BUG-093.md) | Failed refresh completion cannot synchronously block worker on UI thread | Done | app `2823a5c`, Debug and Release x64 validation |
| [BUG-094](../items/BUG-094.md) | Refresh launch failure cannot leak suspended thread objects | Done | app `e5d770e`, Debug and Release x64 validation |
| [BUG-095](../items/BUG-095.md) | WebSocket accepted-client tracking is exception-safe after thread start | Done | app `219be75`, Debug and Release x64 validation |
| [BUG-096](../items/BUG-096.md) | DirectDownload has bounded timeout or cancellation semantics | Done | app `84020af`, Debug and Release x64 validation |
| [BUG-097](../items/BUG-097.md) | Startup-cache save worker cannot outlive shared-file list owner | Done | app `bde9f16`, Debug and Release x64 validation |
| [BUG-074](../items/BUG-074.md) | Archive preview scanner uses volatile cancellation and synchronous UI handoff | Wont-Fix | deprecated/frozen by product decision; app `8c2cc67` source comment |
| [BUG-098](../items/BUG-098.md) | Archive recovery worker uses raw part-file owner across async work | Wont-Fix | deprecated/frozen by product decision; app `8c2cc67` source comment |
| [BUG-099](../items/BUG-099.md) | WebSocket listener startup is exception-safe after global state initialization | Done | app `a4c4dc3`, Debug and Release x64 validation |
| [BUG-100](../items/BUG-100.md) | DirectDownload has hard owner cancellation for background refresh downloads | Done | app `9d765e3`, Debug and Release x64 validation |
| [BUG-101](../items/BUG-101.md) | Shared Files 50k recursive tree stress profile reaches main window | Done | passing artifact `20260508-170043-eMule-main-release`; 50k rows converged cold, after churn, and cached relaunch |
| [CI-018](../items/CI-018.md) | Shared Files 50k-file tree refresh stress gate | Done | tests `92002da`, `aea5e55`, `6ebc3a7`, `8d63a45`, `e751fbb`, `f79199e`, build `756819d`; 50k smoke artifact `20260508-170043-eMule-main-release` and 160-cycle soak artifact `20260508-204401-eMule-main-release` passed with resource thresholds |
| [CI-019](../items/CI-019.md) | HTTPS and REST socket adversity stress gate | Done | tests `ad2ac65`, `96f4759`, `e216f44`, `9e130c3`, `f00ad31`, `704a97b`, `d6b4f82`, build `4a531f6`, `a229e6c`, `17dc429`, app `c5a2794`; HTTPS 32/64 contract-stress artifacts and HTTP socket-adversity artifact passed |
| [CI-020](../items/CI-020.md) | REST and legacy WebServer error-path coverage gate | Done | tests `36a612a`, `f12b49d`, `69b8afa`, `704a97b`; app `2263e64`, `4082be7`, `d1c8af6`, `1ca8c63`, `979ae8f`, `ddff25f`, `c6927cb`, `c062058`, `440e5e5`, `5f0689f`; hard error matrix artifacts `20260508-202554-eMule-main-release` and `20260508-203041-eMule-main-release` passed |
| [CI-021](../items/CI-021.md) | WebSocket and legacy socket leak-churn gate | Done | tests `1d97dd4`, `e88e067`, `ae3a840`, `941c439`, `b8729d3`, `352a2d2`, build `94d1044`, `3ec3674`; app `d75919a`, `1ca4d49`, `b33efb8`, `2cca5ac`, `942c484`, `c5a2794`; HTTP/HTTPS 1000-cycle leak-churn stop/start soaks `20260508-203500-eMule-main-release` and `20260508-203928-eMule-main-release` passed |

## Candidate Decisions

These items are desirable but are not Release 1 blockers unless a later gate
failure proves that they are required.

| ID | Candidate | Release 1 decision |
|----|-----------|--------------------|
| [FEAT-032](../../active/items/FEAT-032.md) | NAT mapping live validation | Deferred; Release E2E did not require NAT proof |
| [FEAT-045](../items/FEAT-045.md) | Transfer detail endpoint | Passed; promoted with `AMUT-002` capability-gated aMuTorrent consumption |
| [FEAT-046](../items/FEAT-046.md) | Server/Kad bootstrap/import APIs | Passed; server.met import, Kad bootstrap, nodes.dat URL import, malformed preservation, and live seed import evidence are covered |
| [FEAT-047](../items/FEAT-047.md) | Search API completeness | Passed; OpenAPI and REST contract document Release 1 behavior |
| [FEAT-048](../items/FEAT-048.md) | Upload queue control completeness | Passed; existing controls are covered, unsupported operations return typed errors, and no new queue mutation was promoted |
| [FEAT-049](../items/FEAT-049.md) | Curated REST preference expansion | Passed; aMuTorrent needs no additional runtime preference keys and the curated surface has live round-trip plus bad-value coverage |

## Execution Plans

Each Release 1 gate and candidate is covered by exactly one cluster execution
plan. Item docs keep acceptance criteria and evidence; the plans own detailed
closure and revalidation flow.

| Plan | Covered items |
|------|---------------|
| [REST/Arr execution plan](RELEASE-0.7.3-REST-ARR-EXECUTION-PLAN.md) | [BUG-075](../items/BUG-075.md), [BUG-076](../items/BUG-076.md), [BUG-077](../items/BUG-077.md), [CI-014](../items/CI-014.md), [CI-015](../items/CI-015.md), [AMUT-001](../items/AMUT-001.md), [ARR-001](../items/ARR-001.md), [FEAT-045](../items/FEAT-045.md), [FEAT-046](../items/FEAT-046.md), [FEAT-047](../items/FEAT-047.md), [FEAT-048](../items/FEAT-048.md), [FEAT-049](../items/FEAT-049.md), [AMUT-002](../items/AMUT-002.md) |
| [Live E2E execution plan](RELEASE-0.7.3-LIVE-E2E-EXECUTION-PLAN.md) | [CI-011](../items/CI-011.md) |
| [Download completion hook execution plan](RELEASE-0.7.3-DOWNLOAD-COMPLETION-HOOK-EXECUTION-PLAN.md) | [FEAT-050](../items/FEAT-050.md) |
| [NAT mapping execution plan](RELEASE-0.7.3-NAT-MAPPING-EXECUTION-PLAN.md) | [FEAT-032](../../active/items/FEAT-032.md) |
| [Beta 0.7.3 stability blockers execution plan](RELEASE-0.7.3-STABILITY-BLOCKERS-EXECUTION-PLAN.md) | [BUG-078](../items/BUG-078.md), [BUG-079](../items/BUG-079.md), [BUG-080](../items/BUG-080.md), [BUG-081](../items/BUG-081.md), [BUG-082](../items/BUG-082.md), [BUG-083](../items/BUG-083.md), [BUG-084](../items/BUG-084.md), [BUG-085](../items/BUG-085.md), [BUG-086](../items/BUG-086.md), [BUG-087](../items/BUG-087.md), [BUG-088](../items/BUG-088.md), [BUG-089](../items/BUG-089.md), [BUG-090](../items/BUG-090.md), [BUG-091](../items/BUG-091.md), [BUG-092](../items/BUG-092.md), [BUG-093](../items/BUG-093.md), [BUG-094](../items/BUG-094.md), [BUG-095](../items/BUG-095.md), [BUG-096](../items/BUG-096.md), [BUG-097](../items/BUG-097.md), [BUG-074](../items/BUG-074.md), [BUG-098](../items/BUG-098.md), [BUG-099](../items/BUG-099.md), [BUG-100](../items/BUG-100.md) |
| [SDET stress execution plan](RELEASE-0.7.3-SDET-STRESS-EXECUTION-PLAN.md) | [CI-018](../items/CI-018.md), [CI-019](../items/CI-019.md), [CI-020](../items/CI-020.md), [CI-021](../items/CI-021.md) |

## Deferred Scope

The following tracks stay outside the first beta release unless a later
release-readiness review promotes a concrete blocker:

- abandoned Boost/POCO and CMake/Ninja/vcpkg adoption ideas: `REF-008`
  through `REF-014`, `CI-001`
- broad CI/toolchain migration: `CI-002` through `CI-007`, `CI-010`
- dependency upgrades: `REF-028`, `REF-034`
- broad networking work: `REF-029`, `REF-030`, `FEAT-018`, `FEAT-035`,
  `FEAT-036`
- broad product/UI expansion: `FEAT-017`, `FEAT-019`, `FEAT-021`,
  `FEAT-031`, `FEAT-037`, `FEAT-039` through `FEAT-044`
- non-release hardening watchpoints: `BUG-031`, `BUG-034`, `BUG-035`,
  `FEAT-001` through `FEAT-006`, `FEAT-034`, `CI-008`, `CI-012`,
  `CI-013`

## Validation

Before tagging `emule-bb-v1.0.0`, run the supported workspace commands:

- `python -m emule_workspace validate`
- `python -m emule_workspace build app --config Debug --platform x64`
- `python -m emule_workspace build app --config Release --platform x64`
- `python -m emule_workspace build tests --config Debug --platform x64`
- `python -m emule_workspace build tests --config Release --platform x64`
- native parity tests through the supported `test` command
- Release x64 `live-e2e`, including aMuTorrent, Prowlarr, Radarr, and Sonarr

Public-network unavailable results are acceptable only when the harness records
the run as inconclusive with enough diagnostics to distinguish environment
failure from product failure.
