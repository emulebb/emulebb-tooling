# eMuleBB Power User Manual

This guide is for a technically capable user who has never used eMule before.
It explains the mental model first, then the operating workflow. The goal is to
make eMuleBB predictable before you add a large profile, a large shared
library, a VPN, a controller, or Arr automation.

eMuleBB keeps classic eMule behavior where it matters: eD2K/Kad compatibility,
direct peer transfers, queues, upload credit, part files, server and Kad
bootstrap, and user-owned profiles. It modernizes the operational layer around
Windows builds, profile handling, long paths, diagnostics, REST, and broadband
usage.

## The Short Version

eMuleBB is not a tracker-style download button. It is a long-running peer client.
You connect to eD2K and/or Kad, find sources for files, wait in remote users'
queues, download verified pieces from many peers, and upload to others while
you wait. Good results come from reachable ports, stable sessions, sensible
limits, careful search choices, and deliberate sharing.

For a first serious setup:

1. Put the app, profile, temp, incoming, and shared directories in separate
   places.
2. Launch with an explicit profile path:

   ```powershell
   emulebb.exe -c C:\eMuleBB\Profiles\main
   ```

3. Configure TCP and UDP ports and confirm High ID or non-firewalled Kad.
4. Add one small shared directory and one small test download.
5. Learn the transfer list before adding many files.
6. Leave the client running long enough to gather sources and queue position.
7. Add REST, aMuTorrent, Prowlarr, Radarr, or Sonarr only after the desktop app
   is healthy.

## If You Know Other P2P Apps

Coming from another tool, map the concepts carefully:

| If You Know... | eMuleBB Difference |
|---|---|
| BitTorrent trackers | eD2K servers help discovery but do not host swarms. |
| DHT | Kad is closer, but eMule still has eD2K-specific identity and source flow. |
| Soulseek-style browsing | eMule can expose shared files, but search is hash/source based. |
| Usenet indexers | Torznab here is an adapter over live eD2K/Kad search, not an NZB index. |
| qBittorrent Web API | eMuleBB `/api/v2` is an Arr adapter subset, not full qBittorrent. |
| Seedboxes | Long uptime helps, but upload queues, credits, and High ID matter. |
| Download managers | eMule waits in other users' upload queues; idle is often normal. |

The main adjustment is patience with source discovery and queues. In eMule,
being well configured makes you more reachable and more useful to the network,
but it does not force rare sources to be online.

## The Main Window Map

Classic eMule-style clients organize the workflow into a few durable pages.
Names vary slightly by skin, language, and build, but the mental model is
stable:

| Area | What It Is For | First-Time User Rule |
|---|---|---|
| Server | eD2K server list, connection, logs, server messages. | Use clean server lists; do not chase random servers. |
| Kad | Kad connection state and bootstrap controls. | Bootstrap once, then let `nodes.dat` stay fresh. |
| Transfers | Downloads, uploads, queue, sources, categories. | Live here while learning the client. |
| Search | eD2K/Kad searches and result inspection. | Search broad, inspect names and sources, then download. |
| Shared Files | Files and directories you publish. | Verify privacy before adding large roots. |
| Messages/Friends | Peer messages and friend slots. | Optional; useful for trusted peers, not normal setup. |
| Statistics | Session and cumulative traffic behavior. | Use it to evaluate long sessions, not minute spikes. |
| Options/Preferences | Ports, directories, limits, WebServer/REST, advanced settings. | Change one major setting at a time. |
| Tools/Diagnostics | Maintenance and evidence collection. | Capture evidence before changing many variables. |

The Transfers page is the cockpit. Search finds candidates; Transfers shows
whether those candidates are actually obtainable.

## First 10 Minutes, First Day, First Week

Use staged confidence instead of trying to finish the whole setup at once.

### First 10 Minutes

1. Launch with `-c`.
2. Set temp and incoming.
3. Set TCP/UDP ports.
4. Connect to eD2K and Kad.
5. Read the status bar: connected, Low ID, firewalled, speeds.
6. Add one small shared directory.
7. Run one broad search.

### First Day

1. Fix High ID or Kad firewalled before adding heavy downloads.
2. Learn the search result colors and source counts.
3. Add a few downloads with different source counts.
4. Watch QR, A4AF, and part availability.
5. Create categories for manual/test/archive work.
6. Let the client run long enough to gather sources and queue position.
7. Shut down cleanly once and confirm the profile reloads.

### First Week

1. Add larger shared roots gradually.
2. Tune upload and connection limits using real observation.
3. Add IP filters only after baseline startup is understood.
4. Add REST and aMuTorrent.
5. Add Prowlarr/Radarr/Sonarr only after manual flows are clear.
6. Create a profile backup routine.
7. Record known-good package, profile, port, and category settings.

## Core Vocabulary

