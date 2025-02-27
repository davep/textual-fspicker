from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Button, Label

from textual_fspicker import SelectDirectory


class BasicSelectDirectoryApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Press to select a directory")
        yield Label()

    @on(Button.Pressed)
    @work
    async def pick_a_directory(self) -> None:
        if opened := await self.push_screen_wait(SelectDirectory()):
            self.query_one(Label).update(str(opened))


if __name__ == "__main__":
    BasicSelectDirectoryApp().run()
