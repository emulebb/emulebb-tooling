# eMule Active Backlog — Issue Index

This directory is the active local backlog/spec and revalidation layer for this
repo. Use [`../INDEX.md`](../INDEX.md) for long-form background and reference
reading.

GitHub-primary backlog workflow uses `emulebb/emulebb` issues
(`https://github.com/emulebb/emulebb/issues`) and the public `eMuleBB Roadmap`
org Project #2 (`https://github.com/orgs/emulebb/projects/2`) as current
status, priority, release placement, discussion, ownership, and PR linkage
authority for migrated items. Local item docs marked `workflow: github` are
engineering spec/evidence records, not workflow status authority.

> Historical reference only: `stale-v0.72a-experimental-clean` and
> `analysis\stale-v0.72a-experimental-clean` are retired reference sources, not
> active branch targets or current baselines. Use them only as provenance or
> idea-extraction sources; landed status is determined against `main`. See
> [Historical References](../HISTORICAL-REFERENCES.md).

## Current Snapshot

**Source of truth:** `EMULE_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main` (`main` branch)
**Current non-done count:** `77`
**Latest release-doc refresh:** 2026-05-23
**Non-done by status:** `58` OPEN, `8` IN_PROGRESS, `11` DEFERRED, `0` BLOCKED.
**Backlog counts:** item tables below are authoritative.
**RC 0.7.3 relevance:** Most non-done items below are future or deferred work;
current RC gate and proof status is controlled by [RELEASE-0.7.3](RELEASE-0.7.3.md).
**Broadband release status:** `emulebb-v0.7.3-rc.1` is the first public
release-candidate target.
**RC-release backlog view:** [RELEASE-0.7.3](RELEASE-0.7.3.md)
**RC-release checklist:** [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md)
**RC-release runbook:** [RELEASE-0.7.3-RUNBOOK](RELEASE-0.7.3-RUNBOOK.md)
**Release test strategy:** [RELEASE-TEST-STRATEGY](RELEASE-TEST-STRATEGY.md)
**Release test campaigns:** [RELEASE-TEST-CAMPAIGNS](RELEASE-TEST-CAMPAIGNS.md)
**Frozen surfaces:** [FROZEN-SURFACES](FROZEN-SURFACES.md)
**RC controller surface matrix:** [CONTROLLER-SURFACE-MATRIX](CONTROLLER-SURFACE-MATRIX.md)
**Future release roadmap:** [FUTURE-ROADMAP](FUTURE-ROADMAP.md)
**GitHub-primary backlog workflow:** GitHub issues in `emulebb/emulebb` plus
the `eMuleBB Roadmap` Project #2 are authoritative for migrated backlog items.
**Backlog process runbook:** [BACKLOG-PROCESS](../reference/BACKLOG-PROCESS.md)
**RC-release execution plan:** [RELEASE-0.7.3-EXECUTION-PLAN](plans/RELEASE-0.7.3-EXECUTION-PLAN.md)
**p2p-overlord product-family plan:** [P2P-OVERLORD-PRODUCT-FAMILY-INTEGRATION](plans/P2P-OVERLORD-PRODUCT-FAMILY-INTEGRATION.md)
**Historical beta evidence:** `docs/history/release-0.7.3/`
**Historical reviews:** `docs/history/reviews/`
**Closed item records:** `docs/history/items/`

Current release trail:

- [RELEASE-0.7.3](RELEASE-0.7.3.md)
- [RELEASE-0.7.3-CHECKLIST](RELEASE-0.7.3-CHECKLIST.md)
- [RELEASE-0.7.3-RUNBOOK](RELEASE-0.7.3-RUNBOOK.md)
- [RELEASE-TEST-STRATEGY](RELEASE-TEST-STRATEGY.md)
- [RELEASE-TEST-CAMPAIGNS](RELEASE-TEST-CAMPAIGNS.md)
- [CONTROLLER-SURFACE-MATRIX](CONTROLLER-SURFACE-MATRIX.md)
- [RELEASE-0.7.3 execution plan](plans/RELEASE-0.7.3-EXECUTION-PLAN.md)

## Operating Rules

**Priority scale:** Critical > Major > Minor > Trivial  
**Status values:** OPEN / IN_PROGRESS / BLOCKED / DEFERRED / PASSED / DONE /
WONT_DO

**Directory role:** `docs/active/` owns current local specs, release control,
active item evidence, and the current release execution plan. Closed item
records and dated review provenance live under `docs/history/`. For
GitHub-primary items marked `workflow: github`, current workflow state lives in
GitHub.

**Important:** Items marked OPEN, IN_PROGRESS, BLOCKED, or DEFERRED link to
active item records. Items marked DONE, PASSED, or WONT_DO link to archived
item records under `docs/history/items/`. IN_PROGRESS work may already be
implemented on dedicated bug/feature branches but is not considered landed
until merged to `main`. Experimental-only work (see individual docs) is not in
`main` unless the item status below says otherwise.

**Revalidation rule:** Before implementing any item, re-check it against current `main`
and current dependency pins.

**Regression rule:** New feature/fix work from this backlog should include targeted
regression checks. When behavior changes, compare `main` against
`baseline/community-0.72a` as the seam-enabled parity and regression baseline
where that comparison is meaningful.

**RC 0.7.3 source rule:** the public RC tag is cut from the selected
reviewed `main` commit after refreshed proof passes and operator approval.
The release stabilization branch is `release/0.7.3` once the operator starts
the RC branch.

**Baseline stack rule:**

- variant key `community` maps to worktree `app\emulebb-community-baseline`
  on branch `baseline/community-0.72a`; it is the seam-enabled parity and
  regression baseline, test-only
- variant key `tracing-harness` maps to worktree
  `app\emulebb-community-tracing-harness` on branch
  `tracing-harness/community-0.72a`; it is the behavior-changing
  variant-client parity harness, not the default baseline

