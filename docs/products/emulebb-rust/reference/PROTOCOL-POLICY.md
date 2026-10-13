# emulebb-rust Protocol Policy

This task-routed annex applies only to eD2K or Kad wire behavior, packets, tags,
capabilities, network identity, protocol state machines, or interoperability.

- Preserve stock/community eMule authority for eD2K and Kad wire behavior,
  packet and tag shapes, opcodes, interoperability state machines, advertised
  capabilities, and network identity.
- Broadband-oriented async I/O is the baseline, not a compatibility toggle.
  IPv6 remains parked and the protocol cores stay IPv4-only.
- Source Exchange is intentionally SX2-only. Absent `OP_REQUESTSOURCES` and
  `OP_ANSWERSOURCES` live paths are not regressions.
- Protocol-adjacent changes require parity evidence through appropriate
  goldens, community baselines, tracing, live diffs, or packet captures.
