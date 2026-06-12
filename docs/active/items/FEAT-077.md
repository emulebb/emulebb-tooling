---
id: FEAT-077
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/73
title: Auto-managed upload friend-slot candidates without mutating manual friends
status: OPEN
priority: Minor
category: feature
labels: [upload, broadband, friends, friend-slot, seeding, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-24
source: GitHub issue #3 and review of historical Broadband 0.60 auto-friend logic
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/73. This local document is retained as an engineering spec/evidence record.

# FEAT-077 - Auto-managed upload friend-slot candidates without mutating manual friends

## Summary

Historical Broadband `0.60` carried an opt-in `BBAutoFriendManagement` feature
from commit `7158312` (`Auto-friend fast HighIDs feature`). The old code tried
to automatically add fast HighID upload clients as Friends after they had
downloaded a configured percentage of the requested file, and remove friends
again if they became slow or LowID.

Do not copy that implementation directly. The old behavior appears to have
confused "Friend" with "Friend Slot": it called `CFriendList::AddFriend()` but
did not enable the new friend's friend-slot flag, so users expecting an
"auto friend slot" could see no scheduling effect. The old demotion path also
removed any slow or LowID friend without tracking whether that friend had been
auto-created, which could silently delete user-managed friends from
`emfriends.met`.

This future item should revive only the useful product idea: automatically
identify good HighID upload peers for seeding priority, while keeping manual
Friends and persistent friend data safe.

## Historical Behavior To Preserve Only As Reference

- Preference key: `BBAutoFriendManagement`.
- Default: `0` disabled.
- Values `1..100`: uploaded-percentage threshold for promotion.
- Promotion condition:
  - client is HighID
  - client is not already a Friend
  - current session upload exceeds the configured percent of the requested file
  - old code only evaluated this while the waiting queue was non-empty and the
    client was not currently classified as slow
- Demotion condition:
  - client is a Friend
  - client is LowID or classified as slow
- Old slow-client state was based on `m_caughtBeingSlow` and
  `BBSlowDownloaderSampleDepth`; current eMuleBB uses the newer
  slow-upload warmup, accumulated slow/zero time, recycle, and cooldown model.

## Known Problems In The Old Implementation

- `AddFriend(this)` created a persistent Friend but did not call
  `SetFriendSlot(true)`, so "auto friend" did not necessarily mean
  "auto friend slot".
- There was no marker separating auto-managed friends from manual friends.
- The demotion path could remove a user's manual friend when the client became
  LowID or slow.
- Promotion was based on percentage of file size rather than sustained upload
  quality alone, making tiny files promote too easily and very large files
  promote rarely.
- Friend-list writes happened from upload scheduling behavior via `SaveList()`,
  so an active session could churn persistent friend metadata.
- Persisted auto-added Friends survived restart without any retained reason or
  policy metadata explaining why they were added.
- The behavior was not surfaced clearly in UI or logs, making it hard to
  diagnose GitHub issue #3 style reports.

## Intended Shape

- Add a new opt-in setting disabled by default.
- Treat this as upload/seeding policy first, not as uncontrolled persistent
  friend-list mutation.
- Prefer a transient/session-scoped "auto friend-slot candidate" or
  "auto upload priority candidate" state before considering persistent Friend
  writes.
- If persistent Friend writes are supported, require a separate explicit legacy
  compatibility option and mark auto-managed friends distinctly in memory and
  on disk where possible.
- Never delete or demote a manual Friend through automatic upload policy.
- Make "auto Friend" and "auto Friend Slot" semantics explicit in the UI label,
  preference name, and product docs.
- Use current eMuleBB slow-upload tracking and cooldown state instead of the old
  `m_caughtBeingSlow` counter.
- Expose clear diagnostics when a client is promoted, suppressed, or demoted:
  HighID/LowID state, upload rate, session bytes, file size/threshold, cooldown
  state, and whether the entry is auto-managed or manual.
- Keep manual friend slots as the stronger user-directed scheduling exception.

## Scope Constraints

- Do not copy old `BBAutoFriendManagement` behavior directly into `main`.
- Do not make automatic friend management enabled by default.
- Do not remove, overwrite, or downgrade manual Friends.
- Do not make LowID transition alone delete persistent friend data.
- Do not bypass existing crypto identity checks in `GetFriendSlot()`.
- Do not let auto-managed candidates bypass banned/bad-client checks.
- Do not weaken FEAT-015 fixed-cap upload scheduling or FEAT-023 queue-score
  semantics without a separately documented decision.
- Do not add broad release-control behavior such as PowerShare, Share Only The
  Need, or release bonus under this item.

## Acceptance Criteria

- [ ] setting is disabled by default and clearly labeled as an advanced
      upload/seeding policy
- [ ] automatic promotion can be represented without persistent Friend writes
- [ ] manual Friends and manual friend slots are never deleted by auto policy
- [ ] if persistent auto Friends are implemented, auto-managed entries are
      distinguishable from manual entries
- [ ] HighID-only promotion, LowID suppression, and slow-upload cooldown
      interaction are covered by native tests
- [ ] friend-slot semantics are covered separately from friend-list membership
- [ ] diagnostics/logging explain every promotion and demotion decision
- [ ] live-profile validation confirms no friend-list churn or repeated
      promotion/demotion oscillation under real upload traffic

## Validation

- `python -m emule_workspace validate`
- focused native tests for:
  - auto-managed versus manual friend identity
  - promotion threshold behavior
  - friend membership versus friend-slot behavior
  - LowID suppression
  - slow-upload cooldown/recycle interaction
  - persistence opt-in behavior, if implemented
- upload queue scoring/seam tests for friend-slot priority interaction
- live real-profile upload run with diagnostics enabled
- x64 Debug and Release app builds before commit
