# eMuleBB Troubleshooting Guide

Troubleshooting should start by collecting evidence, then changing the smallest
setting that explains the symptom. eMuleBB keeps the classic desktop app
model: the live state belongs to the app, while REST and companion tools observe
or request native state changes.

## Evidence First

Collect the support artifact that matches the problem:

| Problem area | Useful evidence |
|---|---|
| Network and Low ID | logs, port test output, firewall state, bind target |
| Kad | Kad state, UDP port state, bootstrap source, firewall and UPnP evidence |
| Sharing and startup | shared-cache state, hash queue, share roots, long-path state |
| Upload performance | upload cap, slot target, slow-slot state, queue and IO diagnostics |
| REST/controllers | WebServer state, bind/port, API key, OpenAPI route, controller logs |
| VPN/interface binding | bind target, resolved bind state, selected local address, route/firewall state |
| UPnP/NAT | P2P UPnP state, WebServer UPnP state, backend mode, router mapping |
| Completion automation | command setting, program path, arguments, completed filename, app log |
| Crashes or hangs | mini dump for crashes, full dump for hangs or memory growth |

Prefer redacted diagnostic snapshots for support. Use raw snapshots only when
the recipient is trusted and the data sensitivity is understood.
The [Diagnostics Guide](GUIDE-DIAGNOSTICS.md) explains snapshot field families,
dump types, unsafe diagnostic REST routes, startup profiling traces, and the
headless media metadata diagnostic command.

## Public Test Report Checklist

When reporting a nightly, RC, or package problem, include enough context for the
failure to be repeated:

- package name or release tag, architecture, and whether it was a nightly, RC,
  or stable package
- Windows version and whether the run was x64 or ARM64
- profile type: disposable, copied real profile, or live-wire real profile
- launch command, including `-c` when an explicit profile path was used
- exact repro steps and whether a clean retry reproduces the problem
- relevant app logs, controller logs, package logs, diagnostic snapshots, or
  dumps
- REST method, route, status code, request body, and response body for API
  failures

Use [Product Guide](GUIDE-EMULEBB.md) for the repeatable public testing flow and
[Setup Guide](GUIDE-SETUP.md) for profile isolation before deeper diagnosis.

## General Triage Rules

- Change one setting at a time.
- Keep notes about the original value.
- Prefer app logs and diagnostic snapshots over memory of what happened.
- Separate P2P network issues from controller/WebServer issues.
- Separate local profile/disk issues from public network behavior.
- Do not diagnose frozen legacy surfaces as release-blocking behavior.

If the issue began after a package or profile change, confirm the setup path in
[Setup Guide](GUIDE-SETUP.md) before changing network settings.

## Low ID Recipe

Low ID normally means the TCP listener is not reachable from the eD2K server.

1. Confirm eMuleBB is connected to an eD2K server.
2. Confirm the configured TCP port in `Preferences > Connection`.
3. Check Windows Firewall rules for that port and executable.
4. Check router/NAT forwarding or P2P UPnP mapping.
5. If bind settings are configured, confirm the resolved bind address is the
   intended interface/address.
6. Run the port test after firewall/router changes.
7. Reconnect to a trusted server and check whether the ID changes.

Do not fix Low ID by changing unrelated upload, search, or IP-filter settings.

## Kad Firewalled Recipe

Kad firewall state depends primarily on UDP reachability and Kad bootstrap
health.

1. Confirm Kad is enabled and started.
2. Confirm the UDP port in `Preferences > Connection`.
3. Check Windows Firewall and router/NAT forwarding for UDP.
4. Check P2P UPnP only after confirming the selected bind path.
5. Bootstrap from trusted nodes or known peers.
6. Recheck Kad firewall state after the network has settled.
7. If UDP remains blocked, compare with Low ID state to determine whether only
   UDP is affected.

Kad may need time after bootstrap before state is meaningful. Avoid repeatedly
restarting it during the first minutes of diagnosis.

## No Search Results Recipe

No results can come from network state, query shape, filter policy, or search
method.

1. Confirm eD2K and/or Kad are connected.
2. Try a broad, ordinary query with the intended search method.
3. Confirm the selected search type and search method.
4. Check whether IP filtering is enabled and has an unexpectedly aggressive
   rule set.
5. Check logs for parse errors, server errors, or Kad search warnings.
6. Compare local desktop search with REST/controller search if automation is
   involved.
7. If controller search fails but desktop search works, inspect the REST route,
   method, body, and OpenAPI contract.

Search result trust signals are hints, not proof. Use filename, size,
availability, comments, and source consistency together.

## Slow Startup Or Hashing Recipe

Large libraries can make startup look slow when the app is scanning,
validating cache state, or hashing.

1. Confirm shared roots are intentional and reachable.
2. Check whether a network share or removable drive is slow or unavailable.
3. Check `shareignore.dat` for broad or incorrect rules.
4. Let hashing and scanning settle before forcing a rescan.
5. Check shared startup cache behavior in
   [Sharing Guide](GUIDE-SHARING.md).
6. Check long path state if deep paths are present.
7. Delete cache sidecars only when intentionally forcing a clean rebuild.

If startup is slow only once after a profile move or package upgrade, allow the
derived caches to rebuild before treating it as a regression.

