# Downloads And Search Guide

This guide covers search, download workflow, categories, filename handling,
transfer limits, and broadband upload behavior.

## Search Modes

eMule BB preserves native eMule search distinctions:

- Server search queries the current eD2K server.
- Global search uses the eD2K server network more broadly.
- Kad search uses decentralized Kad search.
- Automatic/controller search must map to one of the native search modes.

Use server search when a trusted server is enough, global search when wider
server coverage matters, and Kad when decentralized discovery is more useful.

Search result ceilings are configurable so modern sessions do not have to keep
old stock limits. eD2K expansion and Kad total/lifetime settings are persisted
preferences; exact keys and ranges are in [Preferences Guide](GUIDE-PREFERENCES.md).

## Search Result Quality

Search results can include bad names, misleading extensions, spam, or fake-file
signals. Treat the visible row as a candidate, not proof.

eMule BB separates **risk** from **evidence** in the search result list. Risk is
local evidence that a row may be spam, fake, mislabeled, or internally
inconsistent. Evidence is support for a specific claim about the row; it is not
a guarantee that the file is safe or authentic.

Check:

- filename agreement across sources
- suspicious extension/name combinations
- fake-file detector matches
- source count and source diversity
- comments and known metadata
- category destination and expected file type

Do not rely on one signal. File details and comments matter most for rare or
ambiguous files.

The compact **Risk** column summarizes local bad-signal evidence. Ctrl-hover a
search result for the desktop WHY view: risk, availability, complete-source
count, Kad publisher/name consistency when present, AICH hash when present, and
the detailed fake-file report.

The REST search result payload exposes the same model structurally:

- risk evidence: fake-file filter hits, spam score/status, bad or fake ratings,
  header/extension mismatches, executable/archive masquerade, implausible media
  metadata, and conflicting AICH hashes
- availability evidence: total sources, complete sources, directly observed
  clients, server observations, and Kad publisher counts
- name evidence: observed names, canonical-name agreement, ignored release/junk
  tokens, and meaningful name disagreement groups for the same hash
- Kad publisher evidence: Kad `TAG_PUBLISHINFO` decoded as publisher count,
  different-name count, raw Kad value, and a low/normal/high evidence band
- integrity evidence: AICH hash presence, pending header checks, cached header
  evidence, and detected-vs-claimed file type

Unknown evidence is neutral, not positive. For example, unknown Kad publisher
evidence means the row did not provide useful Kad publisher data; it does not
mean the row is trusted.

## Download Actions

Common actions:

- start, resume, pause, stop
- cancel with confirmation
- shifted cancel/delete paths for power-user no-confirm behavior
- open completed file
- open containing folder
- show details and comments
- copy ED2K links, names, paths, summaries, sizes, status, and progress
- change priority
- assign or move category

Keyboard details are in [Keyboard Shortcuts](KEYBOARD-SHORTCUTS.md).

## qBittorrent-Style Shortcuts And Batch Actions

eMule BB exposes selected qBittorrent-style shortcuts and batch menu actions
for faster desktop operation and controller parity. These are convenience
workflows over native eMule behavior, not a replacement behavior model.

Batch rules:

- destructive delete/cancel actions must preserve native confirmation and
  shifted no-confirm semantics.
- category actions must preserve eMule category ownership and destination
  behavior.
- paused and started adds remain distinct.
- completed and incomplete files remain different resources.
- copy actions should preserve enough detail for support, controller imports,
  or manual audits.

When a controller or shortcut behaves unexpectedly, compare it with the native
UI operation it is intended to represent.

## Categories

Categories are persistent workflow state. They affect organization, incoming
paths, filters, and controller expectations.

Good category practice:

- keep names short and stable
- avoid deleting categories that automation still uses
- move downloads intentionally before removing a category
- keep one default catch-all category
- use the category manager for normal edits and `Category.ini` only for careful
  maintenance

## Filename Cleanup

eMule BB can normalize download names on intake and completion. This is intended
to reduce obvious junk, not to erase identity.

Review before batch changes when:

