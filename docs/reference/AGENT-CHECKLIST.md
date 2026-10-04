# Agent Checklist

This is an optional execution and handoff checklist. Policy authority remains
the [Workspace Policy](../WORKSPACE-POLICY.md) and the annexes it routes.

## Start

- Read the core policy once.
- Resolve the product from explicit wording or paths; if still ambiguous,
  default to `emulebb-rust`.
- Read the nearest repo `AGENTS.md` and only the annexes triggered by the task.
- Check status only in the active repo and support repos needed for current-state
  decisions or edits.
- Confirm required inherited environment values without assigning or repairing
  them.
- Identify one coherent outcome and its smallest relevant validation surface.

## Route

| Work | Read next |
| --- | --- |
| Rust daemon, WebUI, REST, persistence, protocol, or Cargo | [Rust Product Policy](../products/emulebb-rust/reference/AGENT-POLICY.md) |
| Harness, baseline/tracing, live network, soak, profile, VPN, or evidence | [Harness And Live Policy](HARNESS-LIVE-POLICY.md) |
| MFC source, C++ build, resources, localization, or release | [MFC Product Policy](../products/emulebb-mfc/reference/AGENT-POLICY.md) |
| Topology, build orchestration, packaging, policy/docs, forks, or automation | [Workspace Operations Policy](WORKSPACE-OPERATIONS-POLICY.md) |

Read multiple annexes only when the task crosses those boundaries. A Rust soak
needs Rust plus harness/live; routine Rust code does not need MFC or operations.

## Work

- Reuse the owning repo's helpers and entrypoints before creating new ones.
- Keep reads, edits, tests, and reporting inside the chosen product scope.
- Preserve unrelated existing work and stage explicit paths.
- Select evidence by the changed surface. Use the owning orchestration rather
  than ad-hoc build or live launch logic.
- Record skipped validation with a concrete reason.

## Finish

- Run scoped validation and `git diff --check` in each edited repo.
- Review diffs for private data, machine paths, real media titles, non-English
  prose, generated output, and accidental unrelated edits.
- Commit each completed coherent slice separately; include a tracked item id
  when the work belongs to one.
- Re-run `git status --short --branch` in every touched repo.
- Do not tag releases without separate approval. Refresh a handoff note only
  when ending the session or when explicitly asked.
