from textual import work
from textual.app import App
from textual.widgets import Label

from textual_fspicker import FileOpen, Filters


class BasicFileOpenApp(App[None]):
    CSS = """
    FileOpen Dialog {
        height: 50%;
    }
    """

    @work
    async def on_mount(self) -> None:
        if opened := await self.push_screen_wait(
            FileOpen(
                filters=Filters(
                    ("Python", lambda p: p.suffix.lower() == ".py"),
                    ("Markdown", lambda p: p.suffix.lower() == ".md"),
                    ("TOML", lambda p: p.suffix.lower() == ".toml"),
                    ("YAML", lambda p: p.suffix.lower() == ".yml"),
                    ("All", lambda _: True),
                )
            )
        ):
            self.query_one(Label).update(str(opened))


if __name__ == "__main__":
    BasicFileOpenApp().run()
