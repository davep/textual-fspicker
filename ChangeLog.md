# ChangeLog

## Unreleased

**Released: 2025-08-26**

- Dropped support for Python 3.9.

## v0.6.0

**Released: 2025-08-26**

- Migrated from `rye` to `uv` for development management.
  ([#71](https://github.com/davep/textual-fspicker/pull/71))
- Added Python 3.14 as a tested/supported Python version.
  ([#72](https://github.com/davep/textual-fspicker/pull/72))
- Added `textual_fspicker.Icons` so that the user of the library can set
  their own icons that are displayed next to directory entries.
  ([#74](https://github.com/davep/textual-fspicker/pull/74))
- Added support for suggested completions when typing paths into the
  `FileOpen` and `FileSave` dialogs.
  ([#76](https://github.com/davep/textual-fspicker/pull/76))

## v0.5.0

**Released: 2025-08-11**

- Added current directory location display to the `FileOpen` and `FileSave`
  dialogs. ([#60](https://github.com/davep/textual-fspicker/pull/60))
- A double-click is now needed to open a directory when selecting with the
  mouse, by default (with the option to turn off).
  ([thanks to marph91](https://github.com/davep/textual-fspicker/pull/54))

## v0.4.3

**Released: 2025-08-08**

- Fixed crash with Python 3.9 (redux).
  ([#55](https://github.com/davep/textual-fspicker/issues/55))

## v0.4.2

**Released: 2025-08-07**

- Fixed crash with Python 3.9.
  ([#55](https://github.com/davep/textual-fspicker/issues/55))

## v0.4.1

**Released: 2025-02-28**

- Added stand-alone documentation.
  ([#31](https://github.com/davep/textual-fspicker/pull/31))

## v0.4.0

**Released: 2025-02-20**

- Added the ability to configure any button label of any dialog.
  ([#26](https://github.com/davep/textual-fspicker/pull/26))
- All hard-coded error messages destined for the error label of the dialogs
  are now soft-coded in class variables to allow easy overriding by the
  developer. ([#28](https://github.com/davep/textual-fspicker/pull/28))

## v0.3.0

**Released: 2025-02-19**

- Handled Windows throwing an `OSError` when `mtime` can't be adequately
  worked out. ([#24](https://github.com/davep/textual-fspicker/pull/24) for
  [6#issuecomment-2669234263](https://github.com/davep/textual-fspicker/issues/6#issuecomment-2669234263))

## v0.2.0

**Released: 2025-01-30**

- Added `default_file` to `FileOpen` and `FileSave`.
  ([#18](https://github.com/davep/textual-fspicker/pull/18))
- Dropped support for Python 3.8.
  ([#19](https://github.com/davep/textual-fspicker/pull/19))

## v0.1.1

**Released: 2025-01-16**

- Fixed a backward-compatibility issue on Windows ([thanks to
  SoulMelody](https://github.com/davep/textual-fspicker/pull/14)).
- Fixed the cosmetics of the directory label in `SelectDirectory`.
  ([#15](https://github.com/davep/textual-fspicker/pull/15))

## v0.1.0

**Released: 2025-01-15**

- Added <kbd>backspace</kbd> as a navigation shortcut for "change to parent"
  ([thanks to ihabunek](https://github.com/davep/textual-fspicker/pull/7)).
- Added support for drive selection on Microsoft Windows
  ([thanks to davidfokkema](https://github.com/davep/textual-fspicker/pull/9)),

## v0.0.10

**Released: 2023-08-07**

- Fixed a breaking change with threaded workers with newer versions of
  Textual ([thanks to
  adeemm](https://github.com/davep/textual-fspicker/pull/3)).
- Fixed the look and size of the main navigation control in all dialogs,
  taking into account recent default styling changes in Textual.

## v0.0.9

**Released: 2023-06-04**

- Changed the underlying type of the dialog screens to be `Path | None`
  rather than `Path`.
- Changed the way the dialogs cancel. Instead of dismissing with no result,
  a result is now set to `None`. That is, if something is selected then a
  `Path` will be the result, if the user cancels then `None` is the result.
- Fixed `SelectDirectory` not showing the current selection on startup.

## v0.0.8

**Released: 2023-06-04**

- Fixed the initial filter in the `FileOpen` and `FileSave` dialogs not
  applying on startup.

## v0.0.7

**Released: 2023-06-03**

- Updated how the messages work to take into account changes around
  `control`.
- Updated dependency information making this require a Textual version of at
  least 0.27.0.

## v0.0.6

**Released: 2023-06-03**

- Add support for setting an alternative to `Path` as the core of path
  handling in the library.
- Fixed a problem where text was unreadable when a Textual application was
  in light mode.

## v0.0.5

**Released: 2023-05-23**

- Added `FileSave`.

## v0.0.4

**Released: 2023-05-22**

- Moved much of the code in `FileOpen` into `FileSystemPickerScreen`,
  providing a common base class for other dialogs.
- Added `SelectDirectory`.

## v0.0.3

**Released: 2023-05-21**

- Added the ability to style the content of the `DirectoryNaviation` widget.
- Added support for file filters to `FileOpen`.

## v0.0.2

**Released: 2023-05-19**

- Typing a directory into the input control of the `FileOpen` dialog now
  changes the directory in the navigator and stays within the dialog.
- Sprinkled some `PermissionError`-handling code around the `FileOpen`
  dialog, so that if the user tries to go where they don't belong, the
  application won't blow up.
- Made it easier for the user of the library to restyle the look of the
  `FileOpen` dialog (documentation will follow for that at some point, but
  reading of the `DEFAULT_CSS` will give some ideas).
- Simplified the internals of prompt creation in the `DirectoryNaviation`
  widget, with a view to setting about improving what's shown and adding
  configurable styling pretty soon.

## v0.0.1

**Released: 2023-05-18**

Initial release.

[//]: # (ChangeLog.md ends here)
