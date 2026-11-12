---
id: RUST-CI-049
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/325
title: Review the Linux daemon service and ownership contract
status: OPEN
priority: Minor
category: ci
labels: [rust, distribution-expansion]
milestone: ""
created: 2026-11-12
source: Operator-approved bounded Linux-service design review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/325. Project #3 owns placement; this item owns the engineering contract.

# RUST-CI-049 - Review the Linux daemon service and ownership contract

## Authorized Deliverable

The parent PM owns a bounded design review with Build/packaging and product
review. Produce one concrete recommendation, deployment/security tradeoffs,
required evidence and an explicit implementation/publication decision for
operator review. System-service delivery is deferred; this open item authorizes
review only, not a unit implementation or indefinitely parked service project.

## Review Contract

- Compare user and system service scope, dedicated identity and explicit
  profile/bootstrap-key/data ownership. Reuse one daemon, adjacent WebUI and
  the existing profile lock; introduce no second ownership/config database.
- Specify listeners, permissions, secret access, logs, start/stop/restart,
  graceful shutdown, stale-instance refusal and opt-in enablement semantics.
- Preserve data and profiles through update, explicit compatible rollback,
  uninstall and reinstall. Do not add migrations, reset, automatic networking
  or unattended moving-nightly updates.
- Treat Ubuntu 24.04 and Debian 13 x64/ARM64 as initial qualification targets,
  not completed support claims. Establish actual ELF/libc requirements from
  selected package bytes before declaring an oldest supported baseline.

## Acceptance

- [ ] A bounded recommendation states user/system scope, ownership, risks and
      the conditions for any future implementation authorization.
- [ ] A target-specific validation proposal covers install, explicit enablement,
      start/status/stop/restart, profile exclusivity, secrets/logs, deterministic
      transfer/resume, update/rollback and state-preserving uninstall.
- [ ] Dependencies on [#297](RUST-CI-043.md), [#234](RUST-FEAT-063.md) and
      [#298](RUST-CI-044.md) are resolved or explicitly identified for parent
      review; no contract is invented by a packaging script.
- [ ] The owning issue records the reviewed disposition. Implementation,
      installation, enablement and publication are separate later decisions.

This optional expansion review does not block Scoop or the mandatory core
Client gate. It changes no required CI/full-nightly check, support claim or
Beta 3/APK/signing hold. It authorizes no service framework, scheduler, hosting,
community submission, signing or paid infrastructure.
