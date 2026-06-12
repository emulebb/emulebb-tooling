---
id: FEAT-109
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/123
title: Materialize suite tool dependencies deterministically
status: OPEN
priority: Minor
category: feature
labels: [tooling, dependencies, live-e2e, deterministic-tests, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-02
source: operator request to download MediaInfo, FFmpeg, 7-Zip, and similar suite deps deterministically
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/123. This local document is retained as an engineering spec/evidence record.

# FEAT-109 - Materialize suite tool dependencies deterministically

## Summary

Make the workspace test and release suites download, pin, verify, and expose
external helper tools such as MediaInfo, FFmpeg, and 7-Zip through the suite
materialization path instead of relying on operator-global installs or whatever
is currently on `PATH`.

The goal is repeatable local and CI behavior: the same suite revision should use
the same helper binaries, with clear provenance and checksum validation.

## Intended Shape

- Add a suite-owned helper-tool manifest with version, architecture, download
  URL, archive layout, expected executable path, and SHA-256 checksum.
- Materialize tools into a deterministic workspace cache or tools directory
  controlled by `repos/emulebb-build`.
- Expose resolved tool paths through the existing workspace dependency contract
  or test configuration layer.
- Prefer portable archives over machine-wide installers.
- Fail early with actionable diagnostics when a tool is missing, corrupt, or
  does not match the pinned checksum.
- Keep download and extraction behavior reproducible across local developer,
  CI, release-campaign, and VM-test runs.

## Candidate Tools

- MediaInfo for media metadata verification.
- FFmpeg/ffprobe for media fixture generation and inspection.
- 7-Zip for deterministic archive extraction and packaging smoke tests.
- Future helper tools required by live E2E, release proof, or packaging
  scenarios.

## Scope Constraints

- Do not depend on mutable "latest" download endpoints.
- Do not silently fall back to arbitrary `PATH` tools for deterministic suite
  runs.
- Do not add machine-global installers as the default path.
- Do not mix app runtime dependencies with suite-only helper tools unless a
  separate product packaging decision requires it.
- Keep operator-local override support explicit for diagnosis, but report the
  override in suite evidence.

## Acceptance Criteria

- [ ] Suite helper tools are declared in a pinned manifest with checksums.
- [ ] Materialization downloads and verifies MediaInfo, FFmpeg/ffprobe, and
      7-Zip or records why a tool is intentionally omitted.
- [ ] Test and release suites consume resolved tool paths from workspace-owned
      configuration instead of raw `PATH` lookup.
- [ ] Missing or checksum-mismatched tools fail before a scenario starts.
- [ ] Suite evidence records tool names, versions, paths, and checksum status.
- [ ] Operator override paths are explicit and visible in evidence.

## Validation

- dependency materialization smoke on a clean workspace cache
- checksum mismatch negative test
- suite smoke using resolved MediaInfo, FFmpeg/ffprobe, and 7-Zip paths
- CI/release-campaign dry run proving no global tool install is required
