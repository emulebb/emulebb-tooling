# Persistence Files

This reference documents the current eMuleBB runtime `.met` and `.dat` files
found in the app source. It covers file roles, ownership, broad structure, and
maintenance risk. It is not a replacement for the source readers and writers;
use it as the map before touching a profile, writing migration code, or
debugging profile corruption.

Most files live in the config/profile directory. Active download metadata lives
beside the incomplete `.part` data in the configured temp directory.

## Maintenance Rules

- Close eMuleBB before hand-editing or replacing profile files.
- Back up the full config directory and all temp directories before profile
  migration or recovery work.
- Do not hand-edit binary profile files such as `preferences.dat`, `known.met`,
  `known2_64.met`, `clients.met`, `.part.met`, `server.met`, or `nodes.dat`.
- Text policy files such as `shareignore.dat`, `shareddir.dat`,
  `staticservers.dat`, `webservices.dat`, and `PreviewApps.dat` are intended
  for controlled editing.
- Cache files can usually be deleted to force rebuild, but identity, credits,
  known-file, part-file, and Kad preference files should be restored from backup
  instead of deleted during normal recovery.

Companion files such as `.tmp`, `.new`, `.bak`, `.backup`, and `temp-*`
candidates are save, backup, download, or recovery artifacts. They are not
separate profile authorities.

## Format Families

| Family | Files | Shape |
|---|---|---|
| Tag-vector `.met` | `known.met`, `.part.met`, `server.met` | Binary header plus records carrying typed tags. Unknown tag IDs are usually skippable when the tag type is known. |
| Fixed binary state | `preferences.dat`, `preferencesKad.dat`, `nodes.dat`, `known2_64.met`, Kad indexes | Versioned or fixed-field binary structures. Treat as implementation-owned. |
| Text lists | `shareddir.dat`, `shareignore.dat`, `addresses.dat`, `staticservers.dat`, autocomplete `.dat` files | Line-oriented or simple text lists, normally editable through Tools or UI. |
| Derived caches | `sharedcache.dat`, `shareddups.dat`, `FakeFile.met`, Kad indexes | Rebuildable acceleration or analysis state. Deletion can slow the next startup or scan. |

Many legacy `.met` timestamps are stored as unsigned 32-bit Unix seconds. That
does not have the signed-2038 storage limit, but the stored range still ends in
2106 and careless signed consumers can still mishandle values after 2038.

## Identity And Peer State

- `preferences.dat`: legacy binary preference and local identity state that
  complements `preferences.ini`. Preserve it and do not hand-edit it.
- `preferencesKad.dat`: local Kad identity and Kad preference state. Current
  saves validate and promote prepared candidates; preserve it for Kad
  continuity.
- `cryptkey.dat`: Base64 private key material for secure user identification
  and credit signing. Preserve it and keep it private.
- `collectioncryptkey.dat`: Base64 key material for signed collection files.
  Preserve it if signed collections matter.
- `clients.met`: peer credit database keyed by user hash. Preserve it for
  credit continuity and do not hand-edit it.
- `emfriends.met`: friend list with hashes and last-known connection fields.
  Preserve it for friend list continuity.

## Known, Shared, And Download State

- `known.met`: canonical known-file database for shared files and remembered
  downloads. It stores file dates, MD4 hashsets, tags, AICH tags, last-shared
  time, and all-time transfer/request statistics. Current saves use a temporary
  file and atomic replacement.
- `known2_64.met`: AICH recovery hashset store for known complete files. It is
  not general file metadata. The structure is `uint8` version `0x02`, then
  repeated AICH master hash, `uint32` hash count, and 20-byte hashes.
- `known2.met`: legacy AICH recovery hashset input converted to
  `known2_64.met` when needed. Do not add new metadata here.
- `cancelled.met`: cancelled-download hash memory. It uses a binary
  header/version/seed/count plus hash records and tags, and is saved through the
  known metadata atomic path.
- `*.part.met`: per-download resume metadata: file identity, hashes, name/size,
  priorities, categories, transfer stats, gaps, corrupted parts, and AICH state.
  It is critical for incomplete downloads and should not be hand-edited.
- `*.part.met.bak`: previous `.part.met` snapshot kept for recovery. Keep it
  with its active download.
- `*.part.met.backup`: additional recovered or imported part metadata backup.
  Keep it during recovery investigations.
- `sharedfiles.dat`: single-file share list outside normal shared-directory
  roots. Preserve it if single-file shares are used.
- `sharedcache.dat`: startup acceleration cache for large shared libraries.
  It reconnects directory snapshots to `known.met` metadata. It is disposable;
  deletion forces a slower rescan.
- `shareddups.dat`: duplicate shared-path cache. It is disposable and can be
  rebuilt.

