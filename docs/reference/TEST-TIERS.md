# Test Tiers — What To Run When

This page is the single answer to "which test command do I run?" The workspace
exposes three named certification tiers through `emulebb-build` orchestration.
Each tier is a strict superset of the one above it, so you pick the smallest
tier that fits the situation instead of assembling individual `test`
subcommands by hand.

All commands run from the workspace root through
`python -m emule_workspace` and honor the canonical `EMULEBB_*` environment.

## The three tiers

| Tier | Command | When |
| --- | --- | --- |
| **Quick** | `python -m emule_workspace test certification --profile quick` | Every change / inner loop |
| **Fast** | `python -m emule_workspace test certification --profile fast` | Pre-commit, and the RC release gate |
| **Overnight** | `python -m emule_workspace test certification --profile overnight` | Release sign-off / full proof |

### Quick — inner loop

Lean by design; this is the command to run after most edits.

- `validate` (static audits)
- `build-app-debug-x64`, `build-tests-debug-x64`
- `python-harness` (full pytest)
- `test-all-debug-x64` — native `parity` / `protocol-parity` / `web_api`,
  **without** the coverage re-run
- `live-fast-ui-rest` — the fast UI/REST live suites

Quick deliberately omits, relative to Fast: the Release-config native pass, the
ARM64 app build, and the native-coverage re-run (which re-executes the native
suites under instrumentation and roughly doubles native runtime). Those belong
to the gate, not the inner loop.

### Fast — the release gate

Quick plus the full release-config and ARM64 build matrix, the second
(Release) native pass, and the native-coverage report. This is the
release-blocking RC certification; its contents are intentionally unchanged so
"certified" keeps its meaning.

### Overnight — full proof

Fast plus the expanded live, UI resource-depth, stabilization-stress, and
aMuTorrent live suites.

Stock/community parity comparisons (`test protocol-parity`,
`test community-core-coverage`) are **on-demand only** and not part of any tier.
eMuleBB is protocol-stable and stock-compatible, so these baseline-build
comparisons are run deliberately when protocol-adjacent code changes, not on
every overnight.

## Tiers vs the release campaign

The `emulebb-0.7.3` release campaign is the comprehensive **evidence map** for a
release, not the everyday command. It runs the Fast certification as one
blocking step, so the campaign no longer re-issues standalone `validate`,
`python-harness`, or `test all` runs — those scenarios remain as evidence rows
(non-blocking) and resolve from the Fast certification output instead of
re-executing. Run the campaign at RC checkpoints; run a tier during routine
work.

## Picking a tier

- Touched code and want a quick confidence check → **Quick**.
- About to commit to `main`, or producing an RC gate result → **Fast**.
- Signing off a release, or chasing a flaky/stress/protocol issue → **Overnight**.