| Term | Meaning |
|---|---|
| eD2K | Server-assisted eDonkey network used for search and source discovery. |
| Kad | Decentralized Kademlia-style network used without central servers. |
| Server | Directory and rendezvous node. It does not host the files you download. |
| Peer/client | Another user's eMule-family client. Peers upload and download file parts. |
| Source | A peer known to have at least one needed part of a file. |
| High ID | eD2K state where peers can connect to your client directly. |
| Low ID | eD2K state where incoming connections are blocked or cannot be routed. |
| Firewalled Kad | Kad state where UDP reachability is blocked or uncertain. |
| Hash | File identity. eMule recognizes downloads by hash, not only by filename. |
| Part/chunk | A verified section of a file. Completed parts can be shared before the whole file completes. |
| `.part` | Incomplete data file in the temp directory. |
| `.part.met` | Metadata for an incomplete download. Losing it can orphan the `.part` data. |
| Incoming | Completed-download directory. |
| Temp | Incomplete-download directory. |
| Shared directory | Directory whose files are published to other peers. |
| Category | Download grouping with color, path, and controller/import meaning. |
| QR | Queue rank: your approximate position in another peer's upload queue. |
| A4AF | Asked For Another File: one source has multiple files you want, but you queue for only one at a time. |
| Credits | Per-peer upload credit that can improve your position in that peer's queue. |
| REST | eMuleBB's local automation API. It is for trusted controllers, not broad exposure. |

## How eMule Actually Downloads

A download is not one connection to one server. The server or Kad network helps
you discover peers. The file is then assembled from parts provided by many
clients.

The normal loop is:

1. You search or add an `ed2k://` link.
2. eMuleBB identifies the file by hash, size, and metadata.
3. eMuleBB asks servers, Kad, and known peers for sources.
4. Each source decides where you are in its upload queue.
5. When a slot opens, you download one or more blocks from that source.
6. eMuleBB verifies completed parts.
7. Verified parts may become available for upload to other peers.
8. When all parts are verified, the file moves from temp to incoming.

This is why a rare file may appear to do nothing for hours, then suddenly
progress. You may be waiting for a source to appear, waiting in a queue, or
waiting for a missing part to become available.

## File Lifecycle

Every download moves through a lifecycle:

| Stage | What Happens | What To Check |
|---|---|---|
| Candidate | Search result or `ed2k://` link is selected. | Hash, size, extension, names, comments. |
| Queued | eMuleBB creates `.part` and `.part.met` state. | Temp path and category. |
| Source discovery | Server, Kad, and peer exchange find sources. | Source counts and network state. |
| Waiting | Your client waits in remote upload queues. | QR and A4AF. |
| Transferring | Blocks arrive from one or more peers. | Speed, compression, part colors. |
| Verifying | Completed parts are hash-checked. | Corruption log entries. |
| Sharing partials | Verified parts can be uploaded. | Upload queue and shared behavior. |
| Completing | Whole file is assembled and moved. | Incoming path, disk space, permissions. |
| Shared complete | Completed file is available to others. | Shared Files page and category path. |

Do not manipulate temp files while the app is running. The `.part` file without
the matching metadata is only raw bytes; the metadata tells eMuleBB what those
bytes mean.

## What Servers Do And Do Not Do

An eD2K server is not a file host. It helps clients find each other. A server can:

- accept your connection
- assign or report your eD2K ID state
- index file/source metadata
- answer searches
- tell peers about each other

A server does not:

- store your downloads
- guarantee a file is complete
- prove a filename is honest
- make a Low ID client fully reachable
- replace Kad

There is no universal "fastest server". A stable and clean server list is more
important than chasing one perfect server. Global searches ask more than the
current server, but they also create more network load and still depend on the
quality of the indexed sources.

## Server List Hygiene

Server lists are operational input. Treat them like a trust list, not a random
collection.

Good habits:

- keep a small, reputable server list
- remove dead or suspicious servers
- avoid auto-importing from untrusted URLs
- use static servers only when the static list is known good
- do not diagnose Kad by changing many server settings at once
- remember that server connection loss is not automatically a download failure

If eMuleBB will not connect to eD2K:

1. Check that the server list is not empty.
2. Check whether "static servers only" blocks connection.
3. Check firewall/router/VPN reachability.
4. Try another known good server.
5. Check logs for rejected, dead, or timed-out servers.
6. Keep Kad separate in your diagnosis.

Global server search is useful, but it asks more servers and takes longer. Use
it when local server search does not find enough, not as the default hammer for
every query.

## What Kad Adds

Kad is decentralized. Instead of relying on a server list, the client learns
about other Kad nodes and uses that network for search and source discovery.

Kad needs bootstrap data. A profile usually carries `nodes.dat`, and a healthy
client keeps it fresh during normal use. On a brand-new profile, Kad may need a
server connection, known clients, or an imported nodes list before it can join
the network.

