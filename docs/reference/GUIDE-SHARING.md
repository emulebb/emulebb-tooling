# Sharing Guide

This guide covers shared directories, monitored shares, share-ignore rules,
large libraries, startup cache behavior, long paths, and recovery.

## Sharing Model

eMule BB keeps classic eMule sharing behavior. Files in configured shared
directories are published through eD2K/Kad according to network state and local
queue policy.

Good sharing starts with intentional roots:

- avoid sharing whole drives or broad home directories
- keep incomplete downloads in Temp, not shared roots
- keep completed downloads in Incoming or curated share roots
- use stable paths and stable drive letters
- avoid high-churn directories unless monitoring is intentional

## Sharing Files

Important sharing files:

| File | Purpose |
|---|---|
| `shareddir.dat` | Main shared directory list |
| `shareddir.monitored.dat` | Roots watched for automatic share changes |
| `shareddir.monitor-owned.dat` | Roots added by monitor ownership |
| `shareignore.dat` | BB-specific ignore rules for share scanning |
| `sharedcache.dat` | Startup cache for large shared libraries |
| `shareddups.dat` | Duplicate path cache |
| `known.met`, `known2_64.met` | Known shared-file metadata and AICH state |

Use the Shared Files page for normal operation. Use text-file editors from
Tools only for controlled maintenance.

## Share Ignore Rules

`shareignore.dat` prevents unwanted paths or patterns from being published.

Use it for:

- temporary files
- generated artifacts
- private sidecar files
- folders managed by another tool
- file patterns that should never be shared

After editing, use the matching Tools reload action. Share-ignore is eMule
BB-specific policy; older stock clients do not understand why BB ignored a
matched file.

## Monitored Shares

Monitored shares are useful when another trusted workflow deposits files into a
known directory. They reduce manual reload work but should be scoped narrowly.

Good monitored-share targets:

- curated completed media folders
- dedicated incoming archive folders
- stable automation output folders

Poor targets:

- whole drives
- build/temp directories
- browser download folders
- cloud-sync roots with constant churn

The current watcher has practical Windows handle limits. If many roots are
needed, prefer fewer higher-quality curated roots rather than monitoring every
folder independently.

Monitored-share files are part of the profile. Back them up with the rest of
the config directory, and edit them only while the app is closed or through the
matching Tools actions when available.

## Large Library Operation

Large libraries need predictable scanning:

- add roots gradually
- keep roots stable
- avoid recursive noise
- use long-path capable Windows setup for deep trees
- let the first scan and hash queue finish
- avoid judging performance during first-run cache creation

Released startup-cache behavior stores verified shared-library state so later
starts can avoid repeating expensive work. If cache sidecars are deleted, the
app can rebuild them, but the next startup or scan may be slower.

The duplicate-path cache helps avoid repeating path resolution and duplicate
work across large trees. Treat `sharedcache.dat` and `shareddups.dat` as
derived profile sidecars: useful for performance, safe to rebuild when
intentionally troubleshooting, but not a substitute for `known.met` or the
configured share-root list.

## Startup Cache Behavior

`sharedcache.dat` is an acceleration cache for the Shared Files startup path.
It is intentionally disposable. eMule BB should never publish stale shared-file
state merely because a cache file exists; if validation is incomplete,
ambiguous, or inconsistent, the app rescans the affected directory and can
write a fresh cache later.

The cache stores per-directory records derived from the configured share roots
and known-file metadata. A usable record includes the canonical shared
directory path, directory identity when Windows can provide it, directory
timestamp, validation mode, cached file count, and cached file entries. Cached
file entries use the file leaf name, file timestamp, and file size to reconnect
startup state with existing `known.met`/`known2_64.met` metadata.

Two validation modes are used:

| Mode | When used | What must match |
|---|---|---|
| Local NTFS journal fast path | Local NTFS volumes with a usable USN journal | Volume key, volume serial, journal ID, checkpoint range, directory file reference, directory identity, directory timestamp, and absence of relevant journal changes |
| Generic file verification | Non-NTFS volumes, remote shares, unsupported path forms, or any case without trusted journal state | Directory identity/timestamp where available, plus a fresh directory inventory matching cached leaf names, timestamps, and sizes |

