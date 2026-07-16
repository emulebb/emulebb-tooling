# Rust Soak Upload/Download Gap Analysis

Owner: RUST-FEAT-033 release-gate soak evidence.

Purpose: keep a commit-safe record of the current Rust soak investigation into
upload/download performance gaps versus the MFC witness. This file intentionally
excludes machine-local paths, process IDs, VPN-provider local settings, public
server endpoints, media titles, and raw live-session logs.

## Current Working Conclusions

The regular Rust soak has reached a healthy connected state during the current
investigation:

- ED2K connects with High ID when a reachable server is selected.
- Kad connects and continues publishing.
- VPN Guard allow-list checks pass before the live profile is treated as valid.
- Rust has produced active upload samples above the synthetic MFC fixture
  baseline, so the upload pipe is not obviously capped below MFC.
- Early zero-upload samples are not actionable while ED2K visibility is still
  low and no waiting demand exists.

The likely risk area is discoverability and request admission, not raw socket
throughput.

## Gap Ledger

**ED2K visibility ramp**

Current outcome: understood. Rust matches MFC's 200-file offer cap and
one-minute cadence, so large catalogs need hours to become fully visible.

Next action: keep soaking. Treat low upload as non-actionable before high ED2K
visibility unless publishing stalls.

**Kad source visibility maturity**

Current outcome: open. Source publishing is paced and may lag ED2K visibility
for large catalogs.

Next action: analyze the Kad source publish scheduler and compare against
MFC/Kad behavior.

**Server startup and fallback**

Current outcome: partially mitigated. A single fixed server can make Rust look
broken when the server is unreachable.

Next action: keep fallback/server-walk parity under review; do not rely on one
public server as proof.

**Upload request admission**

Current outcome: open. MFC directly admits valid requesters when capacity
exists.

Next action: compare Rust handling of filename, file-id, start-upload, and
request-parts flows against MFC.

**Source exchange compatibility**

Current outcome: known product decision. Rust is SX2-only under workspace
policy, but legacy SX1 traffic can still affect live source propagation.

Next action: measure live inbound source-exchange requests in diagnostics mode
if download/source discovery remains weak.

**MFC baseline strength**

Current outcome: weak baseline. The current MFC fixture proves serving behavior
but not public discoverability at Rust catalog scale.

Next action: capture or define a stronger MFC comparison only after Rust
visibility is mature.

## Gap 1: ED2K Visibility Ramp

Outcome: understood; no Rust code defect identified yet.

Rust's ED2K server publish path intentionally sends one bounded
`OP_OFFERFILES` batch, then waits before sending the next batch:

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_server/startup.rs`
  defines `MAX_OFFER_FILES_PER_ADVERTISEMENT = 200`.
- `send_offer_files_advertisement` builds one offer batch, advances the session
  cursor, marks the batch's hashes as published in the session, and records
  publish diagnostics.
- `repos/emulebb-rust/crates/emulebb-core/src/lib.rs` runs the queued shared
  catalog publisher with a two-second debounce and a 60-second minimum interval.
- After a successful partial publish that has not wrapped the catalog, the core
  marks the catalog dirty again so the next batch is sent after the interval.
- If the server is unavailable, the dirty flag remains set and the publisher
  retries after the not-connected delay.

MFC uses the same effective throttle:

- `workspaces/workspace/app/emulebb-main/srchybrid/ServerConnect.cpp` clears
  ED2K publish state and sends the first shared-file list immediately after
  server connect.
- `workspaces/workspace/app/emulebb-main/srchybrid/SharedFileList.cpp`
  `SendListToServer` uses the connected server's soft file limit, falling back
  to 200 when the limit is unknown or too large.
- MFC marks sent files as ED2K-published, then `Process` calls
  `SendListToServer` again every `ED2KREPUBLISHTIME`, which is one minute, while
  files remain unpublished or republish-pending.

Therefore, for a large shared catalog, the visibility slope itself is expected.
At 200 files per minute, a catalog with roughly 64k files needs roughly 320
batches, or more than five hours, before one connected ED2K server has seen the
whole catalog.

## Gap 1 Risk Notes

Rust's order is more dynamic than MFC's simple unpublished-file loop. Rust
re-ranks the catalog using upload/request stats and last ED2K publish time while
also carrying a session-local cursor and published-hash set. Existing Rust tests
cover the important static cases:

- large libraries rotate across batches;
- unpublished hashes are prioritized;
- late new hashes are found;
- fully published catalogs restart cleanly.

The dynamic ranking can change which pending files are sent first, but it should
not strand a large portion of the catalog because the batch builder scans until
it fills with unpublished hashes or exhausts the catalog.

## Gap 1 Decision Rule

Do not change the 200-file, one-minute behavior without separate protocol
justification. It matches the MFC witness and is gentle to public servers.

Use these soak rules:

- Below 90% ED2K visibility, do not classify low/zero upload as an upload-path
  bug unless waiting demand exists or ED2K publishing stalls.
- At or above 90% visibility, repeated zero waiting uploads and zero active
  uploads should move the investigation to discovery, advertised metadata, and
  source-publishing reach.
- If pending entries remain high and published entries stop increasing at the
  expected cadence, investigate the queued publisher and background server
  publish request path.

## Monitoring Caveat

Use the current regular Rust parity-watch output when assessing this soak.
Older live-watch output from a previous run can be stale and should not be mixed
into current status conclusions.
