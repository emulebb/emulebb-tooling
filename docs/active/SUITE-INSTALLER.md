# Suite Installer (generic Windows bootstrap)

Status: design / direction. Captured 2026-06-16. Defines the generic,
version-independent Windows installer for the eMuleBB Suite and where it lives.
The artifact itself is hosted on the org pages site; this is its design record.

## Decision

- The installer is **generic and version-independent**: it pins no product
  version and is **not** an asset of any product release (notably **not** the
  frozen `emulebb` MFC release). It always installs the **latest** of each product.
- **Home (artifact):** the org root pages repo **`emulebb/emulebb.github.io`**
  (checked out locally as `repos/emulebb-pages`), served at the site root. Chosen
  over `emulebb-tooling` because it gives the clean root URL **and** sits outside
  the `powershell-boundary` policy scope (no tracked-`.ps1` restriction, no policy
  amendment, no CI conflict).
- **Home (governance):** this doc + `ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md` in
  `emulebb-tooling`. Tooling documents how it works; pages hosts the artifact.
- **Entry point:** `irm https://emulebb.github.io/install.ps1 | iex`.

## Artifacts (in `emulebb.github.io` root)

| File | Purpose |
|---|---|
| `install.ps1` | the generic bootstrap (PS 5.1; `-Core mfc\|rust`, `-IncludeController`, `-DryRun`) |
| `suite-manifest.json` | source of truth for products, repos, asset patterns, core mapping |
| `install.ps1.sha256` | script integrity (verify-before-`iex` for the security-conscious) |

## How it works

1. Fetch `suite-manifest.json` from the same origin (`$BaseUrl`).
2. **eD2K core** by `-Core`: `mfc` → `emulebb` (MFC client, default); `rust` →
   `emulebb-rust` instead.
3. Always install the BitTorrent companion `qBittorrentBB`.
4. Optionally install the controller `aMuTorrent` (`-IncludeController`). The
   forward controller TrackMuleBB is added to the manifest when it ships.
5. For each product: resolve **`GET /repos/<repo>/releases/latest`**, pick the
   asset matching `assetPattern`, download, **verify SHA-256** against a
   `<asset>.sha256` sibling asset when published, extract under
   `%LOCALAPPDATA%\eMuleBB-Suite\<product>`.
6. Products with no published release yet are **skipped with a warning** (so the
   installer is safe to run before `emulebb-rust`/`qBittorrentBB` cut releases).

## Integrity

- The script is fetched over HTTPS from GitHub Pages; `install.ps1.sha256` lets a
  user verify it before `iex`.
- Each product download is SHA-256-verified against its own release's published
  checksum. **Recommendation:** every product release should publish a
  `<asset>.sha256` sibling so the installer's verification is always active.
- Artifacts remain **unsigned** (org policy); no code signing.

## Manifest shape

`cores` maps `mfc`/`rust` → a product key. `products.<key>` carries `repo`,
`role`, `assetPattern`. `alwaysInstall` lists products installed regardless of
core; `optional` lists opt-in products. Adding a product (e.g. `trackmulebb`) or
changing an asset pattern is a manifest edit only — `install.ps1` stays generic.

## Migration & status

- **Scaffold today.** `install.ps1` parses clean and is structured for real use,
  but the end-to-end flow is **not yet validated** (and `emulebb-rust`/
  `qBittorrentBB` have no releases yet).
- The org README one-liner still points at the **tested** RC bootstrap
  (`emulebb/releases/.../Bootstrap-eMuleBBSuite.ps1`). **Do not flip the public
  README to `emulebb.github.io/install.ps1` until the installer is validated**
  end-to-end against real releases (at minimum: MFC core install + qBittorrentBB).
  That flip is the final step.
- `ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md` is updated to reference this generic,
  pages-hosted approach as the target (superseding the RC-coupled bootstrap).

## Validation plan (before the README flip)

- [ ] `-DryRun` resolves latest releases for `emulebb` + `qBittorrentBB` and
      reports the correct assets.
- [ ] Real install of the MFC core + qBittorrentBB under a throwaway root.
- [ ] `-Core rust` path once `emulebb-rust` cuts a Windows release.
- [ ] SHA-256 verification exercised against a release that publishes `<asset>.sha256`.
- [ ] PSScriptAnalyzer / a smoke test wired into the shared harness.

Related: [PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md),
[SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md),
`plans/ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md`.
