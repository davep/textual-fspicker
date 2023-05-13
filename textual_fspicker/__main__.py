from textual.app     import App, ComposeResult
from textual.binding import Binding

from textual_fspicker.parts.directory_navigation import DirectoryNavigation

class TestApp( App[ None ] ):

    CSS = """
    DirectoryNavigation {
        border: thick cornflowerblue;
    }
    """

    BINDINGS = [
        Binding( "h", "toggle_hidden", "Toggle Hidden" ),
        Binding( "s", "toggle_sort", "Toggle Sorting" )
    ]


    def compose( self ) -> ComposeResult:
        yield DirectoryNavigation( "~" )

    def on_directory_navigation_changed( self, event: DirectoryNavigation.Changed ) -> None:
        self.query_one( DirectoryNavigation ).border_title = str( event.control.location )

    def action_toggle_hidden( self ) -> None:
        self.query_one( DirectoryNavigation ).toggle_hidden()

    def action_toggle_sort( self ) -> None:
        nav = self.query_one( DirectoryNavigation )
        nav.sort_display = not nav.sort_display

if __name__ == "__main__":
    TestApp().run()
