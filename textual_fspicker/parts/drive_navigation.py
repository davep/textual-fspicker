"""Provides a widget for drive navigation."""

##############################################################################
# Python imports.
import os
import pathlib
import platform
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual import on
from textual.message import Message
from textual.widgets import OptionList


##############################################################################
class DriveNavigation(OptionList):
    """A drive navigation widget.

    Provides a single-pane widget that lets the user select a drive. This is
    very useful in combination with the DirectoryNavigation widget. A dialog can
    reload that widget in response to drive selection changes.
    """

    DEFAULT_CSS = """
    DriveNavigation, DriveNavigation:focus {
        border: blank;
        border-right: $panel-darken-1;
        width: 10;
        height: 100%;
    }
    """
    """Default styling for the widget."""

    @dataclass
    class DriveSelected(Message):
        """Message sent when a drive is selected."""

        drive_root: pathlib.Path
        """The selected drive root, like `c:\\`."""

    def on_mount(self) -> None:
        """Add available drives to the widget."""
        if platform.system() == "Windows":
            self.add_options(os.listdrives())

    @on(OptionList.OptionSelected)
    def select_drive(self, event: OptionList.OptionSelected) -> None:
        """Post a DriveSelected message.

        Args:
            event: the drive selected event from the parent OptionList.
        """
        self.post_message(
            self.DriveSelected(drive_root=pathlib.Path(str(event.option.prompt)))
        )


### drive_navigation.py ends here
