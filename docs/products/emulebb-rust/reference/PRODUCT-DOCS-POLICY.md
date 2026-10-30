# emulebb-rust Product Documentation Policy

This task-routed annex applies only to Rust product docs, backlog records,
release scope, design docs, or retained evidence.

- Keep `docs/products/emulebb-rust/active/` limited to `INDEX.md` and `items/`.
  Track every actionable slice and its progress in its owning item instead of
  creating branch-wide ledgers, reviews, or checklists.
- New Rust item IDs use `RUST-<CLASS>-<NNN>`. The migrated cross-product item
  `CI-054` keeps its stable legacy ID; do not reuse or renumber it.
- Keep current scope in `RELEASE-SCOPE.md`, implemented structure in
  `design/architecture.md`, and genuinely forward designs in `design/`.
- Published release notes belong to GitHub Releases. Persisted live and soak
  procedures belong to `repos\emulebb-build-tests`; product docs retain only
  stable conclusions or evidence references.
- Delete completed temporary plans after reconciling evidence into owning
  items. Archive only unique historical analysis that remains useful.
