# Rules

- Read `EMULE_WORKSPACE_ROOT\repos\eMule-tooling\docs\WORKSPACE-POLICY.md`
  before workspace work; it is authoritative for workspace-wide rules.
- This file contains tooling-local deltas only. Do not duplicate branch,
  worktree, setup, dependency, or build/test policy here.
- This repo owns central workspace policy, active backlog docs, helper scripts,
  shared hooks, and static policy audits.
- Keep workspace-wide directives in `docs\WORKSPACE-POLICY.md`; repo READMEs
  and AGENTS files should point there instead of restating it.
- Helper scripts and docs must use `EMULE_WORKSPACE_ROOT` style paths, not old
  fixed machine-local workspace paths.
- Use Doxygen-style comments for new reusable code surfaces; keep trivial glue
  comments sparse.
- Update `docs\RESUME.md` only at session termination or explicit handoff.
- When a tooling helper launches `emule.exe`, pass `-c` so the config root is
  explicit.
