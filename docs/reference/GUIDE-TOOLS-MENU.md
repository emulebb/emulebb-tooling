# eMuleBB Tools Menu Guide

The Tools menu is the power-user control surface for fast navigation,
maintenance, diagnostics, and direct config-file access.

## Tools Organization

The expanded main-shell Tools popup is grouped by task. Both the expanded Tools
popup and compact tray Tools path must stay at a maximum of one submenu level:
top-level groups may open one command list, but those command lists must not
open another nested submenu. The floating `Alt+U` Hotmenu is a separate
quick-navigation surface documented below.

- Session: connect, disconnect, pane jumps, tray, and exit
- Transfers: transfer navigation
- Speed Quick Actions: upload/download/both limit presets
- Refresh interval: desktop UI refresh cadence controls
- Files and categories: common folders, category management, and category config
- Network and Updates: IP filter, direct download, server.met update, port test,
  firewall repair, and geolocation update
- Controllers and Integrations: Prowlarr, Radarr, and Sonarr setup helpers
- Maintenance: reload filters, rescan shared files, save preferences, enable
  Windows long paths, and add Microsoft Defender exclusions
- Diagnostics: open logs, copy diagnostic snapshots, and capture dumps
- Display and views: toolbar skins, text-label display settings, toolbar
  customization, display reset, and table view presets
- Edit Config Files: open editable profile files in the configured text editor
- Links: eMuleBB web links and configured web-service entries

The top-level labels are built from existing localized resources where
possible, so the structure can improve without creating a new translation pass
for menu-only wording.

Menu art follows the same conservative rule: command icons should look native
to the classic eMule/early-2000s Windows shell, use transparent ICO alpha/masks,
and avoid opaque dark backgrounds that turn menu glyphs into black tiles.

## Alt+U Hotmenu

`Alt+U` opens the floating Hotmenu. It is intentionally flatter than Tools:

- connection state: connect, cancel connection, or disconnect
- main navigation: Kad, Servers, Transfers, Search, Shared Files, Messages,
  Statistics, Options, Help
- fast actions: paste eD2K links and open IP Filter
- folders: Incoming, Config, Logs
- links: eMuleBB web links and configured web-service links
- legacy/frozen entries: IRC
- exit

The tray right-click menu is different from the Hotmenu. It is built from the
Tools path with tray-specific Restore/Minimize/connect entries and keeps the
compact tray ordering.

## Session

Session actions mirror high-frequency toolbar behavior:

- connect, cancel connection, or disconnect depending on current state
- jump to Server, Transfers, Search, Shared Files, Messages, IRC, Statistics,
  or Options
- minimize to tray
- exit through the normal shutdown path

Use these actions when running from tray or when the toolbar is hidden or not
focused.

## Transfers, Speed, And Refresh

The expanded Tools popup exposes transfer pane navigation, speed quick actions,
and refresh interval controls as separate top-level groups. The compact tray
menu keeps the same one-level command lists in its shorter ordering.

Speed quick actions change limits for upload only, download only, or both
directions together. Percentage actions apply to the current configured finite
limit and are persisted through the same preference paths as normal limit
changes.

## Files And Categories

The Files and categories group contains folder shortcuts and category actions.

Folder actions open common locations:

- Incoming
- Temp
- Config
- Logs
- WebServer assets
- Skins
- Toolbar assets
- executable directory

Use these instead of manually browsing through profile paths.

Category actions open the category manager and `Category.ini` editor.

## Edit Config Files

The editor actions open text-backed config files directly:

- `preferences.ini`
- `ipfilter.dat`
- fake-file filter rules
- `shareignore.dat`
- `addresses.dat`
- `staticservers.dat`
- `webservices.dat`
- shared-directory files
- `Category.ini`
- `Notifier.ini`
- file comments
- `statistics.ini`

Edits are not all applied live. Use the matching reload action where one exists,
or restart when editing persistent startup, bind, listener, or layout settings.

## Network And Updates

Network actions include the IP filter dialog, direct ED2K download dialog,
server.met update from `addresses.dat`, open ports test, Windows Firewall
repair, and geolocation database update. These actions affect reachability,
bootstrap, and network metadata.

## Controllers And Integrations

The registration helpers launch packaged scripts for current Arr-family
integration:

- `Register eMuleBB in Prowlarr...` launches the Prowlarr Generic Torznab
  setup helper with the current local eMuleBB base URL and API key.
- `Register Radarr integration...` launches the shared Arr helper with
  `-Target Radarr`.
- `Register Sonarr integration...` launches the shared Arr helper with
  `-Target Sonarr`.

The helpers still ask for Prowlarr, Radarr, and Sonarr URLs/API keys at runtime.
They do not turn those external controller credentials into eMuleBB
preferences. The future guided in-app setup work is tracked separately; these
menu items are the current script-launcher surface.

The menu uses eMuleBB-owned classic ICOs for these actions rather than upstream
Radarr, Sonarr, or Prowlarr logos, so the desktop package avoids third-party
logo and trademark attribution requirements.

## Maintenance

Maintenance actions are explicit operational refreshes:

- reload `ipfilter.dat`
- reload fake-file filter rules
- reload `shareignore.dat`
- rescan shared files
- save preferences now
- enable Windows long paths through the packaged elevated action
- add Microsoft Defender exclusions for active Incoming, Temp, and category
  folders

Prefer these over restarting when the action has an explicit reload path. Use
`Save Preferences Now` before risky maintenance when you need current UI state
persisted immediately.

## View Presets

View presets are direct commands under the Display and views group in the
expanded Tools popup. The compact tray menu keeps a one-level View Presets
submenu.

View presets reset table layouts:

- Stock: conservative, classic columns
- Extended: power-user columns without everything visible
- Full: all reviewed columns visible

Each preset exposes preserve-widths and reset-widths commands directly. Use
reset widths when old profiles have cramped or broken column layouts.

## Display

Display actions also live directly under Display and views:

- toolbar bitmap skins
- toolbar skin profiles
- toolbar text-label display modes
- display reset
- toolbar customization

These actions affect main-shell presentation only. They do not change network,
transfer, or persistence behavior beyond the existing UI preference writes.

## Diagnostics

Diagnostics actions include:

- open normal and verbose logs
- copy diagnostic snapshot JSON
- copy redacted diagnostic snapshot JSON
- capture mini dump
- capture full memory dump

Use redacted JSON for public or routine support unless exact addresses, paths,
or command lines are required for private diagnosis. See
[Diagnostics Guide](GUIDE-DIAGNOSTICS.md) for privacy boundaries and dump use.

## Links

The expanded Tools popup and compact tray path expose eMuleBB-owned web links
under one Links group. The fixed entries point to the homepage, online help,
GitHub Releases, FAQ, setup guide, network/VPN binding guide, sharing guide,
downloads and search guide, Tools menu guide, controllers and REST guide, and
troubleshooting guide.

User-configured general actions from `webservices.dat` still appear in the
same group after the fixed documentation links. Edit Web Services opens that
file in the configured text editor.

## Keyboard Notes

`Alt+U` opens the floating Hotmenu. `Alt+W` opens the Tools popup. `Alt+T`
belongs to Transfers. Keyboard shortcut details are maintained in
[Keyboard Shortcuts](KEYBOARD-SHORTCUTS.md).
