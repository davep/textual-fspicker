"""Helper code for making a fresh [`Path`][pathlib.Path] instance.

Allows the user of the library to specify their preference for the Path
class to use when making a fresh [Path][pathlib.Path] instance. Designed to
allow the use of other Path-derived classes, such as
[UPath](https://github.com/fsspec/universal_pathlib), without needing to
make them dependencies of this library.
"""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path
from typing import Callable


##############################################################################
class MakePath:
    """Utility class for setting and getting the [`Path`][pathlib.Path] builder."""

    _path: Callable[[str | Path], Path] = Path
    """The callable to use to make a [`Path`][pathlib.Path]."""

    @classmethod
    def using(cls, path_maker: Callable[[str | Path], Path]) -> None:
        """Set the builder callable to use when making a path.

        Args:
            path_maker: The [callable][typing.Callable] to set as the
                [`Path`][pathlib.Path] builder.
        """
        cls._path = path_maker

    @classmethod
    def of(cls, out_of: str | Path = "") -> Path:  # pylint:disable=invalid-name
        """Make a Path out of the given value.

        Args:
            out_of: The value to make a path out of.

        Returns:
            An instance of a [`Path`][pathlib.Path] or a related class.
        """
        return cls._path(out_of)


### path_maker.py ends here
