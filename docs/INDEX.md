# eMuleBB Documentation

<section class="docs-hero">
  <div>
    <p class="docs-eyebrow">eMuleBB Rust</p>
    <h2>Active eD2K/Kad beta, led by CI-gated nightlies.</h2>
    <p>
      Choose the newest dated nightly prerelease from GitHub Releases.
      Tested for months on live eD2K/Kad networks. Beta 3 is expected after a
      few more weeks of implementation and stabilization.
    </p>
    <p>
      The maintained Windows 0.7.x client remains available for diagnostics,
      critical fixes, and bounded low-risk maintenance.
    </p>
  </div>
</section>

## The eMuleBB Projects

This guide leads with **eMuleBB Rust**, the active beta and only active product-
development lane. Use **eMuleBB Rust** as the display name and `emulebb-rust`
for repository and technical identifiers. The **eMuleBB Windows client** is the
stable `0.7.3` eD2K/Kad desktop app and remains buildable and shippable for
diagnostics, critical fixes, and bounded low-risk maintenance.
Former BitTorrent and controller forks are retired from the current workspace;
TrackMuleBB is archived.
The upstream-aligned Rust `ed2k-server` fork is the sole local deterministic
server; server changes stay minimal, generic, and upstreamable. See the
[Product Direction](active/PRODUCT-DIRECTION.md).

## Start With eMuleBB Rust

