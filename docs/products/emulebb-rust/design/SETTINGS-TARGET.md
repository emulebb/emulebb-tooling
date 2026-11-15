# Configuration and settings target

**Accepted common contract; detailed leaf inventory still requires implementation review.**
The operator accepted the [Public Foundation](PUBLIC-FOUNDATION.md) on
2026-11-15. That is the master scope and behavior specification under
[RUST-CI-043 / #297](../active/items/RUST-CI-043.md). This document owns the
settings-specific detail. Acceptance of the common contract does not blindly
accept all candidate leaves in [SETTINGS-INVENTORY.json](SETTINGS-INVENTORY.json)
or claim implementation. Regenerate/check the final inventory from typed
settings definitions once implemented; do not create another runtime reader.

## Ownership and supported surface

TOML owns only process/profile/control-service bootstrap. SQLite exclusively
owns mutable product settings and durable product state. A restart requirement
does not make a setting bootstrap material. Runtime sockets, timers and active
work stay in memory; payloads, logs and diagnostics remain files.

Application groups are `network`, `transfers`, `storage`, `sharing`, `security`.
Each key has one typed definition, persistence owner and runtime consumer.
`emulebb-settings` owns types, defaults, bounds, units and whole-candidate
validation; `emulebb-metadata` owns coordinated transactions. Core coordinates
runtime application. REST/OpenAPI and SPA consume generated metadata rather
than independent default or validation lists.

JSON uses camelCase; SQL/Rust/TOML use snake_case; URL segments use kebab-case.
Names specify units such as BytesPerSecond and Seconds. Closed current types
receive normal validation, without shims, aliases, remapping, retired-input
lists or tests preserving removed names. Curate actual operator controls;
implementation tuning, generated identities and private keys are not settings.
Download priority and category priority defaults are absent.

## Bootstrap and profile

The sole TOML table is `[rest]`:

| Key | Default | Responsibility |
| --- | --- | --- |
| `bind_addr` | `0.0.0.0:20017` | Authenticated REST/WebUI listener |
| `api_key` | `change_me_123change_me_123change_me_123` | Accepted ready-package/fresh-profile starter secret |
| `web_root_dir` | Unset | Explicit assets directory; omitted default is `webui` beside executable |

Preserve existing bootstrap semantics, accepted key policy and minimum length.
Do not add secret generation, key-renaming or additional validation proposals
under this foundation. Keep secrets out of normal settings/status/log surfaces;
the separately owned authenticated private diagnostic contract remains intact.

Normal startup has only `--profile` as runtime configuration. Omission uses
`current_exe().parent()` on every platform; explicit relative paths use caller
CWD. Missing selected profiles can be created; read-only paths fail visibly.
Installed launchers may supply explicit writable profiles. Keep the fixed
profile-local bootstrap and database filenames. Do not add product environment
overrides or duplicate authorities.

## Default/custom state and settings writes

Persist the complete chosen structure with default/custom markers. A
default-marked leaf resolves directly from the running release at startup;
a custom leaf retains its saved value. No historical-default comparison or
intent tracking. Setting a value equal to the current default marks default;
reset explicitly marks default. Startup resolution needs no caller revision.

REST reads expose one coherent capture of saved settings/default markers,
resolved effective values, saved revision and application status. A write
requires the saved revision read by the caller, validates the entire candidate
and commits all changes atomically. Use checked revision arithmetic. Omitted
leaves stay unchanged; nullable values obey their typed meaning. There is no
full-representation ETag/digest CAS requirement. Runtime application changes
alone do not create a competing saved-settings validator.

Preserve the coordinated transaction/publication owner already implemented;
do not commission a second atomicity actor. After a valid save, a live apply
failure retains desired settings and reports failed fields and effective values.
Restart-bound leaves remain explicitly pending. Broader hot reconfiguration
is outside scope. Invalid candidates and revision conflicts save nothing.

The final exact document/marker encoding, field schemas and response/status
combinations must be recorded with the implementation inventory/OpenAPI before
the coordinated cut. Candidate defaults and bounds are not automatically
accepted simply because they appeared in the prior review inventory.

## REST, CLI and collections

Native settings live at `/api/v1/settings` and `/api/v1/settings/surface`, using
the common native data/meta and structured error conventions. Preserve current
native authentication; future adapters use their protocol's authentication with
the same secret. Typed bounds include request and response size limits.

Offline commands require explicit `--profile`:

```text
emulebb-rust --profile PATH settings get KEY
emulebb-rust --profile PATH settings set KEY VALUE
emulebb-rust --profile PATH settings reset KEY
```

They manage SQLite settings only, require the daemon stopped and use the existing
exclusive profile lease. Get prints only the resolved value; diagnostics go to
stderr. Each set/reset loads and validates the whole candidate, commits one key
atomically and advances revision without caller-supplied CAS. No JSON input
file or staged transaction. REST supports atomic multi-field changes.

Server entries, shared roots, categories, tags, friends and observations remain
dedicated collections, not settings blobs. IP-filter contents stay file-backed
with a configured source and explicit reload. Read-only network discovery
imports feed SQLite directly without retained met/dat files. Import scope
remains the implemented limited MFC scope; no Rust profile migration.

## Paths, numbers and deployment

Relative product paths resolve against the profile; absolute and supported UNC
paths are direct. No shell/environment/tilde expansion. Relative CLI profile and
import paths resolve against caller CWD. Explicit relative web assets are
profile-relative; omitted assets remain beside the executable. Expose resolved
paths where useful. Paths refer to the daemon/container filesystem.

Rates use bytes per second, storage sizes bytes, durations their explicit units.
Calendar timestamps use Unix seconds. JSON counters are numbers with documented
integer bounds and JavaScript precision limits; do not promise all 64-bit
integers are exactly representable in JavaScript or silently clamp them.

Docker uses `/config/emulebb-rust`, `/data/incoming`, `/data/temp`. Canonical
offline operations provision storage only on genuinely fresh first-run setup;
recover interrupted provisioning and preserve initialized profiles. Subsequent
launches pass only `--profile`. Saved settings own P2P interfaces and health
checks follow the configured listener. Existing Python harness owners prepare
new fixtures; no ad-hoc setup or parallel testing framework.

## Qualification boundary

Use the master specification's settings, revision, lease, restart/apply-failure,
Docker and combined-scale acceptance cases. Run normal checks and two review
rounds, retaining exact source evidence. This round ends at a tested pushed
checkpoint, with no PR/merge/publication until operator review. Future automatic
upgrades remain a design objective, not implemented machinery.
