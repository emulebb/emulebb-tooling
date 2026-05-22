# IP Filter Guide

eMule BB uses `ipfilter.dat` to reject peers, sources, Kad contacts, and
optionally servers whose IP ranges match loaded filter rules. IP filtering is a
maintenance and abuse-reduction aid. It is not a privacy substitute for correct
network binding, firewall rules, or VPN operation.

## Practical Model

IP filtering has three separate pieces:

- the local filter file, `config\ipfilter.dat`
- the enabled/disabled state and filter level in preferences
- the update URL and URL history used by the Security page

The file may exist while filtering is disabled. In that state the rules are
available for later reload, but they do not block peers until filtering is
enabled again.

## Where Settings Are Stored

The active update URL is stored in the normal preferences file:

- file: `config\preferences.ini`
- section: `[eMule]`
- key: `IPFilterUpdateUrl`

The Security page dropdown history is separate:

- file: `config\AC_IPFilterUpdateURLs.dat`
- format: UTF-16 text with one URL per line

When `AC_IPFilterUpdateURLs.dat` is missing or has no usable entries, eMule BB
seeds it with built-in suggestions. Existing non-empty user history is left
unchanged.

## Seeded URL Suggestions

The seeded dropdown suggestions are:

1. `https://upd.emule-security.org/ipfilter.zip`
2. `https://emuling.gitlab.io/ipfilter.zip`
3. `https://github.com/DavidMoore/ipfilter/releases/download/lists/ipfilter.zip`
4. `https://raw.githubusercontent.com/Naunter/BT_BlockLists/master/bt_blocklists.gz`

The HTTPS eMule-Security URL is the default active URL for new profiles. The
other entries are suggestions for users who want a fallback or a torrent-style
PeerGuardian blocklist source.

Use trusted providers only. A bad or over-broad blocklist can make searches,
Kad contacts, or server connections look broken.

## Supported Download Formats

The IP filter updater accepts:

- ZIP archives containing `ipfilter.dat`, `guarding.p2p`, or `guardian.p2p`
- GZip-compressed filter files
- RAR archives when RAR support is available
- plain `ipfilter.dat` style text
- PeerGuardian-style text
- PeerGuardian binary files

After a successful update, eMule BB promotes the downloaded filter into
`config\ipfilter.dat`, reloads the running filter table, and shows the loaded
rule count in `Preferences > Security > IP Filter`.

## Enable Filtering Recipe

1. Open `Preferences > Security`.
2. Enable the IP Filter checkbox.
3. Confirm the filter level is appropriate for the selected list.
4. Load or reload the filter.
5. Confirm the stats line shows filtering enabled and a non-zero rule count.
6. Watch logs after the next connect/search cycle for unexpected blocking.

If the rule count is zero, filtering is effectively inactive even if the
checkbox is enabled.

## Update From A URL Recipe

1. Open `Preferences > Security`.
2. Choose or enter a trusted filter URL.
3. Use the load/update action.
4. Wait for the download and parse step to finish.
5. Confirm the loaded rule count changed as expected.
6. If the update fails, keep the previous known-good `ipfilter.dat` until the
   provider or network issue is understood.

The updater should not leave the profile unprotected just because a remote URL
fails. Treat download failures as maintenance events, not as proof that local
filtering is disabled.

## Manual Edit Recipe

Use manual edits when you need a local exception or a local test rule:

1. Close or pause any broad troubleshooting changes.
2. Back up `config\ipfilter.dat`.
3. Edit the file with a text editor that preserves the file format.
4. Save the file.
5. Use **Reload** from `Preferences > Security`.
6. Confirm the rule count and filter level.
7. Re-test the affected peer, search, Kad, or server behavior.

If a manual edit makes networking worse, restore the backup and reload again.

## Filter Level

The filter level is the minimum level used when filtering is enabled. Lower
values are more aggressive because they accept more rules from typical
PeerGuardian-style lists. Higher values are less aggressive.

Use the provider's guidance when a list documents its level semantics. Without
provider guidance, avoid changing the level during unrelated troubleshooting;
otherwise it becomes hard to tell whether the list or the level caused a
behavior change.

## Troubleshooting

IP filter ineffective:

1. Confirm filtering is enabled.
2. Confirm `config\ipfilter.dat` exists.
3. Confirm the loaded rule count is not zero.
4. Confirm the filter level is not excluding the expected rules.
5. Use **Reload** after manual edits.
6. Check whether the IP is covered by the loaded list.

Unexpected connection loss:

1. Disable filtering temporarily.
2. Retry the same server, peer, or Kad action.
3. If behavior changes, inspect the matching rule.
4. Restore a previous known-good list or raise the filter level.
5. Re-enable filtering after the list is corrected.

Update failure:

1. Verify the URL in the dropdown or active field.
2. Try a browser or another network path to check provider availability.
3. Check whether the remote archive contains a supported file.
4. Keep the previous local filter until a valid replacement is loaded.

## Boundaries

IP filtering does not hide the machine's traffic, replace firewall policy, or
guarantee safe peer selection. Use it alongside:

- correct bind/interface configuration
- Windows Firewall and router policy
- trusted server and Kad bootstrap sources
- VPN/provider policy when required
- normal caution with search results and downloaded files

Proxy support is a frozen legacy surface and should not be used as the privacy
answer for IP filtering questions. See
[Frozen Surfaces](../active/FROZEN-SURFACES.md).
