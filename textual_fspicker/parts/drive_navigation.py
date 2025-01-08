import os
import pathlib
from dataclasses import dataclass

from textual import on
from textual.app import App, ComposeResult
from textual.message import Message
from textual.widgets import OptionList, Static


class DriveNavigation(OptionList):
    @dataclass
    class DriveSelected(Message):
        drive_root: str

    def on_mount(self) -> None:
        self.add_options(os.listdrives())

    @on(OptionList.OptionSelected)
    def select_drive(self, event: OptionList.OptionSelected) -> None:
        self.post_message(self.DriveSelected(drive_root=event.option.prompt))


class TestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield DriveNavigation()
        yield Static("No drive selected", id="drive_contents")

    @on(DriveNavigation.DriveSelected)
    def show_drive_contents(self, event: DriveNavigation.DriveSelected) -> None:
        self.query_one("#drive_contents", Static).update(
            "\n".join([str(p) for p in pathlib.Path(event.drive_root).glob("*")])
        )


if __name__ == "__main__":
    TestApp().run()