---

## Bugs

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [BUG-001](../history/items/BUG-001.md) | Major | DONE | 17+ load-only hidden prefs not written back to preferences.ini |
| [BUG-002](../history/items/BUG-002.md) | Minor | WONT_DO | ASSERT(0) FIXME in ArchiveRecovery.cpp — silent fail in release *(kept as-is by product decision)* |
| [BUG-003](../history/items/BUG-003.md) | Minor | DONE | Historical large-file FIXME markers overstated the remaining live issue |
| [BUG-004](../history/items/BUG-004.md) | Minor | DONE | IPFilter overlapping IP ranges not handled — acknowledged correctness gap |
| [BUG-005](../history/items/BUG-005.md) | Minor | WONT_DO | Kad buddy connections broken when RequireCrypt is enabled |
| [BUG-006](../history/items/BUG-006.md) | Minor | WONT_DO | Weak RNG for crypto challenge — rand() seeded with time(NULL) *(accepted risk by product decision)* |
| [BUG-007](../history/items/BUG-007.md) | Minor | DONE | Ring.h — three UB + correctness bugs in CRing\<T\> (CODEREV_003, 004, 011) |
| [BUG-008](../history/items/BUG-008.md) | Minor | WONT_DO | CaptchaGenerator — rand() & 8 bimodal jitter *(low release value; leave to REF-027 if reopened)* |
| [BUG-009](../history/items/BUG-009.md) | Minor | DONE | PartFile — non-atomic part.met replacement (_tremove + _trename crash window) |
| [BUG-010](../history/items/BUG-010.md) | Minor | DONE | PartFile — part.met write on low disk space risks truncation/corruption |
| [BUG-011](../history/items/BUG-011.md) | Minor | DONE | Race — shareddir_list iterated without lock in SendSharedDirectories |
| [BUG-012](items/BUG-012.md) | Minor | IN_PROGRESS | CPartFile destructor calls FlushBuffer after write thread has already exited |
| [BUG-013](../history/items/BUG-013.md) | Minor | WONT_DO | ArchiveRecovery.cpp — three unchecked malloc() calls crash on OOM *(kept as-is by product decision)* |
| [BUG-014](../history/items/BUG-014.md) | Minor | DONE | ZIPFile.cpp — WriteFile return value silently discarded on two paths |
| [BUG-015](../history/items/BUG-015.md) | Minor | DONE | GetTickCount() 49-day overflow in ban expiry and download timeout checks |
| [BUG-016](../history/items/BUG-016.md) | Minor | DONE | UDP obfuscation applied when crypt layer is disabled — IsCryptLayerEnabled() guard missing |
| [BUG-017](../history/items/BUG-017.md) | Minor | DONE | UDP throttler deadlock — sendLocker held when signaling QueueForSendingControlPacket |
| [BUG-018](../history/items/BUG-018.md) | Minor | DONE | Part-file hash layout drift — hash tree can mutate during concurrent hashing |
| [BUG-019](../history/items/BUG-019.md) | Minor | DONE | AICH sync thread concurrency — UI deadlocks, starvation, incomplete/duplicate nodes |
| [BUG-020](../history/items/BUG-020.md) | Minor | DONE | Client socket teardown ordering — cross-link not cleared before Safe_Delete |
| [BUG-021](../history/items/BUG-021.md) | Minor | DONE | Upload queue lock inversion + socket I/O result mishandling + inflate buffer aliasing |
| [BUG-022](../history/items/BUG-022.md) | Major | DONE | Long-path delete-to-recycle-bin still breaks in ShellDeleteFile |
| [BUG-023](../history/items/BUG-023.md) | Minor | DONE | Shared-file ED2K published column shows a false `No` after publish-state reset |
| [BUG-024](../history/items/BUG-024.md) | Minor | DONE | `statUTC(HANDLE)` returns corrupted `st_size` by using `nFileIndexLow` |
| [BUG-025](../history/items/BUG-025.md) | Minor | DONE | KnownFile hashing open failures log stale or wrong error text on Win32 open failure |
| [BUG-026](../history/items/BUG-026.md) | Major | DONE | Search tab teardown frees live result/tab payload objects before the UI detaches them |
| [BUG-027](../history/items/BUG-027.md) | Major | DONE | IP filter update can delete the live `ipfilter.dat` before replacement promotion succeeds |
| [BUG-028](../history/items/BUG-028.md) | Minor | WONT_DO | MP3 ID3 metadata extraction is ANSI-only; non-ACP filenames can silently lose tags |
| [BUG-029](../history/items/BUG-029.md) | Major | DONE | Long-path tail hardening across config, media, shell, and GeoLocation surfaces |
| [BUG-030](../history/items/BUG-030.md) | Minor | DONE | Obfuscated server logins can advertise redundant callback crypto flags and require extra attempts |
| [BUG-031](items/BUG-031.md) | Minor | DEFERRED | Shared-file hashing fails too eagerly on transient sharing and lock violations |
| [BUG-032](../history/items/BUG-032.md) | Minor | DONE | AICH hashset save can fail spuriously after hashing because `known2.met` lock wait times out |
| [BUG-033](../history/items/BUG-033.md) | Minor | WONT_DO | WebSocket and MiniUPnP shutdown still use forced thread termination |
| [BUG-034](items/BUG-034.md) | Minor | IN_PROGRESS | Release paths silently swallow unexpected exceptions via catch (...) plus ASSERT(0) |
| [BUG-035](items/BUG-035.md) | Minor | IN_PROGRESS | Historical control-flow still uses bare ASSERT(0) without recovery or logging |
| [BUG-036](../history/items/BUG-036.md) | Major | DONE | `known.met` and `cancelled.met` still save in place and can truncate on failure |
| [BUG-037](../history/items/BUG-037.md) | Major | DONE | Same-hash KnownFile replacement can unshare or mis-track equivalent files |
| [BUG-038](../history/items/BUG-038.md) | Minor | DONE | Shared Files sort can retain stale rows after backing data changes |
| [BUG-039](../history/items/BUG-039.md) | Minor | DONE | Client list lacked a reusable safe pointer membership check |
| [BUG-040](../history/items/BUG-040.md) | Major | DONE | Downloading Clients list could dereference stale client rows |
| [BUG-041](../history/items/BUG-041.md) | Major | DONE | Known Clients list could dereference stale client rows |
| [BUG-042](../history/items/BUG-042.md) | Major | DONE | Upload list could dereference stale upload rows |
| [BUG-043](../history/items/BUG-043.md) | Major | DONE | Queue list could dereference stale queue rows |
| [BUG-044](../history/items/BUG-044.md) | Major | DONE | Download source rows could outlive their backing source objects |
| [BUG-045](../history/items/BUG-045.md) | Minor | DONE | Server list could dereference stale server rows |
| [BUG-046](../history/items/BUG-046.md) | Major | DONE | Kad contact list could dereference stale contact rows |
| [BUG-047](../history/items/BUG-047.md) | Major | DONE | Kad search list could dereference stale search rows |
| [BUG-048](../history/items/BUG-048.md) | Minor | DONE | IRC nick rows were not cleared before nick objects were deleted |
| [BUG-049](../history/items/BUG-049.md) | Minor | DONE | IRC channel tabs were not detached before channel objects were deleted |
| [BUG-050](../history/items/BUG-050.md) | Minor | DONE | Chat tabs were not detached before chat items were deleted |
| [BUG-051](../history/items/BUG-051.md) | Minor | DONE | IRC channel rows were not cleared before channel entries were deleted |
| [BUG-052](../history/items/BUG-052.md) | Minor | DONE | Kad search constructor accidentally added placeholder rows |
| [BUG-053](../history/items/BUG-053.md) | Major | DONE | part.met backup could be refreshed from the newly written metadata |
| [BUG-054](../history/items/BUG-054.md) | Major | DONE | ESC in shared-file delete confirmation could still delete files |
| [BUG-055](../history/items/BUG-055.md) | Major | DONE | AICH recovery accepted invalid part bounds |
| [BUG-056](../history/items/BUG-056.md) | Major | DONE | Download Clients list could dereference stale rows during display callbacks |
| [BUG-057](../history/items/BUG-057.md) | Minor | DONE | Close All Search Results could leave Kad keyword searches running |
| [BUG-058](../history/items/BUG-058.md) | Minor | DONE | Tree option value labels could contain the parser separator |
| [BUG-059](../history/items/BUG-059.md) | Trivial | DONE | Download Remaining column alignment was inconsistent |
| [BUG-060](../history/items/BUG-060.md) | Major | DONE | REST API should stay available when web templates are absent |
| [BUG-061](../history/items/BUG-061.md) | Major | DONE | Legacy web interface template was missing from the shipped tree |
| [BUG-062](../history/items/BUG-062.md) | Minor | DONE | Obfuscated server timeout did not retry plain connection promptly |
| [BUG-063](../history/items/BUG-063.md) | Major | DONE | ESC in shared-directory delete confirmation could still delete directories |
| [BUG-064](../history/items/BUG-064.md) | Minor | DONE | Client list secondary display path needed stale-row guarding |
| [BUG-065](../history/items/BUG-065.md) | Minor | DONE | Queue list secondary display path needed stale-row guarding |
| [BUG-066](../history/items/BUG-066.md) | Minor | DONE | Upload list secondary display path needed stale-row guarding |
| [BUG-067](../history/items/BUG-067.md) | Minor | DONE | REST log route lacked the expected get alias seam |
| [BUG-068](../history/items/BUG-068.md) | Minor | DONE | Download progress-bar drawing can leak GDI state into neighboring list cells |
| [BUG-069](../history/items/BUG-069.md) | Major | DONE | WebServer static resource requests can escape the web root and allocate whole files |
| [BUG-070](../history/items/BUG-070.md) | Minor | DONE | Ignored helper-thread launch failures can hang shutdown waits |
| [BUG-071](../history/items/BUG-071.md) | Major | DONE | server.met persistence still uses destructive backup and promotion moves |
| [BUG-072](../history/items/BUG-072.md) | Minor | DONE | Kad preferences and routing snapshots still save in place |
| [BUG-073](../history/items/BUG-073.md) | Major | DONE | WebServer session and bad-login state is mutated from request threads without synchronization |
| [BUG-074](../history/items/BUG-074.md) | Minor | WONT_DO | Archive preview scanner uses volatile cancellation and synchronous UI handoff *(deprecated/frozen)* |
| [BUG-075](../history/items/BUG-075.md) | Major | PASSED | REST and WebServer typed error consistency |
| [BUG-076](../history/items/BUG-076.md) | Major | PASSED | WebServer malformed request hardening for REST and legacy HTML |
| [BUG-077](../history/items/BUG-077.md) | Minor | PASSED | WebServer concurrent REST and legacy HTML soak coverage |
| [BUG-078](../history/items/BUG-078.md) | Critical | DONE | qBit compatibility auth can fail open when session RNG is unavailable |
| [BUG-079](../history/items/BUG-079.md) | Critical | DONE | WebSocket shutdown can close the termination event while accepted clients still wait on it |
| [BUG-080](../history/items/BUG-080.md) | Major | DONE | WebSocket shutdown can forcibly terminate the listener thread |
| [BUG-081](../history/items/BUG-081.md) | Major | DONE | HTTPS WebSocket handshake and read loops can spin on WANT_READ/WANT_WRITE |
| [BUG-082](../history/items/BUG-082.md) | Major | DONE | GeoLocation and IPFilter background refresh flags can race and remain stuck |
| [BUG-083](../history/items/BUG-083.md) | Major | DONE | Client UDP malformed-packet logging can read past a one-byte packet |
| [BUG-084](../history/items/BUG-084.md) | Minor | DONE | Web admin high-level actions leak the process token handle |
| [BUG-085](../history/items/BUG-085.md) | Major | DONE | Kad/client UDP encryption preference gating needs beta compatibility proof |
| [BUG-086](../history/items/BUG-086.md) | Critical | DONE | HTTPS WebSocket casts SOCKET storage to mbedtls_net_context |
| [BUG-087](../history/items/BUG-087.md) | Critical | DONE | HTTPS WebSocket queued writes can stall after TLS WANT_READ |
| [BUG-088](../history/items/BUG-088.md) | Major | DONE | WebSocket timeout shutdown leaves global state unsafe for restart |
| [BUG-089](../history/items/BUG-089.md) | Major | DONE | UDP control sender can deadlock on exception while holding sendLocker |
| [BUG-090](../history/items/BUG-090.md) | Major | DONE | Background refresh completion can wedge when UI PostMessage fails |
| [BUG-091](../history/items/BUG-091.md) | Major | DONE | DirectDownload ignores close-time write failures |
| [BUG-092](../history/items/BUG-092.md) | Critical | DONE | Background refresh workers can write through freed owner memory after shutdown |
| [BUG-093](../history/items/BUG-093.md) | Critical | DONE | Failed refresh completion can synchronously block worker on UI thread |
| [BUG-094](../history/items/BUG-094.md) | Major | DONE | ResumeThread failure leaks suspended refresh thread objects |
| [BUG-095](../history/items/BUG-095.md) | Major | DONE | WebSocket accepted-client tracking is not exception-safe after thread start |
| [BUG-096](../history/items/BUG-096.md) | Major | DONE | DirectDownload lacks bounded timeout and cancellation contract |
| [BUG-097](../history/items/BUG-097.md) | Critical | DONE | Startup-cache save worker can outlive shared-file list owner |
| [BUG-098](../history/items/BUG-098.md) | Minor | WONT_DO | Archive recovery worker uses raw part-file owner across async work *(deprecated/frozen)* |
| [BUG-099](../history/items/BUG-099.md) | Major | DONE | WebSocket listener startup is not exception-safe after global state initialization |
| [BUG-100](../history/items/BUG-100.md) | Major | DONE | DirectDownload has bounded timeouts but no hard owner cancellation contract |
| [BUG-101](../history/items/BUG-101.md) | Major | DONE | Shared Files 50k recursive tree stress profile does not reach main window |
| [BUG-102](../history/items/BUG-102.md) | Major | DONE | aMuTorrent browser smoke ignores generated harness port |
| [BUG-111](../history/items/BUG-111.md) | Critical | DONE | Release and help URLs still point outside the emulebb namespace |
| [BUG-112](../history/items/BUG-112.md) | Critical | WONT_DO | WebServer/qBit session tokens need CSPRNG-backed generation |
| [BUG-114](items/BUG-114.md) | Minor | IN_PROGRESS | Prevent Standby can leave Windows sleep prevention asserted after disable |
| [BUG-115](../history/items/BUG-115.md) | Minor | DONE | Tray left-click skips MiniMule and restores maximized windows as normal |
| [BUG-117](items/BUG-117.md) | Minor | DEFERRED | Audit Year-2038-sensitive persisted and runtime timestamps |
| [BUG-118](items/BUG-118.md) | Minor | OPEN | CTag UInt64 values can serialize without guaranteed 64-bit promotion |
| [BUG-119](items/BUG-119.md) | Minor | OPEN | Audit part-file gap and progress arithmetic against eMuleAI hardening |
| [BUG-120](items/BUG-120.md) | Minor | OPEN | Audit obfuscated server retry behavior against eMuleAI repeat-login fix |
| [BUG-121](../history/items/BUG-121.md) | Major | DONE | CorruptionBlackBox split reallocation can invalidate active CArray records |
| [BUG-122](../history/items/BUG-122.md) | Minor | DONE | CRing raw-owned buffer was accidentally copyable |
| [BUG-123](../history/items/BUG-123.md) | Major | DONE | Failed reask source delete needed explicit download-owner detachment |

