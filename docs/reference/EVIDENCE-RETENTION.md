# Evidence Retention

This reference defines how generated workspace evidence is classified before it
is archived, indexed, or cleaned. It applies to generated files under
`workspaces\workspace\state` and legacy generated report output under
`repos\emulebb-build-tests\reports`. It does not change source, docs, or
release package retention.

## Retention Tiers

| Tier | Purpose | Default Handling |
|---|---|---|
| `release-proof` | Active release, RC, artifact, or release-blocking evidence. | Keep until superseded and recorded. |
| `campaign-proof` | Broad regression, certification, live E2E, and overnight evidence. | Keep recent runs; prune superseded payloads. |
| `debug-profile` | Active profiling and crash output. | Keep only while active; prune after the payload retention window. |
| `legacy-generated` | Old reports under `repos\emulebb-build-tests\reports`. | Disposable; prune with current reports. |
| `nightly` | Automated nightly build or test evidence. | Keep latest successful and failed runs per stream. |
| `scratch` | Local experiments, command logs, caches, and transient progress notes. | Disposable after conclusions are promoted. |

## State Directory Expectations

- `state\test-reports` and `state\test-artifacts` may contain both compact
  summaries and very heavy payloads. Heavy payloads should be indexed before
  cleanup.
- `repos\emulebb-build-tests\reports` is legacy generated evidence. It is not
  durable just because older docs mention paths below it.
- `state\diagnostics` is for active debug/profiling evidence. It should not be
  treated as long-term release proof unless a release audit explicitly cites a
  specific run.
- `state\release`, `state\certification`, and release-campaign summaries may
  hold release-proof or campaign-proof evidence. Cleanup must be more
  conservative there than in scratch/debug folders.
- `state\preserved-evidence` is the only generated state folder intended to
  outlive routine cleanup. Use it for selected representative payloads, not for
  full unbounded dump sets.
- Root-level progress Markdown files under `state` are scratch notes. They are
  disposable once any durable conclusion has moved into `docs\active`,
  `docs\history`, a GitHub issue, or a release audit.

## Promotion Rule

Generated evidence becomes durable only when a maintained document names it and
records the fact or conclusion it proves. Maintained docs should not depend on
generated workspace paths as durable evidence references; once the useful fact
is promoted, the generated path remains cleanup-eligible.

## Cleanup Rule

Prefer targeted cleanup scopes over broad recursive deletion:

- routine cleanup for caches, path anomalies, old report payloads, old
  timestamped report runs, profiling payloads older than the retention window,
  and legacy build-test reports
- product-family output cleanup for `node_modules`, Rust `target`, and dist
  folders
- build-output cleanup for native build products and package staging

Routine cleanup is intentionally aggressive for generated report volume but
still dry-run by default. Current defaults keep report payloads for 24 hours,
timestamped report runs for 3 days, and build-log runs for 7 days while
preserving the newest build-log run window. Release state, package staging,
product-family outputs, and root-level legacy state stay explicit opt-in
cleanup scopes.

Before deleting large evidence sets, generate or refresh the heavy-evidence
index so the decision is visible. The index includes both current state output
and legacy generated reports.
