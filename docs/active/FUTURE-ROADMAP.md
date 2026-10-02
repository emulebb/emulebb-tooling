# eMuleBB MFC Maintenance Roadmap

Status: long-term maintenance. Updated 2026-10-02.

eMuleBB MFC remains published as the stable Windows client on the `0.7.x`
line. It is an interesting and useful completed experiment, not an active broad
development program. Stable `0.7.3` is the current public release.

## Accepted maintenance

The lane may accept:

- bug, crash, security, and data-loss fixes;
- bounded compatibility and build fixes;
- low-risk UX or performance improvements that preserve the existing product;
- packaging, diagnostics, documentation, and release-proof improvements;
- dependency work required to keep the supported line buildable and safe.

Every change should be small enough to review and validate as maintenance. The
burden of proof rises when a change touches wire compatibility, persistence,
the REST contract, or long-running session behavior.

## Outside the lane

The maintenance roadmap does not include:

- broad feature expansion or a new MFC architecture;
- an active `0.8.x` modernization program;
- a new cross-client “eMuleBB Suite” roadmap;
- TrackMuleBB, qBittorrentBB, or controller-platform development;
- native Windows VPN integration as a forward product priority.

New product development belongs to `emulebb-rust`, which is the active
experimental beta lane.

## Parked proposals

The former `0.8.0` engineering plans remain useful design records, but they are
parked ideas rather than scheduled work:

- [Performance and async plan](../ideas/IDEA-MFC-0.8.0-PERF-ASYNC-PLAN.md)
- [Startup time-to-interactive](../ideas/IDEA-MFC-0.8.0-STARTUP-TIME-TO-INTERACTIVE.md)
- [Network core thread](../ideas/IDEA-MFC-0.8.0-NETWORK-CORE-THREAD.md)
- [Process-loop migration](../ideas/IDEA-MFC-0.8.0-PROCESS-LOOP-MIGRATION.md)
- [Lean removal plan](../ideas/IDEA-MFC-0.8.0-LEAN-REMOVAL-PLAN.md)

Their associated `FEAT-*` and `REF-*` specifications are `DEFERRED`, not
closed. IDs and details remain available as provenance, but deferred work is
not presented as the active roadmap.

## Release Line Model

- Stable patches continue on `0.7.x` when warranted.
- The shipped `0.7.3` suite installer and aMuTorrent package remain available
  as [historical release context](../history/HIST-SUITE-INSTALLER.md).
- The archived MFC Project #2 preserves the earlier program history.
- Current cross-repository work is summarized on the
  [eMuleBB Roadmap](https://github.com/orgs/emulebb/projects/3).

For the organization-wide view, see the
[Product Portfolio](PRODUCT-PORTFOLIO.md) and
[Roadmap Summary](../reference/ROADMAP-SUMMARY.md).
