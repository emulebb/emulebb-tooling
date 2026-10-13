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
| 1 | Backlog documentation cleanup | IN_PROGRESS | Taxonomy, structure, and GitHub records agree |
| 2 | Closure evidence for RUST-BUG-111, 113, and 116 | PENDING | Focused tests prove every retained criterion |
| 3 | Buddy receive-liveness defect | PENDING | Silent half-open buddy links expire and reconnect |
| 4 | RUST-FEAT-047 durable download history | PENDING | Completed hashes survive file removal and restart |

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
  not republish while a genuine reassignment does.
- `RUST-BUG-113`: retain only criteria matching the intentional always-visible
  share-view policy, then prove the encoded capability and request handling.
- `RUST-BUG-116`: seed an expired ban, run the periodic maintenance path, and
  prove the stored record is physically removed.

### 3. Buddy Receive Liveness

- Track the last successfully decoded inbound buddy message.
- Expire a connected buddy link after the bounded inactivity interval even when
  local ping writes continue to succeed.
- Return through the existing reconnect/backoff path without creating a second
  connection authority.

### 4. Durable Download History

- Define a current-only persisted identity store keyed by ED2K file hash, with
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
| 2026-10-13 | Execution tracker created | this commit | Pending documentation gates |

## Resume Checklist

1. Read this file and the owning item for the first non-complete step.
2. Confirm both work branches still descend from the recorded baselines.
3. Check both repository worktrees before editing.
4. Update the relevant row, validation ledger, and design decisions whenever a
   completed slice changes the remaining work.
5. Never infer completion from code alone; retain focused evidence and keep the
   local item plus GitHub workflow record synchronized.
