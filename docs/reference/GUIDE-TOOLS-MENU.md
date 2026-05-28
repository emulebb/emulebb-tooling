# eMuleBB Tools Menu Guide

The Tools menu is the power-user control surface for fast navigation,
maintenance, diagnostics, and direct config-file access.

## Organization

Tools is grouped by task:

- Session: connect, disconnect, pane jumps, tray, and exit
- Speed Quick Actions: upload, download, and combined throttle presets
- Folders: open important directories
- Categories: manage categories and edit category config
- Edit Config Files: open editable profile files in the configured text editor
- Network and Updates: IP filter, direct download, server.met update, port test,
  firewall repair, geolocation update, and Arr/Prowlarr registration helpers
- Maintenance: reload filters, rescan shared files, save preferences, enable
  Windows long paths, and add Microsoft Defender exclusions
- View Presets: apply stock, extended, or full table layouts
- Diagnostics: open logs, copy diagnostic snapshots, and capture dumps

The goal is fast access without forcing users through Preferences for every
operational action.

## Session

Session actions mirror high-frequency toolbar behavior:

- connect, cancel connection, or disconnect depending on current state
- jump to Server, Transfers, Search, Shared Files, Messages, IRC, Statistics,
  or Options
- minimize to tray
- exit through the normal shutdown path

Use these actions when running from tray or when the toolbar is hidden or not
focused.

## Speed Quick Actions

Speed quick actions change limits for upload only, download only, or both
directions together. Percentage actions apply to the current configured finite
limit and are persisted through the same preference paths as normal limit
changes.

## Folders

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

View presets reset table layouts:

- Stock: conservative, classic columns
- Extended: power-user columns without everything visible
- Full: all reviewed columns visible

Each preset has variants to preserve widths or reset widths. Use reset widths
when old profiles have cramped or broken column layouts.

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

## Keyboard Notes

`Alt+W` opens the Tools popup. `Alt+T` belongs to Transfers. Keyboard shortcut
details are maintained in [Keyboard Shortcuts](KEYBOARD-SHORTCUTS.md).
