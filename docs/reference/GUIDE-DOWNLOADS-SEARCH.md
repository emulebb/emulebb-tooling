# Downloads And Search Guide

This guide covers search, download workflow, categories, filename handling,
transfer limits, and broadband upload behavior.

## Search Modes

eMule BB preserves native eMule search distinctions:

- Server search queries the current eD2K server.
- Global search uses the eD2K server network more broadly.
- Kad search uses decentralized Kad search.
- Automatic/controller search must map to one of the native search modes.

Use server search when a trusted server is enough, global search when wider
server coverage matters, and Kad when decentralized discovery is more useful.

Search result ceilings are configurable so modern sessions do not have to keep
old stock limits. eD2K expansion and Kad total/lifetime settings are persisted
preferences; exact keys and ranges are in [Preferences Guide](GUIDE-PREFERENCES.md).

## Search Result Quality

Search results can include bad names, misleading extensions, spam, or fake-file
signals. Treat the visible row as a candidate, not proof.

eMule BB separates **risk** from **evidence** in the search result list. Risk is
local evidence that a row may be spam, fake, mislabeled, or internally
inconsistent. Evidence is support for a specific claim about the row; it is not
a guarantee that the file is safe or authentic.

Check:

- filename agreement across sources
- suspicious extension/name combinations
- fake-file detector matches
- source count and source diversity
- comments and known metadata
- category destination and expected file type

Do not rely on one signal. File details and comments matter most for rare or
ambiguous files.

The compact **Risk** column summarizes local bad-signal evidence. Ctrl-hover a
search result for the desktop WHY view: risk, availability, complete-source
count, Kad publisher/name consistency when present, AICH hash when present, and
the detailed fake-file report.

The REST search result payload exposes the same model structurally:

- risk evidence: fake-file filter hits, spam score/status, bad or fake ratings,
  header/extension mismatches, executable/archive masquerade, implausible media
  metadata, and conflicting AICH hashes
- availability evidence: total sources, complete sources, directly observed
  clients, server observations, and Kad publisher counts
- name evidence: observed names, canonical-name agreement, ignored release/junk
  tokens, and meaningful name disagreement groups for the same hash
- Kad publisher evidence: Kad `TAG_PUBLISHINFO` decoded as publisher count,
  different-name count, raw Kad value, and a low/normal/high evidence band
- integrity evidence: AICH hash presence, pending header checks, cached header
  evidence, and detected-vs-claimed file type

Unknown evidence is neutral, not positive. For example, unknown Kad publisher
evidence means the row did not provide useful Kad publisher data; it does not
mean the row is trusted.

## Download Actions

Common actions:

- start, resume, pause, stop
- cancel with confirmation
- shifted cancel/delete paths for power-user no-confirm behavior
- open completed file
- open containing folder
- show details and comments
- copy ED2K links, names, paths, summaries, sizes, status, and progress
- change priority
- assign or move category

Keyboard details are in [Keyboard Shortcuts](KEYBOARD-SHORTCUTS.md).

## qBittorrent-Style Shortcuts And Batch Actions

eMule BB exposes selected qBittorrent-style shortcuts and batch menu actions
for faster desktop operation and controller parity. These are convenience
workflows over native eMule behavior, not a replacement behavior model.

Batch rules:

- destructive delete/cancel actions must preserve native confirmation and
  shifted no-confirm semantics.
- category actions must preserve eMule category ownership and destination
  behavior.
- paused and started adds remain distinct.
- completed and incomplete files remain different resources.
- copy actions should preserve enough detail for support, controller imports,
  or manual audits.

When a controller or shortcut behaves unexpectedly, compare it with the native
UI operation it is intended to represent.

## Categories

Categories are persistent workflow state. They affect organization, incoming
paths, filters, and controller expectations.

Good category practice:

- keep names short and stable
- avoid deleting categories that automation still uses
- move downloads intentionally before removing a category
- keep one default catch-all category
- use the category manager for normal edits and `Category.ini` only for careful
  maintenance

