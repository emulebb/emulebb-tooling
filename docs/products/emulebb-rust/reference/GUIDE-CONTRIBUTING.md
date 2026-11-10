# Contribute To eMuleBB Rust

Start with a bounded issue on the [public roadmap](https://github.com/orgs/emulebb/projects/3),
then use managed isolated checkouts and normal review/checks. The active product
is the headless eD2K/Kad daemon, native REST API and embedded browser console.
Future autonomous Indexer/Arr phases remain gated designs.

## Find The Owning Repository

| Repository | Owns |
| --- | --- |
| [emulebb-rust](https://github.com/emulebb/emulebb-rust) | Daemon, protocol/core/metadata, REST and embedded WebUI |
| [emulebb-tooling](https://github.com/emulebb/emulebb-tooling) | Product guides, OpenAPI, policies, backlog and shared checks |
| [emulebb-build](https://github.com/emulebb/emulebb-build) | Workspace setup, supported validation, packaging and orchestration |
| [emulebb-build-tests](https://github.com/emulebb/emulebb-build-tests) | Persisted integration/live/profile harnesses |

Read the [workspace policy](../../../WORKSPACE-POLICY.md), nearest repo `AGENTS.md`
and only the task-routed annexes. Stock/community eMule owns observable wire
behavior; MFC owns only explicitly assigned non-wire outcomes. Current aMule is
interop evidence, not an automatic behavior authority.

## Set Up Once, Keep Operator State Explicit

Follow the authoritative [Builder setup README](https://github.com/emulebb/emulebb-build#readme)
for materialization and its private Python bootstrap/lock. Inherit valid
`EMULEBB_WORKSPACE_ROOT`, external `EMULEBB_WORKSPACE_OUTPUT_ROOT` and
`CARGO_TARGET_DIR`; do not repair them inline or create repo-local build caches.
Source boundaries are `repos` and `workspaces`; generated output belongs outside
them under OUTPUT.

Use the exact Rust toolchain from `rust-toolchain.toml` (currently 1.98.1), the
pinned Python/locked dependencies from Builder, locked WebUI Node/npm inputs and
the supported platform C/linker tools. Both Rust sys crates compile external C;
see [native dependency coupling](../../../reference/GUIDE-PARALLEL-WORKSTREAMS.md)
before assuming a Rust worktree is self-contained. Topology baselines are not
substitutes for hosted immutable dependency pins.

The parent assigns one topic branch/check-out owner per repo, reserves shared
files and coordinates integration. Workers own edits, validation, granular
commits and review-ready PRs. Follow the
[parallel-workstream guide](../../../reference/GUIDE-PARALLEL-WORKSTREAMS.md);
do not create ad-hoc worktrees or switch someone else's branch. Editing and PR
preparation can proceed in parallel; heavyweight local validation remains
serialized through the workspace owner. Normal hooks remain mandatory.

## Run Supported Checks

From the Builder checkout, select the assigned registered workstream. For example:

```powershell
python -m emule_workspace build clients --workstream YOUR-WORKSTREAM
python -m emule_workspace test rust-unit --package emulebb-metadata --workstream YOUR-WORKSTREAM
python -m emule_workspace test rust-webui --workstream YOUR-WORKSTREAM
```

Replace the selector with the parent-assigned ID; commands above illustrate
different scoped checks, not a requirement to run all of them for every edit.
Use the smallest relevant set and the normal full gates required by the changed
contract. Source-set receipts must identify the actual selected revisions.
Live/soak/profile work uses persisted Harness entry points and needs its routed
policy and explicit allocation. Do not start extra local heavy jobs to fill idle
time or use a cache hit as proof for a different source.

## Orient In The Source

- `crates/emulebb-daemon`: CLI, bootstrap, logging and process startup.
- `crates/emulebb-rest` and canonical Tooling OpenAPI: routes, authentication,
  envelopes and API contracts.
- `crates/emulebb-core`: settings/application coordination and controller state.
- `crates/emulebb-ed2k`, `crates/emulebb-kad-*`: protocol and network behavior.
- `crates/emulebb-metadata`: SQLite ownership, identity and durable state.
- `webui`: packaged browser console; keep it aligned with the native API.

Keep changes in the owning layer and tests at meaningful public/lifecycle
boundaries. Use [Rust code-quality guidance](CODE-QUALITY.md) and preserve
single-pass hashing, protocol authority and immutable release provenance.
Minimal bootstrap TOML stability is separate from the explicitly unstable API
and database. Incompatible schemas require a fresh profile; no migration,
silent repair/reset or automatic unfinished-transfer continuation is implied.

## Submit And Follow Through

Link the existing owning issue and stable ID; do not duplicate work. Write
coherent, user-readable commit subjects including the item ID, because nightly
notes group those subjects automatically. Complete applicable normal local
hooks and required hosted/security checks, resolve review findings, and let the
parent coordinate dependent PRs, merge and safe cleanup. A branch or successful
compile alone is not delivered work.

Use [private security reporting](https://github.com/emulebb/emulebb-rust/security/advisories/new)
for suspected vulnerabilities; ordinary issues must contain synthetic or
sanitized evidence. The project is [GPL-2.0-only](https://github.com/emulebb/emulebb-rust/blob/main/LICENSE);
[third-party notices](https://github.com/emulebb/emulebb-rust/blob/main/THIRD-PARTY-LICENSES.md)
retain their own licenses. See the [active backlog](../active/INDEX.md) and
[release scope](../RELEASE-SCOPE.md) before proposing product expansion.
