# Delivery Policy

Read the [Workspace Policy](../WORKSPACE-POLICY.md) first. This annex is
mandatory only for work that creates commits, pushes changes, manages branches
or pull requests, merges work, cleans delivery state, or creates release tags.

## Commits And Branches

- Every managed-repo commit represents one coherent outcome. Stage explicit
  paths; never use `git add -A` or `git add .` in a mixed tree, bundle unrelated
  existing edits, or push WIP/debug commits.
- Routine work targeting a protected default branch uses a workstream topic
  branch and pull request. A topic branch normally carries one related
  workstream across sessions for one or two days, with granular commits and
  one review-ready pull request for the batch. This is a target, not a merge
  deadline. Work targeting an explicitly selected unprotected
  integration branch stays on that branch. Topic branches use
  `feature/<topic>`, `fix/<topic>`, or `chore/<topic>`. Never use `stale/*` as
  an active target without an explicit historical-comparison request.
- Parent-coordinated parallel workstreams are the normal delivery model for
  independent outcomes. Keep exactly one active topic branch per repository
  per workstream and one assigned worker per checkout. Continue checkpoints on
  that branch until integration; do not create replacement or duplicate branches
  for the same outcome. Record any dependency on another unmerged workstream
  with the parent before branching from it. Cross-repository work should use
  the same topic name wherever practical.
- Workers own their assigned edits, validation, commits, pushes, review-ready
  pull requests, check monitoring, and review fixes. The parent owns scope,
  file reservations, shared Git administration, cross-repository dependencies,
  review, merge order, and cleanup. Workers must coordinate before changing
  reserved files, shared contracts, manifests, schemas, or lockfiles. A worker
  contribution is ready for parent review; only the parent reports integration
  and delivery as complete.
