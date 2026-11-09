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

The selected source set must reach nested validators. A successful check of
another checkout is not evidence for the worker's branch. Push validation
requires clean participating source state and records exact source paths and
revisions; source changes during validation invalidate the result.

Heavyweight local checks retain the existing workspace lock, Cargo target,
staged executable, and output paths. The parent schedules these operations;
workers must not bypass a busy lock or launch competing runtime campaigns.
Lightweight commit checks use separate temporary inputs for each invocation.

## Review And Integrate

Workers push validated commits, open complete review-ready pull requests,
monitor checks, and address review. The parent verifies the result and merges
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

After verifying merged work and remote branch disposition, the parent removes
the completed workstream:

```powershell
python -m emule_workspace workstream remove sample-fix --owner parent-agent
```

Removal must refuse dirty worktrees, unpublished commits, and unresolved pull
requests. The normal removal path requires the branch's changes to be integrated.
An explicitly abandoned assignment can use `--abandoned` after its pull requests
are closed and its work is published. Removal retains Git branches; the parent
reviews and removes integrated or superseded local and remote branches separately.
The parent resolves each blocker explicitly. Do not switch canonical checkouts
to complete a worker's lifecycle or remove another agent's worktree.
