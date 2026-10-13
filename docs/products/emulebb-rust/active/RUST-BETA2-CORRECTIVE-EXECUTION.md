# Rust Beta 2 Corrective Execution

This plan is the durable execution ledger for the corrective sequence approved
on 2026-10-13. It records decisions and evidence that must survive individual
agent sessions. The owning backlog items remain authoritative for engineering
scope, while GitHub issues and eMuleBB Roadmap Project #3 remain authoritative
for workflow state.

## Baseline And Branches

- Product baseline: `emulebb-rust` `main` at `29d5316f`.
- Documentation baseline: `emulebb-tooling` `main` at `1ef6867`.
- Product work branch: `work/rust-beta2-corrective-20261013`.
- Documentation work branch: `work/rust-beta2-corrective-20261013`.
- Protected `main` is never edited directly; every coherent slice lands as a
  granular commit and is reviewed before integration.

## Approved Sequence

| Step | Scope | State | Exit Gate |
|------|-------|-------|-----------|
| 1 | Backlog documentation cleanup | COMPLETE | Taxonomy, structure, and GitHub records agree |
| 2 | Closure evidence for RUST-BUG-111, 113, and 116 | COMPLETE | Focused tests prove every retained criterion |
| 3 | Buddy receive-liveness defect | COMPLETE | Silent half-open buddy links expire and reconnect |
| 4 | RUST-FEAT-047 durable download history | IN_PROGRESS | Completed hashes survive file removal and restart |

## Design Decisions

- The product is in beta. Persisted schema, REST API, and configuration may
  break when doing so yields a cleaner long-term design. Do not add migrations,
  compatibility aliases, fallback reads, or deprecated fields.
- `RUST-FEAT-048` must keep future completion-capacity reservation based on
  remaining logical bytes. Sparse allocation and allocated-byte measurement are
  current-usage concerns and must not weaken that reservation invariant.
- One-shot ED2K server sessions do not publish files. Their omission of the
  `offerfiles_v` extension should be an explicit centralized policy, not forced
  fingerprint uniformity and not an accidental `Default` value.
- Server user-search and `OP_INVALID_LOWID` remain unsupported unless executable
  stock/aMule behavior or an independent product requirement is demonstrated;
  opcode declarations alone are not implementation authority.
- Already-downloaded recognition needs a durable completed-download identity
  store. The current shared catalog and active transfer index are insufficient
  because users may move or delete completed files.
- Completed-download history stores content identity and completion metadata,
  never a live-path claim. It has no foreign key to current transfer, share, or
  path rows, and schema `31` intentionally requires a fresh beta profile.
- The authoritative completion-manifest transaction records history only for a
  completed, final-rehash-clean download. Share-in-place manifests are excluded;
  repeat completions preserve the first completion time and reject conflicting
  size or non-null AICH identity.
- Current-local evidence is revalidated against the filesystem and expected
  size before it can block a download. Historical evidence remains pathless and
  survives transfer cleanup, payload removal, and process restart.
- Shared-source identity is independent of transfer state. A deliberate
  re-download may reset managed partial state while preserving an independently
  shared file as upload-readable catalog evidence.
- `KnownFilePolicy` is the single creation policy for ED2K links and search
  results. `reject` is the default; `redownload` applies only to current-local
  or historical evidence. Active transfers, identity mismatches, and duplicate
  hashes within one request are never overrideable.
- Duplicate preflight is serialized across transfer-creation requests and runs
  before transfer/source mutation. REST returns `DOWNLOAD_CONFLICT` with typed
  evidence, and WebUI retries with `redownload` only after explicit confirmation.
- Buddy liveness is based on received peer activity, not merely successful
  writes or recurring local pings.

## Step Details

### 1. Backlog Documentation Cleanup

- Add `RUST-BUG-117` for buddy received-activity expiry.
- Reframe `RUST-BUG-112` around centralized session-role policy.
- Correct `RUST-FEAT-048` capacity semantics.
- Expand `RUST-FEAT-047` to durable completed-download history.
- Correct the AICH rationale in `RUST-FEAT-050`.
- Close `RUST-FEAT-042` and `RUST-FEAT-051` as unsupported parity proposals.
- Close disposition-only `RUST-REF-012` through `RUST-REF-015` after durable
  parity evidence is recorded.

### 2. Closure Evidence

- `RUST-BUG-111`: observe server output and prove redundant `OP_IDCHANGE` does
  not republish while a genuine reassignment does. Audit finding: reassignment
  currently re-enters startup but does not clear the published-hash epoch, so a
  non-empty catalog is not actually republished.
