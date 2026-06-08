# Keyboard Shortcuts

EMULEBB_KEYBOARD_SHORTCUT: this document records deliberate app-level keyboard
ownership for the native MFC shell. Update it with code changes that add,
remove, or repurpose shortcuts.

## Reserved App Shortcuts

| Shortcut | Owner | Behavior |
|----------|-------|----------|
| `Alt+C` | main shell | Connects, cancels a connection attempt, or disconnects. |
| `Alt+K` | main shell | Opens Kad. |
| `Alt+V` | main shell | Opens Servers. |
| `Alt+T` | main shell | Opens Transfers. |
| `Alt+S` | main shell | Opens Search. |
| `Alt+F` | main shell | Opens Shared Files. |
| `Alt+M` | main shell | Opens Messages. |
| `Alt+I` | main shell | Opens IRC. |
| `Alt+A` | main shell | Opens Statistics. |
| `Alt+O` | main shell | Opens Options. |
| `Alt+H` | main shell | Opens Help for the active pane. |
| `Alt+W` | main shell | Opens the Tools popup. |
| `Alt+X` | main shell | Cleanly exits through `CemuleDlg::OnClose()` and respects Prompt on exit. |
| `Alt+U` | main shell | Opens the floating Hotmenu quick-navigation menu. |
| `Alt+1` ... `Alt+9` | main shell | Opens toolbar panes 1 through 9 in visible toolbar order. |
| `Alt+0` | main shell | Opens the Options toolbar pane. |
| `Ctrl+Tab` / `Ctrl+Shift+Tab` | main shell | Cycles primary toolbar panes. |

## Transfers Navigation Shortcuts

These shortcuts are local to the Transfers pane.

| Shortcut | Behavior |
|----------|----------|
| `Ctrl+0` | Switches the Downloads category tab to All. |
| `Ctrl+1` ... `Ctrl+9` | Switches to Downloads category tabs 1 through 9 when present. |
| `Ctrl+D` | Switches to the Downloads list. |
| `Ctrl+Shift+D` | Switches to Downloading Clients. |
| `Ctrl+U` | Switches the Transfers list to Uploading. |
| `Ctrl+Q` | Switches the Transfers list to Queue. |
| `Ctrl+K` | Switches the Transfers list to Known Clients. |
| `F5` | Flushes the current Transfers view refresh. |
| `Numpad +` / `Alt+Right` | Expands the focused download row's source list. |
| `Numpad -` / `Alt+Left` | Collapses the focused download row's source list. |

In split view, the list shortcuts switch the lower Transfers pane. In a
single-list view, they switch the primary full list. Queue and Known Clients
respect their existing disabled preferences.

## Transfer Client List Shortcuts

These shortcuts apply to Uploading, Queue, Known Clients, and Downloading
Clients.

| Shortcut | Behavior |
|----------|----------|
| `Ctrl+I` | Opens details for the selected clients. |
| `Alt+Enter` | Opens details for the selected clients. |

## Searchable List Shortcuts

These shortcuts are inherited by searchable list controls such as client,
queue, upload, download, server, search-results, and shared-files lists.

| Shortcut | Behavior |
|----------|----------|
| `Ctrl+F` | Starts list find. |
| `F3` | Finds the next match after list find is active. |
| `Shift+F3` | Finds the previous match after list find is active. |
| `Esc` | Clears the active list find text when one is set. |
| `Ctrl+A` | Selects all rows in the focused list. |

## File-Like List Sort Shortcuts

Downloads, Search Results, and Shared Files support Total Commander-style sort
shortcuts when the relevant list has focus.

| Shortcut | Behavior |
|----------|----------|
| `Ctrl+F3` | Sorts by name. |
| `Ctrl+F4` | Sorts by type where the list has a type column. |
| `Ctrl+F5` | Sorts by date/time where the list has a date/time column. |
| `Ctrl+F6` | Sorts by size. |
| `Ctrl+F7` | Sorts by status or availability where supported. |
| `Ctrl+F8` | Sorts by progress or complete-source availability where supported. |
| `Ctrl+F9` | Sorts by sources, or by size in Search Results. |
| `Ctrl+F10` | Sorts by speed where supported. |
| `Ctrl+F11` | Sorts by priority where supported. |
| `Ctrl+F12` | Sorts by category where supported. |

Repeating the same shortcut toggles ascending and descending order through the
same path as clicking the column header. In Search, `Ctrl+F4` closes the
selected search-results tab instead of sorting by type. If a list does not have the requested
semantic column, the shortcut is consumed with a native beep and no fallback
sort is guessed. If the matching column is currently hidden, the shortcut is
also consumed with a native beep instead of changing the visible list order
through a hidden sort key. Downloads currently has no type column, and Search
Results currently has no date/time, speed, priority, or category column.

