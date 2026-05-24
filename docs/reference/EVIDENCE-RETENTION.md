# Evidence Retention

This reference defines how generated workspace evidence is classified before it
is archived, indexed, or cleaned. It applies to generated files under
`workspaces\workspace\state` and does not change source, docs, or release
package retention.

## Retention Tiers

| Tier | Purpose | Default Handling |
|---|---|---|
| `release-proof` | Active release, RC, artifact, or release-blocking evidence. | Keep until superseded and recorded. |
| `campaign-proof` | Broad regression, certification, live E2E, and overnight evidence. | Keep recent runs; prune superseded payloads. |
| `debug-profile` | ETW, procdump, UMDH, pageheap, CPU spike, memory, and crash output. | Keep while active; preserve summaries. |
| `nightly` | Automated nightly build or test evidence. | Keep latest successful and failed runs per stream. |
| `scratch` | Local experiments, command logs, caches, and transient progress notes. | Disposable after conclusions are promoted. |

## State Directory Expectations

- `state\test-reports` and `state\test-artifacts` may contain both compact
  summaries and very heavy payloads. Heavy payloads should be indexed before
  cleanup.
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
records why it matters. Otherwise, it remains cleanup-eligible generated state.

## Cleanup Rule

Prefer targeted cleanup scopes over broad recursive deletion:

- routine cleanup for caches, path anomalies, and old lightweight payloads
- profiling cleanup for ETW, dump, UMDH, pageheap, and CPU spike output
- product-family output cleanup for `node_modules`, Rust `target`, and dist
  folders
- build-output cleanup for native build products and package staging

Before deleting large evidence sets, generate or refresh the heavy-evidence
index so the decision is visible.
