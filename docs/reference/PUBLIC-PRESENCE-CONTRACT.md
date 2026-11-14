# Public Presence Contract

The versioned contract at
`manifests/public-presence.v1.json` is the machine-readable authority for the
organization website and GitHub organization profile. It keeps current product
identity and release links, client lanes, repository roles, compatibility
references, public surfaces, and the stable installer owner aligned without
making one public repository mutate another. Schema version 1 requires the
`emulebb-rust` product record while remaining the same contract version for
existing consumers.

The Rust product record treats `nightly_url` as the current public download
channel. `published_version` and `release_url` retain the latest immutable
formal tag only as archival release metadata; current-facing generators must
not render them as a baseline, call to action, or recommendation.

## Reader routes and approved identity

Schema 1 retains all existing product, release, repository and installer keys.
The legacy `development_eta` key contains the next milestone without a date;
it must not introduce a relative delivery promise. Optional `reader_routes`
records the equally prominent Use and Develop routes, platform/download guide
and API-consumer guide. These link to the owning Rust guides rather than
duplicating their platform requirements or qualification claims.

Optional `branding` identifies the operator-approved proposal-5 Rust identity
derivatives by exact public path, role, dimensions, byte count and SHA-256.
Only the three logo tiles, touch icon, existing favicon path and approved
`1280x640` social card belong to that allowlist. Preserve supplied image bytes;
do not derive new artwork during public-surface generation. The site validator
checks asset identities, local image references and accessible dimensions/alt
text. Social metadata uses the approved canonical public card URL.

Proposal 5 replaces only the small 16/24/32/48-pixel icons with the approved
three-color solid block mark. The favicon contains exact 16/32/48-pixel PNG
payloads; the Windows application icon also retains the unchanged 64/128/256
frames. Artwork at 64 pixels and above, including README, logo, social and
touch artwork, remains byte-identical to proposal 1. The enlarged pixel-mark
preview is not application artwork. The supplied source inventory is retained
at `manifests/branding/proposal-5-source.json`; its proposal-time status describes
the supplied candidate, while `branding.selection` records operator approval.
`source_sha256` identifies that retained inventory. The public application
inventory in `branding.application_manifest_url` records exact product paths
and hashes, including Android's unchanged large donkey launcher art and the
mechanical alpha-only square used for Android notifications and themed icons.
The existing Linux package pipeline consumes the canonical Rust PNG files.
macOS CLI archives have no native app-bundle icon surface.

The generated organization profile uses the approved public logo origin or an
actual immutable merged Pages commit URL. Never invent a future commit pin.
The parent coordinates authoritative contract, Pages deployment and profile
integration; a local source reference does not establish live publication.
Legacy schema-1 contracts without these extensions still validate.

## Ownership

- `emulebb-tooling` owns the contract, validator, and deterministic organization
  profile renderer.
- `emulebb.github.io` owns presentation, locale templates, root-site deployment,
  and the stable `install.ps1` entrypoint.
- `emulebb/.github` owns the generated `profile/README.md` artifact and validates
  it against the tooling contract.
- Each repository publishes itself. Cross-repository automation may check drift
  or open a change, but must not push directly into another repository.

The contract intentionally excludes retired Go-server and BitTorrent product
families from current repository listings. The historical MFC `0.7.3` Suite
bundle remains a release fact and may mention its matching aMuTorrent artifact
only as history.

## Validation

Validate the contract from `emulebb-tooling`:

```powershell
python helpers\public-presence.py validate
```

Render or check the organization profile from a workspace containing the
optional `public-presence` profile:

```powershell
python helpers\public-presence.py render-org-profile --output ..\emulebb-org-profile\profile\README.md
python helpers\public-presence.py check-org-profile --input ..\emulebb-org-profile\profile\README.md
```

The root site consumes the same manifest during its own build. Its CI checks
tooling documentation links, renderer output, static-site rules, and the stable
installer checksum before publishing a GitHub Pages artifact.
