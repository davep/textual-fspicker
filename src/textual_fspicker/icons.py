"""Helper code for picking an 'icon' to display along with directory entries.

By default the library will display just two icons: either [a folder style
icon][textual_fspicker.icons.DEFAULT_FOLDER_ICON] next to directory entries,
or [a page style icon][textual_fspicker.icons.DEFAULT_FILE_ICON] next to
file entries.

In your application you may wish to use a richer set of icons, perhaps you
even want to make use of [Nerd Fonts](https://www.nerdfonts.com) or
something similar. The [`Icons`][textual_fspicker.icons.Icons] class lets
you override the icon-picking behaviour.
"""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path
from typing import Callable, Final

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Local imports.
from .safe_tests import is_dir

##############################################################################
# Default icons.
DEFAULT_FOLDER_ICON: Final[Text] = Text.from_markup(":file_folder:")
"""The default icon to use for a folder."""
DEFAULT_FILE_ICON: Final[Text] = Text.from_markup(":page_facing_up:")
"""The default icon to use for a file."""


##############################################################################
def _default_icon_picker(location: Path) -> Text:
    """The default icon picking function.

    Args:
        location: The location to pick an icon for.

    Returns:
        The icon as a Rich [`Text`][rich.text.Text] object.
    """
    return DEFAULT_FOLDER_ICON if is_dir(location) else DEFAULT_FILE_ICON


##############################################################################
class Icons:
    """Helper class for picking the best icon to use for a directory entry."""

    _picker: Callable[[Path], Text] = _default_icon_picker
    """The icon picking function."""

    @classmethod
    def set_picker(cls, icon_picker: Callable[[str | Path], Text]) -> None:
        """Set the function that will pick the best icon for a directory entry.

        Args:
            icon_picker: A function that will return a
                [Rich `Text`][rich.text.Text] object that is the best icon
                for a given directory entry.

        The given function should take a [`Path`][pathlib.Path] and return a
        [Rich `Text`][rich.text.Text] object that is an icon that can be
        used to represent that location. For example, given this function:

        ```python
        from pathlib import Path
        from rich.text import Text
        from textual_fspicker.icons import DEFAULT_FILE_ICON, DEFAULT_FOLDER_ICON
        from textual_fspicker.safe_tests import is_dir

        def my_icon_picker(location: Path) -> Text:
            if location.suffix.lower() == ".py":
                return Text.from_markup(":snake:")
            return DEFAULT_FOLDER_ICON if is_dir(location) else DEFAULT_FILE_ICON
        ```

        If the picker is set to it:

        ```python
        Icons.set_picker(my_icon_picker)
        ```

        Any subsequent use of
        [`Icon.best_for`][textual_fspicker.icons.Icons.best_for] will use a
        snake for any files with a `py` extension:

        ```python
        >>> Icons.best_for(".")
        📁
        >>> Icons.best_for("pyproject.toml")
        📄
        >>> Icons.best_for("src/textual_fspicker/__init__.py")
        🐍
        ```

        !!!important
            Remember to keep the code as fast as possible, as it will be
            called for every entry that is shown in one of the dialogs. Also
            remember to perform tests in the safest way possible (see
            [`safe_tests`][textual_fspicker.safe_tests] for example).
        """
        cls._picker = icon_picker

    @classmethod
    def best_for(cls, location: str | Path) -> Text:
        """Get the best icon for a given location.

        Args:
            location: The location to get an icon for.

        Returns:
            The chosen icon for the location.

        Example:
            ```
            >>> from textual_fspicker import Icons
            >>> Icons.best_for(".")
            📁
            >>> Icons.best_for("pyproject.toml")
            📄
            ```
        """
        return cls._picker(Path(location))


### icons.py ends here
