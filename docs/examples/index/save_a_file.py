from textual import work
from textual.app import App

from textual_fspicker import FileSave


class SaveAFileApp(App[None]):
    @work
    async def on_mount(self) -> None:
        await self.push_screen_wait(FileSave())


if __name__ == "__main__":
    SaveAFileApp().run()
