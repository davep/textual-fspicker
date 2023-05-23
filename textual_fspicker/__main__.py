"""Main entry point for testing the library."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual            import on
from textual.app        import App, ComposeResult
from textual.containers import Center, Horizontal
from textual.widgets    import Label, Button

##############################################################################
# Local imports.
from textual_fspicker import FileOpen, FileSave, Filters, SelectDirectory

##############################################################################
class TestApp( App[ None ] ):
    """A simple test application."""

    CSS = """
    Screen#_default {
        align: center middle;
    }

    Screen#_default Horizontal {
        align: center middle;
        height: auto;
        margin-bottom: 1;
    }

    Screen#_default Horizontal Button {
        margin-left: 1;
        margin-right: 1;
    }
    """

    def compose( self ) -> ComposeResult:
        """Compose the layout of the test application."""
        with Horizontal():
            yield Button( "Open a file", id="open" )
            yield Button( "Save a file", id="save" )
            yield Button( "Select a directory", id="directory" )
        with Center():
            yield Label( "Press the button to pick something" )

    def show_selected( self, to_show: Path ) -> None:
        """Show the file that was selected by the user.

        Args:
            to_show: The file to show.
        """
        self.query_one( Label ).update( str( to_show ) )

    @on( Button.Pressed, "#open" )
    def open_file( self ) -> None:
        """Show the `FileOpen` dialog when the button is pushed."""
        self.push_screen(
            FileOpen( ".", filters=Filters(
                ( "Any",     lambda _: True ),
                ( "Emacs",   lambda p: p.suffix.lower() == ".el" ),
                ( "Lisp",    lambda p: p.suffix.lower() in ( ".lisp", ".lsp", ".cl" ) ),
                ( "Python",  lambda p: p.suffix.lower() == ".py" ),
                ( "Pascal",  lambda p: p.suffix.lower() == ".pas" ),
                ( "Clipper", lambda p: p.suffix.lower() in ( ".prg", ".ch" ) ),
                ( "C",       lambda p: p.suffix.lower() in ( ".c", ".h" ) ),
                ( "C++",     lambda p: p.suffix.lower() in ( ".cpp", ".cc", ".h" ) ),
            ) ),
            callback=self.show_selected
        )

    @on( Button.Pressed, "#save" )
    def save_file( self ) -> None:
        """Show the `FileSave` dialog when the button is pushed."""
        self.push_screen( FileSave(can_overwrite=False), callback=self.show_selected)

    @on( Button.Pressed, "#directory" )
    def select_directory( self ) -> None:
        """show the `SelectDirectory` dialog when the button is pushed."""
        self.push_screen( SelectDirectory(), callback=self.show_selected )

##############################################################################
if __name__ == "__main__":
    TestApp().run()

### __main__.py ends here
