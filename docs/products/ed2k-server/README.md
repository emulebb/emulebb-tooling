# ed2k-server

`emulebb/ed2k-server` is the eMuleBB-managed, Linux-first Rust eD2K index-server
reference fork. It is retained for analysis and potentially upstreamable
contributions. It is not an eMuleBB production service, product roadmap, or
future harness commitment.

## Product role

- **Rust server:** a managed reference implementation for bounded analysis and
  upstream contribution work.
- **goed2k-server:** the currently selected deterministic eMuleBB test server.
- **Lugdunum:** a behavioral reference only. Observable wire behavior may
  inform clean-room tests; decompiled implementation code must not be copied.

Keeping `ed2k-server` in the default workspace does not select it for live,
parity, release, or production campaigns. The retired production-hardening
program is preserved in the history archive.

## Tracking

- [Retired production-hardening roadmap](../../history/HIST-ED2K-SERVER-PRODUCTION-ROADMAP.md)
- [Repository issues](https://github.com/emulebb/ed2k-server/issues)
- [eMuleBB Roadmap](https://github.com/orgs/emulebb/projects/3)
- [Source repository](https://github.com/emulebb/ed2k-server)

New issues are appropriate only for analysis or upstreamable fixes. They must
not recreate the retired production-service program without an explicit
operator decision.
