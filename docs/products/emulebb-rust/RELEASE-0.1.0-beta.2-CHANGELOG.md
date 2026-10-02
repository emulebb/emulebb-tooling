# eMuleBB Rust 0.1.0-beta.2 Changelog

Status: ACTIVE CANDIDATE. Final publication state is recorded only after the
approved `rust-v0.1.0-beta.2` tag and release workflow pass.

## Kad Search

- Fixed public Kad keyword searches that could complete with zero results on a
  VPN or another higher-latency path even though Kad was connected.
- Reserved part of the active Kad lifetime for the sequential value-search
  phase instead of allowing discovery to consume the entire shared deadline.
- Added stock-compatible receive-only result grace: no new requests are sent
  after the active deadline, while replies already in flight remain acceptable
  for 15 seconds.
- Extended the public REST search collector through the result-grace window.

## Validation And Test Infrastructure

- Added deterministic late-result regression coverage for the active-deadline
  boundary.
- Added a preferred WSL2 Docker lane using plain OpenVPN rather than Gluetun,
  with optional interface/IP binding, protocol-obfuscation control, packet
  capture, redacted evidence, and controlled tunnel-delay injection.
- Reproduced beta.1 with one-second injected tunnel delay and retained the same
  scenario as the beta.2 live regression gate.

## Compatibility

- No REST contract, profile schema, wire protocol, or release-scope change.
- The beta.1 feature set, platform matrix, known limits, and unsigned package
  posture remain unchanged.