`BUG-103` through `BUG-110` were superseded internal post-tag evidence labels,
not active item docs.

---

## Refactors

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [REF-001](../history/items/REF-001.md) | Major | WONT_DO | Keep the existing CZIPFile implementation |
| [REF-002](../history/items/REF-002.md) | Major | DONE | Remove Source Exchange v1 branches |
| [REF-003](items/REF-003.md) | Trivial | DEFERRED | Rename stale IRC string resources left over from IRC module removal |
| [REF-004](../history/items/REF-004.md) | Minor | DONE | Audit and disposition 17 load-only preference keys |
| [REF-005](../history/items/REF-005.md) | Trivial | DONE | Remove dead DebugSourceExchange commented-out calls |
| [REF-006](../history/items/REF-006.md) | Trivial | DONE | GetCategory should be const in DownloadListCtrl |
| [REF-007](../history/items/REF-007.md) | Trivial | DONE | WebM vs MKV disambiguation in MIME detection |
| [REF-015](../history/items/REF-015.md) | Minor | WONT_DO | Keep miniupnpc as the active UPnP backend |
| [REF-016](../history/items/REF-016.md) | Trivial | WONT_DO | Keep ResizableLib out-of-tree instead of inlining it |
| [REF-017](../history/items/REF-017.md) | Minor | DONE | Revalidate and close the dead-code sweep backlog item |
| [REF-018](../history/items/REF-018.md) | Minor | DONE | Remove defunct PeerCache surface and legacy INI fallback reads |
| [REF-019](../history/items/REF-019.md) | Minor | DONE | Replace ASSERT(0) + "must be a bug" with OnError() in EncryptedStreamSocket |
| [REF-020](../history/items/REF-020.md) | Minor | DONE | Replace dynamic loading of always-present Win10 APIs with static linking |
| [REF-021](items/REF-021.md) | Minor | DEFERRED | Remove blanket warning suppressions and replace deprecated Winsock APIs |
| [REF-022](items/REF-022.md) | Trivial | OPEN | Replace custom type aliases in types.h with <cstdint> standard types |
| [REF-023](../history/items/REF-023.md) | Minor | DONE | Replace unsafe sprintf/_stprintf/wsprintf with safe equivalents |
| [REF-024](items/REF-024.md) | Trivial | OPEN | Convert #define constants in Opcodes.h to constexpr in namespace |
| [REF-025](items/REF-025.md) | Minor | IN_PROGRESS | Remove legacy feature set — IRC, SMTP, Scheduler, first-start wizard, splash screen, update checker |
| [REF-026](../history/items/REF-026.md) | Minor | DONE | Manifest — keep Win10/11+ compatibility GUID only and move Common Controls into manifests |
| [REF-027](items/REF-027.md) | Minor | OPEN | CaptchaGenerator — replace CxImage with ATL CImage / native GDI |
| [REF-028](items/REF-028.md) | Minor | DEFERRED | Audit current MbedTLS 4.1 integration |
| [REF-029](items/REF-029.md) | Major | OPEN | Move async socket readiness to WSAPoll backends |
| [REF-030](../history/items/REF-030.md) | Minor | DONE | Replace window-message async hostname resolver with worker-thread model |
| [REF-031](../history/items/REF-031.md) | Minor | DONE | Review upload queue scoring against community and stale baselines |
| [REF-032](items/REF-032.md) | Minor | IN_PROGRESS | Use MFC-native property sheets and dynamic layout instead of CTreePropSheet / ResizableLib |
| [REF-033](items/REF-033.md) | Trivial | OPEN | Remove remaining IE/MSHTML drag-drop, HTML Help, and legacy IE web-client baggage |
| [REF-034](items/REF-034.md) | Minor | DEFERRED | Resolve Crypto++ 8.4 vs 8.9 dependency truth |
| [REF-035](items/REF-035.md) | Minor | OPEN | Adopt WIL for narrow Windows and COM RAII cleanup |
| [REF-036](items/REF-036.md) | Minor | OPEN | Adopt GSL contracts for buffer and pointer boundary hardening |
| [REF-037](../history/items/REF-037.md) | Major | DONE | Beta 0.7.3 legacy and frozen feature disposition ledger |
| [REF-038](../history/items/REF-038.md) | Minor | DONE | Harden optional MediaInfo DLL loading and metadata extraction seams |
| [REF-039](../history/items/REF-039.md) | Minor | DONE | Classify MediaInfo loader failures and bound metadata extraction counts |
| [REF-040](../history/items/REF-040.md) | Minor | DONE | Harden external UnRAR DLL loading |
| [REF-041](../history/items/REF-041.md) | Minor | DONE | Move remaining active app DLL probes to LoadLibraryEx |
| [REF-042](items/REF-042.md) | Minor | OPEN | Consolidate WinInet download helpers and review URL shortcut intake |
| [REF-043](items/REF-043.md) | Minor | OPEN | Drop the legacy HTML Web Interface and keep REST as the supported controller surface |
| [REF-044](items/REF-044.md) | Minor | OPEN | Remove remaining import-parts residue and keep legacy import flows retired |
| [REF-045](items/REF-045.md) | Minor | OPEN | Evaluate SQLite-backed storage for local metadata structures |
| [REF-046](items/REF-046.md) | Minor | OPEN | Evaluate JSON or TOML for operator-editable configuration |

