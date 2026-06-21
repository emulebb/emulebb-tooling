# Closed Item Index

Browsable index of closed backlog records under `docs/history/items/`.

!!! note "Provenance only"
    These are closed records (`DONE`, `PASSED`, `WONT_DO`); item IDs are
    never reused. Current work lives in [`docs/active/`](../../active/INDEX.md).
    Back to the [History Archive](../INDEX.md).

Total: 253 closed items.

## BUG — defects (132)

| ID | Title | Status |
| --- | --- | --- |
| [BUG-001](BUG-001.md) | 17 load-only hidden prefs not written back to preferences.ini | Done |
| [BUG-002](BUG-002.md) | ASSERT(0) FIXME in ArchiveRecovery.cpp — unhandled format case falls through silently in release | Wont-Fix |
| [BUG-003](BUG-003.md) | Historical large-file FIXME markers overstated the remaining live issue | Done |
| [BUG-004](BUG-004.md) | IPFilter overlapping IP ranges not handled — acknowledged correctness gap | Done |
| [BUG-005](BUG-005.md) | Kad buddy connections broken when RequireCrypt is enabled | Wont-Fix |
| [BUG-006](BUG-006.md) | Weak RNG for crypto challenge value — rand() seeded with time(NULL) | Wont-Fix |
| [BUG-007](BUG-007.md) | Ring.h — CRing<T> pointer-state, access-guard, and defensive copy cleanup (CODEREV_003, 004, 011) | Done |
| [BUG-008](BUG-008.md) | CaptchaGenerator — rand() & 8 produces bimodal jitter (only 0 or 8, never 1-7) | Wont-Fix |
| [BUG-009](BUG-009.md) | PartFile — non-atomic part.met replacement (_tremove + _trename crash window) | Done |
| [BUG-010](BUG-010.md) | PartFile — part.met written on low disk space, risking truncation/corruption | Done |
| [BUG-011](BUG-011.md) | Race condition — shareddir_list iterated without lock in SendSharedDirectories | Done |
| [BUG-012](BUG-012.md) | CPartFile destructor calls FlushBuffer after write thread has already exited | DONE |
| [BUG-013](BUG-013.md) | ArchiveRecovery.cpp — three unchecked malloc() calls crash on OOM | Wont-Fix |
| [BUG-014](BUG-014.md) | ZIPFile.cpp — WriteFile return value silently discarded on two paths | Done |
| [BUG-015](BUG-015.md) | GetTickCount() 49-day overflow in ban expiry and download timeout checks | Done |
| [BUG-016](BUG-016.md) | UDP obfuscation applied when crypt layer is disabled — IsCryptLayerEnabled() guard missing | Done |
| [BUG-017](BUG-017.md) | UDP throttler deadlock — sendLocker held when signaling QueueForSendingControlPacket | Done |
| [BUG-018](BUG-018.md) | Part-file hash layout drift — hash tree can mutate during concurrent hashing | Done |
| [BUG-019](BUG-019.md) | AICH sync thread concurrency — multiple unsynchronized shared-state accesses | Done |
| [BUG-020](BUG-020.md) | Client socket teardown ordering — cross-link not cleared before Safe_Delete | Done |
| [BUG-021](BUG-021.md) | Upload queue lock inversion + socket I/O result mishandling + inflate buffer aliasing | Done |
| [BUG-022](BUG-022.md) | Long-path delete-to-recycle-bin still breaks in ShellDeleteFile | Done |
| [BUG-023](BUG-023.md) | Shared-file ED2K published column shows a false `No` after publish-state reset | Done |
| [BUG-024](BUG-024.md) | statUTC(HANDLE) returns corrupted `st_size` by combining file size high with file index low | Done |
| [BUG-025](BUG-025.md) | KnownFile hashing open failures log stale or wrong error text on Win32 open failure | Done |
| [BUG-026](BUG-026.md) | Search tab teardown frees live result and tab-parameter objects before the UI detaches them | Done |
| [BUG-027](BUG-027.md) | IP filter update can delete the live `ipfilter.dat` before replacement promotion succeeds | Done |
| [BUG-028](BUG-028.md) | MP3 ID3 metadata extraction is ANSI-only; non-ACP filenames can silently lose tags | Wont-Fix |
| [BUG-029](BUG-029.md) | Long-path tail hardening across config, media, shell, and GeoLocation surfaces | Done |
| [BUG-030](BUG-030.md) | Obfuscated server logins can advertise redundant callback crypto flags and require extra attempts | Done |
| [BUG-031](BUG-031.md) | Shared-file hashing fails too eagerly on transient sharing and lock violations | DONE |
| [BUG-032](BUG-032.md) | AICH hashset save can fail spuriously after hashing because `known2.met` lock wait times out | Done |
| [BUG-033](BUG-033.md) | WebSocket and MiniUPnP shutdown still use forced thread termination | Wont-Fix |
| [BUG-036](BUG-036.md) | known.met and cancelled.met still save in place and can truncate on failure | Done |
| [BUG-037](BUG-037.md) | Same-hash KnownFile replacement can unshare or mis-track equivalent files | Done |
| [BUG-038](BUG-038.md) | Shared Files sort can retain stale rows after backing data changes | Done |
| [BUG-039](BUG-039.md) | Client list lacked a reusable safe pointer membership check | Done |
| [BUG-040](BUG-040.md) | Downloading Clients list could dereference stale client rows | Done |
| [BUG-041](BUG-041.md) | Known Clients list could dereference stale client rows | Done |
| [BUG-042](BUG-042.md) | Upload list could dereference stale upload rows | Done |
| [BUG-043](BUG-043.md) | Queue list could dereference stale queue rows | Done |
| [BUG-044](BUG-044.md) | Download source rows could outlive their backing source objects | Done |
| [BUG-045](BUG-045.md) | Server list could dereference stale server rows | Done |
| [BUG-046](BUG-046.md) | Kad contact list could dereference stale contact rows | Done |
| [BUG-047](BUG-047.md) | Kad search list could dereference stale search rows | Done |
| [BUG-048](BUG-048.md) | IRC nick rows were not cleared before nick objects were deleted | Done |
| [BUG-049](BUG-049.md) | IRC channel tabs were not detached before channel objects were deleted | Done |
| [BUG-050](BUG-050.md) | Chat tabs were not detached before chat items were deleted | Done |
| [BUG-051](BUG-051.md) | IRC channel rows were not cleared before channel entries were deleted | Done |
| [BUG-052](BUG-052.md) | Kad search constructor accidentally added placeholder rows | Done |
| [BUG-053](BUG-053.md) | part.met backup could be refreshed from the newly written metadata | Done |
| [BUG-054](BUG-054.md) | ESC in shared-file delete confirmation could still delete files | Done |
| [BUG-055](BUG-055.md) | AICH recovery accepted invalid part bounds | Done |
| [BUG-056](BUG-056.md) | Download Clients list could dereference stale rows during display callbacks | Done |
| [BUG-057](BUG-057.md) | Close All Search Results could leave Kad keyword searches running | Done |
| [BUG-058](BUG-058.md) | Tree option value labels could contain the parser separator | Done |
| [BUG-059](BUG-059.md) | Download Remaining column alignment was inconsistent | Done |
| [BUG-060](BUG-060.md) | REST API should stay available when web templates are absent | Done |
| [BUG-061](BUG-061.md) | Legacy web interface template was missing from the shipped tree | Done |
| [BUG-062](BUG-062.md) | Obfuscated server timeout did not retry plain connection promptly | Done |
| [BUG-063](BUG-063.md) | ESC in shared-directory delete confirmation could still delete directories | Done |
| [BUG-064](BUG-064.md) | Client list secondary display path needed stale-row guarding | Done |
| [BUG-065](BUG-065.md) | Queue list secondary display path needed stale-row guarding | Done |
| [BUG-066](BUG-066.md) | Upload list secondary display path needed stale-row guarding | Done |
| [BUG-067](BUG-067.md) | REST log route lacked the expected get alias seam | Done |
| [BUG-068](BUG-068.md) | Download progress-bar drawing can leak GDI state into neighboring list cells | Done |
| [BUG-069](BUG-069.md) | WebServer static resource requests can escape the web root and allocate whole files | Done |
| [BUG-070](BUG-070.md) | Ignored helper-thread launch failures can hang shutdown waits | Done |
| [BUG-071](BUG-071.md) | server.met persistence still uses destructive backup and promotion moves | Done |
| [BUG-072](BUG-072.md) | Kad preferences and routing snapshots still save in place | Done |
| [BUG-073](BUG-073.md) | WebServer session and bad-login state is mutated from request threads without synchronization | Done |
| [BUG-074](BUG-074.md) | Archive preview scanner uses volatile cancellation and synchronous UI handoff | Wont-Fix |
| [BUG-075](BUG-075.md) | REST and WebServer typed error consistency | Passed |
| [BUG-076](BUG-076.md) | WebServer malformed request hardening for REST and legacy HTML | Passed |
| [BUG-077](BUG-077.md) | WebServer concurrent REST and legacy HTML soak coverage | Passed |
| [BUG-078](BUG-078.md) | qBit compatibility auth can fail open when session RNG is unavailable | Done |
| [BUG-079](BUG-079.md) | WebSocket shutdown can close the termination event while accepted clients still wait on it | Done |
| [BUG-080](BUG-080.md) | WebSocket shutdown can forcibly terminate the listener thread | Done |
| [BUG-081](BUG-081.md) | HTTPS WebSocket handshake and read loops can spin on WANT_READ/WANT_WRITE | Done |
| [BUG-082](BUG-082.md) | GeoLocation and IPFilter background refresh flags can race and remain stuck | Done |
| [BUG-083](BUG-083.md) | Client UDP malformed-packet logging can read past a one-byte packet | Done |
| [BUG-084](BUG-084.md) | Web admin high-level actions leak the process token handle | Done |
| [BUG-085](BUG-085.md) | Kad/client UDP encryption preference gating needs Release 1 compatibility proof | Done |
| [BUG-086](BUG-086.md) | HTTPS WebSocket casts SOCKET storage to mbedtls_net_context | Done |
| [BUG-087](BUG-087.md) | HTTPS WebSocket queued writes can stall after TLS WANT_READ | Done |
| [BUG-088](BUG-088.md) | WebSocket timeout shutdown leaves global state unsafe for restart | Done |
| [BUG-089](BUG-089.md) | UDP control sender can deadlock on exception while holding sendLocker | Done |
| [BUG-090](BUG-090.md) | Background refresh completion can wedge when UI PostMessage fails | Done |
| [BUG-091](BUG-091.md) | DirectDownload ignores close-time write failures | Done |
| [BUG-092](BUG-092.md) | Background refresh workers can write through freed owner memory after shutdown | Done |
| [BUG-093](BUG-093.md) | Failed refresh completion can synchronously block worker on UI thread | Done |
| [BUG-094](BUG-094.md) | ResumeThread failure leaks suspended refresh thread objects | Done |
| [BUG-095](BUG-095.md) | WebSocket accepted-client tracking is not exception-safe after thread start | Done |
| [BUG-096](BUG-096.md) | DirectDownload lacks bounded timeout and cancellation contract | Done |
| [BUG-097](BUG-097.md) | Startup-cache save worker can outlive shared-file list owner | Done |
| [BUG-098](BUG-098.md) | Archive recovery worker uses raw part-file owner across async work | Wont-Fix |
| [BUG-099](BUG-099.md) | WebSocket listener startup is not exception-safe after global state initialization | Done |
| [BUG-100](BUG-100.md) | DirectDownload has bounded timeouts but no hard owner cancellation contract | Done |
| [BUG-101](BUG-101.md) | Shared Files 50k recursive tree stress profile does not reach main window | Done |
| [BUG-102](BUG-102.md) | aMuTorrent browser smoke ignores generated harness port | Done |
| [BUG-111](BUG-111.md) | Release and help URLs still point outside the emulebb namespace | Done |
| [BUG-112](BUG-112.md) | WebServer/qBit session tokens need CSPRNG-backed generation | Wont-Fix |
| [BUG-113](BUG-113.md) | Auto-category non-regex matching skips usable tokens | Done |
| [BUG-114](BUG-114.md) | Prevent Standby can leave Windows sleep prevention asserted after disable | DONE |
| [BUG-115](BUG-115.md) | Tray left-click skips MiniMule and restores maximized windows as normal | DONE |
| [BUG-116](BUG-116.md) | Search results can leave a floating horizontal scrollbar artifact | DONE |
| [BUG-118](BUG-118.md) | CTag UInt64 values can serialize without guaranteed 64-bit promotion | DONE |
| [BUG-119](BUG-119.md) | Audit part-file gap and progress arithmetic against eMuleAI hardening | DONE |
| [BUG-120](BUG-120.md) | Audit obfuscated server retry behavior against eMuleAI repeat-login fix | DONE |
| [BUG-121](BUG-121.md) | CorruptionBlackBox split reallocation can invalidate active CArray records | DONE |
| [BUG-122](BUG-122.md) | CRing raw-owned buffer was accidentally copyable | DONE |
| [BUG-123](BUG-123.md) | Failed reask source delete needed explicit download-owner detachment | DONE |
| [BUG-124](BUG-124.md) | Log panes can nearly freeze the UI under high-volume output | DONE |
| [BUG-125](BUG-125.md) | Harden client and queue lifetime edges found by focused review | DONE |
| [BUG-126](BUG-126.md) | Harden transfer queue async lifetime edges | DONE |
| [BUG-127](BUG-127.md) | Fix regressions from recent C++ hardening review | DONE |
| [BUG-128](BUG-128.md) | Bound REST compatibility hot-path serialization | DONE |
| [BUG-130](BUG-130.md) | Harden RC1 hot-path worker and metadata edges | DONE |
| [BUG-131](BUG-131.md) | Harden RC1 completion, delete, and startup-cache lifetime edges | DONE |
| [BUG-133](BUG-133.md) | Harden RC1 metadata bounds, REST polling, and worker shutdown edges | DONE |
| [BUG-134](BUG-134.md) | Harden final RC1 shutdown, REST bounds, and AICH repair edges | DONE |
| [BUG-135](BUG-135.md) | Harden final RC1 runtime stabilization edges | DONE |
| [BUG-136](BUG-136.md) | Harden final RC1 review follow-up hot paths | DONE |
| [BUG-137](BUG-137.md) | Harden final RC1 AICH, UPnP, listener, and Kad edges | DONE |
| [BUG-139](BUG-139.md) | Clean exit can leave the shell tray icon behind | DONE |
| [BUG-140](BUG-140.md) | Transfer UI updates can run on split presentation timers | DONE |
| [BUG-141](BUG-141.md) | Source expand icons and video thumbnails can be visually oversized | DONE |
| [BUG-144](BUG-144.md) | Remote shared-directory requests can freeze large shared profiles | DONE |
| [BUG-145](BUG-145.md) | Suite bootstrap flow misses LAN, credential, category, and Arr sync polish | DONE |
| [BUG-148](BUG-148.md) | Shared Files directory tree node stuck expanded after collapse and cannot re-expand | DONE |
| [BUG-149](BUG-149.md) | Shared directory tree rebuild is slow and UI-blocking on large shared sets | DONE |
| [BUG-150](BUG-150.md) | False multiple_names Caution on cosmetic search-name differences | DONE |