- `RUST-BUG-113`: reopen the item. The peer listener intentionally returns an
  empty share list and denies directory browsing, but hello currently advertises
  `no_view_shared_files = 0`. Restore truthful bit `1`; a future browsable-share
  feature must own any configurable allow state.
- `RUST-BUG-116`: seed an expired ban, run the periodic maintenance path, and
  prove the stored record is physically removed. Add retained-entry counts as
  runtime observability so the integration test does not rely on expiry-aware
  lookup behavior.

### 3. Buddy Receive Liveness

- Track the last successfully decoded inbound buddy message.
- Expire a connected buddy link after the bounded inactivity interval even when
  local ping writes continue to succeed.
- Return through the existing reconnect/backoff path without creating a second
  connection authority.

### 4. Durable Download History

- Define a durable persisted identity store keyed by ED2K file hash, with
  the metadata required for user-visible duplicate decisions.
- Record history atomically at successful completion before active-transfer
  cleanup can remove the only durable identity.
- Consult active transfers, current shared files, and completed history through
  one duplicate-decision service used by every transfer-creation entry point.
- Expose explicit API behavior for reject, inspect, and deliberate re-download;
  do not silently discard user intent.

## Validation Ledger

| Date | Slice | Commit | Evidence |
|------|-------|--------|----------|
| 2026-10-13 | Execution tracker created | `5919ad8` | Taxonomy and structure checks pass |
| 2026-10-13 | Backlog contracts corrected | `f44ea99` | Items 112, 047, 048, and 050 synchronized to GitHub |
| 2026-10-13 | Unsupported features closed | `e3ec08e` | GitHub issues 85 and 94 closed not planned |
| 2026-10-13 | Offerfiles extension registered | `afb56cb1` / `9960035` | TOML, taxonomy, and structure checks pass; issue 100 closed |
| 2026-10-13 | Buddy liveness tracked | `dcd9d23` | GitHub issue 103 added to Project #3 as Rust Phase 1 Todo |
| 2026-10-13 | RUST-BUG-111 completed | `4b04be6b` | 1,026 crate tests pass; IDCHANGE wire behavior proven |
| 2026-10-13 | RUST-BUG-113 completed | `3f3bb819` | Hello capability and empty/denied browse policy agree |
| 2026-10-13 | RUST-BUG-116 completed | `c3707c12` / `dfd4c2f7` | 1,026 ED2K tests and all 426 core tests pass; physical pruning proven |
| 2026-10-13 | RUST-BUG-117 completed | `92688d17` / `6a822d1e` / `5225f8f2` / `50227302` | 1,032 ED2K and 428 core tests pass; deterministic liveness and reconnect handoff proven |
| 2026-10-13 | RUST-FEAT-047 history foundation | `576f1b53` | All 38 metadata tests and strict metadata Clippy pass; completion history survives manifest deletion and conflicting identity rolls back atomically |
| 2026-10-13 | RUST-FEAT-047 evidence classification | `995efd2a` | Active, verified-current, and pathless-history evidence are distinguished; restart, absent-file, and removed-payload cases are covered |
| 2026-10-13 | RUST-FEAT-047 re-download storage model | `b09063f7` / `50c14ca1` | Deliberate re-download resets managed transfer state while preserving independent shares and upload readability across restart |
| 2026-10-13 | RUST-FEAT-047 creation authority | `abf711c8` | All 399 core tests and core integrations pass; strict all-target core Clippy passes; batch conflicts do not partially mutate state |
| 2026-10-13 | RUST-FEAT-047 REST conflict surface | `b401bf08` | 117 REST unit tests, 2 REST integrations, and strict all-target REST Clippy pass; both creation routes return typed 409 conflicts |
| 2026-10-13 | RUST-FEAT-047 OpenAPI contract | `6b83783` | YAML parses as OpenAPI 3.1; route checker reports only the pre-existing search sort/order query drift |
| 2026-10-13 | RUST-FEAT-047 WebUI conflict handling | `aeeff64b` / `35be62f7` | 28 unit tests, production build, and all 16 Playwright tests pass; both entry points default to reject and require confirmation before retry |

The global `github-roadmap-check.py --github` run still reports 244 legacy
MFC-label synchronization errors outside this Rust slice. The new Rust issue's
repository, product, phase, and status fields were verified directly in Project
#3; no unrelated labels were changed.

## Resume Checklist

1. Read this file and the owning item for the first non-complete step.
2. Confirm both work branches still descend from the recorded baselines.
3. Check both repository worktrees before editing.
4. Update the relevant row, validation ledger, and design decisions whenever a
   completed slice changes the remaining work.
5. Never infer completion from code alone; retain focused evidence and keep the
   local item plus GitHub workflow record synchronized.
