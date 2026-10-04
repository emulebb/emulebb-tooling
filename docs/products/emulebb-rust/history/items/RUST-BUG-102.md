---
id: RUST-BUG-102
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/23
title: Require a stock-compatible final completion rehash
status: DONE
priority: Major
category: bug
labels: [rust, ed2k, transfer, integrity, aich, parity]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against eMule 0.72a and current aMule 3.1
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/23. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-102 - Require a stock-compatible final completion rehash

## Summary

Do not expose a completed download until a whole-file MD4/ED2K rehash has
validated the assembled bytes. Rust currently verifies each part as it arrives
and records completion, but delivery trusts the persisted completed manifest.
Stock eMule and current aMule both retain a distinct final hashing/completing
transition before the file becomes deliverable.

## Original State

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs` verifies a completed
  part by reading it back, then marks the part complete. It also exposes a
  manual `recheck_transfer` path.
- `crates/emulebb-core/src/delivery.rs` accepts the completed-part manifest as
  sufficient for delivery; no automatic final whole-file recheck is required.
- Stock eMule enters its completing state and hashes the assembled file in
  `workspaces\workspace\app\emulebb-main\srchybrid\PartFile.cpp` before the
  completed file transition.
- Current aMule follows the same completion-after-rehash model in
  `analysis\amule\src\PartFile.cpp` and can use AICH recovery when rehashing
  identifies damaged data.

The gap matters even when every inbound part initially verified: storage can be
mutated after verification, state can survive a crash, and a stale or damaged
manifest can be loaded on restart.

## Why This Matters

Publishing or moving bytes under the expected ED2K identity without validating
the final assembled file violates the integrity boundary users expect from
stock clients. It can also make later corruption look like remote peer failure
rather than local persistence damage.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_transfer\piece_store.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-core\src\delivery.rs`
- `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main\srchybrid\PartFile.cpp`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\PartFile.cpp`

## Intended Shape

- Add an explicit completing/hashing state between all-parts-present and
  deliverable.
- Automatically calculate and compare the complete ED2K MD4 identity before
  first delivery, including recovery after restart into a pending-delivery
  state.
- If the check fails, demote the affected part or parts from complete and make
  them eligible for download again; use available AICH information to localize
  or recover corruption without weakening MD4 acceptance.
- Persist the transition so a crash cannot skip the final check or make a
  partially delivered file appear complete.
- Keep the existing manual recheck as an operator action, but do not rely on it
  for the normal completion guarantee.

## Scope Constraints

- Preserve the ED2K part hash and AICH verification already applied on receipt.
- Do not deliver, share, or announce the destination file before the final
  identity check succeeds.
- Do not accept an AICH result as a substitute for the ED2K file hash.
- Recovery must be bounded and must not silently discard a user's valid file.

## Acceptance Criteria

- [x] Normal completion automatically enters a visible completing/hashing state
      and performs a full assembled-file ED2K rehash.
- [x] Delivery is impossible until the final identity check succeeds.
- [x] Mutating a previously verified part before the last part arrives causes
      completion to fail and the damaged range to become incomplete again.
- [x] Restarting with every part marked complete but damaged bytes on disk
      performs the same check before delivery.
- [x] A clean restart in the pending-delivery state completes without
      redownloading valid data.
- [x] AICH-assisted localization/recovery, when available, retains the MD4 file
      hash as the final acceptance authority.

## Resolution

- Added schema v24 with a persisted `final_rehash_pending` barrier and a visible
  `completing` state between all-parts-present and delivery.
- Routed normal completion, startup recovery, and manual recheck through one
  whole-file ED2K MD4 authority. Delivery now rejects pending transfers.
- On mismatch, authoritative part MD4 hashes demote only corrupt pieces and
  queue AICH-assisted repair metadata; failures that cannot be localized fail
  closed instead of publishing unverified bytes.
- Added a backup-first v23-to-v24 migration for completed but undelivered rows.
- Added source-bound direct NAT-PMP v0 fallback and finite-lease MiniUPnPc retry
  while exercising the completion change through native and VPN live lanes.

## Evidence

- Rust commits `9edda9af` and `94f1ebdc`.
- Full Rust workspace regression: all unit, integration, and doc tests passed.
- Harness regression: `2122 passed, 6 deselected`.
- Final Windows Release/diagnostics build (zero warnings):
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\logs\builds\20261004T101037Z-build-clients`.
- Final Linux package boundary evidence:
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\reports\rust-linux-package-launch\20261004T101330Z\wsl-boundary.json`.
- Final OCI package report:
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\reports\rust-docker-package\20261004T101610Z\report.json`.
- Windows NAT-disabled smoke:
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\reports\rust-windows-direct-smoke\20261004T101626Z\report.json`.
- Windows UPnP smoke (MiniUPnPc, two mappings, High ID):
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\reports\rust-windows-direct-smoke\20261004T101729Z\report.json`.
- Windows exact 2,785 MB completion and delivered-file SHA-256 proof:
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\reports\rust-windows-direct-smoke\20261004T080433Z\report.json`.
- WSL/OpenVPN network and NAT-PMP proof:
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\reports\rust-vpn-live\20261004T094800Z-openvpn-network.json`.
- Docker/Gluetun network and NAT-PMP proof:
  `EMULEBB_WORKSPACE_OUTPUT_ROOT\reports\rust-vpn-live\20261004T095200Z-gluetun-network.json`.
- The VPN provider returned UPnP IGD error 501 in both VPN lanes; the existing
  helper's `upnpc` control failed against the same endpoint while its NAT-PMP
  mappings remained healthy. This is retained as an external capability result,
  not reported as a successful VPN UPnP proof.

## Notes

This is an integrity and lifecycle gap, not a request to replace the existing
per-part verification. Packed-frame caps, compressed-part bounds, short hashset
rejection, and the current AICH trust logic remain strong and are non-goals here.
