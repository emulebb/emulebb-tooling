# Rust Code Quality Policy

This policy is the authoritative source-structure and test-placement annex for
`emulebb-rust`. It applies alongside the workspace-wide policy and the
repository-local `AGENTS.md` deltas.

## Responsibility-Based Structure

Source-file length is an advisory maintainability signal, not a validation
limit. No production or test source fails policy solely because of its line
count.

Organize modules around cohesive responsibilities and stable boundaries. Add a
module when a change introduces an independently nameable responsibility,
lifecycle, protocol component, persistence concern, API mapping layer, or
reusable subsystem. Keep crate roots and high-level orchestrators focused on
wiring, ownership, and public re-exports.

Do not split cohesive control flow merely to reduce file length. Conversely,
the absence of a size limit is not permission to append unrelated behavior to
an existing orchestrator.

When changing legacy mixed-responsibility code, prefer extracting the
responsibility being changed when that extraction is behavior-preserving and
proportionate to the task. Broad prerequisite refactoring is not required. If
an extraction would materially increase risk or obscure the behavioral change,
keep the change focused and record the remaining responsibility boundary in the
active refactoring item.

## Test Placement

Keep production modules focused on production behavior.

- Small white-box tests for private helpers may remain in a local
  `#[cfg(test)]` module when proximity materially improves understanding.
- Substantial unit-test suites belong in a sibling `tests.rs` file or a
  responsibility-focused `tests/` module tree.
- Public behavior, cross-module behavior, lifecycle scenarios, and protocol
  scenarios belong in the crate's integration-test directory when they can use
  the public surface without weakening coverage.
- Reusable fixtures and test utilities belong in explicitly test-only support
  modules. Production code must not depend on test modules or test-only helpers.

Test placement follows responsibility and scope, not a fixed line threshold.
Moving tests must preserve assertions and coverage and should be committed
separately from behavioral changes.

## Maintainability Advisories

The Rust policy checker reports large production files, large test files, and
substantial inline test modules as non-failing advisories. These reports are
review prompts, not exception mechanisms and not authorization to perform an
unrelated refactor.

Advisories list changed Rust files first (working tree and index, or the latest
commit when the tree has no Rust changes), followed by repository-wide context.
Changed-file reporting is capped only to keep CI output reviewable; it does not
create a source-size or file-count limit.

When an advisory applies to a changed file, review whether the change adds an
independently nameable responsibility. A reviewer may accept a cohesive large
file without an allowlist entry or written size exception.

## Lint Suppressions

Fix a warning when practical. When a protocol-shaped or orchestration boundary
deliberately triggers a lint, use the narrowest `#[expect(..., reason = "...")]`
on that item. Checked expectations fail when they become obsolete. Permanent
broad `#[allow(clippy::...)]`, dead-code, or unused-code suppressions are not
accepted by repository policy.

## Policy Maintenance

Machine-readable policy records describe current enforceable state only. Do
not append feature history, test inventories, previous values, or cap-change
narratives to `policy/rust-client.toml`. Git history and tracked item records
carry provenance.