- **Current testing:** [choose the newest dated CI-gated nightly build](https://github.com/emulebb/emulebb-rust/releases).
- **Product scope:** read the [eMuleBB Rust product section](products/emulebb-rust/README.md)
  and [release scope](products/emulebb-rust/RELEASE-SCOPE.md).
- **First launch:** follow the repository
  [README](https://github.com/emulebb/emulebb-rust#first-launch) for package,
  profile, authentication, and browser-console startup.
- **Roadmap:** follow the [active Rust backlog](products/emulebb-rust/active/INDEX.md)
  and [Beta 3 certification item](products/emulebb-rust/active/items/RUST-CI-009.md).

The beta API, configuration, and persistence schemas remain compatibility-
unstable. Breaking changes are allowed when all owned Rust surfaces move
together; this compatibility warning does not change the product's active-beta
status.

## Maintained Windows Client

### Install And Operate

- [Standalone ZIP](reference/GUIDE-SETUP.md#quick-install-zip-extract-run):
  download the current stable `0.7.3` eMuleBB ZIP, extract it into a new app
  folder, and start `emulebb.exe`.
- [Hyper-V isolated package runs](reference/GUIDE-HYPERV-WINDOWS.md):
  prepare clean local Windows guests and run package checks without
  touching the host's daily eMuleBB profile.
- [Running on macOS and Linux](reference/GUIDE-CROSS-PLATFORM.md):
  options for using eMuleBB off Windows through a virtual machine, Wine, a
  Windows-hosted core with a cross-platform controller, or aMule.

Use these guides in order for a first real profile:

1. [Setup Guide](reference/GUIDE-SETUP.md) covers install layout, first launch,
   existing profiles, isolated `-c` profiles, and release-aware testing.
2. [Product Guide](reference/GUIDE-EMULEBB.md) explains what eMuleBB is, what it
   changes, and how to operate it as a power user.
3. [Power User Manual](reference/GUIDE-POWER-USERS.md) teaches eMule from zero
   through full operation: eD2K, Kad, High ID, queues, credits, parts, sharing,
   automation, safety, diagnostics, and tuning.
4. [Network Guide](reference/GUIDE-NETWORK.md) covers eD2K, Kad, ports, bind
   settings, UPnP, firewall behavior, and WebServer listener basics.
5. [Downloads And Search](reference/GUIDE-DOWNLOADS-SEARCH.md) covers search
   quality, categories, transfer actions, disk-space protection, and broadband
   upload policy.
6. [Sharing Guide](reference/GUIDE-SHARING.md) covers shared directories,
   monitored shares, large libraries, and share-ignore rules.
7. [Stack Integration Guide](reference/GUIDE-STACK-INTEGRATIONS.md) covers
   qBittorrent-compatible and Torznab adapter workflows with Prowlarr and Arr.

For Windows maintenance release testing, use the [0.7.3 release notes](active/RELEASE-0.7.3-NOTES.md)
before downloading or reporting package behavior.

## Developer And Release Operator Paths

If you are contributing, validating, or preparing a release, start with the
workspace and release controls instead of the product manual:

| Role | Start Here |
|---|---|
| Contributor or AI agent | [Workspace Policy](WORKSPACE-POLICY.md), then only its task-routed annexes; use the [Agent Checklist](reference/AGENT-CHECKLIST.md) when useful |
| Routine developer | [Development Guide](reference/DEVELOPMENT-GUIDE.md) |
| Backlog owner | [Active Backlog](active/INDEX.md) and [Backlog Process](reference/BACKLOG-PROCESS.md) |
| Release operator | [0.7.3 Release Train Dashboard](active/RELEASE-0.7.3.md) |
| REST/controller reviewer | [REST Contract](rest/REST-API-CONTRACT.md) and [Controller Surface Matrix](active/CONTROLLER-SURFACE-MATRIX.md) |

The routed policy annexes are
[Workspace Operations](reference/WORKSPACE-OPERATIONS-POLICY.md),
[Delivery](reference/DELIVERY-POLICY.md),
[Harness And Live](reference/HARNESS-LIVE-POLICY.md),
[emulebb-rust](products/emulebb-rust/reference/AGENT-POLICY.md), and
[emulebb-mfc](products/emulebb-mfc/reference/AGENT-POLICY.md).

Release operators should also use the
[Execution Plan](active/plans/RELEASE-0.7.3-EXECUTION-PLAN.md) and
[Runbook](active/RELEASE-0.7.3-RUNBOOK.md).

## Power User Paths

<div class="docs-card-grid">
  <article>
    <span>01</span>
    <h3>Bring Your Existing Profile</h3>
    <p>
      Launch with an explicit profile directory, keep temp and incoming paths
      stable, and verify the profile before enabling controllers.
    </p>
    <a href="reference/GUIDE-SETUP.md#existing-profile-recipe">Existing profile recipe</a>
  </article>
  <article>
    <span>02</span>
    <h3>Run Clean Test Builds</h3>
    <p>
      Unpack each package into its own app directory, start with
      <code>-c &lt;profile&gt;</code>, and keep rollback evidence.
    </p>
    <a href="reference/GUIDE-SETUP.md#release-aware-setup">Release-aware setup</a>
  </article>
  <article>
    <span>03</span>
    <h3>Control It Locally</h3>
    <p>
      Use the trusted REST surface for local automation, with explicit bind,
      API key, firewall, and lifecycle rules.
    </p>
    <a href="reference/GUIDE-CONTROLLERS-REST.md">Controllers and REST</a>
  </article>
  <article>
    <span>04</span>
    <h3>Automate Media Workflows</h3>
    <p>
      Present eMuleBB to Prowlarr, Radarr, and Sonarr through Torznab and
      qBittorrent-compatible adapter paths.
    </p>
    <a href="reference/GUIDE-STACK-INTEGRATIONS.md">Stack integration guide</a>
  </article>
</div>

## Automation Fast Path

eMuleBB's main automation story is local and operator-controlled: the native
desktop app owns eD2K/Kad state, while REST, qBittorrent-compatible routes, and
Torznab routes make that state easier to operate.

| Goal | Start Here |
|---|---|
| Make the first authenticated REST call | [REST Quickstart](rest/REST-API-QUICKSTART.md) |
| Understand the exact REST contract | [REST API Contract](rest/REST-API-CONTRACT.md) |
| Wire Prowlarr, Radarr, or Sonarr | [Stack Integration Guide](reference/GUIDE-STACK-INTEGRATIONS.md) |
| Review adapter compatibility | [REST Adapter Notes](rest/REST-API-ADAPTERS.md) |

## First Hour Checklist

For a serious profile, do not start with every feature enabled. Prove the
desktop app first, then layer automation on top.

| Step | What To Prove | Guide |
|---|---|---|
| Install | App directory and profile directory are intentionally separate. | [ZIP install](reference/GUIDE-SETUP.md#quick-install-zip-extract-run) |
| Profile | `preferences.ini`, temp, incoming, categories, and identity files are where expected. | [Persistence Files](reference/GUIDE-PERSISTENCE-FILES.md) |
| Network | TCP, UDP, firewall, UPnP, High ID, and Kad state are understood. | [Network](reference/GUIDE-NETWORK.md) |
| Search | A small search returns believable results before heavy automation starts. | [Downloads And Search](reference/GUIDE-DOWNLOADS-SEARCH.md) |
| Sharing | Shared roots and monitored shares are deliberate, not accidental broad folders. | [Sharing](reference/GUIDE-SHARING.md) |
| Controllers | REST status reads pass before any mutation or Arr workflow is enabled. | [Stack Integration](reference/GUIDE-STACK-INTEGRATIONS.md) |

## Product Guides

| Need | Primary Doc |
|---|---|
| Product overview and operating model | [reference/GUIDE-EMULEBB](reference/GUIDE-EMULEBB.md) |
| Landed behavior matrix and evidence model | [reference/RELEASED-BEHAVIOR-SUMMARY](reference/RELEASED-BEHAVIOR-SUMMARY.md) |
| Public-readable roadmap themes | [reference/ROADMAP-SUMMARY](reference/ROADMAP-SUMMARY.md) |
| Complete eMule manual from zero to power-user operation | [reference/GUIDE-POWER-USERS](reference/GUIDE-POWER-USERS.md) |
| Setup, `-c` profiles, release package testing | [reference/GUIDE-SETUP](reference/GUIDE-SETUP.md) |
| Running on macOS or Linux via VM, Wine, or remote control | [reference/GUIDE-CROSS-PLATFORM](reference/GUIDE-CROSS-PLATFORM.md) |
| Move a Windows P2P workload behind Docker and Gluetun | [reference/GUIDE-DOCKER-GLUETUN-P2P-STACK](reference/GUIDE-DOCKER-GLUETUN-P2P-STACK.md) |
| Search, downloads, categories, limits, upload policy | [reference/GUIDE-DOWNLOADS-SEARCH](reference/GUIDE-DOWNLOADS-SEARCH.md) |
| Shared directories, monitored shares, large libraries | [reference/GUIDE-SHARING](reference/GUIDE-SHARING.md) |
| eD2K, Kad, bind, ports, UPnP, firewall | [reference/GUIDE-NETWORK](reference/GUIDE-NETWORK.md) |
| eMuleBB, Prowlarr, Radarr, and Sonarr setup recipes | [reference/GUIDE-STACK-INTEGRATIONS](reference/GUIDE-STACK-INTEGRATIONS.md) |
| REST semantics, qBit-compatible/Torznab adapter behavior | [reference/GUIDE-CONTROLLERS-REST](reference/GUIDE-CONTROLLERS-REST.md) |
| Preferences and `preferences.ini` reference | [reference/GUIDE-PREFERENCES](reference/GUIDE-PREFERENCES.md) |
| Runtime `.met` and `.dat` file roles | [reference/GUIDE-PERSISTENCE-FILES](reference/GUIDE-PERSISTENCE-FILES.md) |
| IP filter setup and troubleshooting | [reference/GUIDE-IP-FILTERS](reference/GUIDE-IP-FILTERS.md) |
| Long-path behavior on Windows | [reference/GUIDE-LONGPATHS](reference/GUIDE-LONGPATHS.md) |
| Keyboard and menu workflow | [reference/KEYBOARD-SHORTCUTS](reference/KEYBOARD-SHORTCUTS.md) |
| Tools menu operations | [reference/GUIDE-TOOLS-MENU](reference/GUIDE-TOOLS-MENU.md) |
| Diagnostic snapshots, dumps, and metadata diagnostics | [reference/GUIDE-DIAGNOSTICS](reference/GUIDE-DIAGNOSTICS.md) |
| Symptom-led diagnostics and support evidence | [reference/GUIDE-TROUBLESHOOTING](reference/GUIDE-TROUBLESHOOTING.md) |
| Translation policy and glossary | [reference/GUIDE-TRANSLATIONS](reference/GUIDE-TRANSLATIONS.md) |

## API And Automation

REST is the preferred automation surface. The native desktop app remains the
authority for live state.

| Need | Primary Doc |
|---|---|
| First authenticated REST calls | [rest/REST-API-QUICKSTART](rest/REST-API-QUICKSTART.md) |
| Human-readable REST contract | [rest/REST-API-CONTRACT](rest/REST-API-CONTRACT.md) |
| Machine-readable OpenAPI contract | [rest/REST-API-OPENAPI](rest/REST-API-OPENAPI.yaml) |
| qBit, Torznab, and Arr adapter notes | [rest/REST-API-ADAPTERS](rest/REST-API-ADAPTERS.md) |
| REST parity inventory | [rest/REST-API-PARITY-INVENTORY](rest/REST-API-PARITY-INVENTORY.md) |
| Controller surface matrix | [active/CONTROLLER-SURFACE-MATRIX](active/CONTROLLER-SURFACE-MATRIX.md) |

## Translations

The long-form product docs are English-canonical for now. Do not fork large
translated Markdown copies unless there is a review and maintenance owner. Use
[Translations And Localization](reference/GUIDE-TRANSLATIONS.md) for glossary,
terminology, screenshot, command, API field, and localized-quickstart rules.

## Workspace And Release Docs

These docs are for contributors, release operators, and AI agents. They are
kept here because this repository is the canonical documentation home, but they
are not the best first read for users.

| Need | Primary Doc |
|---|---|
| Workspace policy | [WORKSPACE-POLICY](WORKSPACE-POLICY.md) |
| Documentation ownership rules | [DOCS-POLICY](DOCS-POLICY.md) |
| AI contributor checklist | [reference/AGENT-CHECKLIST](reference/AGENT-CHECKLIST.md) |
| Workspace repository map | [reference/WORKSPACE-REPO-MAP](reference/WORKSPACE-REPO-MAP.md) |
| Public website and organization profile contract | [reference/PUBLIC-PRESENCE-CONTRACT](reference/PUBLIC-PRESENCE-CONTRACT.md) |
| Development and validation guide | [reference/DEVELOPMENT-GUIDE](reference/DEVELOPMENT-GUIDE.md) |
| Active backlog and release dashboard | [active/INDEX](active/INDEX.md) |
| Retired cross-product planning | [history/HIST-SUITE-JOINT-ROADMAP](history/HIST-SUITE-JOINT-ROADMAP.md) |
| 0.7.3 release-train control document | [active/RELEASE-0.7.3](active/RELEASE-0.7.3.md) |
| Public 0.7.3 release notes | [active/RELEASE-0.7.3-NOTES](active/RELEASE-0.7.3-NOTES.md) |
| 0.7.3 stable changelog | [active/RELEASE-0.7.3-STABLE-CHANGELOG](active/RELEASE-0.7.3-STABLE-CHANGELOG.md) |
| 0.7.3 release checklist | [active/RELEASE-0.7.3-CHECKLIST](active/RELEASE-0.7.3-CHECKLIST.md) |
| 0.7.3 release runbook | [active/RELEASE-0.7.3-RUNBOOK](active/RELEASE-0.7.3-RUNBOOK.md) |
| Backlog process | [reference/BACKLOG-PROCESS](reference/BACKLOG-PROCESS.md) |
| Backlog item template | [reference/BACKLOG-ITEM-TEMPLATE](reference/BACKLOG-ITEM-TEMPLATE.md) |
| Evidence retention policy | [reference/EVIDENCE-RETENTION](reference/EVIDENCE-RETENTION.md) |
| CI baseline workflow | [reference/CI-BASELINE](reference/CI-BASELINE.md) |
| Test tiers runbook | [reference/TEST-TIERS](reference/TEST-TIERS.md) |
| Test suite inventory | [reference/TEST-INVENTORY](reference/TEST-INVENTORY.md) |
| Test curation decisions | [reference/TEST-CURATION](reference/TEST-CURATION.md) |
| Exploratory Kad publishing and distributed-search design | [ideas/IDEA-KAD-PUBLISHING-AND-DISTRIBUTED-SEARCH](ideas/IDEA-KAD-PUBLISHING-AND-DISTRIBUTED-SEARCH.md) |
| Release branching and packaging | [reference/RELEASE-BRANCHING-AND-PACKAGING](reference/RELEASE-BRANCHING-AND-PACKAGING.md) |
| eD2K ecosystem inventory dashboard and ranked category index | [reference/ED2K-PROJECT-INVENTORY](reference/ED2K-PROJECT-INVENTORY.md) |
| eD2K forums and sites inventory | [reference/ED2K-FORUMS-AND-SITES](reference/ED2K-FORUMS-AND-SITES.md) |
| Dependency status | [dependencies/DEP-STATUS](dependencies/DEP-STATUS.md) |
| Historical-reference rules | [HISTORICAL-REFERENCES](HISTORICAL-REFERENCES.md) |

If a status claim outside `docs/active/` conflicts with `docs/active/`, treat
`docs/active/` as authoritative for current local backlog and release state.
For GitHub-primary current backlog items marked `workflow: github`, the owning
product repo issue and the public `eMuleBB Roadmap` org Project #3 are
authoritative for workflow state. Project #2 is now the MFC archive board:
`eMuleBB Roadmap MFC (archive)`.

## Browser Site

This Markdown tree can be rendered with MkDocs Material:

```powershell
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

Use `python -m mkdocs build --strict` for CI-equivalent local validation. The
Material theme emits a current MkDocs 2.0 compatibility notice as a warning, so
set `$env:NO_MKDOCS_2_WARNING='1'` before strict local builds. The generated
HTML is written to `.local/mkdocs-site` and deployed to GitHub Pages by
`.github/workflows/docs-site.yml` on `main` at
`https://emulebb.github.io/emulebb-tooling/`.

## Notes

- Historical branch names such as `stale-v0.72a-experimental-clean` and old
  branch labels may appear in reference docs as provenance only.
- Preserve commit ids and historical branch names where they add provenance,
  but do not treat them as current-branch guidance unless `docs/active/`
  explicitly says the work is landed on `main`.
