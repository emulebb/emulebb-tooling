---
id: RUST-BUG-114
workflow: local
title: Enforce an explicit maximum upload-slot ceiling and clarify maxUploadSlots semantics
status: OPEN
priority: Minor
category: bug
labels: [rust, ed2k, upload, slots, parity, config]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K upload/ban/slot audit 2026-10-12 vs emulebb-mfc
---

# RUST-BUG-114 - Enforce an explicit maximum upload-slot ceiling and clarify maxUploadSlots semantics

## Summary

The setting named "Maximum upload slots" is consumed as the base slot target,
not as a cap. Under sustained upload underfill, elastic expansion opens
additional slots above that value, so an operator who configures 20 slots can
actually admit up to 36. The upload queue also never enforces the MFC
`MAX_UP_CLIENTS_ALLOWED` (128) ceiling; the effective bound only exists
implicitly because two separate settings happen to multiply to 128.

## Current State

- `crates/emulebb-ed2k/src/ed2k_transfer/upload_queue.rs:49` defines
  `MIN_UP_CLIENTS_ALLOWED = 2` but there is no `MAX_UP_CLIENTS_ALLOWED`.
- `elastic_slot_allowance` (`upload_queue.rs:2693`) computes
  `base * elastic_percent / 100` with `div_ceil`.
- `effective_active_slot_limit` (`upload_queue.rs:2702`) returns
  `base + allowance` while `elastic_underfill_ready`, else `base`; no upper
  clamp is applied.
- `crates/emulebb-settings/src/lib.rs`: the `maxUploadSlots` spec is bounded
  `1..64` (`max: 64`, lines 166-175) and `uploadSlotElasticPercent` is bounded
  `0..100` (`max: 100`, lines 178-185). `64 * 200% = 128` only by coincidence.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `Opcodes.h:107-108`: `MIN_UP_CLIENTS_ALLOWED = 2`,
  `MAX_UP_CLIENTS_ALLOWED = 128`.
- `UploadQueue.cpp:989-991` `GetSoftMaxUploadSlots()` returns
  `max(MIN_UP_CLIENTS_ALLOWED, maxUploadClients)`.
- `UploadQueue.cpp:994-997` `GetElasticMaxUploadSlots()` returns
  `min(MAX_UP_CLIENTS_ALLOWED, max(softMax, elastic))`, so both bounds are
  explicit queue invariants in the master.

## Why This Matters

The label says "Maximum" while the value behaves as a floor. This surprises
operators, makes the true ceiling unreasoned, and leaves the limit split across
two independent settings where either one drifting removes the 128 cap. The
master owns both bounds in the queue, which is the safer long-term shape.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/upload_queue.rs` -
  `effective_active_slot_limit`, `elastic_slot_allowance`,
  `MIN_UP_CLIENTS_ALLOWED`
- `crates/emulebb-settings/src/lib.rs` - `maxUploadSlots`,
  `uploadSlotElasticPercent` number specs
- `workspaces/workspace/app/emulebb-main/srchybrid/Opcodes.h` -
  `MIN_UP_CLIENTS_ALLOWED`, `MAX_UP_CLIENTS_ALLOWED`
- `workspaces/workspace/app/emulebb-main/srchybrid/UploadQueue.cpp` -
  `GetSoftMaxUploadSlots`, `GetElasticMaxUploadSlots`

## Intended Shape

- Add `MAX_UP_CLIENTS_ALLOWED = 128` next to the existing MIN constant and
  clamp `effective_active_slot_limit` to it, exactly like the master.
- Make the setting semantics truthful: either rename `maxUploadSlots` to a
  base-slot-target name, or treat it as a hard cap and derive elasticity below
  it. Pick one and keep the elastic path from ever exceeding the documented
  cap.

## Scope Constraints

- Keep the default behavior unchanged (base 12, elastic 80%).
- Preserve the sustained-underfill elastic-open and slow/idle recycle logic.
- Do not couple this to the connection-rate or queue-size settings.

## Acceptance Criteria

- [ ] The upload queue enforces an explicit maximum total active-slot count.
- [ ] The `maxUploadSlots` setting either becomes a true cap or is renamed to
      reflect base-slot semantics, with docs/OpenAPI/WebUI updated.
- [ ] A unit test proves no configuration can exceed the documented ceiling.

## Validation

- Extend the upload-queue slot-limit tests with base/elastic combinations
  (including the boundary 64 + 100%) and assert the ceiling.
- Settings validation round-trip for the renamed or re-scoped field.

## Notes

Related constant consolidation is tracked by RUST-REF-011. The MIN bound is
already correct and should remain.
