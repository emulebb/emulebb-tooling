# Import stock eMule or eMuleBB MFC hashes

Use this offline tool to retain stock hashes when moving complete shared files
to emulebb-rust. It imports MD4 hashes, available full AICH recovery trees,
shared folder roots, discovered file paths, and supported lifetime upload statistics. Files stay in
place. Python owns stock parsing. Rust applies the archive directly to live tables;
its runtime never consults imported or staging tables.

## Requirements

- Close stock/MFC after its hashing finishes. Save a backup of its configuration.
- Obtain a checkout of `emulebb-build-tests` and Python 3.10 or later.
  Python 3.10 additionally needs `python -m pip install "tomli>=2"`.
- Obtain a Rust executable/image supporting portable SQLite imports and full
  AICH recovery sets. An incompatible older build will fail visibly.
- Choose a fresh or compatible, stopped destination profile. Existing profiles
  receive an additive merge: compatible missing data is enriched, existing file
  preferences are retained, and conflicting path/hash bindings are reported.
  Incompatible schemas require a fresh profile; there is no migration or reset.
- For Docker, have the image loaded locally and the Docker daemon running.
  Windows uses Docker through the selected WSL distribution. Linux uses a local
  Docker daemon; remote Docker contexts are unsupported because bind paths are
  local host paths.

No Rust source checkout, build tools, development workspace variables, VPN,
or live-test Python dependencies are required.

## Run one job

From the harness checkout, copy the appropriate example to a local `import.toml`:

| Target | Example in the harness checkout |
|---|---|
| Windows executable | `manifests/profile-import-windows.example.toml` |
| Docker through Windows/WSL | `manifests/profile-import-wsl-docker.example.toml` |
| Docker on Linux | `manifests/profile-import-linux-docker.example.toml` |

Edit the paths and executable/image, then run:

```text
python -B scripts/import-emule-profile.py --config import.toml
```

The same command works for all three examples. It exports, imports, reconciles,
checks imported hashes and path bindings, and exits. It never launches the
ordinary client or executes pending hashing. Keep real jobs and reports private.

## Job fields and mappings

`schema_version = 1` selects the operator job format. This is separate from the
lower-level export-only job format.

- `source.profile`: old installation directory or its `config` directory.
  On Linux, copy the stock configuration here while preserving its encodings.
  Include `known.met`, `known2_64.met`, `preferences.ini`, `shareddir.dat`, and
  any MFC `shareddir.monitored.dat` / `shareddir.monitor-owned.dat` sidecars.
- `source.flavor`: optional `auto` (default), `stock`, or `mfc`.
- `target.backend`: `windows`, `wsl-docker`, or `docker`.
- `target.profile`: destination directory on the machine running Python.
- `target.binary`: executable path for Windows; `target.image`: local Docker
  image for Docker. Images use `/usr/lib/emulebb-rust/emulebb-rust` as their
  offline executable entry point.
- `target.distribution`: WSL distribution, default `Ubuntu`; applicable to
  `wsl-docker`. `target.timeout_seconds` defaults to 7200 per operation.
- `output.directory`: parent directory for dated reports and portable archives.
  Keep it separate from the profile, source configuration, and shared data.

Relative host paths resolve against the TOML file, not the working directory.
Absolute Windows paths use TOML literal strings, such as `'D:\Shared'`.

Windows preserves original shared paths unless mappings are supplied. Every
Docker shared root must have mapping coverage, including stock Incoming.
Each `[[path_mappings]]` entry contains:

| Field | Meaning |
|---|---|
| `source` | Original Windows path recorded in the stock profile |
| `host` | Actual directory visible to the machine running Python |
| `target` | Directory visible to Rust, inside Docker or on Windows |

On Windows without Docker, mapping `host` and `target` must identify the same
directory. Windows junction aliases are compared by filesystem identity.
Profile/report overlap checks resolve both paths, including existing ancestors
of new destinations, to prevent writing into an aliased shared directory.
On Linux, for example, `D:\Shared` can map from host `/srv/shared`
to container `/data/shared`. Matching uses directory boundaries and the longest
source prefix. The importer removes redundant listed descendants but does not
invent unlisted parent shares. Rust shares roots recursively; review stock roots
before importing if stock only shared selected subdirectories.

Docker data and archive mounts are read-only and containers use `--network none`.
Windows/WSL creates temporary read-only media views plus a metadata-enabled
profile view, then unmounts them. It requires permission to mount drvfs through
WSL root. Linux runs the import container with the invoking user's UID/GID;
configure the eventual client container with that same UID/GID. Windows/WSL
uses UID/GID 1000. On Linux, use a filesystem that supports private file modes.

## Read the result before starting Rust

Exit statuses:

| Code | Meaning |
|---|---|
| 0 | Complete reuse; no pending or unresolved file work reported |
| 2 | Import completed but needs attention; valid imported data is retained |
| 1 | Preflight or execution failure; inspect the diagnostic |

