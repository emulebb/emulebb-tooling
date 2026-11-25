---
id: RUST-BUG-197
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/390
title: Serve classic source exchange from eligible upload peers
status: OPEN
priority: Major
category: bug
labels: [rust, parallel-non-gating]
milestone: post-beta-compatibility
created: 2026-11-25
source: Stock eMule and amule-org aMule protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/390. This local document owns the durable engineering specification and evidence.

# RUST-BUG-197 - Serve classic source exchange from eligible upload peers

Stock eMule `ac3d52e` and amule-org aMule `c5989ec4a` select
waiting and uploading peers from the complete file's upload list in
`KnownFile.cpp`. Rust currently returns an empty list for a shared file
with no download job.

Read a bounded set of eligible waiting or uploading peers for the share.
Use the announced listen endpoint and preserve requester exclusion and
useful-part checks. Classic replies omit genuine LowIDs. Cover a
complete share with no download job in v2 and v4 protocol fixtures.

This is a post-Beta 3 follow-up to
[route preservation](RUST-BUG-189.md). Retain evidence under
[RUST-CI-031](RUST-CI-031.md).
