# Parallel Workstreams

Managed Git worktrees let workers prepare independent changes and pull requests
while one parent coordinates delivery. The [Workspace Operations Policy](WORKSPACE-OPERATIONS-POLICY.md#parent-coordinated-workstreams)
owns layout and validation rules; the [Delivery Policy](DELIVERY-POLICY.md)
owns worker responsibilities, pull requests, integration, and cleanup.

Implementation and qualification are tracked by
[emulebb-build issue #28](https://github.com/emulebb/emulebb-build/issues/28).

## Prepare An Assignment

The parent selects one independently reviewable outcome, its issue, worker,
required repositories, reserved files, dependencies, and acceptance criteria.
Use an isolated worktree for every repository the assignment changes. Reuse
canonical supporting checkouts only when the assignment does not change them;
record their exact revisions with validation evidence.

Check inherited `EMULEBB_WORKSPACE_ROOT`, `EMULEBB_WORKSPACE_OUTPUT_ROOT`, and
`CARGO_TARGET_DIR` before the selected operation needs them. Stop on missing or
invalid operator configuration. Do not set per-worker replacements.

Run supported commands from the canonical `repos/emulebb-build` checkout.
Repository names remain unchanged inside each workstream:

```text
EMULEBB_WORKSPACE_ROOT/
  repos/                         existing canonical checkouts
  workspaces/agents/
    sample-fix/
      emulebb-rust/              one assigned branch and working tree
      emulebb-tooling/           present only when this task changes docs
```

Git worktrees share repository history, refs, and configuration. Workers must
not use shared Git administration to change another worker's state.

## Create And Inspect Checkouts

The parent creates an assignment with an explicit owner and topic branch:

```powershell
python -m emule_workspace workstream create sample-fix --branch fix/sample-fix --owner parent-agent --repo emulebb-rust
python -m emule_workspace workstream add-repo sample-fix --repo emulebb-tooling
python -m emule_workspace workstream status sample-fix --json
```

Use repeated `--repo` options to create several required checkouts together.
Creation also accepts repeated `--issue` and `--pull-request` links for the
assignment's GitHub references. `--owner` identifies the parent responsible for
lifecycle operations; it is coordination metadata, not an authentication boundary.

Each selected repository starts from its freshly fetched `origin/main`; the
registration records the exact base revision. An assignment that must depend
on an unmerged branch needs a parent-recorded baseline and dependency before
work begins. Do not infer a workspace-wide revision from one repository's
branch name or automatically adopt an existing checkout.

Registration lives below `EMULEBB_WORKSPACE_OUTPUT_ROOT/tmp/workstreams` and
is local orchestration state. GitHub issues and Project #3 retain workflow
ownership. A missing, interrupted, or conflicting registration requires parent
inspection; it never authorizes force-removal or deletion of unrelated files.

## Work And Validate

The worker edits only its assigned checkout and reserved files. Coordinate
schema, manifest, lockfile, API contract, or cross-repository changes through
the parent before crossing assignment boundaries.

Commit hooks derive the registered workstream from the checkout. The supported
manual validation entrypoint also accepts explicit selection:

```powershell
python -m emule_workspace local-check --repo <worker-checkout-root> --stage push --workstream sample-fix
```

Hooks use a workstream's registered Builder companion when it has one. Updating
canonical Builder main does not update that companion: the parent refreshes its
branch to include the daytime validation policy before the worker expects fast
push behavior. Keep the selected source identity; do not override it with a
different Builder or environment binding to change which checks run.

The selected source set must reach nested validators. A successful check of
another checkout is not evidence for the worker's branch. Push validation
requires clean participating source state and records exact source paths and
revisions; source changes during validation invalidate the result.

Ordinary commit/push checks run host-only static checks and direct Python test
owners with independent scratch, without the heavyweight lock. Push does not
compile Rust, start WSL/platform matrices or stage a runtime, and never falls
back to an entire Python suite. The parent verifies applicable GitHub workflows
before merging; Rust also enforces required status contexts. These provide the
daytime platform, test and hosted-analysis proof.

The parent schedules explicit full local proof with
`local-check --repo <worker-checkout-root> --stage full --workstream sample-fix`.
Full selects all tracked HEAD inputs even after push or on clean main, retains
the workspace lock and exact clean source fences, and requires owned-runtime
support before a registered product run can stage anything. Preserve inherited
Cargo/output roots. Workers must not bypass a busy lock or launch competing
runtime campaigns.
Lightweight commit checks use separate temporary inputs for each invocation.

## Rust And Native Dependencies

A Rust worktree also consumes external C sources: `emulebb-miniupnpc-sys` and
`emulebb-pcpnatpmp-sys` compile them through `cc`. Assignments must record these
inputs even when the worker changes only Rust files.

The sys build scripts resolve each native source root in this order:

| Native source | Inherited override | Workspace default |
| --- | --- | --- |
| MiniUPnP | `MINIUPNP_ROOT` | `repos/third_party/emulebb-miniupnp` |
| libpcpnatpmp | `PCPNATPMP_ROOT` | `repos/third_party/emulebb-libpcpnatpmp` |

An inherited override takes precedence. Otherwise, `EMULEBB_WORKSPACE_ROOT`
must be an existing absolute directory containing the Rust checkout; the
default paths above are relative to that workspace root. The scripts retain
a legacy fallback relative to `CARGO_MANIFEST_DIR`, which does not resolve the
native sources correctly from managed worktrees. Workers must stop and report
missing or invalid inherited configuration rather than repair it inline.
The authoritative implementations are the
[MiniUPnP build script](https://github.com/emulebb/emulebb-rust/blob/main/crates/emulebb-miniupnpc-sys/build.rs)
and [libpcpnatpmp build script](https://github.com/emulebb/emulebb-rust/blob/main/crates/emulebb-pcpnatpmp-sys/build.rs).

Use the Rust toolchain pin in
[`rust-toolchain.toml`](https://github.com/emulebb/emulebb-rust/blob/main/rust-toolchain.toml)
(currently `1.98.1`). For hosted native-source revisions, read `MINIUPNP_REF`
and `PCPNATPMP_REF` in the Rust
[CI](https://github.com/emulebb/emulebb-rust/blob/main/.github/workflows/ci.yml),
[release](https://github.com/emulebb/emulebb-rust/blob/main/.github/workflows/release.yml),
and [fuzz](https://github.com/emulebb/emulebb-rust/blob/main/.github/workflows/fuzz.yml)
workflows; keep those pins aligned when coordinating a dependency change.
Topology materialization baselines are not package source pins. Path overrides
select directories; the sys build scripts do not enforce their Git revisions.

The Builder's
[`release.py`](https://github.com/emulebb/emulebb-build/blob/main/emule_workspace/release.py)
uses the same override-before-workspace-default selection and records both
native Git commits in package provenance. Compare those recorded revisions
with the assignment's intended inputs; a correct path alone is not revision
qualification. Coordinate native-source or pin changes through the parent.


## Registered Rust Runtime Bundles

Registered Rust validation and native build/package commands stage their
regular daemon, diagnostic executables, native companion files and WebUI under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/tools/workstreams/<id>/emulebb-rust/<target>`.
The canonical operator bundle remains under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/tools/emulebb-rust`. Canonical and hosted commands
keep their existing default behavior.

A ready `stage.json` binds the workstream, selected Rust revision, native source
materials, producer flavor and all staged bytes. Builders prepare an owned
pending directory and publish it only after the native files and WebUI are
complete and source identity still matches. A failure before ready-directory
promotion commits restores the previous ready bundle. After promotion commits,
backup cleanup failure emits a warning and preserves the new ready bytes.
Rebuilding a flavor never carries old PDB files beside its replacement executable.

The full registered quality gate opts into this stage explicitly. Its persisted
REST harness verifies the source receipt and bytes before creating a disposable
profile or launching the fixed daemon name. A missing, stale or changed bundle
fails admission. The heavyweight lock and profile isolation remain required;
the operator/manual/soak runtime path does not change.

The parent selects exact registered sources and chooses when to run supported
build, test and full-validation commands. Working hours guide PM coordination;
they are not tooling gates. Long local tests may run during the day when useful.
The parent coordinates the shared validation slot and retains source, receipt
and cleanup evidence for each run.

The normal parent-owned workstream removal commands retire this generated
namespace after source and pull-request preflight, under the workspace lock.
Retiring only a non-Rust companion preserves the Rust stage. Cleanup does not
launch or stop processes, infer process ownership, remove a workspace lock, or
delete the canonical operator bundle.

## Review And Integrate

For independent PR delivery, workers push validated commits, open complete
review-ready pull requests, monitor checks, and address review. For a declared
integration batch, workers instead hand pushed authored commits and scoped
evidence to the parent without individual PRs. The parent uses a separate
managed integration branch, reviews and cherry-picks compatible contributions,
and runs applicable combined validation before opening one batch PR per repo.
Follow the [PM batching routine](PM-COORDINATION-POLICY.md#batches-and-integration)
for capacity, contract ownership, final local proof and hosted qualification.

The parent verifies the result and merges
in dependency order. Preserve required CI and CodeQL. For parallel Rust pull
requests by the same author, the parent records the reason on every affected
pull request and applies `parallel-approved` to each before expecting the
single-active-PR gate to pass.

Record related pull requests and dependency revisions. A contribution that
depends on an unmerged source revision remains dependent until the parent
reconciles it with the resulting default branch and validates the final diff.
Do not force-push published history without explicit operator approval.

## Finish Or Resume

Preserve a workstream between checkpoints until its scoped outcome is ready
and integrated. On resume, verify its registration, branch, origin, and Git
worktree identity before editing. A stale record is a diagnostic, not a cleanup
instruction.

### Retire One Integrated Companion

When a companion repository is integrated but another repository in the same
workstream is still active, the parent can retire just the completed checkout.
Run from the canonical Builder, outside the workstream being changed:

```powershell
python -m emule_workspace workstream remove-repo sample-fix --repo emulebb-build --owner parent-agent
```

This operation takes the normal heavyweight workspace lock, then the shared
lifecycle and Git guards. It verifies the assigned owner, exact registered
checkout, clean tracked/untracked/ignored state, no open pull request, and
integration into fetched `origin/main` by ancestry or patch equivalence. There
is no abandonment option. It refuses the last repository; use whole-workstream
removal when the entire assignment is finished.

Only the selected worktree is removed, without force. Its branch and history,
the other checkouts, and their registration and coordination fields remain.
An active companion may retain dirty or unpublished work; this operation does
not validate or discard that work.

The atomic registration records a retirement transition before Git removal.
An interrupted transition blocks source selection. Repeat the **same command**,
with the same repository and owner, from outside the workstream to resume.
It verifies the retained branch and either the original checkout or its
completed Git removal before publishing the remaining registration. A changed
branch, conflicting journal, redirected path, or missing checkout with remaining
Git administration is refused for parent inspection. Do not hand-edit the
registration, force removal, or prune records to make a retry pass.

After completion, a retired repository falls back through the existing canonical
topology. Before the next validation or prepared-image launch, the parent must
freeze and record the actual canonical source revision now consumed. Retirement
does not equate the old feature SHA with a rebase-merged SHA or relax an image's
exact source requirement.

After verifying merged work and remote branch disposition, the parent removes
the completed workstream:

```powershell
python -m emule_workspace workstream remove sample-fix --owner parent-agent
```

Removal must refuse dirty worktrees, unpublished commits, and unresolved pull
requests. The normal removal path requires the branch's changes to be integrated.
An explicitly abandoned assignment can use `--abandoned` after its pull requests
are closed, including work that was never published. This explicit parent path
retains each exact checkout head and its reachable history in the canonical
repository's local `refs/recovery/abandoned/<workstream-id>/<repository-name>`
reference before any runtime or checkout removal. It verifies the source head
and recovery reference with Git compare-and-swap; a conflicting recovery reference
refuses cleanup. Dirty, untracked or ignored files and open or unknown pull-request
state still refuse removal. Withdrawn code is not pushed by this operation.
Removal retains Git branches; the parent reviews the recovery refs and removes
integrated or superseded local and remote branches separately using exact-head
leases. Ordinary removal and `remove-repo` still refuse unpublished work.
The parent resolves each blocker explicitly. Do not switch canonical checkouts
to complete a worker's lifecycle or remove another agent's worktree.