## FEAT — features (48)

| ID | Title | Status |
| --- | --- | --- |
| [FEAT-010](FEAT-010.md) | Long path support phase 2 — shell/UI, shared-directory recursion, exact-name paths, and path-helper audit | Done |
| [FEAT-012](FEAT-012.md) | PR_TCPERRORFLOODER — TCP listen-socket flood defense | Done |
| [FEAT-013](FEAT-013.md) | REST API — add authenticated in-process JSON endpoints to WebServer | Done |
| [FEAT-015](FEAT-015.md) | Broadband upload slot allocation — fixed cap + weak-slot reclamation | Done |
| [FEAT-016](FEAT-016.md) | Modern limits — update stale hard-coded defaults for broadband/modern hardware | Done |
| [FEAT-020](FEAT-020.md) | DB-IP city geolocation — location label and flag per peer | Done |
| [FEAT-022](FEAT-022.md) | Startup config directory override — `-c` flag for alternate preferences path | Done |
| [FEAT-023](FEAT-023.md) | Broadband queue scoring and ratio/cooldown UI extras | Done |
| [FEAT-024](FEAT-024.md) | Share-ignore policy with additive `shareignore.dat` | Done |
| [FEAT-025](FEAT-025.md) | Normalize download filenames on intake and completion | Done |
| [FEAT-026](FEAT-026.md) | Shared startup cache with known.met lookup index and `sharedcache.dat` | Done |
| [FEAT-027](FEAT-027.md) | Startup sequencing fix, startup profiling, and shared-view startup churn cleanup | Done |
| [FEAT-028](FEAT-028.md) | Virtualize and harden shared files list | Done |
| [FEAT-029](FEAT-029.md) | Search result ceilings — configurable ed2k expansion plus moderate Kad totals/lifetimes | Done |
| [FEAT-030](FEAT-030.md) | Bind policy completion — global `BindAddr` everywhere else, separate `WebBindAddr` for WebServer | Done |
| [FEAT-033](FEAT-033.md) | Disk-space floor hardening and legacy import-flow retirement | Done |
| [FEAT-038](FEAT-038.md) | Shared-files watcher and live recursive share sync | Done |
| [FEAT-042](FEAT-042.md) | Automatic IP filter update scheduling | Done |
| [FEAT-045](FEAT-045.md) | REST transfer detail endpoint for controller parity | Passed |
| [FEAT-046](FEAT-046.md) | REST server and Kad bootstrap/import APIs | Passed |
| [FEAT-047](FEAT-047.md) | REST search API completeness pass | Passed |
| [FEAT-048](FEAT-048.md) | REST upload queue control completeness | Passed |
| [FEAT-049](FEAT-049.md) | Curated REST preference expansion | Passed |
| [FEAT-050](FEAT-050.md) | Launch external program on completed download | Passed |
| [FEAT-051](FEAT-051.md) | Pro-user context menus and always-on advanced controls | Done |
| [FEAT-052](FEAT-052.md) | Main-shell keyboard shortcuts and mnemonic audit | Done |
| [FEAT-053](FEAT-053.md) | Classic tray balloon notification mode | Done |
| [FEAT-054](FEAT-054.md) | Normalize download message filename display | Done |
| [FEAT-055](FEAT-055.md) | Beta 0.7.3 improvement triage lane | Done |
| [FEAT-057](FEAT-057.md) | Add qBittorrent-style download shortcuts and batch menu actions | Done |
| [FEAT-058](FEAT-058.md) | Beta 0.7.3 closeout UX polish and audit report | Done |
| [FEAT-059](FEAT-059.md) | Move tray icon visibility preference next to minimize-to-tray | Done |
| [FEAT-060](FEAT-060.md) | Preference inventory, mapping, clamp, and persistence audit | Done |
| [FEAT-061](FEAT-061.md) | Strong preference schema validation | Done |
| [FEAT-062](FEAT-062.md) | Category management dialog polish and robustness | Done |
| [FEAT-063](FEAT-063.md) | Web Interface preferences layout polish | DONE |
| [FEAT-065](FEAT-065.md) | Polish the native MiniMule tray popup | DONE |
| [FEAT-066](FEAT-066.md) | Replace MiniMule chrome with table and speed chart | DONE |
| [FEAT-067](FEAT-067.md) | External VPN kill-switch watchdog | WONT_DO |
| [FEAT-071](FEAT-071.md) | Filename mojibake repair for search results and download intake | Done |
| [FEAT-074](FEAT-074.md) | Add main-window visual evidence for connected LowID state | DONE |
| [FEAT-083](FEAT-083.md) | Connection Checker based on public reachability polling | WONT_DO |
| [FEAT-084](FEAT-084.md) | Migration Wizard for legacy profile import | WONT_DO |
| [FEAT-097](FEAT-097.md) | Add connection pressure details to Network Information | DONE |
| [FEAT-118](FEAT-118.md) | Composite Confidence indicator replacing the Risk + Kad-Confidence columns | DONE |
| [FEAT-119](FEAT-119.md) | Quick hide already-known files filter in search results | DONE |
| [FEAT-120](FEAT-120.md) | Sortable Extension column in search results | DONE |
| [FEAT-123](FEAT-123.md) | Shared files one-level auto-updater | DONE |

