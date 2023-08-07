# ChangeLog

## v0.0.10

**Released: WiP**

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
