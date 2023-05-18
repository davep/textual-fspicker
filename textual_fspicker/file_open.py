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
        border: panel $panel-lighten-2;
        background: $panel-lighten-1;
        border-title-color: $text;
        border-title-background: $panel-lighten-2;
        border-subtitle-color: $text;
        border-subtitle-background: $error;
    }

    FileOpen Horizontal#input {
        height: auto;
        align: right middle;
        padding-top: 1;
        padding-right: 1;
        padding-bottom: 1;
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

    def __init__( self, location: str | Path | None=None, title: str="Open", must_exist: bool=True ) -> None:
        """Initialise the `FileOpen` dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            must_exist: Flag to say if the file must exist.
        """
        super().__init__()
        self._location = location
        """The starting location."""
        self._title = title
        """The title for the dialog."""
        self._must_exist = must_exist
        """Must the file exist?"""

    def compose( self ) -> ComposeResult:
        """Compose the child widgets.

        Returns:
            The widgets to compose.
        """
        with Vertical( id="dialog" ) as dialog:
            dialog.border_title = self._title
            yield DirectoryNavigation(self._location)
            with Horizontal( id="input" ):
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
            chosen = self.query_one( DirectoryNavigation ).location / file_name.value
            if self._must_exist and not chosen.exists():
                self.query_one( "#dialog", Vertical ).border_subtitle = "The file must exist"
                return
            self.dismiss( result=chosen )

    @on( Button.Pressed, "#cancel" )
    def _cancel( self, event: Button.Pressed ) -> None:
        """Cancel the dialog.

        Args:
            event: The even to handle.
        """
        event.stop()
        self.dismiss()

    @on( Input.Changed )
    def _clear_error( self ) -> None:
        """Clear any error that might be showing."""
        self.query_one( "#dialog", Vertical ).border_subtitle = ""

### file_open.py ends here
