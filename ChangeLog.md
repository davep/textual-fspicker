# ChangeLog

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