---

## Abandoned Boost/POCO Ideas (historical only)

> These items were closed from the abandoned
> [IDEA-BOOST](../history/ideas/IDEA-BOOST.md) exploration by operator
> decision on 2026-05-21. They remain listed here as historical context only;
> do not promote this lane without a new approved active item.

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [REF-008](../history/items/REF-008.md) | Major | WONT_DO | Replace CAsyncSocketEx custom WinSock wrapper — Boost.Asio or Windows IOCP |
| [REF-009](../history/items/REF-009.md) | Major | WONT_DO | Replace CCriticalSection + CWinThread + Win32 events — std::mutex/thread or Boost |
| [REF-010](../history/items/REF-010.md) | Major | WONT_DO | Replace raw owned pointers with std::unique_ptr / std::shared_ptr |
| [REF-011](../history/items/REF-011.md) | Minor | WONT_DO | Replace GetTickCount / SetTimer with type-safe monotonic clock — std::chrono or Boost |
| [REF-012](../history/items/REF-012.md) | Minor | WONT_DO | Replace CFile + CString path concatenation — std::filesystem or boost::filesystem |
| [REF-013](../history/items/REF-013.md) | Minor | WONT_DO | Replace CString + unsafe sprintf with safe string formatting — std or Boost |
| [REF-014](../history/items/REF-014.md) | Minor | WONT_DO | Replace custom CRing<T> circular buffer — fix in place, std::deque, or boost::circular_buffer |

