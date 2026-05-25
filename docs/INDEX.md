# eMuleBB User Guide

<section class="docs-hero">
  <div>
    <p class="docs-eyebrow">eMule broadband edition</p>
    <h2>Classic eMule control, modern broadband operation.</h2>
    <p>
      eMuleBB is for power users who want a native Windows eMule client that can
      run for long sessions, keep large libraries predictable, expose a trusted
      local REST surface, and still respect stock eD2K/Kad behavior.
    </p>
    <p>
      Start here if you are setting up a profile, moving an existing eMule
      install, testing a release package, or wiring eMuleBB into aMuTorrent,
      Prowlarr, Radarr, or Sonarr.
    </p>
  </div>
  <img alt="eMuleBB broadband edition logo" src="assets/brand/emulebb-broadband-edition-logo.png" />
</section>

## Start Here

Use these guides in order for a first real profile:

1. [Product Guide](reference/GUIDE-EMULEBB.md) explains what eMuleBB is, what it
   changes, and how to operate it as a power user.
2. [Power User Guide](reference/GUIDE-POWER-USERS.md) teaches eMule concepts
   from zero: eD2K, Kad, High ID, queues, credits, parts, sharing, and tuning.
3. [Setup Guide](reference/GUIDE-SETUP.md) covers install layout, first launch,
   existing profiles, isolated `-c` profiles, and release-aware testing.
4. [Network Guide](reference/GUIDE-NETWORK.md) covers eD2K, Kad, ports, bind
   settings, UPnP, firewall behavior, and WebServer listener basics.
5. [Downloads And Search](reference/GUIDE-DOWNLOADS-SEARCH.md) covers search
   quality, categories, transfer actions, disk-space protection, and broadband
   upload policy.
6. [Sharing Guide](reference/GUIDE-SHARING.md) covers shared directories,
   monitored shares, large libraries, and share-ignore rules.
7. [Stack Integration Guide](reference/GUIDE-STACK-INTEGRATIONS.md) covers the
   eMuleBB plus aMuTorrent plus Arr workflow with field-level setup details.

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

## First Hour Checklist

For a serious profile, do not start with every feature enabled. Prove the
desktop app first, then layer automation on top.

| Step | What To Prove | Guide |
|---|---|---|
| Install | App directory and profile directory are intentionally separate. | [Setup](reference/GUIDE-SETUP.md) |
| Profile | `preferences.ini`, temp, incoming, categories, and identity files are where expected. | [Persistence Files](reference/GUIDE-PERSISTENCE-FILES.md) |
| Network | TCP, UDP, firewall, UPnP, High ID, and Kad state are understood. | [Network](reference/GUIDE-NETWORK.md) |
| Search | A small search returns believable results before heavy automation starts. | [Downloads And Search](reference/GUIDE-DOWNLOADS-SEARCH.md) |
| Sharing | Shared roots and monitored shares are deliberate, not accidental broad folders. | [Sharing](reference/GUIDE-SHARING.md) |
| Controllers | REST status reads pass before any mutation or Arr workflow is enabled. | [Stack Integration](reference/GUIDE-STACK-INTEGRATIONS.md) |

## Product Guides

