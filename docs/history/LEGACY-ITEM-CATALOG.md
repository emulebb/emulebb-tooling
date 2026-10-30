# Legacy MFC And Integration Item Catalog

This compact catalog preserves every legacy central backlog ID removed from the
active documentation tree. Full historical specifications remain recoverable from
Git commit `191c7c4dcf615e67fc89b3f24d44da951a4ef6ee`. Recorded statuses are archival facts, not current
workflow state. IDs in this catalog remain permanently reserved and must never be reused.

| ID | Recorded status | Priority | Title |
|---|---|---|---|
| `AMUT-001` | PASSED | Major | aMuTorrent eMule BB browser smoke coverage |
| `AMUT-002` | PASSED | Major | aMuTorrent transfer detail hydration |
| `ARR-001` | PASSED | Major | Full Arr release E2E validation |
| `ARR-002` | OPEN | Major | Make Arr automatic search cache-backed and network-friendly |
| `BUG-001` | DONE | Major | 17 load-only hidden prefs not written back to preferences.ini |
| `BUG-002` | WONT_DO | Minor | ASSERT(0) FIXME in ArchiveRecovery.cpp — unhandled format case falls through silently in release |
| `BUG-003` | DONE | Minor | Historical large-file FIXME markers overstated the remaining live issue |
| `BUG-004` | DONE | Minor | IPFilter overlapping IP ranges not handled — acknowledged correctness gap |
| `BUG-005` | WONT_DO | Minor | Kad buddy connections broken when RequireCrypt is enabled |
| `BUG-006` | WONT_DO | Minor | Weak RNG for crypto challenge value — rand() seeded with time(NULL) |
| `BUG-007` | DONE | Minor | Ring.h — CRing<T> pointer-state, access-guard, and defensive copy cleanup (CODEREV_003, 004, 011) |
| `BUG-008` | WONT_DO | Minor | CaptchaGenerator — rand() & 8 produces bimodal jitter (only 0 or 8, never 1-7) |
| `BUG-009` | DONE | Minor | PartFile — non-atomic part.met replacement (_tremove + _trename crash window) |
| `BUG-010` | DONE | Minor | PartFile — part.met written on low disk space, risking truncation/corruption |
| `BUG-011` | DONE | Minor | Race condition — shareddir_list iterated without lock in SendSharedDirectories |
| `BUG-012` | DONE | Minor | CPartFile destructor calls FlushBuffer after write thread has already exited |
| `BUG-013` | WONT_DO | Minor | ArchiveRecovery.cpp — three unchecked malloc() calls crash on OOM |
| `BUG-014` | DONE | Minor | ZIPFile.cpp — WriteFile return value silently discarded on two paths |
| `BUG-015` | DONE | Minor | GetTickCount() 49-day overflow in ban expiry and download timeout checks |
| `BUG-016` | DONE | Minor | UDP obfuscation applied when crypt layer is disabled — IsCryptLayerEnabled() guard missing |
| `BUG-017` | DONE | Minor | UDP throttler deadlock — sendLocker held when signaling QueueForSendingControlPacket |
| `BUG-018` | DONE | Minor | Part-file hash layout drift — hash tree can mutate during concurrent hashing |
| `BUG-019` | DONE | Minor | AICH sync thread concurrency — multiple unsynchronized shared-state accesses |
| `BUG-020` | DONE | Minor | Client socket teardown ordering — cross-link not cleared before Safe_Delete |
| `BUG-021` | DONE | Minor | Upload queue lock inversion + socket I/O result mishandling + inflate buffer aliasing |
| `BUG-022` | DONE | Major | Long-path delete-to-recycle-bin still breaks in ShellDeleteFile |
| `BUG-023` | DONE | Minor | Shared-file ED2K published column shows a false `No` after publish-state reset |
| `BUG-024` | DONE | Minor | statUTC(HANDLE) returns corrupted `st_size` by combining file size high with file index low |
| `BUG-025` | DONE | Minor | KnownFile hashing open failures log stale or wrong error text on Win32 open failure |
| `BUG-026` | DONE | Major | Search tab teardown frees live result and tab-parameter objects before the UI detaches them |
| `BUG-027` | DONE | Major | IP filter update can delete the live `ipfilter.dat` before replacement promotion succeeds |
| `BUG-028` | WONT_DO | Minor | MP3 ID3 metadata extraction is ANSI-only; non-ACP filenames can silently lose tags |
| `BUG-029` | DONE | Major | Long-path tail hardening across config, media, shell, and GeoLocation surfaces |
| `BUG-030` | DONE | Minor | Obfuscated server logins can advertise redundant callback crypto flags and require extra attempts |
| `BUG-031` | DONE | Minor | Shared-file hashing fails too eagerly on transient sharing and lock violations |
| `BUG-032` | DONE | Minor | AICH hashset save can fail spuriously after hashing because `known2.met` lock wait times out |
| `BUG-033` | WONT_DO | Minor | WebSocket and MiniUPnP shutdown still use forced thread termination |
| `BUG-034` | IN_PROGRESS | Minor | Release paths silently swallow unexpected exceptions via catch (...) plus ASSERT(0) |
| `BUG-035` | IN_PROGRESS | Minor | Historical control-flow still uses bare ASSERT(0) without recovery or logging |
| `BUG-036` | DONE | Major | known.met and cancelled.met still save in place and can truncate on failure |
| `BUG-037` | DONE | Major | Same-hash KnownFile replacement can unshare or mis-track equivalent files |
| `BUG-038` | DONE | Minor | Shared Files sort can retain stale rows after backing data changes |
| `BUG-039` | DONE | Minor | Client list lacked a reusable safe pointer membership check |
| `BUG-040` | DONE | Major | Downloading Clients list could dereference stale client rows |
| `BUG-041` | DONE | Major | Known Clients list could dereference stale client rows |
| `BUG-042` | DONE | Major | Upload list could dereference stale upload rows |
| `BUG-043` | DONE | Major | Queue list could dereference stale queue rows |
| `BUG-044` | DONE | Major | Download source rows could outlive their backing source objects |
| `BUG-045` | DONE | Minor | Server list could dereference stale server rows |
| `BUG-046` | DONE | Major | Kad contact list could dereference stale contact rows |
| `BUG-047` | DONE | Major | Kad search list could dereference stale search rows |
| `BUG-048` | DONE | Minor | IRC nick rows were not cleared before nick objects were deleted |
| `BUG-049` | DONE | Minor | IRC channel tabs were not detached before channel objects were deleted |
| `BUG-050` | DONE | Minor | Chat tabs were not detached before chat items were deleted |
| `BUG-051` | DONE | Minor | IRC channel rows were not cleared before channel entries were deleted |
| `BUG-052` | DONE | Minor | Kad search constructor accidentally added placeholder rows |
| `BUG-053` | DONE | Major | part.met backup could be refreshed from the newly written metadata |
| `BUG-054` | DONE | Major | ESC in shared-file delete confirmation could still delete files |
| `BUG-055` | DONE | Major | AICH recovery accepted invalid part bounds |
| `BUG-056` | DONE | Major | Download Clients list could dereference stale rows during display callbacks |
| `BUG-057` | DONE | Minor | Close All Search Results could leave Kad keyword searches running |
| `BUG-058` | DONE | Minor | Tree option value labels could contain the parser separator |
| `BUG-059` | DONE | Trivial | Download Remaining column alignment was inconsistent |
| `BUG-060` | DONE | Major | REST API should stay available when web templates are absent |
| `BUG-061` | DONE | Major | Legacy web interface template was missing from the shipped tree |
| `BUG-062` | DONE | Minor | Obfuscated server timeout did not retry plain connection promptly |
| `BUG-063` | DONE | Major | ESC in shared-directory delete confirmation could still delete directories |
| `BUG-064` | DONE | Minor | Client list secondary display path needed stale-row guarding |
| `BUG-065` | DONE | Minor | Queue list secondary display path needed stale-row guarding |
| `BUG-066` | DONE | Minor | Upload list secondary display path needed stale-row guarding |
| `BUG-067` | DONE | Minor | REST log route lacked the expected get alias seam |
| `BUG-068` | DONE | Minor | Download progress-bar drawing can leak GDI state into neighboring list cells |
| `BUG-069` | DONE | Major | WebServer static resource requests can escape the web root and allocate whole files |
| `BUG-070` | DONE | Minor | Ignored helper-thread launch failures can hang shutdown waits |
| `BUG-071` | DONE | Major | server.met persistence still uses destructive backup and promotion moves |
| `BUG-072` | DONE | Minor | Kad preferences and routing snapshots still save in place |
| `BUG-073` | DONE | Major | WebServer session and bad-login state is mutated from request threads without synchronization |
| `BUG-074` | WONT_DO | Minor | Archive preview scanner uses volatile cancellation and synchronous UI handoff |
| `BUG-075` | PASSED | Major | REST and WebServer typed error consistency |
| `BUG-076` | PASSED | Major | WebServer malformed request hardening for REST and legacy HTML |
| `BUG-077` | PASSED | Minor | WebServer concurrent REST and legacy HTML soak coverage |
| `BUG-078` | DONE | Critical | qBit compatibility auth can fail open when session RNG is unavailable |
| `BUG-079` | DONE | Critical | WebSocket shutdown can close the termination event while accepted clients still wait on it |
| `BUG-080` | DONE | Major | WebSocket shutdown can forcibly terminate the listener thread |
| `BUG-081` | DONE | Major | HTTPS WebSocket handshake and read loops can spin on WANT_READ/WANT_WRITE |
| `BUG-082` | DONE | Major | GeoLocation and IPFilter background refresh flags can race and remain stuck |
| `BUG-083` | DONE | Major | Client UDP malformed-packet logging can read past a one-byte packet |
| `BUG-084` | DONE | Minor | Web admin high-level actions leak the process token handle |
| `BUG-085` | DONE | Major | Kad/client UDP encryption preference gating needs Release 1 compatibility proof |
| `BUG-086` | DONE | Critical | HTTPS WebSocket casts SOCKET storage to mbedtls_net_context |
| `BUG-087` | DONE | Critical | HTTPS WebSocket queued writes can stall after TLS WANT_READ |
| `BUG-088` | DONE | Major | WebSocket timeout shutdown leaves global state unsafe for restart |
| `BUG-089` | DONE | Major | UDP control sender can deadlock on exception while holding sendLocker |
| `BUG-090` | DONE | Major | Background refresh completion can wedge when UI PostMessage fails |
| `BUG-091` | DONE | Major | DirectDownload ignores close-time write failures |
| `BUG-092` | DONE | Critical | Background refresh workers can write through freed owner memory after shutdown |
| `BUG-093` | DONE | Critical | Failed refresh completion can synchronously block worker on UI thread |
| `BUG-094` | DONE | Major | ResumeThread failure leaks suspended refresh thread objects |
| `BUG-095` | DONE | Major | WebSocket accepted-client tracking is not exception-safe after thread start |
| `BUG-096` | DONE | Major | DirectDownload lacks bounded timeout and cancellation contract |
| `BUG-097` | DONE | Critical | Startup-cache save worker can outlive shared-file list owner |
| `BUG-098` | WONT_DO | Minor | Archive recovery worker uses raw part-file owner across async work |
| `BUG-099` | DONE | Major | WebSocket listener startup is not exception-safe after global state initialization |
| `BUG-100` | DONE | Major | DirectDownload has bounded timeouts but no hard owner cancellation contract |
| `BUG-101` | DONE | Major | Shared Files 50k recursive tree stress profile does not reach main window |
| `BUG-102` | DONE | Major | aMuTorrent browser smoke ignores generated harness port |
| `BUG-111` | DONE | Critical | Release and help URLs still point outside the emulebb namespace |
| `BUG-112` | WONT_DO | Critical | WebServer/qBit session tokens need CSPRNG-backed generation |
| `BUG-113` | DONE | High | Auto-category non-regex matching skips usable tokens |
| `BUG-114` | DONE | Minor | Prevent Standby can leave Windows sleep prevention asserted after disable |
| `BUG-115` | DONE | Minor | Tray left-click skips MiniMule and restores maximized windows as normal |
| `BUG-116` | DONE | Minor | Search results can leave a floating horizontal scrollbar artifact |
| `BUG-117` | DEFERRED | Minor | Audit Year-2038-sensitive persisted and runtime timestamps |
| `BUG-118` | DONE | Minor | CTag UInt64 values can serialize without guaranteed 64-bit promotion |
| `BUG-119` | DONE | Minor | Audit part-file gap and progress arithmetic against eMuleAI hardening |
| `BUG-120` | DONE | Minor | Audit obfuscated server retry behavior against eMuleAI repeat-login fix |
| `BUG-121` | DONE | Major | CorruptionBlackBox split reallocation can invalidate active CArray records |
| `BUG-122` | DONE | Minor | CRing raw-owned buffer was accidentally copyable |
| `BUG-123` | DONE | Major | Failed reask source delete needed explicit download-owner detachment |
| `BUG-124` | DONE | Major | Log panes can nearly freeze the UI under high-volume output |
| `BUG-125` | DONE | Major | Harden client and queue lifetime edges found by focused review |
| `BUG-126` | DONE | Major | Harden transfer queue async lifetime edges |
| `BUG-127` | DONE | Major | Fix regressions from recent C++ hardening review |
| `BUG-128` | DONE | Major | Bound REST compatibility hot-path serialization |
| `BUG-129` | DEFERRED | Major | Follow up remaining C++ hot-path performance findings |
| `BUG-130` | DONE | Major | Harden RC1 hot-path worker and metadata edges |
| `BUG-131` | DONE | Major | Harden RC1 completion, delete, and startup-cache lifetime edges |
| `BUG-132` | DEFERRED | Major | Follow up deferred qBit session and bulk REST hardening |
| `BUG-133` | DONE | Major | Harden RC1 metadata bounds, REST polling, and worker shutdown edges |
| `BUG-134` | DONE | Major | Harden final RC1 shutdown, REST bounds, and AICH repair edges |
| `BUG-135` | DONE | Major | Harden final RC1 runtime stabilization edges |
| `BUG-136` | DONE | Major | Harden final RC1 review follow-up hot paths |
| `BUG-137` | DONE | Major | Harden final RC1 AICH, UPnP, listener, and Kad edges |
| `BUG-138` | DEFERRED | Major | Follow up deferred RC1 REST and search hot-path bounds |
| `BUG-139` | DONE | Minor | Clean exit can leave the shell tray icon behind |
| `BUG-140` | DONE | Major | Transfer UI updates can run on split presentation timers |
| `BUG-141` | DONE | Minor | Source expand icons and video thumbnails can be visually oversized |
| `BUG-142` | OPEN | Minor | Upload soft-queue admission ignores effective score policy |
| `BUG-143` | OPEN | Minor | Upload waiting queue retains clients for unavailable shared files |
| `BUG-144` | DONE | Major | Remote shared-directory requests can freeze large shared profiles |
| `BUG-145` | DONE | Major | Suite bootstrap flow misses LAN, credential, category, and Arr sync polish |
| `BUG-146` | OPEN | Minor | Upload title rate does not match visible uploading row totals |
| `BUG-147` | OPEN | Major | Recursive shared-directory add performs a foreground full shared-file reload |
| `BUG-148` | DONE | Major | Shared Files directory tree node stuck expanded after collapse and cannot re-expand |
| `BUG-149` | DONE | Major | Shared directory tree rebuild is slow and UI-blocking on large shared sets |
| `BUG-150` | DONE | Minor | False multiple_names Caution on cosmetic search-name differences |
| `BUG-151` | OPEN | Major | REST category mutations time out (503) because they block on the main UI thread under load |
| `BUG-152` | OPEN | Major | CServerConnect::DestroySocket can leave a freed CServerSocket pointer in the connectionattempts map |
| `CI-001` | WONT_DO | Major | CMake adoption exploration — replace emule.vcxproj with CMakeLists.txt + Ninja |
| `CI-002` | OPEN | Minor | clang-format — enforce consistent code formatting |
| `CI-003` | DONE | Minor | MSVC compiler hardening — enable SDL, guard checks, and treat warnings as errors |
| `CI-004` | OPEN | Minor | clang-tidy — integrate static analysis into build and CI |
| `CI-005` | OPEN | Minor | cppcheck — integrate complementary bug-class analysis |
| `CI-006` | OPEN | Minor | MSVC AddressSanitizer — enable for debug builds to catch memory errors |
| `CI-007` | OPEN | Minor | Kad — Expand integration and fuzz test coverage beyond helper-unit tests |
| `CI-008` | DONE | Minor | Expand regression coverage for part files, long paths, and WebServer/REST |
| `CI-009` | DONE | Minor | Share-ignore regression coverage and Release test-build stabilization |
| `CI-010` | IN_PROGRESS | Minor | Reduce remaining app-local warning debt after external noise cleanup |
| `CI-011` | DONE | Major | Broadband release live E2E coverage umbrella |
| `CI-012` | DONE | Major | Stabilize Shared Files dynamic folder lifecycle E2E |
| `CI-013` | DONE | Major | Download and search UI live scenarios |
| `CI-014` | PASSED | Major | REST contract manifest and live completeness gate |
| `CI-015` | PASSED | Major | REST malformed and concurrent request matrix |
| `CI-016` | PASSED | Minor | REST-only main vs community regression lane |
| `CI-017` | DONE | Minor | Normalize active workspace line-ending policy to LF by default |
| `CI-018` | DONE | Major | Shared Files 50k-file tree refresh stress gate |
| `CI-019` | DONE | Major | HTTPS and REST socket adversity stress gate |
| `CI-020` | DONE | Major | REST and legacy WebServer error-path coverage gate |
| `CI-021` | DONE | Major | WebSocket and legacy socket leak-churn gate |
| `CI-022` | DONE | Major | Beta 0.7.3 community parity changed-surface ledger |
| `CI-023` | DONE | Major | Beta 0.7.3 post-1.0 hardening regression replay gate |
| `CI-024` | DONE | Major | Beta 0.7.3 controller integration full replay gate |
| `CI-025` | DONE | Major | Beta 0.7.3 REST and adapter contract drift gate |
| `CI-026` | DONE | Major | Beta 0.7.3 shared files, startup cache, and long-path parity gate |
| `CI-027` | DONE | Major | Beta 0.7.3 download and persistence replay gate |
| `CI-028` | DONE | Major | Beta 0.7.3 search, server, and Kad parity replay gate |
| `CI-029` | DONE | Major | Beta 0.7.3 network socket, UDP, WebSocket, HTTPS, and UPnP adversity gate |
| `CI-030` | DONE | Major | Beta 0.7.3 UI, preferences, tray, and language resource parity smoke gate |
| `CI-031` | DONE | Major | Beta 0.7.3 packaging, architecture, and release asset parity gate |
| `CI-032` | DONE | Major | Beta 0.7.3 post-tag focused coverage gaps |
| `CI-033` | DONE | Major | Beta 0.7.3 internal pre-release proof |
| `CI-034` | DONE | Major | Package-release provenance and dirty-input guard |
| `CI-035` | DONE | Major | Final current-head RC proof and fresh package hashes |
| `CI-036` | DONE | Major | Release certification test matrix |
| `CI-037` | PASSED | Major | Expanded live UI and E2E weak-path stress gate |
| `CI-038` | DONE | Major | UI resource-depth and language smoke gate |
| `CI-039` | DONE | Minor | Consolidate Markdown backlog process and validation |
| `CI-040` | DONE | Minor | Standardize current Markdown naming and structure checks |
| `CI-041` | DONE | Minor | Publish Markdown documentation with MkDocs Material |
| `CI-042` | DONE | Minor | Keep only the latest nightly GitHub prerelease per build stream |
| `CI-043` | DONE | Minor | Add aMuTorrent automatic upstream nightly sync and release workflow |
| `CI-044` | OPEN | Major | Add containerized integration profiles for controller and P2P compatibility testing |
| `CI-045` | OPEN | Major | Add workspace-level bind interface selection for predictable live tests |
| `CI-046` | WONT_DO | Minor | Share product-family test profile and fixture hygiene |
| `CI-047` | OPEN | Minor | Add repeatable local package install refresh command |
| `CI-048` | DONE | Minor | Improve documentation navigation and public release guidance |
| `CI-049` | OPEN | Minor | Enable CodeQL code scanning for the app repository |
| `CI-050` | OPEN | Minor | REST surface semantic proof and adapter hardening follow-up |
| `CI-051` | DONE | Major | Move generated workspace outputs outside repos and worktrees |
| `CI-052` | DONE | Major | RC2+ installer-backed test gate rationalization |
| `CI-053` | DONE | Major | Fix ARM64 controlled-smoke PCH virtual-memory exhaustion (native host toolchain) |
| `FEAT-001` | DEFERRED | Minor | Kad FastKad — add diversity-aware bootstrap ranking and aggressive stale decay |
| `FEAT-002` | DEFERRED | Major | Kad SafeKad — evolve from coarse same-IP gate into layered trust model (CGNAT fix) |
| `FEAT-003` | DEFERRED | Minor | Kad — Add response usefulness scoring and subnet-diversity search fanout |
| `FEAT-004` | DEFERRED | Minor | Kad — Generalise KadPublishGuard abuse budget beyond PUBLISH_SOURCE |
| `FEAT-005` | DEFERRED | Minor | Kad — Restore network-change grace handling around routing persistence and probing |
| `FEAT-006` | DEFERRED | Minor | Kad — Add explicit trust, budget, and bootstrap observability counters |
| `FEAT-007` | DEFERRED | Minor | Windows Property Store integration for non-media file metadata |
| `FEAT-008` | DEFERRED | Trivial | Oracle protocol guard seams — integrate stale branch test scaffolding |
| `FEAT-009` | DEFERRED | Trivial | Mirror audit guard seam — WIP work from stale branch parent commit |
| `FEAT-010` | DONE | Minor | Long path support phase 2 — shell/UI, shared-directory recursion, exact-name paths, and path-helper audit |
| `FEAT-011` | DEFERRED | Minor | CShield — integrate ED2K anti-leecher engine (44 bad-client categories) |
| `FEAT-012` | DONE | Minor | PR_TCPERRORFLOODER — TCP listen-socket flood defense |
| `FEAT-013` | DONE | Major | REST API — add authenticated in-process JSON endpoints to WebServer |
| `FEAT-014` | DEFERRED | Minor | REST API follow-up — OpenAPI docs and optional external gateway |
| `FEAT-015` | DONE | Major | Broadband upload slot allocation — fixed cap + weak-slot reclamation |
| `FEAT-016` | DONE | Major | Modern limits — update stale hard-coded defaults for broadband/modern hardware |
| `FEAT-017` | DEFERRED | Major | DPI awareness — Per-Monitor V2 manifest + hardcoded pixel audit |
| `FEAT-018` | DEFERRED | Minor | µTP (Micro Transport Protocol) transport layer — CUtpSocket / libutp |
| `FEAT-019` | DEFERRED | Minor | Dark mode UI — system-aware Windows 10 dark theme integration |
| `FEAT-020` | DONE | Trivial | DB-IP city geolocation — location label and flag per peer |
| `FEAT-021` | DEFERRED | Minor | SourceSaver — persist download source lists between sessions |
| `FEAT-022` | DONE | Minor | Startup config directory override — `-c` flag for alternate preferences path |
| `FEAT-023` | DONE | Minor | Broadband queue scoring and ratio/cooldown UI extras |
| `FEAT-024` | DONE | Minor | Share-ignore policy with additive `shareignore.dat` |
| `FEAT-025` | DONE | Minor | Normalize download filenames on intake and completion |
| `FEAT-026` | DONE | Minor | Shared startup cache with known.met lookup index and `sharedcache.dat` |
| `FEAT-027` | DONE | Minor | Startup sequencing fix, startup profiling, and shared-view startup churn cleanup |
| `FEAT-028` | DONE | Minor | Virtualize and harden shared files list |
| `FEAT-029` | DONE | Minor | Search result ceilings — configurable ed2k expansion plus moderate Kad totals/lifetimes |
| `FEAT-030` | DONE | Minor | Bind policy completion — global `BindAddr` everywhere else, separate `WebBindAddr` for WebServer |
| `FEAT-031` | DEFERRED | Minor | Auto-browse peers that expose remote shared-file inventories |
| `FEAT-032` | DEFERRED | Minor | NAT mapping modernization — lease controls, status visibility, and PCP/NAT-PMP |
| `FEAT-033` | DONE | Minor | Disk-space floor hardening and legacy import-flow retirement |
| `FEAT-034` | DEFERRED | Minor | Shared-files reload should stop blocking the UI on large trees |
| `FEAT-035` | DEFERRED | Major | IPv6 dual-stack compatibility for current eD2K/Kad networking |
| `FEAT-036` | DEFERRED | Major | NAT traversal and extended source exchange for LowID-to-LowID connectivity |
| `FEAT-037` | DEFERRED | Minor | Release-oriented sharing controls — PowerShare, Release Bonus, and Share Only The Need |
| `FEAT-038` | DONE | Minor | Shared-files watcher and live recursive share sync |
| `FEAT-039` | DEFERRED | Minor | Download checker — duplicate and near-duplicate intake guard |
| `FEAT-040` | DEFERRED | Major | Headless core with modern web/mobile controller and multi-user permissions |
| `FEAT-041` | DEFERRED | Minor | Download Inspector automation for stale downloads and majority-name rename |
| `FEAT-042` | DONE | Minor | Automatic IP filter update scheduling |
| `FEAT-043` | DEFERRED | Minor | Known Clients history and incremental list refresh performance |
| `FEAT-044` | DEFERRED | Minor | IP filter input policy - PeerGuardian lists, whitelist, and private-IP exemption |
| `FEAT-045` | PASSED | Major | REST transfer detail endpoint for controller parity |
| `FEAT-046` | PASSED | Major | REST server and Kad bootstrap/import APIs |
| `FEAT-047` | PASSED | Minor | REST search API completeness pass |
| `FEAT-048` | PASSED | Minor | REST upload queue control completeness |
| `FEAT-049` | PASSED | Minor | Curated REST preference expansion |
| `FEAT-050` | PASSED | Minor | Launch external program on completed download |
| `FEAT-051` | DONE | Minor | Pro-user context menus and always-on advanced controls |
| `FEAT-052` | DONE | Minor | Main-shell keyboard shortcuts and mnemonic audit |
| `FEAT-053` | DONE | Minor | Classic tray balloon notification mode |
| `FEAT-054` | DONE | Minor | Normalize download message filename display |
| `FEAT-055` | DONE | Minor | Beta 0.7.3 improvement triage lane |
| `FEAT-056` | DEFERRED | Minor | Post-0.7.3 release proof automation and operator evidence UX |
| `FEAT-057` | DONE | Minor | Add qBittorrent-style download shortcuts and batch menu actions |
| `FEAT-058` | DONE | Minor | Beta 0.7.3 closeout UX polish and audit report |
| `FEAT-059` | DONE | Minor | Move tray icon visibility preference next to minimize-to-tray |
| `FEAT-060` | DONE | Minor | Preference inventory, mapping, clamp, and persistence audit |
| `FEAT-061` | DONE | Minor | Strong preference schema validation |
| `FEAT-062` | DONE | Minor | Category management dialog polish and robustness |
| `FEAT-063` | DONE | Minor | Web Interface preferences layout polish |
| `FEAT-064` | DEFERRED | Minor | Archived post-0.7.3 MFC future roadmap |
| `FEAT-065` | DONE | Minor | Polish the native MiniMule tray popup |
| `FEAT-066` | DONE | Minor | Replace MiniMule chrome with table and speed chart |
| `FEAT-067` | WONT_DO | Minor | External VPN kill-switch watchdog |
| `FEAT-068` | DEFERRED | Minor | Bound REST large-list memory and latency for very large profiles |
| `FEAT-069` | DEFERRED | Minor | Shared-file include and exclude pattern rules |
| `FEAT-070` | DEFERRED | Minor | Add targeted client UserHash and upload-lifecycle diagnostics |
| `FEAT-071` | DONE | Minor | Filename mojibake repair for search results and download intake |
| `FEAT-072` | DEFERRED | Minor | Reduce startup cache UI-thread blocking on large shared libraries |
| `FEAT-073` | WONT_DO | Minor | Incorporate p2p-overlord into the eMuleBB product family |
| `FEAT-074` | DONE | Minor | Add main-window visual evidence for connected LowID state |
| `FEAT-075` | DEFERRED | Minor | Keep startup progress responsive during daily config backup |
| `FEAT-076` | DEFERRED | Minor | Parallelize shared-file hashing across physical volumes and SSDs |
| `FEAT-077` | DEFERRED | Minor | Auto-managed upload friend-slot candidates without mutating manual friends |
| `FEAT-078` | DEFERRED | Minor | Persist auto-browse inventories in a local queryable database |
| `FEAT-079` | DEFERRED | Minor | Save known and cancelled metadata from immutable background snapshots |
| `FEAT-080` | DEFERRED | Minor | Refresh protected-volume disk-space snapshots in the background |
| `FEAT-081` | DEFERRED | Trivial | Add a bounded source-hostname resolver pool only if profiling shows backlog |
| `FEAT-082` | DEFERRED | Minor | Virtualize high-volume downloads, search results, and client-history lists |
| `FEAT-083` | WONT_DO | Minor | Connection Checker based on public reachability polling |
| `FEAT-084` | WONT_DO | Minor | Migration Wizard for legacy profile import |
| `FEAT-085` | WONT_DO | Minor | Establish a shared campaign core for eMuleBB product-family test orchestration |
| `FEAT-086` | DEFERRED | Minor | Parse eMuleAI extension hints without advertising protocol support |
| `FEAT-087` | DEFERRED | Minor | Add transfer minicharts and aggregate progress metrics |
| `FEAT-088` | DEFERRED | Minor | Keep completed upload rows visible briefly |
| `FEAT-089` | DEFERRED | Minor | Add in-app guided Prowlarr indexer setup for eMuleBB |
| `FEAT-090` | DEFERRED | Minor | Tune broadband limits by drive topology and total budget |
| `FEAT-091` | DEFERRED | Minor | Downloads list expand/collapse-all peer rows |
| `FEAT-092` | DEFERRED | Minor | Add layered peer behavior guard for client quarantine and IP-ban escalation |
| `FEAT-093` | DEFERRED | Minor | Safely raise WebServer accepted-client concurrency |
| `FEAT-094` | DEFERRED | Major | Improve UDP burst handling without lock-held backoff |
| `FEAT-095` | DEFERRED | Major | Move part-file durability work off foreground paths |
| `FEAT-096` | DEFERRED | Minor | Improve client and network statistics observability |
| `FEAT-097` | DONE | Minor | Add connection pressure details to Network Information |
| `FEAT-098` | DEFERRED | Major | Add strict bound public-IP guard for VPN profiles |
| `FEAT-099` | DEFERRED | Minor | Add app event webhooks for controller automation |
| `FEAT-100` | DEFERRED | Major | Improve startup progress and UI readiness locking |
| `FEAT-101` | DEFERRED | Minor | Add quick filter textbox to Downloads list |
| `FEAT-102` | DEFERRED | Minor | Exclude known files from search results |
| `FEAT-103` | DEFERRED | Minor | Publish Windows Hyper-V run guide for eMuleBB |
| `FEAT-104` | DEFERRED | Minor | Add optional reverse DNS peer name resolution |
| `FEAT-105` | DEFERRED | Minor | Add stopped upload state for shared files |
| `FEAT-106` | DEFERRED | Major | Add upload bandwidth ramp-up diagnostics and slot policy |
| `FEAT-107` | DEFERRED | Minor | Add upload under-target reason diagnostics |
| `FEAT-108` | DEFERRED | Minor | Add publish effectiveness feedback for shared files |
| `FEAT-109` | DEFERRED | Minor | Materialize suite tool dependencies deterministically |
| `FEAT-110` | DEFERRED | Minor | Add configurable title bar status format |
| `FEAT-111` | DEFERRED | Minor | Add peer and queue diagnostics columns |
| `FEAT-112` | DEFERRED | Minor | Add Torrent search type convenience filter and refresh file-type extensions |
| `FEAT-113` | DEFERRED | Minor | Persist peer upload performance history for slot selection |
| `FEAT-114` | DEFERRED | Minor | Add storage-aware hash and verify throttling |
| `FEAT-115` | DEFERRED | Minor | Add per-volume storage policy hints and diagnostics |
| `FEAT-116` | DEFERRED | Minor | Throttle background share scanning on active slow volumes |
| `FEAT-117` | DEFERRED | Minor | Indicate already-shared files in the unshared-folder share preview |
| `FEAT-118` | DONE | Minor | Composite Confidence indicator replacing the Risk + Kad-Confidence columns |
| `FEAT-119` | DONE | Minor | Quick hide already-known files filter in search results |
| `FEAT-120` | DONE | Minor | Sortable Extension column in search results |
| `FEAT-121` | DEFERRED | Major | STUN UDP egress gate for the VPN guard (eMuleBB and emulebb-rust) |
| `FEAT-122` | WONT_DO | Minor | Do not add GET /api/v1/capabilities to emulebb-mfc |
| `FEAT-123` | DONE | Major | Shared files one-level auto-updater |
| `FEAT-124` | DEFERRED | Minor | Leech mode - monitoring-only build that observes the network without sharing |
| `REF-001` | WONT_DO | Major | Keep the existing CZIPFile implementation |
| `REF-002` | DONE | Major | Remove Source Exchange v1 branches — deprecated protocol superseded by v2 |
| `REF-003` | DEFERRED | Trivial | Rename stale IRC string resources left over from IRC module removal |
| `REF-004` | DONE | Minor | Audit and disposition 17 load-only hidden preference keys |
| `REF-005` | DONE | Trivial | Remove or restore dead DebugSourceExchange log calls in DownloadQueue.cpp |
| `REF-006` | DONE | Trivial | GetCategory const-correctness cleanup in DownloadListCtrl / CPartFile |
| `REF-007` | DONE | Trivial | WebM vs MKV disambiguation in MIME magic-byte detection |
| `REF-008` | WONT_DO | Major | Replace CAsyncSocketEx custom WinSock wrapper — Boost.Asio or Windows IOCP |
| `REF-009` | WONT_DO | Major | Replace CCriticalSection + CWinThread + Win32 events — std::mutex/thread or Boost |
| `REF-010` | WONT_DO | Major | Replace raw owned pointers with std::unique_ptr / std::shared_ptr |
| `REF-011` | WONT_DO | Minor | Replace GetTickCount / SetTimer with type-safe monotonic clock — std::chrono or Boost |
| `REF-012` | WONT_DO | Minor | Replace CFile + CString path concatenation — std::filesystem or boost::filesystem |
| `REF-013` | WONT_DO | Minor | Replace CString + unsafe sprintf with safe string formatting — std or Boost |
| `REF-014` | WONT_DO | Minor | Replace custom CRing<T> circular buffer — fix in place, std::deque, or boost::circular_buffer |
| `REF-015` | WONT_DO | Minor | Keep miniupnpc as the active UPnP backend |
| `REF-016` | WONT_DO | Trivial | Keep ResizableLib out-of-tree instead of inlining it |
| `REF-017` | DONE | Minor | Revalidate and close the dead-code sweep backlog item |
| `REF-018` | DONE | Minor | Remove defunct PeerCache surface and legacy INI fallback reads |
| `REF-019` | DONE | Minor | Replace ASSERT(0) + "must be a bug" with proper error handling in EncryptedStreamSocket |
| `REF-020` | DONE | Minor | Replace dynamic loading of always-present Win10 APIs with static linking |
| `REF-021` | DEFERRED | Minor | Remove blanket warning suppressions and replace deprecated Winsock APIs |
| `REF-022` | DEFERRED | Trivial | Replace custom type aliases in types.h with <cstdint> standard types |
| `REF-023` | DONE | Minor | Replace unsafe sprintf/_stprintf/wsprintf with safe equivalents |
| `REF-024` | DEFERRED | Trivial | Convert #define constants in Opcodes.h to constexpr in namespace |
| `REF-025` | DEFERRED | Minor | Remove legacy feature set — IRC, SMTP, Scheduler, first-start wizard, splash screen, legacy update checker |
| `REF-026` | DONE | Minor | Manifest — drop legacy OS entries, add Common Controls 6.0 dependency |
| `REF-027` | DEFERRED | Minor | CaptchaGenerator — replace CxImage with ATL CImage / native GDI |
| `REF-028` | DEFERRED | Minor | Audit current MbedTLS 4.1 integration |
| `REF-029` | DEFERRED | Major | Move async socket readiness to WSAPoll backends |
| `REF-030` | DONE | Minor | Replace window-message async hostname resolver with worker-thread model |
| `REF-031` | DONE | Minor | Review upload queue scoring against community and stale baselines |
| `REF-032` | DEFERRED | Minor | Use MFC-native property sheets and dynamic layout instead of CTreePropSheet / ResizableLib |
| `REF-033` | DEFERRED | Trivial | Remove remaining IE/MSHTML drag-drop, HTML Help, and legacy IE web-client baggage |
| `REF-034` | DEFERRED | Minor | Resolve Crypto++ 8.4 vs 8.9 dependency truth |
| `REF-035` | DEFERRED | Minor | Adopt WIL for narrow Windows and COM RAII cleanup |
| `REF-036` | DEFERRED | Minor | Adopt GSL contracts for buffer and pointer boundary hardening |
| `REF-037` | DONE | Major | Beta 0.7.3 legacy and frozen feature disposition ledger |
| `REF-038` | DONE | Minor | Harden optional MediaInfo DLL loading and metadata extraction seams |
| `REF-039` | DONE | Minor | Classify MediaInfo loader failures and bound metadata extraction counts |
| `REF-040` | DONE | Minor | Harden external UnRAR DLL loading |
| `REF-041` | DONE | Minor | Move remaining active app DLL probes to LoadLibraryEx |
| `REF-042` | DEFERRED | Minor | Consolidate WinInet download helpers and review URL shortcut intake |
| `REF-043` | DEFERRED | Minor | Drop legacy Web Interface templates and keep REST as the supported controller surface |
| `REF-044` | DEFERRED | Minor | Remove remaining import-parts residue and keep legacy import flows retired |
| `REF-045` | DEFERRED | Minor | Evaluate SQLite-backed storage for local metadata structures |
| `REF-046` | DEFERRED | Minor | Evaluate JSON or TOML for operator-editable configuration |
| `REF-047` | DONE | High | Finalize native REST v1 API standardization before RC1 |
| `REF-048` | DEFERRED | Minor | Reduce queue and tracking scan cost without policy drift |
| `REF-049` | DEFERRED | Major | Shorten upload hot-path locks only after adding lifetime guards |
| `REF-050` | DEFERRED | Minor | Tune compression and hash buffers with bounded memory |
| `REF-051` | DEFERRED | Minor | Remove legacy SOCKS and proxy support |
| `REF-052` | DEFERRED | Minor | Remove archive preview and recovery surfaces |
| `REF-053` | DEFERRED | Minor | Reduce upload queue and upload list linear lookup overhead |
| `REF-054` | DONE | Minor | Stabilize and instrument download queue behavior |
| `REF-055` | DEFERRED | Minor | Post-RC2 code-quality and C++ modernization backlog |
| `REF-056` | DEFERRED | Minor | Standardize agent on-ramp and AGENTS.md pointer layer |
| `REF-057` | DEFERRED | Minor | Defer GeoLocation MMDB load off the pre-window startup path |
| `REF-058` | DEFERRED | Minor | Async known-file and shared-file startup load to unblock the UI thread |
| `REF-059` | DEFERRED | Major | Align the VPN guard across eMuleBB MFC and emulebb-rust |
