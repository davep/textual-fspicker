"""Provides a file opening dialog."""

##############################################################################
# Python imports.
from __future__ import annotations
from pathlib    import Path

##############################################################################
# Textual imports.
from textual            import on
from textual.app        import ComposeResult
from textual.binding    import Binding
from textual.containers import Horizontal, Vertical
from textual.screen     import ModalScreen
from textual.widgets    import Button, Input

##############################################################################
# Local imports.
from .parts import DirectoryNavigation

##############################################################################
class FileOpen( ModalScreen[ Path ] ):
    """A file opening dialog."""

    DEFAULT_CSS = """
    FileOpen {
        align: center middle;
    }

    FileOpen > Vertical#dialog {
        width: 80%;
        height: 80%;
    }

    FileOpen Horizontal#input {
        height: auto;
        align: right middle;
    }

    FileOpen Horizontal#input Button {
        margin-left: 1;
    }

    FileOpen Horizontal#input Input {
        width: 1fr;
    }
    """

    BINDINGS = [
        Binding( "escape", "dismiss" ),
    ]
    """The bindings for the dialog."""

    def compose( self ) -> ComposeResult:
        """Compose the child widgets.

        Returns:
            The widgets to compose.
        """
        with Vertical( id="dialog" ):
            yield DirectoryNavigation()
            with Horizontal( id="input"):
                yield Input()
                yield Button( "Open", id="open" )
                yield Button( "Cancel", id="cancel" )

    @on( DirectoryNavigation.Selected )
    def _select_file( self, event: DirectoryNavigation.Selected ) -> None:
        """Handle a file being selected in the picker.

        Args:
            event: The event to handle.
        """
        file_name       = self.query_one( Input )
        file_name.value = str( event.path.name )
        file_name.focus()

    @on( Input.Submitted )
    @on( Button.Pressed, "#open" )
    def _confirm_file( self, event: Input.Submitted | Button.Pressed ) -> None:
        """Confirm the selection of the file in the input box.

        Args:
            event: The event to handle.
        """
        event.stop()
        file_name = self.query_one( Input )
        if file_name.value:
            self.dismiss( result=self.query_one( DirectoryNavigation ).location / file_name.value )

    @on( Button.Pressed, "#cancel" )
    def _cancel( self, event: Button.Pressed ) -> None:
        """Cancel the dialog.

        Args:
            event: The even to handle.
        """
        event.stop()
        self.dismiss()

### file_open.py ends here