Use both eD2K and Kad when possible:

- eD2K can be simple to connect and useful for server-indexed searches.
- Kad keeps working without a chosen server once bootstrapped.
- Search results can differ between networks.
- Source discovery improves when both paths are healthy.

## Kad Bootstrap Runbook

For a new or broken Kad profile:

1. Confirm UDP is not blocked locally.
2. Confirm the configured UDP port is forwarded if you are behind NAT.
3. Connect to an eD2K server if possible.
4. Start one safe download or search so eMuleBB can encounter peers.
5. Bootstrap Kad from known clients when available.
6. If needed, import a fresh `nodes.dat` from a reputable source.
7. Leave the client running long enough to learn nodes.
8. Restart once and confirm Kad can reconnect from saved state.

Kad states to understand:

| State | Meaning | Next Step |
|---|---|---|
| Off | Kad is not connected. | Start Kad or bootstrap. |
| Connecting | Client is trying to join. | Wait; then check nodes and UDP. |
| Firewalled | Kad works but reachability is poor. | Fix UDP/NAT/VPN. |
| Open/OK | Kad is reachable. | Leave it running and stable. |

Do not constantly delete `nodes.dat`. A healthy profile improves over time.

## High ID, Low ID, And Firewalled Kad

Reachability is the first serious quality gate.

High ID means the eD2K network can route peers directly to your client. Low ID
means peers cannot reach your listening TCP port directly, usually because of a
router, firewall, NAT, VPN, carrier-grade NAT, or wrong local bind address.

Kad has a similar problem space, but UDP reachability matters. You can have a
good eD2K connection and still have Kad show as firewalled if UDP traffic is not
working correctly.

Why this matters:

- Low ID clients can still work, but source discovery and peer connection paths
  are worse.
- Two Low ID clients usually cannot connect directly to each other.
- Servers have to help forward some Low ID interactions.
- Rare files become harder because every lost source matters.
- Upload fairness and queue progress are less effective when reachability is
  poor.

Minimum network checklist:

1. Pick fixed TCP and UDP ports in eMuleBB.
2. Allow `emulebb.exe` through Windows Firewall.
3. Forward the same TCP and UDP ports from router to the eMuleBB machine.
4. Keep the machine's LAN IP stable through DHCP reservation or static address.
5. If using a VPN, confirm the VPN supports incoming port forwarding.
6. If using UPnP, verify it actually created the mappings you expect.
7. Confirm High ID and non-firewalled Kad after reconnecting.

Do not copy old default port numbers blindly. Modern eMule clients can use
different configured ports. Always forward the ports shown in your preferences.

## NAT, VPN, And Port-Forwarding Cases

Most reachability failures fall into one of these cases:

| Case | Symptom | Fix |
|---|---|---|
| Windows Firewall only | Works when firewall disabled. | Allow `emulebb.exe` and configured ports. |
| Home router NAT | Low ID from outside LAN. | Forward TCP/UDP to the eMuleBB machine. |
| Double NAT | Forwarding one router is not enough. | Bridge one router or forward both layers. |
| Carrier-grade NAT | Router has no public address. | Use ISP public IP option or forwarding-capable VPN. |
| VPN without forwarding | Outbound works, incoming does not. | Use VPN provider with forwarded port support. |
| VPN bind mismatch | Traffic leaves wrong interface. | Set bind policy deliberately and verify diagnostics. |
| UPnP partial success | One port maps, another does not. | Inspect router mappings; fall back to manual rules. |
| UDP remapping | eD2K High ID but Kad firewalled. | Preserve UDP port mapping or use different route. |

If testing from inside your LAN, remember that some routers do not support
hairpin NAT. A local test against the public address may fail even when outside
peers can reach you. Use eMuleBB's network status and an external port test
where appropriate.

## WebServer, REST, And P2P Ports Are Different

eMuleBB has P2P listener ports and a WebServer/REST listener. They are separate
surfaces.

| Surface | Purpose | Exposure Rule |
|---|---|---|
| P2P TCP/UDP | eD2K/Kad peer traffic | Needs public reachability for best P2P behavior. |
| WebServer/REST | Local controller and automation API | Keep local or controlled; do not expose broadly. |

Forwarding P2P ports does not mean REST should be reachable from the internet.
For controllers, bind REST to localhost when possible. If a LAN/VPN controller
needs access, use firewall rules, strong API keys, and a deliberate bind
address.

## Profiles And Identity

The profile is the user's eMule identity and working state. Treat it like a
database, not like a cache.

Important files include:

| File | Why It Matters |
|---|---|
| `preferences.ini` | Main readable settings file. |
| `preferences.dat` | Identity-related state. Back it up with the profile. |
| `cryptkey.dat` | Key material used for secure identity. |
| `clients.met` | Credits your client grants to other peers. |
| `server.met` | Known server list. |
| `nodes.dat` | Known Kad nodes. |
| `known.met` / `known2_64.met` | Known shared-file and hash state. |
| `Category.ini` | Download categories and paths. |
| `ipfilter.dat` | IP filter data. |
| `shareddir.dat` | Shared directory records. |
| `.part.met` files | Incomplete download metadata. |

