# eMuleBB Development Guide

This guide is the practical entry point for internal contributors and operators
who make routine documentation updates and light code changes in the canonical
workspace. [Workspace Policy](../WORKSPACE-POLICY.md) remains the authority for
branch, worktree, build, test, release, and documentation rules.
AI contributors should start with the [Agent Checklist](AGENT-CHECKLIST.md)
for the repeatable end-to-end operating path.

## Contributor Model

Routine work happens on `main` in the relevant repo. App source edits belong in
`EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main`; the canonical
`EMULEBB_WORKSPACE_ROOT\repos\emulebb` checkout is the branch-store anchor, not the
normal edit location.

Use `EMULEBB_WORKSPACE_ROOT` style paths in maintained documentation and scripts.
Avoid machine-specific absolute paths in active docs.

The product line is eMule broadband edition, compactly eMuleBB. The first
public release candidate is `0.7.3-rc.1`; release tags use
`emulebb-vMAJOR.MINOR.PATCH[-rc.N]`, and package assets use
`emulebb-MAJOR.MINOR.PATCH[-rc.N]-ARCH.zip`.

## Start Every Change

Before editing:

- Read [Workspace Policy](../WORKSPACE-POLICY.md).
- Check `git status --short --branch` in every repo that will be read for
  current-state decisions or edited.
- Confirm whether the change is docs-only, backlog/docs metadata, light code,
  build orchestration, test harness, website, or org-profile work.
- Keep one coherent outcome per commit.
- Use current docs and source as truth, not historical handoff notes.

## Where To Edit

| Change type | Primary location | Notes |
|---|---|---|
| Workspace policy | `docs\WORKSPACE-POLICY.md` | Mandatory rules only; avoid workflow prose here. |
| Agent repeatability | `docs\reference\AGENT-CHECKLIST.md` | End-to-end checklist for AI contributors. |
| Documentation taxonomy | `docs\DOCS-POLICY.md` | Naming, nav, table, and docs-structure rules. |
| Contributor workflow | `docs\reference\DEVELOPMENT-GUIDE.md` | Practical checklists for routine work. |
| Backlog process | `docs\reference\BACKLOG-PROCESS.md` | Repeatable backlog mechanics and item lifecycle. |
| Active release/status docs | `docs\active\...` | Current release, roadmap, and item state. |
| Product/user guides | `docs\reference\GUIDE-*.md` | User-facing behavior after source and evidence agree. |
| REST docs | `docs\rest\...` | Contract, adapter, and parity documentation. |
| App code | `workspaces\workspace\app\emulebb-main` | Do not edit `repos\emulebb` for routine app work. |
| Build orchestration | `repos\emulebb-build` | Use supported orchestration entry points. |

## Supported Commands

Run workspace build, validation, test, live-test, and packaging work through
`repos\emulebb-build` orchestration:

```powershell
cd $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build
python -m emule_workspace validate
```

Do not run ad hoc direct `MSBuild` from the app worktree, `srchybrid`, or
`repos\emulebb-build-tests`.