`known.met` and `.part.met` are tag-based and are the natural place for durable
file statistics. `known2_64.met` is keyed by AICH hash and stores only recovery
hashsets, so it should not be used for GUI statistics or request timestamps.

## Sharing Policy Files

- `shareddir.dat`: main configured shared-directory roots. It is a text path
  list and is user-editable while the app is closed or through Tools.
- `shareddir.monitored.dat`: roots watched for automatic share changes. It is a
  text path list; edit with care.
- `shareddir.monitor-owned.dat`: directories added and owned by
  monitored-share automation. Prefer app-managed edits.
- `shareddir.monitor-journal.dat`: monitored-share journal state used to track
  observed root state. Preserve it for continuity, or rebuild by rescanning.
- `shareignore.dat`: additive ignore rules for shared-file scanning. It is a
  commented text rule file; reload through the app after edits.
- `FakeFileFilter.dat`: local fake-file signal rules. It is user-editable when
  maintaining fake-file detection inputs.
- `FakeFile.met`: fake-file analyzer cache. It is disposable; deletion loses
  cached analysis only.

## Network And Bootstrap Files

- `server.met`: persisted eD2K server list and imported server-list payload
  format. It uses binary server records with typed tags. Current update paths
  validate candidates before promotion.
- `staticservers.dat`: user-maintained static eD2K servers. It is a text list.
- `addresses.dat`: server-list update URLs, seeded when missing or blank. It is
  user-editable text.
- `nodes.dat`: Kad routing/bootstrap contact snapshot and downloaded bootstrap
  payload format. It stores binary Kad contacts and supports normal and
  bootstrap-only handling. Current import validates before replacement.
- `nodes.fastkad.dat`: eMuleBB Fast Kad sidecar with contact health and
  response metadata. It improves bootstrap quality and can rebuild over time.
- `src_index.dat`: Kad indexed source records. This is derived local DHT state.
- `key_index.dat`: Kad keyword index records. This is derived local DHT state.
- `load_index.dat`: Kad load-tracking index records. This is derived local DHT
  state.

## Filters, Services, And Tools Files

- `ipfilter.dat`: IP filter rules for peers, sources, Kad contacts, and
  servers. It is text ranges with level and optional description; see the IP
  Filters guide for syntax.
- `webservices.dat`: external web-service command definitions used by UI
  actions. It is commented text configuration.
- `PreviewApps.dat`: preview application command configuration. Keep command
  quoting narrow and explicit.
- `onlinesig.dat`: small online-signature status output for external consumers.
  It is runtime output and is usually not edited.

## UI History And Autocomplete Files

- `AC_BootstrapIPs.dat`: Kad bootstrap IP autocomplete/history.
- `AC_IPFilterUpdateURLs.dat`: IP filter update URL autocomplete/history.
- `AC_SearchStrings.dat`: search string autocomplete/history.
- `AC_ServerMetURLs.dat`: server-list URL autocomplete/history.
- `AC_VF_RegExpr.dat`: view/filter regular-expression autocomplete/history.
- `SearchSpam.met`: app-managed search spam filter state. It can be rebuilt
  from future search activity.
- `StoredSearches.met`: stored search state. Preserve it if stored searches
  matter.

Autocomplete files are text lists. Deleting them is safe, but it loses local
history.

## Temporary And Backup Patterns

| Pattern | Role | Maintenance |
|---|---|---|
| `*.tmp`, `*.new` | Prepared save candidates used before replacement. | Normally transient. Investigate only after failed saves. |
| `*.bak`, `*.backup` | Prior snapshots or recovery backups. | Keep until the corresponding live file is known good. |
| `temp-*-server.met`, `temp-*-nodes.dat` | Downloaded update candidates before validation and promotion. | Transient. Not authoritative profile state. |
| `*.part.met.tmp` | Prepared part-file metadata save candidate. | Transient. Live `.part.met` and backups are authoritative. |

## Recovery Priorities

If a profile is damaged, restore files in this order:

1. Identity and trust: `preferences.dat`, `preferencesKad.dat`, `cryptkey.dat`,
   `clients.met`.
2. Incomplete downloads: all `.part`, `.part.met`, `.part.met.bak`, and
   `.part.met.backup` companions from the temp directories.
3. Known/shared metadata: `known.met`, `known2_64.met`, `cancelled.met`,
   share directory files, and monitored-share files.
4. Network startup state: `server.met`, `nodes.dat`, `nodes.fastkad.dat`,
   `addresses.dat`, and `staticservers.dat`.
5. Caches and histories: shared caches, Kad indexes, fake-file cache,
   autocomplete files, and online-signature output.

When in doubt, keep the file and let the app decide whether it is usable. The
current code has validation and recovery paths for several critical files, but
manual deletion can discard evidence that would otherwise be recoverable.
