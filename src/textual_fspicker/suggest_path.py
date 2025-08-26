"""Provides a suggester for paths."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from os import sep
from pathlib import Path

##############################################################################
# Textual imports.
from textual.suggester import Suggester


##############################################################################
class SuggestPath(Suggester):
    """A textual `Input` suggester that suggests a path."""

    def __init__(self, *, root: str | Path = ".") -> None:
        """Initialise the suggester

        Args:
            root: The root directory to work from.

        """
        super().__init__(use_cache=False, case_sensitive=True)
        self.root = Path(root)
        """The root directory to work from when taking suggestions."""

    async def get_suggestion(self, value: str) -> str | None:
        """Get suggestions for the given value.

        Args:
            value: The value to make a suggestion for.

        Returns:
            A suggested completion, or `None` if none could be made.
        """

        # We're going to work with this as a Path.
        path = self.root / value

        # If the value, turned into a path, exists in some capacity, there's
        # nothing to suggest; the user has typed in a thing that exists.
        if path.exists():
            return value

        try:
            suggestion = next(self.root.glob(f"{value}*"), None)
            return str(suggestion).removeprefix(f"{self.root}/") if suggestion else ""
        except NotImplementedError:
            # If we get a NotImplementedError, the most likely reason is
            # that the user has typed in an absolute path of some
            # description. So here we give up on trying to find something
            # relative to self.root and instead treat the whole input in
            # isolation.
            if (input_path := Path(value)).exists():
                return value
            # Note that while `os.sep` isn't the ideal test here, we use it
            # to try and handle an annoying case we run into because the
            # `stem` of a path isn't the file, but the last part of the
            # part. So if we have a pure directory we've got no useful way
            # of deciding on how to glob things. So this cleans up a rare
            # but annoying bad suggestion.
            suggestion = (
                input_path
                if value.endswith(sep)
                else next(input_path.parent.glob(f"{input_path.stem}*"), None)
            )
            return str(suggestion or value)


### suggest_path.py ends here
