"""Provides a file opening dialog."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Local imports.
from .base_dialog import ButtonLabel
from .file_dialog import BaseFileDialog
from .path_filters import Filters


##############################################################################
class FileOpen(BaseFileDialog):
    """A file opening dialog."""

    ERROR_A_FILE_MUST_EXIST = "The file must exist"
    """An error to show a user when a file must exist."""

    def __init__(
        self,
        location: str | Path = ".",
        title: str = "Open",
        *,
        open_button: ButtonLabel = "",
        cancel_button: ButtonLabel = "",
        filters: Filters | None = None,
        must_exist: bool = True,
        default_file: str | Path | None = None,
    ) -> None:
        """Initialise the `FileOpen` dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            open_button: The label for the open button.
            cancel_button: The label for the cancel button.
            filters: Optional filters to show in the dialog.
            must_exist: Flag to say if the file must exist.
            default_file: The default filename to place in the input.

        Notes:
            `open_button` and `cancel_button` can either be strings that
            set the button label, or they can be functions that take the
            default button label as a parameter and return the label to use.
        """
        super().__init__(
            location,
            title,
            select_button=self._label(open_button, "Open"),
            cancel_button=cancel_button,
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
            self._set_error(self.ERROR_A_FILE_MUST_EXIST)
            return False
        return True


### file_open.py ends here
