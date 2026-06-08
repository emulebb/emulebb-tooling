---
id: FEAT-006
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/9
title: Kad — Add explicit trust, budget, and bootstrap observability counters
status: OPEN
priority: Minor
category: feature
labels: [kad, observability, diagnostics, counters]
milestone: ~
created: 2026-04-08
source: AUDIT-KAD.md (AUD_KAD_013, AUD_KAD_014)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/9. This local document is retained as an engineering spec/evidence record.

## Summary

The Kad subsystem has limited runtime observability. There is no easy way to
tell from logs or the UI how the routing table health is evolving, whether the
bootstrap is making progress, or how much abuse is being dropped.

## Proposed Counters / Telemetry

### Routing Table Health

| Counter | Description |
|---------|-------------|
| Verified contacts | Contacts that have completed a full round-trip verification |
| Probation contacts | Contacts admitted but not yet verified (FEAT-002) |
| Same-IP rejections | Hard-gated contacts per session |
| Verified-ID flips | Contacts whose Kad ID changed between probe rounds |

### Abuse Budget

| Counter | Description |
|---------|-------------|
| Dropped expensive requests | By opcode and reason (FEAT-004) |
| Malformed expensive requests | By opcode |
| Escalated abusive senders | Total temp-ban escalations |

### Bootstrap

| Counter | Description |
|---------|-------------|
| Bootstrap source URL | Last URL used for nodes.dat |
| Bootstrap acceptance reason | Why the snapshot was accepted or rejected |
| Bootstrap success/failure | Total bootstrap attempts and outcomes |
| Adaptive timeout estimate | Current FastKad timeout estimate + sample count |

### FastKad Quality

| Counter | Description |
|---------|-------------|
| Mean response time | Per operation type (bootstrap / hello / search) |
| Response jitter | Variance estimate |
| Stale sidecar count | Nodes with dormant FastKad hints |

## Exposure Points

- **Kad debug log** — existing `KademliaWnd.cpp` log area.
- **`KademliaWnd.cpp`** — add a stats pane or tooltip.
- **`theApp.emuledlg->...`** — hookable from status bar.

## Protocol Compatibility

All counters are local diagnostics — no protocol changes.

## Files

- `srchybrid/kademlia/utils/SafeKad.h` / `.cpp` — routing counters
- `srchybrid/kademlia/utils/FastKad.h` / `.cpp` — timing counters
- `srchybrid/kademlia/utils/KadPublishGuard.h` / `.cpp` — abuse counters
- `srchybrid/kademlia/utils/NodesDatSupport.h` / `.cpp` — bootstrap counters
- `srchybrid/KademliaWnd.cpp` — UI exposure
