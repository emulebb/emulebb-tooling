---
id: RUST-BUG-156
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/223
title: Give ED2K server settings one authority
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, config, api, webui, beta]
product: emulebb-rust
phase: Phase 0
milestone: rust-v0.1.0-beta.3
created: 2026-11-04
source: beta settings ownership and stock-default audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/223. This local document owns the durable engineering contract.

# RUST-BUG-156 - Give ED2K server settings one authority

## Summary

Make the `ed2k` settings block the sole authority for ED2K server behavior.
Remove duplicate Core ownership, use stock-safe defaults, and expose keepalive
as a minute-granular preference with zero meaning disabled.

## Intended Shape

- Remove Core `reconnect`, safe-connect, and startup-server insertion fields.
- Keep reconnect, safe connect, startup-server insertion, and server keepalive
  under `ed2k` only.
- Default safe connect and startup-server insertion to `false`.
- Replace arbitrary keepalive seconds with `server_keepalive_minutes`; accept
  zero as disabled and validate a bounded whole-minute value.
- Update daemon consumption, WebUI fields, OpenAPI, example/default settings,
  and focused tests as one breaking beta contract.
- Recreate beta profiles; add no migration, alias, deprecated key, or dual
  reader.

## Acceptance Criteria

- [ ] Exactly one settings field owns each ED2K server behavior.
- [ ] Effective runtime and startup-server merge read the same `ed2k` owner.
- [ ] Fresh defaults match stock: safe connect off, startup insertion off, and
      keepalive disabled.
- [ ] Keepalive is represented in whole minutes and converted once at the
      runtime boundary.
- [ ] REST/OpenAPI, WebUI, config serialization, validation, and daemon tests
      agree on the new schema.
- [ ] Harness profiles that require the 20-minute stock preference set it
      explicitly.

## Validation

- Focused settings serialization/default/validation and daemon-consumption
  tests.
- Focused WebUI and OpenAPI contract checks.
- Full Rust, tooling, and affected harness gates before delivery.
