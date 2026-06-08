# eMuleBB Diagnostics Guide

This guide explains the support artifacts eMuleBB can produce and how to share
them safely. Use it with the symptom-led
[Troubleshooting Guide](GUIDE-TROUBLESHOOTING.md).

## Default Rule

Use redacted diagnostic snapshots for ordinary reports. Keep raw snapshots,
full dumps, API keys, private keys, and profile archives local unless the
recipient is trusted and the exposure is intentional.

Diagnostics can include enough information to reproduce a problem. That also
means they can expose local paths, network addresses, command-line arguments,
loaded modules, and controller configuration.

## Diagnostic Snapshots

The Tools menu can copy diagnostic snapshot JSON in two modes:

| Snapshot | Use |
|---|---|
| Redacted | Default support artifact for public issues and routine triage |
| Raw | Private operator artifact when exact paths, addresses, or command line are needed |

Snapshot data is organized by field families, not by one opaque text dump:

- process identity, command line, build, and runtime state
- profile, config, temp, incoming, log, and package paths
- bind/interface state and process TCP/UDP sockets
- adapter, server, Kad, firewall, and last firewall-repair state
- shared startup cache, startup hashing, and large-library readiness
- socket-buffer, I/O, and other runtime diagnostics useful for performance
  investigations
- loaded module names and paths

The I/O section reports Auto Broadband I/O state, the available physical RAM
used for adaptive download-buffer sizing, the adaptive global budget, effective
file-buffer allowance, total buffered download bytes, active buffered download
file count, and the largest buffered download file.

Redaction is best-effort support hygiene. It does not turn a diagnostic
snapshot into an anonymous public telemetry record. Review snapshots before
posting them to public trackers.

## Dumps

Diagnostic dumps capture process memory state:

| Dump | Use |
|---|---|
| Mini dump | Crashes and ordinary fault reports |
| Full dump | Hangs, memory growth, allocator problems, and difficult state corruption |

Full dumps can contain file names, paths, search text, URLs, API keys,
fragments of downloaded data, and other in-memory private data. Prefer mini
dumps unless the failure requires memory-state analysis.

For crashes, record the exact action, uptime, package build, profile type, and
recent controller activity. For hangs, capture the dump before killing the
process when practical.

## Unsafe Diagnostic REST

The REST API contains explicit diagnostic routes:

- `POST /api/v1/diagnostics/dumps`
- `POST /api/v1/diagnostics/crash-tests`

These routes are disabled unless diagnostic REST endpoints are explicitly
enabled in preferences. They also require confirmation fields in the request
body: `confirmDump: true` for dumps and `confirmCrash: true` for crash tests.

Use them only on localhost or a tightly controlled operator network. Do not
enable them for broad LAN, public, reverse-proxy, or Arr-controller exposure.
They are for release proof, automation harnesses, and controlled support
capture, not daily controller workflows.

These routes are intentionally stronger than ordinary diagnostics. A dump route
can write memory evidence that contains private in-process data, and a
crash-test route intentionally terminates the app. Keep the WebServer listener,
firewall rules, and controller proxying scoped so these routes cannot be
reached by Prowlarr, Radarr, Sonarr, a general LAN client, or the public
internet by accident.

## Startup Diagnostics Trace

Diagnostics release packages and explicit profiling builds can record a Chrome
Trace startup diagnostics. The profiling code is compile-time enabled, so no
runtime environment variable is required:

```powershell
emulebb-diagnostics.exe -c C:\eMuleBB-Profiles\slow-startup
```

The trace is written as `emulebb-diagnostics-startup.trace.json` in the active
profile `logs` directory. Open it with `chrome://tracing`, Perfetto, or another
Chrome Trace viewer.

Use this when a profile is slow before the normal UI feels usable, especially
with large shared libraries, monitored shares, broad IP filters, startup
hashing, or upload-budget initialization. The trace can include phase names,
timing, counters, and file/share/cache activity that are more precise than a
general log.

Privacy and availability rules:

- Treat the trace as private support evidence. It can reveal local paths,
  profile layout, shared-library shape, and startup timing.
- Prefer a disposable or copied profile when measuring a sensitive live
  library.
- Use the standard release package for ordinary launches when profiling traces
  are not needed.
- Standard public package builds strip diagnostics from the
  executable. If a support case needs it, use the paired diagnostics package.
  For local support builds, use the canonical diagnostics build command:

  ```powershell
  python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly --diagnostics
  ```

  The local diagnostics build enables all diagnostics flags and
  emits `emulebb-diagnostics.exe` so it is distinguishable from the standard
  `emulebb.exe`.

## Headless Media Metadata Diagnostic

The command line can probe maintained media metadata extractors and exit
without starting the desktop app:

```powershell
emulebb.exe --diagnose-media-metadata --input C:\Media\sample.mkv --output C:\Temp\metadata.json
```

Behavior:

- `--input <path>` is required.
- `--output <path>` is optional; without it, JSON is written to standard output.
- The output schema is `emulebb.mediaMetadataDiagnostic.v1`.
- The report includes the input path and file size.
- The command must not be combined with certificate generation or a positional
  link/command argument.

Use this when preview or metadata extraction fails, when optional media
libraries behave differently across machines, or when release proof needs a
small reproducible metadata artifact.

## What To Attach

For public issues:

1. Package name, architecture, and profile type.
2. Exact reproduction steps.
3. Relevant logs.
4. Redacted diagnostic snapshot.
5. Mini dump for a crash, if available.

For private maintainer investigations, add raw snapshots or full dumps only
when they directly answer a question that redacted artifacts cannot answer.
