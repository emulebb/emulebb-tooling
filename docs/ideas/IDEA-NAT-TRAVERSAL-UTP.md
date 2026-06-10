# IDEA: NAT Traversal And µTP — aMule #583 / eMuleAI Analysis

> **Exploratory proposal only.** This document is analysis and design exploration,
> not approved scope or a current branch direction. Nothing here is committed to
> `main` until a future active item (e.g. `FEAT-018`, `FEAT-036`) explicitly
> promotes a specific slice. Reference material captured 2026-06-10.

## Context

`amule-project/amule` issue **#583** requests two connectivity features and
points at eMuleAI as the proof-of-concept:

- **NAT-T** — UDP hole-punching so **LowID↔LowID** peers (both behind NAT) can
  connect, which stock eD2K/Kad cannot do.
- **µTP** — UDP transport (LEDBAT congestion control), the transport BitTorrent
  uses for background-friendliness and better NAT behavior.

eMuleBB already tracks these as **FEAT-018 (µTP)**, **FEAT-036 (NAT traversal)**,
and **FEAT-032 (NAT mapping)**. IPv6 (FEAT-035) is set aside here.

## What eMuleBB already has

- Stock **Kad-buddy LowID-callback** baseline (BaseClient/ClientList/
  ClientUDPSocket/ListenSocket).
- Port mapping libs already linked: `miniupnpc`, `pcpnatpmp`, `iphlpapi`
  (statically; REF-020).
- **libutp is not vendored** yet.

## eMuleAI reference (local: `analysis/emuleai`)

eMuleAI is the same Windows MFC `srchybrid` lineage as eMuleBB, so its code is
readable reference (unlike aMule, which is wxWidgets and must reimplement).

- **µTP:** `srchybrid/eMuleAI/UtpSocket.cpp` (~1728 lines) + `Buffer.cpp/h`; a
  cohesive `CAsyncSocketExLayer` wrapper. **libutp itself is external** (MIT,
  ~6–8k lines of C) and must be vendored separately.
- **NAT-T is pervasive, not a module.** Symbol spread: `BaseClient.cpp` ~453,
  `ClientList.cpp` ~346, `ListenSocket.cpp` ~344, `ClientUDPSocket.cpp` ~241,
  plus DownloadQueue/PartFile/UploadQueue/UI and **75 private opcodes**.

## Honest effort estimate

For a developer fluent in the eMule socket stack:

| Feature | Lab PoC | Shippable (default-off, compat-safe, tested) |
|---|---|---|
| µTP | ~2 weeks | ~4–8 engineer-weeks |
| NAT-T | ~3–5 weeks | ~10–20 engineer-weeks |

The dominant cost is **compatibility + test**, not coding. eMuleAI gives working
reference code, but the eMuleBB base has diverged (different eMule baseline +
heavy eMuleBB refactors of exactly the touched files), so it is a
reimplementation guided by reference, not a cherry-pick.

## Key finding: no modified server required

eMuleAI's NAT-T sends only stock `OP_CALLBACKREQUEST` to the server — universal,
every eD2K server supports it. Everything else is peer-to-peer client opcodes
(`OP_EMULEPROT`) and Kad. So it is **deployable on the public network as-is**.
The "eServer Buddy" name means "a buddy that reaches the target via the server's
*stock* callback," not "needs a special server." Two paths:

- **eServer-Buddy relay (TCP):** a LowID asks a HighID buddy peer to relay; the
  buddy uses stock callback to pull the target in (the target need not support
  the protocol). Costs the buddy's bandwidth; needs a willing HighID buddy; both
  on the same server.
- **Kad rendezvous + UDP hole-punch:** serverless; `OP_RENDEZVOUS`/`OP_HOLEPUNCH`
  over Kad with symmetric-NAT port sweeping. Direct connection; needs both peers
  to support it; symmetric NAT can defeat it.

## Opcode audit (why not to byte-copy eMuleAI)

eMuleAI reuses stock client-opcode **values**, disambiguated only by TCP-vs-UDP
dispatch:

| eMuleAI opcode | Value | Collides with stock eMuleBB | Disambiguation |
|---|---|---|---|
| `OP_RENDEZVOUS` | 0xA0 | `OP_BUDDYPONG` (TCP) | UDP-only |
| `OP_HOLEPUNCH` | 0xA1 | `OP_COMPRESSEDPART_I64` (TCP) | UDP-only |
| `OP_SERVINGBUDDYPULL_REQ` | 0xA8 | `OP_KAD_FWTCPCHECK_ACK` (TCP) | UDP-only |
| `OP_SERVINGBUDDYPULL_RES` | 0xA9 | `OP_MULTIPACKET_EXT2` (TCP) | UDP-only |
| `OP_ESERVER_*` | 0xB3–0xBB | *(free gap after 0xB2)* | clean |

The `0xA?` reuse "works" only because client TCP and UDP opcodes dispatch through
separate switches; one stray TCP send of `0xA9` would be misparsed as
`OP_MULTIPACKET_EXT2`. Tag types are squatted too (the author's own note: "none
of the 0xA? tags is banned by any major MOD so we can use safely them").

**Conclusion:** adopt eMuleAI's *mechanics* as reference, but **re-allocate** all
new opcodes into a documented, reserved, transport-guarded range (ideally one
reserved extension opcode carrying a sub-type), prove stock peers ignore them
(packet-capture goldens), keep it default-off. That clean re-spec is the real
prerequisite — and the only version adoptable across clients.

## Honest benefit analysis

- NAT-T helps **only if you are yourself LowID.** A HighID peer (via UPnP/PCP,
  which eMuleBB already ships) already reaches every LowID by callback → NAT-T
  gives it nothing. The beneficiaries are **CGNAT / VPN-without-port-forward**
  users, most valuable for **rare/long-tail** files (eMule's niche).
- **Symmetric NAT** (common in CGNAT) defeats UDP hole-punch; the relay path
  routes around it at bandwidth/abuse cost.
- **Adoption-gated:** ~0% of the current network speaks these protocols, so it is
  largely eMuleBB↔eMuleBB until penetration grows — except the relay path can
  pull in stock LowID targets via stock callback.
- µTP standalone gives mostly latency benefit (only vs other µTP peers); its real
  value is as the UDP substrate for hole-punching.

The version that is genuinely worth it: a **jointly-specced, open eMuleBB+aMule
NAT-T** (issue #583 shows aMule wants it too) rather than a private clone — that
is the network-effect play *and* the only thing that fits eMuleBB's
"no private protocol fork" rule.

## Recommendation

1. **µTP first:** self-contained transport, no eD2K-semantics fork, default-off;
   builds the UDP-demux + capability-negotiation plumbing NAT-T also needs.
2. **NAT-T as an open cross-client spec:** start from the stock Kad-buddy path +
   bounded hole-punch + diagnostics; defer the eServer-buddy/relay private-opcode
   surface until a clean opcode allocation + parity goldens + abuse bounding
   exist. Coordinate with aMule.

Both are post-0.7.3 (0.8.x). See also
[IDEA-LIBTORRENT-MESH](IDEA-LIBTORRENT-MESH.md) for the alternative of reusing
libtorrent instead of hand-porting this stack.
