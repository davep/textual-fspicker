from textual.app import App, ComposeResult

from textual_fspicker.parts.directory_navigation import DirectoryNavigation

class TestApp( App[ None ] ):

    CSS = """
    DirectoryNavigation {
        border: thick cornflowerblue;
    }
    """

    def compose( self ) -> ComposeResult:
        yield DirectoryNavigation()

    def on_directory_navigation_changed( self, event: DirectoryNavigation.Changed ) -> None:
        self.query_one( DirectoryNavigation ).border_title = str( event.location )

if __name__ == "__main__":
    TestApp().run()
