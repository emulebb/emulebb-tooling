# Release Branching And Packaging

This is the durable release policy for eMuleBB branch, tag, version, and
portable package naming. The workspace-wide authority remains
[WORKSPACE-POLICY](../WORKSPACE-POLICY.md); this page gives the operational
shape release work should follow.

## Version Flow

Use explicit prerelease suffixes for public builds that are not stable:

```text
0.7.3-rc.1
0.7.3-rc.2
0.7.3
0.7.4
0.7.5-beta.1
0.7.5-rc.1
0.7.5
```

The first public eMuleBB release candidate is `0.7.3-rc.1`. The first stable
release target remains `0.7.3`. If a stable hotfix is needed after `0.7.3`,
ship it as `0.7.4`. Future prereleases use the future target version plus a
suffix; do not publish an unstable build as a plain patch number.

## Branches

`main` is the active integration branch. Normal feature work, hardening, and
future roadmap work happen on `main` unless the operator asks for a separate
short-lived branch.

Create a release branch when the operator starts release-branch stabilization:

```text
release/0.7.3
```

Release branches are stabilization branches. Some release candidates may be
prepared directly from reviewed `main` until the active release dashboard or
operator starts the stabilization branch. Once a release branch exists, accept
only:

- blocker and high-confidence bug fixes;
- release proof and packaging fixes;
- release documentation, changelog, and version metadata;
- localized release-string fixes required by the release gate.

Do not add new features or broad refactors to a release branch. New work goes
to `main` and waits for a later release.

For post-stable hotfixes, branch from the released stable tag if `main` has
moved on:

```text
emulebb-v0.7.3 -> release/0.7.4
```

Every applicable fix made on a release branch must be merged or cherry-picked
back to `main`.

## Tags

Published tags are immutable annotated tags. Do not move a published tag; if a
candidate is bad, publish the next candidate number.

Tag shapes:

```text
emulebb-v0.7.3-rc.1
emulebb-v0.7.3-rc.2
emulebb-v0.7.3
emulebb-v0.7.4
emulebb-v0.7.5-beta.1
```

Tags are created only after release proof passes and the operator gives a
separate tagging instruction.

## Packages

Portable ZIP assets include the version and architecture in the package name:

```text
emulebb-0.7.3-rc.1-x64.zip
emulebb-0.7.3-rc.1-arm64.zip
emulebb-0.7.3-x64.zip
emulebb-0.7.3-arm64.zip
emulebb-0.7.4-x64.zip
```

Optional controller packages follow the same version policy:

```text
emulebb-0.7.3-rc.1-amutorrent-x64.zip
emulebb-0.7.3-amutorrent-x64.zip
```

SBOM and manifest assets use the same package stem with their normal suffixes.

Main app ZIPs ship the runtime executable, the full release language DLL set,
package-facing notices, REST API docs, and SPDX SBOM/manifest provenance. The
legacy template-based `webserver` payload is not shipped in RC/stable release
assets; REST support is validated through the in-process API and documented
under the packaged `docs/` directory.

Official RC and stable packages use the workspace baseline MSVC toolset
documented in [WORKSPACE-POLICY](../WORKSPACE-POLICY.md), currently `v143`.
The `v145` toolset is a forward-compatibility probe target. It may be published
only as an explicitly labeled experimental CI artifact for tester feedback, not
as an official release asset, until the operator promotes it after sustained
green probe history, package proof, and smoke coverage.

If an experimental `v145` package is produced, the artifact name must make the
toolset status explicit, for example:

```text
emulebb-0.7.3-rc.1-v145-probe-x64.zip
```

Do not reuse the official package stem for a probe build. Probe artifacts must
not be attached to a stable release unless the release notes and operator
approval explicitly classify them as experimental.

The executable inside the standard package remains:

```text
emulebb.exe
```

The paired diagnostics package uses:

```text
emulebb-diagnostics.exe
```

Do not put the version in the executable filename. Version identity belongs in
Windows file properties, About/version UI, logs, package names, manifests,
SBOMs, release notes, and Git tags.

## Fix Timing

During RC:

- fix release blockers on reviewed `main` until the operator starts the
  release branch, then on `release/0.7.3`;
- publish `emulebb-v0.7.3-rc.2`, `rc.3`, and so on only when a new public
  candidate is needed;
- backport applicable fixes to `main`.

After stable:

- fix urgent stable regressions on the next patch branch, such as
  `release/0.7.4`;
- publish `emulebb-v0.7.4` after focused proof;
- backport applicable fixes to `main`;
- keep unrelated future work on `main` for the next feature release.
