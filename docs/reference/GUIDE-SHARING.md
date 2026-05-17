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
| `known.met`, `known2.met` | Known shared-file metadata and AICH state |

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
