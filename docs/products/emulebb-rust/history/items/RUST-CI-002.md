---
id: RUST-CI-002
workflow: local
title: Rationalize and close the core stock-eMule parity evidence gate
status: DONE
priority: Major
category: ci
labels: [parity, tests, evidence, release]
milestone: phase-0
created: 2026-06-19
source: core parity closure review (2026-06-19)
---

# RUST-CI-002 - Rationalize and close the core stock-eMule parity evidence gate

## Summary

Close the emulebb-rust **core client parity** lane against stock eMule wire and
core behavior with one authoritative, reproducible evidence gate. emulebb-mfc
can remain a frozen comparison witness, but it is no longer the product parity
target. The close target is core eD2K/Kad client behavior, deterministic local
cross-client interoperation, and a manual public-network smoke witness. It is
not the full Phase 0 product gate: REST API evolution, indexer, Arr/Torznab,
Docker, and SSE remain separately tracked. The automated tunnel-down leak test
is a separate release-safety gate and is complete under `RUST-FEAT-005`.

This item exists to prevent the parity closure decision from being spread across
ad hoc reports. It owns the close checklist, evidence freshness rule, and test
rationalization.

## Current State

**Closed 2026-09-27.** The authoritative `emulebb-rust-overnight` campaign
passed all seven commands and all eight required blocking evidence rows. The
retained result binds Rust `3a162136`, build-tests `9865967`, build `7eccd29`,
tooling `fc9fb53`, MFC `9466ece`, and goed2k-server `ea5d4b2`. The only Rust
status line was the operator-owned, deliberately untracked `TOMORRAWZ.MD`; the
tracked Rust tree was clean. The archive-only documentation commit follows the
captured tooling head and does not change the tested implementation or harness.

The separate targeted Rust/eMuleBB UDP-reask proof also passed: both configured
MFC slots were occupied, a third Rust peer was observed waiting, its queued TCP
session detached, and its UDP reask received an acknowledgement. This closes
`RUST-FEAT-001` without weakening MFC production anti-abuse behavior or Rust's
stock production reask cadence.

`RUST-BUG-001` remains distinct Phase 0 CI-isolation debt. Forward work in
`RUST-FEAT-002`, `RUST-FEAT-004`, `RUST-FEAT-006`, and `RUST-FEAT-007` is not a
core stock-eMule parity blocker. The regular/manual campaign remains
informational; the overnight campaign is the sole authoritative automated
close gate. Public-network smoke remains optional and nonblocking, and aMule
remains a retired offline reference unless the operator explicitly reopens it.

## Intended Shape

Use `emulebb-rust-overnight` as the authoritative core parity close campaign.
The regular/manual campaign can stay informational unless its manual evidence
rows are converted to JSON-backed evidence and evaluated consistently.

The close gate is:

1. `python -m emule_workspace workspace-status`
2. `python -m emule_workspace validate`
3. `python tools\check_rust_client_policy.py` from `repos\emulebb-rust`
4. Build the MFC release and tracing-harness executables through
   `repos\emulebb-build` orchestration.
5. `python -m emule_workspace test release-campaign --campaign emulebb-rust-overnight --execute --continue-on-failure`
6. Targeted UDP reask proof:
   `python scripts\emulebb-rust-reask-cross-client.py --lan-bind-addr %X_LOCAL_IP%`
7. Optional long-form byte-level confirmation with
   `emulebb-rust-reask-capture-emulebb.py`.
8. Optional public hide.me live-wire smoke using operator-local inputs. Accept it
   only when both obfuscation modes pass with VPN-bound P2P, eD2K/Kad
   connectivity, packet diagnostics, source-exchange evidence, and a completed
   download.

## Scope Constraints

- Core parity closure does not claim full Phase 0 completion.
- Public live-wire remains manual and nonblocking. The completed
  `RUST-FEAT-005` tunnel-down gate is deterministic local safety proof and does
  not turn public-network smoke into a core-parity blocker.
- The July 2026 CI-047 retirement removed aMule launch/control adapters and
  campaign entry points. Current workspace policy treats aMule as an offline
  source/fixture reference, not a release gate; reopening it requires a separate
  operator decision.
- emulebb-mfc source-seam, community/reference parity, VM proof, and
  public-network live proof stay out of the forward suite gate unless explicitly
  requested.
- All public-network proof must follow the workspace live-test network policy
  and must not commit operator-owned live search terms, media names, private
  addresses, or machine paths.

## Acceptance Criteria

- [x] Overnight campaign evidence is regenerated after the current Rust HEAD and
      current MFC/tracing-harness build inputs.
- [x] The retained campaign result records the Rust overnight local client
      pytest proof, source-anchored stock oracle with executable Rust proof
      packages, local ED2K protocol-combination matrix, private parity modules,
      Rust/eMuleBB bidirectional transfer, Rust/Rust bidirectional transfer,
      total parity audit, and REST contract conformance as passed.
- [x] The close decision explicitly states that `RUST-FEAT-002`,
      `RUST-FEAT-004`, `RUST-FEAT-006`, and `RUST-FEAT-007` are forward Phase 0
      or later work, not core stock-eMule parity blockers.
- [x] `RUST-FEAT-005` is closed with a blocking dynamic tunnel-down leak-test;
      that release-safety gate remains distinct from core parity closure.
- [x] The regular release campaign is either documented as informational or its
      manual rows are converted to JSON evidence so it cannot contradict the
      authoritative overnight gate.

## Validation

Required for closing this item:

- `python -m emule_workspace workspace-status`
- `python -m emule_workspace validate`
- `python tools\check_rust_client_policy.py`
- `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`
- `python -m emule_workspace build app --variant tracing-harness --config Release --platform x64 --build-output-mode ErrorsOnly`
- `python -m emule_workspace test release-campaign --campaign emulebb-rust-overnight --execute --continue-on-failure`

Closure results:

- `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\release-campaign-runs\20260927T171451Z-emulebb-rust-overnight\release-campaign-run-result.json`
  passed seven of seven commands and eight of eight required blocking evidence
  rows.
- `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\artifacts\emulebb-rust-reask-cross-client\20260927T164726Z-x64-release-9936\emulebb-rust-reask-cross-client-result.json`
  passed the targeted UDP-reask witness.
- The final regular Rust release build completed without warnings at
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\logs\builds\20260927T165347Z-build-clients\build-result.json`.
- `workspace-status` completed successfully. `workspace validate` passed the
  active policy, branch, dependency-pin, documentation-path, editorconfig,
  environment, localization, output-redirection, PowerShell-boundary, entrypoint,
  and warning-policy audits, then reported the existing workspace artifact-audit
  debt: ignored local virtual environments plus `emulebb-rust/webui/node_modules`.
  Those operator caches are outside this parity closure and were not deleted.

Optional smoke:

- `python scripts\rust-live-wire-hideme.py --inputs live-wire-inputs.local.json`

## Notes

- This item is local because it records the evidence gate and close decision
  rather than a product feature. If the gate needs public workflow visibility,
  promote it to a GitHub-tracked CI item before closure.
- Related owners: completed `RUST-FEAT-001` for UDP reask live validation,
  completed `RUST-FEAT-003` for VPN egress pinning, completed `RUST-FEAT-005`
  for dynamic no-leak automation, and `RUST-BUG-001` for isolated Kad swarm CI
  debt.