---

## Features

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [FEAT-001](items/FEAT-001.md) | Minor | DEFERRED | Kad FastKad — add diversity-aware bootstrap ranking and aggressive stale decay |
| [FEAT-002](items/FEAT-002.md) | Major | OPEN | Kad SafeKad — evolve from coarse same-IP gate into layered trust model (CGNAT fix) |
| [FEAT-003](items/FEAT-003.md) | Minor | OPEN | Kad — Add response usefulness scoring and subnet-diversity search fanout |
| [FEAT-004](items/FEAT-004.md) | Minor | OPEN | Kad — Generalise KadPublishGuard abuse budget beyond PUBLISH_SOURCE |
| [FEAT-005](items/FEAT-005.md) | Minor | OPEN | Kad — Restore network-change grace handling around routing persistence and probing |
| [FEAT-006](items/FEAT-006.md) | Minor | OPEN | Kad — Add explicit trust, budget, and bootstrap observability counters |
| [FEAT-007](items/FEAT-007.md) | Minor | OPEN | Windows Property Store integration for non-media file metadata |
| [FEAT-008](items/FEAT-008.md) | Trivial | OPEN | Oracle protocol guard seams — integrate stale branch test scaffolding |
| [FEAT-009](items/FEAT-009.md) | Trivial | OPEN | Mirror audit guard seam — WIP work from stale branch parent commit |
| [FEAT-010](../history/items/FEAT-010.md) | Minor | DONE | Long path support phase 2 — shell/UI, shared-directory recursion, exact-name paths, and path-helper audit |
| [FEAT-011](items/FEAT-011.md) | Minor | OPEN | CShield — integrate ED2K anti-leecher engine (44 bad-client categories) |
| [FEAT-012](../history/items/FEAT-012.md) | Minor | DONE | PR_TCPERRORFLOODER — TCP listen-socket flood defense |
| [FEAT-013](../history/items/FEAT-013.md) | Major | DONE | REST API — add authenticated in-process JSON endpoints to WebServer |
| [FEAT-014](items/FEAT-014.md) | Minor | OPEN | REST API follow-up — OpenAPI docs and optional external gateway |
| [FEAT-015](../history/items/FEAT-015.md) | Major | DONE | Broadband upload slot controller — budget-based cap + slow-slot reclamation |
| [FEAT-016](../history/items/FEAT-016.md) | Major | DONE | Modern limits — update stale hard-coded defaults for broadband/modern hardware |
| [FEAT-017](items/FEAT-017.md) | Major | OPEN | DPI awareness — Per-Monitor V2 manifest + hardcoded pixel audit |
| [FEAT-018](items/FEAT-018.md) | Minor | OPEN | µTP (Micro Transport Protocol) transport layer — CUtpSocket / libutp |
| [FEAT-019](items/FEAT-019.md) | Minor | OPEN | Dark mode UI — system-aware Windows 10 dark theme integration |
| [FEAT-020](../history/items/FEAT-020.md) | Trivial | DONE | DB-IP city geolocation — location label and flag per peer |
| [FEAT-021](items/FEAT-021.md) | Minor | OPEN | SourceSaver — persist download source lists between sessions |
| [FEAT-022](../history/items/FEAT-022.md) | Minor | DONE | Startup config directory override — `-c` flag for alternate preferences path |
| [FEAT-023](../history/items/FEAT-023.md) | Minor | DONE | Broadband queue scoring and ratio/cooldown UI extras |
| [FEAT-024](../history/items/FEAT-024.md) | Minor | DONE | Share-ignore policy with additive `shareignore.dat` |
| [FEAT-025](../history/items/FEAT-025.md) | Minor | DONE | Normalize download filenames on intake and completion |
| [FEAT-026](../history/items/FEAT-026.md) | Minor | DONE | Shared startup cache with known.met lookup index and `sharedcache.dat` |
| [FEAT-027](../history/items/FEAT-027.md) | Minor | DONE | Startup sequencing fix, startup profiling, and shared-view startup churn cleanup |
| [FEAT-028](../history/items/FEAT-028.md) | Minor | DONE | Virtualize and harden shared files list |
| [FEAT-029](../history/items/FEAT-029.md) | Minor | DONE | Search result ceilings — configurable ed2k expansion plus moderate Kad totals/lifetimes |
| [FEAT-030](../history/items/FEAT-030.md) | Minor | DONE | Bind policy completion — global `BindAddr` everywhere else, separate `WebBindAddr` for WebServer |
| [FEAT-031](items/FEAT-031.md) | Minor | OPEN | Auto-browse peers that expose remote shared-file inventories |
| [FEAT-032](items/FEAT-032.md) | Minor | DEFERRED | NAT mapping modernization — lease controls, status visibility, and PCP/NAT-PMP |
| [FEAT-033](../history/items/FEAT-033.md) | Minor | DONE | Disk-space floor hardening and legacy import-flow retirement |
| [FEAT-034](items/FEAT-034.md) | Minor | IN_PROGRESS | Shared-files reload should stop blocking the UI on large trees |
| [FEAT-035](items/FEAT-035.md) | Major | OPEN | IPv6 dual-stack compatibility for current eD2K/Kad networking |
| [FEAT-036](items/FEAT-036.md) | Major | OPEN | NAT traversal and extended source exchange for LowID-to-LowID connectivity |
| [FEAT-037](items/FEAT-037.md) | Minor | DEFERRED | Release-oriented sharing controls — PowerShare, Release Bonus, and Share Only The Need |
| [FEAT-038](../history/items/FEAT-038.md) | Minor | DONE | Shared-files watcher and live recursive share sync |
| [FEAT-039](items/FEAT-039.md) | Minor | OPEN | Download checker — duplicate and near-duplicate intake guard |
| [FEAT-040](items/FEAT-040.md) | Major | OPEN | Headless core with modern web/mobile controller and multi-user permissions |
| [FEAT-041](items/FEAT-041.md) | Minor | OPEN | Download Inspector automation for stale downloads and majority-name rename |
| [FEAT-042](../history/items/FEAT-042.md) | Minor | DONE | Automatic IP filter update scheduling |
| [FEAT-043](items/FEAT-043.md) | Minor | OPEN | Known Clients history and incremental list refresh performance |
| [FEAT-044](items/FEAT-044.md) | Minor | OPEN | IP filter input policy - PeerGuardian lists, whitelist, and private-IP exemption |
| [FEAT-045](../history/items/FEAT-045.md) | Major | PASSED | REST transfer detail endpoint for controller parity |
| [FEAT-046](../history/items/FEAT-046.md) | Major | PASSED | REST server and Kad bootstrap/import APIs |
| [FEAT-047](../history/items/FEAT-047.md) | Minor | PASSED | REST search API completeness pass |
| [FEAT-048](../history/items/FEAT-048.md) | Minor | PASSED | REST upload queue control completeness |
| [FEAT-049](../history/items/FEAT-049.md) | Minor | PASSED | Curated REST preference expansion |
| [FEAT-050](../history/items/FEAT-050.md) | Minor | PASSED | Launch external program on completed download |
| [FEAT-051](../history/items/FEAT-051.md) | Minor | DONE | Pro-user context menus and always-on advanced controls |
| [FEAT-052](../history/items/FEAT-052.md) | Minor | DONE | Main-shell keyboard shortcuts and mnemonic audit |
| [FEAT-053](../history/items/FEAT-053.md) | Minor | DONE | Classic tray balloon notification mode |
| [FEAT-054](../history/items/FEAT-054.md) | Minor | DONE | Normalize download message filename display |
| [FEAT-055](../history/items/FEAT-055.md) | Minor | DONE | Beta 0.7.3 improvement triage lane |
| [FEAT-056](items/FEAT-056.md) | Minor | DEFERRED | Post-0.7.3 release proof automation and operator evidence UX |
| [FEAT-058](../history/items/FEAT-058.md) | Minor | DONE | Beta 0.7.3 closeout UX polish and audit report |
| [FEAT-059](../history/items/FEAT-059.md) | Minor | DONE | Move tray icon visibility preference next to minimize-to-tray |
| [FEAT-060](../history/items/FEAT-060.md) | Minor | DONE | Preference inventory, mapping, clamp, and persistence audit |
| [FEAT-061](../history/items/FEAT-061.md) | Minor | DONE | Strong preference schema validation |
| [FEAT-062](../history/items/FEAT-062.md) | Minor | DONE | Category management dialog polish and robustness |
| [FEAT-063](../history/items/FEAT-063.md) | Minor | DONE | Web Interface preferences layout polish |
| [FEAT-064](items/FEAT-064.md) | Minor | OPEN | Curated post-0.7.3 future release roadmap |
| [FEAT-065](../history/items/FEAT-065.md) | Minor | DONE | Polish the native MiniMule tray popup |
| [FEAT-066](../history/items/FEAT-066.md) | Minor | DONE | Replace MiniMule chrome with table and speed chart |
| [FEAT-068](items/FEAT-068.md) | Minor | OPEN | Bound REST large-list memory and latency for very large profiles |
| [FEAT-069](items/FEAT-069.md) | Minor | OPEN | Shared-file include and exclude pattern rules |
| [FEAT-070](items/FEAT-070.md) | Minor | OPEN | Add targeted client UserHash and upload-lifecycle diagnostics |
| [FEAT-071](../history/items/FEAT-071.md) | Minor | DONE | Filename mojibake repair for search results and download intake |
| [FEAT-072](items/FEAT-072.md) | Minor | OPEN | Reduce startup cache UI-thread blocking on large shared libraries |
| [FEAT-073](items/FEAT-073.md) | Minor | OPEN | Incorporate p2p-overlord into the eMuleBB product family |
| [FEAT-074](../history/items/FEAT-074.md) | Minor | DONE | Add main-window visual evidence for connected LowID state |
| [FEAT-075](items/FEAT-075.md) | Minor | OPEN | Keep startup progress responsive during daily config backup |
| [FEAT-076](items/FEAT-076.md) | Minor | OPEN | Parallelize shared-file hashing across physical volumes and SSDs |
| [FEAT-077](items/FEAT-077.md) | Minor | OPEN | Auto-managed upload friend-slot candidates without mutating manual friends |
| [FEAT-078](items/FEAT-078.md) | Minor | OPEN | Persist auto-browse inventories in a local queryable database |
| [FEAT-079](items/FEAT-079.md) | Minor | OPEN | Save known and cancelled metadata from immutable background snapshots |
| [FEAT-080](items/FEAT-080.md) | Minor | OPEN | Refresh protected-volume disk-space snapshots in the background |
| [FEAT-081](items/FEAT-081.md) | Trivial | DEFERRED | Add a bounded source-hostname resolver pool only if profiling shows backlog |
| [FEAT-082](items/FEAT-082.md) | Minor | OPEN | Virtualize high-volume downloads, search results, and client-history lists |
| [FEAT-083](../history/items/FEAT-083.md) | Minor | WONT_DO | Connection Checker based on public reachability polling |
| [FEAT-084](../history/items/FEAT-084.md) | Minor | WONT_DO | Migration Wizard for legacy profile import |
| [FEAT-085](items/FEAT-085.md) | Minor | OPEN | Establish a shared campaign core for eMuleBB product-family test orchestration |
| [FEAT-086](items/FEAT-086.md) | Minor | OPEN | Parse eMuleAI extension hints without advertising protocol support |

