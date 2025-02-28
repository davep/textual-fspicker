from textual import work
from textual.app import App

from textual_fspicker import FileOpen


class OpenAFileApp(App[None]):
    @work
    async def on_mount(self) -> None:
        await self.push_screen_wait(FileOpen())


if __name__ == "__main__":
    OpenAFileApp().run()
