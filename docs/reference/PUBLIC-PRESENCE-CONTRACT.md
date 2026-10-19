# Public Presence Contract

The versioned contract at
`manifests/public-presence.v1.json` is the machine-readable authority for the
organization website and GitHub organization profile. It keeps current product
lanes, repository roles, compatibility references, public surfaces, and the
stable installer owner aligned without making one public repository mutate
another.

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
