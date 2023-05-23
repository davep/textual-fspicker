"""Provides a file opening dialog."""

##############################################################################
# Python imports.
from __future__ import annotations
from pathlib    import Path

##############################################################################
# Local imports.
from .file_dialog  import BaseFileDialog
from .path_filters import Filters

##############################################################################
class FileOpen( BaseFileDialog ):
    """A file opening dialog."""

    def __init__(
        self,
        location: str | Path | None = None,
        title: str = "Open",
        *,
        filters: Filters | None = None,
        must_exist: bool = True
    ) -> None:
        """Initialise the `FileOpen` dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            must_exist: Flag to say if the file must exist.
            filters: Optional filters to show in the dialog.
        """
        super().__init__( location, title, select_button="Open", filters=filters )
        self._must_exist = must_exist
        """Must the file exist?"""

    def _should_return( self, candidate: Path ) -> bool:
        """Perform the final checks on the chosen file.

        Args:
            candidate: The file to check.
        """
        if self._must_exist and not candidate.exists():
            self._set_error( "The file must exist" )
            return False
        return True

### file_open.py ends here
