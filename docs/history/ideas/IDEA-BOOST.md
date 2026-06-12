# IDEA-BOOST - Abandoned Boost / POCO Adoption Exploration

> Abandoned historical idea. This is not an active implementation plan, not
> Release 1 scope, and not current branch direction. Operator decision on
> 2026-05-21 closed the linked backlog records as `WONT_DO`.
> Archived sections below preserve migration wording from the original note;
> read them as provenance, not scheduled work.

> Analysis based on the full 611-file C++ codebase at `srchybrid/`.  
> Date: 2026-04-08

---

## Table of Contents

1. [Summary & Rationale](#summary-rationale)
2. [CRITICAL — Networking & Async I/O](#critical-networking-async-io-71-files)
3. [HIGH — Threading & Synchronization](#high-threading-synchronization-15-files)
4. [HIGH — Smart Pointers & Memory Management](#high-smart-pointers-memory-management-extensive)
5. [HIGH — String Handling](#high-string-handling-50-files)
6. [MEDIUM — File I/O & Paths](#medium-file-io-paths-40-files)
7. [MEDIUM — Time & Timers](#medium-time-timers-40-files)
8. [MEDIUM — Circular Buffer](#medium-circular-buffer)
9. [MEDIUM — Error Handling](#medium-error-handling-35-files)
10. [MEDIUM — Logging](#medium-logging)
11. [LOW — Regular Expressions](#low-regular-expressions)
12. [LOW — Configuration Parsing](#low-configuration-parsing)
13. [LOW — Cryptography](#low-cryptography)
14. [Summary Table](#summary-table)
15. [Migration Strategy](#migration-strategy)

---

## Summary & Rationale

eMule's `srchybrid` was written for Windows/MFC circa 2002–2004. It relies heavily on:

- Win32-specific threading primitives (critical sections, events, Win32 handles)
- MFC containers (`CList`, `CMap`, `CArray`, `CTypedPtrList`)
- MFC strings (`CString`) and formatting (`sprintf`, `_T()`)
- A custom WinSock2 async socket wrapper (`CAsyncSocketEx`) spanning thousands of lines
- Raw pointer ownership with manual `new`/`delete`
- `GetTickCount()` (49-day wrap bug), `SetTimer()`, manual scheduler loops
- A custom logging subsystem (`CLogFile`)
- Binary-packed config structs with `#pragma pack`

**Boost** and **POCO** offer battle-tested, cross-platform, exception-safe replacements for nearly all of these. The benefits are:

- **Safety:** RAII-based locking, smart pointers, and typed error codes eliminate entire classes of bugs.
- **Correctness:** `boost::chrono` fixes the 49-day `GetTickCount` wrap; Boost.Asio fixes races in the socket event loop.
- **Maintainability:** Replacing ~3000 lines of custom WinSock infrastructure with Boost.Asio dramatically reduces maintenance burden.
- **Portability:** Reduces coupling to Win32/MFC, enabling future Linux builds.

---

## CRITICAL — Networking & Async I/O (71+ files)

### Problem

`CAsyncSocketEx` is a custom async socket layer built on top of WinSock2 that dispatches events via hidden Win32 window messages:

```cpp
// AsyncSocketEx.h:80-86
#define WM_SOCKETEX_TRIGGER     (WM_USER + 0x101 + 0)
#define WM_SOCKETEX_GETHOST     (WM_USER + 0x101 + 1)
#define WM_SOCKETEX_CALLBACK    (WM_USER + 0x101 + 2)
#define WM_SOCKETEX_NOTIFY      (WM_USER + 0x101 + 3)
#define MAX_SOCKETS (0xBFFF - WM_SOCKETEX_NOTIFY + 1)
```

DNS resolution is done via the old async WinSock callback pattern:

```cpp
// AsyncSocketEx.h:296-298
char *m_pAsyncGetHostByNameBuffer;
HANDLE m_hAsyncGetHostByNameHandle;
USHORT m_nAsyncGetHostByNamePort;
```

UDP queues carry raw pointer lists protected by a per-socket critical section:

```cpp
// UDPSocket.h:51-83
class CUDPSocket : public CAsyncSocket, public CEncryptedDatagramSocket
{
private:
    CTypedPtrList<CPtrList, SServerUDPPacket*> controlpacket_queue;
    CTypedPtrList<CPtrList, SServerDNSRequest*> m_aDNSReqs;
    CCriticalSection sendLocker;
};
```

Raw `SOCKET` handles appear directly in headers:

```cpp
// WebSocket.h:30
SOCKET m_hSocket;
```

**Affected files:** `AsyncSocketEx.h/cpp`, `EMSocket.h/cpp`, `ServerSocket.h/cpp`,
`UDPSocket.h/cpp`, `WebSocket.h/cpp`, `ListenSocket.cpp`, and ~65 more.

### Solution: Boost.Asio

**Boost.Asio** provides a complete async I/O framework (Windows IOCP, Linux epoll,
BSD kqueue) with a unified API:

```cpp
#include <boost/asio.hpp>
using boost::asio::ip::tcp;
using boost::asio::ip::udp;

// TCP socket — replaces raw SOCKET + CAsyncSocketEx
boost::asio::io_context io_ctx;
tcp::socket sock(io_ctx);

// Async connect — replaces WM_SOCKETEX_TRIGGER dispatch
sock.async_connect(endpoint, [](boost::system::error_code ec) {
    if (!ec) { /* connected */ }
});

// Async DNS — replaces m_hAsyncGetHostByNameHandle
tcp::resolver resolver(io_ctx);
resolver.async_resolve("hostname", "4662", [](auto ec, auto results) {
    // results is an endpoint iterator
});

// Async UDP send — replaces controlpacket_queue + sendLocker
udp::socket usock(io_ctx);
usock.async_send_to(boost::asio::buffer(data), remote_ep,
    [](boost::system::error_code ec, std::size_t bytes) {});

// Timer — replaces SetTimer() + GetTickCount() scheduling
boost::asio::steady_timer timer(io_ctx, std::chrono::milliseconds(100));
timer.async_wait([](boost::system::error_code ec) { /* tick */ });
```

**Why it's better:**
- Eliminates the hidden-window message-pump event dispatch entirely
- Built-in async DNS without `gethostbyname` / callback handles
- Scales to thousands of simultaneous connections via IOCP on Windows
- RAII socket lifetime — no raw `SOCKET` handles or `closesocket()` calls
- Integrates timers, DNS, TCP, UDP into one event loop (`io_context`)
- ~3000 lines of custom `CAsyncSocketEx` infrastructure replaced by one library include

---

## HIGH — Threading & Synchronization (15+ files)

### Problem

Raw Win32 synchronization primitives are used throughout:

```cpp
// EMSocket.h:134
CCriticalSection sendLocker;

// EMSocket.h:44 — manual Lock/Unlock (not exception-safe)
void SetConState(uint8 val) { sendLocker.Lock(); byConnected = val; sendLocker.Unlock(); }

// GDIThread.h:23-24
HANDLE m_hEventKill;
HANDLE m_hEventDead;

// GDIThread.cpp:45-57
m_hEventKill = CreateEvent(NULL, TRUE, FALSE, NULL);
m_hEventDead = CreateEvent(NULL, TRUE, FALSE, NULL);

// GDIThread.cpp:72,88,94
while (::WaitForSingleObject(m_hEventKill, 0) == WAIT_TIMEOUT)
    SingleStep();
VERIFY(::SetEvent(m_hEventDead));
::CloseHandle(m_hEventKill);

// PartFileWriteThread.h:64-65
CEvent m_eventThreadEnded;
CEvent m_eventPaused;

// UploadBandwidthThrottler.h:68-69
CCriticalSection m_sendLocker;
CCriticalSection m_queueLocker;

// TLSthreading.cpp:13-44 — manual wrappers around CRITICAL_SECTION
int threading_mutex_init_alt(mbedtls_platform_mutex_t *mutex) noexcept {
    ::InitializeCriticalSection(&mutex->cs);
    mutex->is_valid = 1;
    return 0;
}
int threading_mutex_lock_alt(mbedtls_platform_mutex_t *mutex) noexcept {
    ::EnterCriticalSection(&mutex->cs);
    return 0;
}
```

Also, `CWinThread` is used as the base for worker threads:

```cpp
// GDIThread.h:9,23,61
class CGDIThread : public CWinThread { ... };

// PartFileWriteThread.h:35-68
class CPartFileWriteThread : public CWinThread { ... };

// UploadBandwidthThrottler.h:22-81
class CUploadBandwidthThrottler : public CWinThread { ... };
```

**Problems:**
- `CCriticalSection::Lock/Unlock` are not exception-safe — an exception between Lock and Unlock causes a deadlock.
- `HANDLE`-based events require manual `CloseHandle` and are error-prone.
- `TLSthreading.cpp` duplicates critical section wrapping code that already exists elsewhere.

### Solution: Boost.Thread + Boost.Mutex

```cpp
#include <boost/thread/mutex.hpp>
#include <boost/thread/lock_guard.hpp>
#include <boost/thread/condition_variable.hpp>
#include <boost/thread/thread.hpp>

// Replace CCriticalSection
boost::mutex sendLocker;

// Replace Lock/Unlock — RAII, exception-safe
void SetConState(uint8 val) {
    boost::lock_guard<boost::mutex> guard(sendLocker);
    byConnected = val;
}  // unlocks automatically even if exception thrown

// Replace HANDLE events + WaitForSingleObject/SetEvent
boost::condition_variable cv;
boost::mutex cv_mutex;
bool killFlag = false;

// Waiting thread:
{
    boost::unique_lock<boost::mutex> lk(cv_mutex);
    cv.wait(lk, [] { return killFlag; });
}

// Signaling thread:
{
    boost::lock_guard<boost::mutex> lk(cv_mutex);
    killFlag = true;
}
cv.notify_one();

// Replace CWinThread
boost::thread workerThread([]() {
    // thread body
});
workerThread.join();
```

**Replace `TLSthreading.cpp` wrappers:**
```cpp
// Instead of custom InitializeCriticalSection wrappers, use:
static boost::mutex tls_mutex;
int threading_mutex_lock_alt(mbedtls_platform_mutex_t *mutex) noexcept {
    mutex->boost_mutex.lock();
    return 0;
}
```

**Why it's better:**
- `boost::lock_guard` guarantees unlock on any exit path (return, exception, goto)
- `boost::condition_variable` is semantically correct for signaling; Win32 events are not
- `boost::thread` handles platform-specific thread creation internally
- Eliminates `CreateEvent`/`CloseHandle` boilerplate
- `TLSthreading.cpp` custom wrappers can be deleted entirely

---

## HIGH — Smart Pointers & Memory Management (extensive)

### Problem

Raw pointer ownership is pervasive. Manual allocation and deallocation, with no clear
ownership semantics:

```cpp
// WebSocket.h:12-26 — hand-rolled linked list with raw char*
class CWebSocket
{
public:
    CWebServer *m_pParent;         // non-owning? owning? unclear

    class CChunk
    {
    public:
        char   *m_pData;           // owned
        char   *m_pToSend;         // interior pointer — dangerous
        CChunk *m_pNext;           // owned
        DWORD   m_dwSize;
        ~CChunk() { delete[] m_pData; }  // manual cleanup
    };

    CChunk *m_pHead;               // owns chain
    CChunk *m_pTail;               // non-owning alias
    char   *m_pBuf;
};

// EncryptedStreamSocket.h:115-118
RC4_Key_Struct  *m_pRC4SendKey;       // owned?
RC4_Key_Struct  *m_pRC4ReceiveKey;    // owned?
CSafeMemFile    *m_pfiReceiveBuffer;  // owned
CSafeMemFile    *m_pfiSendBuffer;     // owned
```

**Problems:**
- No clear ownership → memory leaks and double-frees
- Exceptions between `new` and corresponding `delete` leak memory
- Interior pointer `m_pToSend` into `m_pData` is undefined behaviour if `m_pData` moves

### Solution: std::unique_ptr / std::shared_ptr / boost::shared_ptr

```cpp
// WebSocket chunk list — replace with unique_ptr chain
struct CChunk {
    std::unique_ptr<char[]> m_pData;
    std::size_t             m_dwSize;
    std::unique_ptr<CChunk> m_pNext;   // linked-list ownership chain
};
std::unique_ptr<CChunk> m_pHead;       // owns entire list

// Or, simpler: replace the hand-rolled list entirely
std::list<std::vector<char>> m_sendQueue;

// EncryptedStreamSocket — explicit ownership
std::unique_ptr<RC4_Key_Struct>  m_pRC4SendKey;
std::unique_ptr<RC4_Key_Struct>  m_pRC4ReceiveKey;
std::unique_ptr<CSafeMemFile>    m_pfiReceiveBuffer;
std::unique_ptr<CSafeMemFile>    m_pfiSendBuffer;

// Non-owning pointer to parent (replaces raw CWebServer*)
// Use raw pointer or std::weak_ptr if shared ownership is needed
CWebServer *m_pParent;   // explicitly non-owning, documented
```

**Why it's better:**
- `unique_ptr` destructor calls `delete` automatically — no leaks on any exit path
- Ownership is expressed in the type — no guessing from docs or comments
- `shared_ptr` + `weak_ptr` for objects with shared/cyclic ownership (e.g., upload slots referencing clients)
- Eliminates the interior pointer pattern entirely

---

## HIGH — String Handling (50+ files)

### Problem

`CString` is used for essentially all string operations. This couples core logic to MFC
and creates implicit wide/narrow encoding issues.

```cpp
// AsyncSocketEx.h:133,179,186
const CString &sSocketAddress = CString();
bool Bind(UINT nSocketPort, const CString &sSocketAddress = CString());
virtual bool Connect(const CString &sHostAddress, UINT nHostPort);

// OtherFunctions.h:113-115
CString GetNextString(const CString &rstr, LPCTSTR pszTokens, int &riStart);
CString GetNextString(const CString &rstr, TCHAR chToken, int &riStart);

// OtherFunctions.h:120-145 — multiple overloads per integral type
CString CastItoXBytes(uint16 count, bool isK = false, ...);
CString CastItoXBytes(uint32 count, bool isK = false, ...);
CString CastItoXBytes(uint64 count, bool isK = false, ...);
CString SecToTimeLength(UINT uiSec);
```

Formatting uses `sprintf` with manually sized buffers — classic buffer-overflow risk:

```cpp
TCHAR buf[64];
_stprintf(buf, _T("%u KB"), count / 1024);
```

### Solution: std::string + Boost.StringAlgorithms + Boost.Format

```cpp
#include <string>
#include <boost/algorithm/string.hpp>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>

// Replace CString in API signatures
bool Bind(unsigned int port, const std::string &address = {});
bool Connect(const std::string &host, unsigned int port);

// Replace GetNextString tokeniser
std::vector<std::string> tokens;
boost::algorithm::split(tokens, input, boost::is_any_of(",;"));

// Replace manual trim
boost::algorithm::trim(str);
boost::algorithm::to_lower(str);

// Replace sprintf — type-safe, no buffer
std::string msg = boost::str(boost::format("%1% KB") % (count / 1024));
std::string msg2 = boost::str(boost::format("%-20s %10d") % name % value);

// Replace _ttoi / CString -> int conversions
int port = boost::lexical_cast<int>(portString);

// Replace CastItoXBytes overloads — one template
template<typename T>
std::string CastItoXBytes(T count, bool isK = false) {
    if (isK) return boost::str(boost::format("%1% KB") % (count / 1024));
    return boost::str(boost::format("%1% B") % count);
}
```

**Why it's better:**
- `boost::format` is type-safe; mismatched format specifiers are caught at runtime (not silent UB)
- No fixed-size `TCHAR buf[64]` — no buffer overflows
- `boost::algorithm` functions are well-tested and composable
- `std::string` is standard; removes MFC dependency from core string logic
- `boost::lexical_cast` throws `bad_lexical_cast` on invalid input rather than returning 0 silently

---

## MEDIUM — File I/O & Paths (40+ files)

### Problem

File operations go through `CFile` (MFC), and path manipulation is done via string
concatenation on `CString`:

```cpp
// SafeFile.h:74-82
class CSafeFile : public CFile, public CFileDataIO
{
public:
    CSafeFile() = default;
    CSafeFile(LPCTSTR lpszFileName, UINT nOpenFlags)
        : CFile(lpszFileName, nOpenFlags) {}

    virtual UINT Read(void *lpBuf, UINT nCount);
    virtual void Write(const void *lpBuf, UINT nCount);
};

// PartFile.h:145-156
const CString& GetFullName() const { return m_fullname; }
void SetFullName(const CString &name) { m_fullname = name; }
CString GetTmpPath() const;
EMFileSize GetRealFileSize() const { return GetDiskFileSize(GetFilePath()); }
time_t GetFileDate() const { return m_tLastModified; }
```

### Solution: Boost.Filesystem

```cpp
#include <boost/filesystem.hpp>
namespace fs = boost::filesystem;

// Path construction and manipulation
fs::path fullPath = fs::path(baseDir) / filename;  // correct separator on any OS
fs::path tmpPath  = fullPath.parent_path() / (fullPath.stem().string() + ".tmp");

// File info
if (fs::exists(fullPath)) {
    uintmax_t size = fs::file_size(fullPath);
    std::time_t mtime = fs::last_write_time(fullPath);
}

// Directory iteration
for (auto &entry : fs::directory_iterator(incomingDir)) {
    if (entry.path().extension() == ".part")
        processPart(entry.path());
}

// Safe file removal
boost::system::error_code ec;
fs::remove(fullPath, ec);   // ec instead of exception — choose per call-site
```

**Why it's better:**
- Path concatenation with `/` operator handles separators correctly on all platforms
- `fs::exists`, `fs::file_size`, `fs::last_write_time` replace manual Win32 API calls
- Recursive directory operations (`fs::remove_all`, `fs::copy`) in one call
- Strongly typed `fs::path` prevents mixing raw strings and paths
- UTF-8 / UTF-16 path encoding handled transparently

---

## MEDIUM — Time & Timers (40+ files)

### Problem

`GetTickCount()` has a known 49.7-day wrap-around bug. It is used as the primary
timestamp source:

```cpp
// ClientCredits.cpp:51
m_dwSecureWaitTime = m_dwUnSecureWaitTime = ::GetTickCount();

// UploadQueue.cpp:74,85,112
m_dwRemovedClientByScore(::GetTickCount())
VERIFY((h_timer = ::SetTimer(NULL, 0, SEC2MS(1)/10, UploadTimer)) != 0);
const DWORD curTick = ::GetTickCount();
```

Custom performance counter wrapper in `TimeTick.h:11-35`:

```cpp
class CTimeTick
{
    static __int64 m_nPerformanceFrequency;
    LARGE_INTEGER  m_nTime;

public:
    void  Start();
    float Tick();
    static bool isPerformanceCounter() { return m_nPerformanceFrequency != 0; }
};
```

### Solution: Boost.Chrono + Boost.Asio Timers

```cpp
#include <boost/chrono.hpp>
#include <boost/timer/timer.hpp>
#include <boost/asio/steady_timer.hpp>

// Replace GetTickCount() — no wrap, type-safe
auto now = boost::chrono::steady_clock::now();
auto elapsed = boost::chrono::duration_cast<boost::chrono::milliseconds>(
    boost::chrono::steady_clock::now() - startTime);
uint64_t ms = elapsed.count();

// Duration arithmetic is typed — no accidental ms/s mix-ups
auto timeout = boost::chrono::seconds(30);
if (elapsed > timeout) { /* expired */ }

// Replace SetTimer() + UploadTimer callback
boost::asio::steady_timer uploadTimer(io_ctx,
    boost::chrono::milliseconds(SEC2MS(1) / 10));
uploadTimer.async_wait([](boost::system::error_code ec) {
    if (!ec) UploadTimerTick();
});

// Replace CTimeTick entirely
boost::timer::cpu_timer t;
t.start();
// ... work ...
auto ns = t.elapsed().wall;   // nanoseconds, wall-clock
auto cpu = t.elapsed().user;  // nanoseconds, CPU time
```

**Why it's better:**
- `steady_clock` never wraps and never goes backward — fixes the 49-day bug permanently
- Durations are typed (`milliseconds`, `seconds`) — unit mismatches are compile errors
- `boost::asio::steady_timer` integrates with the same `io_context` as the sockets
- `boost::timer::cpu_timer` replaces `CTimeTick` with more precision and zero custom code

---

## MEDIUM — Circular Buffer

### Problem

`ring.h:19-113` contains a 100-line custom `CRing<T>` template with manual pointer
arithmetic over a heap-allocated array:

```cpp
// ring.h:24-50
template<class TYPE> class CRing
{
    UINT_PTR  m_nCount;
    UINT_PTR  m_nIncrement;
    UINT_PTR  m_nSize;
    TYPE     *m_pData;
    TYPE     *m_pEnd;
    TYPE     *m_pHead;
    TYPE     *m_pTail;

    void AddTail(const TYPE &newElement);
    void RemoveAll();
    void RemoveHead();
    // ... ~100 lines of manual index/wrap management
};

// UploadQueue.cpp:64
: average_ur_hist(512, 512)
, activeClients_hist(512, 512)
```

### Solution: boost::circular_buffer

```cpp
#include <boost/circular_buffer.hpp>

// Replace CRing<TransferredData>
boost::circular_buffer<TransferredData> average_ur_hist(512);
boost::circular_buffer<uint32_t>        activeClients_hist(512);

// Usage is identical to std::deque
average_ur_hist.push_back(newSample);
auto oldest = average_ur_hist.front();
average_ur_hist.pop_front();

// Full when at capacity — automatically overwrites oldest
// (CRing behaviour is preserved)
```

**Why it's better:**
- 100 lines of custom code → 1 include + 1 type alias
- Pre-tested edge cases (empty, full, single-element)
- Exception-safe; no raw `new`/`delete`
- Iterators compatible with standard algorithms (`std::accumulate`, `std::copy`)

---

## MEDIUM — Error Handling (35+ files)

### Problem

Error reporting relies on `GetLastError()` / `WSAGetLastError()` with manual string
formatting:

```cpp
// EMSocket.h:147
static int GetLastError() { return WSAGetLastError(); }

// UploadQueue.cpp:87
AddDebugLogLine(true, _T("Failed to create 'upload queue' timer - %s"),
                (LPCTSTR)GetErrorMessage(::GetLastError()));
```

Error codes are plain `int` — no type safety, no association with their message strings.

### Solution: Boost.System

```cpp
#include <boost/system/error_code.hpp>
#include <boost/system/system_error.hpp>

// Operations return error_code instead of raw int
boost::system::error_code ec;
socket.connect(endpoint, ec);
if (ec) {
    // ec.message() returns human-readable string automatically
    LogLine("Connect failed: %s", ec.message().c_str());
    return;
}

// Or throw on error
if (ec)
    throw boost::system::system_error(ec, "connect");

// WSA errors are in the system category on Windows
boost::system::error_code wsaEc(WSAGetLastError(),
                                boost::system::system_category());
LogLine("WSA error: %s", wsaEc.message().c_str());
```

**Why it's better:**
- `error_code` carries both the code and the category (POSIX / Win32 / Asio)
- `.message()` is automatic — no `GetErrorMessage()` helper needed
- Integrates natively with Boost.Asio (all async ops return `error_code`)
- Type-safe: Win32 codes, WSA codes, and custom codes are distinguishable

---

## MEDIUM — Logging

### Problem

`Log.h` implements a custom `CLogFile` class with a raw `FILE*`, manual rotation logic,
and a hand-rolled priority enum:

```cpp
// Log.h
enum EDebugLogPriority : int {
    DLP_VERYLOW = 0, DLP_LOW, DLP_DEFAULT, DLP_HIGH, DLP_VERYHIGH
};

class CLogFile
{
public:
    bool IsOpen() const { return m_fp != NULL; }
    bool Create(LPCTSTR pszFilePath, UINT uMaxFileSize = 1024 * 1024, ...);
    bool Log(LPCTSTR pszMsg, int iLen = -1);

private:
    FILE   *m_fp;
    CString m_strFilePath;
};
```

### Solution: POCO::Logger or Boost.Log

**Option A — POCO::Logger (simpler API):**
```cpp
#include <Poco/Logger.h>
#include <Poco/FileChannel.h>
#include <Poco/PatternFormatter.h>
#include <Poco/FormattingChannel.h>
#include <Poco/AutoPtr.h>

// Setup (once at startup)
Poco::AutoPtr<Poco::FileChannel> fileChannel(new Poco::FileChannel("emule.log"));
fileChannel->setProperty("rotation", "1 M");      // auto-rotate at 1 MB
fileChannel->setProperty("archive", "timestamp");

Poco::AutoPtr<Poco::PatternFormatter> fmt(
    new Poco::PatternFormatter("%Y-%m-%d %H:%M:%S [%p] %t"));
Poco::AutoPtr<Poco::FormattingChannel> fmtChannel(
    new Poco::FormattingChannel(fmt, fileChannel));

Poco::Logger::root().setChannel(fmtChannel);
Poco::Logger::root().setLevel("information");

// Usage (thread-safe, replaces AddLogLine / AddDebugLogLine)
Poco::Logger &log = Poco::Logger::get("emule");
log.information("Server connected");
log.warning("Upload queue full");
log.error("Failed to bind socket on port %hu", port);
```

**Option B — Boost.Log (more powerful, heavier):**
```cpp
#include <boost/log/trivial.hpp>
#include <boost/log/sinks/text_file_backend.hpp>
#include <boost/log/utility/setup/file.hpp>
#include <boost/log/utility/setup/console.hpp>

// Setup
boost::log::add_file_log(
    boost::log::keywords::file_name = "emule_%N.log",
    boost::log::keywords::rotation_size = 1 * 1024 * 1024,
    boost::log::keywords::format = "[%TimeStamp%] [%Severity%] %Message%"
);

// Usage
BOOST_LOG_TRIVIAL(info)    << "Server connected";
BOOST_LOG_TRIVIAL(warning) << "Upload queue full";
BOOST_LOG_TRIVIAL(error)   << "Failed to bind socket on port " << port;
```

**Why it's better:**
- Thread-safe logging — no mutex needed around `CLogFile::Log()`
- Automatic file rotation — no manual size tracking
- Multiple sinks simultaneously (file + console + remote)
- Lazy evaluation — format string is not evaluated if level is filtered out
- Structured log levels map directly to existing `EDebugLogPriority` values

---

## LOW — Regular Expressions

### Problem

`std::basic_regex<TCHAR>` is used in `OtherFunctions.cpp:3271-3290`. Some MSVC
implementations of `std::regex` use a backtracking algorithm with worst-case O(2^n)
behaviour on adversarial input:

```cpp
// OtherFunctions.cpp:3271-3290
bool IsRegExpValid(const CString &regexpr)
{
    try {
        std::basic_regex<TCHAR> reFN(regexpr);
    } catch (const std::regex_error&) {
        return false;
    }
    return true;
}

bool RegularExpressionMatch(const CString &regexpr, const CString &teststring)
{
    try {
        std::basic_regex<TCHAR> reFN(regexpr);
        // match logic ...
    } catch (const std::regex_error&) {
        return false;
    }
}
```

### Solution: Boost.Regex

```cpp
#include <boost/regex.hpp>

bool IsRegExpValid(const std::string &regexpr)
{
    try {
        boost::regex re(regexpr);
        return true;
    } catch (const boost::regex_error &) {
        return false;
    }
}

bool RegularExpressionMatch(const std::string &regexpr, const std::string &input)
{
    try {
        boost::regex re(regexpr);
        return boost::regex_search(input, re);
    } catch (const boost::regex_error &) {
        return false;
    }
}
```

**Why it's better:**
- Boost.Regex uses a non-backtracking DFA/NFA hybrid for predictable performance
- Better Unicode support options (`boost::wregex`, `boost::u32regex`)
- More syntax options (Perl, POSIX extended, ECMAScript)
- Note: if using C++17 with a modern standard library, `std::regex` may be sufficient

---

## LOW — Configuration Parsing

### Problem

`Preferences.h` uses `#pragma pack` binary structs for on-disk settings serialization:

```cpp
// Preferences.h:76-127
#pragma pack(push, 1)
struct Preferences_Ext_Struct
{
    uint8  version;
    uchar  userhash[16];
    WINDOWPLACEMENT EmuleWindowPlacement;
};
#pragma pack(pop)

struct EmailSettings {
    CString sServer;
    CString sFrom;
    CString sTo;
    uint16  uPort;
    TLSmode uTLS;
};

struct ProxySettings {
    CString host;
    uint16  type;
    bool    bUseProxy;
};
```

### Solution: Boost.PropertyTree (INI) or POCO::IniFileConfiguration

**Boost.PropertyTree:**
```cpp
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

boost::property_tree::ptree cfg;
boost::property_tree::read_ini("emule.ini", cfg);

// Read values with defaults
std::string server  = cfg.get<std::string>("email.server", "");
uint16_t    port    = cfg.get<uint16_t>("email.port", 25);
bool        useTls  = cfg.get<bool>("email.tls", false);
std::string proxyHost = cfg.get<std::string>("proxy.host", "");

// Write back
cfg.put("email.server", newServer);
boost::property_tree::write_ini("emule.ini", cfg);
```

**POCO::IniFileConfiguration:**
```cpp
#include <Poco/Util/IniFileConfiguration.h>

Poco::AutoPtr<Poco::Util::IniFileConfiguration> cfg =
    new Poco::Util::IniFileConfiguration("emule.ini");

std::string server = cfg->getString("email.server", "");
int         port   = cfg->getInt("email.port", 25);
bool        useTls = cfg->getBool("email.tls", false);
```

**Why it's better:**
- Human-readable INI format — users can edit settings with a text editor
- No binary compatibility issues between versions
- Eliminates `#pragma pack` structs (which are endian/alignment dependent)
- Type-safe get with defaults — no manual null checks or sscanf parsing

---

## LOW — Cryptography

### Problem

The codebase already uses **Crypto++** (CryptoPP) for MD4 and MD5:

```cpp
// EmuleMD4.h:34-47
class CMD4
{
    CryptoPP::Weak1::MD4 m_md4;
    MD4 m_hash;
public:
    void Reset();
    void Add(LPCVOID pData, size_t nLength);
    void Finish();
    const byte* GetHash() const;
};

// MD5Sum.h:35-50
class MD5Sum
{
public:
    MD5Sum();
    explicit MD5Sum(const CString &sSource);
    void Calculate(const byte *pachSource, size_t nLength);
    CString GetHashString() const;
    const byte* GetRawHash() const { return m_hash.b; }
};
```

### Assessment

**Do not replace CryptoPP** unless you are actively removing it as a dependency.
CryptoPP is a mature, audited library and the existing wrappers are thin.

However, if the goal is to consolidate dependencies, **POCO::Crypto** can replace it:

```cpp
#include <Poco/MD5Engine.h>
#include <Poco/DigestStream.h>

Poco::MD5Engine md5;
md5.update(data, length);
std::string hash = Poco::DigestEngine::digestToHex(md5.digest());
```

For **UUID generation** (if adding new unique ID requirements):
```cpp
#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>

boost::uuids::random_generator gen;
boost::uuids::uuid id = gen();
std::string idStr = boost::uuids::to_string(id);
```

---

## Summary Table

| Priority | Category | Current Technology | Boost/POCO Replacement | Files Affected |
|----------|----------|-------------------|------------------------|---------------|
| **CRITICAL** | Async Networking | `CAsyncSocketEx` (custom WinSock) | **Boost.Asio** | 71+ |
| **CRITICAL** | Async DNS | `m_hAsyncGetHostByNameHandle` | `boost::asio::ip::tcp::resolver` | 20+ |
| **CRITICAL** | UDP packet queues | `CTypedPtrList` + `CCriticalSection` | Boost.Asio + `std::queue` | 10+ |
| **HIGH** | Mutexes | `CCriticalSection` / `Lock/Unlock` | `boost::mutex` + `boost::lock_guard` | 15+ |
| **HIGH** | Thread lifecycle | `CWinThread` + `HANDLE` events | `boost::thread` + `boost::condition_variable` | 8+ |
| **HIGH** | TLS mutex wrappers | Manual `InitializeCriticalSection` | `boost::mutex` unified | 1 |
| **HIGH** | Smart pointers | Raw `new`/`delete`, `char*` chains | `std::unique_ptr`, `std::shared_ptr` | Extensive |
| **HIGH** | Strings | `CString`, `sprintf`, fixed buffers | `std::string`, `boost::format`, `boost::algorithm` | 50+ |
| **MEDIUM** | File paths | `CFile`, `CString` path concat | `boost::filesystem` | 40+ |
| **MEDIUM** | Timers | `GetTickCount`, `SetTimer` | `boost::chrono`, `boost::asio::steady_timer` | 40+ |
| **MEDIUM** | Performance timing | Custom `CTimeTick` | `boost::timer::cpu_timer` | 1 |
| **MEDIUM** | Circular buffer | Custom `CRing<T>` (100 lines) | `boost::circular_buffer<T>` | 2 |
| **MEDIUM** | Error codes | `GetLastError`, `WSAGetLastError` | `boost::system::error_code` | 35+ |
| **MEDIUM** | Logging | Custom `CLogFile` + `FILE*` | **POCO::Logger** or **Boost.Log** | 1 |
| **LOW** | Regex | `std::basic_regex<TCHAR>` | `boost::regex` | 1 |
| **LOW** | Config | `#pragma pack` binary structs | `boost::property_tree` / POCO INI | 1 |
| **LOW** | UUIDs | — | `boost::uuids::random_generator` | New code |
| **LOW** | Crypto | CryptoPP (already integrated) | POCO::Crypto (only if removing CryptoPP) | 3+ |

---

## Migration Strategy

### Phase 1 — Safety (Low Risk, High Value)

These changes are mechanical and localized. Do them first to establish safe patterns.

1. **Replace `CCriticalSection` → `boost::mutex` + `boost::lock_guard`**
   - Files: `EMSocket.h`, `UDPSocket.h`, `UploadBandwidthThrottler.h`, `UploadQueue.h`, `GDIThread.h`
   - Each replacement is 1–3 lines; no logic change required

2. **Replace raw `new`/`delete` → `std::unique_ptr` / `std::shared_ptr`**
   - Start with `WebSocket.h` (clear ownership chain) and `EncryptedStreamSocket.h`
   - Use `make_unique` / `make_shared` at construction sites

3. **Replace `GetTickCount` → `boost::chrono::steady_clock::now()`**
   - Files: `ClientCredits.cpp`, `UploadQueue.cpp` and all callers
   - Define a `using TickMs = boost::chrono::milliseconds` alias for brevity

### Phase 2 — Architecture (Medium Risk, High Value)

4. **Replace `CAsyncSocketEx` → Boost.Asio**
   - This is the largest change. Approach:
     - Introduce `io_context` as a singleton or dependency-injected service
     - Port `CUDPSocket` first (simpler than TCP)
     - Port `CListenSocket` / `CServerSocket` next
     - Port `CEMSocket` last (most complex — handles eMule stream protocol)
   - Keep `CAsyncSocketEx` alive in parallel during transition; compile both

5. **Replace `CWinThread` + `HANDLE` events → `boost::thread` + `boost::condition_variable`**
   - `CGDIThread`, `CPartFileWriteThread`, `CUploadBandwidthThrottler`
   - The Asio `io_context::run()` thread model may subsume some of these

6. **Replace `CString` in new and refactored code → `std::string`**
   - Do not do a bulk replace; migrate path-by-path as files are touched
   - Add conversion helpers `toStd(const CString&)` / `toCStr(const std::string&)` for interop

### Phase 3 — Polish (Low Risk, Low-Medium Value)

7. **Replace `CFile` / path strings → `boost::filesystem::path`**
8. **Replace `CLogFile` → POCO::Logger**
9. **Replace `CRing<T>` → `boost::circular_buffer<T>`**
10. **Replace `Preferences` binary struct → `boost::property_tree` INI**

---

*Generated by analysis of the full `srchybrid` codebase (611 files). See also: `../history/audits/HIST-ARCH-THREADING.md`, `../history/audits/HIST-ARCH-NETWORKING.md`, `IDEA-MODERNIZATION-2026.md`.*
