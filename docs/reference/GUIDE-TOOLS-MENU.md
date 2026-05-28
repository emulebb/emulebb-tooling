# eMuleBB Tools Menu Guide

The Tools menu is the power-user control surface for fast navigation,
maintenance, diagnostics, and direct config-file access.

## Tools Organization

The expanded main-shell Tools popup is grouped by task. The compact tray menu
keeps its shorter ordering so tray use remains stable. The floating `Alt+U`
Hotmenu is a separate quick-navigation surface documented below.

- Session: connect, disconnect, pane jumps, tray, and exit
- Transfers and speed: transfer navigation, upload/download limit presets, and
  refresh interval controls
- Files and categories: common folders, category management, and category config
- Network and Updates: IP filter, direct download, server.met update, port test,
  firewall repair, geolocation update, and Arr/Prowlarr registration helpers
- Maintenance: reload filters, rescan shared files, save preferences, enable
  Windows long paths, and add Microsoft Defender exclusions
- Diagnostics: open logs, copy diagnostic snapshots, and capture dumps
- Display and views: toolbar skins, text-label display settings, toolbar
  customization, display reset, and table view presets
- Edit Config Files: open editable profile files in the configured text editor
- Links and legacy: web links plus the frozen Scheduler and first-run wizard
  entry points while those surfaces still exist

The top-level labels are built from existing localized resources where
possible, so the structure can improve without creating a new translation pass
for menu-only wording.

## Alt+U Hotmenu

`Alt+U` opens the floating Hotmenu. It is intentionally flatter than Tools:

- connection state: connect, cancel connection, or disconnect
- main navigation: Kad, Servers, Transfers, Search, Shared Files, Messages,
  Statistics, Options, Help
- fast actions: paste eD2K links and open IP Filter
- folders: Incoming, Config, Logs
- links: eMuleBB web links and configured web-service links
- legacy/frozen entries: IRC, Scheduler, first-run wizard
- exit

The tray right-click menu is different from the Hotmenu. It is built from the
Tools path with tray-specific Restore/Minimize/connect entries and preserves
the compact tray ordering.

## Session

Session actions mirror high-frequency toolbar behavior:

- connect, cancel connection, or disconnect depending on current state
- jump to Server, Transfers, Search, Shared Files, Messages, IRC, Statistics,
  or Options
- minimize to tray
- exit through the normal shutdown path

Use these actions when running from tray or when the toolbar is hidden or not
focused.

## Transfers And Speed

The Transfers and speed group contains transfer pane navigation, speed quick
actions, and refresh interval controls.

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
repair, geolocation database update, and controller registration helpers. These
actions affect reachability, bootstrap, network metadata, or local automation
setup.

The registration helpers launch packaged scripts for current Arr-family
integration:

- `Register eMuleBB in Prowlarr...` launches the Prowlarr Generic Torznab
  setup helper with the current local eMuleBB base URL and API key.
- `Register Radarr/Sonarr integration...` launches the combined Arr helper
  with the current local eMuleBB base URL and API key.

The helpers still ask for Prowlarr, Radarr, and Sonarr URLs/API keys at runtime.
They do not turn those external controller credentials into eMuleBB
preferences. The future guided in-app setup work is tracked separately; these
menu items are the current script-launcher surface.

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

View presets live under the Display and views group in the expanded Tools
popup. The compact tray menu keeps the older flat View Presets submenu.

View presets reset table layouts:

- Stock: conservative, classic columns
- Extended: power-user columns without everything visible
- Full: all reviewed columns visible

In the expanded Tools popup each preset has its own submenu with preserve-widths
and reset-widths commands. Use reset widths when old profiles have cramped or
broken column layouts.

## Display

Display actions also live under Display and views:

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

## Links And Legacy

The expanded Tools popup moves web links, Scheduler, and the first-run wizard
under one low-priority group. Scheduler and the first-run wizard are frozen
surfaces tracked for deletion through `REF-025`; this grouping makes that
boundary visible without changing their current commands. The compact tray menu
keeps the previous Links and Scheduler placement.

## Keyboard Notes

`Alt+U` opens the floating Hotmenu. `Alt+W` opens the Tools popup. `Alt+T`
belongs to Transfers. Keyboard shortcut details are maintained in
[Keyboard Shortcuts](KEYBOARD-SHORTCUTS.md).
