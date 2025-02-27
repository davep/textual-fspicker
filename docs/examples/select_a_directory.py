from textual import work
from textual.app import App

from textual_fspicker import SelectDirectory


class SelectADirectoryApp(App[None]):
    @work
    async def on_mount(self) -> None:
        await self.push_screen_wait(SelectDirectory())


if __name__ == "__main__":
    SelectADirectoryApp().run()