Do not run multiple eMule-family clients against the same profile. Do not edit
profile files while the app is running unless a guide explicitly says a live
edit is safe.

Before risky work:

1. Close eMuleBB and every eMule-family client.
2. Copy the whole profile directory.
3. Keep the backup outside the active profile base.
4. Record the app package version and architecture.
5. Start the copied profile once without controllers.

## Backup And Restore Runbook

Back up profiles while eMuleBB is closed.

Minimum profile backup:

1. Profile/config directory.
2. Temp directory if you need incomplete downloads.
3. Incoming category configuration if paths live outside the profile.
4. Notes for app version, architecture, ports, and launch command.

Restore carefully:

1. Restore to a new profile base.
2. Launch with `-c <restored-profile>`.
3. Confirm `preferences.ini` paths point to real directories.
4. Do not let a restored profile share private paths accidentally.
5. Start without controllers.
6. Let hashing and known-file checks finish.
7. Only then reconnect automation.

Identity-sensitive files such as `preferences.dat` and `cryptkey.dat` should
stay together. Losing identity state can affect secure recognition and credits.

## Directory Model

Keep five concepts separate:

| Directory | Contains | Mistake To Avoid |
|---|---|---|
| Application | `emulebb.exe`, DLLs, scripts, packaged assets | Do not store live profile state here. |
| Profile/config | identity, preferences, server/Kad state, logs | Do not share it between running clients. |
| Temp | incomplete `.part` and `.part.met` files | Do not delete it to "clean space". |
| Incoming | completed downloads | Do not assume this is the same as shared roots. |
| Shared roots | files you intentionally publish | Do not share broad personal folders. |

When launching with `-c`, eMuleBB uses that directory as the profile base and
creates `config` and `logs` below it when needed. The effective preferences file
is `<profile-dir>\config\preferences.ini`. If that file already exists, its
configured incoming and temp paths take precedence. A clean profile may create
default `<profile-dir>\Incoming` and `<profile-dir>\Temp` directories, but an
existing profile with explicit paths should not create dangling temp or incoming
folders next to the executable.

## First Launch From Zero

Use this sequence for a new profile:

1. Create an empty profile directory.
2. Launch with `emulebb.exe -c <profile-dir>`.
3. Set the temp directory on a fast disk with enough free space.
4. Set incoming to the final storage volume.
5. Configure TCP and UDP ports.
6. Decide between manual router forwarding and UPnP.
7. Connect to eD2K and Kad.
8. Add one small shared folder with non-private files.
9. Search for one safe, broad test file.
10. Watch the transfer list until you understand sources, status, and progress.
11. Shut down cleanly and confirm logs are in the profile.

Do not import a large share, enable controllers, and add hundreds of downloads
on the first run. That creates too many variables.

## Status Bar And Connection Indicators

The status bar is a compressed health report. Use it before opening settings.

Read it for:

- latest log line
- estimated eD2K and Kad users/files
- upload speed
- download speed
- optional protocol overhead
- eD2K server connection
- Kad connection state
- combined connection icon

Color conventions in classic eMule-family clients:

| Color | Network Meaning |
|---|---|
| Red | Offline or not connected. |
| Orange | Connecting. |
| Yellow | Connected but firewalled or Low ID. |
| Green | Connected and reachable. |

For speed, distinguish payload from overhead. Control traffic, pings, server
messages, source exchange, and Kad traffic can consume bandwidth even when no
file payload is moving.

## Searching Well

Search quality is a skill.

Use broad terms first. Add filters only after you see the shape of the result
set. A narrow query can miss good sources because filenames vary, spellings
differ, and old files may have inconsistent metadata.

Evaluate search results with several signals:

- source count
- complete source availability
- file size
- file extension and type
- filename variants reported by sources
- comments and ratings
- fake/trust indicators
- whether results appear on eD2K, Kad, or both

Common patterns:

| Pattern | Meaning |
|---|---|
| Many names, same hash | Normal when users renamed the same file. Check whether names agree in substance. |
| Contradictory names | Possible fake or poisoned result. Inspect before downloading. |
| Many sources, no complete source | It may stall forever if the missing part never appears. |
| Few sources, old file | Expect long waits. Keep the client running. |
| Different eD2K/Kad results | Normal. The networks discover and index differently. |

Do not rely on one search attempt. Try different file type filters, networks,
and terms. Let the client gather sources before concluding a file is dead.

## Search Modes

Use the search mode that matches the question:

