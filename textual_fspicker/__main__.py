"""Main entry point for testing the library."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app        import App, ComposeResult
from textual.containers import Center
from textual.widgets    import Label, Button

##############################################################################
# Local imports.
from textual_fspicker import FileOpen, Filters

##############################################################################
class TestApp( App[ None ] ):
    """A simple test application."""

    CSS = """
    Screen#_default {
        align: center middle;
    }

    Screen#_default Button {
        margin-bottom: 2;
    }
    """

    def compose( self ) -> ComposeResult:
        """Compose the layout of the test application."""
        with Center():
            yield Button( "Select a file" )
        with Center():
            yield Label( "Press the button to pick something" )

    def show_selected( self, to_show: Path ) -> None:
        """Show the file that was selected by the user.

        Args:
            to_show: The file to show.
        """
        self.query_one( Label ).update( str( to_show ) )

    def on_button_pressed( self ) -> None:
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

##############################################################################
if __name__ == "__main__":
    TestApp().run()

### __main__.py ends here
