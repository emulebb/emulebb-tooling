# Rules

- Read `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\WORKSPACE-POLICY.md`
  first; it is authoritative for workspace-wide rules.
- For policy, documentation-system, hook, or shared-helper work, also read the
  routed `docs\reference\WORKSPACE-OPERATIONS-POLICY.md` annex.

Everything below is this repo's local deltas only:

- This repo owns central workspace policy, active backlog docs, helper scripts,
  shared hooks, and static policy audits.
- Keep workspace-wide directives in the core policy or its narrowest applicable
  routed annex; repo READMEs and AGENTS files should link instead of restating.
- Helper scripts and docs must use `EMULEBB_WORKSPACE_ROOT` style paths, not old
  fixed machine-local workspace paths.
- Use Doxygen-style comments for new reusable code surfaces; keep trivial glue
  comments sparse.
- Update `docs\RESUME.md` only at session termination or explicit handoff.
- When a tooling helper launches `emule.exe`, pass `-c` so the config root is
  explicit.
