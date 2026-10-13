# Rust Code Quality Policy

This task-routed annex applies only to Rust source structure, test placement,
refactoring, maintainability, or lint suppressions.

## Responsibility-Based Structure

- Source length is advisory, never a validation limit.
- Organize modules around cohesive responsibilities and stable boundaries. Add
  a module for an independently nameable responsibility, lifecycle, protocol
  component, persistence concern, API mapping layer, or reusable subsystem.
  Keep crate roots and high-level orchestrators focused on wiring, ownership,
  and public re-exports.
- Do not split cohesive control flow merely to reduce length, and do not append
  unrelated behavior merely because no size limit exists.
- When changing mixed-responsibility code, extract the responsibility being
  changed when that is behavior-preserving and proportionate. Otherwise keep
  the change focused and record the remaining boundary in the active
  refactoring item.

## Test Placement

- Small white-box tests for private helpers may stay in a local `#[cfg(test)]`
  module when proximity materially improves understanding.
- Substantial unit suites belong in a sibling `tests.rs` or a
  responsibility-focused `tests/` tree.
- Public, cross-module, lifecycle, and protocol behavior belongs in integration
  tests when the public surface provides equivalent coverage.
- Reusable fixtures and helpers belong in test-only support modules. Production
  code must not depend on them.
- Placement follows responsibility and scope, not line count. Move tests
  without losing assertions or coverage and commit the move separately from
  behavioral changes.

## Maintainability Advisories

- Large production files, test files, and inline test modules produce
  non-failing review prompts, not exceptions or refactoring mandates.
- Reports show changed Rust files first, then repository context. Output caps
  keep CI reviewable and do not create size or file-count limits.
- For a changed-file advisory, review whether the change adds an independently
  nameable responsibility. Cohesive large files need no allowlist or written
  size exception.

## Lint Suppressions

Fix warnings when practical. For deliberate protocol or orchestration cases,
use the narrowest `#[expect(..., reason = "...")]` on the affected item.
Permanent broad `#[allow(clippy::...)]`, dead-code, or unused-code suppressions
are not accepted.

## Policy Maintenance

Machine-readable policy records describe current enforceable state only. Keep
feature history, test inventories, previous values, and cap-change narratives
in Git history or tracked item records, not `policy/rust-client.toml`.
