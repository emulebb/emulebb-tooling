# eMuleBB 0.7.3 Release Notes

These are public-facing notes for the eMuleBB 0.7.3 release line. The current
public release candidate is `emulebb-v0.7.3-rc.2` (with the matching
`amutorrent-v3.8.5-emulebb-v0.7.3-rc.2` controller companion). For the
RC2-specific delta over RC1, see the
[0.7.3 RC2 Changelog](RELEASE-0.7.3-RC2-CHANGELOG.md).

## Why This Release Matters

`0.7.3-rc.2` is the current public eMuleBB release candidate for users who want a
native Windows eMule client that keeps stock-compatible eD2K/Kad behavior while
making long-running broadband operation easier to manage.

The release focuses on:

- safer profile and package testing through explicit `-c` profile directories
- maintained broadband defaults for modern upload and large-library use
- clearer diagnostics for network, disk, sharing, and controller failures
- a trusted local REST API for automation and companion tools
- aMuTorrent, qBittorrent-compatible, and Torznab adapter workflows for local
  power-user stacks
- release packages with manifest, hash, and SBOM evidence

## Compatibility And Frozen Legacy

0.7.3 is the compatibility baseline before broader eMuleBB evolution. It keeps
the native desktop app, existing profile model, and stock-compatible eD2K/Kad
behavior as the release contract. Users should be able to evaluate the new
broadband defaults, diagnostics, packaging, and controller workflows without
being forced into a rewrite-style migration.

Some older eMule-era surfaces may still exist in code, resources, settings, or
old profiles. For this release, that means preserved and frozen: retained where
needed for compatibility or until a later removal pass, but not treated as new
support commitments. Release proof targets the native desktop workflow,
protocol compatibility, REST/controller behavior, profile and package safety,
and diagnostics. Frozen legacy surfaces are not release-gated support.

Future releases will evolve deliberately from this baseline. The current
roadmap favors focused modernization in connectivity, UI polish, startup and
large-library performance, controller reliability, and operations while keeping
profile safety and network compatibility explicit.

## Who Should Test It

Use this release with a backed-up or disposable profile first. Start without
automation, verify the native desktop app first, then add REST, aMuTorrent,
Prowlarr, Radarr, or Sonarr.

Do not point two eMule-family clients at the same live profile. Back up an
existing profile before first launch.

## Package Expectations

Expected 0.7.3 RC2 core packages are:

- `emulebb-0.7.3-rc.2-x64.zip`
- `emulebb-0.7.3-rc.2-arm64.zip`

The optional controller package is:

- `emulebb-0.7.3-rc.2-amutorrent-x64.zip`

All published packages should have:

- matching manifest, SHA-256, and SPDX SBOM artifacts where applicable

Do not treat a nightly or older beta package as this RC. Do not treat this RC as
the later stable `0.7.3` release; the stable tag will be `emulebb-v0.7.3` only
after separate stable proof and operator approval.

## Known Limits

- Frozen legacy surfaces are preserved only as compatibility or pending-removal
  baggage. They are not maintained release proof targets. Use the native
  desktop app and REST/controller docs for supported workflows.
- REST is a trusted local automation surface. It is not designed as a public
  internet service.
- IPv6 Kad, broader NAT modernization, and several future roadmap items remain
  post-`0.7.3` work unless the active release dashboard says otherwise.
- Do not assume packages are code-signed unless the release asset or release
  checklist explicitly records signing evidence. Unsigned ZIP contents may
  trigger Windows reputation or SmartScreen warnings.

## First Test Flow

1. Unpack the package into a new application directory.
2. Start with a disposable or backed-up profile:

   ```powershell
   emulebb.exe -c "$env:TEMP\eMuleBB-TestProfile"
   ```

3. Verify directories, connection state, logs, and shutdown before enabling
   controllers.
4. Run one small search or transfer.
5. Add sharing and automation only after the desktop app is healthy.

Use [Setup Guide](../reference/GUIDE-SETUP.md) for profile setup,
[Troubleshooting Guide](../reference/GUIDE-TROUBLESHOOTING.md) for support
evidence, and [Stack Integration Guide](../reference/GUIDE-STACK-INTEGRATIONS.md)
for aMuTorrent and Arr workflows.
