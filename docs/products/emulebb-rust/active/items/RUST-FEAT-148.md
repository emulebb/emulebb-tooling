---
id: RUST-FEAT-148
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/376
title: Serve and browse eD2K peer shared-file lists
status: OPEN
priority: Major
category: feature
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/376. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-148 - Serve and browse eD2K peer shared-file lists

Beta 3 requires bidirectional browsing against stock eMule and aMule. Serve flat and directory views with Everyone as the fresh-profile default, verified Friends, and Off. Make the existing REST and WebUI browse action fetch bounded peer results. Cover capability advertising, safe virtual directory names, and a 100,000-file catalog.

## Peer contract

- Serve on listener and established outbound sessions. Filter the live
  shareable catalog by negotiated encoding and large-file capabilities. Use
  virtual directory labels and resolve requests only against advertised labels.
- Everyone is the approved Rust fresh-profile default. Friends requires an
  enrolled key and its matching verified session proof. A manually added hash
  requires trusted enrollment before it can authorize a browse. First contact
  alone cannot authenticate an existing friend. Off sets the no-view bit.
- Match stock access denials. A prohibited flat request returns an empty list.
  Prohibited directory requests receive the shared-list denial. An authorized
  request for an unknown directory echoes the label and returns zero entries.
- Serve the complete list when the flat result fits the peer frame. For an
  oversized flat result, explicitly signal denial and retain the directory
  alternative. Stock browse has no continuation packet. Directory groups must
  fit the common 2,000,000-byte payload limit at supported library scale.
- Reuse the existing download-source browse action. Prefer directory browsing
  when the peer supports it and accept a flat list from a legacy peer. Allow
  one browse per connection, correlate directory replies to requests, and
  expose bounded status and paged results separately from global search.

## Qualification

Prove both directions against each oracle. Cover empty, denied, unsupported,
timeout and disconnected responses, Friends enrollment and revocation,
Unicode names, legacy large-file capability, and a 100,000-file catalog.
Verify that no real filesystem paths leave the daemon and normal transfers
remain responsive during browse activity.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.