| Mode | What It Asks | Use When |
|---|---|---|
| Local/server | Current eD2K server. | Quick first check. |
| Global server | Many servers from your list. | Local server has poor results. |
| Kad | Decentralized Kad network. | Server results are weak or you want Kad-only visibility. |
| Automatic/controller | Adapter chooses supported methods. | REST or Arr workflow owns the search. |

Kad and eD2K source counts are not always directly comparable. Treat search
results as candidates. The transfer list becomes more authoritative after
eMuleBB has contacted sources.

## Search Result Triage

Before double-clicking a result, ask:

1. Does the size match the claimed content?
2. Does the extension match the claimed content?
3. Are there complete sources?
4. Do alternative filenames agree?
5. Are comments positive, negative, or suspicious?
6. Is the file already in downloads or shared files?
7. Does the result come from a network you trust for this query?
8. Is this a safe file type to handle on this machine?

For archives, installers, scripts, and executables, use extra caution. eMuleBB
can identify and transfer bytes; it cannot decide whether running those bytes is
safe.

## Reading The Transfer List

The transfer list is the main instrument panel.

Key ideas:

- Progress is part availability, not only speed.
- A file can have many sources and still wait because you are queued.
- A source can be useful for one file and A4AF for another.
- A filename can be changed without changing the underlying file identity.
- A completed verified part can be uploaded before the whole file completes.

Important columns and states:

| Item | How To Read It |
|---|---|
| Sources | How many useful and total sources are known. |
| QR | Your remote queue position with a source. |
| A4AF | The source is currently assigned to another wanted file. |
| Last seen complete | Last time all parts were observed somewhere. |
| Status | Waiting, downloading, paused, stopped, completing, error, or disk-space state. |
| Category | Grouping and often the completed path. |

If the transfer list looks idle, ask:

1. Is the network connected?
2. Is the file paused or stopped?
3. Are there useful sources?
4. Are there complete sources?
5. Are sources reachable or all Low ID/firewalled?
6. Are connection limits too tight?
7. Is disk-space protection active?
8. Is the file waiting normally in queues?

## Progress Bar Colors

Progress bars show availability and state at a glance. Exact colors can vary by
skin, but the classic model is:

| Color | Download Progress Meaning |
|---|---|
| Black | You already have this part and it verified. |
| Yellow | This part is being downloaded now. |
| Blue | Needed part is available from at least one source. Darker means more available. |
| Red | No known source currently has this part. |
| Green | File is complete and verified. |

Expanded source bars show what a specific peer has:

| Color | Source Bar Meaning |
|---|---|
| Black | Peer has a part you need. |
| White/empty | Peer does not have that part. |
| Green | Both you and the peer have it. |
| Yellow | Peer is currently sending it to you. |

Do not panic over red immediately after adding a file. Source discovery takes
time. Worry when the same red gaps remain for days and all known sources miss
the same parts.

## Source Count Formats

Classic eMule-family transfer lists often compress several counts into one
field. Read them as:

| Piece | Meaning |
|---|---|
| useful | Sources you can potentially download from. |
| total | All known sources for the file. |
| A4AF | Sources currently assigned to another wanted file. |
| transferring | Sources actively sending data now. |

The exact display can vary, but the intent is stable: not every known source is
immediately useful, and not every useful source is transferring now.

## Download Priorities

Priorities are relative. Setting everything to high is equivalent to setting
nothing to high.

Use priorities deliberately:

- increase priority for a small number of files that matter now
- lower priority for bulk background downloads
- use categories to separate manual, Radarr, Sonarr, and archival flows
- do not use priority to compensate for bad connectivity
- do not expect priority to create sources that do not exist

Upload priority affects how your client treats requests for your shared files.
It should be used to emphasize intentional releases or important shares, not as
a blanket setting for the whole library.

## A4AF: Asked For Another File

A4AF is not an error. It means the same remote client has more than one file you
want, but your client can queue with that source for only one of them at a time.

Use A4AF controls when:

- one rare file needs a source more than another
- a nearly complete file should finish before a bulk file
- categories split acquisition priorities

Do not micro-manage every A4AF entry. The client normally handles this well
enough unless you have rare files or a specific completion goal.

## Pause, Stop, Resume, Cancel, Delete

These actions are different:

| Action | Meaning |
|---|---|
| Pause | Stop transfer activity but keep source knowledge for quicker resume. |
| Stop | Stop and drop active source state; resume requires fresh source work. |
| Resume/start | Allow the transfer to continue. |
| Cancel | Remove the download from the active list. |
| Delete files | Remove associated data as well; destructive. |

Use pause for temporary bandwidth or priority control. Use stop when you want to
clear active source work. Use delete only when you are sure you no longer want
the incomplete or completed data.

## Uploading, Queueing, And Credits

Uploading is part of how eMule works. It is not just a moral preference; it is
part of the network's scheduling economy.

