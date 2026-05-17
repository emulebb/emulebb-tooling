# eMule BB Development Guide

This guide is the durable entry point for development, validation, release
proof, and recurring product-documentation refresh work. It complements
[Workspace Policy](../WORKSPACE_POLICY.md), which remains the source of truth
for branch, worktree, build, test, and release rules.

## Development Model

Routine work happens on `main` in the relevant repo. App source edits belong in
`EMULE_WORKSPACE_ROOT\workspaces\workspace\app\eMule-main`; the canonical
`EMULE_WORKSPACE_ROOT\repos\eMule` checkout is the branch-store anchor, not the
normal edit location.

Use `EMULE_WORKSPACE_ROOT` style paths in active documentation and scripts.
Avoid machine-specific absolute paths in maintained docs.

The product line is eMule broadband edition, compactly eMule BB. The first
public beta release line is `0.7.3`; release tags use
`emule-bb-vMAJOR.MINOR.PATCH`, and package assets use
`eMule-broadband-MAJOR.MINOR.PATCH-ARCH.zip`.

## Supported Entry Points

Workspace build, validation, test, live-test, and packaging work must go
through `repos\eMule-build` orchestration:

```powershell
cd $env:EMULE_WORKSPACE_ROOT\repos\eMule-build
python -m emule_workspace validate
```

Do not run ad hoc direct `MSBuild` from the app worktree, `srchybrid`, or
`repos\eMule-build-tests`.

Every app code change must rebuild both active x64 app configurations before
commit:

```powershell
python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly
python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly
```

Docs-only and policy-only changes may use a lighter validation path when they
do not alter the build contract.

## Test Strategy

The test model is layered so fast checks do not pretend to replace release
proof:

| Layer | Purpose |
|---|---|
| Hosted baseline CI | Basic hygiene, privacy, and shared policy checks through the reusable tooling workflow |
| Workspace validation | Topology, branch, build policy, documentation path, PowerShell boundary, entrypoint, warning, localization, and normalization audits |
| Native and Python harnesses | Deterministic coverage for app-facing behavior, preference schema, REST, adapters, and helper code |
| UI and resource proof | Desktop workflow coverage, resource smoke, and full stock-language release checks |
| Protocol parity and live proof | eD2K/Kad compatibility, community comparison, live-diff, and live-wire scenarios |
| Packaging proof | x64/ARM64 packages, manifests, provenance, hashes, and release operator gates |

Use [Release Test Strategy](../active/RELEASE-TEST-STRATEGY.md) for the current
release testing model, [Release Test Campaigns](../active/RELEASE-TEST-CAMPAIGNS.md)
for campaign evidence, and [CI Baseline](CI-BASELINE.md) for the reusable
GitHub Actions baseline.

## CI And GitHub Checks

Shared baseline CI is owned by `eMule-tooling`:

- reusable workflow: `.github/workflows/reusable-baseline.yml`
- stable ref: `ci/v8`
- required check names:
  - `baseline / baseline (windows-2022)`
  - `baseline / baseline (windows-2025-vs2026)`

Long-lived consumer branches should use the stable CI ref, not `@main`, and
must pass the same immutable `tooling_ref` into the reusable workflow.

## Live Network Policy

Live tests that launch an eMule profile must enable the main P2P UPnP
preference and bind the P2P stack through the `hide.me` interface by writing
`BindInterface=hide.me`. Live harnesses must not write `hide.me` into
`BindAddr`; `BindAddr` is an address override, while `BindInterface` is the
interface target.

Product documentation should stay provider-neutral. It can describe VPN-aware
interface binding and external VPN kill-switch discipline, but must not claim
that eMule BB ships kill-switch behavior.

## Release Campaign And Evidence

Release readiness is controlled by active release docs, not by source comments
or historical notes:

- [Beta 0.7.3 dashboard](../active/RELEASE-0.7.3.md)
- [Beta 0.7.3 checklist](../active/RELEASE-0.7.3-CHECKLIST.md)
- [Beta 0.7.3 runbook](../active/RELEASE-0.7.3-RUNBOOK.md)
- [Beta 0.7.3 execution plan](../active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md)

No new feature should be described as shipped until the active item state,
source behavior, and relevant validation evidence agree.

## Packaging And Provenance

Packaging is owned by `repos\eMule-build`. Product docs should describe release
package behavior only after the packaging manifest, release runbook, and
verification evidence have been updated together.

Release-package claims should cover:

