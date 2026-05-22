# Long Path Guide

This guide explains how eMuleBB behaves with Windows paths that may exceed the
classic 260-character limit. It is product documentation for users, operators,
and support work. It does not describe source-code changes.

## What Long Path Support Means

Long path support lets eMuleBB work with deep directory trees and long file
names in common file workflows:

- scanning shared directories
- hashing and publishing shared files
- reading files for upload
- writing incomplete downloads
- completing downloads into incoming or category folders
- reading media metadata and preview data where supported
- maintaining profile backups and text configuration files

This matters most for users with large archive libraries, organized media
trees, long descriptive filenames, or nested category/share structures.

Long path support does not make every Windows shell operation or external tool
long-path safe. eMuleBB can be long-path aware while another player, editor,
archive tool, or shell extension still fails on the same path.

## Windows Requirements

Long path behavior depends on both the app and Windows.

Required environment:

- Windows 10 version 1607 or newer, or Windows 11
- system long-path policy enabled
- an eMuleBB build that declares long-path awareness
- a filesystem and external tools that can tolerate the target paths

The Windows policy is named `LongPathsEnabled` under the system filesystem
policy area. It can be enabled by Group Policy, enterprise policy, direct
registry configuration, or `Tools > Maintenance > Enable Windows Long Paths`.
Restart the app after changing the policy.

If the Windows policy is disabled, shorter paths continue to work normally, but
some very deep operations can still fail or be skipped with diagnostics.

## Good Path Hygiene

Long-path support is not a reason to let paths grow without discipline.

Recommended practice:

- keep incoming and temp roots reasonably short
- avoid placing the profile under a very deep directory
- use stable drive letters or stable mount points
- avoid redundant nested folder names
- keep category names short when category incoming paths are used
- avoid mixing short-name aliases and long-name paths for the same root
- avoid sharing whole drives or broad user-profile roots

Shorter base roots give more room for descriptive filenames and reduce the
chance that external tools fail.

## Profile And Config Paths

The config/profile directory contains identity, preferences, network state,
logs, lists, and sidecar files. Keep this path stable and moderate in length.

Long profile paths can affect:

- profile backup creation
- config-file editors launched from Tools
- log opening
- diagnostic dump placement
- WebServer template or asset lookup
- sidecar cache files for sharing and monitoring

If a profile path is too deep, move the whole profile while the app is closed
and start eMuleBB with the intended config location.

## Incoming And Temp Paths

The temp directory holds active incomplete downloads. The incoming directory
holds completed files.

Long-path considerations:

- deep temp paths add length to every incomplete part file
- long category incoming paths add length at completion time
- file completion can fail if the destination path is valid for eMuleBB but
  not valid for an external filesystem filter, antivirus tool, shell handler,
  or destination volume
- keeping temp and incoming roots short reduces completion risk

For reliability, prefer short base roots such as a dedicated data drive folder,
then use categories and filenames for organization.

## Shared Directories

Shared roots are the most common long-path stress point.

eMuleBB can scan and hash deep shared trees, but operators should still keep
shares intentional:

- share curated roots, not entire drives
- avoid high-churn folders unless monitoring is intentional
- use `shareignore.dat` to exclude generated, private, temporary, or noisy paths
- let initial scanning and hashing finish before judging performance
- use diagnostics when a large tree appears stuck

If a deep file is not shared, check whether the path was skipped, ignored,
unreadable, blocked by policy, or still waiting for hashing.

## Monitored Shares

Monitored shares watch selected roots for changes. They are useful for stable
automation output folders but should not be used as a blanket filesystem
watcher.

Long monitored paths can make troubleshooting harder because a failure may come
from the watcher, the scan, the target file, or an external filesystem layer.

Recommended use:

- monitor a small number of curated roots
- keep monitored root paths shorter than the files below them
- avoid cloud-sync roots with constant churn
- reload or rescan after changing ignore rules

## Downloads And Completion

Long filenames often arrive from search results or ED2K links. eMuleBB should
preserve valid names where practical, but completion still depends on the final
destination path.

Before downloading files with very long names:

- choose a short incoming root
- choose a short category incoming path
- avoid adding extra nested folders manually
- review filename cleanup behavior
- verify the target volume and external tools can open the completed path

If completion fails, do not delete the download immediately. Check logs,
diagnostics, destination path length, free space, antivirus activity, and
whether the target path already exists.

## Preview, Metadata, And Archives

Preview and metadata paths can involve optional external components. Long path
support varies by component.

Expected behavior:

- eMuleBB can attempt supported internal reads on long paths
- optional media metadata libraries may have their own limits
- external preview players may reject paths that eMuleBB can store
- archive preview/recovery is legacy behavior and should not be treated as the
  primary way to validate long-path support

When preview or metadata fails but the file otherwise downloads or shares
correctly, treat the failure as a preview/tool compatibility issue first.

## Tools Menu Behavior

Tools actions are useful for long-path operation:

- open config, temp, incoming, logs, and executable folders
- edit text config files
- reload share-ignore and filter files
- rescan shared files
- save preferences
- enable the Windows long-path policy through an elevated one-time action
- copy redacted diagnostic snapshots
- capture dumps for hangs or crashes

Some folder-opening and shell actions can still be limited by Windows Explorer,
shell extensions, file associations, or external editors. If a Tools action
fails but the underlying transfer or share works, test the path with a shorter
external tool chain before changing eMuleBB settings.

## Compatibility With Older Clients

Older stock clients may not understand all eMuleBB path behavior, sidecars, or
profile additions.

Avoid round-tripping one live profile between eMuleBB and older clients when it
contains long paths. Older clients may fail to open, move, share, preview, or
clean up files that eMuleBB can handle.

If rollback is required, restore from a profile backup made before long-path
operation became active.

## Known Limits

Long path support is broad but not unlimited.

Known practical limits:

- Windows policy must be enabled for full OS-level behavior
- external players, editors, shell extensions, and archive tools may still fail
- recycle-bin behavior can be more limited than direct delete/move behavior
- network peers do not care about local path length, but local file operations do
- very deep paths are harder to diagnose and easier to break with external tools
- some UI display strings may be shortened or wrapped even when the operation
  succeeds

The safest operating model is still short base paths plus descriptive filenames.

## Verification Checklist

Use this checklist after enabling long path policy or moving to a deeper
library:

1. Restart eMuleBB.
2. Confirm incoming and temp roots are short and writable.
3. Add one deep shared test folder.
4. Rescan shared files.
5. Confirm the file appears in Shared Files after hashing.
6. Copy its ED2K link.
7. Start a small download whose final destination has a long path.
8. Confirm completion into the intended incoming or category folder.
9. Open a redacted diagnostic snapshot and verify paths and share state.
10. Test any external player or editor separately.

Do not validate long-path readiness by changing a full production library all at
once.

## Troubleshooting

Deep shared file does not appear:

1. Check that the root is actually shared.
2. Check `shareignore.dat`.
3. Reload share-ignore rules.
4. Rescan shared files.
5. Check logs for skipped or inaccessible paths.
6. Check diagnostics for hash queue and startup cache state.

Download completes but move fails:

1. Check destination path length.
2. Check whether the destination already exists.
3. Check free space and write permissions.
4. Temporarily choose a shorter category incoming path.
5. Check antivirus or filesystem filter logs.
6. Keep the `.part` data until the cause is clear.

Preview or metadata fails:

1. Confirm the file exists and is readable.
2. Try a shorter path.
3. Try a different external player or metadata tool.
4. Treat archive preview as legacy and non-authoritative.

Tools folder/editor action fails:

1. Try opening the parent folder manually.
2. Try a shorter editor path.
3. Check whether Explorer or the associated tool is the failing component.
4. Use diagnostics and logs before moving profile files.

## Support Evidence

When reporting long-path issues, include:

- Windows version
- whether long-path policy is enabled
- redacted diagnostic snapshot
- relevant log lines
- path role: profile, temp, incoming, shared, monitored, category, preview
- whether the operation fails inside eMuleBB or only in an external tool
- whether a shorter equivalent path works

Use redacted snapshots for shared support unless exact local paths are required
privately.