Credits are peer-local. If you upload to another client, that client can give
you better queue treatment later. Credits are not a global score you can view
or spend anywhere. They are tied to identity and secure recognition between
clients.

Practical consequences:

- keep a stable profile identity
- upload consistently
- do not delete identity files casually
- avoid very short sessions
- set upload limits so the connection stays usable but busy
- keep a useful upload queue

For broadband users, the right upload limit is usually below the physical
maximum but high enough to keep slots active. Saturating the connection can hurt
latency, DNS, browsing, controllers, and source discovery. Starving upload hurts
credits and network health.

## Upload Slots And Friend Slots

Normal upload slots are managed by the client. A friend slot is a deliberate
exception for a trusted peer. Use it sparingly.

Friend slots are useful when:

- you coordinate with a known peer
- you are helping someone obtain a rare file
- you are testing upload behavior
- you want to prioritize a trusted exchange

They are not a general speed booster. Giving away upload capacity to a friend
changes how much capacity remains for the normal queue.

## Why Downloads Are Not Instant

eMule is strongest when files can be assembled over time from many peers. Speed
depends on:

- your High ID / Kad reachability
- session duration
- upload behavior and credits
- number of sources
- part distribution
- file popularity
- remote clients' queue lengths
- connection limits
- disk state
- whether the file is complete somewhere

Power-user rule: optimize for stable average throughput and completion, not
momentary peak speed.

Good habits:

- keep the client online for long sessions
- download several well-sourced files instead of one lonely file
- avoid huge bursts of new downloads
- keep upload active
- prefer files with enough sources and complete availability
- do not restart constantly while waiting in queues

## Connection Limits And Broadband Tuning

More connections are not automatically better.

Too many connections can cause:

- router table exhaustion
- high CPU use
- poor UI responsiveness
- slow source processing
- connection churn
- "too many connections" source states
- bad behavior during startup

Start conservative. Raise limits only when you can observe that the machine,
router, and profile handle the load.

Tune in this order:

1. Fix High ID/Kad reachability.
2. Set upload limit so latency remains usable.
3. Keep max connections within what your router can handle.
4. Keep hard limits reasonable per file.
5. Avoid adding thousands of downloads at once.
6. Watch CPU, memory, disk queue, and router stability.
7. Change one setting at a time and leave it running long enough to matter.

For a heavy live profile, the slow parts are often startup scanning, hashing,
IP filter loading, server/Kad bootstrap, and transfer source processing. Do not
judge performance from the first minute after launching a huge profile.

## Bandwidth Units

Network providers usually advertise bits per second. eMule-style clients often
show bytes per second.

| Unit | Meaning |
|---|---|
| `Mb/s` or `Mbps` | Megabits per second. Divide by 8 for megabytes/s. |
| `MB/s` | Megabytes per second. Multiply by 8 for megabits/s. |
| `kB/s` | Kilobytes per second. Common client display unit. |

If your upstream is `40 Mbps`, the theoretical maximum is about `5 MB/s`.
Practical upload limits should be below that to leave room for overhead and
other applications.

## Heavy Profile Startup

A heavy profile may do real work before it feels responsive:

- load preferences and categories
- validate temp entries
- read `.part.met` files
- scan known files
- hash new or changed shared files
- load `known.met` and sidecars
- load IP filters
- reconnect eD2K and Kad
- rebuild source state
- initialize REST and controller surfaces

If startup regresses, measure phases separately. "Slow startup" can be disk,
hashing, IP filter parsing, source restoration, networking, or UI list
population. A CPU profile and logs are more useful than changing settings at
random.

## Categories

Categories are not just labels. They can affect color, grouping, completed
path, controller behavior, and Arr import.

Use categories for:

- manual downloads
- Radarr downloads
- Sonarr downloads
- archive projects
- rare-file recovery
- test downloads
- paused/backlog items

Suggested starting shape:

| Category | Use |
|---|---|
| `manual` | Normal operator-added downloads. |
| `archive` | Long-running archival acquisitions. |
| `rare` | Files that may need manual source/A4AF attention. |
| `emulebb-radarr` | Radarr download-client path. |
| `emulebb-sonarr` | Sonarr download-client path. |
| `test` | Disposable package/profile validation. |

Keep category paths visible to the process that needs them. If Radarr or Sonarr
runs in a container, VM, or another machine, configure remote path mappings
there instead of lying to eMuleBB about its local paths.

## Large Library Plan

For a large shared library, stage the rollout:

1. Start with one narrow root.
2. Let hashing finish.
3. Confirm the Shared Files page shows only intended files.
4. Add share-ignore rules for junk and private sidecars.
5. Add the next root.
6. Watch startup time and hash time.
7. Keep a list of public roots outside the app.

For libraries with tens or hundreds of thousands of files, the risk is not only
hashing time. It is accidental sharing, path churn, slow startup, and support
reports that cannot distinguish scan time from network problems.

## Sharing Safely