## Downloads List Shortcuts

These shortcuts are local to the Downloads file list. They operate on the
selected downloads and do not become global app accelerators.

| Shortcut | Behavior |
|----------|----------|
| `Ctrl+P` | Pauses selected downloads that can be paused. |
| `Ctrl+S` | Resumes selected downloads that can be resumed. |
| `Ctrl+T` | Stops selected downloads that can be stopped. |
| `Ctrl+Shift+P` | Pauses all pausable downloads in the current category. |
| `Ctrl+Shift+S` | Resumes all resumable downloads in the current category. |
| `Ctrl+Shift+T` | Stops all stoppable downloads in the current category. |
| `Ctrl+R` | Clears completed downloads from the current category. |
| `Ctrl++` / `Ctrl+-` | Raises or lowers selected download priority one manual step. |
| `Ctrl+Shift++` / `Ctrl+Shift+-` | Sets selected download priority to High or Low. |
| `Ctrl+M` | Opens the category picker for selected downloads. |
| `Ctrl+O` | Opens the selected completed download when it can be opened. |
| `Ctrl+Shift+O` | Opens the selected download's folder. |
| `Ctrl+I` | Opens details for the selected download rows. |
| `Ctrl+L` | Copies selected download ED2K links. |
| `Ctrl+Shift+C` | Copies selected download file summaries. |
| `Delete` / `Canc` | Cancels selected active downloads after confirmation; removes completed downloads from the visible list. |
| `Shift+Delete` / `Shift+Canc` | Cancels selected downloads without confirmation, using the same completed-file path as the Cancel command. |
| `F2` | Renames one selected incomplete download; `Ctrl+F2` runs filename cleanup. |
| `Enter` | Opens the selected completed download when it can be opened. |
| `Alt+Enter` | Opens details for the selected download rows. |
| `Ctrl+C` | Copies selected download ED2K links. |
| `Ctrl+V` | Pastes a direct ED2K download link when available. |
| `Shift+F10` | Opens the Downloads context menu for the focused row. |

## Search Results List Shortcuts

These shortcuts are local to Search Results.

| Shortcut | Behavior |
|----------|----------|
| `Ctrl+D` | Downloads selected search results. |
| `Ctrl+Shift+D` | Downloads selected search results paused. |
| `Ctrl+I` | Opens details for selected results. |
| `Insert` | Downloads selected search results and moves selection to the next visible result. |
| `Enter` | Downloads selected search results. |
| `Shift+Enter` | Downloads selected search results paused. |
| `Ctrl+Enter` | Opens details for selected results. |
| `Alt+Enter` | Opens details for selected results. |
| `Ctrl+L` / `Ctrl+C` | Copies selected result ED2K links. |
| `Ctrl+Shift+C` | Copies selected result summaries. |
| `Ctrl+F` | Starts list find. |
| `Ctrl+PageUp` / `Ctrl+PageDown` | Switches to the previous or next search-results tab. |
| `Ctrl+W` | Closes the selected search-results tab. |
| `Ctrl+F4` | Closes the selected search-results tab. |
| `Numpad +` / `Alt+Right` | Expands the focused grouped result row. |
| `Numpad -` / `Alt+Left` | Collapses the focused grouped result row. |

## Shared Files Shortcuts

These shortcuts are local to the Shared Files list.

| Shortcut | Behavior |
|----------|----------|
| `Ctrl+O` | Opens the selected shared file. |
| `Ctrl+Shift+O` | Opens the selected shared file's folder. |
| `Ctrl+I` | Opens details for selected shared files. |
| `Ctrl+L` / `Ctrl+C` | Copies selected shared-file ED2K links. |
| `Ctrl+Shift+C` | Copies selected shared-file summaries. |
| `Ctrl+F` | Starts list find. |
| `F5` | Reloads the shared-files list. |
| `F2` | Renames the selected shared file through the existing rename action. |
| `Delete` | Runs the existing Delete action for selected shared files. |
| `Space` | Toggles selected shared-file checkboxes when checkbox mode is enabled. |

## Shared Directories Shortcuts

These shortcuts are local to the Shared Directories tree.

| Shortcut | Behavior |
|----------|----------|
| `Ctrl+Shift+O` | Opens the selected directory. |

Shared Directories intentionally keeps keyboard ownership tree-native. File
details and ED2K copy shortcuts are handled by the Shared Files list, where the
file selection is visible.

## Legacy Local Shortcuts

These shortcuts are inherited from existing local controls. They stay local to
their pane or dialog and do not become global app accelerators.