For the local NTFS path, eMule BB resolves the containing volume instead of
trusting only the textual path. That matters for Windows drive letters and
mounted folders:

- `D:\Shares\Media` on a local NTFS drive can use trusted journal validation.
- `C:\Mounts\Archive\Media` can also use trusted journal validation when the
  mount target is a local NTFS volume with a usable journal.
- Moving a share between different local volumes changes the resolved volume
  identity, so old cache data is rejected for that path.
- A UNC share mapped to a drive letter, such as `Z:\Media` backed by
  `\\server\share`, is reported by Windows as a remote drive. It does not use
  local NTFS journal validation and falls back to generic verification.
- Direct UNC paths and unsupported path forms also avoid the trusted local NTFS
  fast path. They are safe, but may need more startup enumeration.

The NTFS journal fast path records a checkpoint from the volume USN journal.
On a later startup, eMule BB verifies that the current volume is the same
volume, the same journal is still active, the checkpoint is still inside the
valid journal range, and no journal records since that checkpoint affect the
tracked shared directory. If the journal was reset, truncated before the
checkpoint, cannot be read, or reports a relevant directory or child-file
change, the app rejects the fast path and rescans.

The generic path performs a current directory enumeration before using cached
entries. The current inventory must exactly match the cached inventory after
sorting by leaf name, timestamp, and size. Extra files, missing files, renamed
files, case changes, timestamp changes, and size changes reject the generic
cache record for that directory. This fallback is safe for remote and
non-journal filesystems, but it is not a cryptographic content check; it relies
on the same name/date/size identity that classic known-file reuse already uses
when journal proof is unavailable.

Cache records are also rejected when:

- the cache file has the wrong magic, version, structure, or incomplete data
- the configured share directory no longer exists or cannot be queried
- the share root resolves to a different verified directory identity
- the directory timestamp differs from the cached timestamp
- required known-file metadata for a cached entry is missing
- a file is excluded by share-ignore rules or no longer qualifies for sharing
- hashing is still pending for the directory when the save snapshot is taken
- the app abandons or invalidates a cache save before it is committed

Cache writes use temporary files and replacement so a failed write should not
turn the cache into source-of-truth state. If startup cache diagnostics show a
reject reason, the normal recovery action is to rescan shared files. Removing
`sharedcache.dat` is safe when deliberately forcing a rebuild; do not remove
`known.met`, `known2_64.met`, or `shareddir.dat` unless following a separate
profile-recovery procedure. See the
[Persistence Files](GUIDE-PERSISTENCE-FILES.md) reference for recovery priority
and `.met`/`.dat` file roles.

## Shared Files UI

The Shared Files page is the main view for:

- visible shared files
- file details
- ED2K links
- open file/folder actions
- reload/rescan behavior
- sort and curation columns
- large-list operation after virtualization/hardening work

Use view presets if old profiles hide useful columns or preserve cramped widths.

## Long Paths

Deep trees can exceed older Windows path assumptions. eMule BB includes
long-path hardening in important file operations, but the OS, filesystem, and
external tools still matter.

Use [Long Path Guide](GUIDE-LONGPATHS.md) for setup, product behavior, limits,
and troubleshooting. In normal operation:

- keep paths meaningful but not unnecessarily deep
- avoid mixing short-name aliases and long names for the same root
- check diagnostics before assuming a deep tree is stuck

## REST Sharing Surface

REST exposes shared files and shared directories to trusted controllers. The
native UI and hashing/scanning state remain authoritative.

If REST and UI appear to disagree:

1. Wait for hashing/scanning to settle.
2. Compare current REST shared-file snapshots with the Shared Files page.
3. Check startup cache and hash queue diagnostics.
4. Rescan shared files if the filesystem changed outside the app.

## Diagnostics

For sharing problems, collect:

- redacted diagnostic snapshot
- share root list
- monitored-root state
- hash queue count
- startup cache status and reject reason
- duplicate path cache status
- recent share/log lines
- long-path status if paths are deep

## Recovery

If sharing behavior looks wrong:

1. Check configured share roots.
2. Check `shareignore.dat`.
3. Reload share-ignore rules.
4. Rescan shared files.
5. Review diagnostics for startup cache state.
6. Remove cache sidecars only when intentionally forcing a rebuild.
7. Restore from a config backup if the share list itself was edited wrongly.
