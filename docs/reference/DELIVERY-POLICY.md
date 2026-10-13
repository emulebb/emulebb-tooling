# Delivery Policy

Read the [Workspace Policy](../WORKSPACE-POLICY.md) first. This annex is
mandatory only for work that creates commits, pushes changes, manages branches
or pull requests, merges work, cleans delivery state, or creates release tags.

## Commits And Branches

- Every managed-repo commit represents one coherent outcome. Stage explicit
  paths; never use `git add -A` or `git add .` in a mixed tree, bundle unrelated
  existing edits, or push WIP/debug commits.
- Routine work stays on the setup-selected integration branch. Short-lived
  branches are exceptional and, when explicitly requested, use
  `feature/<topic>`, `fix/<topic>`, or `chore/<topic>`. Never use `stale/*` as
  an active target without an explicit historical-comparison request.
- Treat the end of every coherent work chunk as a mandatory commit boundary.
  During complex work, also create granular commits at independently
  reviewable, validated intermediate checkpoints; do not accumulate the whole
  task into one final commit.
- Feature, bug, refactor, and CI backlog commits include their stable item id.
  Do not create release tags without separate operator approval after proof.

## Pull Requests And Completion

- Work performed on a non-default branch is not complete until its full
  delivery lifecycle is finished: commit coherent changes granularly, push the
  branch, open a pull request targeting `main`, resolve required checks and
  reviews, merge the pull request, delete the source branch both remotely and
  locally, fetch with pruning, switch back to `main`, fast-forward it, and
  verify a clean worktree. Never end completed work on an unpushed branch, an
  unmerged pull request, or a dangling topic/tracking branch.
- Preserve meaningful granular commits when merging. Use a repository-allowed
  rebase or merge-commit method for a multi-commit pull request; do not squash
  it into one commit. Squash is acceptable only when the pull request already
  contains one coherent commit or when the operator explicitly requests it.
- Before final handoff, audit open pull requests plus local and remote
  non-default branches in every touched repository. Merge completed work and
  delete branches that are integrated or superseded. Explicitly designated
  historical `stale/*` archives may remain. If required external state makes a
  merge impossible, the work remains incomplete: leave a pull request with the
  exact blocker recorded and do not report the task as complete until a later
  continuation merges it and performs the cleanup above.

## Push And Handoff

- Never leave agent-created tracked or untracked files uncommitted when moving
  to another chunk or ending a turn. Finish and commit the chunk, or remove
  only the agent's own incomplete files and edits before stopping. Rerun
  `git status --short --branch` in every touched repository and require a clean
  worktree before handoff.
- Push each validated granular commit to its configured upstream before
  beginning the next chunk and before final handoff. If a push is blocked, stop
  before starting more work and report the committed local SHA. Never
  force-push or rewrite published history without explicit operator approval.
