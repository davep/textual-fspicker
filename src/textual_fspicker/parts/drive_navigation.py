"""Provides a widget for drive navigation."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
import sys
from dataclasses import dataclass
from pathlib import Path

##############################################################################
# Import or provide a version of listdrives.
try:
    from os import listdrives  # type: ignore[attr-defined]
except ImportError:
    import string

    def listdrives() -> list[str]:
        """Return a list containing the names of drives in the system.

        A drive name typically looks like 'C:\\'. This is an implementation for
        Python versions before 3.12. It does _not_ list removable drives which
        have no media inserted.

        Returns:
            list[str]: The list of available drives.
        """
        return [
            f"{letter}:"
            for letter in string.ascii_uppercase
            if Path(f"{letter}:\\").exists()
        ]


##############################################################################
# Textual imports.
from textual import on
from textual.message import Message
from textual.reactive import var
from textual.widgets import OptionList
from textual.widgets.option_list import Option

##############################################################################
# Local imports.
from ..path_maker import MakePath


##############################################################################
class DriveEntry(Option):
    """A drive entry for the `DriveNavigation` class."""

    def __init__(self, drive: Path | str) -> None:
        """Initialise the object.

        Args:
            drive: The drive to handle.
        """
        self.drive_root: Path = MakePath.of(drive)
        """The drive root for this entry."""
        super().__init__(self.drive_root.drive, id=self.drive_root.drive)


##############################################################################
class DriveNavigation(OptionList):
    """A drive navigation widget.

    Provides a single-pane widget that lets the user select a drive. This is
    very useful in combination with the `DirectoryNavigation` widget. A dialog can
    reload that widget in response to drive selection changes.
    """

    DEFAULT_CSS = """
    DriveNavigation, DriveNavigation:focus {
        border: blank;
        border-right: $panel-darken-1;
        width: 10;
        height: 100%;
    }

    DriveNavigation > .option-list--option-highlighted {
        text-style: bold;
        color: white;
    }
    """
    """Default styling for the widget."""

    @dataclass
    class DriveSelected(Message):
        """Message sent when a drive is selected."""

        drive_root: Path
        """The selected drive root, like `c:\\`."""

    drive: var[str] = var[str](MakePath.of(".").absolute().drive, init=False)

    def __init__(self, location: Path | str = ".") -> None:
        """Initialise the drive navigation widget.

        Args:
            location: The starting location.
        """
        super().__init__()
        self.set_reactive(DriveNavigation.drive, MakePath.of(location).absolute().drive)
        if sys.platform == "win32":
            self._entries = [DriveEntry(drive) for drive in listdrives()]
        else:
            self._entries: list[DriveEntry] = []

    def on_mount(self) -> None:
        """Add available drives to the widget."""
        self.add_options(self._entries)
        self.highlight_drive(self.drive)

    def _watch_drive(self, drive: str) -> None:
        """Highlight the new drive.

        Args:
            drive: The new value of the current drive.
        """
        self.highlight_drive(drive)

    def highlight_drive(self, drive: str) -> None:
        """Highlight the given drive.

        Args:
            drive: The drive to be highlighted.
        """
        self.highlighted = self.get_option_index(drive.upper())

    @on(OptionList.OptionSelected)
    def drive_selected(self, event: OptionList.OptionSelected) -> None:
        """Post a DriveSelected message.

        Args:
            event: The drive selected event from the parent `OptionList`.
        """
        assert isinstance(event.option, DriveEntry)
        event.stop()
        self.drive = event.option.drive_root.drive
        self.post_message(self.DriveSelected(drive_root=event.option.drive_root))


### drive_navigation.py ends here