| Context | Shortcut | Behavior |
|---------|----------|----------|
| Category Manager | `Insert` | Adds a category. |
| Category Manager | `Enter` | Edits the selected category. |
| Category Manager | `Delete` | Removes the selected category. |
| Category Manager | `F5` | Refreshes the category list. |
| Category Manager | `Alt+Up` / `Alt+Down` | Moves the selected category up or down. |
| Friends list | `Insert` | Adds a friend. |
| Friends list | `Delete` | Removes the selected friend. |
| Server pane | `Enter` | Adds a server from the focused new-server field or updates from the focused server.met URL field. |
| Server pane | `Delete` | Removes the selected server.met URL history entry when the URL field's autocomplete list has focus. |
| Server pane | `Ctrl+Delete` / `Alt+Delete` | Clears the server.met URL history. |

## File Copy Menus

The Downloads, Search Results, and Shared Files context menus expose a Copy
submenu for power users. Direct shortcuts remain conservative:
`Ctrl+L` copies plain ED2K links and `Ctrl+Shift+C` copies the summary line
where summaries are supported.

Menu-only Copy actions include:

| Context | Additional Copy Fields |
|---------|------------------------|
| Downloads | size, status, progress, file path, folder path, plain ED2K, HTML ED2K, file summary |
| Search Results | size, type, plain ED2K, HTML ED2K, result summary |
| Shared Files | size, file path, folder path, plain ED2K, HTML ED2K, file summary |

## Reserved Main-Shell Mnemonics

These native Alt mnemonics are treated as main-shell toolbar or hotmenu
ownership and should not be reused by modeless child panes:

`Alt+C`, `Alt+K`, `Alt+V`, `Alt+T`, `Alt+S`, `Alt+F`, `Alt+M`, `Alt+I`,
`Alt+A`, `Alt+O`, `Alt+H`, `Alt+U`, `Alt+W`, `Alt+X`, `Alt+1` through
`Alt+9`, and `Alt+0`.

## Search Pane Mnemonics

When Search is the active main pane, the Search parameter bar owns:

| Shortcut | Behavior |
|----------|----------|
| `Alt+N` | Focuses the Name textbox. |
| `Alt+Y` | Focuses Type. |
| `Alt+D` | Focuses Method. |
| `Alt+G` | Activates Search Go. |
| `Alt+E` | Activates More. |
| `Alt+R` | Activates Reset. |
| `Alt+L` | Activates Cancel. |

## Search Pane Navigation

| Shortcut | Behavior |
|----------|----------|
| `F6` | Toggles focus between the Search Name textbox and the search results list. |
| `Tab` from the last enabled Search parameter control | Moves focus to the search results list. |
| `Shift+Tab` from the search results list | Moves focus back to the last enabled Search parameter control. |

## Mnemonic Policy

- EMULEBB_KEYBOARD_SHORTCUT: do not reassign `Alt+X`; it is the direct app-exit
  mnemonic.
- The old hidden hotmenu `Alt+X` button was retired; floating hotmenu ownership
  is now `Alt+U`.
- Main-shell pane shortcuts deliberately reuse the reviewed English toolbar
  mnemonics as app-level commands so they work consistently across languages.
  Localized `&` markers are not the authority for these main-shell shortcuts.
- Numeric main-shell shortcuts deliberately mirror visible toolbar order:
  `Alt+1` through `Alt+9` open Connect through Statistics and `Alt+0` opens
  Options.
- `Alt+T` belongs to Transfers, matching the community baseline English
  toolbar mnemonic. Tools uses `Alt+W` to avoid that collision, and the Tools
  popup title advertises that shortcut.
- Search-local mnemonics deliberately avoid the reserved main-shell letters.
- Shortcut reference stays in this document; do not duplicate it in a Tools
  menu dialog.
- Modal dialogs keep local keyboard behavior. The app-level shortcuts are for
  the main shell and its primary modeless UI.
- Default English resources define the app-level shortcut policy; localized
  `.rc` mnemonic markers must not override the reserved main-shell shortcuts.

## Manual Verification

- With Prompt on exit disabled, `Alt+X` should enter the normal shutdown
  progress path.
- With Prompt on exit enabled, `Alt+X` should show the existing confirmation
  before shutdown.
- `Alt+C`, `Alt+K`, `Alt+V`, `Alt+T`, `Alt+S`, `Alt+F`, `Alt+M`, `Alt+I`,
  `Alt+A`, `Alt+O`, and `Alt+H` should drive Connect, Kad, Servers, Transfers,
  Search, Shared Files, Messages, IRC, Statistics, Options, and Help in every
  active language.
- `Alt+U` should open the floating hotmenu.
- `Alt+W` should open the Tools popup, and the Tools popup title should show
  the `Alt+W` hint.
