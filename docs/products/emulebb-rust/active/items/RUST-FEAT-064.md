---
id: RUST-FEAT-064
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/245
title: Address unusual native paths through lossless API locators
status: OPEN
priority: Minor
category: feature
labels: [rust, api, paths, unicode, portability]
milestone: post-beta-polish
created: 2026-11-06
source: Operator-approved Rust async I/O and path portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/245. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-064 - Address unusual native paths through lossless API locators

## Summary

Own approved follow-up 9. Let authenticated API/UI operations identify supported
native paths without interpreting their human-readable escape strings as
filesystem names. Prefer profile-scoped opaque locators backed by existing
native path records. This is post-beta backlog work.

## Current Findings

At review commit `43855fba`, NativePath stores exact Unix bytes or Windows
UTF-16 units and exposes escaped display text for invalid Unicode. Ordinary
Unicode JSON paths work, and native-byte files can be discovered and served
through a valid shared root. Display strings are not a general round-trip
encoding: JSON cannot directly carry arbitrary Unix bytes or unpaired UTF-16.

Root/path request DTOs are Unicode strings. Some root handling passes through
display strings, so preserving an unusual file inside an ordinary root does
not prove that every unusual root can be configured or addressed by the UI.
Escaped output is not permission to reconstruct an OsString from display text.

## Representative Sites

- `crates/emulebb-metadata/src/native_path.rs`: storage versus display.
- `crates/emulebb-metadata/src/schema.sql`: `local_paths` and native identity.
- `crates/emulebb-core/src/shared_directories.rs`: root request/view models.
- `crates/emulebb-rest/src/handlers/shared_files.rs` and response models.
- `webui/src/views.tsx`: root actions currently pass displayed path strings.
- `crates/emulebb-core/tests/native_path_shared_dir.rs`.

## Intended Shape

Separate a display label from an actionable locator. Reuse existing native path
records where possible, with profile scope and stale-identity/generation checks.
An opaque locator must not become an unchecked raw filesystem capability.

If configuration of a path without an existing record requires an encoded
native representation, define one explicit bounded tagged form using the
existing NativePath codec. Validate platform, encoding, NUL/path rules, allowed
root scope, and authorization. Do not silently reinterpret a foreign platform's
bytes or fall back to a display string when a locator is invalid.

Evolve DTOs, OpenAPI, validators, and the SPA together. Beta compatibility may
break deliberately; no parallel legacy endpoint or ambiguous escape-decoding
shim is required. Native runtime locators are not a portable-profile format,
and Rust database upgradeability is outside this item.

## Acceptance Criteria

- [ ] Supported non-UTF-8 Unix and unpaired-UTF-16 Windows paths can be addressed
      through an explicit locator without replacement characters or wrong opens.
- [ ] Display strings that resemble escape sequences cannot select a different
      native path; operations resolve native records, not rendered labels.
- [ ] Stale, foreign-profile, foreign-platform, malformed, and unauthorized
      locators fail explicitly and cannot act on a reused/wrong file identity.
- [ ] Discovery, list/display, root actions where supported, restart, rename,
      and hash-based serving retain exact native path identity.
- [ ] Valid Unicode paths remain easy to use; API/SPA contract changes have
      authentication, bounds, and integration coverage.
- [ ] No source rename, payload rehash, arbitrary filesystem access, or
      cross-platform byte reinterpretation is introduced.

## Validation and Dependencies

Use synthetic byte/code-unit fixtures, literal escape-looking names, composed
and decomposed text, and profile-isolation/stale-locator tests. Gate real
filesystem cases by actual representability. Coordinate comparison with
RUST-BUG-161 and retain packaged platform evidence in RUST-CI-008.
