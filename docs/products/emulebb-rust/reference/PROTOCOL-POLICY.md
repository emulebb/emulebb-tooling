# emulebb-rust Protocol Policy

This task-routed annex applies only to eD2K or Kad wire behavior, packets, tags,
capabilities, network identity, protocol state machines, or interoperability.

- Preserve stock/community eMule authority for eD2K and Kad wire behavior,
  packet and tag shapes, opcodes, interoperability state machines, advertised
  capabilities, and network identity.
- Maintained eMuleBB MFC may define an explicitly recorded non-wire operational
  or I/O outcome. Current aMule may provide interoperability evidence or an
  optimization candidate, but neither silently overrides stock wire behavior.
- Rust-native optimizations may change internal scheduling, concurrency,
  buffering, batching, or observability only when supported stock interactions
  retain their required external semantics.
- Broadband-oriented async I/O is the baseline, not a compatibility toggle.
  IPv6 remains parked and the protocol cores stay IPv4-only.
- Source Exchange is intentionally SX2-only. Absent `OP_REQUESTSOURCES` and
  `OP_ANSWERSOURCES` live paths are not regressions.
- Peer chat/captcha, peer preview, IPv6, and the stricter stock LAN-mode Kad
  flood distinction remain approved permanent omissions. Do not reopen them as
  incidental parity work.
- A default-on negotiated extension requires an explicit registry contract.
  `offerfiles-v1` remains in the Client gate until deterministic negotiation,
  malformed/rejected input, reconnect reset, stock fallback, current-aMule,
  stock eMule, and scale evidence passes.
- Protocol-adjacent changes require parity evidence through appropriate
  goldens, community baselines, tracing, live diffs, or packet captures.
