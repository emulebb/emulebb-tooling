---
id: FEAT-099
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/104
title: Add app event webhooks for controller automation
status: OPEN
priority: Minor
category: feature
labels: [webhook, rest, automation, controllers, notifications, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-30
source: operator request for app events webhook backlog coverage
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/104. This local document is retained as an engineering spec/evidence record.

# FEAT-099 - Add app event webhooks for controller automation

## Summary

Add an opt-in outbound webhook surface for app events that external
controllers can consume without polling every REST endpoint. This is the
supported replacement direction for legacy direct app notifiers such as SMTP:
eMuleBB emits structured events to operator-configured webhook targets, and
external automation decides how to notify, schedule, or integrate.

## Intended Shape

- Provide an opt-in webhook configuration surface with one or more target URLs.
- Emit structured JSON events for important app transitions such as startup,
  shutdown, server/Kad state changes, transfer completion, transfer errors,
  import/acquisition actions, shared-library hash completion, and health
  warnings.
- Use bounded background delivery so webhook latency never blocks UI, protocol,
  hashing, upload, or download paths.
- Include retry/backoff, delivery timeout, and queue-size limits.
- Add a simple signing or shared-secret mechanism so receivers can verify the
  source when webhooks leave loopback.
- Expose delivery diagnostics through logs and REST status.

## Scope Constraints

- Do not replace the REST API; webhooks are event notification, not command
  execution.
- Do not send raw search terms, filenames, peer IPs, credentials, or private
  profile paths by default.
- Do not deliver webhooks from protocol hot paths synchronously.
- Do not revive SMTP/email notification code. Email, chat, or push delivery
  belongs in external automation fed by these webhooks.
- Do not make public-network behavior depend on webhook delivery success.

## Acceptance Criteria

- [ ] Webhooks are disabled by default and require explicit configuration.
- [ ] Event schemas are documented and versioned.
- [ ] Delivery is queued, bounded, timed out, and retried with backoff.
- [ ] Webhook failures are visible in diagnostics without blocking app work.
- [ ] Sensitive event fields are minimized, redacted, or opt-in.
- [ ] Tests cover disabled mode, successful delivery, timeout, retry, queue
      overflow, shutdown drain, and signature verification.

## Validation

- `python -m emule_workspace validate`
- focused native or harness tests for webhook queue and event serialization
- REST/status contract tests for delivery diagnostics
- x64 Debug and Release app builds before implementation commit