---

## Build / CI / Tooling

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [CI-001](../history/items/CI-001.md) | Major | WONT_DO | CMake adoption exploration — replace emule.vcxproj with CMakeLists.txt + Ninja |
| [CI-002](items/CI-002.md) | Minor | OPEN | clang-format — enforce consistent code formatting |
| [CI-003](../history/items/CI-003.md) | Minor | DONE | MSVC compiler hardening — SDL, guard:cf, /WX (Phase A done: SDL+CFG in commit `5557216`) |
| [CI-004](items/CI-004.md) | Minor | OPEN | clang-tidy — integrate static analysis into build and CI |
| [CI-005](items/CI-005.md) | Minor | OPEN | cppcheck — integrate complementary bug-class analysis |
| [CI-006](items/CI-006.md) | Minor | OPEN | MSVC AddressSanitizer — enable for debug builds to catch memory errors |
| [CI-007](items/CI-007.md) | Minor | OPEN | Kad — Expand integration and fuzz test coverage beyond helper-unit tests |
| [CI-008](../history/items/CI-008.md) | Minor | DONE | Expand regression coverage for part files, long paths, and WebServer/REST |
| [CI-009](../history/items/CI-009.md) | Minor | DONE | Share-ignore regression coverage and Release test-build stabilization |
| [CI-010](items/CI-010.md) | Minor | IN_PROGRESS | Reduce remaining app-local warning debt after external noise cleanup |
| [CI-011](../history/items/CI-011.md) | Major | DONE | Broadband release live E2E coverage umbrella |
| [CI-012](../history/items/CI-012.md) | Major | DONE | Stabilize Shared Files dynamic folder lifecycle E2E |
| [CI-013](../history/items/CI-013.md) | Major | DONE | Download and search UI live scenarios |
| [CI-014](../history/items/CI-014.md) | Major | PASSED | REST contract manifest and live completeness gate |
| [CI-015](../history/items/CI-015.md) | Major | PASSED | REST malformed and concurrent request matrix |
| [CI-016](../history/items/CI-016.md) | Minor | PASSED | REST-only main vs community regression lane |
| [CI-017](../history/items/CI-017.md) | Minor | DONE | Normalize active workspace line-ending policy to LF by default |
| [CI-018](../history/items/CI-018.md) | Major | DONE | Shared Files 50k-file tree refresh stress gate |
| [CI-019](../history/items/CI-019.md) | Major | DONE | HTTPS and REST socket adversity stress gate |
| [CI-020](../history/items/CI-020.md) | Major | DONE | REST and legacy WebServer error-path coverage gate |
| [CI-021](../history/items/CI-021.md) | Major | DONE | WebSocket and legacy socket leak-churn gate |
| [CI-022](../history/items/CI-022.md) | Major | DONE | Beta 0.7.3 community parity changed-surface ledger |
| [CI-023](../history/items/CI-023.md) | Major | DONE | Beta 0.7.3 post-1.0 hardening regression replay gate |
| [CI-024](../history/items/CI-024.md) | Major | DONE | Beta 0.7.3 controller integration full replay gate |
| [CI-025](../history/items/CI-025.md) | Major | DONE | Beta 0.7.3 REST and adapter contract drift gate |
| [CI-026](../history/items/CI-026.md) | Major | DONE | Beta 0.7.3 shared files, startup cache, and long-path parity gate |
| [CI-027](../history/items/CI-027.md) | Major | DONE | Beta 0.7.3 download and persistence replay gate |
| [CI-028](../history/items/CI-028.md) | Major | DONE | Beta 0.7.3 search, server, and Kad parity replay gate |
| [CI-029](../history/items/CI-029.md) | Major | DONE | Beta 0.7.3 network socket, UDP, WebSocket, HTTPS, and UPnP adversity gate |
| [CI-030](../history/items/CI-030.md) | Major | DONE | Beta 0.7.3 UI, preferences, tray, and language resource parity smoke gate |
| [CI-031](../history/items/CI-031.md) | Major | DONE | Beta 0.7.3 packaging, architecture, and release asset parity gate |
| [CI-032](../history/items/CI-032.md) | Major | DONE | Beta 0.7.3 post-tag focused coverage gaps |
| [CI-033](../history/items/CI-033.md) | Major | DONE | Beta 0.7.3 internal pre-release proof |
| [CI-034](../history/items/CI-034.md) | Major | DONE | Package-release provenance and dirty-input guard |
| [CI-035](items/CI-035.md) | Major | OPEN | Final current-head RC proof and fresh package hashes |
| [CI-036](../history/items/CI-036.md) | Major | DONE | Release certification test matrix |
| [CI-037](../history/items/CI-037.md) | Major | PASSED | Expanded live UI and E2E weak-path stress gate |
| [CI-038](../history/items/CI-038.md) | Major | DONE | UI resource-depth and language smoke gate |
| [CI-039](../history/items/CI-039.md) | Minor | DONE | Consolidate Markdown backlog process and validation |
| [CI-040](../history/items/CI-040.md) | Minor | DONE | Standardize current Markdown naming and structure checks |
| [CI-041](../history/items/CI-041.md) | Minor | DONE | Publish Markdown documentation with MkDocs Material |
| [CI-042](../history/items/CI-042.md) | Minor | DONE | Keep only the latest nightly GitHub prerelease per build stream |
| [CI-043](../history/items/CI-043.md) | Minor | DONE | Add aMuTorrent automatic upstream nightly sync and release workflow |

