---
id: FEAT-039
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/16
title: Download checker — duplicate and near-duplicate intake guard
status: OPEN
priority: Minor
category: feature
labels: [downloads, duplicates, file-handling, safety, blacklist, intake]
milestone: ~
created: 2026-04-20
source: eMuleAI release notes
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/16. This local document is retained as an engineering spec/evidence record.

## Summary

Add an intake-time checker that evaluates a new download against existing downloads,
history, and shared files before the item is accepted.

The intent is to catch obvious duplicates, suspicious near-duplicates, and repeated junk
before they clutter the queue.

## Intended Mainline Shape

- compare new downloads against current downloads, known history, and shared inventory
- detect exact duplicates first and optionally warn or reject
- allow looser near-duplicate heuristics as an advanced mode
- optionally auto-blacklist or auto-hide clearly bad repeat items
- present the result as a user-facing decision rather than silently overriding everything

## Why Add It

This is a file-handling convenience feature with real operator value on long-running nodes:

- fewer accidental duplicate downloads
- less queue clutter
- less repeated junk from fake/spam-prone searches

## eMuleAI Implementation References

Review source: eMuleAI commit
[`8e34bdec2b7e4fe9e4307df9d80f691804be99ed`](https://github.com/emulebb/emulebb-ai/tree/8e34bdec2b7e4fe9e4307df9d80f691804be99ed).

- duplicate map load/update/remove/check paths:
  [`DownloadChecker.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/DownloadChecker.h#L10),
  [`DownloadChecker.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/DownloadChecker.cpp#L32),
  [`DownloadChecker.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/DownloadChecker.cpp#L72),
  [`DownloadChecker.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/DownloadChecker.cpp#L139).

## eMuleBB Direction

Start with exact ED2K hash matches against current downloads, completed known
files, and shared files. Near-duplicate heuristics should be later and
user-visible because filename/size similarity can produce false positives.

## Additional Hashes And MD4 Uniqueness

The ED2K file hash should remain the compatibility identity. It is MD4-based,
which means it is old and cryptographically broken, but still extremely useful
for accidental exact-file uniqueness.

For normal media-library and download-queue use, accidental MD4 collisions are
not the practical risk. A 128-bit hash space is large enough that exact-byte
duplicate detection across realistic local libraries, shared inventories, and
download histories is effectively unique. Even at internet-scale catalog sizes,
random collision odds stay tiny compared with ordinary operator problems such
as duplicate encodes, renamed files, tag changes, bad metadata, fake search
results, and partial or corrupt downloads.

The important boundary is adversarial input. MD4 must not be treated as modern
security proof: a motivated attacker can create different byte streams with the
same MD4 far more cheaply than with SHA-256 or BLAKE3. That does not make ED2K
identity useless; it means new stronger hashes should be additive. Use MD4/ED2K
for stock network compatibility and exact-byte legacy identity, then use
SHA-256, BLAKE3, or another strong local sidecar hash when eMuleBB needs extra
confidence for local duplicate checking, diagnostics, or controller metadata.

For "same media" detection, no cryptographic hash is enough by itself. Different
encodes, remuxes, subtitles, tags, cover art, or container metadata will produce
different MD4, SHA-256, and BLAKE3 values. Near-duplicate media detection should
stay a separate optional heuristic or fingerprinting feature, not a property of
the ED2K hash.

## Scope Constraints

- exact-duplicate checks should be deterministic and cheap
- near-duplicate mode must stay optional because false positives are possible
- this feature should complement, not replace, the `KnownFileList` correctness fixes under
  `BUG-037`
- a local strong-hash cache such as a SHA-256 or BLAKE3 sidecar is a valid
  future implementation aid for exact-duplicate confidence, but it is not
  required for the first version
- if a stronger hash is ever exposed on the network, it should start as
  advisory extra metadata for upgraded peers only, not as a replacement for
  MD4/ED2K identity

## Acceptance Criteria

- [ ] exact duplicates can be detected before a new download is added
- [ ] operators can choose warn/reject/allow behavior
- [ ] optional near-duplicate mode can be enabled separately
- [ ] clearly blacklisted repeat items can be filtered automatically when configured
- [ ] no regression for normal add-download flows when the feature is disabled
- [ ] exact-hash duplicate behavior is covered before any fuzzy/near-duplicate
      rule is enabled
