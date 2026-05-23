# Review — 2026-04-13 Main / Workspace / Analysis Revalidation

> Historical reference only: `stale-v0.72a-experimental-clean` and
> `analysis\stale-v0.72a-experimental-clean` are retired reference sources, not
> active branch targets or current baselines. Use them only as provenance or
> idea-extraction sources; landed status is determined against `main`. See
> [Historical References](../../HISTORICAL-REFERENCES.md).

## Scope

Revalidated the live backlog and historical docs against:

- `workspaces\v0.72a\app\eMule-main`
- `analysis\emuleai`
- `analysis\stale-v0.72a-experimental-clean`
- `repos\emulebb-tooling\docs`
- `repos\emulebb-tooling\docs/active`

Current app repo state at review time:

- `main` = `021cb5b` (`FEAT-025 normalize download filenames on intake and completion`)
- current workspace HEAD = `e1ecdee` (`FEAT-027 cut startup path churn and fix startup sequencing`)

## Findings

### 1. Historical `docs/` status drift is real

The legacy `docs/` set still claimed some cleanup work was already done, but the current
app tree still contains that code.

Revalidated examples in current `eMule-main`:

- `srchybrid/Opcodes.h:261-263` still defines `OP_PEERCACHE_QUERY`, `OP_PEERCACHE_ANSWER`, `OP_PEERCACHE_ACK`
- `srchybrid/ListenSocket.cpp:1287-1289` still handles those defunct opcodes
- `srchybrid/OtherFunctions.cpp:2727-2729` still exposes their string names
- `srchybrid/EMSocket.cpp`, `Preferences.h`, `ServerConnect.h`, `ServerConnect.cpp`, `ListenSocket.cpp` still contain `deadlake PROXYSUPPORT` comments

Result:

- historical claims that REFAC_012 and REFAC_014 were complete were stale
- those tasks were reopened in the legacy `docs/` namespace

### 2. `docs/active` item-file drift existed for landed features

The clean index already knew FEAT-015, FEAT-016, and FEAT-023 were done in `main`, but
their individual item pages still said `status: Open`.

Revalidated landed main commits:

- `d731bbe` — FEAT-015 broadband upload slot allocation
- `860d7a5` — FEAT-016 modern limits
- `5470d69` — FEAT-023 queue scoring extras

Result:

- the item pages were updated to `Done`

### 3. One live untracked bug was found

`SharedFileList.cpp:859` still contains the acknowledged publish-state correctness bug:

- the republish/reset path clears `SetPublishedED2K(false)`
- the Shared Files UI reads `GetPublishedED2K()` directly for icon/text
- the list can therefore show a false `No` until the file is shared again

Cross-variant status:

- present in current `eMule-main`
- present in `analysis\emuleai`
- present in `analysis\stale-v0.72a-experimental-clean`

Result:

- added as `BUG-023`

### 4. No live `#if 0` blocks remain in the reviewed current tree

A targeted `rg "#if\\s+0"` scan on the current `srchybrid` tree found no live matches.

That means:

- the old `#if 0` inventory in `docs/AUDIT-DEADCODE.md` is historical
- the current tree is still carrying other legacy cleanup debt, but not that one

### 5. Current workspace HEAD carries two undocumented post-`main` feature slices

Beyond `main`, the current workspace head carries:

- `FEAT-026` shared startup cache / known.met lookup index / `sharedcache.dat`
- `FEAT-027` startup sequencing fix, profiling, and shared-view startup churn cleanup

`FEAT-025` is already on `main`, so it is tracked as **Done**. `FEAT-026` and
`FEAT-027` remain **In Progress** because they are only on the active feature line.

## Obsolete / Legacy Code Still Live

Revalidated still-open cleanup debt in current `eMule-main`:

- PeerCache opcode baggage remains live
- `deadlake PROXYSUPPORT` attribution comments remain live
- `EncryptedStreamSocket.cpp` still has `ASSERT(0); // must be a bug` sites
- `ArchiveRecovery.cpp` still has `ASSERT(0); // FIXME`
- `ArchiveRecovery.cpp` still has unchecked `malloc()` paths
- `AICHSyncThread.cpp`, `MetaDataDlg.cpp`, `SearchList.cpp` still carry `FIXME LARGE FILES`
- `BaseClient.cpp` still carries `TODO LOGREMOVE`
- multiple files still carry `JOHNTODO` comments

## Docs Updated By This Review

`docs/active`:

- `INDEX.md`
- `BUG-023.md`
- `FEAT-015.md`
- `FEAT-016.md`
- `FEAT-023.md`
- `FEAT-025.md`
- `FEAT-026.md`
- `FEAT-027.md`
- this review file

Historical `docs/`:

- `AUDIT-DEADCODE.md`
- `REFACTOR-TASKS.md`
- `INDEX.md`

## Practical Takeaway

The live backlog is now aligned with the current `main` app line, the current workspace
head, and the two comparison trees used in this review. The main remaining discrepancies
were documentation drift, not hidden merged fixes.