---

## Controller Integrations

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [AMUT-001](../history/items/AMUT-001.md) | Major | PASSED | aMuTorrent eMuleBB browser smoke coverage |
| [AMUT-002](../history/items/AMUT-002.md) | Major | PASSED | aMuTorrent transfer detail hydration |
| [ARR-001](../history/items/ARR-001.md) | Major | PASSED | Full Arr release E2E validation |

---

## Release Focus

RC 0.7.3 hardening is controlled by [RELEASE-0.7.3](RELEASE-0.7.3.md).
Use that page for release status, source decision, and the open RC task table.
The current implementation sequence lives in the single
[RC 0.7.3 execution plan](plans/RELEASE-0.7.3-EXECUTION-PLAN.md).
Superseded release gate evidence and old cluster plans live under
`docs\history\release-0.7.3`.

## Reference Material

- [Backlog history](../history/BACKLOG-HISTORY.md)
- [Backlog dependency graph](../history/BACKLOG-DEPENDENCY-GRAPH.md)
- [Backlog source salvage](../history/BACKLOG-SOURCE-SALVAGE.md)

Current issue status is tracked here. Other `docs/` areas contain reference,
history, architecture notes, audits, ideas, and active execution plans according
to [DOCS-POLICY](../DOCS-POLICY.md).
