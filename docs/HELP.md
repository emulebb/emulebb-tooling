# eMuleBB Help

This is the shortest path into the eMuleBB manuals. It is written for users who
already understand eMule-style clients and want exact operating guidance.

## I Want To...

| Task | Start Here |
|---|---|
| Understand what eMuleBB is and why it exists | [Product Guide](reference/GUIDE-EMULEBB.md) |
| Learn eMule from zero before tuning a serious profile | [Power User Manual](reference/GUIDE-POWER-USERS.md) |
| Set up a fresh profile | [Setup Guide](reference/GUIDE-SETUP.md#new-profile-recipe) |
| Use an existing eMule profile | [Setup Guide](reference/GUIDE-SETUP.md#existing-profile-recipe) |
| Launch with an isolated `-c` profile | [Setup Guide](reference/GUIDE-SETUP.md#isolated-profile-recipe) |
| Fix Low ID, Kad firewalled, or bind problems | [Network Guide](reference/GUIDE-NETWORK.md) |
| Improve search and download workflow | [Downloads And Search](reference/GUIDE-DOWNLOADS-SEARCH.md) |
| Share a large library deliberately | [Sharing Guide](reference/GUIDE-SHARING.md) |
| Wire eMuleBB into aMuTorrent or Arr apps | [Stack Integration Guide](reference/GUIDE-STACK-INTEGRATIONS.md) |
| Make the first REST API call | [REST Quickstart](rest/REST-API-QUICKSTART.md) |
| Diagnose a crash, hang, slow startup, or REST failure | [Troubleshooting Guide](reference/GUIDE-TROUBLESHOOTING.md) |
| Translate user-facing docs or homepage text | [Translations And Localization](reference/GUIDE-TRANSLATIONS.md) |

## Safe First Steps

1. Keep the application directory separate from the profile directory.
2. Back up an existing profile before first launch.
3. Use `emulebb.exe -c <profile-dir>` when testing a package or copied profile.
4. Confirm temp, incoming, and shared directories before starting downloads.
5. Verify the desktop app before enabling REST, aMuTorrent, Radarr, or Sonarr.

## Power User Notes

eMuleBB keeps the classic eMule desktop workflow while adding maintained
broadband defaults, diagnostics, large-library handling, and trusted local
controller surfaces.

The desktop app owns live state. Controllers and adapters should read or mutate
that state through documented APIs; they do not replace the native client.