eMule shares:

- files in incoming
- files in directories you marked as shared
- completed verified parts of active downloads

That last point surprises new users. Current downloads participate in sharing
once verified parts exist.

Before adding a shared directory:

1. Confirm it contains only files you intend to publish.
2. Avoid broad roots such as a whole user profile, desktop, documents folder,
   or media library with private subfolders.
3. Use share-ignore rules for clutter, metadata, partial exports, and private
   sidecars.
4. Add large libraries gradually.
5. Let hashing finish before judging search visibility or startup cost.

Large library habits:

- keep shared roots stable
- avoid constantly moving files
- avoid network shares unless you understand the latency
- keep path lengths sane even though eMuleBB supports modern long paths
- document which roots are public
- recheck shares after restoring a profile on a different machine

## Release And Archival Sharing

If you intentionally publish a file:

1. Put it in a stable shared directory.
2. Give it a clear filename before hashing.
3. Let hashing complete.
4. Keep the client online long enough for discovery.
5. Avoid moving or renaming it repeatedly.
6. Use upload priority only for a small set of important files.
7. Watch whether parts spread, not only whether one peer downloaded.

Archival sharing is long-horizon work. A rare file becomes healthier when
multiple reachable clients hold verified parts.

## Temp And Incoming Recovery

Do not delete temp to clean up space unless you intend to delete incomplete
downloads.

If downloads disappear after a crash or restore:

1. Stop eMuleBB.
2. Check that the configured temp path is still correct.
3. Look for `.part.met` and `.part.met.bak` files.
4. Restore from the profile backup if available.
5. Avoid moving `.part` files without their metadata.
6. Use file details to match part numbers and final names if manual recovery is
   needed.

If a completed file cannot move to incoming, check free space and permissions
on the incoming volume. Completion can fail even when temp has space if incoming
is on a different disk and that target disk is full.

## Disk-Space Strategy

eMule downloads can reserve or consume large temp space before completion. Plan
for both temp and incoming:

- keep temp on a disk with enough write endurance and free space
- keep incoming on the final storage volume when possible
- avoid network temp paths
- monitor low-space behavior before the disk is nearly full
- do not use unrelated cleanup tools on temp while eMuleBB is running
- remember that completion may need space or permissions on incoming

If disk pressure appears, pause or stop selected transfers through the app.
External deletion is the last resort.

## IP Filters

An IP filter can block known bad ranges or unwanted peers, but it is not a
security boundary.

Use IP filters as one layer:

- keep the source reputable
- avoid huge unreviewed lists if startup time matters
- reload deliberately
- check logs when a filter update appears to block too much
- do not assume an IP filter protects private data in shared folders

If startup is slow and the IP filter is large, measure filter load time
separately from hashing and source processing. They are different bottlenecks.

## Logs And Diagnostics

Logs are not just for developers. They explain startup, connectivity, parsing,
hashing, REST, and completion failures.

Use logs when:

- ports appear open but status is still Low ID
- Kad remains firewalled
- a file completes but does not move
- IP filter loading is slow
- WebServer/REST does not bind
- controller authentication fails
- startup is much slower than the last known-good build

For hangs and CPU burn, capture diagnostics before closing the process if
possible. A dump or profile taken during the bad state is more valuable than a
description after restart.

## Comments, Ratings, And Fakes

eMule-era networks rely on user judgment. A hash identifies bytes, not truth.

Inspect:

- all discovered filenames for the same hash
- comments and ratings
- size consistency
- extension consistency
- file type filters
- source diversity
- whether one suspicious source dominates a result

Warning signs:

- filenames strongly disagree
- file size does not match the claimed type
- comments report fake, corrupt, passworded, or malware content
- extension does not match expected media or archive type
- a result appears popular but has no complete source

Do not run downloaded executables from untrusted sources. Treat archives and
scripts as risky until inspected outside eMuleBB.

## Content Safety Workflow

For unknown files:

1. Prefer data files over executables.
2. Inspect filenames from multiple sources.
3. Check comments and ratings.
4. Verify extension and size.
5. Scan completed files with local security tooling.
6. Open risky files in an isolated environment if you must inspect them.
7. Do not disable security tools to make a download easier to run.

eMuleBB can help you avoid obvious bad candidates, but final execution safety is
outside the P2P client.

## Security And Privacy

eMule-style P2P is public peer-to-peer traffic. Other peers and servers can see
network-level information needed for the protocol. Plan accordingly.

Rules:

- share only files you intend to publish
- keep profile backups private
- keep API keys out of screenshots and logs
- bind REST locally unless controlled exposure is intentional
- use firewall rules that match your plan
- treat VPN port forwarding as a separate networking project
- do not paste live media titles, private paths, or API keys into public issues
- understand local law and rights before sharing or downloading content

Obfuscation, HTTPS, or a VPN does not turn public P2P activity into private
storage. It only changes parts of the transport path.