- For a parent-declared integration batch, workers push validated contribution
  commits without opening individual PRs. The parent reviews and integrates
  compatible authored commits into one linear branch and opens one coherent
  batch PR per affected repository after applicable combined validation. The
  [PM Coordination Policy](PM-COORDINATION-POLICY.md#batches-and-integration)
  owns selection, file reservations and scheduling. Other independent
  workstreams retain their normal worker-owned PR lifecycle.
- Use managed isolated checkouts as described in
  [Parallel Workstreams](GUIDE-PARALLEL-WORKSTREAMS.md). Do not switch another
  worker's branch, edit its checkout, change shared Git configuration, prune
  shared worktree records, or independently merge or remove a workstream.
- Treat the end of every coherent work chunk as a mandatory commit boundary.
  During complex work, also create granular commits at independently
  reviewable, validated intermediate checkpoints; do not accumulate the whole
  task into one final commit.
- Feature, bug, refactor, and CI backlog commits include their stable item id.
  Do not create release tags without separate operator approval after proof.

## Pull Requests And Completion

- Before opening a pull request, list that author's open pull requests against
  the same default branch. Parent-coordinated workstreams may have independent
  pull requests in the same repository. Honor the repository's enforced author
  limit: in `emulebb-rust`, the parent records the coordination reason on every
  affected pull request and applies the maintainer-controlled
  `parallel-approved` label to each. This is the supported parallel path, not a
  CI bypass. Uncoordinated human work remains limited to one open implementation
  pull request per repository; bot-authored dependency, security, and release
  pull requests remain exempt. Do not label unrelated pull requests to unblock
  a worker without coordinating their ownership.
- Do not open draft pull requests merely to retain work, and do not open a pull
  request for each granular commit. Keep the single work-in-progress branch
  pushed without a pull request until it contains a significant, coherent,
  review-ready chunk whose implementation and source inspection are accepted
  and whose focused local checks and normal hooks have passed. The parent may open this frozen
  review-ready PR while its applicable full local matrix continues, allowing
  hosted checks to run concurrently. State pending local proof explicitly;
  retain every applicable full local and hosted check as a merge condition on
  the final selected sources. Do not open a PR to hide an unresolved known
  failure or incomplete implementation, and do not report qualification as
  delivery.
- A checkpoint is complete when its scoped local validation passes, its
  granular commits are pushed, and the worktree is clean. Sessions and tasks
  may end at this checkpoint while the same workstream branch remains active.
  Report it as a pushed checkpoint, not delivered work. Do not open a pull
  request or delete the branch merely because a session or coherent slice ends.
- A batch is delivered only when its full
  delivery lifecycle is finished: commit coherent changes granularly, push the
  branch, open a pull request targeting `main`, resolve required checks and
  reviews, merge the pull request, and remove integrated delivery state. For a
  managed worker checkout, the parent verifies the merged result, removes the
  clean worktree and its integrated branch, and reconciles the registration.
  Do not switch a shared canonical checkout to finish a worker's lifecycle.
  For a conventional topic checkout, delete the source branch remotely and
  locally, fetch with pruning, return to `main`, fast-forward it, and verify a
  clean worktree. An explicitly active workstream branch may remain between
  checkpoints; it is not a dangling or stale branch.
- Preserve meaningful granular commits when merging. Use a repository-allowed
  rebase or merge-commit method for a multi-commit pull request; do not squash
  it into one commit. Squash is acceptable only when the pull request already
  contains one coherent commit or when the operator explicitly requests it.
- `emulebb-rust` is rebase-merge only. Merge its pull requests with
  `gh pr merge <number> --rebase --delete-branch`; never probe or retry that
  repository with `--merge` because merge commits are disabled.
- Before final handoff, audit open pull requests plus local and remote
  non-default branches in every touched repository. Preserve the explicitly
  active workstream branch. Merge review-ready batches and
  delete branches that are integrated or superseded. Explicitly designated
  historical `stale/*` archives may remain. If required external state makes a
  merge impossible, the work remains incomplete: leave a pull request with the
  exact blocker recorded and do not report the task as complete until a later
  continuation merges it and performs the cleanup above.
- Monitor GitHub Actions with the persisted compact poller from the tooling
  checkout: `python scripts/gh-actions-status.py --pr <number>`. It emits only
  state changes and final or failed names and URLs, and it checks both pull
  request checks and exact-head workflow runs so workflow-definition failures
  with no jobs are not hidden. After merging, monitor a distinct merge SHA with
  `python scripts/gh-actions-status.py --commit <sha> --repo <owner/repo>`.
  For a manual dispatch, rerun, or another workflow run sharing a commit with
  older failures, monitor only that run with
  `python scripts/gh-actions-status.py --run <run-id> --repo <owner/repo>`.
  Do not use `gh run watch`, streamed logs, or
  newly improvised polling loops for routine monitoring. Use `--once` for a
  non-waiting snapshot and inspect logs only after the compact poller reports a
  failure.

## Push And Handoff

- Run applicable local checks before commit and push. The shared pre-commit
  hook runs fast staged-file checks; the shared pre-push hook runs fast
  host-only checks for outgoing changes through
  `python -m emule_workspace local-check --repo <path> --stage push`.
  These cover privacy, hygiene, applicable policy/format/workflow checks and
  existing direct Python test owners. File-level Python tests are not a fixed
  time budget. Push checks never fall back to an entire Python suite or run
  broad Cargo builds, local platform matrices, WSL, or runtime staging. Commit
  and push checks use independent scratch without taking the heavy lock.
- Full local validation is explicit:
  `python -m emule_workspace local-check --repo <path> --stage full`.
  It selects all tracked HEAD inputs, including clean main or already-pushed
  commits, and runs applicable full host/platform checks under the workspace
  lock. Registered Rust build/REST validation requires the selected sources to
  support owned runtime staging; a missing prerequisite fails before staging. The
  parent schedules full runs. Both push and full evidence require clean,
  unchanged exact source revisions. Do not bypass hooks, reuse an old pass,
  silently skip a failed check, or repair inherited environment values.
- The parent verifies applicable GitHub workflows for full platform builds,
  tests and hosted analysis before merging. Rust additionally enforces its
  required status contexts in GitHub. Support repositories still require parent
  review of their workflow results even when branch protection does not enforce
  them. GitHub also owns permissions and publication. A local pass is not remote
  proof. Generated local evidence stays below the configured output root.

- Never leave agent-created tracked or untracked files uncommitted when moving
  to another chunk or ending a turn. Finish and commit the chunk, or remove
  only the agent's own incomplete files and edits before stopping. Rerun
  `git status --short --branch` in every touched repository and require a clean
  worktree before handoff.
- Push each validated granular commit to its configured upstream before
  beginning the next chunk and before final handoff. If a push is blocked, stop
  before starting more work and report the committed local SHA. Never
  force-push or rewrite published history without explicit operator approval.
