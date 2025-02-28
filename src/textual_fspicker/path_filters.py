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
        """Get the filters in a [`Select`][textual.widgets.Select]-friendly way."""
        return [
            (file_filter.name, filter_id)
            for filter_id, file_filter in enumerate(self._filters)
        ]

    def __getitem__(self, filter_id: int) -> Filter:
        return self._filters[filter_id]

    def __bool__(self) -> bool:
        return bool(self._filters)


### path_filters.py ends here