## Filename Cleanup

eMule BB can normalize download names on intake and completion. This is intended
to reduce obvious junk, not to erase identity.

Review before batch changes when:

- the filename becomes generic
- the extension does not match the expected type
- sources disagree
- risk/evidence feedback is mixed
- the result came from a controller import rather than manual selection

Filename cleanup settings and threshold preferences are documented in
[Preferences Guide](GUIDE-PREFERENCES.md).

## Completion Command

Completed downloads can optionally launch an external program. The feature is
profile-owned and should be used for trusted local automation only.

The relevant settings live under `[FileCompletion]`:

- `RunCommandOnFileCompletion`
- `FileCompletionProgram`
- `FileCompletionArguments`

Keep completion commands narrow, deterministic, and safe for filenames that
come from untrusted networks. Prefer explicit tools and explicit arguments over
shell expansion.

## Transfer Limits

Upload and download limits are finite runtime caps. eMule BB defaults are
modernized from older stock assumptions, but users should still set realistic
values for the current line.

Related controls:

- upload limit
- download limit
- max connections
- half-open/churn limits
- sources per file
- queue size
- file buffer size and time limit
- disk-space floors
- commit, sparse, and preallocation behavior

These settings are operational controls. Setting them too high can make network,
disk, or UI behavior worse even on a fast machine.

## Broadband Upload Policy

The broadband upload controller changes the old stock model where upload slot
count could grow heavily with available speed.

Released behavior:

- `MaxUploadClientsAllowed` is the normal upload-slot target.
- Slot decisions use a finite configured upload budget.
- Slow or zero-rate slots can be recycled after warm-up and grace periods.
- Cooldown prevents the same weak slot pattern from churning constantly.
- Collection uploads have an intentional compatibility exception.
- Low-ratio scoring can give selected clients a queue boost.
- Ratio and cooldown data can be shown in UI columns.

Practical tuning:

- set a finite upload limit first
- keep the slot target modest for broadband links
- let warm-up finish before judging a slot as weak
- use diagnostics if upload timer or disk IO pressure appears
- avoid unlimited experiments when diagnosing speed

The exact broadband preference keys live under `[UploadPolicy]` and are listed
in [Preferences Guide](GUIDE-PREFERENCES.md).

## Modern Defaults

Modern-limit work adjusted old conservative assumptions where release changes
landed:

- connection and churn defaults are less constrained
- per-client upload/socket behavior is better suited to faster lines
- disk buffering defaults support larger transfers
- source, queue, and search ceilings are more practical for current use
- selected timeouts and buffers are documented as tunable preferences

Existing profiles keep explicit stored values unless migration or normalization
rules say otherwise.

## File Details And Copy Workflows

Use details for:

- source/name comparison
- comments
- hashes and ED2K links
- category, priority, and path review
- risk/evidence warnings

Use plain ED2K links for import/controller workflows. Use summary-copy actions
for support notes or manual audits.

## Automation Discipline

Controllers should not flatten eMule BB into a generic download-client model.
Native distinctions matter:

- search network choice
- category
- paused vs started add
- delete/cancel semantics
- completed vs incomplete files
- source/risk/evidence feedback
- local path and profile ownership

When controller behavior surprises you, compare the request with the native REST
contract and the UI operation it is supposed to represent.

## Troubleshooting

No results:

1. Confirm server/Kad state.
2. Try a simpler query.
3. Try another search method.
4. Refresh trusted server/Kad bootstrap sources.
5. Compare controller search tokens with REST docs.

Slow uploads:

1. Set a finite upload limit.
2. Check upload slot target.
3. Review ratio/slot columns.
4. Check diagnostic IO and upload timer data.
5. Check active upload socket buffer samples.

Poor names:

1. Compare source names.
2. Check risk/evidence signals.
3. Review comments and file details.
4. Avoid batch cleanup until selected rows have enough supporting evidence.
