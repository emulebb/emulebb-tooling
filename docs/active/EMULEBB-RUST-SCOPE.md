# eMuleBB Rust Scope

`emulebb-rust` is a headless eMuleBB-family core client with local indexing.
The 0.0.3 target is not full historical eMule application parity. It is the
search, share, download, upload, queue, ED2K, Kad, persistence, and controller
surface needed for a real local client behind controllers such as aMuTorrent.

eMuleBB owns the common `/api/v1` REST contract; Rust implements that contract
directly and must not add private aliases or shims.

## Required Capability Target

- REST parity for the eMuleBB `/api/v1` controller surface: app, status,
  preferences, Kad, servers, searches, transfers, shared files/directories,
  uploads, upload queue, categories, friends, logs, and diagnostics where those
  resources are part of the common contract.
- Configured binding only: harnesses may pass operator-local inputs such as
  `X_LOCAL_IP` into generated config, but product code must not hardcode
  `X_LOCAL_IP`, loopback, wildcard, or machine-local listener assumptions.
- ED2K server interoperability: login, HighID/LowID, server list control,
  keyword search, source search, LowID callbacks needed for downloads, shared
  catalog offer, keepalive, packed payloads, large file tags, and required
  obfuscation paths.
- ED2K peer interoperability: hello/hello-answer, eMule extended info, secure
  identification, queue/rank, upload serving, download resume, compressed and
  uncompressed part transfer, hashset/AICH verification, Source Exchange v2,
  and callback downloads where required.
- Kad interoperability: bootstrap/routing from nodes, hello/ack, compatible UDP
  key/obfuscation handling, keyword/source/note lookup, publishing local shared
  files and sources, firewall checks, external port discovery, and Kad source
  supplement for downloads.
- Upload queue and friend basics needed by controller parity: friend slot,
  ban/unban, release/remove, score/wait/rank visibility, and current upload
  state.
- Indexing remains local SQLite/FTS client capability surfaced through existing
  search and shared-file resources; the 0.0.x line does not expose a
  coordinator or remote indexer API.
- Resource visibility should follow eMuleBB-style status surfaces where useful:
  RAM, buffered I/O, index/storage counters, transfer counters, upload counters,
  and REST-visible runtime counters.

## Required Local Matrix

Rust 0.0.3 parity requires deterministic local evidence for:

- Rust to Rust bidirectional transfer.
- eMuleBB to Rust bidirectional transfer through the common REST contract.
- Rust to aMule bidirectional transfer with the staged aMule daemon/control
  adapter.
- Rust REST route, envelope, validation, and capability behavior against the
  eMuleBB OpenAPI contract.

The aMule leg is compatibility proof only. It must use short deterministic
paths, configured LAN control binding, the shared goed2k launcher, and the
existing multi-client matrix. Missing aMule binaries block the Rust parity gate
when the aMule scenario is required.

## Deliberately Out

- Coordinator/control-plane APIs, remote indexer fleet behavior, and any REST
  contract not owned by eMuleBB.
- qBittorrent-compatible `/api/v2` and Torznab-compatible adapters inside Rust
  unless explicitly promoted later; Rust's common controller surface is
  `/api/v1`.
- Legacy HTML WebServer behavior: sessions, cookies, template state, low-rights
  mode, sort/refresh UI state, and host shutdown/reboot.
- Chat/captcha, IRC, social/buddy UI, rich remote shared-file browsing, and
  protocol preview advertising beyond the narrow paths needed for downloads.
- Source Exchange v1, eMule collection/archive edge workflows, media thumbnail
  generation, and weak or obsolete packet paths unless needed to preserve
  stock-compatible transfer/search behavior.
- Public-network hardening, adversarial Kad heuristics, full NAT/UPnP backend
  parity, IPv6/proxy edge paths, long-path aMule coverage, and live VPN
  campaigns as blockers for the 0.0.x Rust parity gate.

## Release Naming

The scoped Rust line is `emulebb-rust` 0.0.3. It should not be described as an
MVP in product or release text. Future release tags follow the eMuleBB family
shape, such as `emulebb-rust-v0.0.3`, and are created only after release proof
and explicit operator tagging approval.