| Need | Primary Doc |
|---|---|
| Product overview and operating model | [reference/GUIDE-EMULEBB](reference/GUIDE-EMULEBB.md) |
| eMule concepts from zero to power-user operation | [reference/GUIDE-POWER-USERS](reference/GUIDE-POWER-USERS.md) |
| Setup, `-c` profiles, release package testing | [reference/GUIDE-SETUP](reference/GUIDE-SETUP.md) |
| Search, downloads, categories, limits, upload policy | [reference/GUIDE-DOWNLOADS-SEARCH](reference/GUIDE-DOWNLOADS-SEARCH.md) |
| Shared directories, monitored shares, large libraries | [reference/GUIDE-SHARING](reference/GUIDE-SHARING.md) |
| eD2K, Kad, bind, ports, UPnP, firewall | [reference/GUIDE-NETWORK](reference/GUIDE-NETWORK.md) |
| eMuleBB, aMuTorrent, Prowlarr, Radarr, Sonarr | [reference/GUIDE-STACK-INTEGRATIONS](reference/GUIDE-STACK-INTEGRATIONS.md) |
| REST, qBit-compatible, Torznab, adapter behavior | [reference/GUIDE-CONTROLLERS-REST](reference/GUIDE-CONTROLLERS-REST.md) |
| Preferences and `preferences.ini` reference | [reference/GUIDE-PREFERENCES](reference/GUIDE-PREFERENCES.md) |
| Runtime `.met` and `.dat` file roles | [reference/GUIDE-PERSISTENCE-FILES](reference/GUIDE-PERSISTENCE-FILES.md) |
| IP filter setup and troubleshooting | [reference/GUIDE-IP-FILTERS](reference/GUIDE-IP-FILTERS.md) |
| Long-path behavior on Windows | [reference/GUIDE-LONGPATHS](reference/GUIDE-LONGPATHS.md) |
| Keyboard and menu workflow | [reference/KEYBOARD-SHORTCUTS](reference/KEYBOARD-SHORTCUTS.md) |
| Symptom-led diagnostics and support evidence | [reference/GUIDE-TROUBLESHOOTING](reference/GUIDE-TROUBLESHOOTING.md) |
| Translation policy and glossary | [reference/GUIDE-TRANSLATIONS](reference/GUIDE-TRANSLATIONS.md) |

## API And Automation

REST is the preferred automation surface. The native desktop app remains the
authority for live state.

| Need | Primary Doc |
|---|---|
| Human-readable REST contract | [rest/REST-API-CONTRACT](rest/REST-API-CONTRACT.md) |
| Machine-readable OpenAPI contract | [rest/REST-API-OPENAPI](rest/REST-API-OPENAPI.yaml) |
| qBit, Torznab, Arr, and aMuTorrent adapter notes | [rest/REST-API-ADAPTERS](rest/REST-API-ADAPTERS.md) |
| REST parity inventory | [rest/REST-API-PARITY-INVENTORY](rest/REST-API-PARITY-INVENTORY.md) |
| Controller surface matrix | [active/CONTROLLER-SURFACE-MATRIX](active/CONTROLLER-SURFACE-MATRIX.md) |

## Translations

The long-form product docs are English-canonical for now. Do not fork large
translated Markdown copies unless there is a review and maintenance owner. Use
[Translations And Localization](reference/GUIDE-TRANSLATIONS.md) for glossary,
terminology, screenshot, command, API field, and localized-homepage rules.

The public homepage in `repos\emulebb-pages` has localized entry pages. Those
pages should link back to this maintained guide set rather than carrying
stale, partial copies of the manuals.

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
| Development and validation guide | [reference/DEVELOPMENT-GUIDE](reference/DEVELOPMENT-GUIDE.md) |
| Active backlog and release dashboard | [active/INDEX](active/INDEX.md) |
| RC release control document | [active/RELEASE-0.7.3](active/RELEASE-0.7.3.md) |
| RC release checklist | [active/RELEASE-0.7.3-CHECKLIST](active/RELEASE-0.7.3-CHECKLIST.md) |
| RC release runbook | [active/RELEASE-0.7.3-RUNBOOK](active/RELEASE-0.7.3-RUNBOOK.md) |
| Backlog process | [reference/BACKLOG-PROCESS](reference/BACKLOG-PROCESS.md) |
| Evidence retention policy | [reference/EVIDENCE-RETENTION](reference/EVIDENCE-RETENTION.md) |
| CI baseline workflow | [reference/CI-BASELINE](reference/CI-BASELINE.md) |
| Release branching and packaging | [reference/RELEASE-BRANCHING-AND-PACKAGING](reference/RELEASE-BRANCHING-AND-PACKAGING.md) |
| eD2K ecosystem inventory | [reference/ED2K-PROJECT-INVENTORY](reference/ED2K-PROJECT-INVENTORY.md) |
| Dependency status | [dependencies/DEP-STATUS](dependencies/DEP-STATUS.md) |
| Historical-reference rules | [HISTORICAL-REFERENCES](HISTORICAL-REFERENCES.md) |

If a status claim outside `docs/active/` conflicts with `docs/active/`, treat
`docs/active/` as authoritative for current local backlog and release state.
For GitHub-primary backlog items marked `workflow: github`, the linked
`emulebb/emulebb` issue and the public `eMuleBB Roadmap` org Project #2 are
authoritative for workflow state.

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
