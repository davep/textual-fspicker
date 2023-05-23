"""Provides a file save dialog."""

##############################################################################
# Python imports.
from __future__ import annotations
from pathlib    import Path

##############################################################################
# Local imports.
from .file_dialog  import BaseFileDialog
from .path_filters import Filters

##############################################################################
class FileSave( BaseFileDialog ):
    """A file save dialog."""

    def __init__(
        self,
        location: str | Path | None = None,
        title: str = "Save as",
        *,
        filters: Filters | None = None,
        can_overwrite: bool = True
    ) -> None:
        """Initialise the `FileOpen` dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            filters: Optional filters to show in the dialog.
            can_overwrite: Flag to say if an existing file can be overwritten.
        """
        super().__init__( location, title, select_button="Save", filters=filters )
        self._can_overwrite = can_overwrite
        """Can an existing file be overwritten?"""

    def _should_return( self, candidate: Path ) -> bool:
        """Perform the final checks on the chosen file.

        Args:
            candidate: The file to check.
        """
        if candidate.exists() and not self._can_overwrite:
            self._set_error( "Overwrite is not allowed" )
            return False
        return True

### file_save.py ends here
