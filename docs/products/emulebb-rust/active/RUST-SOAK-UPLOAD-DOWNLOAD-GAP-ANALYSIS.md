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

Current outcome: understood as a parity-aligned ramp cost. Source publishing is
paced and may lag ED2K visibility for large catalogs.

Next action: keep monitoring source-publish progress and gate state. Investigate
only if source publishes stall while Kad is connected and the gate is allowed.

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

## Gap 2: Kad Source Visibility Maturity

Outcome: understood; no Rust code defect identified yet.

Kad source visibility is expected to mature more slowly than ED2K server
visibility for a large shared catalog. The Rust code intentionally mirrors the
MFC Kad source-store cadence and safety caps:

- `repos/emulebb-rust/crates/emulebb-core/src/kad_publish_schedule.rs`
  uses the stock Kad intervals:
  - source republish interval: 5 hours;
  - keyword republish interval: 24 hours;
  - notes republish interval: 24 hours.
- `repos/emulebb-rust/crates/emulebb-core/src/lib.rs` runs the shared-file Kad
  publish loop every 2 seconds.
- The same Rust loop inspects a bounded scan window, starts at most one new
  source publish per tick, and allows up to four source publishes in flight.
- The Rust DHT config reserves search capacity for non-publish work and applies
  a low publish packet budget so large-library publishing does not monopolize
  Kad traffic.
- Source publish admission records the source clock at start time, not after an
  ACK, matching MFC behavior. If a store cannot be created because the DHT is
  busy, Rust rolls the clock back for retry.

MFC has the same effective shape:

- `workspaces/workspace/app/emulebb-main/srchybrid/Opcodes.h` defines:
  - `KADEMLIAPUBLISHTIME = 2s`;
  - `KADEMLIATOTALSTORESRC = 4`;
  - `KADEMLIAREPUBLISHTIMES = 5h`.
- `workspaces/workspace/app/emulebb-main/srchybrid/SharedFileList.cpp`
  `Publish` selects one best-ranked due source file per source publish tick,
  only when total active store-source searches are below four.
- `workspaces/workspace/app/emulebb-main/srchybrid/KnownFile.cpp`
  `PublishSrc` advances the file's Kad source publish clock when the source
  store is admitted.
- If MFC cannot create the Kad store lookup, it resets the file's source publish
  clock so it can retry.

Therefore, source-publish totals can remain much lower than the ED2K published
count during a large-library startup soak. This is especially visible because
one source publish is one file, while a keyword publish can store many file IDs
under one keyword and an ED2K `OP_OFFERFILES` batch can carry up to 200 files.

## Gap 2 Live Interpretation

Use the source-publish counters as progress/gate evidence, not as a requirement
that Kad should keep pace with ED2K:

- Healthy signs:
  - Kad connected;
  - publish gate allowed;
  - source publish total increasing;
  - attempted contacts and ACKed contacts increasing;
  - low source failure count relative to attempts.
- Investigate if:
  - `kadGateAllowed` is false for repeated samples;
  - source due count is non-zero but source attempts stay at zero while active
    source publishes are below the cap;
  - source publish total stops increasing for several monitor windows;
  - source failures/timeouts dominate ACKed contacts.

The current MFC fixture baseline does not prove public Kad source visibility
because that fixture disables Kad and shares only a tiny local corpus. Use it
for upload serving behavior, not for Kad source-publish parity.

## Gap 2 Decision Rule

Do not loosen Kad publish caps just to make large-catalog startup look faster.
The current Rust caps match the MFC witness and are safer for the public Kad
network.

If upload/download demand remains weak after ED2K visibility matures, treat Kad
source maturity as one discovery factor, but debug it through gate/counter
evidence first. A code change is justified only if Rust is not starting source
publishes under the same conditions where MFC would, or if Rust's published
source tags are incompatible with the expected open, direct-UDP-callback, or
buddy-relay source forms.
