from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Button, Label

from textual_fspicker import FileOpen


class DefaultFileOpenApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Press to open a file")
        yield Label()

    @on(Button.Pressed)
    @work
    async def open_a_file(self) -> None:
        if opened := await self.push_screen_wait(FileOpen(default_file="README.md")):
            self.query_one(Label).update(str(opened))


if __name__ == "__main__":
    DefaultFileOpenApp().run()