## REF — refactors (30)

| ID | Title | Status |
| --- | --- | --- |
| [REF-001](REF-001.md) | Keep the existing CZIPFile implementation | Wont-Fix |
| [REF-002](REF-002.md) | Remove Source Exchange v1 branches — deprecated protocol superseded by v2 | Done |
| [REF-004](REF-004.md) | Audit and disposition 17 load-only hidden preference keys | Done |
| [REF-005](REF-005.md) | Remove or restore dead DebugSourceExchange log calls in DownloadQueue.cpp | Done |
| [REF-006](REF-006.md) | GetCategory const-correctness cleanup in DownloadListCtrl / CPartFile | Done |
| [REF-007](REF-007.md) | WebM vs MKV disambiguation in MIME magic-byte detection | Done |
| [REF-008](REF-008.md) | Replace CAsyncSocketEx custom WinSock wrapper — Boost.Asio or Windows IOCP | WONT_DO |
| [REF-009](REF-009.md) | Replace CCriticalSection + CWinThread + Win32 events — std::mutex/thread or Boost | WONT_DO |
| [REF-010](REF-010.md) | Replace raw owned pointers with std::unique_ptr / std::shared_ptr | WONT_DO |
| [REF-011](REF-011.md) | Replace GetTickCount / SetTimer with type-safe monotonic clock — std::chrono or Boost | WONT_DO |
| [REF-012](REF-012.md) | Replace CFile + CString path concatenation — std::filesystem or boost::filesystem | WONT_DO |
| [REF-013](REF-013.md) | Replace CString + unsafe sprintf with safe string formatting — std or Boost | WONT_DO |
| [REF-014](REF-014.md) | Replace custom CRing<T> circular buffer — fix in place, std::deque, or boost::circular_buffer | WONT_DO |
| [REF-015](REF-015.md) | Keep miniupnpc as the active UPnP backend | Wont-Fix |
| [REF-016](REF-016.md) | Keep ResizableLib out-of-tree instead of inlining it | Wont-Fix |
| [REF-017](REF-017.md) | Revalidate and close the dead-code sweep backlog item | Done |
| [REF-018](REF-018.md) | Remove defunct PeerCache surface and legacy INI fallback reads | Done |
| [REF-019](REF-019.md) | Replace ASSERT(0) + "must be a bug" with proper error handling in EncryptedStreamSocket | Done |
| [REF-020](REF-020.md) | Replace dynamic loading of always-present Win10 APIs with static linking | Done |
| [REF-023](REF-023.md) | Replace unsafe sprintf/_stprintf/wsprintf with safe equivalents | Done |
| [REF-026](REF-026.md) | Manifest — drop legacy OS entries, add Common Controls 6.0 dependency | Done |
| [REF-030](REF-030.md) | Replace window-message async hostname resolver with worker-thread model | DONE |
| [REF-031](REF-031.md) | Review upload queue scoring against community and stale baselines | Done |
| [REF-037](REF-037.md) | Beta 0.7.3 legacy and frozen feature disposition ledger | Done |
| [REF-038](REF-038.md) | Harden optional MediaInfo DLL loading and metadata extraction seams | Done |
| [REF-039](REF-039.md) | Classify MediaInfo loader failures and bound metadata extraction counts | Done |
| [REF-040](REF-040.md) | Harden external UnRAR DLL loading | Done |
| [REF-041](REF-041.md) | Move remaining active app DLL probes to LoadLibraryEx | Done |
| [REF-047](REF-047.md) | Finalize native REST v1 API standardization before RC1 | DONE |
| [REF-054](REF-054.md) | Stabilize and instrument download queue behavior | DONE |

