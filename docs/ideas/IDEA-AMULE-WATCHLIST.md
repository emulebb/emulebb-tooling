# IDEA-AMULE-WATCHLIST - aMule Reference Watchlist

> Exploratory only. This is not an active implementation plan, not release
> scope, and not current branch direction. Treat aMule as reference material
> unless a future `docs/active/` item explicitly promotes a narrow slice.

> Analysis based on `analysis/amule` materialized from
> `https://github.com/amule-project/amule`.
> Date: 2026-05-17

---

## Summary

aMule has limited immediate implementation value for eMule BB because the code
base differs materially in toolkit, build system, runtime assumptions, and app
structure. It remains useful as a compatibility witness and as a source of
focused protocol/file-format fixtures to revisit as aMule evolves.

Do not port aMule code directly by default. Mine it only for:

- wire-format fixtures and parser regression ideas
- offline file-format diagnostic ideas
- tag/name/type inventories for clearer compatibility tests
- future parity checks when aMule adds narrowly relevant behavior

Any promoted work should be implemented through eMule BB-native seams, tests,
or diagnostics, with stock eMule/eD2K/Kad behavior treated as the authority.

## Protocol And Tag Test Ideas

aMule has focused Kad/eD2K tag serialization tests in
`analysis/amule/unittests/tests/CTagTest.cpp`. These are useful as a future
fixture inventory for eMule BB protocol parser regression tests, especially:

- Kad tag-list packets with UTF-8 filenames and mixed file metadata.
- Kad integer width coverage for `uint8`, `uint16`, `uint32`, and `uint64`
  little-endian encodings.
- Kad `BSOB`, hash, float, and blob handling.
- ED2K numeric and string tag-name blob cases.
- Kad/eD2K tag-name inventories that can become compact "known names parse"
  regression tables.

Current recommendation: if revisited, add low-risk native byte-vector tests
first. Avoid linking aMule's test harness or pulling broad production app
runtime into the native test executable.

## File-Format Tool Ideas

aMule includes a `fileview` utility under `analysis/amule/src/utils/fileview`
for read-only inspection of profile and persistence files. It covers:

- `preferences.dat`
- `preferencesKad.dat`
- `nodes.dat`
- `server.met`
- `clients.met`
- `known.met`
- `.part.met`
- `canceled.met`
- `emfriends.met`
- `statistics.dat`
- Kad index files such as `load_index.dat`, `key_index.dat`, and
  `src_index.dat`

This has little immediate implementation value because eMule BB already has
some persistence seams for `server.met`, `nodes.dat`, and `preferencesKad.dat`.
The useful future direction is to mine the file-shape knowledge for richer
offline validators or diagnostics, not to port the utility directly.

Potential future slices:

- Expand `preferencesKad.dat` validation from length-only to parsed IP/client ID
  diagnostics.
- Add a lightweight `preferences.dat` identity/shape validator.
- Enrich `nodes.dat` inspection with version, bootstrap, endpoint, and
  verification diagnostics.
- Add `known.met` and `.part.met` summary validators once tag-vector coverage is
  stronger.
- Reuse tag/name/type display tables for clearer diagnostic output.

## Watch Guidance

Re-check aMule periodically when it changes in areas that overlap eMule BB:

- Kad/eD2K protocol serialization tests
- profile/persistence file decoders
- corruption recovery behavior for `.met` files
- parser hardening around malformed tags or truncated payloads
- compatibility fixes called out in aMule release notes or changelog

Keep this as a watchlist until a specific item has a concrete eMule BB bug,
test gap, support-diagnostic need, or compatibility risk attached to it.
