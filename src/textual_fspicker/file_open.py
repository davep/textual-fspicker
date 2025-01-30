"""Provides a file opening dialog."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Local imports.
from .file_dialog import BaseFileDialog
from .path_filters import Filters


##############################################################################
class FileOpen(BaseFileDialog):
    """A file opening dialog."""

    def __init__(
        self,
        location: str | Path = ".",
        title: str = "Open",
        *,
        filters: Filters | None = None,
        must_exist: bool = True,
        default_file: str | Path | None = None,
    ) -> None:
        """Initialise the `FileOpen` dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            filters: Optional filters to show in the dialog.
            must_exist: Flag to say if the file must exist.
            default_file: The default filename to place in the input.
        """
        super().__init__(
            location,
            title,
            select_button="Open",
            filters=filters,
            default_file=default_file,
        )
        self._must_exist = must_exist
        """Must the file exist?"""

    def _should_return(self, candidate: Path) -> bool:
        """Perform the final checks on the chosen file.

        Args:
            candidate: The file to check.
        """
        if self._must_exist and not candidate.exists():
            self._set_error("The file must exist")
            return False
        return True


### file_open.py ends here
