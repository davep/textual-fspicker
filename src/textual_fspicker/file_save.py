"""Provides a file save dialog."""

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
class FileSave(BaseFileDialog):
    """A file save dialog."""

    ERROR_OVERWRITE_IS_NOT_ALLOWED = "Overwrite is not allowed"
    """The error to show if the user attempts to overwrite a file."""

    def __init__(
        self,
        location: str | Path = ".",
        title: str = "Save as",
        *,
        save_button: ButtonLabel = "",
        cancel_button: ButtonLabel = "",
        filters: Filters | None = None,
        can_overwrite: bool = True,
        default_file: str | Path | None = None,
        suggest_completions: bool = True,
    ) -> None:
        """Initialise the `FileSave` dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            save_button: The label for the save button.
            cancel_button: The label for the cancel button.
            filters: Optional filters to show in the dialog.
            can_overwrite: Flag to say if an existing file can be overwritten.
            default_file: The default filename to place in the input.
            suggest_completions: Should the `Input` suggest completions?

        Notes:
            `open_button` and `cancel_button` can either be strings that
            set the button label, or they can be functions that take the
            default button label as a parameter and return the label to use.
        """
        super().__init__(
            location,
            title,
            select_button=self._label(save_button, "Save"),
            cancel_button=cancel_button,
            filters=filters,
            default_file=default_file,
            suggest_completions=suggest_completions,
        )
        self._can_overwrite = can_overwrite
        """Can an existing file be overwritten?"""

    def _should_return(self, candidate: Path) -> bool:
        """Perform the final checks on the chosen file.

        Args:
            candidate: The file to check.

        Returns:
            [`True`][True] if the file checks out okay, [`False`][False] if
            not.
        """
        if candidate.exists() and not self._can_overwrite:
            self._set_error(self.ERROR_OVERWRITE_IS_NOT_ALLOWED)
            return False
        return True


### file_save.py ends here
