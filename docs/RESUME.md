# eMuleBB Resume Handoff

## Active mandate

Deliver public foundation round 1 as PM and default implementer. Use
[PUBLIC-FOUNDATION](products/emulebb-rust/design/PUBLIC-FOUNDATION.md) as the
contract and phased plan, and
[RUST-REF-016](products/emulebb-rust/active/items/RUST-REF-016.md) for evidence and
remaining qualification. Use the existing Python Harness and Builder; do not
invent launch or monitoring paths. Work one bounded slice at a time, with
scoped checks and granular commits. No standing workers or ordinary delegation.

Fresh profiles only: no migrations, aliases, compatibility shims, remapping or
retired-input handling. Preserve operator profiles and inherited environment.
**No PR, draft PR, merge, main write, release or publication before operator
review.** Sustained soak is follow-up work. Keep the complete goal intact.

## Decision hold

The operator has accepted two decisions:

1. Upload priority and local comment/rating have one persistent hash-level
   owner, editable without an available copy.
2. DELETE removes a server resource, separate from disabling through PATCH;
   later import creates a new ID.

Scan completion tracking is still under discussion: whether acknowledgement and
status expose an opaque token shared by coalesced requests on the existing
worker. No token design is approved. Do not interpret automatic continuations
or silence as approval. PUBLIC-FOUNDATION owns these decisions. The operator
currently requests an explanation of existing scan behavior and implementation
complexity before choosing item 3.

## Source checkpoint

Use the existing managed workstream below
`EMULEBB_WORKSPACE_ROOT/workspaces/agents/public-foundation-round-1` and its
`feature/public-foundation-round-1` branch in each involved repository:

- Rust: `45d8f3cd` (pushed).
- Harness: `0c39dc1a` (pushed).
- Builder: `98fa3d2c` (unchanged).
- Tooling: this handoff and the owning evidence item on the same feature branch.

Rust, Harness and Tooling were clean and synchronized before this handoff edit.
No test/build/container campaign remains running from this session. Completed
specialists are dormant; do not revive them without a concrete difficult task.
Policy and handoff changes on this feature branch are not integrated into main
or the canonical startup checkout; do not claim future sessions inherit them.

## Verified evidence and limits

All paths here are relative to `EMULEBB_WORKSPACE_OUTPUT_ROOT`.

- Rust `d603eb42`: full GNU amd64 package gate, 3,505 workspace tests plus three
  VPN-egress tests and native non-root transfer/restart smoke passed. One ignored
  ownership-child fixture is exercised by its parent tests. Local packages only.
- That GNU archive passed physical 50k-library/100k-retained-job qualification
  at 512 MiB and 100k-library/100k-retained-job qualification at 1 GiB, each with
  one CPU, no swap and no OOM events. Receipts are
  `reports/linux-containers/library/d65ce811618c49d7b894d5486476f94b/report.json`
  and `reports/linux-containers/library/4a9beb312ba0467ea691a83ad0679d42/report.json`.
  Retained downloads are metadata-only history, not active payload pressure.
- Rust `130ca0b2`: Windows release/WebUI build passed with zero warnings. Current
  local REST/OpenAPI campaign passed: 116 declarations, 91 safe operations and
  dedicated persistence/peer/settings phases. Receipt:
  `reports/rust-rest-openapi-ci/20261122T044049Z/report.json`.
- Harness native import repair: 79 tests passed; one Docker/WSL test was skipped
  because `EMULEBB_IMPORT_TEST_IMAGE` was unconfigured. Synthetic import tests
  require a unique pytest `--basetemp` below the output root.
- Rust `45d8f3cd`: library summary/location reads now check profile coherence
  before admission and after SQL await, including absent hashes. 740 Core and
  178 REST tests passed with no warnings. Logs:
  `reports/settings-request-round-1/library-coherence-core.log` and
  `library-coherence-rest.log`.

Do not assign earlier package/live/resource evidence to later revisions.
Canonical library/server REST/OpenAPI/WebUI cutovers, scan completion/calendar
projection, aggregate construction ownership, active payload/session pressure,
expanded canonical-query campaigns and remaining platform/device gates are open.
The current database schema is 114. The overall goal is not complete.
