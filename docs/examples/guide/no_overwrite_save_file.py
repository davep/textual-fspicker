from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Button, Label

from textual_fspicker import FileSave


class DefaultSaveFileApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Press to save a file")
        yield Label()

    @on(Button.Pressed)
    @work
    async def save_a_file(self) -> None:
        if opened := await self.push_screen_wait(FileSave(can_overwrite=False)):
            self.query_one(Label).update(str(opened))


if __name__ == "__main__":
    DefaultSaveFileApp().run()
