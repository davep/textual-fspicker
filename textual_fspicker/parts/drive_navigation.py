"""Provides a widget for drive navigation."""

##############################################################################
# Python imports.
import os
import pathlib
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual import on
from textual.app import App, ComposeResult
from textual.message import Message
from textual.widgets import OptionList, Static


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
    """
    """Default styling for the widget."""

    @dataclass
    class DriveSelected(Message):
        """Message sent when a drive is selected."""

        drive_root: str
        """The selected drive root, like `c:\\`."""

    def on_mount(self) -> None:
        """Add available drives to the widget."""
        self.add_options(os.listdrives())

    @on(OptionList.OptionSelected)
    def select_drive(self, event: OptionList.OptionSelected) -> None:
        """Post a DriveSelected message.

        Args:
            event: The drive selected event from the parent `OptionList`.
        """
        self.post_message(self.DriveSelected(drive_root=event.option.prompt))


class TestApp(App[None]):
    """Simple test app for the DriveNavigation widget."""

    def compose(self) -> ComposeResult:
        yield DriveNavigation()
        yield Static("No drive selected", id="drive_contents")

    @on(DriveNavigation.DriveSelected)
    def show_drive_contents(self, event: DriveNavigation.DriveSelected) -> None:
        """Show selected drive contents.

        Args:
            event (DriveNavigation.DriveSelected): the event for the drive selection.
        """
        self.query_one("#drive_contents", Static).update(
            "\n".join([str(p) for p in pathlib.Path(event.drive_root).glob("*")])
        )


if __name__ == "__main__":
    TestApp().run()


### drive_navigation.py ends here
