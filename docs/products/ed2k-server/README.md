# ed2k-server

`emulebb/ed2k-server` is the eMuleBB-managed, Linux-first Rust eD2K index
server. It is an active Phase 1 production-hardening candidate: build and source
quality automation exist, while resource safety, protocol truth, operational
lifecycle, and scale qualification are tracked before any production
recommendation.

## Product role

- **Rust server:** the implementation being hardened for possible future
  production use.
- **goed2k-server:** the currently selected deterministic eMuleBB test server.
- **Lugdunum:** a behavioral reference only. Observable wire behavior may
  inform clean-room tests; decompiled implementation code must not be copied.

Adding `ed2k-server` to the portfolio and Suite board does not select it for
live, parity, or release campaigns. Harness selection remains a separate
operator decision after the tracked qualification gates pass.

## Tracking

- [Active engineering specs](active/INDEX.md)
- [Repository issues](https://github.com/emulebb/ed2k-server/issues)
- [eMuleBB Suite project](https://github.com/orgs/emulebb/projects/3)
- [Source repository](https://github.com/emulebb/ed2k-server)

GitHub owns workflow state, assignment, priority, discussion, and pull-request
linkage. The Markdown records under `active/items` own the durable engineering
scope and acceptance criteria.
