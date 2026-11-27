---
id: RUST-FEAT-148
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/376
title: Serve and browse eD2K peer shared-file lists
status: IN_PROGRESS
priority: Major
category: feature
labels: [rust, beta3-blocker]
milestone: rust-v0.1.0-beta.3
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/376. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-148 - Serve and browse eD2K peer shared-file lists

Rust serves and browses peer shared-file lists over established eD2K sessions. It supports flat and directory views, with Everyone as the fresh-profile default, verified Friends, and Off. Qualification covered capability advertising, virtual directory names, and a 100,000-file Rust catalog. [Rust PR #394](https://github.com/emulebb/emulebb-rust/pull/394)

## Peer contract

- Serve on listener and established outbound sessions. Filter the live
  shareable catalog by negotiated encoding and large-file capabilities. Use
  virtual directory labels and resolve requests only against advertised labels.
  Include eligible verified partials in the flat view, and use the stock
  `!Incomplete Files` label for the partial-directory view.
- Everyone is the approved Rust fresh-profile default. Friends requires an
  enrolled key and its matching verified session proof. A manually added hash
  requires trusted enrollment before it can authorize a browse. First contact
  alone cannot authenticate an existing friend. Off sets the no-view bit.
  The operator can supply the SHA-256 fingerprint of the trusted peer's DER
  key when creating or updating the friend. Removing the friend revokes it.
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
Unicode names, and legacy large-file capability. A 10,000-file catalog per
reference client is sufficient for interoperability. Qualify Rust catalog
capacity separately at 100,000 files.
Verify that no real filesystem paths leave the daemon and normal transfers
remain responsive during browse activity.

Verify the implementation against stock eMule `ac3d52e` and amule-org aMule `c5989ec4a`. Use stock eMule for supported wire behavior where the peers differ.

Use [RUST-CI-031](RUST-CI-031.md) for deterministic fixtures and
[RUST-CI-006](RUST-CI-006.md) to retain same-revision interoperability
evidence when the feature is in the release scope.

The exact PR head `6ba4662f` qualified all four native requester and publisher
directions at 9,964 rows against stock eMule and the official frozen aMule
3.0.1 build. File bytes progressed on the shared connection during browsing
and the completed transfers matched their expected hashes. The Rust 100,000-row
TCP test and stock publisher run are separate capacity evidence.
[Retained interoperability results](https://github.com/emulebb/emulebb-rust/issues/376)

## Follow-up Acceptance

- [ ] Allow a user to browse a known reachable source whose eD2K session is
      closed. Stock eMule and upstream aMule initiate a connection on demand.
      Reuse normal peer admission and the existing session when present.
      Verify an exact canary filename, size and eD2K hash from both stock
      publishers. Exercise duplicate requests, banned peers and unreachable
      peers within the existing bounds.
      [Rust entry point](https://github.com/emulebb/emulebb-rust/blob/045d9a1d5d176132eb6eeea5add2b0bb50c686ab/crates/emulebb-core/src/transfer_control_api.rs#L6) · [Stock eMule](https://github.com/irwir/eMule/blob/ac3d52e/srchybrid/BaseClient.cpp#L1785) · [aMule](https://github.com/amule-org/amule/blob/c5989ec4a/src/BaseClient.cpp#L3557)
- [ ] Compare one outstanding directory request with a small bounded window
      using both native publishers and an active transfer. The aMule baseline
      spent about 116 seconds on the wire across 30 requests, with a
      3.915-second median per reply. Compare exact rows, browse time, transfer
      throughput and pending memory. Keep the catalog and frame bounds, match
      replies to outstanding raw labels, and cover duplicate, unmatched and
      late replies. Adopt a window only after repeatable improvement.