- the filename becomes generic
- the extension does not match the expected type
- sources disagree
- risk/evidence feedback is mixed
- the result came from a controller import rather than manual selection

Filename cleanup settings and threshold preferences are documented in
[Preferences Guide](GUIDE-PREFERENCES.md).

## Completion Command

Completed downloads can optionally launch an external program. The feature is
profile-owned and should be used for trusted local automation only.

The relevant settings live under `[FileCompletion]`:

- `RunCommandOnFileCompletion`
- `FileCompletionProgram`
- `FileCompletionArguments`

Keep completion commands narrow, deterministic, and safe for filenames that
come from untrusted networks. Prefer explicit tools and explicit arguments over
shell expansion.

## Transfer Limits

Upload and download limits are finite runtime caps. eMule BB defaults are
modernized from older stock assumptions, but users should still set realistic
values for the current line.

Related controls:

- upload limit
- download limit
- max connections
- half-open/churn limits
- sources per file
- queue size
- file buffer size and time limit
- disk-space floors
- commit, sparse, and preallocation behavior

These settings are operational controls. Setting them too high can make network,
disk, or UI behavior worse even on a fast machine.

## Disk-Space Protection

eMule BB treats low disk space as a profile-safety problem, not just a transfer
speed problem. The guard protects the volumes used by active downloads and
metadata so the app does not keep writing when the filesystem is already below
the configured reserve.

Protected roles:

- config: the profile/config directory that stores `preferences.ini`, logs,
  identity files, known-file metadata, and download metadata sidecars
- temp: every configured temporary download directory
- incoming: the default incoming directory
- category incoming: every category-specific incoming directory

The stored preference keys are:

| Key | Role | Hard minimum |
|---|---|---|
| `MinFreeDiskSpaceConfig` | Config/profile volume | 1 GiB |
| `MinFreeDiskSpaceTemp` | Temp download volumes | 5 GiB |
| `MinFreeDiskSpaceIncoming` | Incoming and category incoming volumes | 5 GiB |

The Preferences dialog exposes these floors in GiB under Tweaks. The INI stores
normalized byte values. Direct INI values are normalized on load and save.
Values below the hard minimum are raised to the minimum, and values above the
supported 5120 GiB maximum are clamped to that maximum.

The guard works by resolved volume identity. If several protected paths point
to the same volume, eMule BB merges their roles and uses the largest floor for
that volume. For example, if config and temp are both on `D:`, the temp floor
normally controls that volume because it is higher. If temp and incoming are on
separate volumes, each volume is checked against its own effective requirement.

The effective requirement is:

```text
effective required free space = protected floor + completion reserve
```

The completion reserve is dynamic. For active or resumable downloads, eMule BB
adds the extra temp bytes still needed by the part file. If the completed file
will land on a different incoming volume, it also reserves the completed file
size on that incoming volume. This prevents a profile from accepting work that
fits in temp but cannot be safely completed into the configured incoming path.

When any protected volume is below its effective requirement, the queue enters
a protected disk-space block:

1. A warning is logged with the volume identity, protected role, current free
   bytes, required bytes, configured floor, and completion reserve.
2. Active, empty, hashing-wait, and insufficient downloads are stopped/paused.
3. `.part.met` metadata is saved immediately for every part file where the
   metadata write guard allows it.
4. The same breach is remembered so the log is not spammed repeatedly for an
   unchanged low-space condition.

The normal timed disk-space check runs every 15 minutes during queue activity.
Queue processing and manual actions that add, resume, complete, or flush files
can force a fresh protected-volume snapshot sooner.

The block clears only after protected-volume checks no longer find a breach.
Downloads marked insufficient for disk space are not resumed while a protected
volume is still below its requirement. Resume checks require the relevant temp
volume to have enough free space, including bounded headroom for the file that
previously failed because of insufficient space.

Metadata writes have a separate per-write safety guard. Before writing a
`.part.met` file, eMule BB resolves the metadata target's volume and compares
current free space with the effective requirement for that path. If the volume
cannot be resolved and a nonzero requirement applies, the write is blocked. If
the volume is resolved but below the requirement, the write is skipped and a
warning is logged. Failed metadata writes invalidate the guard state before the
next attempt. This is intentionally conservative: skipping a metadata write is
safer than producing a truncated or partially replaced `.part.met` file on an
exhausted disk.