Each dated output directory contains `hashes.sqlite`, `summary.json`, and
`audit-baseline.sqlite`. The baseline holds metadata fingerprints from before
apply so verification can prove that rejected existing hashes, bindings, and
recovery trees remained unchanged. It contains no payload data, is separate
from the portable archive, and is never imported or consulted by Rust.
The `emulebb.profile-exchange.v2` archive is read-only during Rust apply; it
retains all stock hash records and available recovery trees, including unmatched
records. Native schema 58 contains no `imported_` tables. Regenerate an archive
from stock metadata if it uses the earlier exchange format.
The summary includes MD4/AICH validation, current path bindings, reused files,
pending hashing, unavailable fingerprints, conflicts, and recovery coverage.
`destinationModified` indicates whether profile import was attempted. Preflight
errors before report creation are printed on the console.

Stock records have no directory paths. Python discovers actual paths using
directory metadata and associates unambiguous filename, size, and whole-second
modification-time matches in `file_paths` in the archive. Rust rechecks those
paths and metadata and binds accepted files to native fingerprints, including
Windows file IDs, directly in live tables. Conflicting and unmatched records
stay in the archive for explicit retries. Normal startup, reload, and uploads
use live tables only. No payload bytes are read to preserve stock hashes.
Rust also checks that supplied MD4 part hashes reconstruct their ED2K identity
and supplied AICH part roots reconstruct their master. These consistency checks
hash metadata only. Database/storage failures are execution failures, distinct
from safely rejected content conflicts.

Missing or rejected AICH recovery data does not invalidate usable MD4 hashes.
Full AICH is preserved when it exists in stock; importing cannot manufacture
missing trees without reading payloads. Missing AICH master hashes are shown by
the difference between known records and recovery-set coverage; sets may also
be shared by duplicate contents.

When Rust rejects an optional recovery set, the tool continues MD4 reconciliation
and returns exit 2. Verification permits a wholly absent rejected set or an
existing complete tree proven unchanged against the baseline. Rejection counts
must account for these outcomes. Partial trees, altered existing metadata, and
unexplained missing sets remain failures. The report separates verified imported
sets, unavailable sets, retained existing trees, and preserved conflicting
records/bindings. A source conflict cannot excuse a changed live record.

If hashing is pending, review roots, mappings, file modifications, and whether
stock finished hashing. Do not start the normal client until you accept that
work: normal startup can hash new or changed files. Inaccessible roots fail
preflight; files becoming inaccessible during execution are reported.

On failure or a needs-attention result, preserve the report, archive, and valid
imported profile. Correct the cause and explicitly retry/merge; the tool never
automatically clears a previous attempt.

Importing stock Incoming makes it shared. It does not set Rust's new-download
destination. Configure that separately. Client identities, credentials, network
settings, server/bootstrap lists, and partial-download queues are not imported.
Rust database upgradeability is a separate workstream.

## Portable archives and advanced use

The retained SQLite archive can be moved to another machine. For explicit
low-level operations, use the existing `export-emule-profile.py` exporter and
Rust commands:

```text
emulebb-rust --profile NEW_PROFILE import-emule-profile hashes.sqlite
emulebb-rust --profile NEW_PROFILE reconcile-shared-files
```

A full archive includes target-platform sharing paths. To import only hashes
into an already configured, compatible profile, the existing low-level
`import-emule-profile --hashes-only hashes.sqlite` command preserves its roots.
The operator tool also merges into an existing compatible profile; its normal
job imports both roots and hashes.

## Import a shared-directory list without Python

```text
emulebb-rust --profile PROFILE import-shared-directories shareddir.dat
```

This native command accepts UTF-8 and BOM-marked UTF-16 LE/BE lists, validates
absolute paths, collapses listed descendants, and merges roots. Consolidation
also removes existing explicit child roots covered by an imported parent;
mandatory roots remain. It then runs the normal offline library scan: unchanged
live fingerprints reuse existing hashes; new or changed files are hashed using
the existing MD4/AICH pass. Networking is never started. The original list and
media files are unchanged. A backup filename such as `shareddir.dat.bak_BAK`
works identically.

The same backend consolidation applies to UI/API additions and bulk updates.
A child already covered by a recursive parent is not added separately. Adding
a parent replaces redundant explicit children; unrelated siblings remain.
Incoming and category roots keep their mandatory internal roles.

Unlike metadata import, a directory list carries no hashes. Its command can
therefore read substantial payload data when the live profile has no reusable
hashes. Import a hash archive first to reuse stock knowledge before adding a
broader directory list. Stock directory lists become recursive Rust roots;
children not shared by stock may consequently become shared by Rust.

Completed file hashes are committed during the pass. If the offline process is
interrupted, rerun the same command with the same profile: completed unchanged
files are reused, and an interrupted file is hashed again. Keep the client
stopped while running these offline operations.
Native content and its successfully cached recovery tree commit atomically.
Download finalization saves available recovery metadata before publishing
completion. An optional cache error still permits valid MD4 work to finish;
the directory-import result reports `missingAichRecoverySets` for accepted live
contents large enough for recovery that have a master but no saved full tree.
Missing optional recovery never schedules a payload read by itself.
