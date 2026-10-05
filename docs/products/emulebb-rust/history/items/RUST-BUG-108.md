---
id: RUST-BUG-108
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/34
title: Harden regular-build logging and retention
status: DONE
priority: Major
category: bug
labels: [rust, logging, reliability, observability]
milestone: post-beta-polish
created: 2026-10-05
source: 2026-10-05 operator logging audit and implementation request
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/34. This local document is retained as an engineering spec/evidence record.

# RUST-BUG-108 - Harden regular-build logging and retention

## Summary

Make regular daemon logging predictable and resilient: default console, REST,
and retained file output to INFO; honor one `RUST_LOG` policy; bound retained
state; and prevent noisy network paths or a slow/unavailable file sink from
disrupting the daemon.

## Findings Before Fix

- An unset `RUST_LOG` leaves the regular daemon console at ERROR while the REST
  buffer independently captures INFO and the NAT diagnostic tool defaults to
  INFO.
- The REST layer filters out DEBUG and TRACE before computing its `debug` flag.
- Regular logs are not retained across restarts, and the ten-second runtime
  summary plus malformed-packet paths are too noisy for a default INFO console.
- Logging initialization and the custom REST layer lack direct behavioral tests.

## Intended Shape

- Use one regular-daemon filter specification for human console output, the REST
  log buffer, and bounded daily JSONL files under the validated profile.
- Keep file delivery asynchronous and lossy under backpressure so logging cannot
  stall network workers; expose dropped-line and degraded-file-sink warnings.
- Apply a consistent level and field policy across every tracing call site in
  regular builds, keeping per-packet and per-attempt detail below INFO.
- Preserve the existing REST `LogEntry` schema while making its level and debug
  fields truthful and bounding retained message size and retrieval work.

## Scope Constraints

- Do not change packet-diagnostic schemas, dump writers, or
  `EMULEBB_RUST_LOG_DIR` behavior.
- Do not add persisted settings, profile migrations, or REST contract fields.
- Keep the NAT diagnostic tool out of this regular-build cleanup.
- Never retain credentials, private keys, raw payloads, search terms, or file
  names in regular logs.

## Acceptance Criteria

- [x] Missing, empty, or unusable `RUST_LOG` defaults all regular sinks to INFO;
      valid directives apply consistently to console, REST, and file output.
- [x] Daily JSONL files are written under `<profile>/logs`, retain no more than
      eight matching files, flush on normal shutdown, and degrade without
      blocking startup when unavailable.
- [x] REST DEBUG/TRACE records are retained only when enabled, carry a truthful
      `debug` flag, and remain bounded by entry count and message size.
- [x] INFO contains bounded lifecycle/operator events rather than periodic,
      per-attempt, or per-packet chatter.
- [x] Logging initialization, filtering, formatting, concurrency, retention,
      degraded operation, and REST projection have direct tests.
- [x] Regular Rust unit, policy, quality, and release-build gates pass.

## Implementation

- Replaced the daemon's standalone REST log layer with one regular logging
  module that applies the same `RUST_LOG` filter to console, REST, and file
  sinks and defaults an unset/empty filter to INFO.
- Added asynchronous daily JSONL output under `<profile>/logs`, an 8,192-line
  lossy queue, eight-file retention, dropped-line reporting, normal-shutdown
  flushing, and non-fatal file-sink initialization.
- Kept the REST contract stable while bounding the in-memory ring to 2,000
  records, messages to 4 KiB, and cloning to the requested result limit.
- Audited regular-build tracing callsites. Periodic summaries, protocol
  attempts, searches, callbacks, source acquisition, and per-packet details now
  remain below INFO; search terms, file names, and raw malformed-packet prefixes
  were removed from regular log events.
- Added machine-policy checks for the shared filters, INFO default, JSONL daily
  retention, bounded non-blocking writer, and REST limits. Operator behavior
  and `RUST_LOG` examples are documented in the repository README.

## Evidence

- Rust implementation commits: `emulebb/emulebb-rust@9977569a` and
  `emulebb/emulebb-rust@a6008790`.
- Focused daemon logging tests: 6 passed; focused REST log-buffer tests: 4
  passed, including direct JSONL, retention, degraded setup, Unicode truncation,
  and concurrent-writer coverage.
- `python tools/rust_quality_gate.py build` passed locked debug and release
  workspace builds and staged the release binaries and WebUI.
- `python tools/rust_quality_gate.py test-workspace` passed the complete regular
  Rust workspace unit, integration, and doc-test suite (excluding only the
  separately routed local Kad swarm tests).
- `python tools/rust_quality_gate.py fmt` and
  `python tools/rust_quality_gate.py clippy` passed; Clippy covered all workspace
  targets with warnings denied.
- `python tools/rust_quality_gate.py policy` passed from the committed clean
  tree, including all 50 policy-tool tests. The shared working copy's unrelated
  in-progress ED2K test still triggers the existing IPv4-only guard and was not
  modified or committed by this item.
- `cargo deny check advisories licenses sources` passed.

## Validation Scope

No live, soak, profile, packet-diagnostic behavior, NAT diagnostic behavior, or
MFC work was required. The repository's canonical build gate compiled its
required diagnostics artifact, but this item's implementation and audit were
limited to regular daemon logging.
