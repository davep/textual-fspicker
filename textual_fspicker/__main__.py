"""Main entry point for testing the library."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app     import App, ComposeResult
from textual.widgets import Label, Button

##############################################################################
# Local imports.
from textual_fspicker import FileOpen

##############################################################################
class TestApp( App[ None ] ):
    """A simple test application."""

    def compose( self ) -> ComposeResult:
        yield Label( "Press the button to pick something" )
        yield Button( "Select a file" )

    def show_selected( self, to_open: Path ) -> None:
        self.query_one( Label ).update( str( to_open ) )

    def on_button_pressed( self ):
        self.push_screen( FileOpen( "." ), callback=self.show_selected )

##############################################################################
if __name__ == "__main__":
    TestApp().run()

### __main__.py ends here
