---
id: FEAT-107
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/121
title: Add upload under-target reason diagnostics
status: OPEN
priority: Minor
category: feature
labels: [uploads, diagnostics, bandwidth, observability, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-02
source: operator request to explain upload bandwidth underfill causes
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/121. This local document is retained as an engineering spec/evidence record.

# FEAT-107 - Add Upload Under-Target Reason Diagnostics

## Summary

Add clear diagnostics that explain why upload bandwidth is below the configured
target. The goal is to distinguish discovery, queue, slot scheduling, disk, and
socket backpressure problems without requiring verbose log spelunking.

## Intended Shape

- Emit a concise reason when upload bandwidth remains under target.
- Track reasons with counters suitable for logs and future UI/API exposure.
- Keep diagnostics low-volume and rate-limited.
- Make reasons actionable for live tuning and regression campaigns.

## Candidate Reasons

- no queued clients
- queued clients exist but none are eligible
- waiting for configured slot-open interval
- active slots exist but are too slow
- temporary/ramp-up slot denied by hard cap
- disk read pending or upload read backlog
- socket send backpressure
- bandwidth limiter already considers the target reached
- protocol/client state prevents useful data transfer

## Scope Constraints

- Do not change upload scheduling behavior in this diagnostics item.
- Do not log peer-identifying details unless existing upload diagnostics already
  permit that level.
- Do not emit the reason every tick; rate-limit repeated messages.
- Do not make diagnostics depend on UI visibility.

## Acceptance Criteria

- [ ] Under-target upload periods produce one current reason and counters.
- [ ] Repeated identical reasons are rate-limited.
- [ ] Reasons cover empty queue, ineligible queue, slow slots, disk waits,
      socket backpressure, and limiter state.
- [ ] Diagnostics can be correlated with upload slot/ramp-up decisions.

## Validation

- focused native tests for reason classification helpers
- manual live smoke with no queue, slow clients, and normal full-bandwidth runs
- x64 Debug and Release app builds before implementation commit
