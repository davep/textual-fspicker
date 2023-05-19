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
        Binding( "full_stop", "hidden")
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

    def _set_error( self, message: str="" ) -> None:
        """Set or clear the error message.

        Args:
            message: Optional message to show as an error.
        """
        self.query_one( "#dialog", Vertical ).border_subtitle = message

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

        # Only even try and process this if there's some input.
        if file_name.value:

            # If it looks like the user is typing in some sort of home
            # directory path... (does pathlib let me test for this, or at
            # least ask what the home character is? Docs don't mention this;
            # so for now I'm going to hard-code this).
            if file_name.value.startswith( "~" ):
                # ...let's simply expand and go with that.
                try:
                    chosen = Path( file_name.value ).expanduser()
                except RuntimeError as error:
                    self._set_error( str( error ) )
                    return
            else:
                # It's not a home directory path, so let's combine with the
                # location of the directory navigator widget.
                chosen = (
                    self.query_one( DirectoryNavigation ).location / file_name.value
                ).resolve()

            # If it's a directory, approach it like it's the user simply
            # doing a "cd".
            if chosen.is_dir():
                self.query_one( Input ).value                  = ""
                self.query_one( DirectoryNavigation ).location = chosen
                return

            # At this point it's something that can be picked. Do the "must
            # exist" test if needed.
            if self._must_exist and not chosen.exists():
                self._set_error( "The file must exist" )
                return

            # Finally, we've got some sort of pickable item and it's good to
            # be picked. Let's go with it.
            self.dismiss( result=chosen )

        else:
            self._set_error( "A file must be chosen" )

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
        self._set_error()

    def action_hidden( self ) -> None:
        """Action for toggling the display of hidden files."""
        self.query_one( DirectoryNavigation ).toggle_hidden()

### file_open.py ends here