Every app code change must rebuild both active x64 app configurations and the
diagnostics Release executable before commit. Those exact build commands are
defined once in
[Workspace Policy](../WORKSPACE-POLICY.md#build-validation-and-test-policy); run
them from `repos\emulebb-build`. Documentation-only changes do not require an app
build when they do not alter the build contract.

## Markdown To HTML Publishing

Markdown in `repos\emulebb-tooling\docs` is the maintained source for the public
documentation site. MkDocs Material renders that Markdown to HTML at
`https://emulebb.github.io/emulebb-tooling/`.

Use this repeatable path when product, reference, release, REST, or policy docs
need to be published as formatted HTML:

1. Edit the owning Markdown source under `docs\`.
2. Keep links and navigation current in `docs\INDEX.md` and `mkdocs.yml` when
   adding or moving discoverable pages.
3. Run the local publish gate:

   ```powershell
   cd $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling
   python scripts\docs-publish-check.py
   ```

4. Commit and push the Markdown source. The `Documentation Site` GitHub Actions
   workflow builds the same MkDocs site from `main` and deploys the HTML to
   GitHub Pages.

Generated MkDocs output belongs under `.local\mkdocs-site` and must not be
committed. The static product homepage in `repos\emulebb-pages` is separate:
update it only after the source Markdown is current, then regenerate its
committed HTML through that repo's Jinja renderer.

## Docs-Only Checklist

Use this for Markdown-only changes that do not alter build, source, release
packaging, or API behavior.

- Read the policy and check repo status.
- Update the owning document, not a parallel note.
- Keep workspace-wide rules in policy and workflow instructions in guides.
- Use uppercase hyphen naming for non-item Markdown files.
- Keep broad tables readable in the browser; prefer short tables or existing
  MkDocs CSS behavior for unavoidable wide tables.
- Update `docs\INDEX.md`, `mkdocs.yml`, or README links when discoverability
  changes.
- Run:

```powershell
cd $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling
git diff --check
python scripts\docs-publish-check.py
```

Run `python scripts\docs-item-taxonomy-check.py` when active items, backlog
metadata, active indexes, or taxonomy status counts change.

## Backlog And Roadmap Checklist

Use this when adding, moving, closing, or reclassifying backlog work.

- Start from [Backlog Process](BACKLOG-PROCESS.md).
- Revalidate the item against current `main`, dependency pins, and workspace
  policy before implementation.
- For GitHub-migrated future-roadmap work, treat the linked issue and public
  `eMuleBB Roadmap` project as workflow authority.
- Keep local item docs as engineering specs and evidence, not workflow status
  authority, when `workflow: github` is present.
- Update active indexes and counts together with item metadata.
- Run the item taxonomy check before commit.

## Light Code Checklist

Use this for small source, helper, or test-harness changes.

- Read the policy and check repo status in each touched repo.
- Make the smallest compatibility-preserving change that solves the issue.
- Prefer existing project helpers, platform APIs, or pinned dependencies over
  new custom parsing, encoding, path, crypto, protocol, date/time,
  compression, or structured-data logic.
- Keep app source edits in `workspaces\workspace\app\emulebb-main`.
- Update docs only when behavior, workflow, command-line surface, REST surface,
  or validation expectations change.
- Run `python -m emule_workspace validate`.
- For app code, run both required x64 app builds.
- Add targeted tests or evidence for the changed surface.

## Evidence By Changed Surface

| Changed surface | Minimum evidence expectation |
|---|---|
| Docs-only or policy-only | `git diff --check`, docs structure check, MkDocs strict build |
| Active item metadata | Docs-only checks plus item taxonomy check |
| App code | Workspace validation plus both x64 app builds required by policy |
| Command-line parser | Parser seam/native coverage and guide updates |
| VPN or bind policy | Bind-resolution coverage, diagnostics review, and network-guide updates |
| UPnP or NAT mapping | Backend-selection coverage, failure-path diagnostics, and network/preference docs |
| REST/controller behavior | REST/OpenAPI drift checks, malformed/concurrent request coverage, and controller guide updates |
| Build or dependency policy | Full relevant build/validation matrix |

Do not cite hosted CI as a replacement for local release proof. Hosted CI is a
fast baseline signal; live network, UI/resource, protocol parity, and package
proof remain explicit release-campaign evidence.

## CI And GitHub Checks

Shared baseline CI is owned by `emulebb-tooling`:

- reusable workflow: `.github/workflows/reusable-baseline.yml`
- stable ref: `ci/v8`
- required check names:
  - `baseline / baseline (windows-2022)`
  - `baseline / baseline (windows-2025-vs2026)`

Long-lived consumer branches should use the stable CI ref, not `@main`, and
must pass the same immutable `tooling_ref` into the reusable workflow.

## Command-Line Surface

The app command line is part of the product contract and should stay documented
when parser behavior changes:

```text
emulebb.exe [options] [ed2k-link|magnet-link|collection-file|command]
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
| `--diagnose-media-metadata` | Probe maintained media metadata extractors and exit |
| `--input <path>` | Media file path for `--diagnose-media-metadata` |
| `--output <path>` | Optional JSON output path for `--diagnose-media-metadata` |

Only one positional argument is supported. It may be an `ed2k` link, magnet
link, collection file, or command such as `exit`.

Parser contract:

- singleton options must not be repeated
- `-c` requires an absolute canonical Windows path
- `--generate-webserver-cert` requires `--cert` and `--key`
- `--cert`, `--key`, and `--host` are valid only with
  `--generate-webserver-cert`
- `--host` is repeatable for certificate subject alternative names
- certificate generation does not accept a positional argument
- `--diagnose-media-metadata` requires `--input`
- `--input` and `--output` are valid only with
  `--diagnose-media-metadata`
- metadata diagnostics emit `emulebb.mediaMetadataDiagnostic.v1` JSON and do
  not accept a positional argument
- unknown options and invalid option values are command-line errors

## Product Guide Refresh

Run a product-guide refresh when source behavior, command-line behavior,
REST/controller behavior, network policy, packaging status, or product
messaging changes.

- Start from policy and current active docs.
- Re-scan source truth before changing product claims.
- Update the product guide first, then focused guides that own the affected
  workflow.
- Update public touchpoints only when discoverability or external claims change.
- Keep claims bounded to shipped and evidenced behavior.
- Do not describe open, deferred, exploratory, or future backlog work as
  shipped.
- Do not publish release-package claims before package evidence exists.
- Validate as a docs-only slice unless the refresh is coupled to code changes.

For release campaign, package publication, provenance, and tagging operations,
use the active release checklist and runbook instead of this guide.

## Commit And Push

- Keep one coherent outcome per commit.
- Do not bundle unrelated docs, source, dependency, and release changes.
- Commit and push each completed slice before starting the next unrelated
  slice unless the user explicitly asks to hold local commits.
- Include tracked item IDs in feature, bug, refactor, and CI backlog commits.
- Record skipped validation with a concrete reason in the handoff or review
  notes.
