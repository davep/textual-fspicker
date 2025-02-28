"""Code to handle the filters for the dialogs."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path
from typing import Callable, NamedTuple

##############################################################################
# Typing extension imports.
from typing_extensions import TypeAlias

##############################################################################
FilterFunction: TypeAlias = Callable[[Path], bool]
"""Type of a path filter function."""


##############################################################################
class Filter(NamedTuple):
    """A path filter."""

    name: str
    """The name of the filter.

    This is the text that will be presented to the user in the filtering
    dropdown widget inside any dialog
    """

    tester: FilterFunction
    """The test function for the filter.

    This is the function that will be called to test of a particular
    [`Path`][pathlib.Path] passes the filter.
    """

    def __call__(self, path: Path) -> bool:
        """Test the given path to see if it passes the filter.

        Args:
            path: The [`Path`][pathlib.Path] to test.

        Returns:
            [`True`][True] if the [`Path`][pathlib.Path] passes the filter
                condition, [`False`][False] if not.
        """
        return self.tester(path)


##############################################################################
class Filters:
    """A path filter collection."""

    def __init__(self, *filters: Filter | tuple[str, FilterFunction]) -> None:
        """Initialise the filter collection.

        Args:
            filters: The initial set of filters.
        """
        self._filters: list[Filter] = list(
            path_filter if isinstance(path_filter, Filter) else Filter(*path_filter)
            for path_filter in filters
        )

    @property
    def selections(self) -> list[tuple[str, int]]:
        """The filters in a [`Select`][textual.widgets.Select]-friendly form."""
        return [
            (file_filter.name, filter_id)
            for filter_id, file_filter in enumerate(self._filters)
        ]

    def __getitem__(self, filter_id: int) -> Filter:
        """Get a filter given its numeric ID.

        Args:
            filter_id: The numeric ID for the filter.

        Returns:
            The filter with that ID.

        This is intended to be used in conjunction with
        [`selections`][textual_fspicker.Filters.selections]; where the
        return value for that will include a numeric ID for each filter that
        can be used with a [Textual `Select`
        widget][textual.widgets.Select].
        """
        return self._filters[filter_id]

    def __bool__(self) -> bool:
        """Are there any filters?

        Returns:
            [`True`][True] if there are any filters in the filer collection, [`False`][False] if not.
        """
        return bool(self._filters)


### path_filters.py ends here
