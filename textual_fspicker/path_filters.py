"""Code to handle the filters for the dialogs."""

##############################################################################
# Python imports.
from __future__        import annotations
from pathlib           import Path
from typing            import Callable, NamedTuple
from typing_extensions import TypeAlias

##############################################################################
FilterFunction: TypeAlias = Callable[ [ Path ], bool ]
"""Type of a path filter function."""

##############################################################################
class Filter( NamedTuple ):
    """A path filter."""

    name: str
    """The name of the filter."""

    tester: FilterFunction
    """The tester for the filter."""

    def __call__( self, path: Path ) -> bool:
        return self.tester( path )

##############################################################################
class Filters:
    """A path filter collection."""

    def __init__( self, *filters: Filter | tuple[ str, FilterFunction ] ) -> None:
        """Initialise the filter collection.

        Args:
            filters: The initial set of filters.
        """
        self._filters: list[ Filter ] = list(
            path_filter if isinstance( path_filter, Filter )
            else Filter( *path_filter )
            for path_filter in filters
        )

    @property
    def selections( self ) -> list[ tuple[ str, int ] ]:
        """Get the filters in a `Select`-friendly way."""
        return [
            ( file_filter.name, filter_id  )
            for filter_id, file_filter in enumerate( self._filters )
        ]

    def __getitem__( self, filter_id: int ) -> Filter:
        return self._filters[ filter_id ]

    def __bool__( self ) -> bool:
        return bool( self._filters )

### path_filters.py ends here
