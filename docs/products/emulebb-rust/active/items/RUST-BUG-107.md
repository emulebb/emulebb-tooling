---
id: RUST-BUG-107
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/78
title: Preserve lossless shared-library path identity across platforms
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, sharing, paths, unicode, metadata, portability]
milestone: rust-v0.1.0-beta.3
created: 2026-10-03
source: 2026-10-03 large-library I/O and portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/78. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-107 - Preserve lossless shared-library path identity across platforms

## Summary

Separate human/search normalization from filesystem identity so distinct legal
shared-file paths cannot collapse in SQLite and native paths can be reopened
without lossy Unicode conversion. Define and prove the support policy for
non-UTF-8 Unix filenames, Unicode normalization variants, Windows case-sensitive
directories, aliases, hard links, and coarse-timestamp filesystems. This is a
beta.3 clean-schema change: incompatible profiles fail visibly and require a
fresh profile; product code does not migrate or repair old path rows.

## Current State

- `local_paths.normalized_key` uses Unicode NFKC on every platform and lowercases
  Windows paths. NFKC is appropriate for search but can make two distinct legal
  filesystem names share one database identity.
- `local_paths.native_path` is a BLOB, but it currently stores the UTF-8 bytes of
  the display string rather than the native `OsStr` representation.
- Shared-directory planning, rename handling, and display-name extraction have
  `to_str()`/display-string boundaries. Arbitrary non-UTF-8 Unix names therefore
  cannot round-trip.
- The incremental cache compares path, size, and millisecond mtime. A same-size
  offline change can be missed on a filesystem with coarse timestamp resolution.
- Windows long-path construction preserves normal Unicode names but joins some
  components through lossy string conversion, so the full native namespace is
  not represented exactly.

## Why This Matters

For a 100k-file library, one path collision can overwrite the durable identity
used for reuse, rename, removal, and upload serving. Portability requires exact
filesystem identity even when the UI and network protocol continue to expose a
Unicode display name.

## Representative Sites

- `crates/emulebb-metadata/src/text.rs` `normalize_path_key`
- `crates/emulebb-metadata/src/store.rs` `upsert_local_path`
- `crates/emulebb-metadata/src/schema.sql` `local_paths`
- `crates/emulebb-ed2k/src/long_path.rs` `windows_long_path`
- `crates/emulebb-ed2k/src/ed2k_transfer/reload_index.rs`
- `crates/emulebb-core/src/shared_directories.rs` `target_name`
- `crates/emulebb-core/src/shared_dir_monitor.rs` rename handling

## Intended Shape

- Introduce one native path identity boundary used by metadata, reload indexes,
  watcher state, relocation, and long-path construction. Store Unix `OsStr`
  bytes or Windows UTF-16 code units exactly, with a separate safe Unicode
  display path and search key.
- Do not apply NFKC or compatibility folding to the native identity. Retain that
  normalization only for search/display matching.
- Record stable filesystem identity where available: device/inode on Unix and
  volume/file ID on Windows. Use it to recognize aliases and hard links without
  conflating distinct files.
- Record nanosecond-resolution timestamps and the strongest portable change
  identity available. Rehash conservatively when the filesystem exposes only a
  coarse or otherwise ambiguous timestamp; unchanged reuse must not depend on a
  same-size millisecond timestamp alone.
- Support non-UTF-8 Unix filenames for filesystem identity and file access. Use
  a deterministic escaped Unicode display name for UI and wire surfaces, and
  expose diagnostics whenever such a display surrogate is required.

## Scope Constraints

- Preserve user-visible Unicode names and ED2K/Kad UTF-8 filename behavior.
- Do not canonicalize directory-entry paths in a way that repeats the prior
  Windows Unicode re-normalization failure.
- Bump the clean schema. An older profile fails through the existing
  incompatible-profile path and instructs the user to create a fresh profile;
  do not add migration, fallback reads, repair, or compatibility aliases.
- Storage-device scheduling is tracked separately by `RUST-REF-009`.

## Acceptance Criteria

- [ ] Compatibility-equivalent but distinct legal names do not collide in
      `local_paths`.
- [ ] Supported native paths round-trip through SQLite and reopen the same file
      on Windows, Linux, and macOS.
- [ ] Non-UTF-8 Unix filenames remain shareable through exact native identity,
      use deterministic escaped display names, and emit explicit diagnostics.
- [ ] Windows long-path construction has no lossy component conversion.
- [ ] Case-sensitive Windows directories and case-insensitive/default macOS
      volumes have capability-aware identity tests.
- [ ] Incremental reuse cannot silently accept a same-size changed file solely
      because a coarse mtime value is unchanged.
- [ ] The schema version changes and an older profile fails visibly without
      mutation, migration, fallback reads, or partial acceptance.

## Validation

- Metadata migration and collision tests using synthetic NFC/NFD,
  compatibility-equivalent, case-variant, CJK, emoji, and bracketed names.
- Platform-native integration tests for open, hash, restart, rename, delete, and
  upload serving.
- Capability-gated non-UTF-8 Unix and Windows case-sensitive-directory tests.
- The scale matrix tracked by `RUST-CI-008`.
