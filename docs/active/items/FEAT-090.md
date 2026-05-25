---
id: FEAT-090
title: Tune broadband limits by drive topology and total budget
status: OPEN
priority: Minor
category: feature
labels: [preferences, defaults, performance, storage, hdd, ssd, broadband, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-25
source: operator request to tune eMuleBB broadband limits per drive topology, HDD versus SSD, and total maximum budget
---

# FEAT-090 - Tune Broadband Limits By Drive Topology And Total Budget

## Summary

`FEAT-016` modernized several stale fixed limits for broadband-era hardware.
This follow-up should make the disk-sensitive limits smarter by considering the
actual storage topology behind temp, incoming, config, and shared paths.

The goal is to avoid one set of limits being either too aggressive for a single
rotational HDD or too conservative for SSD/NVMe and multi-drive systems. eMuleBB
should classify storage best-effort, choose conservative defaults when unsure,
and cap the aggregate work so parallelism across drives does not turn into
unbounded disk pressure.

## Intended Shape

- Classify relevant paths by volume, physical device, and storage type where
  Windows can report it reliably.
- Distinguish at least `rotational`, `ssd`, `network/removable`, and `unknown`.
- Apply per-drive budgets for disk-sensitive broadband behavior, such as file
  buffering, flush cadence, hashing concurrency hooks, part-file write pressure,
  and concurrent move/complete work.
- Add a total maximum budget so multiple SSDs do not multiply limits without
  bound.
- Keep operator overrides authoritative through preferences or advanced tuning.
- Record diagnostics that explain the detected topology and selected limits.

## Candidate Policy

Start with conservative buckets rather than a fully dynamic controller:

| Storage class | Default posture |
|---------------|-----------------|
| Rotational HDD | Low parallelism, smaller per-drive write pressure, longer batching only when safe |
| SSD/NVMe | Higher bounded parallelism and larger buffers where memory budget allows |
| Network/removable | Conservative and fail-safe; avoid assuming low latency or reliable media |
| Unknown | Treat like HDD until the operator overrides it |

The total budget should be explicit, for example:

- per-drive worker or queue budget
- global worker or queue budget
- per-drive buffer budget
- global memory budget for file buffers

Exact defaults should come from profiling, not guesswork.

## Scope Constraints

- Do not change eD2K/Kad protocol behavior or advertise non-stock capability.
- Do not make storage-type detection a startup hard dependency.
- Do not force-migrate existing user preference values.
- Do not combine this with `FEAT-076` implementation unless the shared storage
  classifier is already stable; hashing can consume the policy later.
- Do not treat SSD detection as permission for unbounded writes, hashing,
  completion moves, or UI-blocking refreshes.
- Do not let network or removable drive probes block startup or queue
  processing.

## Candidate Implementation Notes

Reuse or share code with storage-related backlog items where practical:

- `FEAT-076` can consume the same volume/device classifier for hash scheduling.
- `FEAT-080` can consume the same protected-volume snapshots and stale-data
  policy.

Windows APIs to evaluate include volume path resolution, drive type detection,
and storage property queries for seek penalty or trim support. Detection must
remain best-effort because USB bridges, virtual disks, and network mounts can
lie or omit media details.

## Acceptance Criteria

- [ ] eMuleBB can classify temp, incoming, config, and shared paths into
      per-volume storage classes without blocking startup on slow paths.
- [ ] Disk-sensitive broadband defaults can differ for HDD, SSD/NVMe,
      network/removable, and unknown storage.
- [ ] A global maximum budget bounds aggregate disk work across all drives.
- [ ] Existing explicit preference values continue to override automatic
      defaults.
- [ ] Diagnostics expose the detected topology, selected storage class, and
      effective limits used by the runtime.
- [ ] Unknown or ambiguous storage falls back to conservative behavior.
- [ ] Focused tests cover classification fallback, per-drive budget selection,
      total-budget clamping, and preference override precedence.

## Validation

- `python -m emule_workspace validate`
- focused native tests for storage classification and limit selection
- synthetic profiles covering single HDD, single SSD, multi-drive, removable,
  network, and unknown storage cases
- profiling evidence before changing defaults beyond the first conservative
  policy table
- x64 Debug and Release app builds before commit
