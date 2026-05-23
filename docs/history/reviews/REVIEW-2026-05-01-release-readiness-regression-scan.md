---
id: REVIEW-2026-05-01-release-readiness-regression-scan
title: Release readiness regression scan after broadband stabilization slices
date: 2026-05-01
scope: eMule-main main from 10a6c20 through 6697302
---

# Release Readiness Regression Scan

This scan reviewed the current `eMule-main` `main` delta from `10a6c20`
through `6697302` with emphasis on release regressions, silent failure paths,
thread/message boundaries, and the new GitHub release update checker.

The reviewed delta is 45 app files, 1133 insertions, and 253 deletions. It
covers the recent `BUG-034` / `BUG-035` stabilization slices, quieter default
preferences, AVI upload-compression retirement, GitHub release update checks,
and eMule BB mod identity advertisement.

## Findings

### 1. Client UDP unknown exceptions are still verbose-gated

`srchybrid/ClientUDPSocket.cpp` still has a release `catch (...)` path that
converts unknown packet-processing exceptions into `"Unknown exception"` and
then only logs the event when verbose logging is enabled.

This is not a regression from the recent slices, but it is the best next
`BUG-034` / `BUG-035` release-silent-failure target because the path processes
external UDP input and already has enough packet metadata to produce a bounded
warning without changing packet-discard behavior.

Recommended slice:

- keep invalid or malformed packet diagnostics behind the existing verbose gate
- log unknown release exceptions unconditionally through the existing warning
  path
- add a tiny seam/test for the unknown-exception diagnostic policy if the
  logging decision is moved behind a helper

### 2. Release update tag parsing lacks an unsigned overflow guard

`srchybrid/ReleaseUpdateCheckSeams.h` parses `MAJOR.MINOR.PATCH` components by
multiplying and adding into `unsigned` without checking overflow. The current
tests cover strict shape, ordering, missing assets, malformed tags, prereleases,
and JSON parse failure, but not overflowed numeric components.

This is a small new hardening gap in an externally-fed parser. It is not likely
to block the release because the GitHub source is controlled, the parser is
bounded by the 512 KiB fetch cap, and malformed release tags are already
ignored. Still, before release it is cheap to reject overflowed components
explicitly and add one native seam test.

Recommended slice:

- reject component values that would exceed `std::numeric_limits<unsigned>::max()`
- add a test for `emule-bb-v42949672960.0.0` or equivalent overflow
- keep the public release-tag grammar unchanged

### 3. Version-check worker lifecycle is acceptable, with one exit-race note

`srchybrid/EmuleDlg.cpp` now runs the GitHub update check on a background MFC
thread and posts an owned result object back to the dialog. The worker deletes
the result if `PostMessage` fails, and the UI handler takes ownership with
`std::unique_ptr`. The network operation is bounded by 7-second WinINet
timeouts and a 512 KiB JSON cap, so the UI thread is not blocked.

The remaining edge is shutdown timing: if the dialog is destroyed after a
successful post but before the message is handled, there is no explicit drain
or cancellation path for the posted result. That would be at worst a bounded
one-result exit leak/stale queued state, not a runtime correctness blocker.
This is lower priority than the UDP diagnostics and release-tag overflow guard.

### 4. Legacy WebServer synchronous UI messages remain a watchpoint

The recent WebServer stabilization slices did not introduce a clear new
regression in the reviewed diff. However, the legacy web request path still has
many synchronous `SendMessage` calls into the UI thread. Some of these are
intentional and depend on stack-owned data remaining valid during a synchronous
call.

This remains a broader concurrency watchpoint, not a release blocker discovered
by this scan. Avoid mixing it into the release unless a narrow hang/crash
reproduction appears.

## Green Checks

- `ServerSocket` packet failure handling now uses explicit recover-or-disconnect
  policy seams and did not show a regression in the reviewed slice.
- `ClientCredits` secure-ident hardening keeps oversized buffers and key-length
  failures explicit without changing the failed-ident result shape.
- Collection import ownership and malformed-entry handling now fail explicitly
  while preserving tolerant import behavior.
- Transfer window invalid view-state handling now has explicit fallback policy.
- The mod identity addition uses the standard `CT_MOD_VERSION` tag and updates
  display text through a focused helper; no protocol compatibility issue was
  found in this pass.
- Fresh-profile defaults are quieter: update notifications are opt-in,
  focus-stealing is disabled by default, preview side effects are reduced, and
  exit confirmation is disabled by default.
- `DontCompressAvi` retirement leaves upload compression policy hard-coded
  around non-compressible media/archive extensions rather than user preference
  state.

## REST Live Proof Addendum

The redesigned `/api/v1` REST surface was live-proved on 2026-05-01 with the
isolated Debug x64 REST smoke lane:

- report: `repos\emulebb-build-tests\reports\rest-api-smoke\20260501-154017-eMule-main-debug`
- command: `python repos\emulebb-build-tests\scripts\rest-api-smoke.py --workspace-root workspaces\v0.72a --configuration Debug --server-search-count 1 --kad-search-count 1 --enable-upnp --keep-artifacts`
- result: passed, including auth checks, resource-style REST surface checks,
  server connect/disconnect, Kad connect/disconnect, one server search, one Kad
  search, HTML root compatibility, and clean app shutdown

The live run exposed no REST contract rollback issue. It did expose Debug-only
automation blockers around startup/shutdown invariants: transfer-window primary
view initialization order, nullable Kad accessors that callers already guard,
branded eMule BB main-window detection in the live harness, and UI cleanup
paths touching already-destroyed tab/list controls during process teardown.
Those were fixed as release-stabilization work so the live REST lane can be
used as a real pre-release gate.

## Updated Risk Counters

Current app source scan results after `6697302`:

- `catch (...)`: 123 matches
- `ASSERT(0)`: 541 matches

These counts include legitimate invariants and low-risk compatibility fallbacks.
They support keeping `BUG-034` and `BUG-035` active as targeted stabilization
buckets, not launching a mechanical rewrite.

## Release Recommendation

Keep the broadband release moving. No reviewed change needs rollback.

Recommended implementation order:

1. `BUG-034` / `BUG-035`: harden the client UDP unknown-exception diagnostic.
2. `REF-025` update checker: reject overflowed release-version components and
   add the missing seam test.
3. Optional: document or guard the version-check posted-result lifecycle if
   shutdown testing exposes a practical leak or stale state.

Do not reopen the already-decided Wont-Fix or Deferred items from this scan.
