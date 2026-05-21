# Historical References

This repo preserves references to retired sibling trees when they are useful as
provenance or implementation history. The main example is the stale
experimental branch:

- branch name: `stale/v0.72a-experimental-clean`
- common local analysis checkout:
  `analysis\stale-v0.72a-experimental-clean`

## Rule

Treat the stale experimental branch as a historical reference source only.

It is:

- not an active branch target
- not a managed worktree
- not the default validation baseline
- not proof that a behavior is landed on current `main`

It may still be cited when it provides:

- the original provenance for a backlog item
- a useful reference implementation
- commit-level history for an idea later ported to `main`
- comparison context for dated review notes

## Documentation Conventions

When a doc mentions the stale experimental branch, the preferred interpretation
is:

- current backlog state is determined against `main`
- `docs/active/INDEX.md` owns the active landed/open status
- the stale branch is there to explain where an idea came from, not to revive
  that branch as an active workflow

References may appear in a few forms:

- `stale-v0.72a-experimental-clean`
- `analysis\stale-v0.72a-experimental-clean`
- old remote or tag spellings such as
  `remotes/origin/stale/v0.72a-experimental-clean`

Those all point at the same historical source family.

## How To Read Provenance Notes

- `source: stale-v0.72a-experimental-clean ...`
  Means the item was discovered or originally framed from that historical tree.
- `Status in stale-v0.72a-experimental-clean: ...`
  Means the historical tree had an implementation or disposition; it does not
  imply current `main` has it.
- `Port Status` or `Main Branch Status`
  These sections decide whether the work is actually live on current `main`.

## Related Docs

- [WORKSPACE-POLICY](WORKSPACE-POLICY.md)
- [../docs/active/INDEX.md](active/INDEX.md)
- [../README.md](../README.md)
