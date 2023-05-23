"""Base file-oriented dialog."""

##############################################################################
# Python imports.
from __future__ import annotations
from pathlib    import Path

##############################################################################
# Textual imports.
from textual         import on
from textual.app     import ComposeResult
from textual.widgets import Button,Input, Select

##############################################################################
# Local imports.
from .base_dialog  import FileSystemPickerScreen
from .parts        import DirectoryNavigation
from .path_filters import Filters

##############################################################################
class FileFilter( Select[ int ] ):
    """The file filter."""

##############################################################################
class BaseFileDialog( FileSystemPickerScreen ):
    """The base dialog for file-oriented picking dialogs."""

    DEFAULT_CSS = """
    BaseFileDialog InputBar Input {
        width: 2fr;
    }

    BaseFileDialog InputBar Select {
        width: 1fr;
    }
    """

    def __init__(
        self,
        location: str | Path | None = None,
        title: str = "Open",
        select_button: str = "",
        *,
        filters: Filters | None = None
    ) -> None:
        """Initialise the base dialog dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            filters: Optional filters to show in the dialog.
        """
        super().__init__( location, title, select_button=select_button )
        self._filters = filters
        """The filters for the dialog."""

    def _input_bar( self ) -> ComposeResult:
        """Provide any widgets for the input before, before the buttons."""
        yield Input()
        if self._filters:
            yield FileFilter(
                self._filters.selections,
                prompt      = "File filter",
                value       = 0,
                allow_blank = False
            )

    @on( DirectoryNavigation.Selected )
    def _select_file( self, event: DirectoryNavigation.Selected ) -> None:
        """Handle a file being selected in the picker.

        Args:
            event: The event to handle.
        """
        file_name       = self.query_one( Input )
        file_name.value = str( event.path.name )
        file_name.focus()

    @on( Input.Changed )
    def _clear_error( self ) -> None:
        """Clear any error that might be showing."""
        super()._clear_error()

    @on( Select.Changed )
    def _change_filter( self, event: Select.Changed ) -> None:
        """Handle a change in the filter.

        Args:
            event: The event to handle.
        """
        if self._filters is not None and isinstance( event.value, int ):
            self.query_one( DirectoryNavigation ).file_filter = self._filters[
                event.value
            ]
        else:
            self.query_one( DirectoryNavigation ).file_filter = None
        self.query_one( DirectoryNavigation ).focus()

    def _should_return( self, candidate: Path ) -> bool:
        """Final check on a picked file before returning it to the caller.

        Args:
            candidate: The file to check.

        Returns:
            `True` if the file should be returned, `False` if not.

        Note:
            This method is designed to be called as a final check; this is a
            good place to set up the display of an error before returning
            `False`, for example.
        """
        del candidate
        return True

    @on( Input.Submitted )
    @on( Button.Pressed, "#select" )
    def _confirm_file( self, event: Input.Submitted | Button.Pressed ) -> None:
        """Confirm the selection of the file in the input box.

        Args:
            event: The event to handle.
        """
        event.stop()
        file_name = self.query_one( Input )

        # Only even try and process this if there's some input.
        if not file_name.value:
            self._set_error( "A file must be chosen" )

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
        try:
            if chosen.is_dir():
                self.query_one( Input ).value                  = ""
                self.query_one( DirectoryNavigation ).location = chosen
                self.query_one( DirectoryNavigation ).focus()
                return
        except PermissionError:
            self._set_error( "Permission error" )
            return

        # If the chosen file passes the final tests...
        if self._should_return( chosen ):
            # ...return it.
            self.dismiss( result=chosen )

### file_dialog.py ends here
