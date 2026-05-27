# eMuleBB 0.7.3 RC Release Notes

These are public-facing notes for the first eMuleBB release-candidate target:
`emulebb-v0.7.3-rc.1`. The release is not published until the active
[release dashboard](RELEASE-0.7.3.md), [checklist](RELEASE-0.7.3-CHECKLIST.md),
and operator approval say the tag and packages are ready.

## Why This Release Matters

`0.7.3-rc.1` is the first public eMuleBB release candidate for users who want a
native Windows eMule client that keeps stock-compatible eD2K/Kad behavior while
making long-running broadband operation easier to manage.

The release focuses on:

- safer profile and package testing through explicit `-c` profile directories
- maintained broadband defaults for modern upload and large-library use
- clearer diagnostics for network, disk, sharing, and controller failures
- a trusted local REST API for automation and companion tools
- aMuTorrent, qBittorrent-compatible, and Torznab adapter workflows for local
  power-user stacks
- release packages with manifest, hash, and SBOM evidence once the RC is cut

## Who Should Test It

Use this RC if you are comfortable with eMule-style clients and can test with a
backed-up or disposable profile. Start without automation, verify the native
desktop app first, then add REST, aMuTorrent, Prowlarr, Radarr, or Sonarr.

Do not point two eMule-family clients at the same live profile. Back up an
existing profile before first launch.

## Package Expectations

Expected RC package families are:

- `emulebb-0.7.3-rc.1-x64.zip`
- `emulebb-0.7.3-rc.1-arm64.zip`
- `emulebb-0.7.3-rc.1-amutorrent-x64.zip`
- matching manifest, SHA-256, and SPDX SBOM artifacts where applicable

Do not treat a nightly package as the RC. The final RC tag is
`emulebb-v0.7.3-rc.1`.

## Known Limits

- The legacy HTML WebServer template UI is frozen and not a maintained release
  proof target. Use the native desktop app and REST/controller docs.
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