## Multi-User Windows Machines

On shared Windows machines:

- use a profile directory owned by the intended user account
- keep temp and incoming outside shared personal folders unless intentional
- do not put API keys in shared scripts
- avoid running eMuleBB elevated unless required for a specific diagnostic
- check filesystem permissions on incoming and shared roots
- document which account owns scheduled starts or controller services

Two Windows users should not launch the same profile concurrently.

## Controllers And Automation

The correct order is:

1. eMuleBB desktop works.
2. REST read-only status works.
3. REST mutations work for one harmless operation.
4. aMuTorrent reads state correctly.
5. Prowlarr Torznab caps/search works.
6. Radarr/Sonarr qBit-compatible download-client test works.
7. One manual acquisition works.
8. Automatic search/import can be enabled.

Do not let automation hide basic client state. If the desktop app shows Low ID,
bad paths, missing categories, disk-space problems, or startup churn, fix that
first.

For full controller setup, use [Stack Integration Guide](GUIDE-STACK-INTEGRATIONS.md).

## Common First-Time Mistakes

| Mistake | Result | Better Habit |
|---|---|---|
| Running from a live profile with no backup | Hard-to-undo state changes | Copy the profile first. |
| Forwarding old default ports | Still Low ID | Forward the configured ports. |
| Sharing a whole personal folder | Privacy leak | Share narrow folders only. |
| Deleting temp | Lost incomplete downloads | Use disk-space triage first. |
| Setting everything high priority | No effective priority | Prioritize a few files. |
| Adding hundreds of downloads at once | Startup and connection churn | Add gradually. |
| Enabling Arr automation immediately | Confusing failures | Prove desktop and REST first. |
| Exposing REST publicly | Credential and control risk | Bind local or controlled LAN/VPN. |
| Restarting repeatedly | Lost queue momentum | Let sessions run. |

## Symptom Map

| Symptom | First Places To Look |
|---|---|
| Low ID | TCP port, router forwarding, firewall, VPN, bind address |
| Kad firewalled | UDP port, NAT behavior, VPN, firewall |
| No search results | Network state, search type, query terms, server/Kad bootstrap |
| Many sources but no speed | Queue rank, credits, upload limit, part availability |
| Red missing parts forever | No complete source, dead file, bad part spread |
| Too many connections | Hard limit, max connections, too many downloads |
| Completed file missing | Incoming path, disk space, permissions, completion error |
| Slow startup | Huge shares, hashing, temp count, IP filter, source processing |
| REST unavailable | WebServer enabled, bind, port, API key, lifecycle state |
| Arr import failure | Category path, remote path mapping, completed path visibility |

## What To Record Before Asking For Help

Useful support reports include:

- eMuleBB package version and architecture
- profile type: new, copied, live, or restored
- whether launch used `-c`
- TCP and UDP ports, without exposing unrelated router secrets
- eD2K ID and Kad firewall state
- whether WebServer/REST is enabled
- temp, incoming, and category path shape with private names redacted
- number of downloads and shared files
- whether the problem happens with a small disposable profile
- recent logs and diagnostic snapshot with API keys removed

Bad reports are vague: "it is slow" or "downloads do not work." Good reports
name the layer: reachability, search, source discovery, queueing, disk,
completion, REST, controller, or import.

## Historical Source Notes

This guide adapts concepts from old eMule and aMule user documentation, but the
wording and eMuleBB operating rules here are maintained for this project:

- Official eMule ports/firewall guide:
  <https://www.emule-project.com/home/perl/help.cgi?l=1&rm=show_topic&topic_id=122>
- Official eMule server and ID FAQ:
  <https://www.emule-project.net/faq/faq_server.htm>
- Official eMule credits FAQ:
  <https://www.emule-project.net/faq/faq_credits.htm>
- Official eMule settings and speed FAQ:
  <https://www.emule-project.net/faq/faq_settings.htm>
- Official eMule downloads and shared files FAQ:
  <https://www.emule-project.net/faq/faq_downloads.htm>
- aMule getting-started guide:
  <https://wiki.amule.org/t/index.php?title=Getting_Started>
- aMule firewall guide:
  <https://wiki.amule.org/t/index.php?title=Firewall>

When those historical docs differ from current eMuleBB behavior, this guide and
the focused eMuleBB references win.

## Related eMuleBB Guides

- [Product Guide](GUIDE-EMULEBB.md)
- [Setup Guide](GUIDE-SETUP.md)
- [Network Guide](GUIDE-NETWORK.md)
- [Downloads And Search](GUIDE-DOWNLOADS-SEARCH.md)
- [Sharing Guide](GUIDE-SHARING.md)
- [Stack Integration Guide](GUIDE-STACK-INTEGRATIONS.md)
- [Troubleshooting Guide](GUIDE-TROUBLESHOOTING.md)
