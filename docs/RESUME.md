# eMuleBB Resume Handoff

Use the [PM coordination policy](reference/PM-COORDINATION-POLICY.md) for the
standing operating routine and [Release Scope](products/emulebb-rust/RELEASE-SCOPE.md)
for product boundaries and holds. GitHub issues and Project #3 own workflow state.

## Accepted Delivery Checkpoint

- [Nightly `0.1.0-beta.2.nightly.20261113.g6429b952`](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.2.nightly.20261113.g6429b952)
  is published from Rust `6429b952eac6f19ee9bf084d3a84d5649dfba0c2`,
  [run 43375379055](https://github.com/emulebb/emulebb-rust/actions/runs/43375379055),
  release `443897042`. The parent accepted 81 public assets, 12 payloads, eight
  lifecycle platforms, both OCI variants, four native image proofs, signed
  subjects and six image tags. The run had 31 successful jobs and three
  intentional skips.
- The final public-byte receipt is
  `reports/nightly-publication-review/43375379055/final-acceptance.json`, SHA-256
  `f19189330222a114338501e78c4d3eed8bca891b006d71d293151a6c226fc241`.
  All report paths here are relative to inherited `EMULEBB_WORKSPACE_OUTPUT_ROOT`.
- Later README-only [PR #330](https://github.com/emulebb/emulebb-rust/pull/330)
  advanced Rust main to `bc0f319d1841e94e7a2b0f0d5428d318065b679c` and proved
  documentation-only CI for both the real PR and actual merged-main push.
  Receipts are `reports/ci-change-scope/pr330-f22daf58/acceptance.json` and
  `reports/ci-change-scope/main-bc0f319d/acceptance.json`. Measured workflow
  intervals were 146/91 seconds and lightweight docs steps 10/11 seconds;
  these are observations, not performance guarantees. Published binaries remain
  from `6429b952`, not `bc0f319d`.
- [Closed records](products/emulebb-rust/history/items/INDEX.md) retain #269
  secure-ident size admission, #278 bounded discovery fetching, #328 native
  Android TLS/startup and #327 trusted CI short-path evidence.

## Accepted Runtime Tuple And Limits

[Android run 43369243640](https://github.com/emulebb/emulebb-build/actions/runs/43369243640)
passed six causal TLS cases and fresh authenticated REST startup/shutdown in an
API 37/x86_64/16 KiB KVM guest. It executed a source-built release-mode daemon
on the development channel, version `0.1.0-beta.2`, from Rust `6429b952`;
it did not execute a downloaded nightly archive. The accepted material tuple is
Builder `3b9ddf42466b07f852f798f6967ca782484056a4`, Tooling
`26abd1eab97b28977f2d55adba17e6ba28821498`, Harness
`7c680ed68e478c2f22c56c65f21f12c3790d3826`, MiniUPnPc
`4e7a10948004ca2085ac8103e14fc77edb898b4c` and libpcpnatpmp
`a6e787f837e507336a8774522c33b54264ef4a4b`.

The receipt is `reports/android-cli-runtime/43369243640/acceptance.json`.
[Open #226](products/emulebb-rust/active/items/RUST-FEAT-056.md) retains the
explicitly unproved Android unavailable/degraded-network run, physical S24+
retest, published-archive execution, ARM/device, UI, transfer and VPN outcomes.
Beta 3 promotion and APK/signing remain held. Long soak remains deferred until
bugs/gaps are resolved and current aMule/stock Rust server inputs are qualified.

## Next Accepted Work

- [#155-A](products/emulebb-rust/active/items/RUST-REF-016.md): one bounded
  persistence owner and friend CRUD, with durable commit, then ordered cache
  publication, and success acknowledgement only after publication. Preserve
  cancellation-safe completion and shutdown drain/join.
- [#233](products/emulebb-rust/active/items/RUST-FEAT-062.md): reuse that storage
  owner for SQLite Kad snapshots and import-only met-file persistence, including
  remaining `nodes.dat` write-back. Keep generation/order and import barriers.
- [#297](products/emulebb-rust/active/items/RUST-CI-043.md) and its current
  config/API findings remain open. The delivered ready-bootstrap slice does
  not complete the broader review. Keep the 39-character shared starter key,
  minimum 32-character validation, snake_case keys and hard rejection of
  obsolete shapes; no aliases, mappings or migrations.
- [Build #62](https://github.com/emulebb/emulebb-build/issues/62): the operator
  approved a 128 GiB soft native-cache pool, 100 GiB minimum free floor plus
  40 GiB growth reserve after this nightly batch. This is **not implemented**;
  retain the current storage/environment until the parent allocates that slice.

Do not infer implementation authority or completed validation from this handoff;
use the owning accepted contracts and the PM policy linked above.