- `Alt+1` through `Alt+9` should open Connect, Kad, Servers, Transfers, Search,
  Shared Files, Messages, IRC, and Statistics; `Alt+0` should open Options.
- In Transfers, `Ctrl+0` should select the All category tab; `Ctrl+1` through
  `Ctrl+9` should select existing category tabs and beep for missing tabs.
- In Transfers, `Ctrl+U`, `Ctrl+Q`, and `Ctrl+K` should switch to Uploading,
  Queue, and Known Clients. In split view they should switch the lower pane;
  outside split view they should switch the primary list.
- In Transfers, `Ctrl+D` should focus or switch to Downloads, and
  `Ctrl+Shift+D` should switch to Downloading Clients.
- In Transfers, `F5` should flush the visible transfer-list refresh without
  changing selection.
- In Transfers, `Numpad +`, `Numpad -`, `Alt+Right`, and `Alt+Left` should
  expand and collapse the focused download row's source list without changing
  download state.
- In Uploading, Queue, Known Clients, and Downloading Clients, `Ctrl+I` and
  `Alt+Enter` should open client details.
- In Downloads, `Ctrl+Shift+P`, `Ctrl+Shift+S`, and `Ctrl+Shift+T` should act on
  the current transfer category, even when no row is selected.
- In Downloads, `Ctrl++`, `Ctrl+-`, `Ctrl+Shift++`, and `Ctrl+Shift+-` should
  update selected download priorities without changing unrelated rows.
- In Downloads, `Ctrl+R` should clear completed rows in the current category
  through the existing Clear Completed command.
- In Downloads, `Ctrl+F7` through `Ctrl+F12` should sort status, progress,
  sources, speed, priority, and category respectively.
- In Downloads, `Shift+F10` should open the same context menu as right-click,
  and `Ctrl+M` should open the category picker for selected download rows.
- In Search, `Alt+N` should focus the Name textbox without selecting existing
  text.
- In Search, `Alt+Y`, `Alt+D`, `Alt+G`, `Alt+E`, `Alt+R`, and `Alt+L` should
  drive Type, Method, Search Go, More, Reset, and Cancel through local native
  mnemonic behavior.
- In Search, `F6` should move focus between the Name textbox and the search
  results list.
- In Search, forward `Tab` from the last enabled parameter control should move
  to results, and `Shift+Tab` from results should return to the last enabled
  parameter control.
- In Search, `Ctrl+Tab` and `Ctrl+Shift+Tab` should cycle main toolbar panes,
  not search-results tabs.
- In Search Results, `Enter`, `Shift+Enter`, and `Ctrl+Enter` should download,
  download paused, and open details respectively.
- In Search Results, `Insert` should download selected results and advance the
  list selection to the next visible result.
- In Search Results, `Alt+Enter` should open details through the same path as
  `Ctrl+Enter`.
- In Search Results, `Ctrl+PageUp` and `Ctrl+PageDown` should switch result
  tabs, and both `Ctrl+W` and `Ctrl+F4` should close the selected result tab.
- In Search Results, `Ctrl+F7`, `Ctrl+F8`, and `Ctrl+F9` should sort
  availability, complete sources, and size respectively.
- In Search Results, both `Ctrl+L` and `Ctrl+C` should copy selected result
  ED2K links.
- In Search Results, `Numpad +`, `Numpad -`, `Alt+Right`, and `Alt+Left`
  should expand and collapse the focused grouped result row.
- In searchable lists, `Ctrl+F`, `F3`, and `Shift+F3` should start find and
  navigate matches without changing transfer state.
- In searchable lists, `Esc` should clear the active find text when one is set,
  and otherwise leave normal list behavior alone.
- In Shared Files, `F5` should reload the shared-files list through the same
  path as the existing reload button.
- In Shared Files, the context menu should show native hints for `F2` rename
  and `Delete`.
- In Shared Files, both `Ctrl+L` and `Ctrl+C` should copy selected shared-file
  ED2K links.
- In Shared Files, `Space` should toggle selected checkboxes only when checkbox
  mode is enabled.
- In Category Manager, `Insert`, `Enter`, `Delete`, `F5`, `Alt+Up`, and
  `Alt+Down` should drive their existing local category actions.
- In Friends, `Insert` and `Delete` should add and remove friends through the
  existing list commands.
- In Servers, `Enter` should submit the focused new-server or server.met URL
  field, while `Delete`, `Ctrl+Delete`, and `Alt+Delete` should affect only the
  server.met URL history when that local field has focus.
- Outside Search, `Alt+N` should not switch panes or steal focus.
- Preferences, About, and confirmation dialogs should retain their normal
  local keyboard handling.
