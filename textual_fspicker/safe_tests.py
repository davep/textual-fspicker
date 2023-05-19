"""Support functions for doing safe filesystem tests.

This module provides some functions for performing tests on entries in the
filesystem in a way that swallows some errors that we don't want causing the
application to crash on. In most cases this is going to be a
PermissionError, which for UI stuff is better ignored than raised.
"""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
def is_dir( location: Path ) -> bool:
    """A safe version of is_dir.

    Args:
        location: The location to test.

    Returns:
        `True` if the location looks like a directory, `False` if not, or if
        it could not be determined.

    Note:
        This function swallows `PermissionError` and just returns that the
        location isn't a directory.
    """
    try:
        return location.is_dir()
    except PermissionError:
        return False

##############################################################################
def is_file( location: Path ) -> bool:
    """A safe version of is_file.

    Args:
        location: The location to test.

    Returns:
        `True` if the location looks like a file or if it could not be
        determined, `False` it can be known it doesn't look like a file.

    Note:
        This function swallows `PermissionError` and just returns that the
        location is a file.
    """
    try:
        return location.is_file()
    except PermissionError:
        return True

##############################################################################
def is_symlink( location: Path ) -> bool:
    """A safe version of is_symlink.

    Args:
        location: The location to test.

    Returns:
        `True` if the location looks like a symlink, `False` if not, or if
        it could not be determined.

    Note:
        This function swallows `PermissionError` and just returns that the
        location isn't a symlink.
    """
    try:
        return location.is_symlink()
    except PermissionError:
        return False

### safe_tests.py ends here