New-download placement also uses protected-volume availability. When several
temp directories exist, eMule BB evaluates each candidate after subtracting the
protected requirement. It avoids duplicate volume candidates, rejects FAT
volumes for files above the old FAT-safe size limit, prefers a valid temp
volume that shares the incoming volume when appropriate, and otherwise chooses
a candidate that can satisfy both temp demand and any separate incoming demand.
If no candidate can satisfy the protected-volume snapshot, the add cannot
select a temp directory.

Native REST add-transfer requests go through the same placement logic. If the
disk-space guard rejects the transfer because no configured temp volume can
accept it safely, the API reports an error/failed item for that request instead
of returning a successful `ok: true` outcome.

Preview paths perform additional checks because preview may need temporary
copies. Archive-copy preview requires enough free space for the protected floor
plus two copies of the file size. Normal preview requires the floor plus the
completed bytes available for preview and a small extra buffer.

Operational guidance:

- keep config, temp, and incoming on volumes with predictable free space
- raise floors for very large download queues or automation-heavy profiles
- avoid putting temp on a nearly full system drive
- keep category incoming paths on volumes that can receive completed files
- treat repeated disk-space guard warnings as a storage issue, not a network
  issue
- free space or move paths, then resume downloads after the protected block has
  cleared
- do not lower floors to force a download through an exhausted volume; that
  increases the risk of metadata and part-file damage

## Broadband Upload Policy

The broadband upload controller changes the old stock model where upload slot
count could grow heavily with available speed.

Released behavior:

- `MaxUploadClientsAllowed` is the normal upload-slot target.
- Slot decisions use a finite configured upload budget.
- Slow or zero-rate slots can be recycled after warm-up and grace periods.
- Cooldown prevents the same weak slot pattern from churning constantly.
- Collection uploads have an intentional compatibility exception.
- Low-ratio scoring can give selected clients a queue boost.
- Ratio and cooldown data can be shown in UI columns.

Practical tuning:

- set a finite upload limit first
- keep the slot target modest for broadband links
- let warm-up finish before judging a slot as weak
- use diagnostics if upload timer or disk IO pressure appears
- avoid unlimited experiments when diagnosing speed

The exact broadband preference keys live under `[UploadPolicy]` and are listed
in [Preferences Guide](GUIDE-PREFERENCES.md).

## Modern Defaults

Modern-limit work adjusted old conservative assumptions where release changes
landed:

- connection and churn defaults are less constrained
- per-client upload/socket behavior is better suited to faster lines
- disk buffering defaults support larger transfers
- source, queue, and search ceilings are more practical for current use
- selected timeouts and buffers are documented as tunable preferences

Existing profiles keep explicit stored values unless migration or normalization
rules say otherwise.

## File Details And Copy Workflows

Use details for:

- source/name comparison
- comments
- hashes and ED2K links
- category, priority, and path review
- risk/evidence warnings

Use plain ED2K links for import/controller workflows. Use summary-copy actions
for support notes or manual audits.

## Automation Discipline

Controllers should not flatten eMule BB into a generic download-client model.
Native distinctions matter:

- search network choice
- category
- paused vs started add
- delete/cancel semantics
- completed vs incomplete files
- source/risk/evidence feedback
- local path and profile ownership

When controller behavior surprises you, compare the request with the native REST
contract and the UI operation it is supposed to represent.

## Troubleshooting

No results:

1. Confirm server/Kad state.
2. Try a simpler query.
3. Try another search method.
4. Refresh trusted server/Kad bootstrap sources.
5. Compare controller search tokens with REST docs.

Slow uploads:

1. Set a finite upload limit.
2. Check upload slot target.
3. Review ratio/slot columns.
4. Check diagnostic IO and upload timer data.
5. Check active upload socket buffer samples.

Poor names:

1. Compare source names.
2. Check risk/evidence signals.
3. Review comments and file details.
4. Avoid batch cleanup until selected rows have enough supporting evidence.
