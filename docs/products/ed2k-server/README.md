# ed2k-server

`emulebb/ed2k-server` is the eMuleBB-managed, Linux-first Rust eD2K index-server
fork and the workspace's sole local deterministic server. Keep it close to
upstream: prefer harness-side adaptation and keep server changes minimal,
generic, and upstreamable. It is not an eMuleBB production service or product
roadmap.

## Product role

- **Rust server:** the selected local deterministic server and managed reference
  implementation for bounded analysis and upstream contribution work.
- **Lugdunum:** a behavioral reference only. Observable wire behavior may
  inform clean-room tests; decompiled implementation code must not be copied.

Local live and parity campaigns use `ed2k-server` when they require a controlled
server. That selection does not make it a public production service or add it to
product release campaigns. The retired production-hardening program is
preserved in the history archive.

## Tracking

- [Archived production-hardening context](../../history/INDEX.md)
- [Repository issues](https://github.com/emulebb/ed2k-server/issues)
- [eMuleBB Roadmap](https://github.com/orgs/emulebb/projects/3)
- [Source repository](https://github.com/emulebb/ed2k-server)

New issues are appropriate for deterministic local-server capability, upstream
alignment, or upstreamable fixes. They must not recreate the retired
production-service program without an explicit operator decision.
