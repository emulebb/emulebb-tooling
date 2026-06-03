---
id: FEAT-110
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/129
title: Add configurable title bar status format
status: OPEN
priority: Minor
category: feature
labels: [ui, title-bar, status, preferences, observability, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-03
source: operator request to show additional runtime info in the title bar
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/129. This local document is retained as an engineering spec/evidence record.

# FEAT-110 - Add Configurable Title Bar Status Format

## Summary

Allow operators to customize the main window title with a format string that can
include additional runtime status such as uptime, upload/download limits,
current rates, IP address, connection state, and version information.

The default title should preserve the current compact behavior unless the user
chooses a richer format.

## Intended Shape

- Add a persisted title bar format preference.
- Render the main window title from a bounded, validated format string.
- Provide a reset-to-default path.
- Keep the update cadence aligned with existing UI title/rate refresh logic.
- Treat IP display as opt-in by placeholder, not automatic.
- Avoid network, DNS, or adapter probing work inside the title update hot path.

## Candidate Placeholders

Initial placeholder names should be stable, ASCII, and not localized. Candidate
tokens include:

- `{app}` for compact product name.
- `{version}` for product version and architecture where useful.
- `{upRate}` and `{downRate}` for current rates.
- `{upLimit}` and `{downLimit}` for configured transfer limits.
- `{uptime}` for current session uptime.
- `{server}` for server connection state or current server name.
- `{kad}` for Kad connection state.
- `{ip}` for the selected public, bind, or effective P2P IP value once the
  implementation defines the exact source.
- `{bind}` for configured bind interface or bind address.
- `{uploads}` and `{downloads}` for active transfer counts.

The implementation should start with a small reviewed token set and add more
only when each source is cheap, stable, and testable.

## Scope Constraints

- Do not change network binding, public-IP detection, or protocol behavior.
- Do not expose IP address by default.
- Do not localize placeholder tokens; only labels, help text, and examples
  should be localized.
- Do not let malformed format strings crash, assert, or make the title blank.
- Do not allow unbounded title growth.
- Do not block UI updates on network discovery or slow adapter enumeration.

## Candidate Implementation Notes

- Keep title rendering in a small helper that takes a snapshot of already-known
  runtime values.
- Clamp rendered title length before calling the window title API.
- Preserve unknown placeholders literally or report a validation error in the
  preferences UI; choose one behavior and test it.
- Store the preference in the normal preference path and expose it in an
  appropriate UI preferences page.
- Consider a short live preview in preferences so users can test the format
  without restarting.
- Add a default format that matches the current title, for example current
  transfer rates plus `eMuleBB` version text.

## Acceptance Criteria

- [ ] Users can configure and persist a title bar status format string.
- [ ] The default format preserves the existing title behavior.
- [ ] Supported placeholders include at least current upload/download rates,
      upload/download limits, uptime, app/version, and one explicit IP or bind
      token.
- [ ] Malformed, unknown, or overly long formats are handled safely.
- [ ] IP-related values appear only when the configured format includes an
      IP-related placeholder.
- [ ] Title updates use cached/current app state and do not perform blocking
      network or filesystem work.
- [ ] The preference has a reset-to-default path and clear user-facing labels.

## Validation

- focused native tests for title format parsing and rendering
- focused preference persistence tests if a seam exists or is introduced
- manual UI smoke for default, custom, malformed, long, and IP-containing
  formats
- localization coverage for any new UI strings
- x64 Debug and Release app builds before implementation commit