## CI — build/packaging/gates (40)

| ID | Title | Status |
| --- | --- | --- |
| [CI-001](CI-001.md) | CMake adoption exploration — replace emule.vcxproj with CMakeLists.txt + Ninja | WONT_DO |
| [CI-003](CI-003.md) | MSVC compiler hardening — enable SDL, guard checks, and treat warnings as errors | Done |
| [CI-008](CI-008.md) | Expand regression coverage for part files, long paths, and WebServer/REST | Done |
| [CI-009](CI-009.md) | Share-ignore regression coverage and Release test-build stabilization | Done |
| [CI-011](CI-011.md) | Broadband release live E2E coverage umbrella | Done |
| [CI-012](CI-012.md) | Stabilize Shared Files dynamic folder lifecycle E2E | Done |
| [CI-013](CI-013.md) | Download and search UI live scenarios | Done |
| [CI-014](CI-014.md) | REST contract manifest and live completeness gate | Passed |
| [CI-015](CI-015.md) | REST malformed and concurrent request matrix | Passed |
| [CI-016](CI-016.md) | REST-only main vs community regression lane | Passed |
| [CI-017](CI-017.md) | Normalize active workspace line-ending policy to LF by default | Done |
| [CI-018](CI-018.md) | Shared Files 50k-file tree refresh stress gate | Done |
| [CI-019](CI-019.md) | HTTPS and REST socket adversity stress gate | Done |
| [CI-020](CI-020.md) | REST and legacy WebServer error-path coverage gate | Done |
| [CI-021](CI-021.md) | WebSocket and legacy socket leak-churn gate | Done |
| [CI-022](CI-022.md) | Beta 0.7.3 community parity changed-surface ledger | Done |
| [CI-023](CI-023.md) | Beta 0.7.3 post-1.0 hardening regression replay gate | Done |
| [CI-024](CI-024.md) | Beta 0.7.3 controller integration full replay gate | Done |
| [CI-025](CI-025.md) | Beta 0.7.3 REST and adapter contract drift gate | Done |
| [CI-026](CI-026.md) | Beta 0.7.3 shared files, startup cache, and long-path parity gate | Done |
| [CI-027](CI-027.md) | Beta 0.7.3 download and persistence replay gate | Done |
| [CI-028](CI-028.md) | Beta 0.7.3 search, server, and Kad parity replay gate | Done |
| [CI-029](CI-029.md) | Beta 0.7.3 network socket, UDP, WebSocket, HTTPS, and UPnP adversity gate | Done |
| [CI-030](CI-030.md) | Beta 0.7.3 UI, preferences, tray, and language resource parity smoke gate | Done |
| [CI-031](CI-031.md) | Beta 0.7.3 packaging, architecture, and release asset parity gate | Done |
| [CI-032](CI-032.md) | Beta 0.7.3 post-tag focused coverage gaps | Done |
| [CI-033](CI-033.md) | Beta 0.7.3 internal pre-release proof | Done |
| [CI-034](CI-034.md) | Package-release provenance and dirty-input guard | Done |
| [CI-036](CI-036.md) | Release certification test matrix | DONE |
| [CI-037](CI-037.md) | Expanded live UI and E2E weak-path stress gate | PASSED |
| [CI-038](CI-038.md) | UI resource-depth and language smoke gate | DONE |
| [CI-039](CI-039.md) | Consolidate Markdown backlog process and validation | DONE |
| [CI-040](CI-040.md) | Standardize current Markdown naming and structure checks | DONE |
| [CI-041](CI-041.md) | Publish Markdown documentation with MkDocs Material | DONE |
| [CI-042](CI-042.md) | Keep only the latest nightly GitHub prerelease per build stream | DONE |
| [CI-043](CI-043.md) | Add aMuTorrent automatic upstream nightly sync and release workflow | DONE |
| [CI-048](CI-048.md) | Improve documentation navigation and public release guidance | DONE |
| [CI-051](CI-051.md) | Move generated workspace outputs outside repos and worktrees | DONE |
| [CI-052](CI-052.md) | RC2+ installer-backed test gate rationalization | DONE |
| [CI-053](CI-053.md) | Fix ARM64 controlled-smoke PCH virtual-memory exhaustion (native host toolchain) | DONE |

## AMUT — aMuTorrent integration (2)

| ID | Title | Status |
| --- | --- | --- |
| [AMUT-001](AMUT-001.md) | aMuTorrent eMule BB browser smoke coverage | Passed |
| [AMUT-002](AMUT-002.md) | aMuTorrent transfer detail hydration | Passed |

## ARR — Arr integration (1)

| ID | Title | Status |
| --- | --- | --- |
| [ARR-001](ARR-001.md) | Full Arr release E2E validation | Passed |
