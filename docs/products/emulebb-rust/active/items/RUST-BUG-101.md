---
id: RUST-BUG-101
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/19
title: Kad VPN searches complete before delayed results are collected
status: IN_PROGRESS
priority: Major
category: bug
labels: [kad, search, vpn, regression, release]
milestone: release-0.1.0-beta.2
created: 2026-10-02
source: public beta feedback in emulebb-rust issue 19
---

# RUST-BUG-101 - Kad VPN searches complete before delayed results are collected

## Symptom

The `0.1.0-beta.1` AppImage can connect to Kad through a VPN and retain a live
routing table, yet a public keyword search completes with zero results. Binding
to the VPN interface, binding to both its interface and address, restarting the
daemon, and disabling protocol obfuscation do not change the outcome.

## Reproduction And Root Cause

The plain WSL2 Docker + OpenVPN lane reproduced the failure with a controlled
one-second tunnel delay: Kad remained connected with dozens of contacts, emitted
the value-search request, and still completed with zero results.

Rust ran Kad discovery and value search as sequential phases under one 45-second
deadline. Discovery could consume essentially the whole lifetime, leaving the
first `SEARCH_KEY_REQ` only about 50 milliseconds to receive a reply. A valid VPN
reply arrived roughly 177 milliseconds after Rust had completed the search.
Interface binding and obfuscation were not causal; tunnel latency only exposed
the deadline race.

Stock eMule interleaves discovery and value requests and, after stopping new
search traffic, keeps the search registered for 15 seconds to accept delayed
results (`CSearch::PrepareToStop`).

## Fix Shape

- Bound phase-one discovery so the sequential Rust traversal reserves time for
  phase-two fanout and the normal per-query response budget.
- Stop emitting new phase-two requests at the 45-second active deadline, but
  keep collecting already-requested results for a separate 15-second grace.
- Keep the public REST search collector alive through both windows.
- Add a deterministic regression in which the result arrives after the active
  deadline but before the result grace expires.
- Retain a plain OpenVPN live lane with controlled tunnel latency and packet
  capture so the public failure mode remains reproducible.

## Acceptance Criteria

- [x] Reproduce the beta.1 zero-result Kad search through plain OpenVPN.
- [x] Prove interface binding and protocol obfuscation are not the cause.
- [x] Add a deterministic late-result regression.
- [x] Pass focused Kad/core tests, full workspace tests, policy, formatting,
  Clippy, diagnostics, WebUI tests, and debug/release builds.
- [ ] Pass the fixed candidate through the one-second OpenVPN latency lane.
- [ ] Publish `rust-v0.1.0-beta.2` native packages and versioned GHCR image.
- [ ] Update public issue 19 with the diagnosis, evidence, and release link.

## Evidence

Generated live reports and PCAPs remain below the external workspace output
root. They contain no committed VPN credentials, public addresses, search terms,
or result identities. The release record will retain only redacted summaries and
the published workflow evidence.
