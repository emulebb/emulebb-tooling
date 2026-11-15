# eMuleBB Resume Handoff

Use the [PM coordination policy](reference/PM-COORDINATION-POLICY.md) for the
standing operating routine and [Release Scope](products/emulebb-rust/RELEASE-SCOPE.md)
for product boundaries and holds. GitHub issues and Project #3 own workflow state.

## Operator Finish Line

The operator narrowed this chunk to a stable merged main, documentation and
integrated-workstream cleanup, then stop. Do not start more backlog work, another
nightly, or a poweroff operation from this handoff. Use Android emulators unless
the operator asks for a phone test. Beta 3 promotion remains held.

## Delivered Source And Packages

- Rust [PR #333](https://github.com/emulebb/emulebb-rust/pull/333) delivered the
  Android 12+ launcher/service, signing and packaging, storage handling, mobile
  WebUI, diagnostics and branding. Its source is
  `23e685b87bb76db21489c9b1cc725dd0da4241c1`.
- The signed universal APK and both native Android archives are public in
  [nightly `0.1.0-beta.2.nightly.20261115.g23e685b8`](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.2.nightly.20261115.g23e685b8).
  [RUST-FEAT-056](products/emulebb-rust/active/items/RUST-FEAT-056.md) owns exact
  producer identities, public-byte hashes and API 31–37 emulator evidence.
  [Platform instructions](products/emulebb-rust/reference/GUIDE-DOWNLOADS-PLATFORMS.md)
  separate the APK from experimental Termux/native archive usage.
- [PR #334](https://github.com/emulebb/emulebb-rust/pull/334), merged at
  `e735319bbd7b72cbd21dac6ef172d318b3543947`, repaired boolean settings PATCH,
  strict NAT null validation and typed profile-lease release. Its fresh-main
  workflows and explicitly selected Android guest/TLS proof passed.
- [PR #335](https://github.com/emulebb/emulebb-rust/pull/335), merged at
  `0840e9005fd2ab28e9cbe262054dd692262e5698`, delivered proof validation before
  payload I/O, parked-credit failure preservation, bounded deletion-marker
  reads, mobile keyboard-focus visibility and process-isolated executable
  copying in profile tests. The exact pre-merge source
  `c6b9ceff0590b222fe5c5cc23df8622c229809d1` passed all six local stages and
  all applicable hosted checks. The local report is
  `reports/local-check/emulebb-rust/20261115T075009Z-41880a82`, relative to
  inherited `EMULEBB_WORKSPACE_OUTPUT_ROOT`. Fresh merged-main workflows are
  separate evidence; consult their actual results before claiming main green.

PRs #334 and #335 did not republish the APK. Do not assign their provider pins
or source identities to the existing public release.

## Retained Limits And Open Owners

- [#162](products/emulebb-rust/history/items/RUST-BUG-136.md) is closed and
  Project #3 Done. Its archived spec records bounded reads and restart/retry proof.
- [#250](products/emulebb-rust/active/items/RUST-BUG-166.md) retains request
  correlation and solicited-answer admission beyond delivered proof-before-I/O.
- [#155](products/emulebb-rust/active/items/RUST-REF-016.md) retains the broader
  persistence owner, friend CRUD and separate first-bind/add/flush boundary.
  [#233](products/emulebb-rust/active/items/RUST-FEAT-062.md) remains a related
  storage-contract owner.
- [#297](products/emulebb-rust/active/items/RUST-CI-043.md) retains the broader
  configuration/API review; revision/ETag designs are not accepted implementation.
- [#226](products/emulebb-rust/active/items/RUST-FEAT-056.md) retains Android
  endurance, native archive/Termux runtime and other recorded gaps. Emulator
  screen-off smoke is not 24-hour proof. Historical physical-phone evidence
  uses an older source. Public serving was not demonstrated. Boot resume is
  deliberately deferred; manual user launch is accepted.

Keep source qualification distinct from published bytes. Preserve the signing
key and operator profiles, and leave unrelated workstreams and processes alone.
