from pathlib import Path

from textual.app     import App, ComposeResult
from textual.widgets import Label, Button

from textual_fspicker.file_open import FileOpen

class TestApp( App[ None ] ):

    def compose( self ) -> ComposeResult:
        yield Label( "Press the button to pick something" )
        yield Button( "Select a file" )

    def _open_file( self, to_open: Path ) -> None:
        self.query_one( Label ).update( str( to_open ) )

    def on_button_pressed( self ):
        self.push_screen( FileOpen("."), callback=self._open_file )

if __name__ == "__main__":
    TestApp().run()