- target architecture
- package name
- selected `main` commit
- package manifest
- SHA-256 hash
- provenance of bundled assets
- release-gate status

## Command-Line Surface

The app command line is part of the product contract and should stay documented
when parser behavior changes:

```text
emule.exe [options] [ed2k-link|magnet-link|collection-file|command]
```

Supported options:

| Option | Behavior |
|---|---|
| `--help`, `-h`, `/?` | Print command-line usage and exit |
| `-c <base-dir>` | Use an isolated eMule base directory; the path must be an absolute canonical Windows path |
| `-ignoreinstances` | Start without the running-instance guard unless the positional argument must be forwarded to an existing instance |
| `-AutoStart` | Mark the session as automatic startup |
| `-assertfile` | In Debug builds, write CRT assertion output to a file |
| `--generate-webserver-cert` | Generate a WebServer TLS certificate and exit |
| `--cert <path>` | Certificate output path for `--generate-webserver-cert` |
| `--key <path>` | Private-key output path for `--generate-webserver-cert` |
| `--host <dns-or-ip>` | Subject alternative name for generated certificate; repeatable |

Only one positional argument is supported. It may be an `ed2k` link, magnet
link, collection file, or command such as `exit`.

## Product Guide Refresh Workflow

Run this workflow whenever feature status, release proof, command-line behavior,
REST/controller behavior, network policy, packaging, or product messaging
changes.

1. Start from policy and status.
   - Read `docs\WORKSPACE_POLICY.md`.
   - Check `git status --short --branch` in every repo that will be read or
     edited.
   - Confirm whether the change is docs-only, app code, build orchestration,
     test harness, website, or org-profile work.
2. Re-scan source truth.
   - Active release truth: `docs\active\RELEASE-0.7.3*.md`,
     `docs\active\INDEX.md`, and `docs\active\items\`.
   - Landed feature history: `docs\history\items\FEAT-*.md`,
     `BUG-*.md`, `CI-*.md`, and `REF-*.md` as needed.
   - Command line: app parser seams and `Emule.cpp`.
   - Preferences: [Preferences Guide](GUIDE-PREFERENCES.md) and the preference
     schema manifest.
   - REST: [REST API contract](../rest/REST-API-CONTRACT.md), OpenAPI, and
     adapter docs.
   - Packaging: `repos\eMule-build` release orchestration and active release
     runbook.
   - Website and org copy: public pages must follow tooling docs, not invent
     status.
3. Update the product docs in owner order.
   - [Product Guide](GUIDE-EMULEBB.md): product summary, landed feature matrix,
     quality evidence, performance summary, compatibility, and release status.
   - Focused guides: setup, network, downloads/search, sharing, controllers,
     preferences, IP filters, long paths, shortcuts, and troubleshooting.
   - This guide: development, validation, CI, command-line, packaging, and
     refresh workflow changes.
4. Update navigation and public touchpoints.
   - `docs\INDEX.md`
   - `docs\HELP.md`
   - `README.md`
   - `repos\eMulebb-pages\docs\SITE-HANDBOOK.md`
   - `repos\eMulebb-org-profile\profile\README.md`
5. Keep claims bounded.
   - Do not describe open, deferred, exploratory, or future backlog work as
     shipped.
   - Do not use retired release labels as current public release names.
   - Do not describe an external VPN kill-switch design as built-in product
     behavior.
   - Do not publish release-package claims before package evidence exists.
6. Validate the docs-only slice.
   - Run `git diff --check` in each edited repo.
   - Run `python scripts\docs-item-taxonomy-check.py` from `repos\eMule-tooling`
     after item, active-index, or taxonomy changes.
   - Search for stale paths, retired release labels, missing new-guide links,
     and accidental overclaims before committing.
7. Commit and push coherent slices.
   - Keep tooling-doc changes together.
   - Commit website handbook changes separately if only the pages repo changed.
   - Commit org-profile copy separately if only the org profile changed.

## Regular Refresh Checklist

For a scheduled product/development guide refresh, record the outcome in the
commit message or review notes:

- Product guide feature matrix still matches closed feature records.
- Focused guides document every landed user-visible feature.
- Development guide still matches workspace policy, CI, build, and release
  entrypoints.
- Command-line options match current parser behavior.
- VPN/interface binding language is provider-neutral outside live-test policy.
- REST/controller docs match OpenAPI and adapter docs.
- Release status links point to active `0.7.3` docs.
- Public website and org profile link to the updated guide set.
- Docs-only validation was run, or any skipped check is explained.