For developer or local release builds, use the `EMULE_STARTUP_PROFILE`
environment switch from the [Diagnostics Guide](GUIDE-DIAGNOSTICS.md) to create
`startup-profile.trace.json`. It separates app startup phases, shared-cache
validation, hashing, and upload-budget setup more clearly than the ordinary
log.

If the profile uses monitored shares, confirm the monitored roots are stable
and narrow. Watcher churn can look like startup/cache trouble when another tool
is constantly creating, renaming, or deleting files under a monitored root.

## Slow Upload Or Queue Recipe

Upload performance should be diagnosed through the broadband upload policy, not
through stock-era assumptions about unlimited slot growth.

1. Confirm the configured upload cap.
2. Check active upload slot count and slot target behavior.
3. Check whether slow or zero-rate slots are being recycled after warm-up,
   grace, and cooldown windows.
4. Check disk and CPU load before blaming peers.
5. Check whether IP filters or firewall rules are removing many peers.
6. Compare a longer operating window rather than a single short observation.

Changing many queue, slot, and source limits together makes the result hard to
interpret. Change one policy area at a time.

## Disk-Space Protection Recipe

When disk-space protection triggers, eMuleBB is protecting profile and part
file integrity.

1. Identify the breached volume in logs.
2. Check config, temp, incoming, and category incoming volumes.
3. Free space on the volume or move paths deliberately.
4. Confirm temp and incoming directories are still reachable.
5. Let part metadata save complete before restarting downloads.
6. Resume downloads only after the effective floor and completion demand are
   satisfied.

Do not lower free-space floors to zero to force progress. See
[Downloads and Search Guide](GUIDE-DOWNLOADS-SEARCH.md) for the floor model.

## REST Or Controller Failure Recipe

REST failures should be split into listener, authentication, route, lifecycle,
and adapter problems.

1. Confirm WebServer/REST is enabled.
2. Confirm bind address, port, firewall, and allowed IP policy.
3. Confirm the API key or password path used by the controller.
4. Confirm the route exists in
   [OpenAPI](../rest/REST-API-OPENAPI.yaml).
5. Check whether the app is starting or shutting down.
6. Compare native `/api/v1` behavior with qBit/Torznab adapter behavior.
7. Capture request method, route, status code, response body, and logs.

The legacy HTML WebServer UI is frozen pending removal. Do not use legacy
template behavior as proof that REST is broken or supported.

## IP Filter Problem Recipe

IP filter problems usually come from disabled filtering, zero rules, a bad
provider list, or an overly aggressive level.

1. Confirm filtering is enabled.
2. Confirm `config\ipfilter.dat` exists.
3. Confirm the loaded rule count is not zero.
4. Confirm the filter level matches the selected list.
5. Use **Reload** after manual edits.
6. Temporarily disable filtering only long enough to isolate the symptom.
7. Restore a known-good list if a provider update caused the problem.

See [IP Filter Guide](GUIDE-IP-FILTERS.md).

## Completion Command Failure Recipe

Completion automation runs a configured external program after a download
finishes.

1. Confirm completion automation is enabled.
2. Confirm the configured executable exists.
3. Prefer a full path to a trusted local executable.
4. Confirm arguments match the program's expected syntax.
5. Check completed filename and path quoting.
6. Check app logs after the file completes.
7. Disable the command while diagnosing unrelated completion problems.

Do not use completion automation to run untrusted files from incoming folders.

## Crash Or Hang Recipe

For crashes:

1. Capture a mini dump.
2. Record what the app was doing.
3. Keep the relevant log files.
4. Preserve the profile state if the crash is reproducible.

For hangs or memory growth:

1. Capture a full dump.
2. Record uptime and active workload.
3. Record controller activity, sharing state, and network state.
4. Avoid killing the process until evidence is collected when practical.

## Media Metadata Diagnostic Recipe

Use the headless metadata diagnostic when preview or media metadata extraction
behaves differently across machines:

```powershell
emulebb.exe --diagnose-media-metadata --input C:\Media\sample.mkv --output C:\Temp\metadata.json
```

The output uses `emulebb.mediaMetadataDiagnostic.v1` and includes the input
path. Review it before sharing publicly.

## Frozen Legacy Surfaces

The following areas are intentionally frozen and are not release-gated support
surfaces:

- archive preview and archive recovery
- IRC and IRC-adjacent chat UI
- legacy Scheduler and scheduler preferences
- SMTP/email notifications
- SAPI text-to-speech notifications
- first-run connection wizard
- splash screen
- legacy WebServer HTML templates and page UI
- proxy support

If one of these surfaces fails, treat it as unsupported legacy behavior unless
the explicit task is removal or proving that removal did not damage supported
behavior.

## Related Guides

- [Product Guide](GUIDE-EMULEBB.md)
- [Setup Guide](GUIDE-SETUP.md)
- [Network Guide](GUIDE-NETWORK.md)
- [Sharing Guide](GUIDE-SHARING.md)
- [Downloads and Search Guide](GUIDE-DOWNLOADS-SEARCH.md)
- [Controllers and REST Guide](GUIDE-CONTROLLERS-REST.md)
- [IP Filter Guide](GUIDE-IP-FILTERS.md)
- [Long Path Guide](GUIDE-LONGPATHS.md)
